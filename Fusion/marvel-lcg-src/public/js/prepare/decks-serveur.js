// decks-serveur.js — les decks importés vivent SUR LE SERVEUR, pas dans le cache.
//
// ⚠ POURQUOI CE FICHIER EXISTE (16/09/2026). Les decks importés depuis
// marvelcdb étaient rangés dans le `localStorage` (`prefs.savedDecks`), donc
// DANS UN NAVIGATEUR. Conséquences vécues le jour même : « je suis sur le
// téléphone et je ne retrouve pas les decks que j'ai importés, alors que je les
// ai sur PC ». Et le pire n'était pas là : vider le cache, changer de
// navigateur ou passer en navigation privée les effaçait sans un mot.
//
// Le chemin serveur existait DÉJÀ, et il était même utilisé : l'invité qui
// importe un deck depuis le salon écrit sur le serveur (`salon/app.js`), via
// `POST /save_deck`. Seul l'hôte, dans l'assistant, restait au cache. Ce module
// ne fait que le brancher sur la même route.
//
// Où le deck atterrit : `deck/serveur-<place>/`, le PREMIER dossier de
// `deck_folders` (voir tools/config_serveur.py). C'est le dossier propre au
// compte, séparé par place, sauvegardé avec le reste. Le moteur l'expose
// ensuite par `/list_deck` et `/get_hero_json`.
"use strict";

import { api, fileName, oublierDecksSauvegardes } from "/public/js/prepare/api.js";
import { prefs } from "/public/js/prepare/prefs.js";

/** Marque qu'on a déjà remonté les decks du cache vers le serveur. */
const CLE_MIGRATION = "mc_decks_migres_v1";

/** Un deck du joueur est celui qui vit dans SON dossier, pas dans le commun.
 *
 *  `/list_deck` rend les chemins des trois sources à la fois : `deck/starter/`
 *  (les decks de base), `deck/custom/` (le commun, lu par tout le monde) et
 *  `deck/serveur-<place>/`. Seul le dernier appartient au joueur. */
function estDuJoueur(chemin) {
    return /[\\/]serveur-\d+[\\/]/.test(String(chemin));
}

function memeHeros(deck, heroCardId) {
    const attendu = String(heroCardId || "").split(",")[0];
    const sien = String((deck && deck.hero && deck.hero[0]) || "").split(",")[0];
    return sien && attendu && sien === attendu;
}

/** Un nom de fichier stable : deux imports du même deck ne s'empilent pas. */
function nomDeFichier(deck) {
    const base = String((deck && deck.name) || "deck").trim();
    return "mcdb-" + base.replace(/[^a-zA-Z0-9_-]+/g, "_").replace(/^_+|_+$/g, "").slice(0, 50);
}

/**
 * Écrit le deck sur le serveur. Rend `true` s'il y est.
 *
 * ⚠ LE CACHE RESTE LE FILET, ET SEULEMENT LE FILET. Si le serveur refuse (hors
 * ligne, table qui redémarre), on garde le deck en local pour ne pas le perdre
 * sous les yeux du joueur, et la prochaine lecture le remontera. Ce qu'on ne
 * fait plus, c'est s'en contenter.
 */
export async function sauverDeck(deck) {
    try {
        const reponse = await fetch("/save_deck", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ file_name: nomDeFichier(deck), deck }),
        });
        const rep = await reponse.json().catch(() => ({}));
        if (!reponse.ok || rep.error) throw new Error(rep.error || "HTTP " + reponse.status);
        oublierDecksSauvegardes();
        return true;
    } catch (souci) {
        prefs.saveDeck(deck);           // filet : on ne perd rien
        return false;
    }
}

/** Supprime un deck sauvegardé sur le serveur. `idFichier` est le nom de fichier sans extension. */
export async function supprimerDeck(idFichier) {
    const reponse = await fetch("/delete_deck", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ file_name: idFichier }),
    });
    const rep = await reponse.json().catch(() => ({}));
    if (!reponse.ok || rep.error) throw new Error(rep.error || "HTTP " + reponse.status);
    oublierDecksSauvegardes();
}

/** Les decks du joueur présents sur le serveur, contenu chargé. */
async function decksDuServeur() {
    let chemins = [];
    try {
        chemins = await api.listSavedDecks();
    } catch (souci) {
        return null;                    // serveur muet : l'appelant retombe sur le cache
    }
    const noms = (chemins || []).filter(estDuJoueur).map(fileName);
    const decks = await Promise.all(noms.map(async (nom) => {
        try {
            return await api.deck(nom);
        } catch (souci) {
            return null;                // un fichier illisible n'empêche pas les autres
        }
    }));
    return decks.filter(Boolean);
}

/**
 * Remonte une fois les decks restés dans le cache, puis ne les lit plus.
 *
 * On ne VIDE pas le cache après coup : si la remontée a échoué à moitié, le
 * joueur garderait un trou sans le savoir. Il reste là, ignoré.
 */
async function migrerLeCache() {
    let deja = false;
    try { deja = window.localStorage.getItem(CLE_MIGRATION) === "1"; } catch (e) { deja = false; }
    if (deja) return;
    const locaux = prefs.savedDecks();
    if (!locaux.length) {
        try { window.localStorage.setItem(CLE_MIGRATION, "1"); } catch (e) { /* refusé */ }
        return;
    }
    const sorts = await Promise.all(locaux.map((deck) => sauverDeck(deck)));
    if (sorts.every(Boolean)) {
        try { window.localStorage.setItem(CLE_MIGRATION, "1"); } catch (e) { /* refusé */ }
    }
}

/**
 * Les decks sauvegardés de ce héros, serveur d'abord.
 *
 * Le cache ne sert plus que de repli quand le serveur ne répond pas : un joueur
 * hors ligne garde ses decks à l'écran, mais ce n'est plus là qu'ils vivent.
 */
export async function decksSauvegardesPourHeros(heroCardId) {
    await migrerLeCache();
    const duServeur = await decksDuServeur();
    if (duServeur === null) return prefs.savedDecksForHero(heroCardId);
    return duServeur.filter((deck) => memeHeros(deck, heroCardId));
}
