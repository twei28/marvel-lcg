// brouillon.js — la campagne en cours de creation, le temps d'un aller-retour.
//
// Creer une campagne demande de choisir une equipe, et le seul endroit qui
// sait le faire est l'ecran de preparation (heros, identites alternatives,
// decks, aspects). Plutot que de reecrire ce selecteur, on l'emprunte :
// campagne.html depose ici ce qu'il sait deja (boite, nom, difficulte, nombre
// de heros), envoie le joueur sur /prepare.html?campagne, et recupere l'equipe
// au retour. Le brouillon ne survit pas a la creation : il est efface des que
// la campagne est enregistree sur le serveur.
"use strict";

const CLE = "mc-campagne-brouillon";

export function lireBrouillon() {
    try {
        const brut = window.localStorage.getItem(CLE);
        return brut ? JSON.parse(brut) : null;
    } catch (e) {
        return null;
    }
}

export function ecrireBrouillon(brouillon) {
    try {
        window.localStorage.setItem(CLE, JSON.stringify(brouillon));
    } catch (e) { /* stockage indisponible : la creation echouera proprement */ }
}

export function effacerBrouillon() {
    try { window.localStorage.removeItem(CLE); } catch (e) {}
}
