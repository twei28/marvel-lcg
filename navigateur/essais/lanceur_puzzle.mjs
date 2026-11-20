// node lanceur_puzzle.mjs <dossier-dist> : partie_puzzle.py dans Pyodide, archive du moteur chargee en memoire. PUZZLE_JSON passe par l'environnement.
import { loadPyodide } from "../dist/pyodide.mjs";
import fs from "node:fs";
import path from "node:path";
const dist = path.resolve(process.argv[2] || "../dist");
const py = await loadPyodide({ indexURL: dist + "/" });
await py.loadPackage(["aiohttp", "typing-extensions", "requests", "packaging", "numpy", "pillow"]);
py.FS.mkdir("/eng");
py.unpackArchive(new Uint8Array(fs.readFileSync(path.join(dist, "moteur.zip"))), "zip", { extractDir: "/eng" });
for (const d of ["/eng/persist", "/eng/persist/replays", "/eng/persist/campagnes", "/eng/persist/deck", "/eng/persist/deck/custom"]) py.FS.mkdirTree(d);
py.globals.set("PUZZLE_JSON_TEXTE", process.env.PUZZLE_JSON || "");
py.runPython(`import os
os.environ["PUZZLE_JSON"] = PUZZLE_JSON_TEXTE
os.environ["ENG_DIR"] = "/eng"; os.environ["SANS_FILS"] = "1"`);
py.runPython(fs.readFileSync(process.argv[3] || "partie_puzzle.py", "utf8"));
