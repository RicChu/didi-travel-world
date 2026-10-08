#!/usr/bin/env node
/* 把 turkey/index.src.html（明文母檔）建成 turkey/index.html（發佈用）。
 *
 *   node turkey/scripts/lock.js <密碼>
 *
 * 發佈檔有兩份內容：
 *   公開版：任何人打開都看得到。拿掉訂單看板（訂位代號、名字、租車、門票）、
 *          飯店名稱與位置、兩個人的暱稱。
 *   完整版：原本整個 <body>，用 PBKDF2-SHA256 從密碼導出 AES-256-GCM 金鑰加密。
 *          裝置上存過密碼（右上角「🔒 私密內容」輸入一次）才會解開顯示。
 * CSS 留在明文（不含任何個資）。
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

/* ── 切出 head（保留）與 body ───────────────────────── */
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

head = head.replace('<meta name="viewport"', '<meta name="robots" content="noindex,nofollow,noarchive">\n<meta name="viewport"');

/* ── 公開版：拿掉私密內容 ─────────────────────────────── */
function must(s, a, b) {
  if (!s.includes(a)) { console.error('公開版處理失敗，找不到：' + a.slice(0, 60)); process.exit(1); }
  return s.split(a).join(b);
}
/* 長的先換，避免「Henna Hotel 屋頂早餐」先被「Henna Hotel」吃掉變成「飯店 屋頂早餐」 */
const WORDS = [
  ['Henna Hotel 屋頂早餐', '飯店屋頂早餐'], ['回 Henna Hotel', '回飯店'],
  ['Basilissis Hotel → Istanbul Airport', '飯店 → Istanbul Airport'],
  ['Bellamaritimo Hotel', '飯店'], ['Henna Hotel', '飯店'], ['Basilissis Hotel', '飯店'],
];
let pubH = html.replace(/<p class="hero-who" data-private>[^<]*<\/p>\s*/, '');
let pubJ = js;
const pb = pubJ.indexOf('var PANELS={'), pe = pubJ.indexOf('\n};\n', pb);
if (pb < 0 || pe < 0) { console.error('找不到 PANELS'); process.exit(1); }
pubJ = pubJ.slice(0, pb) + "var PANELS={stay:{rows:[]},fly:{rows:[],subRows:[]},car:{rows:[]},other:{rows:[]}};" + pubJ.slice(pe + 3);
pubJ = must(pubJ, 'var FULL=true;', 'var FULL=false;');
/* 飯店座標與地名換成鎮中心；JS 註解整段拿掉（裡面寫了住宿細節） */
pubJ = pubJ
  .replace(/^(\s*bella:)'[^']*'/m, "$1'Pamukkale'")
  .replace(/^(\s*henna:)'[^']*'/m, "$1'Göreme'")
  .replace(/^(\s*basil:)'[^']*'/m, "$1'Sultanahmet Istanbul'")
  .replace(/^(\s*basilissis:)'[^']*'/m, "$1'Sultanahmet, Istanbul'")
  .replace(/^(\s*bella:)'[\d.,]+'/m, "$1'37.9205,29.1196'")
  .replace(/^(\s*henna:)'[\d.,]+'/m, "$1'38.6431,34.8289'")
  .replace(/\/\*[\s\S]*?\*\//g, '');
for (const [a, b] of WORDS) pubJ = pubJ.split(a).join(b);
/* 點位的 key 名稱本身就是飯店名 */
pubJ = pubJ.replace(/\bbasilissis\b/g, 'hotelI').replace(/\bbasil\b/g, 'hotelI2')
           .replace(/\bbella\b/g, 'hotelP').replace(/\bhenna\b/g, 'hotelC');
/* 訂單 id 裡帶了飯店名與暱稱 */
pubJ = pubJ.replace(/'(stay-[a-z]+|fly-ann-out|fly-chu-out|fly-ann-back|fly-chu-back)'/g,
  (m, id) => "'" + ({ 'fly-ann-out': 'fly-out-a', 'fly-chu-out': 'fly-out-b', 'fly-ann-back': 'fly-back-a', 'fly-chu-back': 'fly-back-b' }[id] || 'stay') + "'");

/* 最後檢查：公開版不能出現任何一個私密字串 */
const LEAK = /henna|bellamar|basilis|güzelsanatlar|安安|豬豬|anyi|hsieh|UQE3KZ|TB5RZM|D438G7|38\.642261|37\.918462|whats ?app/i;
for (const [name, s] of [['HTML', pubH], ['JS', pubJ]]) {
  const m = s.match(LEAK);
  if (m) {
    const i = m.index;
    console.error('❌ 公開版' + name + '還有私密字串：…' + s.slice(Math.max(0, i - 40), i + 40).replace(/\n/g, ' ') + '…');
    process.exit(1);
  }
}

/* ── 加密完整版 ──────────────────────────────────────── */
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
  /* 公開版以 JSON 字串放進 <script>，</ 要拆開才不會提早結束標籤 */
  const pub = JSON.stringify({ t: title, h: pubH, j: pubJ }).replace(/<\//g, '<\\/');

  const out = head + `</head>
<body>

<div id="app"></div>

<script>
/* 完整版以 AES-256-GCM 加密，金鑰由密碼經 PBKDF2-SHA256 導出；沒有密碼解不開。
   裝置上存過密碼（didi.k）就顯示完整版，否則顯示公開版。 */
var ENC={n:${ITER},s:'${b64(salt)}',i:'${b64(iv)}',c:'${b64(ct)}'};
var PUB=${pub};
(function(){
  var K='didi.k', KK='didi.kk', C=window.crypto&&window.crypto.subtle;
  function get(k){try{return localStorage.getItem(k);}catch(_){return null;}}
  function set(k,v){try{localStorage.setItem(k,v);}catch(_){}}
  function raw(b){var s=atob(b),u=new Uint8Array(s.length);for(var i=0;i<s.length;i++)u[i]=s.charCodeAt(i);return u;}
  function b64(u){var s='';for(var i=0;i<u.length;i++)s+=String.fromCharCode(u[i]);return btoa(s);}
  function render(d){
    document.title=d.t;
    document.getElementById('app').innerHTML=d.h;
    (0,eval)(d.j);
  }
  /* 密碼 → 金鑰要跑 60 萬次 PBKDF2（手機約 1 秒），算出來的金鑰跟這版的 salt 一起存，下次直接用 */
  function bits(pass){
    return C.importKey('raw',new TextEncoder().encode(pass),'PBKDF2',false,['deriveBits'])
      .then(function(km){ return C.deriveBits({name:'PBKDF2',salt:raw(ENC.s),iterations:ENC.n,hash:'SHA-256'},km,256); })
      .then(function(b){ return new Uint8Array(b); });
  }
  function open(kb){
    return C.importKey('raw',kb,'AES-GCM',false,['decrypt'])
      .then(function(k){ return C.decrypt({name:'AES-GCM',iv:raw(ENC.i)},k,raw(ENC.c)); })
      .then(function(buf){ return JSON.parse(new TextDecoder().decode(buf)); });
  }
  window.__unlock=function(pass){
    if(!C) return Promise.reject(new Error('no-subtle'));
    return bits(pass).then(function(kb){
      return open(kb).then(function(){ set(K,pass); set(KK,JSON.stringify({s:ENC.s,k:b64(kb)})); });
    });
  };
  var pass=get(K), kk=null;
  try{ kk=JSON.parse(get(KK)||'null'); }catch(_){}
  if(!C||!pass){ render(PUB); return; }
  document.getElementById('app').innerHTML='<p style="padding:40px 20px;text-align:center;color:#756467">解鎖中…</p>';
  var kp=(kk&&kk.s===ENC.s)?Promise.resolve(raw(kk.k)):bits(pass).then(function(kb){ set(KK,JSON.stringify({s:ENC.s,k:b64(kb)})); return kb; });
  kp.then(open).then(render,function(){
    try{ localStorage.removeItem(K); localStorage.removeItem(KK); }catch(_){}
    render(PUB);
  });
})();
<\/script>
</body>
</html>
`;
  fs.writeFileSync(OUT, out, 'utf8');
  const kb = n => (n / 1024).toFixed(0) + ' KB';
  console.log('✅ 已產生 ' + path.relative(process.cwd(), OUT));
  console.log('   公開版 ' + kb(pub.length) + '；完整版 ' + kb(payload.length) + ' → 密文 ' + kb(ct.length) + '，PBKDF2 ' + ITER.toLocaleString() + ' 次');
  console.log('   密碼：' + pass.replace(/./g, '•') + '（' + pass.length + ' 字）');
})();
