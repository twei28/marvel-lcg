// api.js — client des endpoints de données (lecture seule) + cache mémoire.
// Aucun endpoint n'est modifié côté serveur ; on ne fait que consommer l'existant.
"use strict";

const _cache = new Map();

async function getJSON(url) {
    if (_cache.has(url)) return _cache.get(url);
    const res = await fetch(url);
    if (!res.ok) throw new Error("HTTP " + res.status + " of " + url);
    const json = await res.json();
    _cache.set(url, json);
    return json;
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

/** Image d'une carte : la route serveur résout /<card_id> -> image. */
export function cardImageUrl(cardId) {
    if (!cardId) return "";
    return "/" + String(cardId).split(",")[0];
}
/** Image d'une boîte d'extension : /sets/<clé>. encodeURI (pas ...Component)
 *  pour garder les apostrophes intactes (ex. "Galaxy's Most Wanted"). */
export function extensionImageUrl(key) {
    return "/sets/" + encodeURI(key);
}
