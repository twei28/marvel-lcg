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
// REAFFICHAGE UNIQUE (decision de l'utilisateur, 20/10/2026) : la fenetre est posee une fois de plus a TOUS les joueurs,
// y compris ceux qui avaient deja vu l'ancienne (cle `mc_phase_mode_vu_v1` a « 1 », qui ne compte plus). Meme mecanisme
// que la migration datee : la cle porte la VERSION du choix ; valeur a jour = jamais plus. Aucune migration des choix
// ici (les choix deja ranges sont gardes et preselectionnes).
export const CLE_PHASE_CHOIX_VU = "mc_phase_choix_vu";
export const VERSION_CHOIX_PHASE = "2026-10-20";

export const DETAILLE = "detaille";
export const SUR_TABLE = "sur-table";
export const INSTANTANE = "instantane";

// TROIS CHOIX (19/10/2026) : « Guidée » (valeur `detaille`, présentation `tris`), « Plateau animé » (`sur-table`),
// « Accéléré » (`instantane`). « Étape par étape » (`etape`), « Étape par étape bis » (`bis`) et « Phase dynamique » sont cachés, pas
// supprimés (drapeaux `PHASE_ETAPE_VISIBLE` / `PHASE_DYNAMIQUE_VISIBLE` de ui-app/src/board/phase-presentation.ts).
// La valeur `detaille` reste celle du mode : elle se lit « tris », sa présentation par défaut.
export const CLE_PRESENTATION_PHASE = "mc_phase_presentation";
const CLE_ANCIENNE_PHASE_BIS = "mc_phase_bis";
export const PRESENTATION_PAR_DEFAUT = "tris";

/**
 * Les captures de la fenêtre « Choisis ta phase du méchant » (img/phase-modes/*.jpg) sont CACHÉES depuis
 * le 19/10/2026 (trop anciennes) : seulement le nom et une courte description de chaque mode. Les fichiers
 * et le code du carrousel restent : remettre `true` les montre de nouveau.
 */
export const PHASE_IMAGES_VISIBLES = false;

/**
 * PASSAGE UNIQUE AUX TROIS CHOIX (19/10/2026), jumeau de `migrerPhaseTroisChoix` de
 * ui-app/src/board/phase-presentation.ts (même clé de passage, même version : le premier des deux qui passe
 * fait le travail). Qui était sur « Étape par étape » (`etape`, ou l'ancien `mc_phase_bis` à « non »), « Étape par étape bis »
 * (`bis`) ou « Phase dynamique » passe sur « tris » (« Guidée »). Version `2026-10-19b` : ceux déjà passés sur « bis » le sont une seconde fois. Le mode (`detaille`, `sur-table`, `instantane`) n'est
 * jamais touché. Rend vrai si le passage vient d'avoir lieu. Le choix vit dans le navigateur seulement.
 */
export const CLE_MIGRATION_PHASE = "mc_phase_trois_choix_migre";
export const VERSION_MIGRATION_PHASE = "2026-10-19b";
export function migrerPhaseTroisChoix(stockage) {
    try {
        if (!stockage || stockage.getItem(CLE_MIGRATION_PHASE) === VERSION_MIGRATION_PHASE) return false;
        const stocke = stockage.getItem(CLE_PRESENTATION_PHASE);
        const ancienNon = stocke === null && stockage.getItem(CLE_ANCIENNE_PHASE_BIS) === "non";
        if (ancienNon || (stocke !== null && stocke !== PRESENTATION_PAR_DEFAUT)) stockage.setItem(CLE_PRESENTATION_PHASE, PRESENTATION_PAR_DEFAUT);
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

/** Faut-il montrer la fenêtre ? Seulement si la version vue n'est pas la version courante (`CLE_PHASE_CHOIX_VU`). */
export function doitProposerLeChoix(vu) {
    return vu !== VERSION_CHOIX_PHASE;
}

/**
 * Que écrire dans `CLE_MODE_PHASE` à la validation ? `null` = ne rien écrire.
 *
 * ⚠ ON N'ÉCRIT QUE CE QUI CHANGE. Le plateau migre une fois les anciens
 * réglages de phase (`migrerReglagesPhase`), et ne le fait plus dès que la clé
 * porte une valeur du nouveau schéma. Écrire « detaille » pour quelqu'un qui n'a
 * rien touché lui ferait perdre cette migration.
 */
export function modeAEcrire(brutAvant, choisi, tablette = false) {
    // Tablette sans reglage : le plateau demarrerait sur « Plateau anime » (moteur.ts), le choix s'ecrit donc toujours.
    if (tablette && brutAvant === null) return MODES.includes(choisi) ? choisi : null;
    if (choisi === normaliser(brutAvant)) return null;
    return MODES.includes(choisi) ? choisi : null;
}

/**
 * LA TABLETTE (24/10/2026, decisions 8 et 11) : un joueur qui n'a encore rien choisi part de « Plateau anime »
 * (la table reste entiere au doigt). Meme regle que ui-app/src/board/tablette/tablette.ts : tactile sans souris,
 * 768 px de large et plus de 500 px de haut, ou le reglage « Jeu au doigt ».
 */
export const CLE_JEU_AU_DOIGT = "marvel-jeu-au-doigt";
export const REQUETE_TABLETTE = "(pointer: coarse) and (hover: none) and (min-width: 768px) and (min-height: 501px)";
export function estTablette(reglage, appareil) {
    if (reglage === "oui") return true;
    if (reglage === "non") return false;
    return appareil === true;
}
export function choixInitial(brutAvant, tablette) {
    if (tablette && brutAvant === null) return SUR_TABLE;
    return normaliser(brutAvant);
}
