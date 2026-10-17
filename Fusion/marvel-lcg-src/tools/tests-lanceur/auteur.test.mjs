// Tests du module pur `public/js/prepare/auteur.js`.
//
//     node --test tools/tests-lanceur/auteur.test.mjs
//
// Le nom d'un héros fan-made s'affiche suivi de son créateur entre
// parenthèses (demande du 18/09/2026). Le créateur est le champ `custom`
// de la face héros dans cards.json.
import { test } from "node:test";
import assert from "node:assert/strict";
import { nomAvecAuteur } from "../../public/js/prepare/auteur.js";

test("un héros fan-made porte son créateur entre parenthèses", () => {
    assert.equal(nomAvecAuteur("Lockjaw", "Nugget", true), "Lockjaw (Nugget)");
});

test("un héros officiel ne porte rien, même si un auteur traîne", () => {
    assert.equal(nomAvecAuteur("Thor", "Rainy", false), "Thor");
});

test("un fan-made sans créateur connu garde son nom nu", () => {
    assert.equal(nomAvecAuteur("Squirrel Girl", "", true), "Squirrel Girl");
    assert.equal(nomAvecAuteur("Squirrel Girl", undefined, true), "Squirrel Girl");
});

test("le créateur déjà dans le libellé des homonymes n'est pas répété", () => {
    // leverLesHomonymes a déjà rebaptisé la tuile « Spider-Man (Rainy) ».
    assert.equal(nomAvecAuteur("Spider-Man (Rainy)", "Rainy", true), "Spider-Man (Rainy)");
    assert.equal(nomAvecAuteur("Yondu", "BlueHG + DesignHacker", true), "Yondu (BlueHG + DesignHacker)");
});

test("la casse du créateur ne compte pas pour la répétition", () => {
    assert.equal(nomAvecAuteur("Hulk (RAINY)", "Rainy", true), "Hulk (RAINY)");
});

import { createursDe, createursDeTout } from "../../public/js/prepare/auteur.js";

test("les créateurs sont listés une fois, séparés sur le « + », triés", () => {
    const heroes = [
        { homebrew: true, auteur: "Rainy" },
        { homebrew: true, auteur: "BlueHG + DesignHacker" },
        { homebrew: true, auteur: "DesignHacker" },
        { homebrew: true, auteur: "rainy" },
        { homebrew: true, auteur: "" },
        { homebrew: false, auteur: "Officiel" },
    ];
    assert.deepEqual(createursDe(heroes), ["BlueHG", "DesignHacker", "Rainy"]);
});

test("aucun créateur : liste vide, pas de phrase", () => {
    assert.deepEqual(createursDe([]), []);
    assert.deepEqual(createursDe([{ homebrew: true }]), []);
});

import { auteurUnique } from "../../public/js/prepare/auteur.js";

test("un set dont toutes les cartes portent le meme createur le rend", () => {
    assert.equal(auteurUnique(["BlueHG", "BlueHG", "BlueHG"]), "BlueHG");
    assert.equal(auteurUnique(["Rainy"]), "Rainy");
});

test("deux createurs, ou une carte officielle melee, ne rendent rien", () => {
    // Le set « Electro » existe en officiel ET chez Ripper3 : ne rien attribuer.
    assert.equal(auteurUnique(["Ripper3", undefined]), "");
    assert.equal(auteurUnique([undefined, "Ripper3"]), "");
    assert.equal(auteurUnique(["BlueHG", "DesignHacker"]), "");
    assert.equal(auteurUnique(["Rainy", ""]), "");
});

test("un set officiel ou vide ne rend rien", () => {
    assert.equal(auteurUnique([]), "");
    assert.equal(auteurUnique([undefined, undefined]), "");
    assert.equal(auteurUnique(null), "");
});

test("les créateurs d'extensions donnés à la main (16/10/2026)", async () => {
    const { auteurConnuDeLExtension } = await import("../../public/js/prepare/auteur.js");
    assert.equal(auteurConnuDeLExtension("Web of Deceit"), "Ripper3");
    assert.equal(auteurConnuDeLExtension("  gorr the god butcher "), "BlueHG");
    assert.equal(auteurConnuDeLExtension("Skrull Menace"), "");
    assert.equal(auteurConnuDeLExtension(undefined), "");
});

test("createursDeTout : héros et extensions fan-made réunis, chacun une fois, officiels exclus", () => {
    const heroes = [
        { homebrew: true, auteur: "Inkwire" },
        { homebrew: true, auteur: "BlueHG + DesignHacker" },
        { homebrew: false, auteur: "Marvel" },
    ];
    assert.deepEqual(
        createursDeTout(heroes, ["Inkwire", "Ripper3", "", undefined]),
        ["BlueHG", "DesignHacker", "Inkwire", "Ripper3"],
    );
    assert.deepEqual(createursDeTout([], []), []);
    assert.deepEqual(createursDeTout(null, null), []);
});
