// Tests du module pur `public/js/palettes/couleurs.js` (éditeur de palettes).
//
//     node --test tools/tests-lanceur/palettes-couleurs.test.mjs
import { test } from "node:test";
import assert from "node:assert/strict";
import {
    hexVersRgb, rgbVersHex, fondDe, identiteDe, grouperParIdentite,
    couleursDepuisChamps, memePalette, coordonneesDansCanvas, moyenneAutour,
} from "../../public/js/palettes/couleurs.js";

/** Une image de test : `couleurs` est une grille de [r,v,b,a] par pixel. */
function pixels(largeur, hauteur, donne) {
    const data = new Uint8ClampedArray(largeur * hauteur * 4);
    for (let y = 0; y < hauteur; y += 1) {
        for (let x = 0; x < largeur; x += 1) {
            const c = donne(x, y);
            const i = (y * largeur + x) * 4;
            data[i] = c[0]; data[i + 1] = c[1]; data[i + 2] = c[2];
            data[i + 3] = c.length > 3 ? c[3] : 255;
        }
    }
    return data;
}

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
    // ⚠ ORDRE REVU (23/09/2026, demande de l'utilisateur) : la primaire
    // (140,41,31) reste au coin (0 %), la TERTIAIRE (219,220,222) tient
    // l'arret du milieu (22 %), la secondaire (32,43,114) tient le dernier
    // arret visible (38 %) -- pas l'ordre du fichier. Forces au maximum
    // (1,0 / 0,9 / 0,75) et positions elargies (« la couleur primaire peut
    // ressortir un peu plus »).
    const fond = fondDe([[140, 41, 31], [32, 43, 114], [219, 220, 222]], "#111");
    assert.equal(
        fond,
        "linear-gradient(315deg, rgba(140,41,31,1) 0%, rgba(219,220,222,0.9) 22%, " +
        "rgba(32,43,114,0.75) 38%, rgba(32,43,114,0) 50%), #111");
});

test("un héros d'une seule couleur garde la longueur de la bande", () => {
    // Onze cadres sont noirs ou gris : la dernière couleur se répète, la bande
    // garde son dégradé.
    const fond = fondDe([[18, 18, 17]], "#111");
    assert.equal(
        fond,
        "linear-gradient(315deg, rgba(18,18,17,1) 0%, rgba(18,18,17,0.9) 22%, " +
        "rgba(18,18,17,0.75) 38%, rgba(18,18,17,0) 50%), #111");
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

test("le clic est ramene aux pixels de l'image, quelle que soit la taille affichee", () => {
    // Canvas de 600x900 affiche dans une boite de 300x450 : un clic au milieu
    // de la boite doit tomber au milieu de l'image.
    const rect = { left: 10, top: 20, width: 300, height: 450 };
    assert.deepEqual(coordonneesDansCanvas(rect, 600, 900, 160, 245), { x: 300, y: 450 });
    assert.deepEqual(coordonneesDansCanvas(rect, 600, 900, 10, 20), { x: 0, y: 0 });
    // Hors cadre : rien, plutot qu'un pixel invente au bord.
    assert.equal(coordonneesDansCanvas(rect, 600, 900, 5, 245), null);
    assert.equal(coordonneesDansCanvas(rect, 600, 900, 160, 500), null);
    assert.equal(coordonneesDansCanvas(null, 600, 900, 160, 245), null);
});

test("la pipette MOYENNE un carre, elle ne lit pas un pixel isole", () => {
    // Un damier noir et blanc : la moyenne doit tomber au gris, alors qu'un
    // pixel seul rendrait 0 ou 255 selon le pixel touche.
    const data = pixels(9, 9, (x, y) => ((x + y) % 2 ? [255, 255, 255] : [0, 0, 0]));
    const moyenne = moyenneAutour(data, 9, 9, 4, 4, 2);
    assert.ok(Math.abs(moyenne[0] - 128) <= 12, `moyenne = ${moyenne}`);
});

test("la pipette reste dans l'image quand on clique au bord", () => {
    const data = pixels(4, 4, () => [10, 20, 30]);
    assert.deepEqual(moyenneAutour(data, 4, 4, 0, 0, 2), [10, 20, 30]);
    assert.deepEqual(moyenneAutour(data, 4, 4, 3, 3, 2), [10, 20, 30]);
});

test("les pixels transparents ne tirent pas la moyenne vers le noir", () => {
    // Coin arrondi d'un scan : moitie transparente, moitie rouge.
    const data = pixels(5, 5, (x) => (x < 2 ? [0, 0, 0, 0] : [200, 40, 30]));
    assert.deepEqual(moyenneAutour(data, 5, 5, 3, 2, 2), [200, 40, 30]);
    // Tout transparent : rien a prelever, on le DIT.
    const vide = pixels(5, 5, () => [0, 0, 0, 0]);
    assert.equal(moyenneAutour(vide, 5, 5, 2, 2, 2), null);
});
