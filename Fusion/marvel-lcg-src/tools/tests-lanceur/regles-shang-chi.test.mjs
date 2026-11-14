// Tests du module pur `public/js/deckbuilder/regles.js`, côté « Multiple Forms » de Shang-Chi (ch001b).
//
//     node --test tools/tests-lanceur/regles-shang-chi.test.mjs
//
// « You may include up to 3 copies of 1 ATTACK event from each aspect other than your chosen aspect. »
// Décision utilisateur du 24/10/2026 : « chaque autre aspect » = Aggression, Justice, Leadership, Protection
// + Determination, Venomized, 'Pool (pas les voies TMNT). Un TITRE par autre aspect, 3 exemplaires.
//
// Ce que ce fichier prouve : la règle lève la limite d'aspect POUR UN TITRE ATTACK PAR AUTRE ASPECT et pour rien d'autre,
// et elle est lue dans le VRAI deck de départ (deck/starter/shang_chi.json), pas dans une copie.
import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { validerDeck } from "../../public/js/deckbuilder/regles.js";

const deck = JSON.parse(readFileSync(new URL("../../deck/starter/shang_chi.json", import.meta.url), "utf8"));
const CATALOGUE = {};
// Les 15 signatures : des cartes neutres pour le décompte (leur contenu ne sert pas ici).
for (const id of deck.hero_deck) CATALOGUE[id] = { name: `Sig ${id}`, class: "Hero", type: "Event", desc: { Class: "Hero" }, traits: ["ATTACK"] };
const att = (nom, classe) => ({ name: nom, class: classe, type: "Event", traits: ["ATTACK"], desc: {} });
const evt = (nom, classe) => ({ name: nom, class: classe, type: "Event", traits: ["SKILL"], desc: {} });
// Le corps du deck : 9 titres différents en Leadership (limite de 3 exemplaires par titre).
for (let i = 1; i <= 9; i++) CATALOGUE[`lead${i}`] = { name: `Pilier ${i}`, class: "Leadership", type: "Ally", desc: {} };
Object.assign(CATALOGUE, {
    j1: att("Coup Justice 1", "Justice"), j2: att("Coup Justice 2", "Justice"), jnon: evt("Pensee Justice", "Justice"),
    a1: att("Coup Aggression", "Aggression"), p1: att("Coup Protection", "Protection"),
    d1: att("Coup Determination", "Determination"), v1: att("Coup Venomized", "Venomized"), pool1: att("Coup Pool", "'Pool"),
    t1: att("Coup Taijutsu", "Taijutsu"),
    jall: { name: "Allié Justice", class: "Justice", type: "Ally", desc: {}, traits: ["ATTACK"] },
});
const carte = (id) => CATALOGUE[id];
const hero = { id: "shang_chi", name: "Shang-Chi", deck };

function choisies(extra) {
    const m = new Map(Object.entries(extra));
    let reste = 25 - Object.values(extra).reduce((a, b) => a + b, 0);
    for (let i = 1; reste > 0; i++) {
        const n = Math.min(3, reste);
        m.set(`lead${i}`, n);
        reste -= n;
    }
    return m;
}
const juger = (extra) => validerDeck({ hero, choisies: choisies(extra), carte });
const hasAspects = (v) => v.problemes.some((p) => /aspects/i.test(p));

test("Multiple Forms : 3 exemplaires d'UN événement ATTACK de chaque autre aspect sont légaux", () => {
    const v = juger({ j1: 3, a1: 3, p1: 3 });
    assert.equal(v.ok, true, v.problemes.join(" | "));
    assert.equal(v.horsAspect, 3);
});

test("Multiple Forms : les trois aspects maison (Determination, Venomized, 'Pool) comptent aussi", () => {
    const v = juger({ j1: 3, d1: 3, v1: 3, pool1: 3 });
    assert.equal(v.ok, true, v.problemes.join(" | "));
    assert.equal(v.horsAspect, 4);
});

test("Multiple Forms : DEUX titres ATTACK du même autre aspect sont refusés (1 titre par aspect)", () => {
    const v = juger({ j1: 2, j2: 2 });
    assert.equal(v.ok, false);
    assert.ok(v.problemes.some((p) => /par autre aspect/.test(p)), v.problemes.join(" | "));
});

test("Multiple Forms : un événement qui n'est PAS une attaque d'un autre aspect est refusé", () => {
    const v = juger({ jnon: 2 });
    assert.equal(v.ok, false);
    assert.ok(hasAspects(v), v.problemes.join(" | "));
});

test("Multiple Forms : un ALLIÉ d'un autre aspect, même portant le trait ATTACK, est refusé (type Event exigé)", () => {
    const v = juger({ jall: 2 });
    assert.equal(v.ok, false);
});

test("Multiple Forms : une voie TMNT (Taijutsu) n'est PAS un aspect : la règle ne la couvre pas (carte Shinobi sans Path, deck refusé)", () => {
    const v = juger({ j1: 3, t1: 3 });
    assert.equal(v.ok, false);
    assert.ok(v.problemes.some((p) => /Shinobi|Path/.test(p)), v.problemes.join(" | "));
    assert.equal(v.horsAspect, 1, "seule la Justice sort du décompte, jamais la voie");
});

test("Multiple Forms : sans carte hors aspect, la règle ne change rien (deck à un seul aspect légal)", () => {
    const v = juger({});
    assert.equal(v.ok, true, v.problemes.join(" | "));
    assert.equal(v.horsAspect, 0);
});

test("Multiple Forms : 4 exemplaires du même titre hors aspect dépassent la limite ordinaire de 3 par titre", () => {
    const v = juger({ j1: 4 });
    assert.equal(v.ok, false);
    assert.ok(v.problemes.some((p) => /Trop d’exemplaires/.test(p)), v.problemes.join(" | "));
});
