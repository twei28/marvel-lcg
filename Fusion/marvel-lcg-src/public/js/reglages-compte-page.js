// reglages-compte-page.js : les reglages du joueur, gardes sur son COMPTE, pour les pages HTML du jeu (14/11/2026).
//
// Jumeau de ui-app/src/board/reglages-compte.ts (le plateau). Meme contrat, cle par cle :
//   - le compte a la cle : il fait foi, le navigateur prend sa valeur ;
//   - le compte ne l'a pas, le navigateur si : le navigateur la VERSE au compte (c'est ainsi que les reglages
//     d'avant cette mise a jour sont recuperes, a la premiere visite) ;
//   - invite, hors site ou cadre de spectateur : le navigateur reste seul.
// Ensuite tout changement fait dans le navigateur part vers le compte (releve toutes les 4 s, et au depart de la page).
//
// ⚠ LES TROIS LISTES SE TIENNENT : REGLAGES_CLES (server_get.py), REGLAGES_DU_COMPTE (reglages-compte.ts) et
// celle-ci. ui-app/src/board/reglages-compte.test.ts les compare.
// ⚠ HORS COMPTE, EXPRES : l'image de fond (trop lourde), l'historique de la partie (sessionStorage), le rapport en
// attente, les pointeurs `mc-campagne-partie` et `mc-puzzle-courant`, les marqueurs de migration, la vue joueur de
// l'admin. Campagnes, hauts faits, parties, Legacy et decks vivent deja sur le serveur.
//
// Charge par teinte-page.js, donc par toutes les pages. LA LANGUE : une page deja dessinee ne se retraduit pas, elle se
// recharge UNE fois (garde en sessionStorage) quand la langue du compte n'est pas celle du navigateur.
"use strict";

import { cookieLangue } from "/public/js/prepare/langue-resolution.js";

export const REGLAGES_DU_COMPTE = [
    "marvel-board-action-mode", "marvel-board-animations", "marvel-board-annuler-explique",
    "marvel-board-auto-cible", "marvel-board-avance-auto", "marvel-board-curseurs",
    "marvel-board-delai-pas-a-pas", "marvel-board-dos-cartes", "marvel-board-facon-de-jouer",
    "marvel-board-fin-tour-auto", "marvel-board-meteo", "marvel-board-mode-phase-mechant",
    "marvel-board-musique", "marvel-board-paiement-auto", "marvel-board-phase-auto", "marvel-board-phase-rapide",
    "marvel-board-piste-phases", "marvel-board-revelation", "marvel-board-sauvegarde-auto",
    "marvel-board-scans-fr", "marvel-board-sons", "marvel-board-tutoriel", "marvel-board-validation-courte",
    "marvel-board-volume-musique", "marvel-board-volume-sons", "marvel-encoche-gauche", "marvel-tel-aide-debut",
    "marvel-tel-colonnes-zones", "marvel-tel-plateau", "marvel-tel-plateau-choisi",
    "marvel-tel-plateau-memorise", "marvel-tel-taille-texte", "marvel-tel-verrou-portrait",
    "marvel-tel-vibrations", "marvel-tel-visite-piles", "mc_aide_bulle_table", "mc_ameliorations_chevauchement",
    "mc_ameliorations_cote", "mc_apercu_zoom", "mc_barre_avantage", "mc_card_art_v1", "mc_etiquettes_table",
    "mc_noms_zones_v1", "mc_phase_bis", "mc_phase_presentation", "mc_piles_inversees", "mc_resource_art_v1",
    "mc_traits_pastilles",
    "marvel-langue",
    "marvel-langue-choisie", "marvel-board-succes", "marvel-board-marvelcdb", "marvel-board-design-essai",
    "marvel-board-ambiance-demande", "marvel-boite-phase-mechant", "marvel-tchat-position",
    "marvel-tchat-taille", "marvel-tsm-bandeau-place", "marvel-tchat-pseudo-play", "marvel-tchat-langues",
    "marvel-tchat-fermees", "mode-plateau", "marvel-jeu-au-doigt", "mc-puzzles-crees", "mc-puzzle-pseudo",
    "mc_prepare_prefs_v1", "mc_ext_groupe_v1", "mc_roue_fanmade", "mc_phase_choix_vu", "mc_phase_mode_vu_v1",
    "mc_card_art_noask_v1", "marvel-legacy-explique", "marvelcdb_favoris", "mc-deckbuilder-filtres-replies",
    "mc-deckbuilder-drafts", "mc_sandbox_garnir", "mc-campagne-brouillon",
];
export const LONGUEUR_MAX = 2000;
export const LONGUEUR_PAR_CLE = {
    "mc-deckbuilder-drafts": 65536,
    "mc-campagne-brouillon": 32768,
    "mc-puzzles-crees": 16384,
    "mc_prepare_prefs_v1": 16384,
    "marvelcdb_favoris": 16384,
};
const CHANGEMENTS_PAR_APPEL = 60;   // le serveur en refuse plus de 100
const RELEVE_MS = 4000;
const GARDE_RECHARGE = "mc_reglages_langue_rechargee";

