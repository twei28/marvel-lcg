// affichage-choix.js : le réglage « Affichage : Normal / Coloré / Sobre ».
//
// Une seule clé de stockage, `mc_affichage_v1`, lue AUSSI par le plateau
// (ui-app/src/board/affichage.ts). Valeurs : "epure" (défaut), "normal" ou "sobre".
//
// ⚠ LES NOMS ONT CHANGÉ (18/10/2026, demande de l'utilisateur) SANS CHANGER LES VALEURS RANGÉES :
//   valeur "epure"  -> se lit « Normal » (l'affichage de départ de tout le monde, ex-« Épuré »)
//   valeur "normal" -> se lit « Coloré » (couleurs du héros, halo vif, ex-« Normal »)
//   valeur "sobre"  -> se lit « Sobre » (inchangé)
//
// Module PUR (ni DOM ni stockage) : testé par
// `node --test tools/tests-lanceur/affichage-choix.test.mjs`.
"use strict";

export const CLE_AFFICHAGE = "mc_affichage_v1";
export const NORMAL = "normal";
export const SOBRE = "sobre";
export const EPURE = "epure";

/** L'affichage de départ : "epure", qui se lit « Normal » (18/10/2026). */
export const PAR_DEFAUT = EPURE;

/** Toute valeur inconnue (absente, abîmée, ancienne) vaut l'affichage de départ. */
export function normaliser(valeur) {
    return valeur === NORMAL || valeur === SOBRE || valeur === EPURE ? valeur : PAR_DEFAUT;
}

/** Le bouton de l'en-tête fait tourner : Normal (epure), Coloré (normal), Sobre, Normal... */
export function suivant(valeur) {
    const v = normaliser(valeur);
    return v === EPURE ? NORMAL : v === NORMAL ? SOBRE : EPURE;
}

/**
 * Les attributs posés sur <html>. ⚠ L'ÉPURÉ EST UN SOBRE EN PLUS DÉPOUILLÉ :
 * `data-affichage` vaut « sobre » pour les deux (toute la feuille sobre et
 * chaque test `=== "sobre"` valent aussi en épuré), `data-epure` ajoute le
 * reste. Jumeau de `appliquerAffichage` (ui-app/src/board/affichage.ts).
 */
export function attributsDe(valeur) {
    const v = normaliser(valeur);
    return { affichage: v === NORMAL ? NORMAL : SOBRE, epure: v === EPURE };
}

/**
 * L'ÉPURÉ EST RÉSERVÉ AU COMPTE DE L'ADMINISTRATEUR (16/10/2026, demande de
 * l'utilisateur). Le serveur décide (`/get_site_admin`, comme lien-admin.js et
 * board/essais.ts) ; sa réponse est retenue pour la session de l'onglet, pour
 * que chaque page la connaisse dès son premier dessin. Un moteur lancé sur la
 * machine (`localhost`) y a droit, la vue « compte classique » non.
 * Un choix « épuré » rangé ailleurs se montre en SOBRE, sans être effacé.
 */
export const CLE_EPURE_PERMIS = "mc_epure_permis";

function hoteLocal() {
    const h = globalThis.location && globalThis.location.hostname;
    return h === "localhost" || h === "127.0.0.1" || h === "[::1]";
}

/**
 * L'ÉPURÉ POUR TOUT LE MONDE (18/10/2026) : c'est l'affichage « Normal », celui de départ. Tant que ce réglage
 * est vrai, `epurePermis()` répond oui à tous (aussi dans la vue « compte classique » de l'administrateur) ;
 * faux, l'ancienne réserve à l'administrateur (`epurePermisReserve`) reprend. Les trois affichages (Normal,
 * Coloré, Sobre) se CHOISISSENT : plus rien n'est forcé ni caché (« ils choisissent entre les trois »).
 */
let epurePourTous = true;
export function reglerEpurePourTous(valeur) { epurePourTous = !!valeur; }

