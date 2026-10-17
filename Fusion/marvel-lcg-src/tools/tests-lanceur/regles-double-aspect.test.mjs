// Tests des cartes DOUBLE ASPECT (`desc.Class = "Aggression;Justice"`), pack
// tmnt_aspect_dual (Inkwire, TMNT Aspects, prefixe ud), 16/10/2026.
//
//     node --test tools/tests-lanceur/regles-double-aspect.test.mjs
//
// Ce que ce fichier prouve : une carte imprimee « AGGRESSION/JUSTICE » entre
// dans un deck Aggression OU dans un deck Justice, sans y ajouter d'aspect, et
// reste refusee dans un deck d'un TROISIEME aspect. Le scan n'imprime aucune
// autre regle de construction (ni limite, ni « both aspects ») : c'est la
// lecture des deux bandeaux de couleur.
//
// Avant le correctif, deux defauts l'empechaient (vus ROUGES ici) :
//  - `estCarteJoueur` lisait `c.class` brut : « Aggression;Justice » n'est ni un
//    aspect ni une classe neutre, la carte sortait du pool (pas de tuile) ;
//  - `validerDeck` comptait la carte pour son PREMIER aspect seulement : dans un
//    deck Justice, Ronin ajoutait « Aggression » et le deck etait refuse.
import { test } from "node:test";
import assert from "node:assert/strict";
import { estCarteJoueur, validerDeck, aspectsDeClasse } from "../../public/js/deckbuilder/regles.js";
import { filtresVides, passeFiltres } from "../../public/js/deckbuilder/filtres.js";

const CATALOGUE = {
    ud001: { name: "* Rōnin", subtitle: "Mikey", class: "Aggression;Justice", type: "Ally", desc: {} },
    ud002: { name: "* Doomsayer", subtitle: "Donnie", class: "Aggression;Leadership", type: "Ally", desc: {} },
    ud004: { name: "* Stealth Fighter", subtitle: "Raph", class: "Justice;Leadership", type: "Ally", desc: {} },
    ud006: { name: "* Nightwatcher", subtitle: "Jenny", class: "Leadership;Protection", type: "Ally", desc: {} },
    // Une signature de Spider-Woman : « Hero;Aggression » n'est PAS un double aspect.
    sig_sw: { name: "Venom Blast", class: "Hero;Aggression", type: "Event", desc: {} },
};
for (const asp of ["Aggression", "Justice", "Leadership", "Protection"]) {
    for (let i = 1; i <= 9; i++) CATALOGUE[`${asp}${i}`] = { name: `${asp} ${i}`, class: asp, type: "Event", desc: {} };
}
for (let i = 1; i <= 9; i++) CATALOGUE[`basic${i}`] = { name: `Basique ${i}`, class: "Basic", type: "Event", desc: {} };

const carte = (id) => CATALOGUE[id];
const heros = (id) => ({ id, name: id, deck: { hero_deck: Array(15).fill("sig") } });

/** 15 signatures + 25 choisies : `extra`, complete avec des cartes de `fond`. */
function choisies(extra, fond) {
    const m = new Map(Object.entries(extra));
    let reste = 25 - Object.values(extra).reduce((a, b) => a + b, 0);
    for (let i = 1; reste > 0; i++) {
        const n = Math.min(3, reste);
        m.set(`${fond}${i}`, n);
        reste -= n;
    }
    return m;
}

test("aspectsDeClasse : deux aspects lus, la signature « Hero;X » n'est pas un double aspect", () => {
    assert.deepEqual(aspectsDeClasse("Aggression;Justice"), ["Aggression", "Justice"]);
    assert.deepEqual(aspectsDeClasse("Justice"), ["Justice"]);
    assert.deepEqual(aspectsDeClasse("Basic"), []);
});

