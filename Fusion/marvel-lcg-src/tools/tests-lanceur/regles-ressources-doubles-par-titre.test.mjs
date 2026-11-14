// Tests du module pur `public/js/deckbuilder/regles.js` : « Max 1 per deck. » des ressources doubles se compte PAR TITRE.
//
//     node --test tools/tests-lanceur/regles-ressources-doubles-par-titre.test.mjs
//
// RR « A copy of a card is defined by title » (arbitrage du 26/10/2026) : l'Energy redessinée d'un pack fan-made (rz013, cr017, ...)
// et l'Energy officielle 01088 sont DEUX exemplaires de la même carte. Un deck qui en prend une de chaque dépasse « Max 1 per deck ».
// On lit le VRAI `data/cards.json` : le test couvre tous les re-skins du dépôt, pas une liste écrite à la main.
import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { validerDeck } from "../../public/js/deckbuilder/regles.js";

const brut = JSON.parse(readFileSync(new URL("../../data/cards.json", import.meta.url), "utf8"));
const catalogue = new Map();
for (const liste of Object.values(brut)) {
    if (!Array.isArray(liste)) continue;
    for (const c of liste) if (c && c.card_id) catalogue.set(c.card_id, { ...c, class: (c.desc || {}).Class });
}
const carte = (id) => catalogue.get(id);
const roz = { id: "roz", name: "Roz", deck: JSON.parse(readFileSync(new URL("../../deck/starter/roz.json", import.meta.url), "utf8")) };
const OFFICIELLES = { Energy: "01088", Genius: "01089", Strength: "01090" };

const depassements = (choisies) =>
    validerDeck({ hero: roz, choisies: new Map(choisies), carte }).problemes.filter((p) => /Trop d’exemplaires de/.test(p));

// Tous les re-skins « ressource double » : type Resource, classe Basic, « Max 1 per deck », titre Energy / Genius / Strength.
const RESKINS = [...catalogue.values()].filter(
    (c) => c.type === "Resource" && c.class === "Basic" && c.desc.MaxPerDeck === "1" && OFFICIELLES[c.name] && !Object.values(OFFICIELLES).includes(c.card_id),
);

test("le catalogue contient bien les re-skins des packs fan-made (garde-fou du test)", () => {
    assert.ok(RESKINS.length >= 27, `${RESKINS.length} re-skins trouvés`);
    for (const id of ["rz013", "bg020", "bm023", "cr017", "hz016", "rl018", "co017", "sz016", "wt023"]) assert.ok(carte(id), id);
});

test("⚠ chaque re-skin + la ressource OFFICIELLE de même titre : dépassement de « Max 1 per deck »", () => {
    for (const c of RESKINS) {
        const officielle = OFFICIELLES[c.name];
        const p = depassements([[officielle, 1], [c.card_id, 1]]);
        assert.equal(p.length, 1, `${c.card_id} (${c.name}) + ${officielle} : ${JSON.stringify(p)}`);
        assert.match(p[0], new RegExp(`« ${c.name} » : 2/1`), c.card_id);
    }
});

test("⚠ deux exemplaires du MÊME re-skin dépassent aussi", () => {
    for (const c of RESKINS) assert.equal(depassements([[c.card_id, 2]]).length, 1, c.card_id);
});

test("un seul exemplaire (re-skin ou officielle) est légal, et deux titres DIFFÉRENTS ne se gênent pas", () => {
    for (const c of RESKINS) assert.deepEqual(depassements([[c.card_id, 1]]), [], c.card_id);
    assert.deepEqual(depassements([["01088", 1]]), []);
    assert.deepEqual(depassements([["rz013", 1], ["rz014", 1], ["rz015", 1]]), [], "Energy + Genius + Strength : trois titres");
});
