// facon-de-jouer.js : « Automatique ou Manuel façon OCTGN », le choix PAR DEFAUT
// (05/10/2026). Le lanceur le lit pour cocher le choix d'une nouvelle partie ;
// les Réglages du plateau l'écrivent (ui-app/src/board/FenetreReglages.tsx), sous
// la même clé : lanceur et plateau partagent le localStorage de l'hôte.
//
// Le choix d'UNE partie reste libre au lancement : cette clé n'est qu'un défaut.
//
// Module PUR (le stockage est passé en paramètre) :
// `node --test tools/tests-lanceur/facon-de-jouer.test.mjs`.
"use strict";

export const CLE_FACON_DE_JOUER = "marvel-board-facon-de-jouer";

export const AUTO = "auto";
export const MANUEL = "manuel";

/** Toute valeur inconnue (absente, abîmée) vaut « auto ». */
export function normaliser(valeur) {
    return valeur === MANUEL ? MANUEL : AUTO;
}

/** Le défaut enregistré ; un stockage absent ou qui jette vaut « auto ». */
export function faconParDefaut(stockage) {
    try {
        return normaliser(stockage?.getItem(CLE_FACON_DE_JOUER));
    } catch {
        return AUTO;
    }
}

/** La partie se lance-t-elle en manuel ? (règle `mode_manuel`) */
export function lanceEnManuel(facon) {
    return normaliser(facon) === MANUEL;
}
