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

// ⚠ RIEN SUR LE PLATEAU DU TELEPHONE (retire le 08/09/2026, sur demande).
// Le plateau paysage a ete livre puis abandonne des le premier essai sur un
// vrai telephone : la carte est coupee et les menus ne sont pas faits pour le
// doigt. La refonte en portrait attend dans
// `.planning/todos/2026-09-07-parcours-solo-mobile-portrait.md`. On n'annonce
// pas aux joueurs une facon de jouer qu'on ne leur conseille pas encore.
export const NOUVEAUTES = [
    {
        date: "2026-09-11",
        genre: "jeu",
        fr: "SP//dr est de nouveau jouable. Depuis le 1er septembre, toute partie avec Peni Parker s'arrêtait dès la mise en place : son héros étant une carte à part, le jeu ne trouvait pas de face héros sur sa carte.",
        en: "SP//dr is playable again. Since September 1st, any game with Peni Parker died during setup: her hero being a separate card, the game could not find a hero face on her card.",
    },
    {
        date: "2026-09-11",
        genre: "jeu",
        fr: "Une Crise en jeu empêche désormais de cibler le complot principal avec un contre, comme un sbire Garde protège le méchant. Le complot porte un bandeau « Crise » et l'aperçu nomme la manigance responsable. Avant, la carte partait sans effet, sans un mot.",
        en: "A Crisis in play now prevents targeting the main scheme with a thwart, just as a Guard minion protects the villain. The main scheme shows a “Crisis” badge and the preview names the side scheme responsible. Cards used to fizzle without a word.",
    },
    {
        date: "2026-09-11",
        genre: "correction",
        fr: "Wolverine, Storm, Cyclops, Phoenix, Gambit, Rogue, Colossus, Shadowcat, Groot et Rocket montraient leur alter ego en grand à la sélection du héros. C'est réparé.",
        en: "Wolverine, Storm, Cyclops, Phoenix, Gambit, Rogue, Colossus, Shadowcat, Groot and Rocket showed their alter ego on the big card at hero selection. Fixed.",
    },
    {
        date: "2026-09-11",
        genre: "correction",
        fr: "La raison affichée sur une carte injouable disait l'inverse de la carte : « seulement en alter ego » pour une action de héros. C'est réparé.",
        en: "The reason shown on an unplayable card said the opposite of the card: “alter-ego only” for a hero action. Fixed.",
    },
    {
        date: "2026-09-10",
        genre: "jeu",
        fr: "Une carte grisée dit pourquoi au survol : forme de héros ou d'alter ego, ressources manquantes, aucune cible possible.",
        en: "A greyed-out card now says why on hover: hero or alter-ego form, missing resources, no legal target.",
    },
    {
        date: "2026-09-10",
        genre: "jeu",
        fr: "Les decks MarvelCDB de chaque héros peuvent être triés par popularité, avec leur rang dans le classement du site.",
        en: "Each hero's MarvelCDB decks can be sorted by popularity, with their rank in the site's ranking.",
    },
    {
        date: "2026-09-09",
        genre: "jeu",
        fr: "Un lien MarvelCDB d'un autre héros ne fait plus changer de héros : le tien reste en place et récupère les 25 cartes d'aspect du deck collé, si elles respectent ses règles de construction.",
        en: "A MarvelCDB link from another hero no longer switches heroes: yours stays, and picks up the 25 aspect cards of the pasted deck, provided they respect its deckbuilding rules.",
    },
    {
        date: "2026-09-08",
        genre: "jeu",
        fr: "On peut glisser une carte sur sa cible : le héros sur le méchant pour attaquer, sur une manigance pour contrer, un allié dans sa zone pour le jouer. Le clic marche toujours.",
        en: "Cards can be dragged onto their target: the hero onto the villain to attack, onto a scheme to thwart, an ally into its area to play it. Clicking still works.",
    },
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
