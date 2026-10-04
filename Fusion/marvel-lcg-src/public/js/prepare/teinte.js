// teinte.js : la teinte du fond, cote preparation (04/10/2026).
//
// Stockage (`mc_teinte_v1`, lu aussi par le plateau), envoi au compte, et la
// roue de couleurs de la fenetre « Choisis ton affichage ». Les calculs sont
// dans teinte-choix.js, jumeau de `ui-app/src/board/teinte.ts`.
"use strict";

import {
    BORNES, CLE_TEINTE, TEINTE_DE_DEPART, bornerTeinte, ecrireTeinteEnTexte, lireTeinte,
    pointDeLaTeinte, teinteDuCompte, teinteDuPoint, variablesDeTeinte,
} from "/public/js/prepare/teinte-choix.js";
import { t } from "/public/js/prepare/langue.js";

export function teinteActuelle() {
    try { return lireTeinte(localStorage.getItem(CLE_TEINTE)); }
    catch (e) { return undefined; }
}

function envoyer(valeur) {
    try {
        fetch("/save_preferences", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ changements: { teinte: valeur } }),
        }).catch(() => {});
    } catch (e) { /* hors ligne : le navigateur garde le choix */ }
}

/** Range le choix ; `undefined` = couleur d'origine. */
export function choisirTeinte(teinte, versLeCompte = true) {
    try {
        if (teinte) localStorage.setItem(CLE_TEINTE, ecrireTeinteEnTexte(teinte));
        else localStorage.removeItem(CLE_TEINTE);
    } catch (e) { /* stockage indisponible */ }
    if (versLeCompte) envoyer(teinte ? ecrireTeinteEnTexte(teinte) : null);
}

/** Aligne le navigateur sur le compte, avec la reponse deja lue de
 *  `/get_preferences` (synchroniserAffichage la rend). */
export function synchroniserTeinte(reponse) {
    const duCompte = teinteDuCompte(reponse);
    if (duCompte === undefined) return;
    choisirTeinte(duCompte ?? undefined, false);
}

/** Les couleurs de l'apercu : la teinte choisie, ou le fond d'origine. */
function couleursApercu(teinte) {
    if (!teinte) return { table: "#14181f", bandeau: "#1e1e1e", panneau: "#1e1e1e", titre: "rgba(226, 232, 240, 0.78)" };
    const v = variablesDeTeinte(teinte);
    return { table: v["--teinte-table"], bandeau: v["--teinte-bandeau"], panneau: v["--teinte-panneau"], titre: v["--teinte-texte-table"] };
}

/**
 * La roue de couleurs, avec son curseur de luminosite, son bouton « Couleur
 * d'origine » et un petit apercu de table (bandeau, panneau, trois cartes)
 * qui change en direct. `quandChange(teinte|undefined)` a chaque geste.
 */
export function roueTeinte(depart, quandChange) {
    let valeur = depart;
    const el = (tag, attrs = {}, ...enfants) => {
        const n = document.createElement(tag);
        for (const [k, v] of Object.entries(attrs)) {
            if (k === "class") n.className = v;
            else if (k.startsWith("on")) n.addEventListener(k.slice(2), v);
            else n.setAttribute(k, v);
        }
        for (const e of enfants) n.append(e);
        return n;
    };
    const repere = el("span", { class: "rt-repere", "aria-hidden": "true" });
    const disque = el("div", {
        class: "rt-disque", role: "slider", tabindex: "0",
        "aria-label": t("Teinte du fond"), "aria-valuemin": "0", "aria-valuemax": "359",
    }, repere);
    const clarte = el("input", { type: "range", min: String(BORNES.l[0]), max: String(BORNES.l[1]), "aria-label": t("Luminosité du fond") });
    const origine = el("button", { type: "button", class: "rt-origine" }, t("Couleur d’origine"));
    const apercuTitre = el("span", { class: "rt-apercu-titre" }, t("Méchant"));
    const apercuBandeau = el("div", { class: "rt-apercu-bandeau" });
    const apercuPanneau = el("div", { class: "rt-apercu-panneau" });
    const apercu = el("div", { class: "rt-apercu", "aria-hidden": "true" },
        apercuBandeau, apercuTitre,
        el("div", { class: "rt-apercu-cartes" }, el("i"), el("i"), el("i")),
        apercuPanneau);

    const dessiner = () => {
        const tnt = valeur || TEINTE_DE_DEPART;
        const lDessin = Math.max(20, tnt.l);
        const teintes = Array.from({ length: 13 }, (_, i) => `hsl(${i * 30} ${BORNES.s[1]}% ${lDessin}%)`).join(", ");
        disque.style.background = `radial-gradient(closest-side, hsl(0 0% ${lDessin}%), hsl(0 0% ${lDessin}% / 0)), conic-gradient(${teintes})`;
        const p = pointDeLaTeinte(tnt);
        repere.style.left = `${50 + p.x * 50}%`;
        repere.style.top = `${50 + p.y * 50}%`;
        repere.style.background = `hsl(${tnt.h} ${tnt.s}% ${tnt.l}%)`;
        disque.setAttribute("aria-valuenow", String(tnt.h));
        clarte.value = String(tnt.l);
        origine.disabled = !valeur;
        const c = couleursApercu(valeur);
        apercu.style.background = c.table;
        apercuBandeau.style.background = c.bandeau;
        apercuPanneau.style.background = c.panneau;
        apercuTitre.style.color = c.titre;
    };
    const changer = (suivante) => {
        valeur = suivante ? bornerTeinte(suivante) : undefined;
        dessiner();
        quandChange(valeur);
    };
    const depuisLePointeur = (e) => {
        const boite = disque.getBoundingClientRect();
        const rayon = boite.width / 2;
        changer(teinteDuPoint(e.clientX - boite.left - rayon, e.clientY - boite.top - rayon, rayon, (valeur || TEINTE_DE_DEPART).l));
    };
    disque.addEventListener("pointerdown", (e) => { disque.setPointerCapture(e.pointerId); depuisLePointeur(e); });
    disque.addEventListener("pointermove", (e) => { if (disque.hasPointerCapture(e.pointerId)) depuisLePointeur(e); });
    disque.addEventListener("keydown", (e) => {
        const tnt = valeur || TEINTE_DE_DEPART;
        const pas = e.shiftKey ? 15 : 5;
        const suivante = e.key === "ArrowRight" ? { ...tnt, h: tnt.h + pas }
            : e.key === "ArrowLeft" ? { ...tnt, h: tnt.h - pas }
            : e.key === "ArrowUp" ? { ...tnt, s: tnt.s + 1 }
            : e.key === "ArrowDown" ? { ...tnt, s: tnt.s - 1 }
            : null;
        if (!suivante) return;
        e.preventDefault();
        changer(suivante);
    });
    clarte.addEventListener("input", () => changer({ ...(valeur || TEINTE_DE_DEPART), l: Number(clarte.value) }));
    origine.addEventListener("click", () => changer(undefined));
    dessiner();
    return el("div", { class: "rt" },
        el("div", { class: "rt-commandes" },
            disque,
            el("label", { class: "rt-clarte" }, el("span", {}, t("Plus sombre")), clarte, el("span", {}, t("Plus clair"))),
            origine),
        apercu);
}
