// Parcours complet de l'assistant de création de puzzle (E5) dans un vrai navigateur.
// Prérequis : le jeu tourne sur http://127.0.0.1:2345/ (LANCEUR-LINUX.sh).
// Lancement : node outils/test_puzzle_assistant.mjs [dossier_des_captures]
// Joue les 8 étapes, envoie le puzzle au moteur (/new_puzzle) et vérifie que le plateau s'ouvre
// avec les cartes choisies ; échoue sur la moindre erreur de page ou de console.
import { createRequire } from "node:module";
import { fileURLToPath } from "node:url";
import path from "node:path";
const racine = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const { chromium } = createRequire(path.join(racine, "ui-check", "package.json"))("playwright");
const sortie = process.argv[2];

const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: 1280, height: 800 } });
const erreurs = [];
p.on("pageerror", (e) => erreurs.push("pageerror " + e.message));
p.on("console", (m) => { if (m.type() === "error") erreurs.push("console " + m.text()); });
const photo = async (nom) => { if (sortie) await p.screenshot({ path: path.join(sortie, nom + ".png") }); };
const suivant = async () => { await p.getByRole("button", { name: "Suivant" }).click(); await p.waitForTimeout(400); };

await p.goto("http://127.0.0.1:2345/", { waitUntil: "load" });
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
await p.getByText("Tester ce puzzle").click();
await p.waitForURL("**/app/board.html", { timeout: 20000 }).catch((e) => erreurs.push("pas de plateau : " + e.message));
await p.waitForTimeout(6000);
await photo("9-plateau");
// Ce que le moteur a réellement monté : PV du méchant (9 sur 14), menace (4 sur 7), l'allié posé.
// (Le panneau Objectifs, lui, vient du plateau COMPILÉ : il n'apparaît qu'après le déploiement.)
const vus = {
  "méchant 9/14": await p.getByText("9 / 14").count(),
  "menace 4/7": await p.getByText("4 / 7").count(),
  "Jessica Jones": await p.locator("img[alt*='essica']").count() + await p.getByText("Jessica", { exact: false }).count(),
};
await b.close();
const manquants = Object.entries(vus).filter(([, n]) => !n).map(([nom]) => nom);
if (erreurs.length || manquants.length) {
  console.error("ECHEC", erreurs.join("\n"), manquants.length ? "absent du plateau : " + manquants.join(", ") : "");
  process.exit(1);
}
console.log("OK : l'assistant a monté un puzzle jouable (" + Object.keys(vus).join(", ") + ")");
