// node --test tools/tests-lanceur/deckbuilder-fautives.test.mjs
// Les cartes soulignées le sont d'après le VERDICT de regles.js, pas d'après
// une règle réécrite ici.
import { test } from "node:test";
import assert from "node:assert/strict";
import { cartesFautives } from "../../public/js/deckbuilder/fautives.js";
import { validerDeck, reglesAspect } from "../../public/js/deckbuilder/regles.js";

const CARTES = {
    p1: { name: "Counter-Punch", type: "Event", class: "Protection", desc: { Cost: "0" } },
    p2: { name: "Armored Vest", type: "Upgrade", class: "Protection", desc: { Cost: "0" } },
    j1: { name: "Get Ready", type: "Event", class: "Justice", desc: { Cost: "0" } },
    b1: { name: "Emergency", type: "Event", class: "Basic", desc: { Cost: "0" } },
};
const carte = (id) => CARTES[id];
const heros = { id: "colossus", name: "Colossus", deck: { hero_deck: Array.from({ length: 15 }, (_, i) => `k${i}`) } };

function verdict(choisies) {
    return validerDeck({ hero: heros, choisies, carte });
}

test("un deck valide ne souligne rien", () => {
    const choisies = new Map([["p1", 3], ["p2", 3], ["b1", 3]]);
    const v = { ok: true, problemes: [], aspects: ["Protection"] };
    assert.equal(cartesFautives({ choisies, carte, verdict: v, regle: reglesAspect(heros) }).size, 0);
});

test("trop d'exemplaires : la carte citée est soulignée", () => {
    const choisies = new Map([["p1", 4], ["b1", 1]]);
    const v = verdict(choisies);
    assert.equal(v.ok, false);
    const f = cartesFautives({ choisies, carte, verdict: v, regle: reglesAspect(heros) });
    assert.deepEqual([...f], ["p1"]);
});

test("héros à un aspect : l'aspect minoritaire est souligné, pas le basique", () => {
    const choisies = new Map([["p1", 3], ["p2", 3], ["j1", 1], ["b1", 3]]);
    const v = verdict(choisies);
    assert.equal(v.ok, false);
    const f = cartesFautives({ choisies, carte, verdict: v, regle: reglesAspect(heros) });
    assert.deepEqual([...f], ["j1"]);
});

test("un deck trop petit ne souligne aucune carte en particulier", () => {
    const choisies = new Map([["p1", 1]]);
    const v = verdict(choisies);
    assert.equal(v.ok, false);
    assert.equal(cartesFautives({ choisies, carte, verdict: v, regle: reglesAspect(heros) }).size, 0);
});
