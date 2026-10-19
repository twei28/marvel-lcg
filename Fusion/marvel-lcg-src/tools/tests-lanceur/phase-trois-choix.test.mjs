// Passage unique aux trois choix de la phase du méchant (19/10/2026), côté préparation.
//
//     node --test tools/tests-lanceur/phase-trois-choix.test.mjs
import { test } from "node:test";
import assert from "node:assert/strict";
import { PRESENTATION_PAR_DEFAUT, PHASE_IMAGES_VISIBLES, CLE_MODE_PHASE, CLE_PRESENTATION_PHASE, CLE_MIGRATION_PHASE, VERSION_MIGRATION_PHASE, migrerPhaseTroisChoix, normaliser }
    from "../../public/js/prepare/phase-mode-choix.js";

function stockage(depart = {}) {
    const m = new Map(Object.entries(depart));
    return { getItem: (k) => (m.has(k) ? m.get(k) : null), setItem: (k, v) => m.set(k, v), lu: (k) => (m.has(k) ? m.get(k) : null) };
}

test("migration : l'ancien « Étape par étape » passe sur tris, une seule fois", () => {
    const s = stockage({ [CLE_PRESENTATION_PHASE]: "etape" });
    assert.equal(migrerPhaseTroisChoix(s), true);
    assert.equal(s.lu(CLE_PRESENTATION_PHASE), "tris");
    assert.equal(VERSION_MIGRATION_PHASE, "2026-10-19b");
    assert.equal(s.lu(CLE_MIGRATION_PHASE), VERSION_MIGRATION_PHASE);
    s.setItem(CLE_PRESENTATION_PHASE, "etape");
    assert.equal(migrerPhaseTroisChoix(s), false);
    assert.equal(s.lu(CLE_PRESENTATION_PHASE), "etape");
});

test("migration : dynamique et l'ancien mc_phase_bis=non passent sur tris ; les modes sont conservés", () => {
    const a = stockage({ [CLE_PRESENTATION_PHASE]: "dynamique" });
    migrerPhaseTroisChoix(a);
    assert.equal(a.lu(CLE_PRESENTATION_PHASE), "tris");
    const b = stockage({ mc_phase_bis: "non" });
    migrerPhaseTroisChoix(b);
    assert.equal(b.lu(CLE_PRESENTATION_PHASE), "tris");
    const c = stockage({ [CLE_MODE_PHASE]: "sur-table", [CLE_PRESENTATION_PHASE]: "etape" });
    migrerPhaseTroisChoix(c);
    assert.equal(c.lu(CLE_MODE_PHASE), "sur-table");
    const d = stockage({ [CLE_MODE_PHASE]: "instantane" });
    migrerPhaseTroisChoix(d);
    assert.equal(d.lu(CLE_MODE_PHASE), "instantane");
});

test("migration : stockage absent ou refusé", () => {
    assert.equal(migrerPhaseTroisChoix(null), false);
    assert.equal(migrerPhaseTroisChoix({ getItem() { throw new Error("non"); }, setItem() {} }), false);
});

test("défaut : un navigateur neuf se lit detaille, qui s'affiche « tris »", () => {
    assert.equal(normaliser(null), "detaille");
});

test("migration : bis (déjà migré par erreur à 2026-10-19) repasse sur tris", () => {
    const s = stockage({ [CLE_PRESENTATION_PHASE]: "bis", [CLE_MIGRATION_PHASE]: "2026-10-19" });
    assert.equal(migrerPhaseTroisChoix(s), true);
    assert.equal(s.lu(CLE_PRESENTATION_PHASE), "tris");
    const n = stockage({ [CLE_PRESENTATION_PHASE]: "bis" });
    migrerPhaseTroisChoix(n);
    assert.equal(n.lu(CLE_PRESENTATION_PHASE), "tris");
});

test("défaut tris, images de la fenêtre cachées", () => {
    assert.equal(PRESENTATION_PAR_DEFAUT, "tris");
    assert.equal(PHASE_IMAGES_VISIBLES, false);
});
