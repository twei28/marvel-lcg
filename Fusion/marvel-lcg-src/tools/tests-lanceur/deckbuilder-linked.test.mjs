// Cartes « Linked » : mises de côté par leur carte liée, jamais dans le deck d'un joueur (Rules Reference : « Linked »).
// Elles ne doivent donc PAS apparaître dans la grille du deck-builder (`estCarteJoueur`).
// Constat du 26/10/2026 : aucune n'était masquée (23 sur 27 proposées, dont sy018 et sy043 des Starjammers Aspects).
//
//     node --test tools/tests-lanceur/deckbuilder-linked.test.mjs
import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { estCarteJoueur } from "../../public/js/deckbuilder/regles.js";

const donnees = JSON.parse(readFileSync(new URL("../../data/cards.json", import.meta.url), "utf8"));
const toutes = Object.values(donnees).flatMap((v) => (Array.isArray(v) ? v : []));
const liees = toutes.filter((c) => c && c.desc && c.desc.Linked).map((c) => ({ ...c, class: c.desc.Class, id: c.card_id }));

test("il y a des cartes Linked dans le catalogue (le test n'est pas vide)", () => {
    assert.ok(liees.length >= 27, `seulement ${liees.length} cartes Linked`);
});

test("aucune carte Linked n'est proposée par le deck-builder", () => {
    const proposees = liees.filter((c) => estCarteJoueur(c)).map((c) => `${c.card_id} ${c.name}`);
    assert.deepEqual(proposees, []);
});

test("sy018 Blade of the Phoenix et sy043 Thorn Crew sont bien des cartes Linked", () => {
    for (const id of ["sy018", "sy043"]) assert.ok(liees.some((c) => c.card_id === id), `${id} n'est pas Linked`);
});

test("une carte d'aspect ordinaire reste proposée", () => {
    const sy016 = toutes.find((c) => c.card_id === "sy016");
    assert.ok(sy016 && !(sy016.desc || {}).Linked);
    assert.equal(estCarteJoueur({ ...sy016, class: sy016.desc.Class, id: sy016.card_id }), true);
});
