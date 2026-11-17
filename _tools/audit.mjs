// Layout audit: reports horizontal overflow and out-of-viewport elements at several widths.
import { spawn } from 'node:child_process';
import { mkdtempSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';

const url = process.argv[2];
const widths = (process.argv[3] || '360,390,430,768,1024,1280,1440,1920').split(',').map(Number);
const CHROME = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const PORT = 9500 + Math.floor(Math.random() * 400);
const profile = mkdtempSync(join(tmpdir(), 'audit-'));
const chrome = spawn(CHROME, ['--headless=new', '--disable-gpu', '--no-first-run', '--no-default-browser-check',
  `--remote-debugging-port=${PORT}`, `--user-data-dir=${profile}`, '--window-size=1440,900', 'about:blank'], { stdio: 'ignore' });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
async function getWs() {
  for (let i = 0; i < 120; i++) {
    try { const j = await (await fetch(`http://127.0.0.1:${PORT}/json/version`)).json(); if (j.webSocketDebuggerUrl) return j.webSocketDebuggerUrl; } catch {}
    await sleep(120);
  }
  throw new Error('no chrome');
}
const ws = new WebSocket(await getWs());
await new Promise((res, rej) => { ws.onopen = res; ws.onerror = rej; });
let id = 0; const pending = new Map();
ws.onmessage = (ev) => { const m = JSON.parse(ev.data); if (m.id && pending.has(m.id)) { const p = pending.get(m.id); pending.delete(m.id); m.error ? p.rej(new Error(JSON.stringify(m.error))) : p.res(m.result); } };
const send = (method, params = {}, sessionId) => new Promise((res, rej) => { const mid = ++id; pending.set(mid, { res, rej }); ws.send(JSON.stringify({ id: mid, method, params, sessionId })); });
const { targetId } = await send('Target.createTarget', { url: 'about:blank' });
const { sessionId } = await send('Target.attachToTarget', { targetId, flatten: true });
const S = (m, p) => send(m, p, sessionId);
await S('Page.enable');
await S('Page.navigate', { url });
await sleep(3500);

const expr = `(() => {
  const vw = document.documentElement.clientWidth;
  const out = [];
  document.querySelectorAll('body *').forEach(el => {
    const r = el.getBoundingClientRect();
    if (r.width === 0 && r.height === 0) return;
    if (r.right > vw + 1 || r.left < -1) {
      out.push({ tag: el.tagName.toLowerCase(), cls: (el.className && el.className.toString().slice(0,60)) || '', left: Math.round(r.left), right: Math.round(r.right) });
    }
  });
  return JSON.stringify({
    vw,
    scrollW: document.documentElement.scrollWidth,
    bodyScrollW: document.body.scrollWidth,
    overflow: Math.max(document.documentElement.scrollWidth, document.body.scrollWidth) - vw,
    offenders: out.slice(0, 12),
    total: out.length
  });
})()`;

for (const w of widths) {
  await S('Emulation.setDeviceMetricsOverride', { width: w, height: 900, deviceScaleFactor: 1, mobile: w < 768 });
  await sleep(500);
  const { result } = await S('Runtime.evaluate', { expression: expr, returnByValue: true });
  const d = JSON.parse(result.value);
  console.log(`\n== ${w}px == viewport ${d.vw} scrollW ${d.scrollW}/${d.bodyScrollW} overflow ${d.overflow}px, offenders ${d.total}`);
  d.offenders.forEach(o => console.log(`   ${o.tag}.${o.cls} [${o.left} .. ${o.right}]`));
}
ws.close(); chrome.kill(); process.exit(0);
