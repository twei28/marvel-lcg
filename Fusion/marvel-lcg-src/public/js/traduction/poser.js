// poser.js : la traduction posée sur un scan anglais, pour les pages hors
// plateau (deckbuilder, galerie). Même rendu que TraductionPosee.tsx du plateau,
// avec les modules transpilés de ce dossier (generer-traduction-public.mjs).
"use strict";

import { detecterZoneTexte, formeDuCache, ligneDeTraits, texteEnHtml } from "./traduction-posee.js";
import { TRAITS_FR } from "./traits-fr.js";
import { TEXTES_FR } from "./textes-fr.js";
import { CODES_SCAN_FR } from "./scans-fr-liste.js";
import { langueActuelle } from "/public/js/prepare/langue.js";
import { texteFr, CARTES_FR } from "/public/js/prepare/cartes-fr.js";

const LARGEUR = 300;
const HAUTEUR = 420;
const SCANS_FR_MAISON = new Set(["tough", "stunned", "confused"]);
const zones = new Map();
let fanmade = null;
let complets = null;
let zonesArts = null;
const SERIES_ALTERNATIVES = /_(cb|rog|rog2|m3t)$/;

function feuilleDeStyle() {
    if (document.getElementById("traduction-posee-css")) return;
    const lien = document.createElement("link");
    lien.id = "traduction-posee-css";
    lien.rel = "stylesheet";
    lien.href = "/public/js/traduction/traduction-posee.css";
    document.head.append(lien);
}

/** Le texte français à poser, ou null : seulement en français, seulement sur un
 *  scan resté anglais faute de scan français, et seulement s'il existe.
 *  `scanAnglais` : l'image montrée est anglaise même si un scan français existe
 *  (art alternatif, scan HD de la fenêtre des variantes) ; le texte officiel
 *  complet (textes-fr-complets.js, ~1 Mo) est alors chargé à la demande. */
export async function texteAPoser(code, { scanAnglais = false } = {}) {
    if (!code || langueActuelle() !== "fr") return null;
    if (!scanAnglais && (CODES_SCAN_FR.has(code) || SCANS_FR_MAISON.has(code))) return null;
    if (TEXTES_FR[code]) return TEXTES_FR[code];
    if (CARTES_FR[code]) return texteFr({ card_id: code });
    if (!fanmade) fanmade = import("./textes-fr-fanmade.js").then((m) => m.TEXTES_FR_FANMADE);
    const maison = (await fanmade)[code];
    if (maison || !scanAnglais) return maison || null;
    if (!complets) complets = import("./textes-fr-complets.js").then((m) => m.TEXTES_FR_COMPLETS);
    return (await complets)[code] || null;
}

/** « /hd/01001a_cb?x » -> « 01001a_cb » */
function codeImage(url) {
    return decodeURIComponent(String(url).split("?")[0].split("/").pop() || "").replace(/\.[a-z]+$/i, "");
}

function zoneDuScan(url) {
    if (zones.has(url)) return zones.get(url);
    // Les arts alternatifs de héros ont leur zone relevée image par image
    // (zones-arts-alternatifs.js, même table que le plateau).
    const image = codeImage(url);
    if (SERIES_ALTERNATIVES.test(image)) {
        if (!zonesArts) zonesArts = import("./zones-arts-alternatifs.js").then((m) => m.ZONES_ARTS_ALTERNATIFS);
        const promesse = zonesArts.then((table) => table[image] || null).catch(() => null);
        zones.set(url, promesse);
        return promesse;
    }
    const promesse = new Promise((resoudre) => {
        const image = new Image();
        image.onload = () => {
            try {
                if (image.naturalWidth > image.naturalHeight) return resoudre(null);
                const toile = document.createElement("canvas");
                toile.width = LARGEUR;
                toile.height = HAUTEUR;
                const contexte = toile.getContext("2d", { willReadFrequently: true });
                contexte.drawImage(image, 0, 0, LARGEUR, HAUTEUR);
                resoudre(detecterZoneTexte(contexte.getImageData(0, 0, LARGEUR, HAUTEUR).data, LARGEUR, HAUTEUR));
            } catch (e) {
                resoudre(null);
            }
        };
        image.onerror = () => resoudre(null);
        image.src = url;
    });
    zones.set(url, promesse);
    return promesse;
}

/** Réduit la police jusqu'à ce que le texte tienne, sans passer sous un plancher. */
function ajuster(element) {
    const carte = element.parentElement ? element.parentElement.clientWidth : 300;
    let taille = carte * 0.05;
    const plancher = carte * 0.026;
    element.style.fontSize = `${taille}px`;
    while (element.scrollHeight > element.clientHeight + 1 && taille > plancher) {
        taille -= carte * 0.0015;
        element.style.fontSize = `${taille}px`;
    }
}

/**
 * Pose la traduction sur `cadre` (un conteneur en position relative, exactement
 * de la taille de l'image `url`). Ne fait rien si la carte n'a rien à poser ou
 * si sa zone de texte n'est pas reconnue. Renvoie true si la pose a eu lieu.
 */
export async function poserTraduction(cadre, url, code, traits = [], options = {}) {
    const texte = await texteAPoser(code, options);
    if (!texte) return false;
    const zone = await zoneDuScan(url);
    if (!zone || !cadre.isConnected) return false;
    feuilleDeStyle();
    const forme = formeDuCache(zone);
    const boite = document.createElement("div");
    boite.className = "traduction-posee";
    boite.lang = "fr";
    Object.assign(boite.style, {
        left: `${zone.x0 * 100}%`,
        top: `${zone.y0 * 100}%`,
        width: `${(zone.x1 - zone.x0) * 100}%`,
        height: `${(zone.y1 - zone.y0) * 100}%`,
        background: `rgb(${zone.fond.join(",")})`,
        clipPath: forme.clipPath,
    });
    for (const [cote, encoche] of [["gauche", forme.gauche], ["droite", forme.droite]]) {
        if (!encoche) continue;
        const reserve = document.createElement("span");
        reserve.className = `tp-encoche tp-encoche-${cote}`;
        reserve.style.height = `${encoche.hauteur}%`;
        reserve.style.width = `${encoche.largeur}%`;
        boite.append(reserve);
    }
    const ligne = ligneDeTraits(traits, TRAITS_FR);
    if (ligne) {
        const tete = document.createElement("div");
        tete.className = "tp-traits";
        tete.textContent = ligne;
        boite.append(tete);
    }
    const corps = document.createElement("div");
    corps.innerHTML = texteEnHtml(texte);
    boite.append(corps);
    cadre.append(boite);
    ajuster(boite);
    if (document.fonts) document.fonts.ready.then(() => ajuster(boite));
    return true;
}
