// tel-pages.js : le mode téléphone des pages hors assistant (galerie, campagne,
// éditeur de deck). Zone 2 de la refonte du 09/10/2026
// (.planning/todos/2026-10-09-mode-telephone-refonte.md).
//
// Mêmes briques que l'assistant (js/prepare/tel.js, réutilisé tel quel) :
// `html.tel` sous 768 px, poignée des feuilles basses. Ajoute ce que ces pages
// partagent : l'en-tête fin à burger, et la feuille basse inscrite dans
// l'historique (Retour Android la ferme au lieu de quitter la page).
// Au-dessus de 768 px, rien ici ne fait quoi que ce soit.
"use strict";

import { estTel, suivreTel, ajouterPoignee } from "/public/js/prepare/tel.js";
import { t, boutonLangue, enregistrerTraductions } from "/public/js/prepare/langue.js";
import { boutonAffichage } from "/public/js/prepare/affichage.js";
import { urlNarval } from "/public/js/prepare/narval.js";

export { estTel, suivreTel, ajouterPoignee };

enregistrerTraductions({
    "Menu": "Menu",
    "Accueil du jeu": "Game home",
    "Jouer": "Play",
    "Campagne": "Campaign",
    "Galerie": "Gallery",
    "Éditeur de deck": "Deck editor",
    "Retour": "Back",
});

function el(tag, attrs, ...enfants) {
    const n = document.createElement(tag);
    for (const [k, v] of Object.entries(attrs || {})) {
        if (v == null) continue;
        if (k === "onclick") n.addEventListener("click", v);
        else n.setAttribute(k, v);
    }
    for (const e of enfants) if (e != null) n.append(e.nodeType ? e : document.createTextNode(String(e)));
    return n;
}

const LIENS = [
    ["/prepare.html", "Jouer"],
    ["/campagne.html", "Campagne"],
    ["/galerie.html", "Galerie"],
    ["/deck-builder.html", "Éditeur de deck"],
];

/**
 * L'en-tête fin du téléphone : retour (narval), titre, langue, burger. Le menu
 * se déroule sous l'en-tête, un voile derrière ; la page courante n'y figure
 * pas. `extra` : nœuds ajoutés en bas du menu (outils propres à la page).
 */
export function enteteTel({ titre, retour = "/prepare.html", ici = "", extra = [] }) {
    const entete = el("header", { class: "tp-entete" });
    const fermer = () => basculer(false);
    const basculer = (ouvert) => {
        entete.classList.toggle("menu-ouvert", ouvert);
        burger.setAttribute("aria-expanded", ouvert ? "true" : "false");
    };
    const burger = el("button", {
        class: "tp-burger", type: "button", "aria-label": t("Menu"), "aria-expanded": "false",
        onclick: () => basculer(!entete.classList.contains("menu-ouvert")),
    }, "☰");
    const menu = el("nav", { class: "tp-menu", "aria-label": t("Menu") },
        ...LIENS.filter(([href]) => href !== ici).map(([href, libelle]) =>
            el("a", { class: "tp-lien", href }, t(libelle))),
        boutonAffichage("tp-lien tp-affichage"),
        ...extra);
    entete.append(
        el("div", { class: "tp-rang" },
            el("a", { class: "tp-retour", href: retour, "aria-label": t("Retour") },
                el("span", { class: "tp-chevron", "aria-hidden": "true" }, "‹"),
                el("img", { class: "tp-narval", src: urlNarval(), alt: "" })),
            el("h1", { class: "tp-titre mvl" }, titre),
            boutonLangue("tp-langue"),
            burger),
        el("div", { class: "tp-voile", onclick: fermer }),
        menu);
    document.addEventListener("keydown", (e) => { if (e.key === "Escape") fermer(); });
    return entete;
}

/* ---- Feuille basse inscrite dans l'historique ------------------------------
   Ouvrir pousse une entrée ; Retour Android la retire et ferme la feuille.
   Fermer par l'interface recule d'un cran (la pile reste propre). `apres`
   (facultatif) ne s'exécute qu'une fois le recul fait, pour qu'une action qui
   pousse à son tour une entrée (changer d'écran) ne s'emmêle pas avec lui. */
export function feuilleDansHistorique(fermer) {
    if (!estTel()) return (apres) => { fermer(); if (apres) apres(); };
    let ouverte = true;
    try { history.pushState({ telFeuille: 1 }, ""); } catch (e) { /* sans historique, la feuille marche quand même */ }
    const surRetour = () => {
        if (!ouverte) return;
        ouverte = false;
        window.removeEventListener("popstate", surRetour);
        fermer();
    };
    window.addEventListener("popstate", surRetour);
    return (apres) => {
        if (!ouverte) { if (apres) apres(); return; }
        ouverte = false;
        window.removeEventListener("popstate", surRetour);
        fermer();
        if (history.state && history.state.telFeuille) {
            if (apres) window.addEventListener("popstate", () => apres(), { once: true });
            history.back();
        } else if (apres) apres();
    };
}

/**
 * Une feuille basse prête à l'emploi : voile, panneau, poignée, corps qui
 * défile. Fermée par la poignée (glisser ou toucher), le voile, Échap ou
 * Retour Android. Rend la fonction de fermeture (qui accepte un `apres`).
 */
export function ouvrirFeuille({ classe = "", titre = null, contenu = [], quandFermee = null }) {
    const corps = el("div", { class: "tp-feuille-corps" }, ...contenu);
    const panneau = el("div", { class: "tp-feuille " + classe, role: "dialog", "aria-modal": "true" },
        titre, corps);
    const voile = el("div", { class: "tp-feuille-voile" }, panneau);
    const surTouche = (e) => { if (e.key === "Escape") fermer(); };
    const fermer = feuilleDansHistorique(() => {
        voile.remove();
        document.removeEventListener("keydown", surTouche);
        if (quandFermee) quandFermee();
    });
    voile.addEventListener("click", (e) => { if (e.target === voile) fermer(); });
    document.addEventListener("keydown", surTouche);
    ajouterPoignee(panneau, () => fermer());
    document.body.append(voile);
    return fermer;
}
