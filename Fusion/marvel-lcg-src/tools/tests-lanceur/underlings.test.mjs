// Tests du module pur `public/js/prepare/underlings.js` (Fear No Evil).
//
//     node --test tools/tests-lanceur/underlings.test.mjs
import { test } from "node:test";
import assert from "node:assert/strict";
import { regrouperUnderlings, scenarioDuVilain, tuileContient, nomDeManigance, nomDuVilain } from "../../public/js/prepare/underlings.js";

const sc = (id, name, villain) => ({ id, name, villainCards: [villain], tileImage: villain });
const ext = { manigances: ["art_museum_heist", "the_getaway"], underlings: ["hammerhead", "bullseye", "electro"] };
const catalogue = [
    sc("art_museum_heist_hammerhead", "Art Museum Heist (Hammerhead)", "60086"),
    sc("kingpin", "Kingpin", "60159a"),
    sc("art_museum_heist_bullseye", "Art Museum Heist (Bullseye)", "60065"),
    sc("the_getaway_electro", "The Getaway (Electro)", "60076"),
];

test("une tuile par manigance, dans l'ordre du catalogue, Kingpin garde la sienne", () => {
    const tuiles = regrouperUnderlings(catalogue, ext, {});
    assert.deepEqual(tuiles.map((t) => t.id), ["art_museum_heist", "kingpin", "the_getaway"]);
    const amh = tuiles[0];
    assert.equal(amh.name, "Art Museum Heist");
    assert.equal(amh.interchangeable, true);
    // Les vilains dans l'ordre de l'extension, pas du catalogue.
    assert.deepEqual(amh.underlings.map((u) => [u.id, u.nom, u.villainCardId]), [
        ["hammerhead", "Hammerhead", "60086"],
        ["bullseye", "Bullseye", "60065"],
    ]);
    assert.deepEqual(amh.scenarioIds, ["art_museum_heist_hammerhead", "art_museum_heist_bullseye"]);
    assert.equal(amh.courant.id, "hammerhead");
    assert.equal(tuiles[1].interchangeable, undefined);
});

test("sans memoire, chaque affaire montre un vilain DIFFERENT", () => {
    // Signale le 19/09/2026 : cinq affaires, cinq fois le meme portrait. La
    // tuile de rang N prend le vilain de rang N, donc la rangee les montre
    // tous. Ici les deux manigances portent les trois memes vilains.
    const complet = {
        manigances: ["art_museum_heist", "the_getaway", "protection_racket"],
        underlings: ["hammerhead", "bullseye", "electro"],
    };
    const cartes = [];
    for (const m of complet.manigances) {
        for (const u of complet.underlings) {
            cartes.push(sc(`${m}_${u}`, `Affaire (${u})`, `${m}-${u}`));
        }
    }
    const tuiles = regrouperUnderlings(cartes, complet, {});
    assert.deepEqual(tuiles.map((t) => t.courant.id), ["hammerhead", "bullseye", "electro"]);
    // Et le tour de role repart au debut quand il y a plus d'affaires que de
    // vilains : jamais d'index hors liste.
    const quatre = { ...complet, manigances: [...complet.manigances, "stop_the_presses"] };
    for (const u of complet.underlings) {
        cartes.push(sc(`stop_the_presses_${u}`, `Affaire (${u})`, `stp-${u}`));
    }
    const tuiles4 = regrouperUnderlings(cartes, quatre, {});
    assert.equal(tuiles4[3].courant.id, "hammerhead");
});

test("la memoire choisit le vilain montre par la tuile ; une memoire perimee retombe sur le tour de role", () => {
    const [amh] = regrouperUnderlings(catalogue, ext, { art_museum_heist: "bullseye" });
    assert.equal(amh.courant.id, "bullseye");
    assert.equal(amh.villainCards[0], "60065");
    const [amh2] = regrouperUnderlings(catalogue, ext, { art_museum_heist: "disparu" });
    assert.equal(amh2.courant.id, "hammerhead");
});

test("tuile_sbire_scenarios : la modale montre la carte du SOUS-FIFRE, pas celle du vilain commun aux deux scenarios", () => {
    // One Last Kill (Jigsaw) et (Hobgoblin) partagent le meme vilain actif (Punisher, dans `villain`/`villainCards`
    // des deux fichiers de scenario) : sans le repli sur `tuile_sbire_scenarios`, les deux options de la modale
    // montraient la meme carte Punisher (signale par l'utilisateur le 29/10/2026 : « il ne montre pas la bonne
    // carte »). `villainCards: ["x"]` ci-dessous simule ce partage : les deux scenarios y pointent vers le meme id.
    const scPunisher = (id, name) => ({ id, name, villainCards: ["punisher-commun"], tileImage: "punisher-commun" });
    const unique = { manigances: ["one_last_kill"], underlings: ["jigsaw", "hobgoblin"], tuileSbireScenarios: { one_last_kill_jigsaw: "pu056a", one_last_kill_hobgoblin: "pu071a" } };
    const cat = [scPunisher("one_last_kill_jigsaw", "One Last Kill (Jigsaw)"), scPunisher("one_last_kill_hobgoblin", "One Last Kill (Hobgoblin)")];
    const [tuile] = regrouperUnderlings(cat, unique, {});
    assert.deepEqual(tuile.underlings.map((u) => [u.id, u.villainCardId]), [["jigsaw", "pu056a"], ["hobgoblin", "pu071a"]]);
});

