#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""本機預覽 + 原始碼編輯伺服器。

用法：

    python3 turkey/scripts/dev.py                 # 自動開瀏覽器
    python3 turkey/scripts/dev.py --autocommit    # 存檔停 3 秒後自動 git commit
    python3 turkey/scripts/dev.py --port 9000 --no-open

預設 port 8770；若被佔用會自動往上找下一個可用的，並在啟動訊息裡印出實際用的 port
（**要看啟動訊息印的網址，不要憑記憶輸入 port**）。

兩個頁面：

    /__edit                左邊原始碼、右邊即時預覽，Cmd+S 存檔（**主要工作畫面**）
    /turkey/index.html     只有預覽

改任何 .html / .md / 圖片存檔後預覽會自動重新載入，並保留原本展開的日卡與捲動位置。
重新載入用的程式碼是這支腳本即時注入的，**不會寫進檔案**，隨時可以直接 commit。
"""

import argparse
import functools
import hashlib
import http.server
import json
import os
import subprocess
import threading
import time
import urllib.parse
import webbrowser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WATCH_SUFFIX = {".html", ".md", ".css", ".js", ".json", ".jpg", ".jpeg", ".png", ".webp", ".svg"}
EDITABLE_SUFFIX = {".html", ".htm", ".md", ".css", ".js", ".json", ".txt"}
SKIP_DIR = {".git", "node_modules", ".playwright-mcp", "__pycache__"}
DEFAULT_FILE = "turkey/index.html"

# ───────────────────────── 注入到預覽頁的程式碼 ─────────────────────────

RELOAD_JS = """
<script>
/* ── 本機預覽用，由 turkey/scripts/dev.py 即時注入，不存在於原始檔 ── */
(function(){
  var KEY = '__dev_view_state';

  try {
    var st = JSON.parse(sessionStorage.getItem(KEY) || 'null');
    if (st) {
      sessionStorage.removeItem(KEY);
      (st.open || []).forEach(function(d){
        var el = document.querySelector('.day[data-day="' + d + '"]');
        if (!el) return;
        el.classList.add('open');
        var w = el.querySelector('.day-wrap');
        if (w) w.style.maxHeight = 'none';   /* 不跑動畫，避免跟還原捲動位置打架 */
      });
      var y = st.y || 0;
      window.scrollTo(0, y);
      requestAnimationFrame(function(){ window.scrollTo(0, y); });
      setTimeout(function(){ window.scrollTo(0, y); }, 150);
    }
  } catch (e) {}

  function saveState(){
    try {
      var open = [].map.call(document.querySelectorAll('.day.open'), function(el){
        return el.getAttribute('data-day');
      });
      sessionStorage.setItem(KEY, JSON.stringify({ y: window.scrollY, open: open }));
    } catch (e) {}
  }

  var inFrame = false;
  try { inFrame = window.parent !== window; } catch (e) {}
  var setBadge = function(){};

  if (!inFrame) {
    var badge = document.createElement('div');
    badge.style.cssText = 'position:fixed;left:10px;bottom:calc(env(safe-area-inset-bottom,0px) + 10px);'
      + 'z-index:9999;font:11px/1 -apple-system,BlinkMacSystemFont,sans-serif;letter-spacing:.12em;'
      + 'padding:6px 9px;border-radius:999px;background:rgba(13,59,102,.72);color:#fff;pointer-events:none';
    badge.textContent = 'LIVE';
    document.addEventListener('DOMContentLoaded', function(){ document.body.appendChild(badge); });
    setBadge = function(t){ badge.textContent = t; };
  } else {
    /* 在編輯器裡：點預覽的文字 → 通知外層跳到原始碼對應位置 */
    document.addEventListener('click', function(e){
      var t = e.target;
      if (t.closest && t.closest('a')) return;          /* 連結照常運作 */
      /* 只有一個子元素、文字又完全相同時，往下鑽到真正帶文字的那層 */
      while (t.children && t.children.length === 1 && t.textContent === t.children[0].textContent) {
        t = t.children[0];
      }
      /* 有子元素的話只取「直屬的文字節點」，避免把整張卡的文字串成一長條 */
      var txt = '';
      if (t.children && t.children.length) {
        for (var i = 0; i < t.childNodes.length; i++) {
          if (t.childNodes[i].nodeType === 3) txt += t.childNodes[i].textContent;
        }
      }
      if (!txt.trim()) txt = t.textContent || '';
      txt = txt.replace(/\\s+/g, ' ').trim();
      if (txt) window.parent.postMessage({ __devFind: txt.slice(0, 120) }, '*');
    }, true);
  }

  var known = null;
  function poll(){
    fetch('/__ver', { cache: 'no-store' })
      .then(function(r){ return r.text(); })
      .then(function(v){
        if (known === null) { known = v; }
        else if (v !== known) { setBadge('RELOAD'); saveState(); location.reload(); return; }
        setTimeout(poll, 400);
      })
      .catch(function(){ setBadge('OFFLINE'); setTimeout(poll, 1500); });
  }
  poll();
})();
</script>
"""

# ───────────────────────────── 編輯器頁面 ─────────────────────────────

EDITOR_HTML = """<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>編輯 __FILE__</title>
<style>
:root{--bg:#12151b;--panel:#191d26;--line:#2a3140;--ink:#dbe2ef;--mute:#7c889c;
  --acc:#4a9eff;--ok:#3ec98a;--warn:#e8b93f}
*{box-sizing:border-box}
html,body{margin:0;height:100%;overflow:hidden;background:var(--bg);color:var(--ink);
  font:14px/1.5 -apple-system,BlinkMacSystemFont,"SF Pro Text","PingFang TC",sans-serif}
#bar{display:flex;align-items:center;gap:10px;height:46px;padding:0 12px;
  background:var(--panel);border-bottom:1px solid var(--line);flex:none}
