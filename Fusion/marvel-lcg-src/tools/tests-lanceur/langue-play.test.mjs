// Langue de l'habillage de PLAY (navigateur/src/navigateur.html et shim.js).
//
// ⚠ play.<domaine> et <domaine> sont deux ORIGINES : le `marvel-langue` choisi sur le site n'existe pas dans le
// localStorage de Play. Constat du 26/10/2026 (téléphone) : le message « Sur téléphone, ce mode est expérimental »
// s'affichait en français à un joueur anglophone, alors que le texte anglais existait. La langue se résout donc dans
// cet ordre : ?langue=en|fr (puis retenu) > choix déjà fait ici (marvel-langue) > cookie nc_langue posé par le site sur le
// domaine parent (site/orchestrateur.py, route /langue) > langue du navigateur > français.
//
// Le bloc `langueDePlay` est écrit à l'identique dans navigateur.html et shim.js (deux fichiers qui n'ont aucun module
// commun) : ce test vérifie qu'ils sont identiques et le fait tourner sur une fausse page.
import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const ici = dirname(fileURLToPath(import.meta.url));
const racine = join(ici, "..", "..", "..", "..");
const HTML = readFileSync(join(racine, "navigateur", "src", "navigateur.html"), "utf8");
const SHIM = readFileSync(join(racine, "navigateur", "src", "shim.js"), "utf8");

function bloc(texte, nom) {
  const m = texte.match(/\/\/ LANGUE-PLAY-DEBUT\n([\s\S]*?)\/\/ LANGUE-PLAY-FIN/);
  assert.ok(m, `${nom} : le bloc LANGUE-PLAY-DEBUT / LANGUE-PLAY-FIN est absent`);
  return m[1];
}

function fabrique(texte, nom) {
  // eslint-disable-next-line no-new-func
  return new Function(`${bloc(texte, nom)}\nreturn langueDePlay;`)();
}

function faux({ stocke = {}, langue = "", langues = undefined, recherche = "", sansStockage = false, cookie = "" } = {}) {
  const donnees = { ...stocke };
  const storage = sansStockage
    ? { getItem() { throw new Error("stockage bloqué"); }, setItem() { throw new Error("stockage bloqué"); } }
    : { getItem: (k) => (k in donnees ? donnees[k] : null), setItem: (k, v) => { donnees[k] = String(v); } };
  return { donnees, storage, nav: { language: langue, languages: langues }, loc: { search: recherche }, cookie };
}

for (const [nom, texte] of [["navigateur.html", HTML], ["shim.js", SHIM]]) {
  test(`${nom} : le navigateur en anglais, sans choix, donne l'anglais`, () => {
    const f = fabrique(texte, nom); const c = faux({ langue: "en-US" });
    assert.equal(f(c.storage, c.nav, c.loc, c.cookie), "en");
  });
  test(`${nom} : le navigateur en français ou inconnu donne le français`, () => {
    const f = fabrique(texte, nom);
    for (const langue of ["fr-FR", "de-DE", "", "ja"]) {
      const c = faux({ langue });
      assert.equal(f(c.storage, c.nav, c.loc, c.cookie), "fr", `langue « ${langue} »`);
    }
  });
  test(`${nom} : le choix déjà fait ici l'emporte sur le navigateur`, () => {
    const f = fabrique(texte, nom);
    let c = faux({ stocke: { "marvel-langue": "fr" }, langue: "en-GB" });
    assert.equal(f(c.storage, c.nav, c.loc, c.cookie), "fr");
    c = faux({ stocke: { "marvel-langue": "en" }, langue: "fr-FR" });
    assert.equal(f(c.storage, c.nav, c.loc, c.cookie), "en");
  });
  test(`${nom} : une valeur de stockage inconnue est ignorée`, () => {
    const f = fabrique(texte, nom); const c = faux({ stocke: { "marvel-langue": "xx" }, langue: "en-US" });
    assert.equal(f(c.storage, c.nav, c.loc, c.cookie), "en");
  });
  test(`${nom} : la première langue de la liste sert quand « language » est vide`, () => {
    const f = fabrique(texte, nom); const c = faux({ langue: "", langues: ["en-CA", "fr"] });
    assert.equal(f(c.storage, c.nav, c.loc, c.cookie), "en");
  });
  test(`${nom} : un stockage bloqué ne casse rien (navigateur en anglais -> anglais)`, () => {
    const f = fabrique(texte, nom); const c = faux({ sansStockage: true, langue: "en-US" });
    assert.equal(f(c.storage, c.nav, c.loc, c.cookie), "en");
  });
  test(`${nom} : ?langue=en l'emporte, et est retenu pour la prochaine fois`, () => {
    const f = fabrique(texte, nom); const c = faux({ stocke: { "marvel-langue": "fr" }, langue: "fr-FR", recherche: "?page=/prepare.html&langue=en" });
    assert.equal(f(c.storage, c.nav, c.loc, c.cookie), "en");
    assert.equal(c.donnees["marvel-langue"], "en");
  });
  test(`${nom} : ?langue=klingon est ignoré`, () => {
    const f = fabrique(texte, nom); const c = faux({ langue: "en-US", recherche: "?langue=klingon" });
    assert.equal(f(c.storage, c.nav, c.loc, c.cookie), "en");
    assert.equal(c.donnees["marvel-langue"], undefined);
  });
}

