// Tests du module pur `public/js/prepare/phase-mode-choix.js`.
//
//     node --test tools/tests-lanceur/phase-mode-choix.test.mjs
import { test } from "node:test";
import assert from "node:assert/strict";
import { CLE_MODE_PHASE, CLE_PHASE_MODE_VU, MODES, normaliser, doitProposerLeChoix, modeAEcrire }
    from "../../public/js/prepare/phase-mode-choix.js";

test("la clé du mode est celle que lit le plateau", () => {
    assert.equal(CLE_MODE_PHASE, "marvel-board-mode-phase-mechant");
    assert.equal(CLE_PHASE_MODE_VU, "mc_phase_mode_vu_v1");
});

test("trois modes, le défaut d'abord", () => {
    assert.deepEqual(MODES, ["detaille", "sur-table", "instantane"]);
});

test("toute valeur inconnue vaut detaille", () => {
    for (const v of [undefined, null, "", "pas-a-pas", "INSTANTANE", 1]) assert.equal(normaliser(v), "detaille");
    assert.equal(normaliser("sur-table"), "sur-table");
});

test("la fenêtre n'est montrée qu'à qui ne l'a jamais vue", () => {
    assert.equal(doitProposerLeChoix(null), true);
    assert.equal(doitProposerLeChoix(""), true);
    assert.equal(doitProposerLeChoix("1"), false);
});

test("rien n'est écrit quand le choix ne change rien", () => {
    assert.equal(modeAEcrire(null, "detaille"), null);
    assert.equal(modeAEcrire("pas-a-pas", "detaille"), null);
    assert.equal(modeAEcrire("instantane", "instantane"), null);
});

test("un autre mode est écrit", () => {
    assert.equal(modeAEcrire(null, "sur-table"), "sur-table");
    assert.equal(modeAEcrire("detaille", "instantane"), "instantane");
    assert.equal(modeAEcrire("sur-table", "detaille"), "detaille");
});

test("un choix invalide n'écrit rien", () => {
    assert.equal(modeAEcrire("detaille", "fluo"), null);
});
