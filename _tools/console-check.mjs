// Console + failed-request check for a URL.
import { spawn } from 'node:child_process';
import { mkdtempSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';

const url = process.argv[2];
const CHROME = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const PORT = 9500 + Math.floor(Math.random() * 400);
const profile = mkdtempSync(join(tmpdir(), 'con-'));
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
let id = 0; const pending = new Map(); const logs = []; const failed = [];
ws.onmessage = (ev) => {
  const m = JSON.parse(ev.data);
  if (m.id && pending.has(m.id)) { const p = pending.get(m.id); pending.delete(m.id); m.error ? p.rej(new Error(JSON.stringify(m.error))) : p.res(m.result); return; }
  if (m.method === 'Runtime.consoleAPICalled') logs.push(m.params.type + ': ' + (m.params.args || []).map(a => a.value ?? a.description ?? a.type).join(' '));
  if (m.method === 'Runtime.exceptionThrown') logs.push('EXCEPTION: ' + (m.params.exceptionDetails.exception?.description || m.params.exceptionDetails.text));
  if (m.method === 'Log.entryAdded' && m.params.entry.level === 'error') logs.push('LOG: ' + m.params.entry.text);
  if (m.method === 'Network.loadingFailed') failed.push(m.params.errorText + ' ' + (m.params.requestId || ''));
  if (m.method === 'Network.responseReceived' && m.params.response.status >= 400) failed.push(m.params.response.status + ' ' + m.params.response.url.slice(0, 120));
};
const send = (method, params = {}, sessionId) => new Promise((res, rej) => { const mid = ++id; pending.set(mid, { res, rej }); ws.send(JSON.stringify({ id: mid, method, params, sessionId })); });
const { targetId } = await send('Target.createTarget', { url: 'about:blank' });
const { sessionId } = await send('Target.attachToTarget', { targetId, flatten: true });
const S = (m, p) => send(m, p, sessionId);
await S('Runtime.enable'); await S('Log.enable'); await S('Network.enable'); await S('Page.enable');
await S('Page.navigate', { url });
await sleep(6000);
await S('Runtime.evaluate', { expression: 'window.scrollTo(0,document.body.scrollHeight); 1' });
await sleep(2500);
console.log('CONSOLE (' + logs.length + '):');
logs.slice(0, 25).forEach(l => console.log('  ' + l.slice(0, 200)));
console.log('FAILED (' + failed.length + '):');
failed.slice(0, 25).forEach(l => console.log('  ' + l.slice(0, 200)));
ws.close(); chrome.kill(); process.exit(0);
