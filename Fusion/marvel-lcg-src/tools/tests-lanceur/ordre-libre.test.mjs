// Tests du module pur `public/js/campagne/ordre-libre.js` (campagne Fear No Evil).
//
//     node --test tools/tests-lanceur/ordre-libre.test.mjs
import { test } from "node:test";
import assert from "node:assert/strict";
import {
    affaires, scenarioFinal, etatAffaire, marques, affairesOuvertes, kingpinDisponible,
    tirerLaProgression, vilainsPossibles, inscrireLeVilain, scenarioDuCatalogue, appliquerLaDefaite,
    CLE_COMPLETED, CLE_FAILED,
} from "../../public/js/campagne/ordre-libre.js";

const definition = {
    vilains: [
        { id: "hammerhead", nom: "Hammerhead", ordre: 1 },
        { id: "bullseye", nom: "Bullseye", ordre: 2 },
        { id: "electro", nom: "Electro", ordre: 3 },
        { id: "purple_man", nom: "Purple Man", ordre: 4 },
        { id: "typhoid_mary", nom: "Typhoid Mary", ordre: 4 },
    ],
    scenarios: [
        { id: "art_museum_heist", manigance: true },
        { id: "the_getaway", manigance: true },
        { id: "protection_racket", manigance: true },
        { id: "the_raft_breakout", manigance: true },
        { id: "stop_the_presses", manigance: true },
        { id: "kingpin", catalogue: "kingpin_fne", final: true },
    ],
};
const des = (...valeurs) => { let i = 0; return () => valeurs[i++ % valeurs.length]; };

test("affaires et final : cinq manigances, Kingpin à part", () => {
    assert.equal(affaires(definition).length, 5);
    assert.equal(scenarioFinal(definition).id, "kingpin");
});

test("état d'une affaire : Completed, Failed, sinon ouverte", () => {
    const carnet = { [CLE_COMPLETED]: "the_getaway;art_museum_heist", [CLE_FAILED]: "stop_the_presses" };
    assert.equal(etatAffaire(carnet, "the_getaway"), "completed");
    assert.equal(etatAffaire(carnet, "stop_the_presses"), "failed");
    assert.equal(etatAffaire(carnet, "protection_racket"), "ouverte");
    assert.deepEqual(affairesOuvertes(definition, carnet).map((a) => a.id), ["protection_racket", "the_raft_breakout"]);
    assert.equal(kingpinDisponible(definition, carnet), false);
});

test("Kingpin n'est disponible que lorsque tout est résolu", () => {
    const carnet = { [CLE_COMPLETED]: "the_getaway;art_museum_heist;protection_racket", [CLE_FAILED]: "stop_the_presses;the_raft_breakout" };
    assert.equal(kingpinDisponible(definition, carnet), true);
});

test("progression : deux affaires ouvertes tirées au hasard, une marque chacune", () => {
    const { carnet, tirees, echouees } = tirerLaProgression(definition, {}, des(0, 0));
    assert.deepEqual(tirees, ["art_museum_heist", "the_getaway"]);
    assert.equal(marques(carnet, "art_museum_heist"), 1);
    assert.equal(marques(carnet, "the_getaway"), 1);
    assert.equal(marques(carnet, "protection_racket"), 0);
    assert.deepEqual(echouees, []);
});

test("progression : une seule affaire ouverte prend deux marques", () => {
    const carnet0 = { [CLE_COMPLETED]: "the_getaway;art_museum_heist;protection_racket", [CLE_FAILED]: "stop_the_presses" };
    const { carnet, tirees } = tirerLaProgression(definition, carnet0, des(0));
    assert.deepEqual(tirees, ["the_raft_breakout"]);
    assert.equal(marques(carnet, "the_raft_breakout"), 2);
});

test("progression : trois marques = affaire Failed, et le carnet d'entrée n'est pas modifié", () => {
    const carnet0 = { "Progress: art_museum_heist": "2" };
    const { carnet, echouees } = tirerLaProgression(definition, carnet0, des(0, 0));
    assert.deepEqual(echouees, ["art_museum_heist"]);
    assert.equal(etatAffaire(carnet, "art_museum_heist"), "failed");
    assert.equal(marques(carnet, "art_museum_heist"), 3);
    assert.equal(carnet0[CLE_FAILED], undefined);
});

test("progression : rien à tirer quand tout est résolu", () => {
    const carnet0 = { [CLE_COMPLETED]: "the_getaway;art_museum_heist;protection_racket;the_raft_breakout;stop_the_presses" };
    const { tirees } = tirerLaProgression(definition, carnet0, des(0));
    assert.deepEqual(tirees, []);
});

test("vilain : l'ordre recommandé au premier parcours, jamais deux fois le même", () => {
    let carnet = {};
    let v = vilainsPossibles(definition, carnet, "the_getaway");
    assert.equal(v.impose, null);
    assert.equal(v.suggere, "hammerhead");
    carnet = inscrireLeVilain(carnet, "the_getaway", "hammerhead");
    v = vilainsPossibles(definition, carnet, "art_museum_heist");
    assert.equal(v.suggere, "bullseye");
    assert.deepEqual(v.choix, ["bullseye", "electro", "purple_man", "typhoid_mary"]);
});

test("vilain : une affaire déjà jouée garde son vilain", () => {
    const carnet = { "Villain: the_getaway": "electro" };
    const v = vilainsPossibles(definition, carnet, "the_getaway");
    assert.equal(v.impose, "electro");
    assert.deepEqual(v.choix, ["electro"]);
});

test("scénario du catalogue : <affaire>_<vilain>, ou l'id de catalogue du final", () => {
    assert.equal(scenarioDuCatalogue({ id: "the_getaway" }, "bullseye"), "the_getaway_bullseye");
    assert.equal(scenarioDuCatalogue(scenarioFinal(definition), null), "kingpin_fne");
});

test("défaite sur une affaire : rien en standard, une marque en expert, Failed à la troisième", () => {
    const std = appliquerLaDefaite(definition, { "Progress: the_getaway": "2" }, "the_getaway", false);
    assert.equal(marques(std.carnet, "the_getaway"), 2);
    const exp = appliquerLaDefaite(definition, { "Progress: the_getaway": "2" }, "the_getaway", true);
    assert.equal(marques(exp.carnet, "the_getaway"), 3);
    assert.equal(exp.echouee, "the_getaway");
    assert.equal(etatAffaire(exp.carnet, "the_getaway"), "failed");
    assert.equal(exp.perdue, false);
});

test("défaite contre Kingpin : en expert on retourne un environnement Completed, sans il n'y a plus de campagne", () => {
    const carnet0 = { [CLE_COMPLETED]: "the_getaway;art_museum_heist", [CLE_FAILED]: "stop_the_presses" };
    const std = appliquerLaDefaite(definition, carnet0, "kingpin", false);
    assert.equal(std.perdue, false);
    assert.deepEqual(std.carnet, carnet0);
    const sansChoix = appliquerLaDefaite(definition, carnet0, "kingpin", true);
    assert.deepEqual(sansChoix.aChoisir, ["the_getaway", "art_museum_heist"]);
    const avec = appliquerLaDefaite(definition, carnet0, "kingpin", true, "the_getaway");
    assert.equal(etatAffaire(avec.carnet, "the_getaway"), "failed");
    assert.equal(etatAffaire(avec.carnet, "art_museum_heist"), "completed");
    assert.equal(avec.echouee, "the_getaway");
    const perdue = appliquerLaDefaite(definition, { [CLE_FAILED]: "the_getaway" }, "kingpin", true);
    assert.equal(perdue.perdue, true);
});
