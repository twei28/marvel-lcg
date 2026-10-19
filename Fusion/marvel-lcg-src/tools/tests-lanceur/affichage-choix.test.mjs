// Tests du module pur `public/js/prepare/affichage-choix.js`.
//
//     node --test tools/tests-lanceur/affichage-choix.test.mjs
//
// LES NOMS (18/10/2026) : valeur "epure" = « Normal » (affichage de départ de tout le monde), valeur "normal" =
// « Coloré », valeur "sobre" = « Sobre ». Les valeurs rangées n'ont pas changé.
import { test } from "node:test";
import assert from "node:assert/strict";
import { migrerAffichage, CLE_MIGRATION_AFFICHAGE, VERSION_MIGRATION_AFFICHAGE, normaliser, suivant, attributsDe, reconcilier, CLE_AFFICHAGE, PAR_DEFAUT, doitProposerLeChoix, valeurPermise, epurePermis, reglerEpurePourTous } from "../../public/js/prepare/affichage-choix.js";

test("la clé est celle que lit le plateau", () => {
    assert.equal(CLE_AFFICHAGE, "mc_affichage_v1");
});

test("l'affichage de départ est epure, qui se lit « Normal »", () => {
    assert.equal(PAR_DEFAUT, "epure");
});

test("toute valeur inconnue vaut l'affichage de départ", () => {
    for (const v of [undefined, null, "", "fluo", "SOBRE", 1]) assert.equal(normaliser(v), "epure");
    assert.equal(normaliser("normal"), "normal");
    assert.equal(normaliser("sobre"), "sobre");
    assert.equal(normaliser("epure"), "epure");
});

test("suivant fait tourner : Normal (epure), Coloré (normal), Sobre, Normal", () => {
    assert.equal(suivant("epure"), "normal");
    assert.equal(suivant("normal"), "sobre");
    assert.equal(suivant("sobre"), "epure");
    assert.equal(suivant(undefined), "normal");
});

test("l'épuré est un sobre de plus : data-affichage vaut sobre, data-epure s'ajoute", () => {
    assert.deepEqual(attributsDe("normal"), { affichage: "normal", epure: false });
    assert.deepEqual(attributsDe("sobre"), { affichage: "sobre", epure: false });
    assert.deepEqual(attributsDe("epure"), { affichage: "sobre", epure: true });
    assert.deepEqual(attributsDe(undefined), { affichage: "sobre", epure: true });
});

test("compte sans fichier : le choix du navigateur y est versé, sauf le départ", () => {
    assert.deepEqual(reconcilier("normal", { compte: true, existe: false, preferences: {} }),
        { affichage: "normal", pousser: { affichage: "normal" } });
    assert.deepEqual(reconcilier("sobre", { compte: true, existe: false, preferences: {} }),
        { affichage: "sobre", pousser: { affichage: "sobre" } });
    // Le départ (Normal, valeur epure) n'a rien à verser.
    assert.deepEqual(reconcilier("epure", { compte: true, existe: false, preferences: {} }),
        { affichage: "epure", pousser: {} });
    assert.deepEqual(reconcilier(null, { compte: true, existe: false, preferences: {} }),
        { affichage: "epure", pousser: {} });
});

test("invité ou moteur local : le navigateur reste maître", () => {
    assert.equal(reconcilier("sobre", { compte: false, existe: false, preferences: {} }), null);
    assert.equal(reconcilier("sobre", null), null);
});

test("compte avec fichier : il fait foi, même sans clé d'affichage", () => {
    assert.deepEqual(reconcilier("normal", { compte: true, existe: true, preferences: { affichage: "sobre" } }),
        { affichage: "sobre", pousser: {} });
    assert.deepEqual(reconcilier("sobre", { compte: true, existe: true, preferences: {} }),
        { affichage: "epure", pousser: {} });
});

test("tout le monde a droit à l'épuré (Normal) : les trois affichages rangés sont respectés, rien n'est forcé", () => {
    reglerEpurePourTous(true);
    assert.equal(epurePermis(), true);
    assert.equal(valeurPermise("epure"), "epure");
    assert.equal(valeurPermise("normal"), "normal");
    assert.equal(valeurPermise("sobre"), "sobre");
    assert.equal(valeurPermise(null), "epure");
    assert.equal(valeurPermise("fluo"), "epure");
});

test("tout le monde commence en Normal : aucune fenêtre « Choisis ton affichage » proposée d'office", () => {
    reglerEpurePourTous(true);
    assert.equal(doitProposerLeChoix(null, null), false);
    assert.equal(doitProposerLeChoix(null, { compte: true, existe: true, preferences: { arts: {} } }), false);
});

test("ancienne règle conservée (réserve à l'administrateur) : sans droit, l'épuré et le départ se montrent en sobre", () => {
    reglerEpurePourTous(false);
    try {
        // Sous node : ni hôte local, ni réponse retenue du serveur.
        assert.equal(epurePermis(), false);
        assert.equal(valeurPermise("epure"), "sobre");
        assert.equal(valeurPermise(null), "sobre");
        assert.equal(valeurPermise("sobre"), "sobre");
        assert.equal(valeurPermise("normal"), "normal");
        // La fenêtre de choix, elle, se propose de nouveau à qui n'a jamais choisi.
        assert.equal(doitProposerLeChoix(null, null), true);
        assert.equal(doitProposerLeChoix("normal", null), false);
        assert.equal(doitProposerLeChoix(null, { compte: true, existe: true, preferences: { affichage: "normal" } }), false);
    } finally {
        reglerEpurePourTous(true);
    }
});

// PASSAGE UNIQUE AU NOUVEL AFFICHAGE (19/10/2026) : ceux qui avaient rangé Coloré ou Sobre repassent sur « Normal »
// (valeur epure) à leur première connexion, une seule fois ; leur choix suivant est respecté.
function faux(init = {}) {
    const m = new Map(Object.entries(init));
    return { getItem: (k) => (m.has(k) ? m.get(k) : null), setItem: (k, v) => m.set(k, String(v)), m };
}
test("passage unique : un choix Coloré rangé repasse sur le nouvel affichage, et le passage est noté", () => {
    const s = faux({ [CLE_AFFICHAGE]: "normal" });
    assert.equal(migrerAffichage(s), true);
    assert.equal(s.getItem(CLE_AFFICHAGE), PAR_DEFAUT);
    assert.equal(s.getItem(CLE_MIGRATION_AFFICHAGE), VERSION_MIGRATION_AFFICHAGE);
});
test("passage unique : un choix Sobre rangé repasse aussi sur le nouvel affichage", () => {
    const s = faux({ [CLE_AFFICHAGE]: "sobre" });
    assert.equal(migrerAffichage(s), true);
    assert.equal(s.getItem(CLE_AFFICHAGE), PAR_DEFAUT);
});
test("passage unique : une seule fois, le choix fait ensuite dans les options est respecté", () => {
    const s = faux({ [CLE_AFFICHAGE]: "normal" });
    assert.equal(migrerAffichage(s), true);
    s.setItem(CLE_AFFICHAGE, "normal"); // le joueur reprend Coloré dans les options
    assert.equal(migrerAffichage(s), false);
    assert.equal(s.getItem(CLE_AFFICHAGE), "normal");
});
test("passage unique : sans stockage ou stockage cassé, rien ne plante", () => {
    assert.equal(migrerAffichage(null), false);
    assert.equal(migrerAffichage({ getItem() { throw new Error("x"); }, setItem() {} }), false);
});
