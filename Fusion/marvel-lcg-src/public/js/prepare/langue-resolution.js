// langue-resolution.js — la langue du jeu, de façon PURE (sans DOM, sans stockage).
//
// Décision du 26/10/2026 : sur une table en ligne (p<N>.<domaine>, une autre ORIGINE que le site), le jeu ne voyait pas le choix de
// langue fait sur le site : il partait en français. Il suit maintenant, dans cet ordre :
//   1. le choix déjà fait DANS le jeu (localStorage « marvel-langue ») ;
//   2. le cookie « nc_langue », posé par le site avec Domain=.<domaine> (site/orchestrateur.py, route /langue) ;
//   3. la langue du navigateur (« en… » = anglais) ;
//   4. le français.
// Le jeu écrit aussi ce cookie quand le joueur change de langue (cookieLangue) : le site et les autres tables suivent.
//
// ⚠ TROIS JUMEAUX À GARDER IDENTIQUES : ce module ; langue-classique.js (pour les petits scripts non-modules de la page de
// préparation, qui ne peuvent rien importer) ; ui-app/src/board/langue-resolution.ts (le plateau React). Les tests
// (tools/tests-lanceur/langue-jeu.test.mjs et ui-app/src/board/langue-resolution.test.ts) les comparent sur les mêmes cas.
"use strict";

export const CLE_LANGUE = "marvel-langue";
export const COOKIE_LANGUE = "nc_langue";
const DUREE_COOKIE_S = 31536000; // un an, comme le site

/** « en » ou « fr » ; tout le reste → "". */
export function langueValide(valeur) {
    return valeur === "en" || valeur === "fr" ? valeur : "";
}

/** La langue portée par le cookie nc_langue d'un `document.cookie`, ou "". */
export function lireCookieLangue(cookie) {
    for (const morceau of String(cookie || "").split(";")) {
        const i = morceau.indexOf("=");
        if (i < 0) continue;
        if (morceau.slice(0, i).trim() === COOKIE_LANGUE) {
            const valeur = morceau.slice(i + 1).trim();
            if (valeur === "en" || valeur === "fr") return valeur;
        }
    }
    return "";
}

/** « en » si le navigateur est en anglais, sinon « fr ». */
export function langueDuNavigateur(navigateur) {
    const l = String((navigateur && (navigateur.language || (navigateur.languages && navigateur.languages[0]))) || "").toLowerCase();
    return l.startsWith("en") ? "en" : "fr";
}

/** { stockage, cookie, navigateur } → « fr » | « en ». Voir l'ordre en tête de fichier. */
export function resoudreLangue(entrees) {
    const e = entrees || {};
    const stockee = langueValide(e.stockage);
    if (stockee) return stockee;
    const cookie = lireCookieLangue(e.cookie);
    if (cookie) return cookie;
    return langueDuNavigateur(e.navigateur);
}

/** Le « Domain= » du cookie de langue pour cet hôte, comme le site (le domaine PARENT), ou "" (pas de Domain).
 *  p<N>.<domaine>, play.<domaine> et www.<domaine> remontent au domaine ; le domaine lui-même se garde ; ni IP, ni localhost,
 *  ni hôte inconnu n'ont de Domain (un cookie y resterait propre à l'hôte, ce qui est le bon comportement en local). */
export function domaineParentCookie(hote) {
    const brut = String(hote || "").trim().toLowerCase();
    if (!brut) return "";
    if (brut.startsWith("[")) return ""; // IPv6
    const sansPort = brut.replace(/:\d+$/, "");
    if (!sansPort || sansPort.includes(":")) return "";
    if (/^\d+(\.\d+){3}$/.test(sansPort)) return ""; // IPv4
    const etiquettes = sansPort.split(".");
    if (etiquettes.length < 2 || etiquettes.some((x) => !x)) return "";
    if (etiquettes.length >= 3 && /^(p\d+|play|www)$/.test(etiquettes[0])) return "." + etiquettes.slice(1).join(".");
    if (etiquettes.length === 2) return "." + sansPort;
    return "";
}

/** La valeur à écrire dans `document.cookie` : mêmes attributs que le site (Path=/, un an, SameSite=Lax, Domain parent,
 *  Secure en https). */
export function cookieLangue(langue, hote, protocole) {
    const l = langue === "en" ? "en" : "fr";
    let cookie = COOKIE_LANGUE + "=" + l + "; Path=/; Max-Age=" + DUREE_COOKIE_S + "; SameSite=Lax";
    const domaine = domaineParentCookie(hote);
    if (domaine) cookie += "; Domain=" + domaine;
    if (protocole === "https:") cookie += "; Secure";
    return cookie;
}
