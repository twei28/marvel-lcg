// Tests du module pur `public/js/prepare/affichage-choix.js`.
//
//     node --test tools/tests-lanceur/affichage-choix.test.mjs
import { test } from "node:test";
import assert from "node:assert/strict";
import { normaliser, inverse, reconcilier, CLE_AFFICHAGE } from "../../public/js/prepare/affichage-choix.js";

test("la clé est celle que lit le plateau", () => {
    assert.equal(CLE_AFFICHAGE, "mc_affichage_v1");
});

test("toute valeur inconnue vaut normal", () => {
    for (const v of [undefined, null, "", "fluo", "SOBRE", 1]) assert.equal(normaliser(v), "normal");
    assert.equal(normaliser("sobre"), "sobre");
});

test("inverse bascule entre les deux modes", () => {
    assert.equal(inverse("normal"), "sobre");
    assert.equal(inverse("sobre"), "normal");
    assert.equal(inverse(undefined), "sobre");
});

test("invité ou moteur local : le navigateur reste maître", () => {
    assert.equal(reconcilier("sobre", { compte: false, existe: false, preferences: {} }), null);
    assert.equal(reconcilier("sobre", null), null);
});

test("compte sans fichier : le choix du navigateur y est versé", () => {
    assert.deepEqual(reconcilier("sobre", { compte: true, existe: false, preferences: {} }),
        { affichage: "sobre", pousser: { affichage: "sobre" } });
    // Le défaut n'a rien à verser.
    assert.deepEqual(reconcilier(null, { compte: true, existe: false, preferences: {} }),
        { affichage: "normal", pousser: {} });
});

test("compte avec fichier : il fait foi, même sans clé d'affichage", () => {
    assert.deepEqual(reconcilier("normal", { compte: true, existe: true, preferences: { affichage: "sobre" } }),
        { affichage: "sobre", pousser: {} });
    assert.deepEqual(reconcilier("sobre", { compte: true, existe: true, preferences: {} }),
        { affichage: "normal", pousser: {} });
});

import { doitProposerLeChoix } from "../../public/js/prepare/affichage-choix.js";

test("jamais choisi (rien dans le navigateur, pas de compte) : on propose la fenêtre", () => {
    assert.equal(doitProposerLeChoix(null, null), true);
    assert.equal(doitProposerLeChoix(null, { compte: false, existe: false, preferences: {} }), true);
});

test("déjà choisi dans ce navigateur, même « normal » : on ne propose plus", () => {
    assert.equal(doitProposerLeChoix("normal", null), false);
    assert.equal(doitProposerLeChoix("sobre", null), false);
});

test("déjà choisi sur le compte, depuis un autre appareil : on ne propose plus", () => {
    assert.equal(doitProposerLeChoix(null, { compte: true, existe: true, preferences: { affichage: "normal" } }), false);
});

test("compte sans ce réglage (ancien joueur) : on propose, une fois", () => {
    assert.equal(doitProposerLeChoix(null, { compte: true, existe: true, preferences: { arts: {} } }), true);
    assert.equal(doitProposerLeChoix(null, { compte: true, existe: false, preferences: {} }), true);
});