#bar b{font-weight:600;font-size:13px}
#bar .sp{flex:1}
select,button,input{font:inherit;color:var(--ink);background:#232a36;border:1px solid var(--line);
  border-radius:7px;padding:6px 10px;outline:none}
button{cursor:pointer}
button:hover{border-color:var(--acc)}
button.primary{background:var(--acc);border-color:var(--acc);color:#08101c;font-weight:600}
button.primary:disabled{opacity:.4;cursor:default}
#find{width:220px}
#stat{font-size:12.5px;color:var(--mute);min-width:104px;text-align:right;font-variant-numeric:tabular-nums}
#stat.ok{color:var(--ok)}
#stat.dirty{color:var(--warn)}
#split{display:flex;height:calc(100% - 46px)}
#left{width:52%;min-width:280px;display:flex;flex-direction:column;position:relative}
#gutter{width:6px;cursor:col-resize;background:var(--line);flex:none}
#gutter:hover{background:var(--acc)}
#right{flex:1;min-width:280px;background:#fff}
#right iframe{width:100%;height:100%;border:0;display:block}
#src{flex:1;width:100%;resize:none;border:0;border-radius:0;padding:14px 14px 40px;
  background:#0e1116;color:#cbd5e6;tab-size:2;
  font:12.5px/1.75 ui-monospace,SFMono-Regular,Menlo,monospace;white-space:pre;overflow:auto}
#hint{position:absolute;left:0;right:0;bottom:0;padding:5px 12px;background:var(--panel);
  border-top:1px solid var(--line);font-size:11.5px;color:var(--mute);
  white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
</style>
</head>
<body>
<div id="bar">
  <b>__FILE__</b>
  <button id="save" class="primary" disabled>儲存 &#8984;S</button>
  <span id="stat">載入中…</span>
  <span class="sp"></span>
  <input id="find" placeholder="搜尋原始碼（Enter 找下一個）">
  <select id="pick">__OPTIONS__</select>
  <button id="open">預覽開新分頁</button>