// Même code, indentation différente (navigateur.html est au niveau du module, shim.js dans une fonction).
const sansIndentation = (t) => t.replace(/^[ \t]+/gm, "");

for (const [nom, texte] of [["navigateur.html", HTML], ["shim.js", SHIM]]) {
  test(`${nom} : le cookie nc_langue du site donne la langue choisie sur le site`, () => {
    const f = fabrique(texte, nom);
    let c = faux({ langue: "fr-FR", cookie: "a=1; nc_langue=en; b=2" });
    assert.equal(f(c.storage, c.nav, c.loc, c.cookie), "en");
    c = faux({ langue: "en-US", cookie: "nc_langue=fr" });
    assert.equal(f(c.storage, c.nav, c.loc, c.cookie), "fr");
  });
  test(`${nom} : le choix fait ici l'emporte sur le cookie du site`, () => {
    const f = fabrique(texte, nom); const c = faux({ stocke: { "marvel-langue": "fr" }, cookie: "nc_langue=en" });
    assert.equal(f(c.storage, c.nav, c.loc, c.cookie), "fr");
  });
  test(`${nom} : un cookie illisible ou inconnu est ignoré`, () => {
    const f = fabrique(texte, nom);
    for (const cookie of ["nc_langue=klingon", "xnc_langue=en", "", undefined]) {
      const c = faux({ langue: "fr-FR", cookie });
      assert.equal(f(c.storage, c.nav, c.loc, c.cookie), "fr", `cookie « ${cookie} »`);
    }
  });
}

test("le bloc de langue est identique dans navigateur.html et shim.js", () => {
  assert.equal(sansIndentation(bloc(HTML, "navigateur.html")), sansIndentation(bloc(SHIM, "shim.js")));
});

test("navigateur.html : la langue vient de langueDePlay, plus d'une lecture directe du localStorage", () => {
  assert.match(HTML, /langueDePlay\(/);
  assert.doesNotMatch(HTML, /const EN = \(\(\) => \{ try \{ return localStorage\.getItem\("marvel-langue"\) === "en"/);
});

test("shim.js : tr() passe par langueDePlay", () => {
  assert.match(SHIM, /const tr = \(fr, en\) => \{[\s\S]*?langueDePlay\(st, navigator, location, ck\) === "en" \? en : fr/);
});

test("navigateur.html : les messages de démarrage du moteur sont traduits (plus de français seul)", () => {
  for (const fr of ["Demarrage de Python...", "Chargement des bibliotheques...", "Chargement du moteur..."]) {
    assert.ok(HTML.includes(fr), `la table de traduction doit connaître « ${fr} »`);
  }
  assert.match(HTML, /Starting Python/);
  assert.match(HTML, /Loading libraries/);
  assert.match(HTML, /Loading the engine/);
});

test("navigateur.html : les erreurs d'import d'une sauvegarde sont traduites", () => {
  for (const fr of ["fichier trop gros", "ce n'est pas un fichier d'export valide", "ce n'est pas un export de ce jeu"]) {
    assert.ok(HTML.includes(fr), `« ${fr} » doit rester la clé française`);
  }
  assert.match(HTML, /file too large/);
  assert.match(HTML, /not a valid export file/);
  assert.match(HTML, /not an export of this game/);
});
