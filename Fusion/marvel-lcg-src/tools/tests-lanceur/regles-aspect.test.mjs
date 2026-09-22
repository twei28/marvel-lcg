// Tests du module pur `public/js/deckbuilder/regles.js`, côté LIMITE D'ASPECT.
//
//     node --test tools/tests-lanceur/regles-aspect.test.mjs
//
// Ce que ce fichier prouve, et qu'aucune lecture de code ne prouve : un héros
// dont la carte lève la limite d'aspect la lève POUR SES CARTES À LUI, et pour
// personne d'autre. Les deux moitiés comptent autant l'une que l'autre — une
// exemption trop large rendrait légal n'importe quel deck à quatre couleurs.
//
// Écrit le 22/09/2026 après un refus signalé en jeu : un deck marvelcdb de
// Cable bâti sur les manigances annexes était recalé au collage (« Trop
// d'aspects (Justice, Leadership, Aggression, Protection) »), alors que
// Nathan Summers (40001b) dit mot pour mot « You may include player side
// schemes from any aspect in your deck ».
import { test } from "node:test";
import assert from "node:assert/strict";
import { exemptDeLaLimiteAspect, validerDeck } from "../../public/js/deckbuilder/regles.js";

/** Un catalogue minuscule : ce que `validerDeck` lit d'une carte, et rien de
 *  plus (`class`, `type`, `name`, `desc`). */
const CATALOGUE = {
    // Les manigances annexes des TROIS autres aspects : le cœur du signalement.
    ps_justice: { name: "Manigance Justice", class: "Justice", type: "PlayerSideScheme", desc: {} },
    ps_aggression: { name: "Manigance Aggression", class: "Aggression", type: "PlayerSideScheme", desc: {} },
    ps_protection: { name: "Manigance Protection", class: "Protection", type: "PlayerSideScheme", desc: {} },
    // L'orthographe de marvelcdb, que `TYPES_JOUEUR` accepte aussi.
    ps_marvelcdb: { name: "Manigance importée", class: "Justice", type: "Player_Side_Scheme", desc: {} },
    // Une carte hors aspect qui N'EST PAS une manigance annexe : l'exemption
    // ne doit pas déborder dessus.
    allie_justice: { name: "Allié Justice", class: "Justice", type: "Ally", desc: {} },
};

// Le corps du deck, dans l'aspect choisi. Neuf titres DIFFÉRENTS et non un
// seul répété : la limite ordinaire est de 3 exemplaires par titre, et c'est
// elle qui parlerait sinon, à la place de la règle qu'on mesure.
for (let i = 1; i <= 9; i++) {
    CATALOGUE[`lead${i}`] = { name: `Pilier ${i}`, class: "Leadership", type: "Ally", desc: {} };
}

const carte = (id) => CATALOGUE[id];
const heros = (id) => ({ id, name: id, deck: { hero_deck: Array(15).fill("sig") } });

/** Un deck de 40 cartes : 15 signatures + 25 choisies, dont `extra`. */
function choisies(extra) {
    const m = new Map(Object.entries(extra));
    let reste = 25 - somme(extra);
    for (let i = 1; reste > 0; i++) {
        const n = Math.min(3, reste);
        m.set(`lead${i}`, n);
        reste -= n;
    }
    return m;
}
const somme = (o) => Object.values(o).reduce((a, b) => a + b, 0);

test("Cable : les manigances annexes d'autres aspects ne comptent pas", () => {
    const verdict = validerDeck({
        hero: heros("cable"),
        choisies: choisies({ ps_justice: 2, ps_aggression: 2, ps_protection: 2 }),
        carte,
    });
    assert.deepEqual(verdict.problemes, []);
    assert.equal(verdict.ok, true);
    assert.deepEqual(verdict.aspects, ["Leadership"]);
    assert.equal(verdict.total, 40);
});

test("Cable : l'orthographe Player_Side_Scheme de marvelcdb passe aussi", () => {
    assert.equal(exemptDeLaLimiteAspect(heros("cable"), CATALOGUE.ps_marvelcdb), true);
});

test("⚠ Cable : l'exemption s'arrête aux manigances, un allié hors aspect reste refusé", () => {
    const verdict = validerDeck({
        hero: heros("cable"),
        choisies: choisies({ ps_justice: 2, allie_justice: 2 }),
        carte,
    });
    assert.equal(verdict.ok, false);
    assert.deepEqual(verdict.aspects.sort(), ["Justice", "Leadership"]);
    assert.match(verdict.problemes.join(" "), /Trop d’aspects/);
});

test("⚠ LE TÉMOIN QUI MORD : le même deck chez un autre héros reste refusé", () => {
    // Sans ce cas, une exemption posée pour tout le monde passerait au vert
    // au-dessus, et rendrait légal n'importe quel deck à quatre couleurs.
    const verdict = validerDeck({
        hero: heros("spider_man"),
        choisies: choisies({ ps_justice: 2, ps_aggression: 2, ps_protection: 2 }),
        carte,
    });
    assert.equal(verdict.ok, false);
    assert.match(verdict.problemes.join(" "), /Trop d’aspects/);
    assert.deepEqual(verdict.aspects.sort(), ["Aggression", "Justice", "Leadership", "Protection"]);
});