export function epurePermis() {
    return epurePourTous || epurePermisReserve();
}

/** L'ancienne règle : réservé à l'administrateur (conservée, voir `epurePourTous`). */
export function epurePermisReserve() {
    try {
        if (globalThis.localStorage && globalThis.localStorage.getItem("mc_vue_joueur") === "oui") return false;
        if (hoteLocal()) return true;
        return !!globalThis.sessionStorage && globalThis.sessionStorage.getItem(CLE_EPURE_PERMIS) === "oui";
    } catch (e) { return false; }
}

/** La valeur montrée : l'épuré devient sobre pour qui n'y a pas droit. */
export function valeurPermise(valeur) {
    const v = normaliser(valeur);
    return v === EPURE && !epurePermis() ? SOBRE : v;
}

let verification = null;
/** Demande une fois au serveur si l'épuré est permis, et retient la réponse. */
export function verifierEpurePermis() {
    verification = verification || (async () => {
        if (hoteLocal() || !epurePermisPossible()) return epurePermis();
        let ok = false;
        try {
            const r = await fetch("/get_site_admin", { cache: "no-store" });
            const d = r.ok ? await r.json() : null;
            ok = !!(d && d.url);
        } catch (e) { ok = false; }
        try { globalThis.sessionStorage.setItem(CLE_EPURE_PERMIS, ok ? "oui" : "non"); } catch (e) { /* stockage indisponible */ }
        return ok;
    })();
    return verification;
}

function epurePermisPossible() {
    try { return !(globalThis.localStorage && globalThis.localStorage.getItem("mc_vue_joueur") === "oui"); }
    catch (e) { return true; }
}

/** Pose ces attributs sur un élément (<html>). */
export function poserAttributs(racine, valeur) {
    const a = attributsDe(valeurPermise(valeur));
    racine.dataset.affichage = a.affichage;
    if (a.epure) racine.dataset.epure = "oui"; else delete racine.dataset.epure;
}

/**
 * Réconcilie le navigateur avec la réponse de `/get_preferences`, sur le même
 * contrat que les arts de héros (arts-heros-choix.js, `reconcilier`).
 *
 * Rend `null` quand le serveur n'est pas la référence (invité, moteur local).
 * Sinon `{ affichage, pousser }` : la valeur à garder dans le navigateur, et
 * les changements à envoyer au compte (vide si rien).
 *  - le compte a déjà un fichier : il fait foi ;
 *  - sinon on y verse le choix du navigateur, s'il diffère du défaut.
 */
export function reconcilier(local, reponse) {
    if (!reponse || !reponse.compte) return null;
    const ici = normaliser(local);
    if (!reponse.existe) {
        return { affichage: ici, pousser: ici !== PAR_DEFAUT ? { affichage: ici } : {} };
    }
    const prefs = reponse.preferences || {};
    return { affichage: normaliser(prefs.affichage), pousser: {} };
}

/**
 * Faut-il proposer la fenêtre « Choisis ton affichage » ? (04/10/2026)
 *
 * Choix de l'utilisateur : tout joueur qui n'a JAMAIS choisi la voit une fois,
 * nouveau comme ancien. A déjà choisi :
 *  - le navigateur qui a une valeur rangée (`local`, brute, avant
 *    normalisation : `null` veut dire « jamais touché ») ;
 *  - le compte dont le fichier de préférences porte déjà `affichage`.
 */
export function doitProposerLeChoix(local, reponse) {
    // Tout le monde commence en Normal (18/10/2026) : rien à proposer d'office. Le choix reste dans « Options »
    // et le bouton de l'en-tête.
    if (epurePermis()) return false;
    if (local === NORMAL || local === SOBRE || local === EPURE) return false;
    const prefs = reponse && reponse.compte && reponse.existe ? (reponse.preferences || {}) : {};
    return !Object.prototype.hasOwnProperty.call(prefs, "affichage");
}
