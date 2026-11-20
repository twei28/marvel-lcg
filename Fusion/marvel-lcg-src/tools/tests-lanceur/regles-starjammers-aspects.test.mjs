// Tests du module pur `public/js/deckbuilder/regles.js`, côté STARJAMMERS ASPECTS (préfixe `sy`, 50 cartes d'aspect et Basic).
//
//     node --test tools/tests-lanceur/regles-starjammers-aspects.test.mjs
//
// On lit le VRAI `data/cards.json` : ce qui doit être vrai pour que le deck-builder PROPOSE ces cartes.
//   1. les 50 cartes sy001-sy050 sont des cartes de joueur (aspect ou Basic, type jouable), sauf les 2 cartes Linked
//      (sy018 Blade of the Phoenix, sy043 Thorn Crew : mises de côté par leur carte, masquées, 26/10/2026) ;
//   2. le gabarit d'allié face cachée `sy_thorn_ally` n'en est PAS une (il ne doit jamais apparaître dans la grille) ;
//   3. les plafonds imprimés sont lus : « Max 1 per deck » (sy007, sy008 : 1), « Max 2 per deck » (sy015 : 2), le reste 3 ;
//   4. les cinq classes sont toutes représentées (Basic 15, Aggression 9, Justice 8, Leadership 9, Protection 9).
import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { estCarteJoueur, maxParDeck } from "../../public/js/deckbuilder/regles.js";

const donnees = JSON.parse(readFileSync(new URL("../../data/cards.json", import.meta.url), "utf8"));
// Même forme que le chargeur du deck-builder : `class` vient de `desc.Class`.
const cartes = (donnees.starjammers_aspects || []).map((c) => ({ ...c, class: c.desc && c.desc.Class, id: c.card_id }));
const sy = cartes.filter((c) => /^sy\d{3}$/.test(c.card_id));

const LIEES = ["sy018", "sy043"];

test("les 48 cartes sy non Linked sont proposées au deck-builder, les 2 Linked sont masquées", () => {
    assert.equal(sy.length, 50);
    for (const c of sy.filter((x) => !LIEES.includes(x.card_id))) assert.ok(estCarteJoueur(c), `${c.card_id} ${c.name} (${c.class}, ${c.type}) n'est pas une carte de joueur`);
    for (const id of LIEES) assert.equal(estCarteJoueur(sy.find((c) => c.card_id === id)), false, `${id} (Linked) ne doit pas être proposée`);
});

test("le gabarit d'allié face cachée n'est pas une carte de joueur", () => {
    const g = cartes.find((c) => c.card_id === "sy_thorn_ally");
    assert.ok(g, "gabarit sy_thorn_ally absent de cards.json");
    assert.equal(estCarteJoueur(g), false);
});

test("plafonds par deck imprimés", () => {
    const max = (id) => maxParDeck(sy.find((c) => c.card_id === id));
    assert.equal(max("sy007"), 1);
    assert.equal(max("sy008"), 1);
    assert.equal(max("sy015"), 2);
    assert.equal(max("sy016"), 3);
});

test("répartition par classe", () => {
    const n = (k) => sy.filter((c) => c.class === k).length;
    assert.deepEqual([n("Basic"), n("Aggression"), n("Justice"), n("Leadership"), n("Protection")], [15, 9, 8, 9, 9]);
});
