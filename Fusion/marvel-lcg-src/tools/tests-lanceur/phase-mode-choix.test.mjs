// Tests du module pur `public/js/prepare/phase-mode-choix.js`.
//
//     node --test tools/tests-lanceur/phase-mode-choix.test.mjs
import { test } from "node:test";
import assert from "node:assert/strict";
import { CLE_MODE_PHASE, CLE_PHASE_MODE_VU, CLE_PHASE_CHOIX_VU, VERSION_CHOIX_PHASE, MODES, normaliser, doitProposerLeChoix, modeAEcrire }
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
    assert.equal(doitProposerLeChoix("1"), true, "l'ancienne cle « 1 » ne compte plus : reaffichage unique du 20/10/2026");
    assert.equal(doitProposerLeChoix(VERSION_CHOIX_PHASE), false);
    assert.equal(VERSION_CHOIX_PHASE, "2026-10-20");
    assert.equal(CLE_PHASE_CHOIX_VU, "mc_phase_choix_vu");
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

test("réaffichage unique du 20/10/2026 : fenêtre posée, choix conservé, aucune nouvelle migration", async () => {
    const { migrerPhaseTroisChoix, CLE_MIGRATION_PHASE, VERSION_MIGRATION_PHASE, CLE_PRESENTATION_PHASE } =
        await import("../../public/js/prepare/phase-mode-choix.js");
    const magasin = new Map([
        [CLE_MIGRATION_PHASE, VERSION_MIGRATION_PHASE],   // déjà passé aux trois choix
        [CLE_MODE_PHASE, "instantane"],                    // son choix
        [CLE_PRESENTATION_PHASE, "tris"],
        [CLE_PHASE_MODE_VU, "1"],                          // a vu l'ancienne fenêtre
    ]);
    const stockage = { getItem: (k) => (magasin.has(k) ? magasin.get(k) : null), setItem: (k, v) => magasin.set(k, String(v)) };
    // clé absente (ancien joueur ou navigateur neuf) : la fenêtre est posée
    assert.equal(doitProposerLeChoix(stockage.getItem(CLE_PHASE_CHOIX_VU)), true);
    // la migration datée ne repasse pas et ne touche à rien
    assert.equal(migrerPhaseTroisChoix(stockage), false);
    assert.equal(normaliser(stockage.getItem(CLE_MODE_PHASE)), "instantane", "le choix est conservé, donc présélectionné");
    // validation : la clé est posée à jour, la fenêtre ne revient plus
    stockage.setItem(CLE_PHASE_CHOIX_VU, VERSION_CHOIX_PHASE);
    assert.equal(doitProposerLeChoix(stockage.getItem(CLE_PHASE_CHOIX_VU)), false);
    assert.equal(modeAEcrire(stockage.getItem(CLE_MODE_PHASE), "instantane"), null);
});

test("tablette (24/10/2026) : Plateau animé présélectionné pour un joueur neuf, et son choix toujours écrit", async () => {
    const { estTablette, choixInitial, REQUETE_TABLETTE } = await import("../../public/js/prepare/phase-mode-choix.js");
    assert.equal(REQUETE_TABLETTE, "(pointer: coarse) and (hover: none) and (min-width: 768px) and (min-height: 501px)");
    assert.equal(estTablette(null, true), true);
    assert.equal(estTablette("non", true), false);
    assert.equal(estTablette("oui", false), true);
    assert.equal(choixInitial(null, true), "sur-table");
    assert.equal(choixInitial("detaille", true), "detaille", "un choix déjà fait est gardé");
    assert.equal(choixInitial(null, false), "detaille", "le PC ne change pas");
    // garder « Guidée » sur tablette neuve doit s'écrire, sinon le plateau partirait en « Plateau animé »
    assert.equal(modeAEcrire(null, "detaille", true), "detaille");
    assert.equal(modeAEcrire(null, "detaille", false), null);
});
