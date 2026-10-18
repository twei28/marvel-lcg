// Tests du module pur `public/js/prepare/affichage-choix.js`.
//
//     node --test tools/tests-lanceur/affichage-choix.test.mjs
import { test } from "node:test";
import assert from "node:assert/strict";
import { normaliser, suivant, attributsDe, reconcilier, CLE_AFFICHAGE, reglerEpurePourTous } from "../../public/js/prepare/affichage-choix.js";

// Depuis le 18/10/2026 l'épuré est l'affichage de TOUS (modes Normal et Sobre désactivés, pas supprimés). Ces tests vérifient
// l'ancienne règle (réserve à l'administrateur) : on la remet ici ; le test « pour tout le monde » en bas la coupe à nouveau.
reglerEpurePourTous(false);

test("la clé est celle que lit le plateau", () => {
    assert.equal(CLE_AFFICHAGE, "mc_affichage_v1");
});

test("toute valeur inconnue vaut normal", () => {
    for (const v of [undefined, null, "", "fluo", "SOBRE", 1]) assert.equal(normaliser(v), "normal");
    assert.equal(normaliser("sobre"), "sobre");
    assert.equal(normaliser("epure"), "epure");
});

test("suivant fait tourner : normal, sobre, épuré, normal", () => {
    assert.equal(suivant("normal"), "sobre");
    assert.equal(suivant("sobre"), "epure");
    assert.equal(suivant("epure"), "normal");
    assert.equal(suivant(undefined), "sobre");
});

test("l'épuré est un sobre de plus : data-affichage vaut sobre, data-epure s'ajoute", () => {
    assert.deepEqual(attributsDe("normal"), { affichage: "normal", epure: false });
    assert.deepEqual(attributsDe("sobre"), { affichage: "sobre", epure: false });
    assert.deepEqual(attributsDe("epure"), { affichage: "sobre", epure: true });
});

test("un navigateur qui a rangé « epure » a déjà choisi", () => {
    assert.equal(doitProposerLeChoix("epure", null), false);
    assert.equal(doitProposerLeChoix(null, null), true);
});

test("compte sans fichier : l'épuré du navigateur y est versé", () => {
    assert.deepEqual(reconcilier("epure", { compte: true, existe: false, preferences: {} }),
        { affichage: "epure", pousser: { affichage: "epure" } });
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

test("l'épuré est réservé à l'administrateur : sans droit, il se montre en sobre (16/10/2026)", async () => {
    const { valeurPermise, epurePermis } = await import("../../public/js/prepare/affichage-choix.js");
    // Sous node : ni hôte local, ni réponse retenue du serveur.
    assert.equal(epurePermis(), false);
    assert.equal(valeurPermise("epure"), "sobre");
    assert.equal(valeurPermise("sobre"), "sobre");
    assert.equal(valeurPermise("normal"), "normal");
});

test("qui a droit à l'épuré n'a plus que lui : normal et sobre rangés ne se montrent plus, plus de fenêtre de choix (18/10/2026)", async () => {
    const { valeurPermise, doitProposerLeChoix } = await import("../../public/js/prepare/affichage-choix.js");
    globalThis.location = { hostname: "localhost" };
    try {
        for (const v of ["normal", "sobre", "epure", null, "fluo"]) assert.equal(valeurPermise(v), "epure");
        assert.equal(doitProposerLeChoix(null, null), false);
    } finally {
        delete globalThis.location;
    }
});

test("l'épuré pour tout le monde, seul affichage : défaut du site depuis le 18/10/2026", async () => {
    const { valeurPermise, epurePermis, doitProposerLeChoix } = await import("../../public/js/prepare/affichage-choix.js");
    reglerEpurePourTous(true);
    try {
        // Sous node : ni hôte local, ni réponse du serveur, et pourtant :
        assert.equal(epurePermis(), true);
        for (const v of ["normal", "sobre", "epure", null, "fluo"]) assert.equal(valeurPermise(v), "epure");
        assert.equal(doitProposerLeChoix(null, null), false);
    } finally {
        reglerEpurePourTous(false);
    }
});
