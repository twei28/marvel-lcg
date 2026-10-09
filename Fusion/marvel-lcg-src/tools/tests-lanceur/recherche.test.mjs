// node --test tools/tests-lanceur/recherche.test.mjs
import { test } from "node:test";
import assert from "node:assert/strict";
import { correspondRecherche } from "../../public/js/deckbuilder/recherche.js";
import { NOMS_FR } from "../../public/js/prepare/noms-fr.js";

const tanteMay = { card_id: "01006", name: "Aunt May", text: "", traits: ["PERSONA"] };
const opts = { nomsFr: NOMS_FR };

test("trouve une carte par son nom français officiel", () => {
    assert.equal(correspondRecherche(tanteMay, "tante may", opts), true);
});

test("trouve toujours par le nom anglais", () => {
    assert.equal(correspondRecherche(tanteMay, "Aunt", opts), true);
});

test("ignore les accents et les apostrophes typographiques", () => {
    const salto = { card_id: "01003", name: "Backflip", text: "" };
    assert.equal(correspondRecherche(salto, "salto arriere", opts), true);
    const sens = { card_id: "01004", name: "Enhanced Spider-Sense", text: "" };
    assert.equal(correspondRecherche(sens, "sens d’araignee", opts), true);
});

test("refuse une carte qui ne correspond pas", () => {
    assert.equal(correspondRecherche(tanteMay, "lance-toile", opts), false);
});

test("une requête vide laisse tout passer", () => {
    assert.equal(correspondRecherche(tanteMay, "  ", opts), true);
});
