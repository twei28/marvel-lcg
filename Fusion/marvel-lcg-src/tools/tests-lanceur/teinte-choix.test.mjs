// Tests du module pur `public/js/prepare/teinte-choix.js`.
//
//     node --test tools/tests-lanceur/teinte-choix.test.mjs
//
// ⚠ Les valeurs attendues sont COPIEES de `ui-app/src/board/teinte.test.ts` :
// le plateau et la preparation doivent rendre exactement les memes couleurs.
import { test } from "node:test";
import assert from "node:assert/strict";
import {
    CLE_TEINTE, bornerTeinte, ecrireTeinteEnTexte, hslVersRgb, lireTeinte,
    pointDeLaTeinte, teinteDuCompte, teinteDuPoint, variablesDeTeinte,
} from "../../public/js/prepare/teinte-choix.js";

test("la cle est celle que lit le plateau", () => {
    assert.equal(CLE_TEINTE, "mc_teinte_v1");
});

test("lit « h,s,l » dans les bornes, refuse le reste", () => {
    assert.deepEqual(lireTeinte("210,12,18"), { h: 210, s: 12, l: 18 });
    for (const m of ["210,40,18", "400,10,18", "210,10,90", "210,10,3", "rouge", "210,10", 12, null, "-1,0,10"])
        assert.equal(lireTeinte(m), undefined);
});

test("borne toute teinte", () => {
    assert.deepEqual(bornerTeinte({ h: 370, s: 80, l: 95 }), { h: 10, s: 18, l: 62 });
    assert.equal(ecrireTeinteEnTexte({ h: -30, s: 3.4, l: 1 }), "330,3,6");
});

test("conversion HSL -> RGB", () => {
    assert.equal(hslVersRgb(0, 0, 50), "128 128 128");
    assert.equal(hslVersRgb(0, 100, 50), "255 0 0");
});

test("memes couleurs que le plateau (table sombre)", () => {
    assert.deepEqual(variablesDeTeinte({ h: 210, s: 12, l: 18 }), {
        "--teinte-table": "hsl(210 12% 18%)",
        "--teinte-table-rgb": "40 46 51",
        "--teinte-bandeau": "hsl(210 12% 14%)",
        "--teinte-bandeau-rgb": "31 36 40",
        "--teinte-panneau": "hsl(210 12% 20%)",
        "--teinte-panneau-rgb": "45 51 57",
        "--teinte-cadre": "hsl(210 16% 30%)",
        "--teinte-texte-table": "rgba(226, 232, 240, 0.78)",
    });
});

test("table gris clair : bandeau et panneaux sombres, titres fonces", () => {
    const v = variablesDeTeinte({ h: 40, s: 6, l: 60 });
    assert.equal(v["--teinte-bandeau"], "hsl(40 6% 26%)");
    assert.equal(v["--teinte-panneau"], "hsl(40 6% 24%)");
    assert.equal(v["--teinte-texte-table"], "#1b1d21");
});

test("la roue : angle = teinte, rayon = saturation", () => {
    assert.deepEqual(teinteDuPoint(0, -100, 100, 20), { h: 0, s: 18, l: 20 });
    assert.deepEqual(teinteDuPoint(100, 0, 100, 20), { h: 90, s: 18, l: 20 });
    const p = pointDeLaTeinte({ h: 90, s: 9, l: 20 });
    assert.ok(Math.abs(p.x - 0.5) < 1e-9 && Math.abs(p.y) < 1e-9);
});

test("le compte : sa teinte fait foi, son absence vaut couleur d'origine", () => {
    assert.deepEqual(teinteDuCompte({ compte: true, existe: true, preferences: { teinte: "10,5,30" } }), { h: 10, s: 5, l: 30 });
    assert.equal(teinteDuCompte({ compte: true, existe: true, preferences: {} }), null);
    assert.equal(teinteDuCompte({ compte: false }), undefined);
});
