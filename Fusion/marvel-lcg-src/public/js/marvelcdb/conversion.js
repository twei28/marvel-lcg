// conversion.js — deck MarvelCDB -> deck moteur.
//
// Un deck marvelcdb est un `slots` de 40 cartes qui MÉLANGE les cartes
// signature du héros et la pioche du joueur. Le moteur, lui, veut hero_deck
// (signature) et player_deck (pioche) séparés, plus le squelette du héros
// (obligations, némésis, set_aside) qu'il ne faut jamais reconstruire : on le
// reprend tel quel dans le deck de départ du jeu.
"use strict";

/**
 * @param {{id: number, nom: string, cartes: Object}} entree  entrée d'index ou deck collé
 * @param {Object} deckStarter  deck de départ du héros, tel que servi par le jeu
 * @param {(cardId: string) => string} classeDe  classe d'une carte ("Hero" pour une signature)
 */
export function versDeckMoteur(entree, deckStarter, classeDe) {
    const player_deck = [];
    for (const id in (entree.cartes || {})) {
        // 26002 : exclusion héritée de deck.html, conservée à l'identique.
        if (id === "26002") continue;
        // « Hero;Aggression » (signatures de Spider-Woman) est aussi une signature.
        if (String(classeDe(id) || "").split(";").includes("Hero")) continue;
        for (let n = 0; n < entree.cartes[id]; n++) player_deck.push(id);
    }
    return {
        name: entree.nom || deckStarter.name,
        version: deckStarter.version,
        metadata: { url: "https://marvelcdb.com/decklist/view/" + entree.id },
        hero: deckStarter.hero,
        hero_deck: deckStarter.hero_deck,
        player_deck,
        obligations: deckStarter.obligations,
        nemesis_set: deckStarter.nemesis_set,
        set_aside: deckStarter.set_aside,
    };
}

/**
 * Contrôle de cohérence : le total déclaré par marvelcdb doit se répartir
 * exactement entre les signatures du jeu et la pioche produite. Un écart
 * signale une carte signature que le catalogue n'a pas reconnue, donc un deck
 * à ne pas proposer tel quel.
 */
export function ecartDeConversion(entree, deck) {
    const total = Object.values(entree.cartes || {}).reduce((s, n) => s + n, 0);
    return total - (deck.hero_deck || []).length - (deck.player_deck || []).length;
}
