// affichage-choix.js : le réglage « Affichage : Normal / Sobre ».
//
// Une seule clé de stockage, `mc_affichage_v1`, lue AUSSI par le plateau
// (ui-app/src/board/affichage.ts). Valeurs : "normal" (défaut) ou "sobre".
//
// Module PUR (ni DOM ni stockage) : testé par
// `node --test tools/tests-lanceur/affichage-choix.test.mjs`.
"use strict";

export const CLE_AFFICHAGE = "mc_affichage_v1";
export const NORMAL = "normal";
export const SOBRE = "sobre";

/** Toute valeur inconnue (absente, abîmée, ancienne) vaut « normal ». */
export function normaliser(valeur) {
    return valeur === SOBRE ? SOBRE : NORMAL;
}

export function inverse(valeur) {
    return normaliser(valeur) === SOBRE ? NORMAL : SOBRE;
}

/**
 * Réconcilie le navigateur avec la réponse de `/get_preferences`, sur le même
 * contrat que les arts de héros (arts-heros-choix.js, `reconcilier`).
 *
 * Rend `null` quand le serveur n'est pas la référence (invité, moteur local).
 * Sinon `{ affichage, pousser }` : la valeur à garder dans le navigateur, et
 * les changements à envoyer au compte (vide si rien).
 *  - le compte a déjà un fichier : il fait foi ;
 *  - sinon on y verse le choix du navigateur, s'il diffère du défaut.
 */
export function reconcilier(local, reponse) {
    if (!reponse || !reponse.compte) return null;
    const ici = normaliser(local);
    if (!reponse.existe) {
        return { affichage: ici, pousser: ici === SOBRE ? { affichage: SOBRE } : {} };
    }
    const prefs = reponse.preferences || {};
    return { affichage: normaliser(prefs.affichage), pousser: {} };
}

/**
 * Faut-il proposer la fenêtre « Choisis ton affichage » ? (04/10/2026)
 *
 * Choix de l'utilisateur : tout joueur qui n'a JAMAIS choisi la voit une fois,
 * nouveau comme ancien. A déjà choisi :
 *  - le navigateur qui a une valeur rangée (`local`, brute, avant
 *    normalisation : `null` veut dire « jamais touché ») ;
 *  - le compte dont le fichier de préférences porte déjà `affichage`.
 */
export function doitProposerLeChoix(local, reponse) {
    if (local === NORMAL || local === SOBRE) return false;
    const prefs = reponse && reponse.compte && reponse.existe ? (reponse.preferences || {}) : {};
    return !Object.prototype.hasOwnProperty.call(prefs, "affichage");
}
