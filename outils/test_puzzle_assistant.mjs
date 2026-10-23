// Parcours complet de l'assistant de création de puzzle (E5) dans un vrai navigateur.
// Prérequis : le jeu tourne sur http://127.0.0.1:2345/ (LANCEUR-LINUX.sh).
// Lancement : node outils/test_puzzle_assistant.mjs [dossier_des_captures]
// Joue les 8 étapes, envoie le puzzle au moteur (/new_puzzle) et vérifie que le plateau s'ouvre
// avec les cartes choisies ; échoue sur la moindre erreur de page ou de console.
import { spawn } from "node:child_process";
import { createRequire } from "node:module";
import { fileURLToPath } from "node:url";
import path from "node:path";
const racine = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const { chromium } = createRequire(path.join(racine, "ui-check", "package.json"))("playwright");
const sortie = process.argv[2];

// Un vrai serveur de puzzles (le Handler de l'orchestrateur, base temporaire) pour publier et lire par code.
const serveur = spawn("python3", ["-c", `
import os, sys, tempfile
sys.path.insert(0, ${JSON.stringify(path.join(racine, "site"))})
os.environ["BASE"] = os.path.join(tempfile.mkdtemp(), "s.db")
import orchestrateur as o
from http.server import ThreadingHTTPServer
s = ThreadingHTTPServer(("127.0.0.1", 0), o.Handler)
print(s.server_address[1], flush=True)
s.serve_forever()
`], { stdio: ["ignore", "pipe", "ignore"] });
const portSite = await new Promise((ok) => serveur.stdout.once("data", (d) => ok(Number(String(d).trim()))));

const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: 1280, height: 800 } });
const erreurs = [];
p.on("pageerror", (e) => erreurs.push("pageerror " + e.message));
p.on("console", (m) => { if (m.type() === "error") erreurs.push("console " + m.text()); });
const photo = async (nom) => { if (sortie) await p.screenshot({ path: path.join(sortie, nom + ".png") }); };
const suivant = async () => { await p.getByRole("button", { name: "Suivant" }).click(); await p.waitForTimeout(400); };

await p.addInitScript((port) => { window.MC_SITE_PUZZLES = "http://127.0.0.1:" + port; }, portSite);
await p.goto("http://127.0.0.1:2345/", { waitUntil: "load" });
await p.evaluate(() => { try { localStorage.clear(); } catch (e) {} });
await p.evaluate(() => import("/public/js/prepare/puzzle-assistant.js").then((m) => m.ouvrirAssistant()));
await p.waitForSelector(".pa-carte");
await p.locator(".pa-recherche").fill("spider-man");
await p.locator(".pa-carte", { hasText: "Spider-Man" }).first().click();
await photo("1-heros");
await suivant();
await p.locator(".pa-recherche").fill("rhino");
await p.locator(".pa-carte", { hasText: "rhino" }).first().click();
await p.waitForTimeout(1500);
await photo("2-ennemi");
await suivant();
await p.locator("input[type=range]").first().fill("9");
await p.locator("input[type=range]").nth(1).fill("4");
await photo("3-menace");
await suivant();
await photo("4-cartes");
await suivant();
await p.locator(".pa-recherche").fill("jessica jones");
await p.locator(".pa-resultats .pa-carte").first().click();
await p.getByRole("button", { name: "Amélioration" }).click();
await p.locator(".pa-recherche").fill("web-shooter");
await p.locator(".pa-resultats .pa-carte").first().click();
await photo("5-en-jeu");
await suivant();
await p.getByRole("button", { name: "Épuisé" }).first().click();
await photo("6-etats");
await suivant();
await p.getByRole("button", { name: "Vaincre le méchant" }).click();
await photo("7-objectif");
await suivant();
await p.locator("input.pa-texte").first().fill("Puzzle de test");
await photo("8-presentation");
// --- Publier : le code s'affiche, la clé est gardée dans « Mes puzzles »
await p.locator("input.pa-texte").nth(1).fill("Testeur");
await p.getByRole("button", { name: "Publier" }).click();
await p.waitForSelector("text=Puzzle publié", { timeout: 15000 });
const code = (await p.locator(".pa-corps strong").first().textContent()).trim();
await photo("9-publie");
if (!/^PZ-[A-Z0-9]{4}$/.test(code)) erreurs.push("code publié illisible : " + code);
const gardes = await p.evaluate(() => JSON.parse(localStorage.getItem("mc-puzzles-crees") || "[]"));
if (!gardes.some((x) => x.code === code && x.cle)) erreurs.push("la clé n'est pas gardée dans Mes puzzles");
await p.getByRole("button", { name: "Fermer" }).click();

