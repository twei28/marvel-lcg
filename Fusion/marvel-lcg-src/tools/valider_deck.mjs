// Juge la legalite d'un deck avec LES MEMES regles que l'editeur et l'import (public/js/deckbuilder/regles.js).
//
//   node tools/valider_deck.mjs <heros> <fichier.txt>
//
//   <heros>        le nom du fichier de deck/starter/ sans .json (raphael, leonardo, spider_man...)
//   <fichier.txt>  une carte par ligne : « 3 ub012 » ou « 3x ub012 » (nombre puis identifiant). Les lignes vides et
//                  celles qui commencent par # ou // sont ignorees ; un commentaire peut suivre l'identifiant.
//
// Rend le verdict (ok / problemes), le total de cartes, et la liste lisible du deck. Sortie 0 si legal, 1 sinon.
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { validerDeck } from "../public/js/deckbuilder/regles.js";

const RACINE = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const [, , nomHeros, fichier] = process.argv;
if (!nomHeros || !fichier) { console.error("usage : node tools/valider_deck.mjs <heros> <fichier.txt>"); process.exit(2); }

const brut = JSON.parse(fs.readFileSync(path.join(RACINE, "data", "cards.json"), "utf8"));
const catalogue = {};
for (const liste of Object.values(brut)) for (const c of Array.isArray(liste) ? liste : []) {
    if (c && c.card_id) catalogue[c.card_id] = { ...c, class: (c.desc && c.desc.Class) || c.class, cost: c.desc && c.desc.Cost };
}
const carte = (id) => catalogue[String(id).split(",")[0]];

const depart = JSON.parse(fs.readFileSync(path.join(RACINE, "deck", "starter", nomHeros + ".json"), "utf8"));
const idHeros = String(depart.hero[0]).split(",")[0];
const cHeros = carte(idHeros);
const hero = { id: nomHeros, heroCardId: idHeros, name: cHeros ? cHeros.name : nomHeros, deck: depart };

const choisies = new Map();
for (const ligne of fs.readFileSync(fichier, "utf8").split(/\r?\n/)) {
    const l = ligne.trim();
    if (!l || l.startsWith("#") || l.startsWith("//")) continue;
    const m = /^(\d+)\s*x?\s+([A-Za-z0-9_]+)/.exec(l);
    if (!m) { console.error("ligne illisible : " + l); process.exit(2); }
    if (!carte(m[2])) { console.error("carte inconnue : " + m[2]); process.exit(2); }
    choisies.set(m[2], (choisies.get(m[2]) || 0) + Number(m[1]));
}

const verdict = validerDeck({ hero, choisies, carte });
console.log(`${hero.name} : ${verdict.ok ? "LEGAL" : "ILLEGAL"} ; ${verdict.total} cartes (signature comprise)`);
for (const p of verdict.problemes || []) console.log("  - " + p);
const parClasse = {};
for (const [id, n] of choisies) { const c = carte(id); const k = (c && c.class) || "?"; parClasse[k] = (parClasse[k] || 0) + n; }
console.log("  par classe : " + Object.entries(parClasse).map(([k, n]) => `${k} ${n}`).join(", "));
process.exit(verdict.ok ? 0 : 1);
