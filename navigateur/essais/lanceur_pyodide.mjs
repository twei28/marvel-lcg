// node lanceur_pyodide.mjs <dossier-dist> : une partie headless dans Pyodide, archive du moteur chargee en memoire.
import { loadPyodide } from "../dist/pyodide.mjs";
import fs from "node:fs";
import path from "node:path";
const dist = path.resolve(process.argv[2] || "../dist");
const py = await loadPyodide({ indexURL: dist + "/" });
await py.loadPackage(["aiohttp", "typing-extensions", "requests", "packaging", "numpy", "pillow"]);
py.FS.mkdir("/eng");
py.unpackArchive(new Uint8Array(fs.readFileSync(path.join(dist, "moteur.zip"))), "zip", { extractDir: "/eng" });
for (const d of ["/eng/persist", "/eng/persist/replays", "/eng/persist/campagnes", "/eng/persist/deck", "/eng/persist/deck/custom"]) py.FS.mkdirTree(d);
py.runPython(`import os
for k in ("HERO","VILLAIN","SEED","MAX_ASKS","TRACE"): os.environ[k] = ${JSON.stringify(Object.fromEntries(["HERO", "VILLAIN", "SEED", "MAX_ASKS", "TRACE"].map((k) => [k, process.env[k] || ""])))}[k]
os.environ["ENG_DIR"] = "/eng"; os.environ["SANS_FILS"] = "1"`);
py.runPython(fs.readFileSync(process.argv[3] || "partie_headless.py", "utf8"));
