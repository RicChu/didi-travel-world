#!/usr/bin/env node
/* 把 turkey/index.src.html（明文母檔）加密成 turkey/index.html（發佈用）。
 *
 *   node turkey/scripts/lock.js <密碼>
 *
 * 做法：整個 <body> 的內容（版面 + 全部 JS + 全部行程資料）序列化成 JSON，
 * 用 PBKDF2-SHA256 從密碼導出 AES-256-GCM 金鑰加密，只把密文寫進輸出檔。
 * 沒有密碼的人看原始碼只會看到一串 base64，連標題都看不到。
 * CSS 留在明文（不含任何個資，而且鎖定畫面本身要用）。
 */
const fs = require('fs');
const path = require('path');
const { webcrypto: wc } = require('crypto');

const ITER = 600000;                       // PBKDF2 迭代次數，拖慢暴力破解
const DIR  = path.resolve(__dirname, '..');
const SRC  = path.join(DIR, 'index.src.html');
const OUT  = path.join(DIR, 'index.html');

const pass = process.argv[2];
if (!pass) { console.error('用法：node turkey/scripts/lock.js <密碼>'); process.exit(1); }

const src = fs.readFileSync(SRC, 'utf8');

/* ── 切出 head（保留）與 body（加密） ───────────────────────── */
const headEnd   = src.indexOf('</head>');
const bodyStart = src.indexOf('<body>') + '<body>'.length;
const bodyEnd   = src.lastIndexOf('</body>');
if (headEnd < 0 || bodyStart < 6 || bodyEnd < 0) { console.error('找不到 head / body 邊界'); process.exit(1); }

let head = src.slice(0, headEnd);
const body = src.slice(bodyStart, bodyEnd);

const sOpen = body.indexOf('<script>');
const sClose = body.lastIndexOf('</script>');
if (sOpen < 0 || sClose < 0) { console.error('找不到 <script> 區塊'); process.exit(1); }
const html = body.slice(0, sOpen);
const js   = body.slice(sOpen + '<script>'.length, sClose);

const title = (src.match(/<title>([^<]*)<\/title>/) || [, ''])[1];

/* head 去掉會洩漏目的地的標題與 theme-color，補上 noindex */
head = head
  .replace(/<title>[^<]*<\/title>/, '<title>行程</title>')
  .replace(/<meta name="theme-color"[^>]*>\n?/, '')
  .replace('<meta name="viewport"', '<meta name="robots" content="noindex,nofollow,noarchive">\n<meta name="viewport"');

/* ── 加密 ──────────────────────────────────────────────── */
(async () => {
  const payload = new TextEncoder().encode(JSON.stringify({ t: title, h: html, j: js }));
  const salt = wc.getRandomValues(new Uint8Array(16));
  const iv   = wc.getRandomValues(new Uint8Array(12));
  const km   = await wc.subtle.importKey('raw', new TextEncoder().encode(pass), 'PBKDF2', false, ['deriveKey']);
  const key  = await wc.subtle.deriveKey(
    { name: 'PBKDF2', salt, iterations: ITER, hash: 'SHA-256' },
    km, { name: 'AES-GCM', length: 256 }, false, ['encrypt']);
  const ct = new Uint8Array(await wc.subtle.encrypt({ name: 'AES-GCM', iv }, key, payload));
  const b64 = u8 => Buffer.from(u8).toString('base64');

  const out = head + `</head>
<body>

<div id="lock">
  <form id="lockForm" autocomplete="off">
    <div class="lock-k">PRIVATE</div>
    <h1 class="lock-t">這份行程是鎖起來的</h1>
    <p class="lock-s">輸入密碼才看得到內容。</p>
    <input id="lockPw" type="password" inputmode="text" autocomplete="current-password" placeholder="密碼" aria-label="密碼">
    <label class="lock-r"><input id="lockRemember" type="checkbox" checked>記住這台裝置</label>
    <button type="submit" id="lockGo">解鎖</button>
    <p class="lock-e" id="lockErr" hidden>密碼不對</p>
  </form>
</div>
<div id="app"></div>

<script>
/* 內容以 AES-256-GCM 加密，金鑰由密碼經 PBKDF2-SHA256 導出。
   沒有正確密碼時，下面這串 base64 解不開，也拿不到任何明文。 */
var ENC={n:${ITER},s:'${b64(salt)}',i:'${b64(iv)}',c:'${b64(ct)}'};
(function(){
  var KEY='didi.k';
  var form=document.getElementById('lockForm'), pw=document.getElementById('lockPw'),
      err=document.getElementById('lockErr'), go=document.getElementById('lockGo'),
      rem=document.getElementById('lockRemember');
  function raw(b){var s=atob(b),u=new Uint8Array(s.length);for(var i=0;i<s.length;i++)u[i]=s.charCodeAt(i);return u;}
  function open(pass){
    var C=window.crypto&&window.crypto.subtle;
    if(!C) return Promise.reject(new Error('no-subtle'));
    return C.importKey('raw',new TextEncoder().encode(pass),'PBKDF2',false,['deriveKey'])
      .then(function(km){
        return C.deriveKey({name:'PBKDF2',salt:raw(ENC.s),iterations:ENC.n,hash:'SHA-256'},
                           km,{name:'AES-GCM',length:256},false,['decrypt']);
      })
      .then(function(k){ return C.decrypt({name:'AES-GCM',iv:raw(ENC.i)},k,raw(ENC.c)); })
      .then(function(buf){
        var d=JSON.parse(new TextDecoder().decode(buf));
        document.title=d.t;
        document.getElementById('app').innerHTML=d.h;
        var l=document.getElementById('lock'); if(l) l.remove();
        (0,eval)(d.j);
      });
  }
  function fail(e){
    if(e&&e.message==='no-subtle'){ err.textContent='這個瀏覽器不支援解密，請改用 HTTPS 或較新的瀏覽器'; }
    else { err.textContent='密碼不對'; try{localStorage.removeItem(KEY);}catch(_){} }
    err.hidden=false; go.disabled=false; go.textContent='解鎖'; pw.select();
  }
  form.addEventListener('submit',function(e){
    e.preventDefault(); err.hidden=true; go.disabled=true; go.textContent='解鎖中…';
    var v=pw.value;
    open(v).then(function(){ if(rem.checked){ try{localStorage.setItem(KEY,v);}catch(_){} } }).catch(fail);
  });
  var saved=null; try{ saved=localStorage.getItem(KEY); }catch(_){}
  if(saved){ go.disabled=true; go.textContent='解鎖中…'; open(saved).catch(function(){ go.disabled=false; go.textContent='解鎖'; pw.focus(); }); }
  else { pw.focus(); }
})();
<\/script>
</body>
</html>
`;
  fs.writeFileSync(OUT, out, 'utf8');
  const kb = n => (n / 1024).toFixed(0) + ' KB';
  console.log('✅ 已產生 ' + path.relative(process.cwd(), OUT));
  console.log('   明文 ' + kb(payload.length) + ' → 密文 ' + kb(ct.length) + '，PBKDF2 ' + ITER.toLocaleString() + ' 次');
  console.log('   密碼：' + pass.replace(/./g, '•') + '（' + pass.length + ' 字）');
})();