</div>
<div id="split">
  <div id="left">
    <textarea id="src" spellcheck="false" wrap="off"></textarea>
    <div id="hint">點右邊預覽的任何文字 → 左邊自動跳到原始碼那一行</div>
  </div>
  <div id="gutter"></div>
  <div id="right"><iframe id="pv" src="__PREVIEW__"></iframe></div>
</div>

<script>
var FILE = "__FILE__", PREVIEW = "__PREVIEW__";
var src = document.getElementById('src'), stat = document.getElementById('stat'),
    saveBtn = document.getElementById('save'), hint = document.getElementById('hint');
var saved = null;

function setStat(t, cls){ stat.textContent = t; stat.className = cls || ''; }
function isDirty(){ return saved !== null && src.value !== saved; }
function sync(){
  var d = isDirty();
  saveBtn.disabled = !d;
  setStat(d ? '未儲存' : '已同步', d ? 'dirty' : 'ok');
}

var stamp = null;                     /* 載入當下的檔案指紋 */

function load(){
  return fetch('/__raw?f=' + encodeURIComponent(FILE))
    .then(function(r){ stamp = r.headers.get('X-Stamp'); return r.text(); })
    .then(function(t){ src.value = saved = t; sync(); })
    .catch(function(e){ setStat('讀取失敗', 'dirty'); hint.textContent = String(e); });
}
load();

/* 檔案在外部被改過（例如 Claude 動了它）就提醒，不要等到存檔才發現 */
function watchOutside(){
  if (isDirty()) return;              /* 自己有未存的修改時不自動覆蓋 */
  fetch('/__stamp?f=' + encodeURIComponent(FILE), { cache: 'no-store' })
    .then(function(r){ return r.text(); })
    .then(function(now){
      if (now && stamp && now !== stamp) {
        hint.textContent = '檔案在外部被改過，已自動重新載入';
        load();
      }
    }).catch(function(){});
}
setInterval(watchOutside, 2000);

var pendingForce = false;
function save(){
  if (!isDirty()) return;
  var body = src.value, force = pendingForce;
  pendingForce = false;
  setStat('儲存中…');
  fetch('/__save', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ f: FILE, text: body, stamp: stamp, force: force })
  }).then(function(r){ return r.json(); })
    .then(function(res){
      if (res.ok) { saved = body; stamp = res.stamp; sync(); setStat('已儲存', 'ok'); return; }
      if (res.stale) {
        setStat('有衝突', 'dirty');
        hint.textContent = '檔案在你編輯的期間被改過。按「重新載入」拿最新版（你這邊未存的修改會消失），'
          + '或按「強制覆蓋」用你這份蓋掉。';
        if (confirm('這個檔案在你編輯的期間被別人／其他程式改過了。\n\n'
                  + '按「確定」＝重新載入最新版（丟掉你未儲存的修改）\n'
                  + '按「取消」＝保留你的版本，之後可再按一次儲存強制覆蓋')) {
          load(); setStat('已重新載入', 'ok');
        } else {
          pendingForce = true;
          hint.textContent = '已保留你的版本。再按一次儲存就會強制覆蓋。';
        }
        return;
      }
      setStat('失敗', 'dirty'); hint.textContent = '儲存失敗：' + (res.error || '?');
    })
    .catch(function(e){ setStat('失敗', 'dirty'); hint.textContent = '儲存失敗：' + e; });
}
saveBtn.addEventListener('click', save);
src.addEventListener('input', sync);
document.addEventListener('keydown', function(e){
  if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 's') { e.preventDefault(); save(); }
});
window.addEventListener('beforeunload', function(e){
  if (isDirty()) { e.preventDefault(); e.returnValue = ''; }
});

