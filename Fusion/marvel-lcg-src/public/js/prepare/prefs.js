// prefs.js — préférences locales (favoris, récents, dernier deck) via localStorage.
"use strict";
const KEY = "mc_prepare_prefs_v1";

/**
 * Collection d'arts des ressources doubles, PAR HÉROS. Clé DÉDIÉE (et non le
 * blob de préférences ci-dessus) parce qu'elle est lue par un autre frontend :
 * le plateau (ui-app) s'en sert pour choisir l'image des cartes 01088/01089/01090.
 * Valeurs : "standard" (défaut), "random", ou un code de collection ("th", "sm"…).
 */
const KEY_RES_ART = "mc_resource_art_v1";
const KEY_HERO_ART = "mc_hero_art_v1";

function read() {
    try { return JSON.parse(localStorage.getItem(KEY)) || {}; }
    catch (e) { return {}; }
}
function write(o) {
    try { localStorage.setItem(KEY, JSON.stringify(o)); } catch (e) {}
}
function readResArt() {
    try { return JSON.parse(localStorage.getItem(KEY_RES_ART)) || {}; }
    catch (e) { return {}; }
}
function readHeroArt() {
    try { return JSON.parse(localStorage.getItem(KEY_HERO_ART)) || {}; }
    catch (e) { return {}; }
}

export const prefs = {
    /** Collection d'arts des ressources doubles pour ce héros ("standard" par défaut). */
    /** Art alternatif de la carte de héros ("standard" par défaut). */
    heroArt(heroCardId) {
        return readHeroArt()[String(heroCardId || "").split(",")[0].replace(/[a-z]$/, "")] || "standard";
    },
    setHeroArt(heroCardId, code) {
        const o = readHeroArt();
        const cle = String(heroCardId || "").split(",")[0].replace(/[a-z]$/, "");
        if (!cle) return;
        if (code === "standard") delete o[cle]; else o[cle] = code;
        try { localStorage.setItem(KEY_HERO_ART, JSON.stringify(o)); } catch (e) { /* stockage indisponible */ }
    },
    resourceArt(heroCardId, defaut) {
        // Rien d'enregistré : on prend le défaut proposé (la collection au nom
        // du héros), et « standard » seulement à défaut de défaut.
        const enregistre = readResArt()[String(heroCardId || "").split(",")[0].replace(/[a-z]$/, "")];
        return enregistre || defaut || "standard";
    },
    setResourceArt(heroCardId, code) {
        const o = readResArt();
        const cle = String(heroCardId || "").split(",")[0].replace(/[a-z]$/, "");
        if (!cle) return;
        // « Standard » s'ENREGISTRE désormais au lieu de s'effacer : sans cela,
        // un joueur qui le remet volontairement retrouverait la collection du
        // héros au chargement suivant, sans comprendre pourquoi.
        o[cle] = code;
        try { localStorage.setItem(KEY_RES_ART, JSON.stringify(o)); } catch (e) {}
    },

    favHeroes()      { return read().favHeroes || []; },
    isFavHero(id)    { return this.favHeroes().includes(id); },
    toggleFavHero(id) {
        const o = read(); const s = new Set(o.favHeroes || []);
        s.has(id) ? s.delete(id) : s.add(id);
        o.favHeroes = [...s]; write(o); return s.has(id);
    },
    lastDeckFor(heroId) { return (read().lastDeck || {})[heroId] || null; },
    setLastDeck(heroId, deckId) {
        const o = read(); o.lastDeck = o.lastDeck || {}; o.lastDeck[heroId] = deckId; write(o);
    },
    lastScenario()   { return read().lastScenario || null; },
    setLastScenario(id) { const o = read(); o.lastScenario = id; write(o); },

    // Decks importés/sauvegardés localement (marvelcdb, etc.)
    savedDecks()     { return read().savedDecks || []; },
    savedDecksForHero(heroCardId) {
        const id = String(heroCardId || "").split(",")[0];
        return this.savedDecks().filter((d) => d && d.hero && String(d.hero[0] || "").split(",")[0] === id);
    },
    saveDeck(deck) {
        const o = read(); o.savedDecks = o.savedDecks || [];
        // évite les doublons exacts (même nom + même hero)
        const key = (deck.name || "") + "|" + (deck.hero && deck.hero[0]);
        o.savedDecks = o.savedDecks.filter((d) => ((d.name || "") + "|" + (d.hero && d.hero[0])) !== key);
        o.savedDecks.push(deck); write(o);
    },

    // La progression et le journal de campagne ont vécu ici quand la campagne était
    // un mode du wizard. Ils sont partis avec lui le 12/08/2026 : la campagne a son
    // écran (`/campagne.html`), et son état est écrit SUR LE SERVEUR
    // (`/save_campagne`), pas dans le stockage local d'un navigateur. Les anciennes
    // entrées `campaignProgress` et `campaignLog` d'un stockage local existant sont
    // simplement ignorées.
};
