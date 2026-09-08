// nouveautes.js — le journal des nouveautés, tel que les JOUEURS le lisent.
//
// Affiché sur l'accueil de l'assistant, sous les tuiles de mode : les trois
// dernières lignes visibles, le reste sous « Tout voir ».
//
// ⚠ ÉCRIT POUR UN JOUEUR, JAMAIS POUR UN DÉVELOPPEUR. « Blade rejoint le
// roster », pas « feat(blade): pack fan-made 17 cartes set 165 ». Personne ne
// lit un message de commit pour savoir ce qu'il peut jouer ce soir.
//
// ⚠ L'ANGLAIS N'EST PAS FACULTATIF (décision du 08/09/2026). L'assistant est
// bilingue : une entrée sans `en` afficherait du français à un anglophone, au
// milieu d'un écran traduit. Le filet `ui-check/tests/nouveautes.spec.ts`
// refuse une entrée incomplète.
//
// ⚠ PAS DE PASTILLE « NOUVEAU » (décision du 08/09/2026) : la date suffit, et
// rien n'est retenu du passage de chacun.
//
// Une entrée :
//   date  : "AAAA-MM-JJ". Sert au tri ET à l'affichage.
//   genre : une clé de GENRES ci-dessous. Change l'étiquette de couleur.
//   fr    : une phrase, deux au maximum. Pas de point-virgule, pas de jargon.
//   en    : la même chose en anglais.
//
// L'ordre du tableau n'a pas d'importance : l'accueil trie par date, la plus
// récente en tête. Ajouter une ligne EN TÊTE reste la façon la plus lisible
// de tenir le fichier.
"use strict";

/** Les familles de nouveautés, et leur étiquette dans les deux langues.
 *  Les quatre ont été retenues le 08/09/2026 : le joueur veut savoir ce qu'il
 *  peut jouer, ce qui change dans le jeu, ce qui a été réparé, et ce qui se
 *  passe derrière le rideau. */
export const GENRES = {
    heros:      { fr: "Roster",     en: "Roster" },
    jeu:        { fr: "Jeu",        en: "Play" },
    correction: { fr: "Correction", en: "Fix" },
    coulisses:  { fr: "Coulisses",  en: "Behind the scenes" },
};

export const NOUVEAUTES = [
    {
        date: "2026-09-08",
        genre: "coulisses",
        fr: "Un écran de suivi des parties, pour voir d'un coup d'œil qui joue, à quoi, et comment ça s'est terminé.",
        en: "A game tracker screen, to see at a glance who is playing, against whom, and how it ended.",
    },
    {
        date: "2026-09-07",
        genre: "heros",
        fr: "Ares et Blade rejoignent le roster fan-made, chacun avec ses cartes signature et son set némésis.",
        en: "Ares and Blade join the fan-made roster, each with their signature cards and nemesis set.",
    },
    {
        date: "2026-09-07",
        genre: "jeu",
        fr: "Le plateau du téléphone montre de vraies cartes en deux rangées, en plein écran et en paysage.",
        en: "The phone board now shows real cards in two rows, full screen and in landscape.",
    },
    {
        date: "2026-09-07",
        genre: "jeu",
        fr: "La phase du méchant se déroule comme une case de bande dessinée : le jeton tombe, les cartes se retournent.",
        en: "The villain phase plays out like a comic panel: the token drops, the cards flip over.",
    },
    {
        date: "2026-09-07",
        genre: "jeu",
        fr: "Le deck-builder filtre par ressource et par mot-clé, avec les icônes du jeu.",
        en: "The deck builder filters by resource and by keyword, with the game icons.",
    },
    {
        date: "2026-09-07",
        genre: "jeu",
        fr: "Les textes de cartes affichent les ressources avec les icônes du jeu, au lieu de les nommer.",
        en: "Card texts show resources with the game icons instead of spelling them out.",
    },
    {
        date: "2026-09-07",
        genre: "jeu",
        fr: "L'assistant et le plateau prennent les couleurs des Vengeurs, avec la police des comics.",
        en: "The wizard and the board take on the Avengers colours, with the comics typeface.",
    },
    {
        date: "2026-09-07",
        genre: "correction",
        fr: "« Manigance sur », le verbe des règles françaises, remplace « complote contre ».",
        en: "The French rules wording for scheming replaced an invented phrase.",
    },
];

/** Les nouveautés de la plus récente à la plus ancienne.
 *
 *  ⚠ ON TRIE SUR LA CHAÎNE, ET C'EST VOULU : « AAAA-MM-JJ » se compare
 *  alphabétiquement dans le bon ordre, sans passer par `Date` et sans risquer
 *  le décalage de fuseau qui fait reculer une date d'un jour. */
export function nouveautesTriees() {
    return NOUVEAUTES
        .filter((n) => n && n.date && n.fr && n.en && GENRES[n.genre])
        .slice()
        .sort((a, b) => (a.date < b.date ? 1 : a.date > b.date ? -1 : 0));
}
