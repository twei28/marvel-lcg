// Tests du module pur `public/js/prepare/arts-cartes-choix.js`.
//
//     node --test tools/tests-lanceur/arts-cartes-choix.test.mjs
import { test } from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import {
    cleCarte, artsDe, serieDuHeros, codeParDefaut, codeAffiche, picIdAvecArt, changementsPourCarte,
    appliquer, cartesAvecArt, lignesDeChoix, doitProposer, serieExclusive, exclusiveRefusee, STANDARD,
} from "../../public/js/prepare/arts-cartes-choix.js";
import { ARTS_CARTES, SERIES_ARTS } from "../../public/js/prepare/arts-cartes-table.js";

// Tables de test : indépendantes des données réelles.
const ARTS = { 56013: ["tmnt"], "01057": ["tmnt"], 32043: [] };
const SERIES = {
    tmnt: {
        heros_cartes: ["tl001", "tj001"], heros_ids: ["leonardo", "jennika"],
        sets_exclusifs: ["TMNT Aggression", "TMNT Basic"],
    },
};

test("la série du héros se reconnaît par sa carte (toutes faces) ou son identifiant de deck", () => {
    assert.equal(serieDuHeros("tl001a", SERIES), "tmnt");
    assert.equal(serieDuHeros("tl001b", SERIES), "tmnt");
    assert.equal(serieDuHeros("tj001a,tj001b", SERIES), "tmnt");
    assert.equal(serieDuHeros("leonardo", SERIES), "tmnt");
    assert.equal(serieDuHeros("38001a", SERIES), null);
    assert.equal(serieDuHeros("", SERIES), null);
});

test("défaut : l'art TMNT pour un héros TMNT, l'officielle pour les autres", () => {
    assert.equal(codeParDefaut("56013", "tl001a", ARTS, SERIES), "tmnt");
    assert.equal(codeParDefaut("56013", "38001a", ARTS, SERIES), STANDARD);
    assert.equal(codeParDefaut("32043", "tl001a", ARTS, SERIES), STANDARD); // aucun art
    assert.equal(codeParDefaut("99999", "tl001a", ARTS, SERIES), STANDARD);
});

test("le choix enregistré l'emporte sur le défaut, « standard » compris", () => {
    assert.equal(codeAffiche("56013", { 56013: "standard" }, "tl001a", ARTS, SERIES), STANDARD);
    assert.equal(codeAffiche("56013", { 56013: "tmnt" }, "38001a", ARTS, SERIES), "tmnt");
    assert.equal(codeAffiche("56013", {}, "tl001a", ARTS, SERIES), "tmnt");
    assert.equal(codeAffiche("56013", {}, "38001a", ARTS, SERIES), STANDARD);
});

test("un code inconnu de la carte est ignoré (retour au défaut)", () => {
    assert.equal(codeAffiche("56013", { 56013: "zzz" }, "tl001a", ARTS, SERIES), "tmnt");
    assert.equal(codeAffiche("56013", { 56013: "zzz" }, "38001a", ARTS, SERIES), STANDARD);
    assert.equal(codeAffiche("32043", { 32043: "tmnt" }, "tl001a", ARTS, SERIES), STANDARD);
});

test("l'image demandée : <id>_<code>, ou l'identifiant seul pour l'officielle", () => {
    assert.equal(picIdAvecArt("56013", "tmnt"), "56013_tmnt");
    assert.equal(picIdAvecArt("56013", STANDARD), "56013");
    assert.equal(picIdAvecArt("56013,56013", "tmnt"), "56013_tmnt");
});

test("changements : un code l'écrit, null l'efface ; appliquer ne modifie pas l'original", () => {
    assert.deepEqual(changementsPourCarte("56013", "standard"), { 56013: "standard" });
    assert.deepEqual(changementsPourCarte("56013", null), { 56013: null });
    assert.deepEqual(changementsPourCarte("", "tmnt"), {});
    const avant = { 56013: "tmnt", "01057": "standard" };
    const apres = appliquer(avant, { 56013: null, 32043: "tmnt" });
    assert.deepEqual(apres, { "01057": "standard", 32043: "tmnt" });
    assert.deepEqual(avant, { 56013: "tmnt", "01057": "standard" });
});

test("les cartes d'un deck qui ont un art, une fois chacune, dans l'ordre", () => {
    assert.deepEqual(cartesAvecArt(["01057", "32043", "56013", "01057", "99999"], ARTS), ["01057", "56013"]);
    assert.deepEqual(cartesAvecArt([], ARTS), []);
    assert.deepEqual(cartesAvecArt(undefined, ARTS), []);
});

test("lignes de choix : officielle d'abord, exemplaires comptés, art affiché", () => {
    const l = lignesDeChoix(["56013", "56013", "01057"], { "01057": "standard" }, "tl001a", ARTS, SERIES);
    assert.deepEqual(l, [
        { id: "56013", exemplaires: 2, codes: ["standard", "tmnt"], affiche: "tmnt" },
        { id: "01057", exemplaires: 1, codes: ["standard", "tmnt"], affiche: "standard" },
    ]);
});

test("la fenêtre n'est proposée que s'il y a des arts et que « ne plus proposer » est décoché", () => {
    assert.equal(doitProposer(["56013"], false, ARTS), true);
    assert.equal(doitProposer(["56013"], true, ARTS), false);
    assert.equal(doitProposer(["32043", "99999"], false, ARTS), false);
});

test("exclusives : refusées hors héros de la série, admises pour ses héros", () => {
    assert.equal(serieExclusive("TMNT Aggression", SERIES), "tmnt");
    assert.equal(serieExclusive("Core Set", SERIES), null);
    assert.equal(exclusiveRefusee("TMNT Aggression", "38001a", SERIES), true);
    assert.equal(exclusiveRefusee("TMNT Aggression", "tj001a", SERIES), false);
    assert.equal(exclusiveRefusee("TMNT Aggression", "leonardo", SERIES), false);
    assert.equal(exclusiveRefusee("Core Set", "38001a", SERIES), false);
    assert.equal(exclusiveRefusee("", "38001a", SERIES), false);
});

test("cleCarte ignore la liste de faces", () => {
    assert.equal(cleCarte("tl001a,tl001b"), "tl001a");
    assert.equal(cleCarte(undefined), "");
});

test("données réelles : chaque art alternatif déclaré a son image et la source est alignée", () => {
    // Les tables générées reflètent le JSON source.
    const source = JSON.parse(fs.readFileSync(new URL("../../data/arts_alternatifs.json", import.meta.url), "utf8"));
    assert.deepEqual(ARTS_CARTES, Object.fromEntries(Object.entries(source.cartes).sort()));
    assert.deepEqual(SERIES_ARTS, source.series);
    // Une carte ne se déclare pas elle-même exclusive ET à art alternatif.
    const cards = JSON.parse(fs.readFileSync(new URL("../../data/cards.json", import.meta.url), "utf8"));
    const parId = new Map();
    for (const v of Object.values(cards)) if (Array.isArray(v)) for (const c of v) if (c && c.card_id) parId.set(c.card_id, c);
    for (const id of Object.keys(ARTS_CARTES)) {
        const c = parId.get(id);
        assert.ok(c, `carte ${id} inconnue`);
        assert.equal(serieExclusive(c.set_name), null, `${id} est à la fois art alternatif et exclusive`);
    }
    assert.deepEqual(artsDe("00000"), []);
});
