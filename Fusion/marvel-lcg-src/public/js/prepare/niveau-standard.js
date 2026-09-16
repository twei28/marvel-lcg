// niveau-standard.js — Standard I, II ou III, au choix du joueur.
//
// ⚠ POURQUOI CE FICHIER EXISTE (16/09/2026). Question d'un joueur : « is
// standard III implemented ». Les cartes l'étaient : 7 cartes pour Standard III
// et 6 pour Standard II, toutes scriptées. Mais PERSONNE NE POUVAIT LES
// CHOISIR. L'écran de difficulté n'offrait que « Standard » et « Expert », et
// `catalog.js` écarte de la liste des modulaires tout set dont le nom commence
// par « standard ». Résultat : les 6 cartes de Standard II n'avaient jamais été
// jouées, aucun scénario ne les déclarant.
//
// Comment le jeu s'en sert, relevé dans `data/scenarios/` :
//   rhino          -> ["standard"]
//   rhino_expert   -> ["standard", "expert"]      (Expert S'AJOUTE)
//   wd_kingpin     -> ["kingpin", "standard_iii", "bodyguard"]  (III REMPLACE)
//
// D'où la règle, qui tient en une phrase : le niveau choisi REMPLACE le set de
// la famille standard, et ne touche à rien d'autre — ni au set Expert, ni aux
// modulaires, ni aux sets propres au scénario.
"use strict";

/** Les trois niveaux, dans l'ordre où le joueur les voit. */
export const NIVEAUX_STANDARD = ["standard", "standard_ii", "standard_iii"];

/** Le libellé d'un niveau. Les chiffres romains sont ceux des boîtes. */
export function libelleNiveau(niveau) {
    return { standard: "Standard I", standard_ii: "Standard II", standard_iii: "Standard III" }[niveau]
        || "Standard I";
}

/** Un set appartient-il à la famille standard ? (`standard_pvp` non : c'est le
 *  set de base du mode Bataille, qui n'a pas de niveaux.) */
export function estSetStandard(nom) {
    return NIVEAUX_STANDARD.includes(String(nom));
}

/**
 * Le niveau qu'un scénario impose de lui-même, ou `"standard"` par défaut.
 *
 * C'est ce qui doit être PRÉSÉLECTIONNÉ : ouvrir un scénario de Web of Deceit
 * en montrant « Standard I » alors qu'il joue Standard III serait un écran qui
 * ment.
 */
export function niveauDuScenario(raw) {
    const sets = (raw && raw.encounter_sets) || [];
    return sets.find(estSetStandard) || "standard";
}

/**
 * La liste des sets de rencontre, avec le niveau demandé.
 *
 * ⚠ ON NE FAIT QU'ÉCHANGER. Un scénario qui ne déclare AUCUN set standard
 * (certains n'en ont pas) n'en reçoit pas un : lui en ajouter changerait sa
 * difficulté sans que personne l'ait demandé.
 */
export function appliquerNiveau(sets, niveau) {
    const voulu = NIVEAUX_STANDARD.includes(niveau) ? niveau : "standard";
    const liste = [...(sets || [])];
    const place = liste.findIndex(estSetStandard);
    if (place === -1) return liste;
    liste[place] = voulu;
    // Un doublon si le set voulu était déjà ailleurs dans la liste.
    return liste.filter((nom, i) => i === place || nom !== voulu);
}
