// Tests du module pur `public/js/prepare/titres-extensions.js`.
//
//     node --test tools/tests-lanceur/titres-extensions.test.mjs
import { test } from "node:test";
import assert from "node:assert/strict";
import { nomExtension, numeroDExtension, titreDeBoite, TITRES_FR } from "../../public/js/prepare/titres-extensions.js";

test("en français, une boîte porte son titre imprimé en France", () => {
    assert.equal(nomExtension("4. The Rise of Red Skull"), "L’Avènement de Crâne Rouge");
    assert.equal(nomExtension("60. Fear No Evil", "fr"), "Peur de Rien");
    assert.equal(nomExtension("16. Galaxy's Most Wanted"), "Convoitise Galactique");
    assert.equal(nomExtension("32. Mutant Genesis"), "La Genèse des Mutants");
    assert.equal(nomExtension("1. Core Set"), "Set de base");
});

test("en anglais, la clé sans son numéro, jamais la table française", () => {
    assert.equal(nomExtension("4. The Rise of Red Skull", "en"), "The Rise of Red Skull");
    assert.equal(nomExtension("60. Fear No Evil", "en"), "Fear No Evil");
});

test("un titre identique dans les deux langues n'a pas de ligne et reste tel quel", () => {
    assert.equal(nomExtension("56. Civil War"), "Civil War");
    assert.equal(nomExtension("3. Captain America"), "Captain America");
    assert.equal(nomExtension("99. Custom (Rainy)"), "Custom (Rainy)");
});

test("une clé sans numéro ou vide ne casse rien", () => {
    assert.equal(nomExtension("defis"), "defis");
    assert.equal(nomExtension(""), "");
    assert.equal(nomExtension(undefined), "");
    assert.equal(numeroDExtension("Custom"), null);
    assert.equal(numeroDExtension("12. Ant-Man"), 12);
});

test("le titre d'une vague suit la même table", () => {
    assert.equal(titreDeBoite("The Mad Titan's Shadow"), "L’Ombre du Titan Fou");
    assert.equal(titreDeBoite("The Mad Titan's Shadow", "en"), "The Mad Titan's Shadow");
    assert.equal(titreDeBoite("NeXt Evolution"), "NeXt Evolution");
    assert.equal(titreDeBoite(""), "");
});

test("la table ne contient que des numéros et des titres non vides", () => {
    for (const [k, v] of Object.entries(TITRES_FR)) {
        assert.match(k, /^\d+$/);
        assert.ok(v && v.trim().length > 2, k);
    }
});
