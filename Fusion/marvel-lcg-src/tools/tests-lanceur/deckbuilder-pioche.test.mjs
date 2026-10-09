// node --test tools/tests-lanceur/deckbuilder-pioche.test.mjs
import { test } from "node:test";
import assert from "node:assert/strict";
import { construirePaquet, melanger, probaAuMoinsUne, probasParTour } from "../../public/js/deckbuilder/pioche.js";

test("le paquet contient le kit et chaque exemplaire choisi", () => {
    const p = construirePaquet(["a1,a2", "b"], new Map([["x", 3], ["y", 1]]));
    assert.deepEqual(p, ["a1", "b", "x", "x", "x", "y"]);
});

test("le mélange garde toutes les cartes", () => {
    const p = ["a", "b", "c", "d", "e"];
    let graine = 0.37;
    const m = melanger(p, () => { graine = (graine * 9301 + 49297) % 1; return graine; });
    assert.deepEqual([...m].sort(), p);
    assert.deepEqual(p, ["a", "b", "c", "d", "e"]);
});

test("3 exemplaires sur 40 cartes, main de 6 : 1 - (34·33·32)/(40·39·38)", () => {
    const p = probaAuMoinsUne(40, 3, 6);
    assert.ok(Math.abs(p - (1 - (34 * 33 * 32) / (40 * 39 * 38))) < 1e-9, `obtenu ${p}`);
});

test("cas limites : aucun exemplaire, tout le paquet tiré, paquet vide", () => {
    assert.equal(probaAuMoinsUne(40, 0, 6), 0);
    assert.equal(probaAuMoinsUne(40, 1, 40), 1);
    assert.equal(probaAuMoinsUne(40, 1, 99), 1);
    assert.equal(probaAuMoinsUne(0, 1, 6), 0);
});

test("les chances montent tour après tour", () => {
    const t = probasParTour(40, 1, 6);
    assert.deepEqual(t.map((x) => x.tour), [1, 2, 3]);
    assert.ok(t[0].proba < t[1].proba && t[1].proba < t[2].proba);
    assert.ok(Math.abs(t[0].proba - 6 / 40) < 1e-9);
});
