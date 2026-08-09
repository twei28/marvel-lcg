// tutoriel-etat.js — décide si le coach du mode Découverte doit être armé.
//
// Module PUR (aucun import, aucun accès direct au navigateur) : node peut
// l'exécuter tel quel, ce que fait outils/verifier-tutoriel-etat.mjs. Même
// esprit que salon-etat.js.
//
// La clé de stockage est un état GLOBAL et PERSISTANT : rien ne la rattache à
// la partie qui l'a posée. C'est ce qui faisait déborder le coach sur toutes
// les parties suivantes : lancé une fois puis abandonné en cours de route, le
// mode Découverte laissait dans le stockage le nom de la leçon atteinte, et
// chaque partie ultérieure la relisait — y compris les puzzles, les reprises
// et le multijoueur, qui n'arment jamais rien eux-mêmes.
//
// La règle est donc : le wizard DÉSARME au chargement, quoi qu'il arrive, et
// seul un lancement en mode Découverte réarme, juste avant de rejoindre le
// plateau. Le coach survit ainsi à un rechargement du plateau (on ne repasse
// pas par le wizard) mais jamais à un retour à la préparation.
"use strict";

export const CLE_TUTORIEL = "marvel-board-tutoriel";

/** Identifiant de la première leçon.
 *  À changer EN MÊME TEMPS que `PREMIERE_LECON` de
 *  ui-app/src/board/CoucheCoach.tsx : public/js/ et ui-app/ sont deux mondes
 *  séparés, aucun import n'est possible entre eux. */
export const PREMIERE_LECON = "mulligan";

/** Valeur à écrire pour ce mode, ou null quand il faut effacer la clé. */
export function valeurTutoriel(mode) {
    return mode && mode.id === "decouverte" ? PREMIERE_LECON : null;
}

/** Applique la décision à un stockage (localStorage ou équivalent de test).
 *  Rend la valeur écrite, ou null si la clé a été effacée. */
export function appliquerTutoriel(stockage, mode) {
    const valeur = valeurTutoriel(mode);
    try {
        if (valeur === null) stockage.removeItem(CLE_TUTORIEL);
        else stockage.setItem(CLE_TUTORIEL, valeur);
    } catch (e) {
        /* stockage indisponible : le coach ne s'armera pas, le jeu reste jouable */
    }
    return valeur;
}
