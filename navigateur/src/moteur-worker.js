import { loadPyodide } from "./pyodide.mjs";
const N = 4 * 1024 * 1024; let ctrl, data;
const dec = new TextDecoder();
const V = new URL(import.meta.url).searchParams.get("v") || "";   // version du paquet : force le rechargement a chaque publication
const log = (m) => postMessage({ type: "log", json: m });
function lire() {
  const head = Atomics.load(ctrl, 0); let tail = Atomics.load(ctrl, 1); const out = [];
  while (tail < head) {
    let len = 0; for (let i = 0; i < 4; i++) len |= data[(tail + i) % N] << (8 * i);
    const b = new Uint8Array(len); for (let i = 0; i < len; i++) b[i] = data[(tail + 4 + i) % N];
    out.push(dec.decode(b)); tail += 4 + len;
  }
  Atomics.store(ctrl, 1, tail); return out;
}
globalThis.pomper = (ms) => { const tail = Atomics.load(ctrl, 1);
  if (Atomics.load(ctrl, 0) === tail) Atomics.wait(ctrl, 0, tail, ms); return JSON.stringify(lire()); };
globalThis.envoyer = (type, json) => postMessage({ type, json });
globalThis.journal = log;
onmessage = async (e) => {
  if (e.data.type !== "init") return;
  ctrl = new Int32Array(e.data.ctrl); data = new Uint8Array(e.data.data);
  const t = performance.now();
  try {
    log("Demarrage de Python...");
    const py = await loadPyodide({ indexURL: "./" });
    log("Chargement des bibliotheques...");
    await py.loadPackage(["aiohttp", "typing-extensions", "requests", "packaging", "numpy", "pillow"]);
    log("Chargement du moteur...");
    const buf = new Uint8Array(await (await fetch("./moteur.zip?v=" + V)).arrayBuffer());
    py.FS.mkdir("/eng"); py.unpackArchive(buf, "zip", { extractDir: "/eng" });
    for (const d of ["/eng/persist", "/eng/persist/replays", "/eng/persist/campagnes", "/eng/persist/deck", "/eng/persist/deck/custom"]) py.FS.mkdirTree(d);
    for (const [chemin, octets] of e.data.fichiers || []) {   // ce que le joueur avait sauvegarde
      py.FS.mkdirTree(chemin.slice(0, chemin.lastIndexOf("/")) || "/"); py.FS.writeFile(chemin, octets);
    }
    log(`Pret en ${Math.round(performance.now() - t)} ms (${(e.data.fichiers || []).length} fichiers restaures)`);
    const code = await (await fetch("./boot_navigateur.py?v=" + V)).text();
    py.runPython(code);
  } catch (err) { log("ERREUR: " + String(err.message || err).split("\n").slice(-8).join(" | ")); postMessage({ type: "erreur", json: String(err.message || err) }); }
};
