// puzzle-client.js : le côté NAVIGATEUR des puzzles publiés (E6/E8/E9, docs/puzzle/PLAN.md).
//
// Parle au serveur de puzzles du site (/api/puzzle/..., site/api_puzzles.py) et au moteur de la table
// (/new_puzzle). Sans dépendance de page : tourne sous Node (outils/test_puzzle_client.mjs) ; chaque
// fonction accepte ses dépendances (fetch, location, stockage) pour les tests.
"use strict";

const CLE_MES_PUZZLES = "mc-puzzles-crees";

/** L'adresse du site qui garde les puzzles, ou null hors ligne.
 *
 *  La table vit sur `p<N>.<domaine>` (ou `play.<domaine>`) et le site sur `<domaine>` : on retire ce
 *  préfixe. Un jeu local (127.0.0.1, localhost) n'a pas de site : publication et lecture par code sont
 *  alors indisponibles, sauf si `MC_SITE_PUZZLES` donne une adresse (essais). */
export function urlSite(loc = globalThis.location, surcharge = globalThis.MC_SITE_PUZZLES) {
    if (surcharge) return String(surcharge).replace(/\/+$/, "");
    if (!loc || !loc.hostname) return null;
    const m = /^(?:p\d+|play|discord)\.(.+\..+)$/.exec(loc.hostname);
    if (m) return `${loc.protocol}//${m[1]}${loc.port ? ":" + loc.port : ""}`;
    if (/^(127\.0\.0\.1|localhost|\[::1\])$/.test(loc.hostname)) return null;
    return `${loc.protocol}//${loc.host}`;
}

function erreur(raisons, statut) {
    const e = new Error(Array.isArray(raisons) ? raisons.join(" ; ") : String(raisons));
    e.raisons = Array.isArray(raisons) ? raisons : [String(raisons)];
    e.statut = statut;
    return e;
}

async function appeler(site, methode, chemin, corps, f) {
    if (!site) throw erreur(["Les puzzles publiés demandent une connexion au site (indisponible hors ligne)."], 0);
    let reponse;
    try {
        reponse = await f(site + chemin, {
            method: methode,
            headers: corps === undefined ? {} : { "Content-Type": "application/json" },
            body: corps === undefined ? undefined : JSON.stringify(corps),
            credentials: "omit",
        });
    } catch (e) {
        throw erreur(["Le site ne répond pas."], 0);
    }
    let donnees = {};
    try { donnees = await reponse.json(); } catch (e) { /* corps vide */ }
    if (!reponse.ok) throw erreur(donnees.erreur || [`Erreur ${reponse.status}`], reponse.status);
    return donnees;
}

export function publierPuzzle(puzzle, pseudo, { site = urlSite(), f = globalThis.fetch } = {}) {
    return appeler(site, "POST", "/api/puzzle/publier", { puzzle, pseudo }, f);
}
export function lirePuzzle(code, { jouer = false, site = urlSite(), f = globalThis.fetch } = {}) {
    return appeler(site, "GET", `/api/puzzle/${encodeURIComponent(code)}${jouer ? "?jouer=1" : ""}`, undefined, f);
}
export function modifierPuzzle(code, cle, puzzle, { site = urlSite(), f = globalThis.fetch } = {}) {
    return appeler(site, "POST", `/api/puzzle/${encodeURIComponent(code)}/modifier`, { cle, puzzle }, f);
}
export function supprimerPuzzle(code, cle, { site = urlSite(), f = globalThis.fetch } = {}) {
    return appeler(site, "POST", `/api/puzzle/${encodeURIComponent(code)}/supprimer`, { cle }, f);
}

/** Monte un puzzle sur la table (le puzzle voyage dans le CORPS : une adresse est trop courte). */
export async function monterPuzzle(puzzle, { f = globalThis.fetch } = {}) {
    const reponse = await f("/new_puzzle", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(puzzle) });
    if (!reponse.ok) {
        const texte = await reponse.text().catch(() => "");
        throw erreur([texte || "Le moteur a refusé ce puzzle."], reponse.status);
    }
}

/** Résoudre par code : lit sur le site (ce qui remet le compteur de 28 jours à zéro), puis monte la table. */
export async function jouerParCode(code, deps = {}) {
    const trouve = await lirePuzzle(code, { ...deps, jouer: true });
    await monterPuzzle(trouve.puzzle, deps);
    return trouve;
}

// ------------------------------------------------------------------ Mes puzzles (ce navigateur)
// La clé d'édition n'est montrée qu'une fois, puis gardée ici : la perdre, c'est perdre la main sur le puzzle.
export function mesPuzzles(stockage = globalThis.localStorage) {
    try {
        const liste = JSON.parse(stockage.getItem(CLE_MES_PUZZLES) || "[]");
        return Array.isArray(liste) ? liste : [];
    } catch (e) { return []; }
}
export function memoriserPuzzle(entree, stockage = globalThis.localStorage) {
    const liste = mesPuzzles(stockage).filter((x) => x.code !== entree.code);
    liste.unshift({ code: entree.code, cle: entree.cle, titre: entree.titre || "", cree: entree.cree || Date.now(), expire_le: entree.expire_le || 0 });
    try { stockage.setItem(CLE_MES_PUZZLES, JSON.stringify(liste.slice(0, 200))); return true; } catch (e) { return false; }
}
export function oublierPuzzle(code, stockage = globalThis.localStorage) {
    try { stockage.setItem(CLE_MES_PUZZLES, JSON.stringify(mesPuzzles(stockage).filter((x) => x.code !== code))); } catch (e) { /* rien */ }
}
