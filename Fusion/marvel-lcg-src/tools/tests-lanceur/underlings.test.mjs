// Tests du module pur `public/js/prepare/underlings.js` (Fear No Evil).
//
//     node --test tools/tests-lanceur/underlings.test.mjs
import { test } from "node:test";
import assert from "node:assert/strict";
import { regrouperUnderlings, scenarioDuVilain, tuileContient, nomDeManigance, nomDuVilain } from "../../public/js/prepare/underlings.js";

const sc = (id, name, villain) => ({ id, name, villainCards: [villain], tileImage: villain });
const ext = { manigances: ["art_museum_heist", "the_getaway"], underlings: ["hammerhead", "bullseye", "electro"] };
const catalogue = [
    sc("art_museum_heist_hammerhead", "Art Museum Heist (Hammerhead)", "60086"),
    sc("kingpin", "Kingpin", "60159a"),
    sc("art_museum_heist_bullseye", "Art Museum Heist (Bullseye)", "60065"),
    sc("the_getaway_electro", "The Getaway (Electro)", "60076"),
];

test("une tuile par manigance, dans l'ordre du catalogue, Kingpin garde la sienne", () => {
    const tuiles = regrouperUnderlings(catalogue, ext, {});
    assert.deepEqual(tuiles.map((t) => t.id), ["art_museum_heist", "kingpin", "the_getaway"]);
    const amh = tuiles[0];
    assert.equal(amh.name, "Art Museum Heist");
    assert.equal(amh.interchangeable, true);
    // Les vilains dans l'ordre de l'extension, pas du catalogue.
    assert.deepEqual(amh.underlings.map((u) => [u.id, u.nom, u.villainCardId]), [
        ["hammerhead", "Hammerhead", "60086"],
        ["bullseye", "Bullseye", "60065"],
    ]);
    assert.deepEqual(amh.scenarioIds, ["art_museum_heist_hammerhead", "art_museum_heist_bullseye"]);
    assert.equal(amh.courant.id, "hammerhead");
    assert.equal(tuiles[1].interchangeable, undefined);
});

test("la memoire choisit le vilain montre par la tuile ; une memoire perimee retombe sur le premier", () => {
    const [amh] = regrouperUnderlings(catalogue, ext, { art_museum_heist: "bullseye" });
    assert.equal(amh.courant.id, "bullseye");
    assert.equal(amh.villainCards[0], "60065");
    const [amh2] = regrouperUnderlings(catalogue, ext, { art_museum_heist: "disparu" });
    assert.equal(amh2.courant.id, "hammerhead");
});

test("une manigance a un seul vilain porte a sa tuile, sans modale (un seul choix)", () => {
    const getaway = regrouperUnderlings(catalogue, ext, {})[2];
    assert.equal(getaway.underlings.length, 1);
    assert.equal(scenarioDuVilain(getaway, "n'importe").id, "the_getaway_electro");
});

test("scenarioDuVilain et tuileContient", () => {
    const [amh] = regrouperUnderlings(catalogue, ext, {});
    assert.equal(scenarioDuVilain(amh, "bullseye").id, "art_museum_heist_bullseye");
    assert.equal(scenarioDuVilain(amh, "electro").id, "art_museum_heist_hammerhead");
    assert.equal(tuileContient(amh, "art_museum_heist_bullseye"), true);
    assert.equal(tuileContient(amh, "kingpin"), false);
    assert.equal(tuileContient({ id: "kingpin" }, "kingpin"), true);
});

test("sans declaration d'underlings, la liste est rendue telle quelle", () => {
    assert.deepEqual(regrouperUnderlings(catalogue, {}, {}).map((t) => t.id), catalogue.map((s) => s.id));
});

test("les noms", () => {
    assert.equal(nomDeManigance("Art Museum Heist (Hammerhead)"), "Art Museum Heist");
    assert.equal(nomDeManigance("Kingpin"), "Kingpin");
    assert.equal(nomDuVilain("Art Museum Heist (Typhoid Mary)", "typhoid_mary"), "Typhoid Mary");
    assert.equal(nomDuVilain("sans parenthese", "purple_man"), "Purple Man");
});
