// Full-page screenshot in vertical slices using CDP.
// Usage: node slice.mjs <url> <outprefix> <width> <sliceHeight> [maxSlices]
import { spawn } from 'node:child_process';
import { writeFileSync, mkdtempSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';

const [, , url, outPrefix, widthArg, sliceArg, maxArg, startArg] = process.argv; const startY = Number(startArg || 0);
const width = Number(widthArg || 1440);
const sliceH = Number(sliceArg || 2400);
const maxSlices = Number(maxArg || 40);
const CHROME = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const PORT = 9500 + Math.floor(Math.random() * 400);
const profile = mkdtempSync(join(tmpdir(), 'slice-'));

const chrome = spawn(CHROME, [
  '--headless=new', '--disable-gpu', '--hide-scrollbars', '--no-first-run',
  '--no-default-browser-check', `--remote-debugging-port=${PORT}`,
  `--user-data-dir=${profile}`, `--window-size=${width},900`, 'about:blank',
], { stdio: 'ignore' });

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
async function getWs() {
  for (let i = 0; i < 120; i++) {
    try {
      const j = await (await fetch(`http://127.0.0.1:${PORT}/json/version`)).json();
      if (j.webSocketDebuggerUrl) return j.webSocketDebuggerUrl;
    } catch {}
    await sleep(120);
  }
  throw new Error('chrome did not start');
}
const ws = new WebSocket(await getWs());
await new Promise((res, rej) => { ws.onopen = res; ws.onerror = rej; });
let id = 0; const pending = new Map(); const events = [];
ws.onmessage = (ev) => {
  const m = JSON.parse(ev.data);
  if (m.id && pending.has(m.id)) { const p = pending.get(m.id); pending.delete(m.id); m.error ? p.rej(new Error(JSON.stringify(m.error))) : p.res(m.result); }
  else if (m.method) events.push(m);
};
const send = (method, params = {}, sessionId) => new Promise((res, rej) => { const mid = ++id; pending.set(mid, { res, rej }); ws.send(JSON.stringify({ id: mid, method, params, sessionId })); });

const { targetId } = await send('Target.createTarget', { url: 'about:blank' });
const { sessionId } = await send('Target.attachToTarget', { targetId, flatten: true });
const S = (m, p) => send(m, p, sessionId);

await S('Page.enable');
await S('Emulation.setDeviceMetricsOverride', { width, height: 900, deviceScaleFactor: 1, mobile: false });
await S('Page.navigate', { url });
await sleep(4000);
await S('Runtime.evaluate', { expression: `document.querySelectorAll('img[data-src]').forEach(i=>{if(!i.getAttribute('src'))i.setAttribute('src',i.getAttribute('data-src'))}); document.querySelectorAll('.lazy-bg').forEach(e=>e.classList.add('lazy-bg-loaded')); document.querySelectorAll('.jv-nav,.cvt-1568371626-sticky-container').forEach(e=>{e.style.position='static';e.style.transform='none'}); window.scrollTo(0,document.body.scrollHeight); 1` });
await sleep(1500);
await S('Runtime.evaluate', { expression: 'window.scrollTo(0,0); 1' });
await sleep(500);
const { result } = await S('Runtime.evaluate', { expression: 'JSON.stringify({h:Math.max(document.documentElement.scrollHeight,document.body.scrollHeight)})', returnByValue: true });
const total = JSON.parse(result.value).h;
const n = Math.min(Math.ceil((total - startY) / sliceH), maxSlices);
for (let i = 0; i < n; i++) {
  const y = startY + i * sliceH;
  const height = Math.min(sliceH, total - y);
  const shot = await S('Page.captureScreenshot', {
    format: 'png', captureBeyondViewport: true,
    clip: { x: 0, y, width, height, scale: 1 },
  });
  const f = `${outPrefix}_${String(i + 1).padStart(2, '0')}.png`;
  writeFileSync(f, Buffer.from(shot.data, 'base64'));
  console.log(`OK ${f} y=${y} h=${height}`);
}
console.log(`TOTAL ${total}`);
ws.close(); chrome.kill(); process.exit(0);



