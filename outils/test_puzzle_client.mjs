// Tests du module client des puzzles publiés (puzzle-client.js) contre un VRAI serveur de puzzles :
// le Handler de l'orchestrateur, lancé sur une base temporaire.
// Lancement : node outils/test_puzzle_client.mjs
import { spawn } from "node:child_process";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
const racine = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const client = await import(pathToFileURL(path.join(racine, "Fusion/marvel-lcg-src/public/js/prepare/puzzle-client.js")).href);
const brouillon = await import(pathToFileURL(path.join(racine, "Fusion/marvel-lcg-src/public/js/prepare/puzzle-brouillon.js")).href);

let echecs = 0;
const cas = (nom, obtenu, attendu) => {
  const ok = JSON.stringify(obtenu) === JSON.stringify(attendu);
  console.log(`  ${ok ? "ok   " : "ECHEC"} ${nom}${ok ? "" : ` : attendu ${JSON.stringify(attendu)}, obtenu ${JSON.stringify(obtenu)}`}`);
  if (!ok) echecs++;
};

// --- urlSite
const loc = (hostname, port = "") => ({ hostname, protocol: "https:", port, host: hostname + (port ? ":" + port : "") });
cas("table p3 -> site", client.urlSite(loc("p3.exemple.fr"), ""), "https://exemple.fr");
cas("play -> site", client.urlSite(loc("play.exemple.fr"), ""), "https://exemple.fr");
cas("le site lui-même", client.urlSite(loc("exemple.fr"), ""), "https://exemple.fr");
cas("jeu local : hors ligne", client.urlSite(loc("127.0.0.1", "2345"), ""), null);
cas("surcharge d'essai", client.urlSite(loc("127.0.0.1", "2345"), "http://127.0.0.1:9/"), "http://127.0.0.1:9");

// --- hors ligne : message clair, jamais d'appel
try { await client.publierPuzzle({}, "x", { site: null, f: () => { throw new Error("ne doit pas être appelé"); } }); cas("hors ligne", "publié", "refusé"); }
catch (e) { cas("hors ligne : message clair", e.raisons[0].includes("hors ligne"), true); }

// --- serveur réel
const serveur = spawn("python3", ["-c", `
import os, sys, tempfile, threading
sys.path.insert(0, ${JSON.stringify(path.join(racine, "site"))})
os.environ["BASE"] = os.path.join(tempfile.mkdtemp(), "s.db")
os.environ["DOMAINE"] = "exemple.test"
import orchestrateur as o
from http.server import ThreadingHTTPServer
s = ThreadingHTTPServer(("127.0.0.1", 0), o.Handler)
print(s.server_address[1], flush=True)
s.serve_forever()
`], { stdio: ["ignore", "pipe", "inherit"] });
const port = await new Promise((ok) => serveur.stdout.once("data", (d) => ok(Number(String(d).trim()))));
const site = `http://127.0.0.1:${port}`;

