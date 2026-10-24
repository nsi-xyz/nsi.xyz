// Capture de discover.nsi.xyz dans son style « Glassmorphisme » (sombre et violet).
// La page retient le style choisi dans le stockage du navigateur : on le règle avant la capture,
// ce que le simple mode capture de Chrome ne permet pas. Utilise le protocole DevTools de Chrome.
//
//   node scripts/apercu-discover.mjs
//
// Nécessite Node 22 ou plus et Google Chrome. Écrit assets/apercus/discover.nsi.xyz.png,
// que scripts/apercus.py convertit ensuite en WebP (python scripts/apercus.py --convertir discover).
import { spawn } from "node:child_process";
import { mkdtempSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

const CHROME = "C:/Program Files/Google/Chrome/Application/chrome.exe";
const URL_SITE = "https://discover.nsi.xyz/";
const STYLE = "glass";
const OUT = new URL("../assets/apercus/discover.nsi.xyz.png", import.meta.url);

const profile = mkdtempSync(join(tmpdir(), "apercu-"));
const chrome = spawn(CHROME, ["--headless=new", "--disable-gpu", "--hide-scrollbars", "--remote-debugging-port=9333",
  `--user-data-dir=${profile}`, "--window-size=1280,800", "about:blank"], { stdio: "ignore" });
const wait = ms => new Promise(r => setTimeout(r, ms));

try {
  let target;
  for (let i = 0; i < 50 && !target; i++) {
    await wait(200);
    try { target = (await (await fetch("http://127.0.0.1:9333/json")).json()).find(t => t.type === "page"); } catch {}
  }
  const ws = new WebSocket(target.webSocketDebuggerUrl);
  await new Promise(r => ws.addEventListener("open", r));
  let id = 0;
  const pending = new Map();
  ws.addEventListener("message", e => {
    const msg = JSON.parse(e.data);
    if (pending.has(msg.id)) { pending.get(msg.id)(msg.result); pending.delete(msg.id); }
  });
  const send = (method, params = {}) => new Promise(r => { pending.set(++id, r); ws.send(JSON.stringify({ id, method, params })); });

  await send("Emulation.setDeviceMetricsOverride", { width: 1280, height: 800, deviceScaleFactor: 2, mobile: false });
  await send("Page.navigate", { url: URL_SITE });
  await wait(2500);
  await send("Runtime.evaluate", { expression: `localStorage.setItem("nsi-style", "${STYLE}")` });
  await send("Page.reload", {});
  await wait(4000);
  const shot = await send("Page.captureScreenshot", { format: "png" });
  writeFileSync(OUT, Buffer.from(shot.data, "base64"));
  console.log("ok     discover.nsi.xyz  (style Glassmorphisme)");
  ws.close();
} finally {
  chrome.kill();
}