export function reglageValide(cle, valeur) {
    return typeof valeur === "string" && valeur.length <= (LONGUEUR_PAR_CLE[cle] || LONGUEUR_MAX) && !/[\x00-\x1f\x7f]/.test(valeur);
}

export function lireReglages(stockage = window.localStorage) {
    const reglages = {};
    try {
        for (const cle of REGLAGES_DU_COMPTE) {
            const valeur = stockage.getItem(cle);
            if (reglageValide(cle, valeur)) reglages[cle] = valeur;
        }
    } catch (e) { /* stockage refuse : rien a garder */ }
    return reglages;
}

/** Ce que le navigateur prend du compte, et ce qu'il lui verse (les cles que le compte n'a pas). */
export function rapprocher(compte, navigateur) {
    const versNavigateur = {};
    const versCompte = {};
    for (const cle of REGLAGES_DU_COMPTE) {
        const duCompte = compte[cle];
        if (reglageValide(cle, duCompte)) {
            if (navigateur[cle] !== duCompte) versNavigateur[cle] = duCompte;
        } else if (cle in navigateur) {
            versCompte[cle] = navigateur[cle];
        }
    }
    return { versNavigateur, versCompte };
}

/** Ce qui a change entre deux releves (`null` = reglage efface). */
export function changementsDepuis(avant, apres) {
    const changements = {};
    for (const cle of REGLAGES_DU_COMPTE) {
        if (avant[cle] === apres[cle]) continue;
        changements[cle] = cle in apres ? apres[cle] : null;
    }
    return changements;
}

function envoyer(changements, enPartant = false) {
    const cles = Object.keys(changements);
    for (let i = 0; i < cles.length; i += CHANGEMENTS_PAR_APPEL) {
        const lot = {};
        for (const cle of cles.slice(i, i + CHANGEMENTS_PAR_APPEL)) lot[cle] = changements[cle];
        fetch("/save_preferences", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ changements: lot }),
            keepalive: enPartant,
        }).catch(() => {});
    }
}

function poserDansLeNavigateur(reglages) {
    for (const [cle, valeur] of Object.entries(reglages)) {
        try {
            const ancienne = window.localStorage.getItem(cle);
            window.localStorage.setItem(cle, valeur);
            window.dispatchEvent(new StorageEvent("storage", { key: cle, oldValue: ancienne, newValue: valeur }));
        } catch (e) { /* stockage refuse : le reglage du compte ne vaut que pour cette visite */ }
    }
}

let suivi = false;
function suivre() {
    if (suivi) return;
    suivi = true;
    let releve = lireReglages();
    const relever = (enPartant = false) => {
        const maintenant = lireReglages();
        const changements = changementsDepuis(releve, maintenant);
        releve = maintenant;
        if (Object.keys(changements).length) envoyer(changements, enPartant);
    };
    window.setInterval(relever, RELEVE_MS);
    window.addEventListener("pagehide", () => relever(true));
}

/** La langue du compte vient d'etre posee : le cookie du site et la narration du moteur la suivent, la page se recharge une fois. */
function appliquerLangueDuCompte() {
    const langue = window.localStorage.getItem("marvel-langue") === "en" ? "en" : "fr";
    try { document.cookie = cookieLangue(langue, location.host, location.protocol); } catch (e) { /* cookies bloques */ }
    fetch("/set_language?" + langue).catch(() => {});
    try {
        if (window.sessionStorage.getItem(GARDE_RECHARGE) === langue) return;
        window.sessionStorage.setItem(GARDE_RECHARGE, langue);
    } catch (e) { return; }
    location.reload();
}

export async function chargerReglagesDuCompte() {
    if (new URLSearchParams(window.location.search).has("cadre")) return;
    try {
        const reponse = await fetch("/get_preferences", { cache: "no-store" });
        if (!reponse.ok) return;
        const corps = await reponse.json();
        if (!corps || !corps.compte) return;
        const { versNavigateur, versCompte } = rapprocher(corps.preferences || {}, lireReglages());
        poserDansLeNavigateur(versNavigateur);
        if (Object.keys(versCompte).length) envoyer(versCompte);
        suivre();
        if ("marvel-langue" in versNavigateur) appliquerLangueDuCompte();
    } catch (e) { /* hors ligne, hors site : le navigateur reste la reference */ }
}

// Une seule fois par page : teinte-page.js l'importe sur toutes les pages, et rien d'autre ne doit le relancer.
if (!window.__reglagesCompteLance) {
    window.__reglagesCompteLance = true;
    chargerReglagesDuCompte();
}
