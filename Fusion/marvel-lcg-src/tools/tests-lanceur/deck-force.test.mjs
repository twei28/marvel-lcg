// Tests du module pur `public/js/prepare/deck-force.js`.
//
//     node --test tools/tests-lanceur/deck-force.test.mjs
//
// Le jeu REFUSAIT un deck importé que ses règles de construction jugent illégal.
// Or ces règles sont du code écrit à la main (Spider-Woman, Fatalis, Ares…) et
// peuvent se tromper : un joueur ne doit pas être bloqué par NOTRE erreur. Le
// refus devient donc « d'après notre code, ce n'est pas possible, mais tu peux
// forcer », et forcer envoie un rapport automatique (deck + raisons du refus)
// pour qu'on voie qui avait raison, du joueur ou du code.
import { test } from "node:test";
import assert from "node:assert/strict";
import { messageDeForcage, rapportDeckForce } from "../../public/js/prepare/deck-force.js";

const HERO = { name: "Spider-Woman", heroCardId: "05001a" };
const DECK = {
    name: "Mon deck",
    hero_deck: ["05001a", "05002"],
    player_deck: ["01001", "01001", "01050", "05010"],
};
const CATALOGUE = {
    "05001a": { name: "Spider-Woman" }, "05002": { name: "Web Shooters" },
    "01001": { name: "Jessica Drew" }, "01050": { name: "Hulk" }, "05010": { name: "Stinger" },
};
const nomCarte = (id) => (CATALOGUE[id] || {}).name;
const PROBLEMES = ["Trop d'aspects (Justice, Leadership, Aggression)", "Il faut deux aspects"];

test("le message dit que c'est NOTRE code qui refuse, liste les raisons et prévient de l'envoi", () => {
    const m = messageDeForcage(HERO, PROBLEMES, (x) => x);
    assert.match(m, /Spider-Woman/);
    assert.match(m, /Trop d'aspects/);
    assert.match(m, /Il faut deux aspects/);
    assert.match(m, /notre code/i);
    // La joueuse doit savoir, AVANT de valider, que le deck part chez nous.
    assert.match(m, /envoy/i);
});

test("le rapport porte le héros, le deck, ses cartes comptées, la source et les raisons du refus", () => {
    const r = rapportDeckForce({
        hero: HERO, deck: DECK, problemes: PROBLEMES, source: "marvelcdb 1234567", ecran: "préparation", nomCarte,
    });
    assert.match(r.nom, /forc/i);
    assert.match(r.description, /Spider-Woman/);
    assert.match(r.description, /05001a/);
    assert.match(r.description, /Mon deck/);
    assert.match(r.description, /marvelcdb 1234567/);
    assert.match(r.description, /Trop d'aspects/);
    // Les exemplaires sont comptés : 2 Jessica Drew, pas deux lignes.
    assert.match(r.description, /2 ?x.*Jessica Drew|Jessica Drew.*x ?2/);
    assert.match(r.description, /Hulk/);
    assert.match(r.description, /préparation/);
});

test("une carte inconnue du catalogue est rapportée par son identifiant, jamais perdue", () => {
    const r = rapportDeckForce({
        hero: HERO, deck: { name: "X", player_deck: ["99999"] }, problemes: ["x"], source: "", ecran: "salon", nomCarte,
    });
    assert.match(r.description, /99999/);
});
