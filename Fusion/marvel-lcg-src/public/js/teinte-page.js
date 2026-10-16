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
import { CLE_AFFICHAGE, SOBRE, normaliser, poserAttributs, verifierEpurePermis } from "/public/js/prepare/affichage-choix.js";

const NOMS = Object.keys(variablesDeTeinte({ h: 0, s: 0, l: 20 }));

let teinteDemandee;

/** Pose (ou retire, avec `undefined`) la teinte sur la page. En affichage
 *  sobre, la teinte est retenue mais pas posee. */
export function appliquerTeintePage(teinte) {
    teinteDemandee = teinte;
    const racine = document.documentElement;
    for (const nom of NOMS) racine.style.removeProperty(nom);
    if (!teinte || racine.dataset.affichage === SOBRE) { delete racine.dataset.teinte; return; }
    for (const [nom, valeur] of Object.entries(variablesDeTeinte(teinte))) racine.style.setProperty(nom, valeur);
    racine.dataset.teinte = bornerTeinte(teinte).l >= SEUIL_TABLE_CLAIRE ? "claire" : "sombre";
}

function lireDuNavigateur() {
    try { return lireTeinte(localStorage.getItem(CLE_TEINTE)); }
    catch (e) { return undefined; }
}

// L'AFFICHAGE SOBRE (09/10/2026) vaut sur toutes les pages, pas seulement la
// preparation : on le pose ici, et il retire la teinte du fond (gris neutre).
function lireAffichage() {
    try { return normaliser(localStorage.getItem(CLE_AFFICHAGE)); }
    catch (e) { return normaliser(null); }
}

if (!document.documentElement.dataset.affichage) poserAttributs(document.documentElement, lireAffichage());
// L'épuré n'est permis qu'à l'administrateur : une fois le serveur entendu, on repose.
verifierEpurePermis().then(() => poserAttributs(document.documentElement, lireAffichage()));
appliquerTeintePage(lireDuNavigateur());
// La bascule de l'en-tete change `data-affichage` sans recharger : suivre.
new MutationObserver(() => appliquerTeintePage(teinteDemandee)).observe(document.documentElement, { attributes: true, attributeFilter: ["data-affichage"] });
// Un autre onglet (le plateau, la preparation) a change la couleur ou l'affichage : suivre.
window.addEventListener("storage", (e) => {
    if (e.key === CLE_AFFICHAGE || e.key === null) poserAttributs(document.documentElement, lireAffichage());
    if (e.key === CLE_TEINTE || e.key === null) appliquerTeintePage(lireDuNavigateur());
});
