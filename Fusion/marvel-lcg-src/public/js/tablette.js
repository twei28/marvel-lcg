// tablette.js : la tablette sur les pages hors plateau (chantier du 24/10/2026,
// .planning/todos/2026-10-24-mode-tablette.md, decision 11).
//
// Meme regle que le plateau (ui-app/src/board/tablette/tablette.ts) : un ecran
// tactile SANS souris, 768 px de large et plus de 500 px de haut, ou le reglage
// « Jeu au doigt » (Auto / Oui / Non) du plateau, retenu sur cet appareil.
// `marquerTablette()` pose <html data-tablette> : les feuilles de style des
// pages s'en servent (cibles de 44 px, pas de survol).
"use strict";

export const CLE_JEU_AU_DOIGT = "marvel-jeu-au-doigt";
export const REQUETE_TABLETTE = "(pointer: coarse) and (hover: none) and (min-width: 768px) and (min-height: 501px)";

/** La regle, PURE : le reglage l'emporte, Auto suit l'appareil. */
export function tabletteEffective(reglage, appareil) {
    if (reglage === "oui") return true;
    if (reglage === "non") return false;
    return appareil === true;
}

export function estTablette() {
    let reglage = null;
    try { reglage = localStorage.getItem(CLE_JEU_AU_DOIGT); } catch (e) { /* stockage indisponible */ }
    let appareil = false;
    try { appareil = window.matchMedia(REQUETE_TABLETTE).matches; } catch (e) { /* pas de matchMedia */ }
    return tabletteEffective(reglage, appareil);
}

/** Pose (ou retire) <html data-tablette>, et le tient a jour si l'ecran change. */
export function marquerTablette() {
    // La feuille des pages au doigt, posee une fois (elle ne vise que html[data-tablette]).
    if (!document.querySelector('link[data-tablette-pages]')) {
        const lien = document.createElement("link");
        lien.rel = "stylesheet";
        lien.href = "/public/css/tablette-pages.css?v=1";
        lien.setAttribute("data-tablette-pages", "");
        document.head.append(lien);
    }
    const appliquer = () => document.documentElement.toggleAttribute("data-tablette", estTablette());
    appliquer();
    try { window.matchMedia(REQUETE_TABLETTE).addEventListener("change", appliquer); } catch (e) { /* rien a suivre */ }
    return estTablette();
}
