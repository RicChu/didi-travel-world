#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""本機預覽伺服器：改 index.html 存檔 → 瀏覽器自動重新載入。

用法：

    python3 turkey/scripts/dev.py                 # 開 http://localhost:8787/turkey/index.html
    python3 turkey/scripts/dev.py --autocommit    # 另外：每次存檔停 3 秒後自動 git commit
    python3 turkey/scripts/dev.py --port 9000 --no-open

重新載入時會保留「原本展開的日卡」與「捲動位置」，所以可以停在某一天邊改邊看。

注入的重新載入程式碼只存在於這支腳本送出去的回應裡，**檔案本身不會被改到**，
所以隨時可以直接 commit。
"""

import argparse
import functools
import hashlib
import http.server
import os
import subprocess
import threading
import time
import webbrowser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WATCH_SUFFIX = {".html", ".md", ".css", ".js", ".json", ".jpg", ".jpeg", ".png", ".webp", ".svg"}
SKIP_DIR = {".git", "node_modules", ".playwright-mcp", "__pycache__"}

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

  var badge = document.createElement('div');
  badge.style.cssText = 'position:fixed;left:10px;bottom:calc(env(safe-area-inset-bottom,0px) + 10px);'
    + 'z-index:9999;font:11px/1 -apple-system,BlinkMacSystemFont,sans-serif;letter-spacing:.12em;'
    + 'padding:6px 9px;border-radius:999px;background:rgba(13,59,102,.72);color:#fff;pointer-events:none';
  badge.textContent = 'LIVE';
  document.addEventListener('DOMContentLoaded', function(){ document.body.appendChild(badge); });

  var known = null;
  function poll(){
    fetch('/__ver', { cache: 'no-store' })
      .then(function(r){ return r.text(); })
      .then(function(v){
        if (known === null) { known = v; }
        else if (v !== known) { badge.textContent = 'RELOAD'; saveState(); location.reload(); return; }
        setTimeout(poll, 400);
      })
      .catch(function(){ badge.textContent = 'OFFLINE'; setTimeout(poll, 1500); });
  }
  poll();
})();
</script>
"""


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


class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):  # noqa: N802
        if self.path.split("?")[0] == "/__ver":
            body = version().encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)
            return

        if self.path.split("?")[0] == "/favicon.ico":
            self.send_response(204)
            self.send_header("Content-Length", "0")
            self.end_headers()
            return

        target = Path(self.translate_path(self.path))
        if target.is_dir():
            target = target / "index.html"
        if target.suffix.lower() in (".html", ".htm") and target.is_file():
            html = target.read_text(encoding="utf-8")
            if "</body>" in html:
                html = html.replace("</body>", RELOAD_JS + "</body>", 1)
            else:
                html += RELOAD_JS
            body = html.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)
            return

        super().do_GET()

    def log_message(self, fmt, *args):
        if "/__ver" in (args[0] if args else ""):
            return
        super().log_message(fmt, *args)


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
        print("  ↳ 已 commit：chore: 手動編輯 %s" % stamp)


def main():
    ap = argparse.ArgumentParser(description="改檔存檔即自動重新載入的本機預覽伺服器")
    ap.add_argument("--port", type=int, default=8787)
    ap.add_argument("--page", default="turkey/index.html")
    ap.add_argument("--autocommit", action="store_true", help="存檔停 3 秒後自動 git commit")
    ap.add_argument("--no-open", action="store_true", help="不要自動開瀏覽器")
    args = ap.parse_args()

    if args.autocommit:
        threading.Thread(target=autocommit_loop, daemon=True).start()

    url = "http://localhost:%d/%s" % (args.port, args.page.lstrip("/"))
    handler = functools.partial(Handler, directory=str(ROOT))
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", args.port), handler)

    print("  預覽：%s" % url)
    print("  監看：%s" % ROOT)
    print("  自動 commit：%s" % ("開" if args.autocommit else "關（用 --autocommit 打開）"))
    print("  Ctrl+C 結束\n")
    if not args.no_open:
        threading.Timer(0.6, webbrowser.open, args=(url,)).start()
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\n  結束")


if __name__ == "__main__":
    main()