test("sans tuile_sbire_scenarios, repli sur villainCards comme avant (compat)", () => {
    const [amh] = regrouperUnderlings(catalogue, ext, {});
    assert.equal(amh.underlings[0].villainCardId, "60086");
});

test("une manigance a un seul vilain porte a sa tuile, sans modale (un seul choix)", () => {
    const getaway = regrouperUnderlings(catalogue, ext, {})[2];
    assert.equal(getaway.underlings.length, 1);
    assert.equal(scenarioDuVilain(getaway, "n'importe").id, "the_getaway_electro");
});

test("scenarioDuVilain et tuileContient", () => {
    const [amh] = regrouperUnderlings(catalogue, ext, {});
    assert.equal(scenarioDuVilain(amh, "bullseye").id, "art_museum_heist_bullseye");
    assert.equal(scenarioDuVilain(amh, "electro").id, "art_museum_heist_hammerhead");
    assert.equal(tuileContient(amh, "art_museum_heist_bullseye"), true);
    assert.equal(tuileContient(amh, "kingpin"), false);
    assert.equal(tuileContient({ id: "kingpin" }, "kingpin"), true);
});

test("sans declaration d'underlings, la liste est rendue telle quelle", () => {
    assert.deepEqual(regrouperUnderlings(catalogue, {}, {}).map((t) => t.id), catalogue.map((s) => s.id));
});

test("les noms", () => {
    assert.equal(nomDeManigance("Art Museum Heist (Hammerhead)"), "Art Museum Heist");
    assert.equal(nomDeManigance("Kingpin"), "Kingpin");
    assert.equal(nomDuVilain("Art Museum Heist (Typhoid Mary)", "typhoid_mary"), "Typhoid Mary");
    assert.equal(nomDuVilain("sans parenthese", "purple_man"), "Purple Man");
});

// ---- MC×DC 2026 : la liste libre n'a plus de doublons (22/10/2026) ------------------------------------------------------------------------------------
import { readFileSync } from "node:fs";
import { sansVariantesDeCampagne } from "../../public/js/prepare/underlings.js";

test("sansVariantesDeCampagne : la partie libre retire les variantes de campagne, la campagne les garde toutes", () => {
    const e = { scenariosCampagne: ["tracking_the_buyer_x_jigsaw"] };
    const liste = [sc("x_jigsaw", "X (Jigsaw)", "1"), sc("tracking_the_buyer_x_jigsaw", "Tracking the Buyer: X (Jigsaw)", "1")];
    assert.deepEqual(sansVariantesDeCampagne(liste, e).map((s) => s.id), ["x_jigsaw"]);
    assert.deepEqual(sansVariantesDeCampagne(liste, e, { campagne: true }).map((s) => s.id), ["x_jigsaw", "tracking_the_buyer_x_jigsaw"]);
    assert.deepEqual(sansVariantesDeCampagne(liste, {}).map((s) => s.id), ["x_jigsaw", "tracking_the_buyer_x_jigsaw"]);   // extension sans declaration : rien ne change
});

test("MC×DC 2026 reel : 5 tuiles d'affaires a 2 sous-fifres (Jigsaw, Hobgoblin), zero variante de campagne dans la liste libre", () => {
    const info = Object.values(JSON.parse(readFileSync(new URL("../../data/sets_info.json", import.meta.url), "utf8"))).find((v) => v && v.name === "punisher_mcdc_2026");
    const ext = { manigances: info.manigances, underlings: info.underlings, scenariosCampagne: info.scenarios_campagne, tuileManigance: info.tuile_manigance };
    const nomDe = (id) => JSON.parse(readFileSync(new URL(`../../data/scenarios/${id}.json`, import.meta.url), "utf8")).name;
    const schemesDe = (id) => JSON.parse(readFileSync(new URL(`../../data/scenarios/${id}.json`, import.meta.url), "utf8")).schemes;
    const catalogueReel = info.scenarios.map((id) => ({ id, name: nomDe(id), villainCards: ["x"], tileImage: "x", schemes: schemesDe(id) }));
    const libre = regrouperUnderlings(sansVariantesDeCampagne(catalogueReel, ext), ext, {});
    const tuiles = libre.filter((t) => t.interchangeable);
    assert.deepEqual(tuiles.map((t) => t.id), ["art_museum_heist", "the_getaway", "protection_racket", "the_raft_breakout", "stop_the_presses"]);
    for (const t of tuiles) assert.deepEqual(t.underlings.map((u) => u.id), ["jigsaw", "hobgoblin"]);
    // la tuile montre l'AFFAIRE (manigance annexe), pas le sous-fifre (demande du 22/10/2026)
    for (const t of tuiles) assert.equal(t.tileImage, schemesDe(t.courant.scenarioId)[0].split(",")[1]);
    assert.equal(libre.filter((s) => /^tracking_the_buyer_|^punishment_/.test(s.id)).length, 0);
    // le reste : The Big Apple x2, La Chute du Roi, One Last Kill x2 (les 4 defis vivent dans leur propre extension fan-made, 22/10/2026)
    const autres = libre.filter((t) => !t.interchangeable).map((s) => s.id).sort();
    assert.deepEqual(autres, ["kingsfall", "one_last_kill_hobgoblin", "one_last_kill_jigsaw", "the_big_apple", "the_big_apple_uptown"]);
});
