// E10 de Hellfire Hunt (livret p.5) : les cartes de campagne (allies RECRUITED hf013-hf028, captifs hf208-hf211, classe « Campaign;Basic »)
// ne sont JAMAIS proposees par le deck-builder ; les cartes d'aspect du meme set (hf001-hf012) le restent.
//
//     node --test tools/tests-lanceur/deckbuilder-hellfire-campagne.test.mjs
import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { estCarteJoueur } from "../../public/js/deckbuilder/regles.js";

const donnees = JSON.parse(readFileSync(new URL("../../data/cards.json", import.meta.url), "utf8"));
const toutes = Object.values(donnees).flatMap((v) => (Array.isArray(v) ? v : []));
const carte = (id) => {
    const c = toutes.find((x) => x.card_id === id);
    assert.ok(c, `${id} absente du catalogue`);
    return { ...c, class: c.desc.Class.split(";")[0], id: c.card_id };   // comme module/card_info.js : la classe du client est le PREMIER element
};
const id = (n) => `hf${String(n).padStart(3, "0")}`;

test("les 16 allies RECRUITED (hf013-hf028) ne sont pas proposes", () => {
    const proposees = [];
    for (let n = 13; n <= 28; n++) if (estCarteJoueur(carte(id(n)))) proposees.push(id(n));
    assert.deepEqual(proposees, []);
});

test("les 4 allies CAPTIVE du scenario 2 (hf208-hf211) ne sont pas proposes", () => {
    for (const i of ["hf208", "hf209", "hf210", "hf211"]) assert.equal(estCarteJoueur(carte(i)), false, i);
});

test("TEMOIN : les cartes d'aspect de Marvel Girl (hf001-hf009) et les ressources (hf010-hf012) restent proposees", () => {
    for (let n = 1; n <= 12; n++) assert.equal(estCarteJoueur(carte(id(n))), true, id(n));
});
