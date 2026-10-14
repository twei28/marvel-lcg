// Rules Reference 1.8, annexe I : l'échange Team-Up à la mise en place, et les
// cartes permanentes hors de la taille du deck.
//
//     node --test tools/tests-lanceur/team-up-et-permanentes.test.mjs
import { test } from "node:test";
import assert from "node:assert/strict";
import { echangesTeamUp, appliquerEchange } from "../../public/js/prepare/team-up.js";
import { validerDeck } from "../../public/js/deckbuilder/regles.js";

const CATALOGUE = {
    "33001a": { card_id: "33001a", name: "Cyclops", type: "Hero", desc: {} },
    "33001b": { card_id: "33001b", name: "Scott Summers", type: "AlterEgo", desc: {} },
    "33002": { card_id: "33002", name: "* Phoenix", subtitle: "Jean Grey", type: "Ally", desc: {} },
    "33003": { card_id: "33003", name: "Optic Blast", type: "Event", desc: {} },
    "33023": { card_id: "33023", name: "Psychic Rapport", type: "Event", desc: { TeamUp: "Cyclops;Phoenix" } },
    "34001a": { card_id: "34001a", name: "Phoenix", type: "Hero", desc: {} },
    "34001b": { card_id: "34001b", name: "Jean Grey", type: "AlterEgo", desc: {} },
    "01001a": { card_id: "01001a", name: "Spider-Man", type: "Hero", desc: {} },
    "01001b": { card_id: "01001b", name: "Peter Parker", type: "AlterEgo", desc: {} },
};
const carte = (id) => CATALOGUE[String(id).split(",")[0]];
const toutes = Object.keys(CATALOGUE);

const cyclops = { hero: ["33001a,33001b"], hero_deck: ["33002", "33003"], player_deck: [] };
const phoenix = { hero: ["34001a,34001b"], hero_deck: [], player_deck: [] };
const spider = { hero: ["01001a,01001b"], hero_deck: [], player_deck: [] };

test("Cyclops avec l'alliée Phoenix face au héros Phoenix : échange proposé contre Psychic Rapport", () => {
    const e = echangesTeamUp([{ index: 0, deck: cyclops }, { index: 1, deck: phoenix }], carte, toutes);
    assert.deepEqual(e, [{ joueur: 0, autre: 1, retirer: "33002", ajouter: "33023" }]);
    const apres = appliquerEchange(cyclops, e[0]);
    assert.deepEqual(apres.hero_deck, ["33023", "33003"]);
    assert.deepEqual(cyclops.hero_deck, ["33002", "33003"], "le deck d'origine reste intact");
});

test("deux cartes Team-Up nomment les deux : celle du pack du joueur est proposée", () => {
    // Reimpression : meme objet que l'originale sous un autre numero (`full_link`).
    const avecReimpression = (id) => (String(id) === "34023" ? CATALOGUE["33023"] : carte(id));
    const e = echangesTeamUp([{ index: 0, deck: cyclops }, { index: 1, deck: phoenix }], avecReimpression, ["34023", ...toutes]);
    assert.equal(e[0].ajouter, "33023");
});

test("la réimpression de la carte Team-Up déjà dans le deck n'est pas proposée", () => {
    const avecReimpression = (id) => (String(id) === "34023" ? CATALOGUE["33023"] : carte(id));
    const deja = { ...cyclops, player_deck: ["33023"] };
    assert.deepEqual(echangesTeamUp([{ index: 0, deck: deja }, { index: 1, deck: phoenix }], avecReimpression, ["34023", ...toutes]), []);
});

test("aucun autre joueur ne joue Phoenix : rien à proposer", () => {
    assert.deepEqual(echangesTeamUp([{ index: 0, deck: cyclops }, { index: 1, deck: spider }], carte, toutes), []);
});

test("en solo : rien à proposer", () => {
    assert.deepEqual(echangesTeamUp([{ index: 0, deck: cyclops }], carte, toutes), []);
});

test("pas de carte Team-Up qui nomme les deux identités : rien à proposer", () => {
    const sansTeamUp = toutes.filter((id) => id !== "33023");
    assert.deepEqual(echangesTeamUp([{ index: 0, deck: cyclops }, { index: 1, deck: phoenix }], carte, sansTeamUp), []);
});

test("la carte Team-Up est déjà dans le deck : rien à proposer", () => {
    const deja = { ...cyclops, player_deck: ["33023"] };
    assert.deepEqual(echangesTeamUp([{ index: 0, deck: deja }, { index: 1, deck: phoenix }], carte, toutes), []);
});

// « The identity card and any cards with the permanent keyword are not counted
// as part of this number. » (Deck Customization)
const PERM = {};
for (let i = 0; i < 15; i++) PERM[`sig${i}`] = { name: `Signature ${i}`, type: "Upgrade", class: "Hero", desc: i < 4 ? { Permanent: "1" } : {} };
for (let i = 1; i <= 12; i++) PERM[`p${i}`] = { name: `Pilier ${i}`, class: "Protection", type: "Ally", desc: {}, text: "" };
PERM.perm = { name: "Permanente d'aspect", class: "Protection", type: "Upgrade", desc: { Permanent: "1" }, text: "" };
const cartePerm = (id) => PERM[id];
const HEROS = { id: "sentinel", deck: { hero_deck: Array.from({ length: 15 }, (_, i) => `sig${i}`) } };
const piliers = (n) => {
    const m = new Map();
    for (let i = 1; n > 0; i++) { const k = Math.min(3, n); m.set(`p${i}`, k); n -= k; }
    return m;
};
const taille = (v) => v.problemes.filter((p) => /Deck trop/.test(p));

test("4 signatures permanentes : 11 + 29 = 40 cartes comptées, deck légal", () => {
    const v = validerDeck({ hero: HEROS, choisies: piliers(29), carte: cartePerm });
    assert.equal(v.total, 40);
    assert.deepEqual(taille(v), []);
});

test("4 signatures permanentes : 11 + 25 = 36, deck trop petit (on comptait 40)", () => {
    const v = validerDeck({ hero: HEROS, choisies: piliers(25), carte: cartePerm });
    assert.equal(v.total, 36);
    assert.equal(taille(v).length, 1);
});

test("une permanente choisie ne compte pas non plus", () => {
    const choisies = piliers(29);
    choisies.set("perm", 1);
    assert.equal(validerDeck({ hero: HEROS, choisies, carte: cartePerm }).total, 40);
});
