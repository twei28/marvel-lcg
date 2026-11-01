// Tests du module pur `public/js/prepare/difficulte-logique.js`.
//
//     node --test tools/tests-lanceur/difficulte-logique.test.mjs
import { test } from "node:test";
import assert from "node:assert/strict";
import {
    basculerSet, combinaisonsDuScenario, difficulteEstimee, estJouable, filtrerGroupes, grouperParBoite,
    libelleDifficulte, nombreMaxDeSets, normaliser, raisonGrisee,
} from "../../public/js/prepare/difficulte-logique.js";
import { VILLAINTHEORY } from "../../public/js/prepare/villaintheory.js";

const combo = (o) => ({ scenarios: ["rhino"], nom: "X", defaut: false, difficulte: 0, incertain: false, sets: [], manquants: [], ...o });

test("la recherche ignore accents, casse et ponctuation", () => {
    assert.equal(normaliser("Alerte à la Bombe !"), "alerte a la bombe");
    assert.equal(normaliser("S.H.I.E.L.D."), "s h i e l d");
});

test("les propositions d'un scénario : le défaut d'abord, puis du plus facile au plus dur", () => {
    const donnees = { combinaisons: [
        combo({ nom: "Dur", difficulte: 3 }),
        combo({ nom: "Autre scénario", scenarios: ["klaw"] }),
        combo({ nom: "Défaut", defaut: true }),
        combo({ nom: "Facile", difficulte: -1 }),
    ] };
    assert.deepEqual(combinaisonsDuScenario("rhino", donnees).map((c) => c.nom), ["Défaut", "Facile", "Dur"]);
});

test("une proposition avec un set absent du jeu est grisée, avec la raison", () => {
    assert.equal(estJouable(combo({})), true);
    const grisee = combo({ manquants: ["Armadillo"] });
    assert.equal(estJouable(grisee), false);
    assert.equal(raisonGrisee(grisee), "Set « Armadillo » absent du jeu");
    assert.equal(raisonGrisee(combo({ manquants: ["A", "B"] })), "Sets absents du jeu : A, B");
    assert.equal(raisonGrisee(combo({})), "");
});

test("libellé de difficulté : signe typographique, point d'interrogation si l'auteur doute", () => {
    assert.equal(libelleDifficulte(2), "+2");
    assert.equal(libelleDifficulte(0), "+0");
    assert.equal(libelleDifficulte(-1), "−1");
    assert.equal(libelleDifficulte(3, true), "+3?");
    assert.equal(libelleDifficulte(null), "");
});

test("difficulté estimée : la note de la proposition exacte, +0 pour le recommandé, sinon rien", () => {
    const props = [combo({ nom: "Stay Hydrated", difficulte: 1, sets: ["hydra_patrol"] }),
                   combo({ nom: "Défaut", defaut: true, sets: ["bomb_scare"] })];
    assert.deepEqual(difficulteEstimee(["hydra_patrol"], ["bomb_scare"], props),
        { valeur: 1, incertain: false, source: "villaintheory", nom: "Stay Hydrated" });
    assert.equal(difficulteEstimee(["bomb_scare"], ["bomb_scare"], props).source, "recommande");
    assert.equal(difficulteEstimee(["bomb_scare"], ["bomb_scare"], props).valeur, 0);
    assert.equal(difficulteEstimee(["hydra_patrol", "bomb_scare"], ["bomb_scare"], props).valeur, null);
});

test("sets rangés par boîte : boîtes dans l'ordre, sets par nom, sans boîte à la fin", () => {
    const sets = [
        { name: "b", displayName: "Zeta" }, { name: "a", displayName: "Alpha" },
        { name: "c", displayName: "Omega" }, { name: "x", displayName: "Orphelin" },
    ];
    const boites = { a: "2. Deux", b: "2. Deux", c: "1. Un" };
    const groupes = grouperParBoite(sets, (n) => boites[n] || "", (k) => parseInt(k, 10) || 0, (k) => k.replace(/^\d+\.\s*/, ""));
    assert.deepEqual(groupes.map((g) => g.titre), ["Un", "Deux", "Autres"]);
    assert.deepEqual(groupes[1].sets.map((s) => s.displayName), ["Alpha", "Zeta"]);
});

test("filtre : par nom de set, ou par boîte entière", () => {
    const groupes = [
        { cle: "1", titre: "Set de base", sets: [{ displayName: "Alerte à la Bombe" }, { displayName: "Sous Attaque" }] },
        { cle: "2", titre: "Le Bouffon Vert", sets: [{ displayName: "Power Drain" }] },
    ];
    assert.equal(filtrerGroupes(groupes, "").length, 2);
    assert.deepEqual(filtrerGroupes(groupes, "bombe").map((g) => g.sets.length), [1]);
    assert.equal(filtrerGroupes(groupes, "bouffon")[0].sets.length, 1);
    assert.equal(filtrerGroupes(groupes, "zzz").length, 0);
});

test("basculer un set : ajoute, retire, sans doublon", () => {
    assert.deepEqual(basculerSet(["a"], "b"), ["a", "b"]);
    assert.deepEqual(basculerSet(["a", "b"], "a"), ["b"]);
});

test("données importées : chaque proposition a des sets connus ou des manquants, et vise un scénario du jeu", () => {
    assert.ok(VILLAINTHEORY.combinaisons.length > 500);
    for (const c of VILLAINTHEORY.combinaisons) {
        assert.ok(c.scenarios.length > 0, c.nom + " sans scénario");
        assert.ok(c.sets.length + c.manquants.length > 0, c.nom + " sans set");
        assert.ok(Number.isInteger(c.difficulte), c.nom + " sans difficulté");
    }
});

test("données importées : tous les identifiants de sets existent dans data/encounter_sets", async () => {
    const { existsSync } = await import("node:fs");
    const { fileURLToPath } = await import("node:url");
    const dossier = fileURLToPath(new URL("../../data/encounter_sets/", import.meta.url));
    const inconnus = new Set();
    for (const c of VILLAINTHEORY.combinaisons) for (const s of c.sets) if (!existsSync(dossier + s + ".json")) inconnus.add(s);
    assert.deepEqual([...inconnus], []);
});

test("données importées : Rhino a sa proposition « Stay Hydrated » avec Hydra Patrol", () => {
    const rhino = combinaisonsDuScenario("rhino", VILLAINTHEORY);
    const hydrate = rhino.find((c) => c.nom.startsWith("Stay Hydrated"));
    assert.ok(hydrate, "Stay Hydrated introuvable pour Rhino");
    assert.deepEqual(hydrate.sets, ["hydra_patrol"]);
    assert.equal(hydrate.difficulte, 1);
});

test("plafond de sets : 8 au moins, davantage si le scénario en recommande plus", () => {
    assert.equal(nombreMaxDeSets({ modularSlots: { max: 4 } }), 8);
    assert.equal(nombreMaxDeSets({ modularSlots: { max: 10 } }), 10);
    assert.equal(nombreMaxDeSets(null), 8);
    assert.ok(Math.max(...VILLAINTHEORY.combinaisons.map((c) => c.sets.length)) <= nombreMaxDeSets(null));
});
