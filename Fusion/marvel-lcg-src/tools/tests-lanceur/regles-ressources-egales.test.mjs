// Tests du module pur `public/js/deckbuilder/regles.js`, regle declaree RESSOURCES_EGALES.
//
//     node --test tools/tests-lanceur/regles-ressources-egales.test.mjs
//
// Carol Danvers (gs001b, Galactic Storm, Kajislav) : « You must include an equal number of
// cards with a printed [energy], [mental], and [physical] resource in your deck. »
// On compte des CARTES ; le wild ne compte pas ; les cartes de campagne non plus (FAQ p.22).
import { test } from "node:test";
import assert from "node:assert/strict";
import { validerDeck, problemesRessourcesEgales } from "../../public/js/deckbuilder/regles.js";

const CATALOGUE = {
    sigY: { name: "Sig Y", class: "Hero", type: "Event", desc: { RES: "Y" } },
    sigB: { name: "Sig B", class: "Hero", type: "Event", desc: { RES: "B" } },
    sigR: { name: "Sig R", class: "Hero", type: "Event", desc: { RES: "R" } },
    energy: { name: "Energy", class: "Basic", type: "Resource", desc: { RES: "YY", MaxPerDeck: "1" } },
    genius: { name: "Genius", class: "Basic", type: "Resource", desc: { RES: "BB", MaxPerDeck: "1" } },
    strength: { name: "Strength", class: "Basic", type: "Resource", desc: { RES: "RR", MaxPerDeck: "1" } },
    joker: { name: "Joker", class: "Basic", type: "Upgrade", desc: { RES: "G" } },
    campagne: { name: "Allie de campagne", class: "Campaign", type: "Ally", desc: { RES: "Y" } },
};
for (let i = 1; i <= 8; i++) {
    CATALOGUE[`y${i}`] = { name: `Y ${i}`, class: "Aggression", type: "Event", desc: { RES: "Y" } };
    CATALOGUE[`b${i}`] = { name: `B ${i}`, class: "Aggression", type: "Event", desc: { RES: "B" } };
    CATALOGUE[`r${i}`] = { name: `R ${i}`, class: "Aggression", type: "Event", desc: { RES: "R" } };
}
const carte = (id) => CATALOGUE[id];
const SIGNATURES = [...Array(5).fill("sigY"), ...Array(5).fill("sigB"), ...Array(5).fill("sigR")];
const REGLE = { ressources_egales: { couleurs: ["Y", "B", "R"], label: "autant (Carol Danvers)" } };
const BINARY = { id: "binary", deck: { hero_deck: SIGNATURES, metadata: { deckbuilding: REGLE } } };
const SANS_REGLE = { id: "autre", deck: { hero_deck: SIGNATURES, metadata: {} } };

function deck(paires) {
    const m = new Map();
    for (const [id, n] of paires) m.set(id, n);
    return m;
}
const EQUILIBRE = [["y1", 3], ["y2", 3], ["y3", 2], ["b1", 3], ["b2", 3], ["b3", 2], ["r1", 3], ["r2", 3], ["r3", 2]];

test("deck equilibre 13/13/13 (signatures 5/5/5 + 8/8/8) : aucune remarque", () => {
    assert.deepEqual(problemesRessourcesEgales(BINARY, deck(EQUILIBRE), carte), []);
});

test("une carte [energy] de trop : refuse, les trois comptes cites", () => {
    const p = problemesRessourcesEgales(BINARY, deck([...EQUILIBRE, ["y4", 1]]), carte);
    assert.equal(p.length, 1);
    assert.match(p[0], /énergie 14, mentale 13, physique 13/);
});

test("on compte des CARTES : Energy (YY) compte 1, pas 2", () => {
    const v = deck([...EQUILIBRE, ["energy", 1], ["genius", 1], ["strength", 1]]);
    assert.deepEqual(problemesRessourcesEgales(BINARY, v, carte), []);
});

test("un wild ne compte pour aucune couleur", () => {
    assert.deepEqual(problemesRessourcesEgales(BINARY, deck([...EQUILIBRE, ["joker", 2]]), carte), []);
});

test("une carte de campagne ne compte pas (FAQ du livret p.22)", () => {
    assert.deepEqual(problemesRessourcesEgales(BINARY, deck([...EQUILIBRE, ["campagne", 1]]), carte), []);
});

test("les signatures comptent : un heros sans la regle n'a aucune remarque, meme desequilibre", () => {
    assert.deepEqual(problemesRessourcesEgales(SANS_REGLE, deck([...EQUILIBRE, ["y4", 3]]), carte), []);
});

test("validerDeck relaie le probleme", () => {
    const v = validerDeck({ hero: BINARY, choisies: deck([...EQUILIBRE, ["y4", 2]]), carte });
    assert.ok(v.problemes.some((p) => /Carol Danvers/.test(p)), v.problemes.join(" | "));
});