/* ── 搜尋並選取 ── */
function reveal(idx, len){
  if (idx < 0) return false;
  src.focus();
  src.setSelectionRange(idx, idx + len);
  var line = src.value.slice(0, idx).split('\\n').length - 1;
  var lh = parseFloat(getComputedStyle(src).lineHeight) || 22;
  src.scrollTop = Math.max(0, line * lh - src.clientHeight / 2);
  return true;
}
var findBox = document.getElementById('find');
findBox.addEventListener('keydown', function(e){
  if (e.key !== 'Enter') return;
  var q = findBox.value;
  if (!q) return;
  var i = src.value.indexOf(q, src.selectionEnd || 0);
  if (i < 0) i = src.value.indexOf(q);      /* 繞回開頭 */
  hint.textContent = reveal(i, q.length) ? ('找到「' + q + '」') : ('找不到：' + q);
});

/* ── 點預覽 → 跳到原始碼 ── */
window.addEventListener('message', function(ev){
  var q = ev.data && ev.data.__devFind;
  if (!q) return;
  /* 渲染後的文字可能被 <strong> 切開、或整張卡串成一條，所以準備多組候選字串 */
  var cand = [q];
  q.split(/[。，、；：·|—]|\\s{2,}|→/).forEach(function(seg){
    seg = seg.trim();
    if (seg.length >= 5) cand.push(seg);
  });
  for (var n = q.length; n >= 6; n -= 3) cand.push(q.slice(0, n));
  /* 長的先試，比較不會誤中 */
  cand.sort(function(a, b){ return b.length - a.length; });
  for (var k = 0; k < cand.length; k++) {
    var i = src.value.indexOf(cand[k]);
    if (i >= 0) { reveal(i, cand[k].length); hint.textContent = '跳到：' + cand[k].slice(0, 50); return; }
  }
  hint.textContent = '原始碼裡找不到：' + q.slice(0, 40);
});

document.getElementById('pick').addEventListener('change', function(){
  if (isDirty() && !confirm('有未儲存的修改，要放棄嗎？')) { this.value = FILE; return; }
  location.href = '/__edit?f=' + encodeURIComponent(this.value);
});
document.getElementById('open').addEventListener('click', function(){ window.open(PREVIEW, '_blank'); });

