// phase-mode-choix.js : la fenêtre « Choisis ta phase du méchant » (05/10/2026).
//
// Demandée par l'utilisateur : à la première connexion, et pour tout joueur qui
// n'a pas encore vu les trois façons de vivre la phase du méchant, les lui
// présenter avec une image chacune, comme pour Normal / Sobre.
//
// Deux clés de stockage :
//  - `CLE_MODE_PHASE`, celle que LIT LE PLATEAU (ui-app/src/board/moteur.ts) ;
//  - `CLE_PHASE_MODE_VU`, « cette fenêtre a été montrée », propre à cette page.
//
// Module PUR (ni DOM ni stockage) : testé par
// `node --test tools/tests-lanceur/phase-mode-choix.test.mjs`.
"use strict";

export const CLE_MODE_PHASE = "marvel-board-mode-phase-mechant";
export const CLE_PHASE_MODE_VU = "mc_phase_mode_vu_v1";

export const DETAILLE = "detaille";
export const SUR_TABLE = "sur-table";
export const INSTANTANE = "instantane";

/** Dans l'ordre où le plateau les propose : le mode par défaut d'abord. */
export const MODES = [DETAILLE, SUR_TABLE, INSTANTANE];

/** Toute valeur inconnue (absente, abîmée, ancien schéma) vaut « detaille ». */
export function normaliser(valeur) {
    return MODES.includes(valeur) ? valeur : DETAILLE;
}

/** Faut-il montrer la fenêtre ? Seulement à qui ne l'a jamais vue. */
export function doitProposerLeChoix(vu) {
    return vu !== "1";
}

/**
 * Que écrire dans `CLE_MODE_PHASE` à la validation ? `null` = ne rien écrire.
 *
 * ⚠ ON N'ÉCRIT QUE CE QUI CHANGE. Le plateau migre une fois les anciens
 * réglages de phase (`migrerReglagesPhase`), et ne le fait plus dès que la clé
 * porte une valeur du nouveau schéma. Écrire « detaille » pour quelqu'un qui n'a
 * rien touché lui ferait perdre cette migration.
 */
export function modeAEcrire(brutAvant, choisi) {
    if (choisi === normaliser(brutAvant)) return null;
    return MODES.includes(choisi) ? choisi : null;
}
