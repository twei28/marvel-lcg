// teinte-page.js : pose la TEINTE DU FOND sur une page du jeu (04/10/2026).
//
// Choix de l'utilisateur : la couleur du fond vaut « partout » (plateau,
// preparation, pages du jeu). Le plateau a son propre module (ui-app,
// board/teinte.ts) ; les pages HTML chargent celui-ci, avec la feuille
// /public/css/teinte-pages.css. Les couleurs viennent de teinte-choix.js, le
// jumeau du plateau : memes calculs, memes valeurs.
//
// ⚠ SUR CES PAGES, LE TEXTE EST POSE A MEME LE FOND. Le fond prend donc la
// luminosite des PANNEAUX (24 % au plus), pas celle de la table qui peut aller
// jusqu'au gris clair : la teinte et sa saturation suivent, la lisibilite reste.
"use strict";

import { CLE_TEINTE, SEUIL_TABLE_CLAIRE, bornerTeinte, lireTeinte, variablesDeTeinte } from "/public/js/prepare/teinte-choix.js";

const NOMS = Object.keys(variablesDeTeinte({ h: 0, s: 0, l: 20 }));

/** Pose (ou retire, avec `undefined`) la teinte sur la page. */
export function appliquerTeintePage(teinte) {
    const racine = document.documentElement;
    for (const nom of NOMS) racine.style.removeProperty(nom);
    if (!teinte) { delete racine.dataset.teinte; return; }
    for (const [nom, valeur] of Object.entries(variablesDeTeinte(teinte))) racine.style.setProperty(nom, valeur);
    racine.dataset.teinte = bornerTeinte(teinte).l >= SEUIL_TABLE_CLAIRE ? "claire" : "sombre";
}

function lireDuNavigateur() {
    try { return lireTeinte(localStorage.getItem(CLE_TEINTE)); }
    catch (e) { return undefined; }
}

appliquerTeintePage(lireDuNavigateur());
// Un autre onglet (le plateau, la preparation) a change la couleur : suivre.
window.addEventListener("storage", (e) => {
    if (e.key === CLE_TEINTE || e.key === null) appliquerTeintePage(lireDuNavigateur());
});
