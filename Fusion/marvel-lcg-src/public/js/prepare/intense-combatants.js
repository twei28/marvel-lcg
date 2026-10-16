// intense-combatants.js : l'environnement OPTIONNEL te201 Intense Combatants (TMNT).
//
// « TMNT Standard and Expert only. (This is an optional environment for those
//   wanting additional hijinx.) Permanent. Setup. »
//
// Décision de l'utilisateur (16/10/2026) : une case de la préparation, DÉCOCHÉE
// par défaut, proposée seulement quand le scénario joue le set TMNT Standard ou
// TMNT Expert. Cochée, le lanceur pose la règle `tmnt_intense_combatants` dans
// `rules`, le même canal que Skirmish ou Héroïque ; le moteur met alors te201 en
// jeu à l'étape 11 de la mise en place (src/game/world/world.py,
// `CartesSetupOptionnelles`), et ignore la règle hors TMNT.
"use strict";

export const REGLE_INTENSE = "tmnt_intense_combatants";
export const CARTE_INTENSE = "te201";

/** Le scénario (liste de ses sets de rencontre) joue-t-il TMNT Standard ou Expert ? */
export function proposerIntense(sets) {
    return (sets || []).some((s) => /^tmnt_(standard|expert)/.test(String(s)));
}

/** La règle à ajouter au descripteur : seulement case cochée ET sets TMNT. */
export function reglesIntense(coche, sets) {
    return coche === true && proposerIntense(sets) ? [REGLE_INTENSE] : [];
}

/** Le texte de la carte, sans balises, sur une ligne (info-bulle de la case). */
export function texteSansBalises(texte) {
    return String(texte || "").replace(/<[^>]*>/g, "").replace(/\s*\n\s*/g, " ").trim();
}

let texteFr = null;
/** Le texte FR de te201 (textes-fr-fanmade, seule traduction de la carte). */
export function chargerTexteFr() {
    if (!texteFr) {
        texteFr = import("/public/js/traduction/textes-fr-fanmade.js")
            .then((m) => texteSansBalises(m.TEXTES_FR_FANMADE[CARTE_INTENSE]))
            .catch(() => "");
    }
    return texteFr;
}
