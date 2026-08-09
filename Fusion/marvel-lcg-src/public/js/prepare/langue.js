// langue.js — bascule FR/EN du wizard (et pages associées).
//
// Même contrat que ui-app/src/board/langue.ts : le français est la langue
// source du code, t('texte français') renvoie l'anglais via DICO_EN quand la
// langue est 'en'. La bascule prévient le moteur (/set_language) pour que la
// narration de la partie suive, puis recharge la page.
"use strict";

import { DICO_EN_BASE } from "/public/js/prepare/dico-en.js";

const CLE_LANGUE = "marvel-langue";

export function langueActuelle() {
    try {
        return localStorage.getItem(CLE_LANGUE) === "en" ? "en" : "fr";
    } catch (e) {
        return "fr";
    }
}

/** Français → anglais. Base commune (dico-en.js) + ajouts par écran ; une clé
    absente reste en FR. */
const DICO_EN = { ...DICO_EN_BASE };

export function enregistrerTraductions(entrees) {
    Object.assign(DICO_EN, entrees);
}

export function t(fr) {
    if (langueActuelle() === "fr") return fr;
    return Object.prototype.hasOwnProperty.call(DICO_EN, fr) ? DICO_EN[fr] : fr;
}

/** Aligne la narration du moteur sur la langue choisie (au chargement). */
export function synchroniserLangueServeur() {
    fetch("/set_language?" + langueActuelle()).catch(() => {});
}

export async function basculerLangue() {
    const nouvelle = langueActuelle() === "fr" ? "en" : "fr";
    try {
        localStorage.setItem(CLE_LANGUE, nouvelle);
    } catch (e) { /* stockage indisponible : la bascule serveur reste utile */ }
    try {
        await fetch("/set_language?" + nouvelle);
    } catch (e) { /* hors ligne : le client bascule quand même */ }
    location.reload();
}

/** Bouton 🌐 FR/EN prêt à poser dans un header (élément DOM autonome). */
export function boutonLangue(classe) {
    const bouton = document.createElement("button");
    bouton.type = "button";
    bouton.className = classe || "btn-langue";
    bouton.title = langueActuelle() === "fr"
        ? "Interface et narration en français : cliquer pour passer en anglais"
        : "Interface and narration in English: click to switch to French";
    bouton.textContent = "🌐 " + (langueActuelle() === "fr" ? "FR" : "EN");
    bouton.addEventListener("click", () => { basculerLangue(); });
    return bouton;
}
