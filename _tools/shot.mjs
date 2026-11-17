// Full-page screenshot helper using Chrome DevTools Protocol (no npm deps).
// Usage: node shot.mjs <url> <outfile.png> [width] [--mobile]
import { spawn } from 'node:child_process';
import { writeFileSync, mkdtempSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';

const [, , url, out, widthArg, mode] = process.argv;
const width = Number(widthArg || 1440);
const mobile = mode === '--mobile';
const CHROME = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const PORT = 9500 + Math.floor(Math.random() * 400);
const profile = mkdtempSync(join(tmpdir(), 'shot-'));

const chrome = spawn(CHROME, [
  '--headless=new',
  '--disable-gpu',
  '--hide-scrollbars',
  '--no-first-run',
  '--no-default-browser-check',
  `--remote-debugging-port=${PORT}`,
  `--user-data-dir=${profile}`,
  `--window-size=${width},900`,
  'about:blank',
], { stdio: 'ignore' });

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

async function getWs() {
  for (let i = 0; i < 100; i++) {
    try {
      const r = await fetch(`http://127.0.0.1:${PORT}/json/version`);
      const j = await r.json();
      if (j.webSocketDebuggerUrl) return j.webSocketDebuggerUrl;
    } catch {}
    await sleep(120);
  }
  throw new Error('chrome did not start');
}

const wsUrl = await getWs();
const ws = new WebSocket(wsUrl);
await new Promise((res, rej) => { ws.onopen = res; ws.onerror = rej; });

let id = 0;
const pending = new Map();
const events = [];
ws.onmessage = (ev) => {
  const msg = JSON.parse(ev.data);
  if (msg.id && pending.has(msg.id)) {
    const { res, rej } = pending.get(msg.id);
    pending.delete(msg.id);
    msg.error ? rej(new Error(JSON.stringify(msg.error))) : res(msg.result);
  } else if (msg.method) events.push(msg);
};
function send(method, params = {}, sessionId) {
  const mid = ++id;
  return new Promise((res, rej) => {
    pending.set(mid, { res, rej });
    ws.send(JSON.stringify({ id: mid, method, params, sessionId }));
  });
}

// Create an isolated target
const { targetId } = await send('Target.createTarget', { url: 'about:blank' });
const { sessionId } = await send('Target.attachToTarget', { targetId, flatten: true });
const S = (m, p) => send(m, p, sessionId);

await S('Page.enable');
await S('Runtime.enable');
await S('Emulation.setDeviceMetricsOverride', {
  width,
  height: 900,
  deviceScaleFactor: 1,
  mobile,
});
if (mobile) await S('Emulation.setTouchEmulationEnabled', { enabled: true });

const loaded = new Promise((res) => {
  const t = setInterval(() => {
    if (events.some((e) => e.method === 'Page.loadEventFired' && e.sessionId === sessionId)) {
      clearInterval(t); res();
    }
  }, 100);
  setTimeout(() => { clearInterval(t); res(); }, 25000);
});
await S('Page.navigate', { url });
await loaded;
await sleep(2500);

// Lazy backgrounds/images: force all data-src into src, then settle
await S('Runtime.evaluate', {
  expression: `(() => {
    document.querySelectorAll('img[data-src]').forEach(img => { if (!img.getAttribute('src')) img.setAttribute('src', img.getAttribute('data-src')); });
    document.querySelectorAll('[data-bg]').forEach(el => { el.style.backgroundImage = 'url(' + el.getAttribute('data-bg') + ')'; });
    window.scrollTo(0, document.body.scrollHeight);
    return document.body.scrollHeight;
  })()`,
  awaitPromise: false,
});
await sleep(1200);
await S('Runtime.evaluate', { expression: 'window.scrollTo(0,0); 1' });
await sleep(600);

const { result } = await S('Runtime.evaluate', {
  expression: `JSON.stringify({h: Math.max(document.documentElement.scrollHeight, document.body.scrollHeight), w: document.documentElement.scrollWidth})`,
  returnByValue: true,
});
const { h, w } = JSON.parse(result.value);
const height = Math.min(h, 30000);
await S('Emulation.setDeviceMetricsOverride', { width, height, deviceScaleFactor: 1, mobile });
await sleep(900);

const shot = await S('Page.captureScreenshot', {
  format: 'png',
  captureBeyondViewport: true,
  clip: { x: 0, y: 0, width: Math.max(w, width), height, scale: 1 },
});
writeFileSync(out, Buffer.from(shot.data, 'base64'));
console.log(`OK ${out} ${width}x${height} (doc ${w}x${h})`);

ws.close();
chrome.kill();
process.exit(0);
