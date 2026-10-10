// Tests du module pur `public/js/deckbuilder/regles.js`, côté mot-clé STARTING.
//
//     node --test tools/tests-lanceur/regles-starting.test.mjs
//
// Livret Fear No Evil p.3 : « Each deck cannot include more than one card with
// starting. » Une seule CARTE, pas un seul titre : deux exemplaires du même
// titre sont aussi refusés.
import { test } from "node:test";
import assert from "node:assert/strict";
import { validerDeck } from "../../public/js/deckbuilder/regles.js";
import { cartesFautives } from "../../public/js/deckbuilder/fautives.js";

const STARTING = "Starting. <i>(You may add this card to your hand before drawing your starting hand.)</i>\n";
const CATALOGUE = {
    reflexes: { name: "Innate Reflexes", class: "Protection", type: "Upgrade", desc: {}, text: `${STARTING}Your hero gets +1 DEF.` },
    perception: { name: "Innate Perception", class: "Protection", type: "Upgrade", desc: {}, text: `${STARTING}Your hero gets +1 THW.` },
    // « starting » ailleurs dans le texte n'est pas le mot-clé.
    leurre: { name: "Faux départ", class: "Protection", type: "Event", desc: {}, text: "Draw 1 card from your starting hand size." },
};
for (let i = 1; i <= 12; i++) CATALOGUE[`p${i}`] = { name: `Pilier ${i}`, class: "Protection", type: "Ally", desc: {}, text: "" };
const carte = (id) => CATALOGUE[id];
const HEROS = { id: "storm", deck: { hero_deck: Array.from({ length: 15 }, (_, i) => `sig${i}`) } };

function deck(extra) {
    const choisies = new Map();
    for (let i = 1; i <= 8; i++) choisies.set(`p${i}`, 3);
    for (const [id, n] of extra) choisies.set(id, n);
    return choisies;
}
const starting = (v) => v.problemes.filter((p) => /Starting/.test(p));

test("une seule carte Starting : légal", () => {
    const v = validerDeck({ hero: HEROS, choisies: deck([["reflexes", 1]]), carte });
    assert.deepEqual(starting(v), []);
});

test("deux cartes Starting différentes : refusé, les deux citées et soulignées", () => {
    const choisies = deck([["reflexes", 1], ["perception", 1]]);
    const v = validerDeck({ hero: HEROS, choisies, carte });
    assert.equal(starting(v).length, 1);
    assert.match(starting(v)[0], /Innate Reflexes/);
    assert.match(starting(v)[0], /Innate Perception/);
    const fautives = cartesFautives({ choisies, carte, verdict: v, regle: { max: 1 } });
    assert.ok(fautives.has("reflexes") && fautives.has("perception"));
    assert.ok(!fautives.has("p1"));
});

test("deux exemplaires du même titre Starting : refusé", () => {
    const v = validerDeck({ hero: HEROS, choisies: deck([["reflexes", 2]]), carte });
    assert.equal(starting(v).length, 1);
});

test("le mot « starting » hors mot-clé ne compte pas", () => {
    const v = validerDeck({ hero: HEROS, choisies: deck([["reflexes", 1], ["leurre", 1]]), carte });
    assert.deepEqual(starting(v), []);
});