/* ── 拖拉分隔線 ── */
(function(){
  var g = document.getElementById('gutter'), left = document.getElementById('left'), drag = false;
  g.addEventListener('mousedown', function(e){ drag = true; e.preventDefault(); document.body.style.cursor = 'col-resize'; });
  window.addEventListener('mouseup', function(){ drag = false; document.body.style.cursor = ''; });
  window.addEventListener('mousemove', function(e){
    if (!drag) return;
    var pct = Math.min(80, Math.max(20, e.clientX / window.innerWidth * 100));
    left.style.width = pct + '%';
  });
})();
</script>
</body>
</html>
"""

# ───────────────────────────────── 伺服器 ─────────────────────────────────


def version() -> str:
    """把所有被監看檔案的 (相對路徑, mtime, size) 壓成一個字串。"""
    h = hashlib.sha1()
    for base, dirs, files in os.walk(ROOT):
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIR and not d.startswith("."))
        for name in sorted(files):
            if Path(name).suffix.lower() not in WATCH_SUFFIX:
                continue
            fp = Path(base) / name
            try:
                st = fp.stat()
            except OSError:
                continue
            h.update(str(fp.relative_to(ROOT)).encode())
            h.update(b"%d:%d" % (int(st.st_mtime_ns), st.st_size))
    return h.hexdigest()


def editable_files():
    out = []
    for base, dirs, files in os.walk(ROOT):
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIR and not d.startswith("."))
        for name in sorted(files):
            if Path(name).suffix.lower() in EDITABLE_SUFFIX:
                out.append(str((Path(base) / name).relative_to(ROOT)))
    return sorted(out)


def file_stamp(fp: Path) -> str:
    """檔案內容的指紋，用來偵測「載入之後有沒有被別人改過」。"""
    return hashlib.sha1(fp.read_bytes()).hexdigest()


def resolve_editable(rel: str) -> Path:
    """把相對路徑解成 ROOT 底下的實體檔案，擋掉跳出專案目錄與不該編輯的檔案。"""
    fp = (ROOT / rel.lstrip("/")).resolve()
    if not str(fp).startswith(str(ROOT) + os.sep):
        raise ValueError("路徑超出專案目錄")
    if fp.suffix.lower() not in EDITABLE_SUFFIX:
        raise ValueError("不是可編輯的檔案類型：%s" % fp.suffix)
    if not fp.is_file():
        raise ValueError("檔案不存在")
    return fp


class Handler(http.server.SimpleHTTPRequestHandler):
    def _send(self, body: bytes, ctype: str, code: int = 200):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _json(self, obj, code: int = 200):
        self._send(json.dumps(obj, ensure_ascii=False).encode(),
                   "application/json; charset=utf-8", code)

    def do_GET(self):  # noqa: N802
        path = self.path.split("?")[0]
        qs = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)

        if path == "/__ver":
            return self._send(version().encode(), "text/plain; charset=utf-8")

        if path == "/favicon.ico":
            self.send_response(204)
            self.send_header("Content-Length", "0")
            self.end_headers()
            return

        if path == "/__stamp":
            try:
                fp = resolve_editable(qs.get("f", [DEFAULT_FILE])[0])
            except ValueError as exc:
                return self._send(str(exc).encode(), "text/plain; charset=utf-8", 400)
            return self._send(file_stamp(fp).encode(), "text/plain; charset=utf-8")

        if path == "/__raw":
            try:
                fp = resolve_editable(qs.get("f", [DEFAULT_FILE])[0])
            except ValueError as exc:
                return self._send(str(exc).encode(), "text/plain; charset=utf-8", 400)
            data = fp.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.send_header("Cache-Control", "no-store")
            # 存檔時拿這個指紋比對，檔案在編輯期間被改過就擋下來，不讓覆蓋
            self.send_header("X-Stamp", file_stamp(fp))
            self.end_headers()
            self.wfile.write(data)
            return

        if path == "/__edit":
            rel = qs.get("f", [DEFAULT_FILE])[0].lstrip("/")
            try:
                resolve_editable(rel)
            except ValueError as exc:
                return self._send(("無法編輯：%s" % exc).encode(),
                                  "text/plain; charset=utf-8", 400)
            opts = "".join(
                '<option value="%s"%s>%s</option>' % (f, " selected" if f == rel else "", f)
                for f in editable_files()
            )
            preview = "/" + (rel if rel.lower().endswith((".html", ".htm")) else DEFAULT_FILE)
            html = (EDITOR_HTML.replace("__OPTIONS__", opts)
                    .replace("__PREVIEW__", preview)
                    .replace("__FILE__", rel))
            return self._send(html.encode("utf-8"), "text/html; charset=utf-8")

        # 一般 .html：注入自動重新載入
        target = Path(self.translate_path(self.path))
        if target.is_dir():
            target = target / "index.html"
        if target.suffix.lower() in (".html", ".htm") and target.is_file():
            html = target.read_text(encoding="utf-8")
            html = (html.replace("</body>", RELOAD_JS + "</body>", 1)
                    if "</body>" in html else html + RELOAD_JS)
            return self._send(html.encode("utf-8"), "text/html; charset=utf-8")

        super().do_GET()

    def do_POST(self):  # noqa: N802
        if self.path.split("?")[0] != "/__save":
            return self._json({"ok": False, "error": "未知路徑"}, 404)
        try:
            n = int(self.headers.get("Content-Length") or 0)
            payload = json.loads(self.rfile.read(n).decode("utf-8"))
            fp = resolve_editable(payload["f"])
            text = payload["text"]
            if not isinstance(text, str):
                raise ValueError("內容不是文字")
            sent = payload.get("stamp")
            now = file_stamp(fp)
            if sent and sent != now and not payload.get("force"):
                print("  ⚠️  擋下覆蓋：%s 在編輯期間被改過" % payload["f"], flush=True)
                return self._json({"ok": False, "stale": True,
                                   "error": "這個檔案在你編輯的期間被改過了"}, 409)
            fp.write_text(text, encoding="utf-8")
        except Exception as exc:  # noqa: BLE001
            return self._json({"ok": False, "error": str(exc)}, 400)
        print("  ↳ 已儲存 %s（%d 字）" % (payload["f"], len(text)), flush=True)
        return self._json({"ok": True, "stamp": file_stamp(fp)})

    def log_message(self, fmt, *args):
        # send_error() 會傳 HTTPStatus 進來，不是字串，所以一定要先轉成 str，
        # 否則下面的 in 運算會丟 TypeError、把整個連線弄斷（瀏覽器看到 ERR_EMPTY_RESPONSE）
        first = str(args[0]) if args else ""
        if "/__ver" in first or "/__stamp" in first or "/favicon.ico" in first:
            return
        super().log_message(fmt, *args)


def serve_on_free_port(handler, first_port: int, tries: int = 25):
    """從 first_port 開始找一個能綁的 port。回傳 (server, port, skipped)。"""
    skipped = []
    for port in range(first_port, first_port + tries):
        try:
            return http.server.ThreadingHTTPServer(("127.0.0.1", port), handler), port, skipped
        except OSError as exc:
            if exc.errno not in (48, 98):  # EADDRINUSE (macOS / Linux)
                raise
            skipped.append(port)
    raise SystemExit(
        "  %d～%d 全部被佔用，用 --port 指定其他 port" % (first_port, first_port + tries - 1)
    )


def autocommit_loop(quiet_seconds: float = 3.0):
    """檔案停止變動 quiet_seconds 後自動 commit 一次。"""
    last = version()
    pending_since = None
    while True:
        time.sleep(1.0)
        now = version()
        if now != last:
            last, pending_since = now, time.time()
            continue
        if pending_since is None or time.time() - pending_since < quiet_seconds:
            continue
        pending_since = None
        dirty = subprocess.run(
            ["git", "-C", str(ROOT), "status", "--porcelain"],
            capture_output=True, text=True,
        ).stdout.strip()
        if not dirty:
            continue
        stamp = time.strftime("%Y-%m-%d %H:%M")
        subprocess.run(["git", "-C", str(ROOT), "add", "-A"], check=False)
        subprocess.run(
            ["git", "-C", str(ROOT), "commit", "-m", "chore: 手動編輯 %s" % stamp],
            check=False, capture_output=True,
        )
        print("  ↳ 已 commit：chore: 手動編輯 %s" % stamp, flush=True)


def main():
    ap = argparse.ArgumentParser(description="本機預覽 + 原始碼編輯伺服器")
    ap.add_argument("--port", type=int, default=8770, help="預設 8770；被佔用時自動往上找")
    ap.add_argument("--file", default=DEFAULT_FILE, help="開啟時要編輯的檔案")
    ap.add_argument("--autocommit", action="store_true", help="存檔停 3 秒後自動 git commit")
    ap.add_argument("--no-open", action="store_true", help="不要自動開瀏覽器")
    args = ap.parse_args()

    if args.autocommit:
        threading.Thread(target=autocommit_loop, daemon=True).start()

    handler = functools.partial(Handler, directory=str(ROOT))
    srv, port, skipped = serve_on_free_port(handler, args.port)
    edit_url = "http://localhost:%d/__edit?f=%s" % (port, urllib.parse.quote(args.file))
    view_url = "http://localhost:%d/%s" % (port, args.file.lstrip("/"))

    if skipped:
        print("  ⚠️  %s 已被其他程式佔用，改用 %d"
              % ("、".join(str(x) for x in skipped), port), flush=True)
    print("  監看：%s" % ROOT, flush=True)
    print("  自動 commit：%s" % ("開" if args.autocommit else "關（用 --autocommit 打開）"), flush=True)
    print("  Ctrl+C 結束", flush=True)
    print("\n  ▶ 編輯（原始碼 + 預覽）：%s" % edit_url, flush=True)
    print("    只看預覽：            %s\n" % view_url, flush=True)
    if not args.no_open:
        threading.Timer(0.6, webbrowser.open, args=(edit_url,)).start()
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\n  結束", flush=True)


if __name__ == "__main__":
    main()