try {
  const b = brouillon.brouillonVide();
  Object.assign(b, { title: "Essai client", villain: ["01094"], schemes: ["01097a,01097b"], encounterDeck: ["01110"] });
  Object.assign(b.players[0], { identity: "01001b", hand: ["01071"], deck: ["01072"] });
  b.enJeu.push({ kind: "ally", card: "01059", siege: 0, state: { health: 2 } });
  const puzzle = brouillon.brouillonVersPuzzle(b, { auteur: "t" });

  const pub = await client.publierPuzzle(puzzle, "Arnaud", { site });
  cas("publié : un code PZ-", /^PZ-[A-Z0-9]{4}$/.test(pub.code), true);
  const lu = await client.lirePuzzle(pub.code, { site });
  cas("lu : même titre", lu.puzzle.title, "Essai client");
  cas("lu : la commande de l'allié est là", lu.puzzle.puzzle_command.some((c) => c.includes("'01059', 'ally'")), true);
  cas("lu : nb_jeux 0 avant de jouer", lu.nb_jeux, 0);

  // jouerParCode : lit avec jouer=1, puis monte la table (ici un faux /new_puzzle)
  const envois = [];
  const f = async (url, init) => {
    if (String(url).startsWith("/new_puzzle")) { envois.push(JSON.parse(init.body)); return { ok: true, status: 200 }; }
    return fetch(url, init);
  };
  const joue = await client.jouerParCode(pub.code, { site, f });
  cas("jouer : la table a reçu le puzzle", envois.length === 1 && envois[0].title === "Essai client", true);
  cas("jouer : compté", joue.nb_jeux, 1);

  // refus du serveur : les raisons remontent
  try { await client.publierPuzzle({ ...puzzle, puzzle_command: ["Puzzle.Win()"] }, "x", { site }); cas("refus", "publié", "refusé"); }
  catch (e) { cas("refus : statut 400 et raison", [e.statut, e.raisons.join(" ").includes("inconnue")], [400, true]); }

  // mauvais code
  try { await client.lirePuzzle("PZ-ZZZZ", { site }); cas("inconnu", "lu", "404"); }
  catch (e) { cas("inconnu : 404", e.statut, 404); }

  // modifier / supprimer
  await client.modifierPuzzle(pub.code, pub.cle, { ...puzzle, title: "Renommé" }, { site });
  cas("modifié", (await client.lirePuzzle(pub.code, { site })).puzzle.title, "Renommé");
  try { await client.supprimerPuzzle(pub.code, "mauvaise", { site }); cas("mauvaise clé", "supprimé", "403"); }
  catch (e) { cas("mauvaise clé : 403", e.statut, 403); }
  await client.supprimerPuzzle(pub.code, pub.cle, { site });
  try { await client.lirePuzzle(pub.code, { site }); cas("supprimé", "lu", "404"); }
  catch (e) { cas("supprimé : 404", e.statut, 404); }

  // le puzzle monté est gardé pour « Recommencer »
  const mem0 = new Map();
  const stock0 = { getItem: (k) => mem0.get(k) ?? null, setItem: (k, v) => mem0.set(k, v) };
  await client.monterPuzzle(puzzle, { f: async () => ({ ok: true, status: 200 }), stockage: stock0 });
  cas("puzzle courant gardé tel quel", JSON.parse(mem0.get("mc-puzzle-courant")).title, "Essai client");
  await client.monterPuzzle(puzzle, { f: async () => ({ ok: true, status: 200 }), stockage: { setItem: () => { throw new Error("bloqué"); } } });
  cas("stockage bloqué : le puzzle monte quand même", true, true);

  // refus du moteur local
  try { await client.monterPuzzle(puzzle, { f: async () => ({ ok: false, status: 400, text: async () => "Puzzle refusé : x" }) }); cas("moteur", "monté", "refusé"); }
  catch (e) { cas("moteur : le refus remonte", e.raisons[0], "Puzzle refusé : x"); }

  // Mes puzzles : stockage
  const mem = new Map();
  const stockage = { getItem: (k) => mem.get(k) ?? null, setItem: (k, v) => mem.set(k, v) };
  client.memoriserPuzzle({ code: "PZ-AAAA", cle: "k1", titre: "A" }, stockage);
  client.memoriserPuzzle({ code: "PZ-BBBB", cle: "k2", titre: "B" }, stockage);
  client.memoriserPuzzle({ code: "PZ-AAAA", cle: "k3", titre: "A2" }, stockage);
  cas("mes puzzles : le plus récent en tête, sans doublon", client.mesPuzzles(stockage).map((x) => x.code + x.cle), ["PZ-AAAAk3", "PZ-BBBBk2"]);
  client.oublierPuzzle("PZ-BBBB", stockage);
  cas("oublier", client.mesPuzzles(stockage).map((x) => x.code), ["PZ-AAAA"]);
  cas("stockage cassé : liste vide", client.mesPuzzles({ getItem: () => { throw new Error("bloqué"); } }), []);
} finally {
  serveur.kill();
}
process.exit(echecs ? 1 : 0);
