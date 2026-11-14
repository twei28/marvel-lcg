// Tests du module pur `public/js/deckbuilder/regles.js`, côté HEPZIBAH (hz001b, « Weapons Officer »).
//
//     node --test tools/tests-lanceur/regles-hepzibah.test.mjs
//
// « Weapons Officer — You may include up to 3 WEAPONS in your deck from aspects other than your chosen aspect. »
// La règle est DÉCLARÉE dans `deck/starter/hepzibah.json` (`metadata.deckbuilding.hors_aspect`) : on lit le VRAI fichier,
// c'est lui qui fait foi. Quatre moitiés :
//   1. le quota est lu (3 cartes, trait WEAPON) ;
//   2. trois armes d'un autre aspect : légal ;
//   3. une QUATRIÈME arme d'un autre aspect, ou une carte d'un autre aspect qui n'est pas une arme : refusé ;
//   4. le témoin : chez un autre héros, les mêmes armes d'un autre aspect sont refusées (la règle ne fuit pas).
import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { quotaHorsAspect, validerDeck } from "../../public/js/deckbuilder/regles.js";

const deck = JSON.parse(readFileSync(new URL("../../deck/starter/hepzibah.json", import.meta.url), "utf8"));
const hepzibah = { id: "hepzibah", name: "Hepzibah", deck };
const autre = { id: "spider_man", name: "Spider-Man", deck: { hero_deck: Array(15).fill("sig") } };

const CATALOGUE = {
    // Armes d'un AUTRE aspect que celui du deck (Protection).
    arme1: { name: "Arme 1", class: "Aggression", type: "Upgrade", traits: ["WEAPON"], desc: {} },
    arme2: { name: "Arme 2", class: "Aggression", type: "Upgrade", traits: ["WEAPON"], desc: {} },
    arme3: { name: "Arme 3", class: "Justice", type: "Upgrade", traits: ["WEAPON"], desc: {} },
    arme4: { name: "Arme 4", class: "Leadership", type: "Upgrade", traits: ["WEAPON"], desc: {} },
    // Une carte d'un autre aspect qui n'est PAS une arme.
    evenement: { name: "Événement Aggression", class: "Aggression", type: "Event", traits: ["ATTACK"], desc: {} },
};
for (let i = 1; i <= 9; i++) CATALOGUE[`pilier${i}`] = { name: `Pilier ${i}`, class: "Protection", type: "Event", desc: {} };
const carte = (id) => CATALOGUE[id];
const somme = (o) => Object.values(o).reduce((a, b) => a + b, 0);

/** 15 signatures + 25 cartes choisies, dont `extra`, le reste en piliers Protection (3 exemplaires max par titre). */
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

test("le quota est DÉCLARÉ dans le deck de départ : 3 cartes WEAPON", () => {
    const quota = quotaHorsAspect(hepzibah);
    assert.ok(quota, "quotaHorsAspect(hepzibah) doit rendre une règle");
    assert.equal(quota.max, 3);
    assert.equal(quota.test(CATALOGUE.arme1), true);
    assert.equal(quota.test(CATALOGUE.evenement), false);
});

test("Weapons Officer : trois armes d'autres aspects sont légales", () => {
    const verdict = validerDeck({ hero: hepzibah, choisies: choisies({ arme1: 1, arme2: 1, arme3: 1 }), carte });
    assert.deepEqual(verdict.problemes, []);
    assert.equal(verdict.ok, true);
});

test("Weapons Officer : une QUATRIÈME arme d'un autre aspect est refusée", () => {
    const verdict = validerDeck({ hero: hepzibah, choisies: choisies({ arme1: 1, arme2: 1, arme3: 1, arme4: 1 }), carte });
    assert.equal(verdict.ok, false);
});

test("Weapons Officer : une carte d'un autre aspect qui n'est pas une arme est refusée", () => {
    const verdict = validerDeck({ hero: hepzibah, choisies: choisies({ arme1: 1, evenement: 1 }), carte });
    assert.equal(verdict.ok, false);
});

test("témoin : chez un autre héros, une arme d'un autre aspect reste refusée", () => {
    const verdict = validerDeck({ hero: autre, choisies: choisies({ arme1: 1 }), carte });
    assert.equal(verdict.ok, false);
});
