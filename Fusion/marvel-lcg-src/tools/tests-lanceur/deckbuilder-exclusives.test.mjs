// Cartes EXCLUSIVES TMNT (regle de l'utilisateur, 17/10/2026) : une carte dont
// quelque chose change (nom, traits, texte, cout...) n'est utilisable que dans
// le deck d'un heros TMNT. Les sets reserves viennent de data/arts_alternatifs.json.
//
//     node --test tools/tests-lanceur/deckbuilder-exclusives.test.mjs
import { test } from "node:test";
import assert from "node:assert/strict";
import { validerDeck } from "../../public/js/deckbuilder/regles.js";

const CATALOGUE = {
    ex1: { name: "* Bo-Wing", subtitle: "Donnie", class: "Aggression", type: "Ally", set_name: "TMNT Aggression", desc: {} },
    off1: { name: "Winter Soldier", class: "Aggression", type: "Ally", set_name: "Falcon", desc: {} },
};
for (let i = 1; i <= 9; i++) CATALOGUE[`Aggression${i}`] = { name: `Aggression ${i}`, class: "Aggression", type: "Event", desc: {} };

const carte = (id) => CATALOGUE[id];
const heros = (id, heroCardId) => ({ id, heroCardId, name: id, deck: { hero_deck: Array(15).fill("sig") } });
const choisies = (extra) => {
    const m = new Map(Object.entries(extra));
    let reste = 25 - Object.values(extra).reduce((a, b) => a + b, 0);
    for (let i = 1; reste > 0; i++) { const n = Math.min(3, reste); m.set(`Aggression${i}`, n); reste -= n; }
    return m;
};
const refus = (r) => r.problemes.filter((p) => p.includes("réservées aux héros TMNT"));

test("un héros d'un autre pack refuse une exclusive TMNT", () => {
    const r = validerDeck({ hero: heros("captain_marvel", "04001a"), choisies: choisies({ ex1: 1 }), carte });
    assert.equal(refus(r).length, 1);
    assert.match(refus(r)[0], /Bo-Wing/);
});

test("un héros TMNT l'accepte (reconnu par sa carte ou par son identifiant de deck)", () => {
    assert.equal(refus(validerDeck({ hero: heros("leonardo", "tl001a"), choisies: choisies({ ex1: 1 }), carte })).length, 0);
    assert.equal(refus(validerDeck({ hero: heros("jennika", undefined), choisies: choisies({ ex1: 1 }), carte })).length, 0);
});

test("témoin : une carte ordinaire n'est jamais refusée pour ce motif", () => {
    assert.equal(refus(validerDeck({ hero: heros("captain_marvel", "04001a"), choisies: choisies({ off1: 1 }), carte })).length, 0);
});
