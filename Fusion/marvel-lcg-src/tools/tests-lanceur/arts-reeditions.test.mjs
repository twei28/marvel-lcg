// node --test tools/tests-lanceur/arts-reeditions.test.mjs
import { test } from "node:test";
import assert from "node:assert/strict";
import { versionsDe, versionDansLeDeck, changerVersion } from "../../public/js/deckbuilder/arts-reeditions.js";

test("une carte réimprimée avec un autre art liste ses versions, origine en tête", () => {
    assert.deepEqual(versionsDe("01072"), ["01072", "45019"]);
    assert.deepEqual(versionsDe("45019"), ["01072", "45019"]);
    assert.deepEqual(versionsDe("12030"), ["12030", "43017", "ma026"]);
});

test("une carte sans autre illustration n'a pas de versions", () => {
    assert.deepEqual(versionsDe("01189"), []);
    assert.deepEqual(versionsDe("01088"), []);
});

test("retrouve la version présente dans le deck", () => {
    assert.equal(versionDansLeDeck("01072", new Map([["45019", 2]])), "45019");
    assert.equal(versionDansLeDeck("01072", new Map()), null);
});

test("changer de version déplace toutes les copies sans en perdre", () => {
    const deck = new Map([["01072", 2], ["01088", 1]]);
    changerVersion(deck, "45019");
    assert.deepEqual([...deck], [["01088", 1], ["45019", 2]]);
});

test("changer de version d'une carte absente du deck ne l'y ajoute pas", () => {
    const deck = new Map();
    changerVersion(deck, "45019");
    assert.equal(deck.size, 0);
});
