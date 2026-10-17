// Parite MOTEUR / DECK-BUILDER sur l'unicite par sous-titre (decision du 17/10/2026).
//
//     node --test tools/tests-lanceur/unicite-sous-titre.test.mjs
//
// La table `unicite-sous-titre-cas.json` est lue AUSSI par `tools/cas/unicite_sous_titre.py`
// (moteur, filtre `[unique-st]`). Ici le deck-builder (`validerDeck`, vraie base `data/cards.json`)
// doit rendre, pour chaque cas, le meme verdict que celui que le moteur doit rendre : « se correspondent »
// (conflit) ou non. Un cas `parite: false` est un ecart voulu et n'est pas compare.
import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { validerDeck } from "../../public/js/deckbuilder/regles.js";

const lire = (chemin) => JSON.parse(readFileSync(new URL(chemin, import.meta.url), "utf8"));
const TABLE = lire("./unicite-sous-titre-cas.json");
const CATALOGUE = new Map();
for (const liste of Object.values(lire("../../data/cards.json"))) {
    if (Array.isArray(liste)) for (const c of liste) if (c && c.card_id) CATALOGUE.set(c.card_id, c);
}
const carte = (id) => CATALOGUE.get(id);

function verdictDeckBuilder(c) {
    const hero = { id: c.heros, name: c.heros, deck: { hero: [TABLE.heros_faces[c.heros]], hero_deck: [] } };
    const choisies = new Map();
    for (const id of [...(c.en_jeu || []), c.a_jouer]) choisies.set(id, 1);
    const v = validerDeck({ hero, choisies, carte });
    return v.problemes.some((p) => /se correspondent/.test(p));
}

for (const c of TABLE.cas) {
    test(`${c.parite === false ? "(hors parite) " : ""}${c.nom}`, () => {
        for (const id of [...(c.en_jeu || []), c.a_jouer]) assert.ok(carte(id), `carte ${id} absente de cards.json`);
        if (c.parite === false) return;
        assert.equal(verdictDeckBuilder(c), c.conflit, `deck-builder : conflit attendu = ${c.conflit}`);
    });
}
