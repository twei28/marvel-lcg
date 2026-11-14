// Tests du verrou Legacy : les héros de la vague 1 sont libres dès le départ.
//
//     node --test tools/tests-lanceur/legacy-vague-1-libre.test.mjs
//
// Décision du 11/11/2026 : la vague 1 se joue avec le core set, sans jetons.
// Les scénarios de la vague 1 restent gardés par la progression.
import { test } from "node:test";
import assert from "node:assert/strict";
import { fabriquerVerrou } from "../../public/js/prepare/legacy-verrou.js";

const etat = {
    parcours: {
        etapes: [
            { vague: 0, nom: "Set de base", ouvert: true, franchi: false },
            { vague: 1, nom: "Vague 1", ouvert: false, franchi: false },
            { vague: 2, nom: "Vague 2", ouvert: false, franchi: false },
        ],
        jetons: { gagnes: 0, depenses: 0, restants: 0 },
        vagueOuverte: 0,
    },
    fiche: { jetonsDepenses: [] },
    paliers: [
        { vague: 1, scenarios: [{ nom: "Bouffon Vert" }] },
    ],
};

test("un héros de la vague 1 est ouvert sans franchir le Set de base", () => {
    const verrou = fabriquerVerrou(etat, [], (x) => x);
    const h = verrou.heros({ heroCardId: "01001a", vague: 1 });
    assert.equal(h.ouvert, true);
    assert.equal(h.condition, "");
});

test("un héros de la vague 2 reste fermé tant que la vague 1 n'est pas franchie", () => {
    const verrou = fabriquerVerrou(etat, [], (x) => x);
    const h = verrou.heros({ heroCardId: "02001a", vague: 2 });
    assert.equal(h.ouvert, false);
});

test("un scénario de la vague 1 reste gardé par la progression", () => {
    const verrou = fabriquerVerrou(etat, [], (x) => x);
    const sc = verrou.scenario({ name: "Bouffon Vert" });
    assert.equal(sc.ouvert, false);
});
