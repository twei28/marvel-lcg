import { test } from "node:test";
import assert from "node:assert/strict";
import { CLE_FACON_DE_JOUER, faconParDefaut, lanceEnManuel, normaliser } from "../../public/js/prepare/facon-de-jouer.js";

test("une valeur inconnue ou absente vaut auto", () => {
    assert.equal(normaliser(undefined), "auto");
    assert.equal(normaliser(null), "auto");
    assert.equal(normaliser("n'importe quoi"), "auto");
    assert.equal(normaliser("manuel"), "manuel");
});

test("le défaut se lit sous la clé partagée avec le plateau", () => {
    const stockage = { getItem: (cle) => (cle === CLE_FACON_DE_JOUER ? "manuel" : null) };
    assert.equal(faconParDefaut(stockage), "manuel");
    assert.equal(faconParDefaut({ getItem: () => null }), "auto");
});

test("un stockage absent ou qui jette donne auto", () => {
    assert.equal(faconParDefaut(undefined), "auto");
    assert.equal(faconParDefaut({ getItem: () => { throw new Error("bloqué"); } }), "auto");
});

test("seul manuel lance la règle mode_manuel", () => {
    assert.equal(lanceEnManuel("manuel"), true);
    assert.equal(lanceEnManuel("auto"), false);
    assert.equal(lanceEnManuel(undefined), false);
});