// --- Modifier : « Mes puzzles » rouvre l'assistant sur ce puzzle et met le MÊME code à jour
await p.evaluate(() => import("/public/js/prepare/puzzles.js"));
await p.getByRole("button", { name: /Puzzles/ }).first().click();
await p.getByRole("button", { name: "Modifier" }).first().click();
await p.waitForSelector(".pa-carte");
for (let i = 0; i < 7; i++) { await p.getByRole("button", { name: "Suivant" }).click(); await p.waitForTimeout(250); }
await p.locator("input.pa-texte").first().fill("Titre modifié");
await p.getByRole("button", { name: "Enregistrer les changements" }).click();
await p.waitForSelector("text=Puzzle mis à jour", { timeout: 15000 });
const apres = await p.evaluate(async ({ port, code }) => (await (await fetch("http://127.0.0.1:" + port + "/api/puzzle/" + code)).json()).puzzle.title, { port: portSite, code });
if (apres !== "Titre modifié") erreurs.push("le puzzle n'a pas été modifié : " + apres);
await p.getByRole("button", { name: "Fermer" }).click();

// --- Résoudre par code, depuis le panneau Puzzles
await p.getByRole("button", { name: /Puzzles/ }).first().click();
await p.waitForSelector("text=Mes puzzles");
await photo("10-panneau");
await p.locator(".puzzles-boite input[type=text]").fill(code.toLowerCase());
await p.getByRole("button", { name: "Résoudre par code" }).click();
await p.waitForURL("**/app/board.html", { timeout: 20000 }).catch((e) => erreurs.push("pas de plateau par code : " + e.message));
await p.waitForTimeout(6000);
await photo("11-plateau-par-code");
const vus = {
  "méchant 9/14": await p.getByText("9 / 14").count(),
  "menace 4/7": await p.getByText("4 / 7").count(),
};

// --- Tester : on reprend le brouillon enregistré et on monte la table directement
await p.addInitScript((port) => { window.MC_SITE_PUZZLES = "http://127.0.0.1:" + port; }, portSite);
await p.goto("http://127.0.0.1:2345/", { waitUntil: "load" });
const ouverture = p.evaluate(() => import("/public/js/prepare/puzzle-assistant.js").then((m) => m.ouvrirAssistant()));
await p.getByRole("button", { name: "Reprendre mon brouillon" }).click();
await ouverture;
await p.getByText("Tester ce puzzle").click();
await p.waitForURL("**/app/board.html", { timeout: 20000 }).catch((e) => erreurs.push("pas de plateau (Tester) : " + e.message));
await p.waitForTimeout(6000);
vus["méchant 9/14 (Tester)"] = await p.getByText("9 / 14").count();
await photo("12-plateau-tester");
await b.close();
serveur.kill();
const manquants = Object.entries(vus).filter(([, n]) => !n).map(([nom]) => nom);
if (erreurs.length || manquants.length) {
  console.error("ECHEC", erreurs.join("\n"), manquants.length ? "absent du plateau : " + manquants.join(", ") : "");
  process.exit(1);
}
console.log("OK : l'assistant publie (" + code + "), le panneau résout par code, Tester monte la table (" + Object.keys(vus).join(", ") + ")");
