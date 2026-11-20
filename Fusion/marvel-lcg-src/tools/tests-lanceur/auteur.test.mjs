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

// ---- 26/10/2026 : « Phenexian and Mysteltainn » sont DEUX personnes ----
import { separerCreateurs } from "../../public/js/prepare/auteur.js";

test("« X and Y », « X et Y », « X + Y », « X & Y » : deux créateurs distincts", () => {
    assert.deepEqual(separerCreateurs("Phenexian and Mysteltainn"), ["Phenexian", "Mysteltainn"]);
    assert.deepEqual(separerCreateurs("Phenexian et Mysteltainn"), ["Phenexian", "Mysteltainn"]);
    assert.deepEqual(separerCreateurs("BlueHG + DesignHacker"), ["BlueHG", "DesignHacker"]);
    assert.deepEqual(separerCreateurs("A & B"), ["A", "B"]);
});

test("un nom seul reste un nom, les espaces et les vides sont ignorés", () => {
    assert.deepEqual(separerCreateurs("  Dipsome "), ["Dipsome"]);
    assert.deepEqual(separerCreateurs(""), []);
    assert.deepEqual(separerCreateurs(undefined), []);
    assert.deepEqual(separerCreateurs("Grawlix Ipsum"), ["Grawlix Ipsum"]);
});

test("« and » dans un nom plus long n'est pas un séparateur", () => {
    assert.deepEqual(separerCreateurs("Sandra Anderson"), ["Sandra Anderson"]);
    assert.deepEqual(separerCreateurs("Brandon"), ["Brandon"]);
});

test("la ligne de remerciement compte Phenexian et Mysteltainn une fois chacun", () => {
    const heroes = [
        { homebrew: true, auteur: "Phenexian and Mysteltainn" },
        { homebrew: true, auteur: "Phenexian" },
        { homebrew: true, auteur: "Mysteltainn" },
        { homebrew: true, auteur: "phenexian and mysteltainn" },
    ];
    assert.deepEqual(createursDe(heroes), ["Mysteltainn", "Phenexian"]);
    assert.deepEqual(createursDeTout([], ["Phenexian and Mysteltainn", "Mysteltainn"]), ["Mysteltainn", "Phenexian"]);
});

test("l'affichage derrière le nom du héros reste le libellé imprimé sur les cartes", () => {
    assert.equal(nomAvecAuteur("Corsair", "Phenexian and Mysteltainn", true), "Corsair (Phenexian and Mysteltainn)");
});
