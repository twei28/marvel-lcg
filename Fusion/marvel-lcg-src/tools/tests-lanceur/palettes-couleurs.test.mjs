// Tests du module pur `public/js/palettes/couleurs.js` (éditeur de palettes).
//
//     node --test tools/tests-lanceur/palettes-couleurs.test.mjs
import { test } from "node:test";
import assert from "node:assert/strict";
import {
    hexVersRgb, rgbVersHex, fondDe, identiteDe, grouperParIdentite,
    couleursDepuisChamps, memePalette,
} from "../../public/js/palettes/couleurs.js";

test("un hex se lit avec ou sans dièse, en majuscules comme en minuscules", () => {
    assert.deepEqual(hexVersRgb("#1a2b3c"), [26, 43, 60]);
    assert.deepEqual(hexVersRgb("1A2B3C"), [26, 43, 60]);
    assert.deepEqual(hexVersRgb("  #ffffff "), [255, 255, 255]);
});

test("une saisie qui n'est pas une couleur est REFUSÉE, pas devinée", () => {
    // ⚠ Le plus important de ce fichier : l'éditeur écrit dans un fichier du
    // dépôt. Une saisie approximative doit s'arrêter ici.
    for (const mauvais of ["", "#12345", "#1234567", "rouge", "#12g456", null, undefined]) {
        assert.equal(hexVersRgb(mauvais), null, `« ${mauvais} » aurait dû être refusé`);
    }
});

test("l'aller-retour hex → rgb → hex ne perd rien", () => {
    for (const hex of ["#000000", "#ffffff", "#8c291f", "#202b72"]) {
        assert.equal(rgbVersHex(hexVersRgb(hex)), hex);
    }
});

test("une composante hors bornes est ramenée dans 0..255", () => {
    assert.equal(rgbVersHex([-10, 300, 12.6]), "#00ff0d");
});

test("le fond reproduit la bande diagonale du plateau", () => {
    const fond = fondDe([[140, 41, 31], [32, 43, 114], [219, 220, 222]], "#111");
    assert.equal(
        fond,
        "linear-gradient(315deg, rgba(140,41,31,0.46) 0%, rgba(32,43,114,0.34) 16%, " +
        "rgba(219,220,222,0.2) 30%, rgba(219,220,222,0) 50%), #111");
});

test("un héros d'une seule couleur garde la longueur de la bande", () => {
    // Onze cadres sont noirs ou gris : la dernière couleur se répète, la bande
    // garde son dégradé.
    const fond = fondDe([[18, 18, 17]], "#111");
    assert.equal(
        fond,
        "linear-gradient(315deg, rgba(18,18,17,0.46) 0%, rgba(18,18,17,0.34) 16%, " +
        "rgba(18,18,17,0.2) 30%, rgba(18,18,17,0) 50%), #111");
});

test("sans couleur, le fond reste celui du plateau", () => {
    assert.equal(fondDe([], "#111"), "#111");
    assert.equal(fondDe(undefined, "#111"), "#111");
});

test("les faces d'une identité se rejoignent sous une seule clé", () => {
    assert.equal(identiteDe("03001a"), "03001");
    assert.equal(identiteDe("03001b"), "03001");
    assert.equal(identiteDe("31002a"), "31002");
    // Une clé sans lettre finale reste telle quelle.
    assert.equal(identiteDe("12345"), "12345");
});

test("le regroupement rend les faces triées et la palette commune", () => {
    const groupes = grouperParIdentite({
        "03001b": [[1, 2, 3]],
        "03001a": [[1, 2, 3]],
        "aa001a": [[4, 5, 6], [7, 8, 9]],
    });
    assert.deepEqual(groupes.get("03001").cartes, ["03001a", "03001b"]);
    assert.deepEqual(groupes.get("03001").couleurs, [[1, 2, 3]]);
    assert.deepEqual(groupes.get("aa001").couleurs, [[4, 5, 6], [7, 8, 9]]);
});

test("deux couleurs suffisent, un TROU au milieu est refusé", () => {
    assert.deepEqual(couleursDepuisChamps(["#010203", "#040506", ""]),
        { erreur: "", couleurs: [[1, 2, 3], [4, 5, 6]] });
    assert.equal(couleursDepuisChamps(["#010203", "", "#040506"]).erreur, "trou");
    assert.equal(couleursDepuisChamps(["", "", ""]).erreur, "vide");
    assert.equal(couleursDepuisChamps(["#010203", "bleu", ""]).erreur, "hex");
});

test("une correction identique à la palette générée n'en est pas une", () => {
    assert.equal(memePalette([[1, 2, 3]], [[1, 2, 3]]), true);
    assert.equal(memePalette([[1, 2, 3]], [[1, 2, 4]]), false);
    assert.equal(memePalette([[1, 2, 3]], [[1, 2, 3], [4, 5, 6]]), false);
});
