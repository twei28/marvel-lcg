// api.js — client des endpoints de données (lecture seule) + cache mémoire.
// Aucun endpoint n'est modifié côté serveur ; on ne fait que consommer l'existant.
"use strict";

import { picIdLangue } from "/public/js/prepare/scans-fr.js";

const _cache = new Map();

async function getJSON(url) {
    if (_cache.has(url)) return _cache.get(url);
    const res = await fetch(url);
    if (!res.ok) throw new Error("HTTP " + res.status + " of " + url);
    const json = await res.json();
    _cache.set(url, json);
    return json;
}

/**
 * Oublie la liste des decks sauvegardés, pour la relire au prochain appel.
 *
 * ⚠ Nécessaire depuis que l'INVITÉ peut importer un deck MarvelCDB depuis le
 * salon : le deck est alors écrit sur le serveur APRÈS que l'hôte a lu sa
 * liste, et sans cet oubli l'hôte garderait sa version d'avant — le choix de
 * l'invité resterait introuvable, donc silencieusement ignoré.
 */
export function oublierDecksSauvegardes() {
    _cache.delete("list_deck?");
}

/** "./deck/starter/spider_man.json" -> "spider_man" */
export function fileName(path) {
    return String(path).replace(/^.*[\\/]/, "").replace(/\.[^/.]+$/, "");
}

export const api = {
    setsInfo:        () => getJSON("get_sets_json?"),
    listScenarios:   () => getJSON("list_scenarios?"),
    customScenarios: () => getJSON("get_sets_custom_scenario?"),
    scenario:        (name) => getJSON("get_scenario_json?" + encodeURIComponent(name)),
    listStarterDecks:() => getJSON("list_starter_deck?"),
    listSavedDecks:  () => getJSON("list_deck?"),
    aspectDecks:     () => getJSON("get_aspect_decks?"),
    deck:            (name) => getJSON("get_hero_json?" + encodeURIComponent(name)),
    listEncounterSets:() => getJSON("list_encounter_sets?"),
    encounterSet:    (name) => getJSON("get_encounter_set_json?" + encodeURIComponent(name)),
    completionRate:  () => fetch("get_completion_rate?").then(r => r.text()),
    gamers:          () => fetch("get_gamers?").then(r => r.text()),
};

/** Image d'une carte : la route serveur résout /<card_id> -> image.
 *
 *  En français, on demande le scan FR (`fr_<code>`). C'est LE point de passage
 *  de toutes les images hors plateau : le wizard, le constructeur de decks, le
 *  salon, l'écran de campagne et les puzzles passent tous par ici. Auparavant
 *  seule la galerie appelait `picIdLangue`, et une interface en français
 *  affichait donc des cartes en anglais partout ailleurs.
 *
 *  Aucun risque si un scan FR manque : le moteur retombe de lui-même sur
 *  l'anglais (repli écrit dans engine/file/cache.py, voir scans-fr.js). */
export function cardImageUrl(cardId) {
    if (!cardId) return "";
    return "/" + picIdLangue(String(cardId).split(",")[0]);
}
/** Image d'une boîte d'extension : /sets/<clé>. encodeURI (pas ...Component)
 *  pour garder les apostrophes intactes (ex. "Galaxy's Most Wanted"). */
export function extensionImageUrl(key) {
    return "/sets/" + encodeURI(key);
}
