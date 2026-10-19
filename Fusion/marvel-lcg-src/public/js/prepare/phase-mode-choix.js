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

// TROIS CHOIX (19/10/2026) : « Étape par étape bis » (valeur `detaille`, présentation `bis`), « Sur la table »,
// « D'un coup ». L'ancien « Étape par étape » (présentation `etape`) et « Phase dynamique » sont cachés, pas
// supprimés (drapeaux `PHASE_ETAPE_VISIBLE` / `PHASE_DYNAMIQUE_VISIBLE` de ui-app/src/board/phase-presentation.ts).
// La valeur `detaille` reste celle du mode : elle se lit « bis », sa présentation par défaut.
export const CLE_PRESENTATION_PHASE = "mc_phase_presentation";
const CLE_ANCIENNE_PHASE_BIS = "mc_phase_bis";
export const PRESENTATION_PAR_DEFAUT = "bis";

/**
 * PASSAGE UNIQUE AUX TROIS CHOIX (19/10/2026), jumeau de `migrerPhaseTroisChoix` de
 * ui-app/src/board/phase-presentation.ts (même clé de passage, même version : le premier des deux qui passe
 * fait le travail). Qui était sur l'ancien « Étape par étape » (présentation `etape`, ou l'ancien `mc_phase_bis`
 * à « non ») ou sur « Phase dynamique » passe sur « bis ». Le mode (`detaille`, `sur-table`, `instantane`) n'est
 * jamais touché. Rend vrai si le passage vient d'avoir lieu. Le choix vit dans le navigateur seulement.
 */
export const CLE_MIGRATION_PHASE = "mc_phase_trois_choix_migre";
export const VERSION_MIGRATION_PHASE = "2026-10-19";
export function migrerPhaseTroisChoix(stockage) {
    try {
        if (!stockage || stockage.getItem(CLE_MIGRATION_PHASE) === VERSION_MIGRATION_PHASE) return false;
        const stocke = stockage.getItem(CLE_PRESENTATION_PHASE);
        const ancienNon = stocke === null && stockage.getItem(CLE_ANCIENNE_PHASE_BIS) === "non";
        if (ancienNon || (stocke !== null && stocke !== PRESENTATION_PAR_DEFAUT && stocke !== "tris")) stockage.setItem(CLE_PRESENTATION_PHASE, PRESENTATION_PAR_DEFAUT);
        stockage.setItem(CLE_MIGRATION_PHASE, VERSION_MIGRATION_PHASE);
        return true;
    } catch (e) { return false; }
}

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
