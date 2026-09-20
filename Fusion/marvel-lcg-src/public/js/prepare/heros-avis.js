// heros-avis.js — ce que la communauté pense de chaque héros, affiché sous la
// biographie dans la fiche du wizard (voir avisDuHeros dans app.js).
//
// ⚠ CE FICHIER PARLE DU JEU, pas du personnage. C'est exactement pour ça
// qu'il est SÉPARÉ de `heros-info.js`, dont l'en-tête promet l'inverse
// (« ces textes décrivent le PERSONNAGE, pas sa mécanique de jeu »).
// Ne pas fusionner les deux : ils n'ont ni la même source, ni la même durée
// de vie. Une biographie ne change jamais, un avis vieillit à chaque sortie.
//
// Indexé par le card_id de la FACE HÉROS, comme `heros-info.js`, et pour la
// même raison : deux héros peuvent porter le même nom.
//
// ⚠ RÉSERVÉ AUX HÉROS OFFICIELS. Un héros maison n'a pas de communauté qui
// l'a joué, donc pas d'avis à rapporter : lui en inventer un serait mentir.
// Un card_id absent n'affiche simplement aucun bloc.
//
// TROIS NOTES, ET ELLES NE SE DÉDUISENT PAS L'UNE DE L'AUTRE :
//   complexite : combien de décisions et d'interactions à tenir en tête.
//                C'est ce qui compte le plus pour un débutant.
//   puissance  : est-ce qu'on gagne avec.
//   plaisir    : est-ce que les gens l'aiment.
// Iron Man est le cas qui justifie la séparation : il est dans la boîte de
// base, donc un débutant le prend naturellement, et c'est l'un des plus
// exigeants du jeu. Aucune note unique ne dirait ça.
//
// `clivant: true` quand les avis se contredisent franchement. Une moyenne sur
// un héros que la moitié adore et l'autre déteste est un mensonge.
//
// ⚠ NE RIEN ÉCRIRE ICI QU'ON NE PUISSE SOURCER. Sur un héros récent ou peu
// joué, la matière manque : laisser le card_id absent vaut mieux qu'une note
// fabriquée. Le lecteur croira ce qui est écrit.
"use strict";

/** Quand ces avis ont été relevés. Affiché sur la fiche, parce qu'un
 *  classement de héros vieillit : un héros jugé faible à sa sortie remonte
 *  parfois beaucoup avec une nouvelle carte. */
export const AVIS_DATE = "septembre 2026";
export const AVIS_DATE_EN = "September 2026";

/** Le cadre du classement de puissance, affiché aussi, parce qu'une note de
 *  puissance sans son cadre est trompeuse : en solo le classement change. */
export const AVIS_CADRE = "à deux joueurs, avec les cartes de base";
export const AVIS_CADRE_EN = "two players, base cards only";

export const HEROS_AVIS = {
    // Spider-Man (Peter Parker) — boîte de base
    "01001a": {
        complexite: 1,
        puissance: 4,
        plaisir: 5,
        avis: "Le héros avec lequel presque tout le monde commence, et il tient très bien la route. Sa capacité se déclenche toute seule et pardonne les erreurs.",
        avisEn: "The hero almost everyone starts with, and he holds up very well. His ability triggers on its own and forgives mistakes.",
    },

    // Captain America
    "03001a": {
        complexite: 2,
        puissance: 4,
        plaisir: 4,
        avis: "Robuste, lisible, bon partout sans être extrême. Un deuxième héros idéal.",
        avisEn: "Sturdy, readable, good at everything without being extreme. An ideal second hero.",
    },

    // Docteur Strange
    "09001a": {
        complexite: 5,
        puissance: 5,
        plaisir: 5,
        avis: "Le plus dépaysant du jeu : il a son propre paquet d'invocations. Compte une ou deux parties pour le comprendre, ensuite c'est l'un des plus forts qui existent. À éviter en premier héros.",
        avisEn: "The most unusual hero in the game: he has his own invocation deck. Give yourself a game or two to get him, after which he is one of the strongest there is. Not a good first hero.",
    },

    // Iron Man — boîte de base
    "01029a": {
        complexite: 4,
        puissance: 3,
        plaisir: 3,
        piege: "Piège de la boîte de base : il a l'air d'un héros de départ, il n'en est pas un.",
        piegeEn: "Base box trap: he looks like a starter hero, he is not one.",
        avis: "Une seule carte en main tant qu'il n'a pas monté son armure, ce qui demande de la patience et de savoir quoi garder.",
        avisEn: "A single card in hand until his armour is assembled, which takes patience and knowing what to hold on to.",
    },

    // Hulk
    "10001a": {
        complexite: 2,
        puissance: 1,
        plaisir: 2,
        clivant: true,
        avis: "Il défausse sa main à chaque tour, donc impossible d'enchaîner des combos, et il ne sait quasiment pas gérer les complots : chaque partie est une course contre la montre. Beaucoup le considèrent comme le plus faible du jeu. D'autres aiment justement cette contrainte.",
        avisEn: "He discards his hand every turn, so combos are out of reach, and he can barely deal with schemes: every game becomes a race against the clock. Many consider him the weakest hero in the game. Others enjoy precisely that constraint.",
    },

    // Valkyrie
    "25001a": {
        complexite: 2,
        puissance: 1,
        plaisir: 3,
        avis: "Classée parmi les plus faibles. À noter : les critiques portent surtout sur le thème et le contenu du paquet, pas sur ses mécaniques, que les tests trouvent plutôt réussies.",
        avisEn: "Ranked among the weakest. Worth noting: the criticism is mostly about the theme and the contents of the pack, not about her mechanics, which reviewers find rather well made.",
    },
};

/** Le mot qui accompagne un chiffre, parce que « 4 / 5 » tout seul ne dit pas
 *  dans quel sens lire l'échelle. Index 0 inutilisé : les notes vont de 1 à 5. */
export const ECHELLES = {
    complexite: [null, "Très simple", "Simple", "Demande un peu d'habitude", "Exigeant", "Très exigeant"],
    puissance: [null, "Faible", "Modeste", "Correct", "Fort", "Très fort"],
    plaisir: [null, "Rejeté", "Peu apprécié", "Mitigé", "Apprécié", "Adoré"],
};
