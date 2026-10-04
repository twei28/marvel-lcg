// Tests du module pur `public/js/prepare/arts-heros-choix.js`.
//
//     node --test tools/tests-lanceur/arts-heros-choix.test.mjs
import { test } from "node:test";
import assert from "node:assert/strict";
import {
    cleHeros, lireChoix, changementsPour, appliquer, codeAlterEgoAffiche, reconcilier, memesArts,
} from "../../public/js/prepare/arts-heros-choix.js";

test("la clé du héros ignore la face", () => {
    assert.equal(cleHeros("38001a"), "38001");
    assert.equal(cleHeros("38001a,38001b"), "38001");
    assert.equal(cleHeros("gp001a"), "gp001");
});

test("lecture : standard par défaut, l'alter ego suit tant qu'il n'a pas le sien", () => {
    assert.deepEqual(lireChoix({}, "15001a"), { heros: "standard", alterEgo: null });
    assert.deepEqual(lireChoix({ 15001: "rog" }, "15001a"), { heros: "rog", alterEgo: null });
    assert.deepEqual(lireChoix({ 15001: "rog", "15001b": "cb" }, "15001a"), { heros: "rog", alterEgo: "cb" });
});

test("changements : standard efface la clé du héros, null laisse l'alter ego suivre", () => {
    assert.deepEqual(changementsPour("15001a", "rog", null), { 15001: "rog", "15001b": null });
    assert.deepEqual(changementsPour("15001a", "standard", null), { 15001: null, "15001b": null });
    assert.deepEqual(changementsPour("15001a", "rog", "standard"), { 15001: "rog", "15001b": "standard" });
    assert.deepEqual(changementsPour("", "rog", null), {});
});

test("appliquer ne modifie pas la table d'origine", () => {
    const avant = { 15001: "rog", "15001b": "cb" };
    const apres = appliquer(avant, { 15001: null, 38001: "cb" });
    assert.deepEqual(apres, { "15001b": "cb", 38001: "cb" });
    assert.deepEqual(avant, { 15001: "rog", "15001b": "cb" });
});

test("l'alter ego affiche son art, celui du héros s'il l'a, sinon son scan", () => {
    assert.equal(codeAlterEgoAffiche({ heros: "rog", alterEgo: null }, ["cb", "rog"]), "rog");
    assert.equal(codeAlterEgoAffiche({ heros: "m3t", alterEgo: null }, ["cb"]), "standard");
    assert.equal(codeAlterEgoAffiche({ heros: "rog", alterEgo: "cb" }, ["cb", "rog"]), "cb");
    assert.equal(codeAlterEgoAffiche({ heros: "rog", alterEgo: "standard" }, ["cb", "rog"]), "standard");
    assert.equal(codeAlterEgoAffiche({ heros: "rog", alterEgo: null }, undefined), "standard");
});

test("réconciliation : un invité ou un moteur local garde son navigateur", () => {
    assert.equal(reconcilier({ 1: "cb" }, { compte: false, existe: false, arts: {} }), null);
    assert.equal(reconcilier({ 1: "cb" }, null), null);
});

test("réconciliation : premier passage, le compte reçoit le navigateur", () => {
    const r = reconcilier({ 15001: "rog" }, { compte: true, existe: false, arts: {} });
    assert.deepEqual(r, { arts: { 15001: "rog" }, pousser: { 15001: "rog" } });
    assert.deepEqual(reconcilier({}, { compte: true, existe: false, arts: {} }), { arts: {}, pousser: {} });
});

test("réconciliation : le fichier du compte fait foi, une clé locale en trop disparaît", () => {
    const r = reconcilier({ 15001: "rog", 38001: "cb" }, { compte: true, existe: true, arts: { 15001: "cb" } });
    assert.deepEqual(r, { arts: { 15001: "cb" }, pousser: {} });
});

test("memesArts compare sans tenir compte de l'ordre", () => {
    assert.ok(memesArts({ a: "1", b: "2" }, { b: "2", a: "1" }));
    assert.ok(!memesArts({ a: "1" }, { a: "2" }));
    assert.ok(!memesArts({ a: "1" }, {}));
});