test("le pool du constructeur garde la carte double aspect (tuile visible)", () => {
    assert.equal(estCarteJoueur(CATALOGUE.ud001), true);
    // Garde-fou : la signature de Spider-Woman reste hors du pool.
    assert.equal(estCarteJoueur(CATALOGUE.sig_sw), false);
});

test("Rōnin (Aggression/Justice) dans un deck JUSTICE : legal, un seul aspect", () => {
    const v = validerDeck({ hero: heros("x"), choisies: choisies({ ud001: 1 }, "Justice"), carte });
    assert.deepEqual(v.problemes, []);
    assert.deepEqual(v.aspects, ["Justice"]);
});

test("Rōnin (Aggression/Justice) dans un deck AGGRESSION : legal, un seul aspect", () => {
    const v = validerDeck({ hero: heros("x"), choisies: choisies({ ud001: 1 }, "Aggression"), carte });
    assert.deepEqual(v.problemes, []);
    assert.deepEqual(v.aspects, ["Aggression"]);
});

test("⚠ Rōnin dans un deck LEADERSHIP : refuse (trop d'aspects)", () => {
    const v = validerDeck({ hero: heros("x"), choisies: choisies({ ud001: 1 }, "Leadership"), carte });
    assert.equal(v.ok, false);
    assert.match(v.problemes.join(" "), /Trop d’aspects/);
    assert.equal(v.aspects.length, 2);
    assert.ok(v.aspects.includes("Leadership"));
});

test("deux doubles qui partagent un aspect, sans autre carte d'aspect : UN aspect (le commun)", () => {
    const v = validerDeck({ hero: heros("x"), choisies: choisies({ ud001: 1, ud002: 1 }, "basic"), carte });
    assert.deepEqual(v.problemes, []);
    assert.deepEqual(v.aspects, ["Aggression"]);
});

test("deux doubles dont l'aspect commun est le SECOND de l'un : UN aspect (Justice)", () => {
    const v = validerDeck({ hero: heros("x"), choisies: choisies({ ud001: 1, ud004: 1 }, "basic"), carte });
    assert.deepEqual(v.problemes, []);
    assert.deepEqual(v.aspects, ["Justice"]);
});

test("⚠ deux doubles SANS aspect commun et sans autre carte : deux aspects, refuse", () => {
    const v = validerDeck({ hero: heros("x"), choisies: choisies({ ud001: 1, ud006: 1 }, "basic"), carte });
    assert.equal(v.ok, false);
    assert.equal(v.aspects.length, 2);
});

test("Spider-Woman (exactement 2 aspects) : Aggression + Justice + Rōnin, legal", () => {
    const m = new Map([["ud001", 1], ["Aggression1", 3], ["Aggression2", 3], ["Aggression3", 3], ["Aggression4", 3],
                       ["Justice1", 3], ["Justice2", 3], ["Justice3", 3], ["Justice4", 3], ["Justice5", 1]]);
    const v = validerDeck({ hero: heros("spider_woman"), choisies: m, carte });
    // Le seul ecart toleré ici serait l'egalite des comptes : Rōnin rejoint l'aspect le moins fourni.
    assert.deepEqual(v.problemes, []);
    assert.deepEqual([...v.aspects].sort(), ["Aggression", "Justice"]);
});

test("filtre d'aspect : Rōnin visible sous « Justice » ET sous « Aggression », pas sous « Leadership »", () => {
    const ctx = { ressourcesDe: () => [], motsClesDe: () => [], correspondTexte: () => true };
    const f = filtresVides();
    f.fanMade = true;
    f.aspects = new Set(["Justice", "Basic"]);
    assert.equal(passeFiltres(CATALOGUE.ud001, f, ctx), true);
    f.aspects = new Set(["Aggression"]);
    assert.equal(passeFiltres(CATALOGUE.ud001, f, ctx), true);
    f.aspects = new Set(["Leadership", "Basic"]);
    assert.equal(passeFiltres(CATALOGUE.ud001, f, ctx), false);
});
