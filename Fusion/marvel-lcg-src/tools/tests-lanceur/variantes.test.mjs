// Tests du module pur `public/js/prepare/variantes.js`.
//
//     node --test tools/tests-lanceur/variantes.test.mjs
//
// Le lanceur n'avait AUCUN test jusqu'au 11/09/2026 : la logique de la modale
// du héros est donc sortie du DOM dans un module pur, testé ici.
import { test } from "node:test";
import assert from "node:assert/strict";
import {
    regrouperVariantes, versionsDe, deckDeLaVersion, optionsDuHeros, cleIdentite, apercuVersion, VERSION_DE_BASE,
} from "../../public/js/prepare/variantes.js";

const deck = (id, meta, extra) => ({ id, deck: { name: id, hero: ["x001a,x001b"], metadata: meta || {}, ...(extra || {}) } });

test("une variante se replie sous sa base, dans l'ordre, et la base se nomme", () => {
    const heroes = [
        deck("hellcat", { variante_nom: "Iron Man (allié signature)" }),
        deck("spider_man"),
        deck("hellcat_she_hulk", { variante_de: "hellcat", variante_nom: "Miss Hulk (alliée signature)" }),
    ];
    const tuiles = regrouperVariantes(heroes);
    assert.deepEqual(tuiles.map((h) => h.id), ["hellcat", "spider_man"]);
    assert.deepEqual(versionsDe(tuiles[0]).map((v) => [v.id, v.nom]), [
        ["hellcat", "Iron Man (allié signature)"],
        ["hellcat_she_hulk", "Miss Hulk (alliée signature)"],
    ]);
    // Un héros sans variante n'a que sa propre version, au libellé par défaut.
    assert.deepEqual(versionsDe(tuiles[1]).map((v) => [v.id, v.nom]), [["spider_man", VERSION_DE_BASE]]);
});

test("une variante dont la base a disparu garde sa tuile", () => {
    const heroes = [deck("orphelin", { variante_de: "absent" })];
    assert.deepEqual(regrouperVariantes(heroes).map((h) => h.id), ["orphelin"]);
});

test("une variante qui se désigne elle-même n'est pas repliée", () => {
    const heroes = [deck("boucle", { variante_de: "boucle" })];
    assert.deepEqual(regrouperVariantes(heroes).map((h) => h.id), ["boucle"]);
});

test("le deck de la version choisie, et le deck de base si la mémoire est périmée", () => {
    const heroes = regrouperVariantes([
        deck("hellcat", {}, { hero_deck: ["hc002"] }),
        deck("hellcat_she_hulk", { variante_de: "hellcat" }, { hero_deck: ["hc012"] }),
    ]);
    assert.deepEqual(deckDeLaVersion(heroes[0], "hellcat_she_hulk").hero_deck, ["hc012"]);
    assert.deepEqual(deckDeLaVersion(heroes[0], "supprimee").hero_deck, ["hc002"]);
});

test("aucune option : la modale ne s'ouvre pas ; une seule suffit à l'ouvrir", () => {
    const seul = regrouperVariantes([deck("spider_man")])[0];
    assert.equal(optionsDuHeros(seul, { arts: [], collection: null }).aucune, true);
    // Les ressources n'ouvrent la modale que si le héros a SA collection.
    assert.equal(optionsDuHeros(seul, { arts: [], collection: "sm" }).aucune, false);
    assert.equal(optionsDuHeros(seul, { arts: [], collection: "sm" }).ressources, true);
    // Un art alternatif suffit, et il invite les ressources.
    const o = optionsDuHeros(seul, { arts: [{ code: "m3t" }], collection: null });
    assert.equal(o.aucune, false);
    assert.equal(o.arts.length, 1);
    assert.equal(o.ressources, true);
    // Deux versions suffisent.
    const deux = regrouperVariantes([deck("a"), deck("b", { variante_de: "a" })])[0];
    assert.equal(optionsDuHeros(deux, {}).versions.length, 2);
});

test("la clé d'une identité est le couple de faces, pas la face héros seule", () => {
    assert.equal(cleIdentite({ hero: ["su001a,su001c"], heroCardId: "su001a" }), "su001a,su001c");
    assert.equal(cleIdentite({ heroCardId: "th001c" }), "th001c");
    assert.equal(cleIdentite(null), "");
});

test("la vignette d'une version est la carte que les autres versions n'ont pas, base comprise", () => {
    const heroes = regrouperVariantes([
        deck("hellcat", { variante_nom: "Iron Man (allié signature)" }, { hero_deck: ["hc002", "hc003"] }),
        deck("hellcat_she_hulk", { variante_de: "hellcat", variante_nom: "Miss Hulk" }, { hero_deck: ["hc012", "hc003"] }),
    ]);
    const [base, variante] = versionsDe(heroes[0]);
    assert.equal(apercuVersion(heroes[0], base), "hc002");
    assert.equal(apercuVersion(heroes[0], variante), "hc012");
    // Une seule version : la carte de heros.
    const seul = regrouperVariantes([deck("spider_man")])[0];
    assert.equal(apercuVersion(seul, versionsDe(seul)[0]), "x001a");
});
