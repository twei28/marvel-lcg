// Tests du module pur `public/js/deckbuilder/regles.js`, côté U.S. AGENT (us001b John Walker, « Master of None »).
//
//     node --test tools/tests-lanceur/regles-us-agent.test.mjs
//
// « Master of None — You may include cards in your deck from any aspect. You cannot include allies or basic cards. »
// La règle est DÉCLARÉE dans `deck/starter/us_agent.json` (`metadata.deckbuilding`) : on lit le VRAI fichier, c'est lui
// qui fait foi. Trois moitiés, aussi importantes l'une que l'autre :
//   1. les aspects sont LIBRES (un deck à quatre aspects est légal) ;
//   2. les alliés (de toute classe) et les cartes Basic sont REFUSÉS ;
//   3. le témoin : la règle ne fuit pas chez un autre héros (un deck Basic reste légal chez lui).
// Clé NEUVE `classes_interdites` (25/10/2026) : `classesInterdites(hero)` dans regles.js.
import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { classesInterdites, validerDeck } from "../../public/js/deckbuilder/regles.js";

const deck = JSON.parse(readFileSync(new URL("../../deck/starter/us_agent.json", import.meta.url), "utf8"));
const walker = { id: "us_agent", name: "U.S. Agent", deck };
const autre = { id: "spider_man", name: "Spider-Man", deck: { hero_deck: Array(15).fill("sig") } };

const CATALOGUE = {
    // Un événement de chaque aspect, de quoi bâtir un deck à QUATRE aspects.
    ev_a: { name: "Événement Aggression", class: "Aggression", type: "Event", desc: {} },
    ev_j: { name: "Événement Justice", class: "Justice", type: "Event", desc: {} },
    ev_l: { name: "Événement Leadership", class: "Leadership", type: "Event", desc: {} },
    ev_p: { name: "Événement Protection", class: "Protection", type: "Event", desc: {} },
    // Les cartes interdites.
    ressource_basic: { name: "Ressource Basic", class: "Basic", type: "Resource", desc: {} },
    evenement_basic: { name: "Événement Basic", class: "Basic", type: "Event", desc: {} },
    allie_basic: { name: "Allié Basic", class: "Basic", type: "Ally", desc: {} },
    allie_aggression: { name: "Allié Aggression", class: "Aggression", type: "Ally", desc: {} },
};
for (let i = 1; i <= 9; i++) CATALOGUE[`pilier${i}`] = { name: `Pilier ${i}`, class: "Protection", type: "Event", desc: {} };
const carte = (id) => CATALOGUE[id];
const somme = (o) => Object.values(o).reduce((a, b) => a + b, 0);

/** 15 signatures + 25 cartes choisies, dont `extra`, le reste en piliers Protection (9 titres différents, 3 max chacun). */
function choisies(extra) {
    const m = new Map(Object.entries(extra));
    let reste = 25 - somme(extra);
    for (let i = 1; reste > 0; i++) {
        const n = Math.min(3, reste);
        m.set(`pilier${i}`, n);
        reste -= n;
    }
    return m;
}

test("la règle est DÉCLARÉE dans le deck de départ : classes interdites = Basic, types interdits = Ally", () => {
    assert.deepEqual(classesInterdites(walker), ["Basic"]);
    assert.deepEqual(deck.metadata.deckbuilding.types_interdits, ["Ally"]);
    assert.equal(deck.metadata.deckbuilding.aspects.max, 99);
});

test("Master of None : un deck à QUATRE aspects est légal", () => {
    const verdict = validerDeck({ hero: walker, choisies: choisies({ ev_a: 3, ev_j: 3, ev_l: 3, ev_p: 3 }), carte });
    assert.deepEqual(verdict.problemes, []);
    assert.equal(verdict.ok, true);
});

test("⚠ Master of None : une carte BASIC est refusée (ressource ou événement)", () => {
    for (const basique of ["ressource_basic", "evenement_basic"]) {
        const verdict = validerDeck({ hero: walker, choisies: choisies({ ev_a: 2, [basique]: 1 }), carte });
        assert.equal(verdict.ok, false, basique);
        assert.match(verdict.problemes.join(" "), /refuse ce type de carte/, basique);
    }
});

test("⚠ Master of None : un ALLIÉ est refusé, d'aspect comme Basic", () => {
    for (const allie of ["allie_aggression", "allie_basic"]) {
        const verdict = validerDeck({ hero: walker, choisies: choisies({ [allie]: 1 }), carte });
        assert.equal(verdict.ok, false, allie);
        assert.match(verdict.problemes.join(" "), /refuse ce type de carte/, allie);
    }
});

test("⚠ LE TÉMOIN QUI MORD : chez un autre héros les cartes Basic et les alliés restent légaux", () => {
    // Sans ce cas, une interdiction posée pour tout le monde passerait au vert au-dessus.
    const verdict = validerDeck({ hero: autre, choisies: choisies({ ressource_basic: 1, allie_basic: 1 }), carte });
    assert.deepEqual(verdict.problemes, []);
    assert.equal(verdict.ok, true);
});

test("⚠ LE TÉMOIN QUI MORD : chez un autre héros, quatre aspects restent refusés (la liberté d'aspect ne fuit pas)", () => {
    const verdict = validerDeck({ hero: autre, choisies: choisies({ ev_a: 3, ev_j: 3, ev_l: 3 }), carte });
    assert.equal(verdict.ok, false);
    assert.match(verdict.problemes.join(" "), /Trop d’aspects/);
});
