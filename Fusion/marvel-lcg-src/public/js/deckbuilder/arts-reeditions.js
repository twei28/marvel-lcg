// Rééditions de cartes joueur imprimées avec une AUTRE illustration.
// Relevé visuel du 09/10/2026 sur assets/pics : les autres rééditions
// (`full_link` de data/cards.json) reprennent l'image d'origine et ne sont
// pas listées. Les ressources 01088-01090 ont leur propre sélecteur.
// Module pur, testé par tools/tests-lanceur/arts-reeditions.test.mjs.
"use strict";

/** Carte d'origine -> rééditions à illustration différente. */
export const REEDITIONS_ILLUSTREES = {
    "01055": ["45047"], // The Power of Aggression
    "01062": ["47017"], // The Power of Justice
    "01072": ["45019"], // The Power of Leadership
    "01079": ["48019"], // The Power of Protection
    "04016": ["45013"], // Team Training
    "05023": ["36026"], // Endurance
    "05033": ["34024"], // Down Time
    "06015": ["35019"], // Mean Swing
    "09020": ["38013"], // Unflappable
    "10015": ["32046"], // Toe to Toe
    "12024": ["46021"], // Team-Building Exercise
    "12030": ["43017", "ma026"], // Moment of Triumph
    "13033": ["32016"], // Perseverance
    "15014": ["34019"], // Swift Retribution
    "15030": ["32015"], // Bait and Switch
    "15031": ["46022"], // Recuperation
    "16024": ["49023"], // Deft Focus
    "18012": ["45046"], // Clobber
    "18020": ["37020"], // Hit and Run
    "21022": ["32051"], // Ready to Rumble
    "23035": ["40030"], // Sidearm
    "30014": ["40052"], // Even the Odds
    "30019": ["40055"], // Overwatch
    "32014": ["60051"], // Powerful Punch
    "38016": ["52015"], // Not Today!
};

const RACINE = new Map();
for (const [origine, reeditions] of Object.entries(REEDITIONS_ILLUSTREES)) {
    RACINE.set(origine, origine);
    for (const r of reeditions) RACINE.set(r, origine);
}

/** Toutes les versions d'une carte, origine en tête ; [] si elle n'a qu'un art. */
export function versionsDe(id) {
    const origine = RACINE.get(String(id));
    return origine ? [origine, ...REEDITIONS_ILLUSTREES[origine]] : [];
}

/** La version de cette carte déjà présente dans le deck, ou null. */
export function versionDansLeDeck(id, choisies) {
    return versionsDe(id).find((v) => (choisies.get(v) || 0) > 0) || null;
}

/** Passe toutes les copies du deck sur la version `vers` (même carte, autre art). */
export function changerVersion(choisies, vers) {
    let total = 0;
    for (const v of versionsDe(vers)) {
        total += choisies.get(v) || 0;
        choisies.delete(v);
    }
    if (total) choisies.set(vers, total);
}
