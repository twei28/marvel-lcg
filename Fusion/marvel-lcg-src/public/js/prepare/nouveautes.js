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
        date: "2026-10-09",
        genre: "jeu",
        fr: "Les cartes restées en anglais faute de scan français montrent maintenant leur traduction directement sur la carte agrandie, à la place du texte anglais, dans la police des vraies cartes.",
        en: "Cards still shown in English (no French scan) now display their French translation right on the enlarged card, over the English text, in the real card font.",
    },
    {
        date: "2026-10-09",
        genre: "jeu",
        fr: "Éditeur de deck : la recherche trouve aussi les cartes par leur nom français, sans se soucier des accents. En anglais, un bouton « Arts » permet de choisir l'illustration des cartes rééditées avec un nouvel art.",
        en: "Deck builder: search now also finds cards by their French name, accents optional. In English, an « Arts » button lets you pick the artwork of cards reprinted with new art.",
    },
    {
        date: "2026-10-09",
        genre: "jeu",
        fr: "Nouvelle campagne fan-made Hunting Season : affronte Vermin, Scorpion, Lizard, Vulture puis Kraven, et dépense ton expérience au Lodge entre les scénarios. Mode expert et mode Hunter inclus.",
        en: "New fan-made campaign Hunting Season: face Vermin, Scorpion, Lizard, Vulture and then Kraven, and spend your experience at the Lodge between scenarios. Expert and Hunter modes included.",
    },
    {
        date: "2026-10-08",
        genre: "jeu",
        fr: "En relecture et en spectateur, un bouton Réglages affiche les réglages du joueur (lecture seule). Quand un choix n'a qu'une seule option possible, le journal l'indique.",
        en: "In replay and spectator mode, a Settings button shows the player's settings (read-only). When a choice has only one possible option, the log now says so.",
    },
    {
        date: "2026-10-08",
        genre: "jeu",
        fr: "Nouvelle tuile « Partie au hasard » : une roue tire tes héros et ton scénario dans toutes les boîtes, et chaque bandeau peut être relancé.",
        en: "New “Random game” tile: a wheel draws your heroes and your scenario from every box, and each reel can be spun again.",
    },
    {
        date: "2026-10-08",
        genre: "correction",
        fr: "Daredevil peut de nouveau jouer la carte du dessus de son deck Sens. Merci pour le signalement.",
        en: "Daredevil can play the top card of his Sense deck again. Thanks for the report.",
    },
    {
        date: "2026-10-08",
        genre: "correction",
        fr: "Luke Cage garde tous ses Tenaces quand il change de forme. Merci Aghenatak.",
        en: "Luke Cage keeps all his tough cards when he changes form. Thanks Aghenatak.",
    },
    {
        date: "2026-10-08",
        genre: "correction",
        fr: "Hellcat : son Action la met en jeu gratuitement quand ton identité est Defender, et on peut toujours la jouer normalement. Merci BL-Stark.",
        en: "Hellcat: her Action puts her into play for free when your identity is a Defender, and she can still be played normally. Thanks BL-Stark.",
    },
    {
        date: "2026-10-08",
        genre: "jeu",
        fr: "Le nombre de cartes d'une pile s'affiche maintenant en haut à droite.",
        en: "The number of cards in a pile now shows in the top right corner.",
    },
    {
        date: "2026-10-08",
        genre: "jeu",
        fr: "Revoir une partie montre maintenant exactement ce que tu voyais : les fenêtres de paiement et tes choix dedans, les cartes que tu agrandissais, tes menus. La barre de lecture se cache toute seule, Espace et les flèches la pilotent.",
        en: "Replaying a game now shows exactly what you saw: the payment windows and your choices in them, the cards you zoomed in on, your menus. The playback bar hides by itself, Space and the arrow keys control it.",
    },
    {
        date: "2026-10-08",
        genre: "jeu",
        fr: "Choisis un héros ou un scénario : 35 héros et 8 méchants ont maintenant leurs répliques.",
        en: "Pick a hero or a scenario: 35 heroes and 8 villains now have their voice lines.",
    },
    {
        date: "2026-10-08",
        genre: "jeu",
        fr: "Nouvel écran de défaite.",
        en: "New defeat screen.",
    },
    {
        date: "2026-10-08",
        genre: "correction",
        fr: "Ant-Man (Hank Pym) mis en jeu par Appel de détresse : la fenêtre pour payer son coût reste ouverte, et chaque ressource en trop lui donne bien un jeton pym. Merci Phocéa.",
        en: "Ant-Man (Hank Pym) put into play with Make the Call: the window to pay his cost now stays open, and each extra resource gives him a pym counter. Thanks Phocéa.",
    },
    {
        date: "2026-10-08",
        genre: "jeu",
        fr: "Choisis Wolverine dans le choix des héros.",
        en: "Pick Wolverine in the hero selection.",
    },
    {
        date: "2026-10-08",
        genre: "jeu",
        fr: "Tes 3 dernières parties terminées sont gardées : ouvre « Revoir » dans le menu pour les rejouer en un clic, ou les télécharger.",
        en: "Your last 3 finished games are kept: open “Replay” in the menu to watch them again in one click, or download them.",
    },
    {
        date: "2026-10-08",
        genre: "jeu",
        fr: "En mode Manuel, tout fonctionne maintenant comme sur OCTGN : Maj+clic pour cibler une carte, Maj+glisser pour tracer une flèche, le pavé numérique pour colorer une carte, Ctrl+clic pour en sélectionner plusieurs, Ctrl+I pour lire une carte. La carte boost se pose face cachée à côté du méchant.",
        en: "In Manual mode, everything now works like OCTGN: Shift+click to target a card, Shift+drag to draw an arrow, the numeric keypad to colour a card, Ctrl+click to select several, Ctrl+I to read a card. The boost card goes face down next to the villain.",
    },
    {
        date: "2026-10-08",
        genre: "jeu",
        fr: "Glisse un événement de ta main n'importe où sur la table pour le jouer, ou directement sur sa cible. Plus besoin de cliquer la carte puis « Jouer ».",
        en: "Drag an event from your hand anywhere on the table to play it, or straight onto its target. No more clicking the card and then “Play”.",
    },
    {
        date: "2026-10-08",
        genre: "correction",
        fr: "Plus de 800 cartes ont maintenant leur nom et leur texte en français, et 289 leur scan français, dont tout Peur de Rien, Jessica Jones et Luke Cage. Merci à mc4db pour les traductions.",
        en: "More than 800 cards now have their French name and text, and 289 their French scan, including all of Fear No Evil, Jessica Jones and Luke Cage. Thanks to mc4db for the translations.",
    },
    {
        date: "2026-10-07",
        genre: "jeu",
        fr: "Revois tes parties : à la fin d'une partie, télécharge-la, puis ouvre « Revoir » dans le menu pour la rejouer pas à pas, avec chaque carte jouée, ce qu'elle a coûté et les dégâts.",
        en: "Watch your games again: at the end of a game, download it, then open “Replay” in the menu to play it back step by step, with every card played, what it cost and the damage.",
    },
    {
        date: "2026-10-07",
        genre: "jeu",
        fr: "Range tes cartes en jeu comme tu veux : maintiens Alt et glisse une carte dans sa rangée, ou une amélioration de l'autre côté de son personnage. En Manuel, un simple glisser suffit.",
        en: "Arrange your cards in play as you like: hold Alt and drag a card within its row, or an upgrade to the other side of its character. In Manual mode, a simple drag is enough.",
    },
    {
        date: "2026-10-07",
        genre: "jeu",
        fr: "La table se personnalise encore plus : renomme une zone d'un double-clic dans « Modifier la table », choisis de quel côté se posent les améliorations, et un onglet Aide rappelle les gestes cachés.",
        en: "More ways to personalise the table: rename a zone with a double-click in “Edit the table”, choose which side upgrades go on, and a Help tab lists the hidden gestures.",
    },
    {
        date: "2026-10-07",
        genre: "jeu",
        fr: "Quand tu regardes la partie d'un autre, tu vois son curseur, ses clics et la phase du méchant avancer en direct.",
        en: "When you watch someone else's game, you see their cursor, their clicks and the villain phase moving forward live.",
    },
    {
        date: "2026-10-07",
        genre: "coulisses",
        fr: "Nouveaux bruitages avec un volume réglable, nouvel écran de face-à-face et nouvelle image de victoire. Les étiquettes de type disparaissent des cartes en jeu (un réglage les remet).",
        en: "New sound effects with adjustable volume, a new face-off screen and a new victory image. Type labels are gone from cards in play (a setting brings them back).",
    },
    {
        date: "2026-10-07",
        genre: "correction",
        fr: "La phase du méchant ne saute plus d'étape et n'avance plus toute seule pendant que tu lis, la fenêtre de défense reste dans l'écran, et une partie ordinaire ne valide plus un scénario de campagne.",
        en: "The villain phase no longer skips a step or moves on by itself while you read, the defence window stays on screen, and an ordinary game no longer completes a campaign scenario.",
    },
    {
        date: "2026-10-06",
        genre: "jeu",
        fr: "Le journal de la partie est plus lisible : les noms de cartes s'affichent en survol, et les phases et les rounds sont séparés.",
        en: "The game log is easier to read: card names show on hover, and phases and rounds are separated.",
    },
    {
        date: "2026-10-05",
        genre: "jeu",
        fr: "Deux façons de jouer : Automatique, où le moteur fait tout, ou Manuel, comme sur OCTGN, où tu poses, tournes et comptes tout à la main. Un interrupteur en haut permet de passer de l'une à l'autre en pleine partie, et un onglet à droite rappelle les raccourcis.",
        en: "Two ways to play: Automatic, where the engine does everything, or Manual, like OCTGN, where you place, turn and count everything by hand. A switch at the top flips between them mid-game, and a tab on the right lists the shortcuts.",
    },
    {
        date: "2026-10-05",
        genre: "jeu",
        fr: "La table se réarrange à ta main : tu peux séparer ou regrouper les cartes (héros, soutiens, alliés, sbires, manigances...) et poser chaque zone où tu veux. Rien ne change tant que tu n'y touches pas.",
        en: "The table now rearranges to your liking: split or group cards (heroes, supports, allies, minions, schemes...) and put each zone wherever you want. Nothing changes until you touch it.",
    },
    {
        date: "2026-10-05",
        genre: "jeu",
        fr: "La phase du méchant se vit comme tu préfères : étape par étape, directement sur la table dans un carré déplaçable, ou d'un coup. Une fenêtre te présente les trois façons à ta première partie, et le choix se change dans les Réglages.",
        en: "The villain phase plays out the way you like: step by step, right on the table in a movable square, or all at once. A window shows the three ways on your first game, and you can change it in Settings.",
    },
    {
        date: "2026-10-05",
        genre: "correction",
        fr: "Les bulles de dégâts et de jetons se posent maintenant d'après l'art affiché, y compris pour les arts alternatifs, au lieu de la carte officielle.",
        en: "Damage and token bubbles are now placed according to the displayed art, alternate arts included, instead of the official card.",
    },
    {
        date: "2026-10-03",
        genre: "jeu",
        fr: "Les arts alternatifs se choisissent maintenant dans un grand carrousel, une série pour le héros et une autre pour son alter ego si tu veux. Avec un compte, ton choix te suit sur tous tes appareils.",
        en: "Alternate arts are now picked in a big carousel, one set for the hero and another for the alter ego if you like. With an account, your choice follows you across devices.",
    },
    {
        date: "2026-10-02",
        genre: "jeu",
        fr: "Près de 170 arts alternatifs de héros et d'alter ego, de Spider-Man à Luke Cage, à choisir dans la fiche du héros. Les valeurs et le texte sont ceux de la vraie carte.",
        en: "Nearly 170 alternate hero and alter-ego arts, from Spider-Man to Luke Cage, to pick from the hero sheet. Values and text match the real card.",
    },
    {
        date: "2026-10-02",
        genre: "heros",
        fr: "Conan rejoint le roster fan-made : il passe librement de Thief à Barbarian, accumule des compteurs Crom sur The Cimmerian jusqu'à devenir King Conan, et affronte deux sbires némésis.",
        en: "Conan joins the fan-made roster: he switches freely between Thief and Barbarian, builds Crom counters on The Cimmerian until he becomes King Conan, and faces two nemesis minions.",
    },
    {
        date: "2026-10-02",
        genre: "correction",
        fr: "Les alliés de Luke Cage et une quinzaine d'alliés fan-made (Lockjaw, Okoye, Iron Lad, Red Sonja...) subissent maintenant leurs dégâts consécutifs, et « Piecing It All Together » ne compte plus dans la limite de manigances de joueur.",
        en: "Luke Cage allies and about fifteen fan-made allies (Lockjaw, Okoye, Iron Lad, Red Sonja...) now take their consequential damage, and \"Piecing It All Together\" no longer counts against the player side scheme limit.",
    },
    {
        date: "2026-10-02",
        genre: "correction",
        fr: "Pack Jessica Jones revérifié carte par carte : les alliés (Squirrel Girl, Spider-Woman...) subissent bien les dégâts consécutifs en attaquant ou en contrant, la menace de départ de plusieurs complots est corrigée, et Ticked Off, Strategy Session et deux autres cartes fonctionnent comme sur la carte.",
        en: "Jessica Jones pack rechecked card by card: allies (Squirrel Girl, Spider-Woman...) now take consequential damage when attacking or thwarting, the starting threat of several schemes is fixed, and Ticked Off, Strategy Session and two other cards work as printed.",
    },
    {
        date: "2026-10-01",
        genre: "jeu",
        fr: "Chez Storm, les cartes Météo que tu n'utilises pas se rangent maintenant sous celle qui est en jeu, et chacune se survole pour la lire.",
        en: "On Storm's board, the Weather cards you aren't using now tuck under the one in play, and you can hover each one to read it.",
    },
    {
        date: "2026-10-01",
        genre: "correction",
        fr: "Le bandeau « À toi de jouer » ne passe plus sous les boutons du haut, et il se déplace comme les autres fenêtres. Un bouton « Voir la table » rend les fenêtres transparentes pour regarder le plateau.",
        en: "The “Your turn” banner no longer slides under the top buttons, and it can be dragged like the other windows. A “See the table” button makes windows see-through so you can look at the board.",
    },
    {
        date: "2026-10-01",
        genre: "correction",
        fr: "Une carte d'identité n'affiche plus à tort « Injouable » pendant la mise en place.",
        en: "An identity card no longer wrongly shows “Unplayable” during setup.",
    },
    {
        date: "2026-09-30",
        genre: "correction",
        fr: "En fin de phase joueur, les obligations et attachements de la rencontre épuisés se redressent bien, comme le demandent les règles.",
        en: "At the end of the player phase, exhausted encounter obligations and attachments now ready properly, as the rules say.",
    },
    {
        date: "2026-09-29",
        genre: "jeu",
        fr: "Le jeu se lance depuis un salon vocal du serveur Discord : le premier qui ouvre l'activité tient la table avec son compte, les autres s'assoient en un clic, avec leur compte ou en invité.",
        en: "The game now launches from a voice channel on the Discord server: whoever opens the activity first hosts the table with their account, everyone else takes a seat in one click, with their account or as a guest.",
    },
    {
        date: "2026-09-28",
        genre: "jeu",
        fr: "Répartir des dégâts ou un soin sur plusieurs cibles ne se fait plus clic par clic : un bouton « +N » sur chaque carte lui assigne d'un coup tout ce qu'elle peut encore recevoir.",
        en: "Splitting damage or healing across several targets no longer takes one click per point: a “+N” button on each card assigns it everything it can still take, in one click.",
    },
    {
        date: "2026-09-28",
        genre: "jeu",
        fr: "La fenêtre de décision peut se faire glisser par son bandeau : pratique quand deux décisions s'empilent et que celle du dessus cache ce qu'il y a dessous.",
        en: "The decision window can now be dragged by its title bar: handy when two decisions stack up and the top one hides what's underneath.",
    },
    {
        date: "2026-09-28",
        genre: "jeu",
        fr: "Une sélection où l'ordre de clic compte (remettre des cartes sur le dessus du deck, choisir quel sbire s'active en premier…) numérote maintenant chaque carte choisie, avec deux boutons pour échanger deux cartes sans tout recommencer.",
        en: "A selection where click order matters (putting cards back on top of the deck, choosing which minion activates first…) now numbers each chosen card, with two buttons to swap two of them without starting over.",
    },
    {
        date: "2026-09-28",
        genre: "jeu",
        fr: "Quand une carte Renfort enchaîne une deuxième révélation, un bandeau « Renfort : … » le dit clairement, au lieu de laisser passer les deux cartes d'un coup sans prévenir.",
        en: "When a Surge card triggers a second reveal, a “Surge: …” banner now says so clearly, instead of both cards flashing by unannounced.",
    },
    {
        date: "2026-09-28",
        genre: "correction",
        fr: "Annuler revient exactement sur ta dernière action, plus jamais plusieurs coups en arrière. Les cartes qui n'ont rien à voir avec ce coup ne rejouent plus leur animation d'arrivée à chaque annulation.",
        en: "Undo now steps back exactly one action, never several at once. Cards unrelated to that action no longer replay their entrance animation every time you undo.",
    },
    {
        date: "2026-09-28",
        genre: "correction",
        fr: "Une capacité qui annule la révélation d'une carte cachée (Spider-Tingle, Scarlet Spider, Protection Mystique…) ne nomme plus la carte avant qu'elle soit révélée : le suspense reste entier.",
        en: "An ability that cancels a face-down card's reveal (Spider-Tingle, Scarlet Spider, Mystical Protection…) no longer names the card before it's actually revealed: the suspense stays intact.",
    },
    {
        date: "2026-09-28",
        genre: "correction",
        fr: "SP//dr : payer un coût en mélangeant une interface et une ressource de carte en main ne perd plus le paiement déjà posé, quel que soit l'ordre dans lequel tu cliques.",
        en: "SP//dr: paying a cost by mixing an interface and a hand card's resource no longer loses the payment you already made, whatever order you click in.",
    },
    {
        date: "2026-09-25",
        genre: "correction",
        fr: "Sur l'écran « Statistiques », tes dégâts, soins, cartes piochées et succès sont enfin les tiens : ils ne se mélangeaient plus avec ceux d'un invité sur ta table.",
        en: "On the “Statistics” screen, your damage, healing, cards drawn and feats are finally your own: they no longer mixed with a guest's on your table.",
    },
    {
        date: "2026-09-25",
        genre: "correction",
        fr: "Le portrait de Cloak & Dagger (DesignHacker) s'affiche enfin correctement, dans la grille comme en grand : les deux héros bien visibles côte à côte, et leur nom complet au survol.",
        en: "Cloak & Dagger's (DesignHacker) portrait finally displays correctly, in the grid and full-size: both heroes clearly visible side by side, with their full name on hover.",
    },
    {
        date: "2026-09-25",
        genre: "jeu",
        fr: "Sur le plateau, ton héros reste collé à son deck spécial au lieu de flotter au centre de sa zone. En partie à plusieurs, ta propre zone reste toujours à gauche, même quand la vue suit le tour d'un autre joueur.",
        en: "On the board, your hero now stays right next to its special deck instead of floating in the middle of its zone. In multiplayer games, your own zone always stays on the left, even when the view follows another player's turn.",
    },
    {
        date: "2026-09-24",
        genre: "jeu",
        fr: "La liste « Reprendre une partie » se trie par date, se filtre par recherche, et chaque sauvegarde a son propre bouton supprimer. Les vieilles sauvegardes de plus de deux semaines s'effacent maintenant toutes seules.",
        en: "The “Resume a game” list now sorts by date, can be searched, and each save has its own delete button. Saves older than two weeks now clear themselves out automatically.",
    },
    {
        date: "2026-09-24",
        genre: "correction",
        fr: "Wave et Red Sonja ont enfin leur halo de couleur autour du plateau : il manquait depuis leur arrivée dans le roster.",
        en: "Wave and Red Sonja finally have their board color halo: it was missing since they joined the roster.",
    },
    {
        date: "2026-09-24",
        genre: "jeu",
        fr: "La barre du haut en partie est plus légère : Menu regroupe le retour au menu et la déconnexion, et un bouton ⚙️ range la pause, l'historique, les réglages et la langue.",
        en: "The in-game top bar is lighter: Menu now groups going back to the menu and disconnecting, and a ⚙️ button holds pause, history, settings and language.",
    },
    {
        date: "2026-09-24",
        genre: "jeu",
        fr: "En partie à plusieurs héros, une confirmation apparaît si tu t'apprêtes à agir pour un héros différent de celui affiché à l'écran.",
        en: "In multi-hero games, a confirmation now appears if you're about to act for a hero other than the one shown on screen.",
    },
    {
        date: "2026-09-24",
        genre: "jeu",
        fr: "Dans le sélecteur de vue, l'onglet d'un héros qui a fini son tour s'affiche grisé.",
        en: "In the view selector, a hero's tab now dims once they've finished their turn.",
    },
    {
        date: "2026-09-24",
        genre: "jeu",
        fr: "La mise en place d'une partie est plus calme : seule la manigance principale s'affiche en grand, le reste ne vole plus dans tous les sens à l'écran.",
        en: "Game setup is calmer now: only the main scheme gets the big reveal, everything else stops flying across the screen.",
    },
    {
        date: "2026-09-24",
        genre: "jeu",
        fr: "Nouveaux réglages (⚙️ Réglages) : finir son tour automatiquement quand il ne reste plus rien à jouer, payer automatiquement quand une seule ressource peut couvrir un coût, et la touche Espace pour terminer son tour sans cliquer. Le jeu demande ton accord la première fois pour les deux premiers.",
        en: "New settings (⚙️ Settings): auto-ending your turn when nothing's left to play, auto-paying when only one resource can cover a cost, and the Space key to end your turn without clicking. The game asks for your OK the first time for the first two.",
    },
    {
        date: "2026-09-24",
        genre: "jeu",
        fr: "Une sauvegarde automatique se fait maintenant à chaque changement de phase, en plus des trois emplacements manuels.",
        en: "An automatic save now happens at every phase change, in addition to the three manual save slots.",
    },
    {
        date: "2026-09-23",
        genre: "heros",
        fr: "Wave (Pearl Pangan) rejoint le roster fan-made : sa zone Rising Tide retourne des cartes face visible ou cachée pour alimenter ses pouvoirs, avec un set némésis de cinq cartes (Alontech).",
        en: "Wave (Pearl Pangan) joins the fan-made roster: her Rising Tide area flips cards face up or down to fuel her powers, with a five-card nemesis set (Alontech).",
    },
    {
        date: "2026-09-23",
        genre: "heros",
        fr: "Red Sonja rejoint le roster fan-made : son action She-Devil incline une arme pour jouer un événement à moindre coût, avec Conan en allié signature et un set némésis glacial (Ice Queen).",
        en: "Red Sonja joins the fan-made roster: her She-Devil action exhausts a weapon to play an event at reduced cost, with Conan as a signature ally and an icy nemesis set (Ice Queen).",
    },
    {
        date: "2026-09-23",
        genre: "jeu",
        fr: "La bande de couleur du héros, en bas à droite du plateau, ressort davantage : la teinte principale est maintenant pleine plutôt que dégradée.",
        en: "The hero's color band, at the bottom right of the board, stands out more: the primary tint is now solid instead of faded.",
    },
    {
        date: "2026-09-23",
        genre: "correction",
        fr: "La zone « Mises de côté / autres piles » n'empiète plus sur le deck du héros quand elle contient plusieurs piles (set némésis, cartes mises de côté…) : elle défile dans son propre espace au lieu de chevaucher la pile voisine.",
        en: "The “Set-aside / other piles” area no longer overlaps the hero's deck when it holds several piles (nemesis set, set-aside cards…): it now scrolls within its own space instead of spilling onto the neighboring pile.",
    },
    {
        date: "2026-09-19",
        genre: "correction",
        fr: "« Mes signalements » a enfin un bouton sur l'écran de préparation, et la pastille de réponse ouvre la bonne page au lieu d'un onglet vide.",
        en: "\u201cMy reports\u201d finally has a button on the preparation screen, and the reply badge opens the right page instead of a blank tab.",
    },
    {
        date: "2026-09-19",
        genre: "jeu",
        fr: "Chaque boîte de campagne montre la couverture de son livret dans le choix des scénarios, à la place de la photo du produit.",
        en: "Every campaign box now shows its rulebook cover in the scenario picker, instead of the product photo.",
    },
    {
        date: "2026-09-19",
        genre: "jeu",
        fr: "Le livret de règles et le carnet de campagne de Fear No Evil rejoignent le panneau Documents.",
        en: "Fear No Evil's rulebook and campaign log join the Documents panel.",
    },
    {
        date: "2026-09-19",
        genre: "jeu",
        fr: "Les cinq affaires de Fear No Evil sont dans l'ordre du livret, Kingpin en dernier, et chaque tuile montre un sous-fifre différent au lieu de cinq fois le même.",
        en: "Fear No Evil's five cases now follow the rulebook order, Kingpin last, and each tile shows a different underling instead of the same one five times.",
    },
    {
        date: "2026-09-19",
        genre: "jeu",
        fr: "Fear No Evil arrive en entier : les cinq affaires et Kingpin, chaque affaire contre le sous-fifre de ton choix. En campagne, tu les joues dans l'ordre que tu veux.",
        en: "Fear No Evil lands in full: the five cases plus Kingpin, each case against the underling you pick. In campaign mode you play them in any order you like.",
    },
    {
        date: "2026-09-19",
        genre: "correction",
        fr: "Les récompenses de campagne arrivent vraiment au scénario suivant. Neuf oublis corrigés, dans six boîtes : artefacts rapportés, Pierre du Pouvoir, matériel S.H.I.E.L.D. amélioré, Maraudeurs vaincus, serrures de la cellule.",
        en: "Campaign rewards now really carry into the next scenario. Nine misses fixed across six boxes: recovered artifacts, the Power Stone, upgraded S.H.I.E.L.D. tech, defeated Marauders, the holding cell locks.",
    },
    {
        date: "2026-09-19",
        genre: "jeu",
        fr: "Chaque campagne montre la couverture de son livret dans l'écran de sélection.",
        en: "Every campaign now shows its rulebook cover in the selection screen.",
    },
    {
        date: "2026-09-19",
        genre: "jeu",
        fr: "Sur le plateau, ton deck et ta défausse sont à la hauteur de ton héros, au lieu d'être relégués en bas.",
        en: "On the board, your deck and discard pile now sit at your hero's height instead of being pushed to the bottom.",
    },
    {
        date: "2026-09-19",
        genre: "correction",
        fr: "À l'aperçu, les héros maison montrent enfin leurs deux faces, héros et alter-ego. Soixante-trois d'entre eux n'en montraient qu'une.",
        en: "In the preview, custom heroes finally show both sides, hero and alter-ego. Sixty-three of them only showed one.",
    },
    {
        date: "2026-09-19",
        genre: "correction",
        fr: "En Costume cherche bien un allié ET une amélioration qui peut s'attacher à lui. Il laissait prendre deux améliorations, puis se défaussait sans rien donner.",
        en: "Suit Up now really looks for an ally AND an upgrade that can be attached to it. It used to let you take two upgrades, then discard itself for nothing.",
    },
    {
        date: "2026-09-19",
        genre: "jeu",
        fr: "Un lien Accueil dans la barre du site : installé en application, le jeu n'a pas de bouton Précédent.",
        en: "A Home link in the site bar: installed as an app, the game has no Back button.",
    },
    {
        date: "2026-09-19",
        genre: "correction",
        fr: "« Mes signalements » montre tout ce qui vient de tes tables, quel que soit le siège, en nommant l'auteur.",
        en: "\u201cMy reports\u201d now shows everything from your tables, whatever the seat, naming who wrote it.",
    },
    {
        date: "2026-09-19",
        genre: "correction",
        fr: "Un signalement dont l'envoi échoue n'est plus perdu : il t'est rendu à la réouverture du panneau.",
        en: "A report that fails to send is no longer lost: you get it back when you reopen the panel.",
    },
    {
        date: "2026-09-17",
        genre: "correction",
        fr: "Sur le plateau, quand ta table a été fermée, le bandeau finit par le dire au lieu de répéter « nouvel essai » sans fin, et te propose de revenir à l'accueil.",
        en: "On the board, when your table has been closed, the banner now says so instead of endlessly retrying, and offers to take you back to the home page.",
    },
    {
        date: "2026-09-17",
        genre: "jeu",
        fr: "En français, les portraits des héros et des méchants prennent désormais l'illustration anglaise, qui n'a pas de filigrane. Le texte des cartes, lui, reste en français partout où on le lit.",
        en: "In French, hero and villain portraits now use the English artwork, which has no watermark. Card text stays in French everywhere it is read.",
    },
    {
        date: "2026-09-17",
        genre: "jeu",
        fr: "Le narval change de costume toutes les trois heures : Captain America, Magneto, Cyclope, Wolverine, Thor. Dans l'onglet comme sur les pages.",
        en: "The narwhal changes costume every three hours: Captain America, Magneto, Cyclops, Wolverine, Thor. In the tab as well as on the pages.",
    },
    {
        date: "2026-09-17",
        genre: "jeu",
        fr: "L'accueil porte le narval, et le journal des mises à jour est passé dans sa propre tuile, classé par famille. La page d'attente pendant l'allumage ne clignote plus.",
        en: "The home screen now shows the narwhal, and the update log moved into its own tile, sorted by family. The waiting screen no longer flickers while your game starts.",
    },
    {
        date: "2026-09-17",
        genre: "correction",
        fr: "Hercule : « Defeat the Hydra » ne cherchait un sbire que dans le deck de rencontre et sa défausse, jamais dans les cartes mises de côté. Elle y trouve enfin l'Hydre de Lerne, au lieu de partir sans rien faire.",
        en: "Hercules: “Defeat the Hydra” only looked for a minion in the encounter deck and its discard pile, never among the set-aside cards. It now finds the Lernean Hydra instead of doing nothing.",
    },
    {
        date: "2026-09-17",
        genre: "correction",
        fr: "Hercule : « Ancient Rivalry » ne redressait que les héros. Elle redresse maintenant l'allié Thor, qui est pourtant ce qui te permet de jouer la carte.",
        en: "Hercules: “Ancient Rivalry” only readied heroes. It now also readies the Thor ally, which is what lets you play the card in the first place.",
    },
    {
        date: "2026-09-16",
        genre: "correction",
        fr: "Lancer une partie pouvait échouer sans un mot quand ton deck était volumineux. Le bouton semblait mort, il ne l'est plus.",
        en: "Starting a game could fail silently when your deck was large. The button looked dead; it no longer is.",
    },
    {
        date: "2026-09-16",
        genre: "jeu",
        fr: "Tu peux désormais choisir Standard I, II ou III au lieu d'un seul niveau. Les cartes de Standard II et III étaient dans le jeu depuis toujours sans que personne puisse les sélectionner.",
        en: "You can now pick Standard I, II or III instead of a single level. The Standard II and III cards were always in the game, with no way to select them.",
    },
    {
        date: "2026-09-16",
        genre: "jeu",
        fr: "Les decks que tu importes depuis marvelcdb sont enregistrés sur le serveur. Ils te suivent d'un appareil à l'autre, et ne disparaissent plus avec le cache de ton navigateur.",
        en: "Decks you import from marvelcdb are now saved on the server. They follow you from one device to another and no longer vanish with your browser cache.",
    },
    {
        date: "2026-09-16",
        genre: "correction",
        fr: "Quand ta table a été fermée, l'écran de préparation te le dit au lieu de tourner dans le vide.",
        en: "When your table has been closed, the setup screen now says so instead of spinning for nothing.",
    },
    {
        date: "2026-09-16",
        genre: "jeu",
        fr: "Le site parle anglais de bout en bout : connexion, inscription, salon et choix de la langue.",
        en: "The site now speaks English throughout: sign-in, sign-up, lobby and language choice.",
    },
    {
        date: "2026-09-16",
        genre: "jeu",
        fr: "Quand une mise à jour du jeu est arrivée, un bandeau te propose de recharger. Plus besoin d'y penser toi-même.",
        en: "When a game update lands, a banner offers to reload. You no longer have to think about it yourself.",
    },
    {
        date: "2026-09-16",
        genre: "coulisses",
        fr: "L'écran de préparation interrogeait le serveur toutes les deux secondes, même quand rien ne bougeait. Il se tait quand ton onglet est caché, et le serveur respire.",
        en: "The setup screen polled the server every two seconds, even when nothing was happening. It stays quiet when your tab is hidden, and the server breathes.",
    },
    {
        date: "2026-09-16",
        genre: "coulisses",
        fr: "Une table sans personne se ferme au bout de trente minutes, pour laisser la place aux autres.",
        en: "An empty table now closes after thirty minutes, to make room for others.",
    },
    {
        date: "2026-09-16",
        genre: "jeu",
        fr: "Dans le mode Legacy, une boîte s'ouvre maintenant dès que tu as battu tous ses méchants. Les héros ne bloquent plus rien : ta première victoire avec un héros officiel te rapporte un jeton, deux si elle est prise en expert.",
        en: "In Legacy mode, a box now opens as soon as you have beaten every villain in it. Heroes no longer block anything: your first win with an official hero earns a token, two if it was on expert.",
    },
    {
        date: "2026-09-16",
        genre: "jeu",
        fr: "Le mode Legacy s'ouvre désormais sur une page qui explique ses règles. Une case « Ne plus afficher » la range pour de bon.",
        en: "Legacy mode now opens on a page explaining its rules. A “Don't show this again” box puts it away for good.",
    },
    {
        date: "2026-09-16",
        genre: "jeu",
        fr: "Quand tu signales un bug depuis ta propre table, tu retrouves ta demande dans « Mes signalements » : son état, ma réponse, et de quoi ajouter un mot.",
        en: "When you report a bug from your own table, you now find it under “My reports”: its state, my answer, and room to add something.",
    },
    {
        date: "2026-09-16",
        genre: "jeu",
        fr: "L'écran du choix de la langue te prévient : une carte qui n'a pas encore de scan dans ta langue reste affichée en anglais, avec sa traduction dans l'infobulle.",
        en: "The language screen now warns you: a card with no scan in your language yet stays in English, with its translation in the tooltip.",
    },
    {
        date: "2026-09-16",
        genre: "correction",
        fr: "Le mot EXPERT ne s'affiche plus sur le portrait des méchants : la difficulté se choisit à la préparation, pas sur l'image.",
        en: "The word EXPERT no longer shows on villain portraits: difficulty is picked during setup, not on the picture.",
    },
    {
        date: "2026-09-16",
        genre: "correction",
        fr: "Le bouton FR / EN n'apparaît plus en double dans la barre du haut.",
        en: "The FR / EN button no longer shows up twice in the top bar.",
    },
    {
        date: "2026-09-15",
        genre: "jeu",
        fr: "Une partie ne commence plus en montrant toute la mise en place. La manigance principale s'affiche face visible, tu fais OK, elle se retourne et pose sa menace de départ.",
        en: "A game no longer starts by showing the whole setup. The main scheme appears face up, you click OK, it flips over and places its starting threat.",
    },
    {
        date: "2026-09-15",
        genre: "correction",
        fr: "Trois corrections du glisser-déposer : lâcher ton héros sur le méchant ne propose plus l'attaque d'un allié, une carte jouée se pose près de son héros et non chez le méchant, et une carte sans cible peut enfin se lâcher sur le terrain.",
        en: "Three drag-and-drop fixes: dropping your hero on the villain no longer offers an ally's attack, a played card lands next to its hero instead of the villain's side, and a card with no target can finally be dropped on the table.",
    },
    {
        date: "2026-09-15",
        genre: "jeu",
        fr: "La barre du haut est remise en ordre : l'avancée de la partie à gauche, les boutons à droite.",
        en: "The top bar is tidied up: game progress on the left, buttons on the right.",
    },
    {
        date: "2026-09-14",
        genre: "jeu",
        fr: "Les réglages deviennent une fenêtre à onglets, au lieu d'un menu caché dans un menu.",
        en: "Settings are now a tabbed window instead of a menu hidden inside a menu.",
    },
    {
        date: "2026-09-14",
        genre: "jeu",
        fr: "Les cartes du plateau grandissent avec la taille de ton écran.",
        en: "Board cards now grow with your screen size.",
    },
    {
        date: "2026-09-14",
        genre: "correction",
        fr: "Cinq cartes étaient injouables. Elles sont corrigées, et un contrôle empêche désormais qu'une carte parte dans cet état.",
        en: "Five cards could not be played. They are fixed, and a check now prevents a card from shipping in that state.",
    },
    {
        date: "2026-09-13",
        genre: "jeu",
        fr: "Si ta table se ferme pendant que tu joues (mise à jour, inactivité), ta partie est sauvegardée et le site te propose de la reprendre là où tu l'avais laissée dès ta prochaine visite. Tu peux aussi commencer autre chose : la sauvegarde reste dans « Reprendre ».",
        en: "If your table closes while you are playing (update, inactivity), your game is saved and the site offers to resume it right where you left off on your next visit. You can also start something else: the save stays under “Resume”.",
    },
    {
        date: "2026-09-13",
        genre: "correction",
        fr: "En partie, quand le méchant t'attaque, les boutons Défendre / Demander / Passer restent collés au bas de la fenêtre : plus besoin de faire défiler pour trouver quoi répondre.",
        en: "In game, when the villain attacks you, the Defend / Ask / Pass buttons now stay pinned to the bottom of the window: no more scrolling to find what to answer.",
    },
    {
        date: "2026-09-13",
        genre: "jeu",
        fr: "À ta prochaine visite, le jeu te demande une fois dans quelle langue tu veux tes cartes. Tu peux changer d'avis quand tu veux avec le bouton FR / EN, en haut de l'écran.",
        en: "On your next visit, the game asks you once which language you want your cards in. You can change your mind whenever you like with the FR / EN button at the top of the screen.",
    },
    {
        date: "2026-09-13",
        genre: "jeu",
        fr: "Le jeu s'installe sur ton téléphone : sur narwhalchampions.com, menu du navigateur, « Ajouter à l'écran d'accueil ». Une icône, un plein écran, et il t'amène droit à ta table. C'est un raccourci, pas une version hors ligne : le jeu tourne sur le serveur, il faut une connexion pour jouer.",
        en: "The game installs on your phone: on narwhalchampions.com, browser menu, “Add to Home screen”. An icon, full screen, and it takes you straight to your table. It is a shortcut, not an offline version: the game runs on the server, you need a connection to play.",
    },
    {
        date: "2026-09-13",
        genre: "jeu",
        fr: "Nouveau mode Legacy, sur l'accueil : tu commences avec la boîte de base et ses cinq héros, et tu débloques la suite boîte par boîte en gagnant. Ce qui est fermé reste visible, grisé, avec ce qu'il faut faire pour l'ouvrir. Chaque première victoire avec un héros officiel donne un jeton, qui débloque le héros fan-made de ton choix ; en expert, deux. Le deck-building suit : seules les cartes des boîtes déjà ouvertes s'ajoutent au deck.",
        en: "New Legacy mode on the home screen: you start with the core set and its five heroes, and unlock the rest box by box by winning. Locked content stays visible, greyed out, with what it takes to open it. Every first win with an official hero grants a token, which unlocks the fan-made hero of your choice; two on expert. Deck-building follows suit: only cards from boxes you have opened can go in the deck.",
    },
    {
        date: "2026-09-13",
        genre: "jeu",
        fr: "Si quelqu'un t'écrit, une pastille verte apparaît en bas à droite, dans la préparation comme en pleine partie, et ouvre la conversation. Tant que personne ne t'écrit, il n'y a rien à l'écran.",
        en: "If someone writes to you, a green badge appears at the bottom right, on the setup screens and in game, and opens the conversation. As long as nobody writes, there is nothing on screen.",
    },
    {
        date: "2026-09-13",
        genre: "jeu",
        fr: "Chaque partie terminée est gardée : tu peux la revoir pas à pas avec le bouton « Revoir », comme si tu y étais. Les cinquante dernières restent disponibles.",
        en: "Every finished game is kept: you can replay it step by step with the “Resume” button, as if you were there. The last fifty stay available.",
    },
    {
        date: "2026-09-13",
        genre: "correction",
        fr: "Les trois emplacements de sauvegarde étaient les mêmes pour tout le monde : on pouvait écraser la partie d'un autre, ou en charger une qu'on n'avait jamais jouée. Chacun a désormais les siens.",
        en: "The three save slots were shared by everyone: you could overwrite someone else's game, or load one you had never played. Everyone now has their own.",
    },
    {
        date: "2026-09-13",
        genre: "coulisses",
        fr: "Une table laissée ouverte sans qu'on y joue se ferme au bout de trois quarts d'heure, pour rendre la place à quelqu'un d'autre. Ta partie est sauvegardée avant : tu la retrouves avec « Reprendre ».",
        en: "A table left open without anyone playing closes after forty-five minutes, to give the seat back to someone else. Your game is saved first: you will find it again under “Resume”.",
    },
    {
        date: "2026-09-13",
        genre: "heros",
        fr: "Sentinel rejoint le roster. Ce Sentinelle de T-Wrecks porte quatre composants qu'on installe sur lui ; les coups les détruisent un à un, et il passe la partie à les réparer. Il amène aussi un nouvel état, Exposé, qui fait encaisser plus cher la prochaine attaque.",
        en: "Sentinel joins the roster. T-Wrecks’ Sentinel carries four components attached to it; hits destroy them one by one, and it spends the game repairing them. It also brings a new status, Exposed, which makes the next attack hurt more.",
    },
    {
        date: "2026-09-13",
        genre: "jeu",
        fr: "Quand une mise à jour approche, un bandeau rouge traverse le haut de l'écran toutes les trente secondes, avec le temps qu'il reste. Il ne gêne pas le jeu : les clics le traversent. C'est le moment de sauvegarder ta partie, elle ne survit pas au redémarrage.",
        en: "When an update is coming, a red banner sweeps across the top of the screen every thirty seconds with the time left. It never blocks play: clicks go straight through it. That is the moment to save your game, it does not survive the restart.",
    },
    {
        date: "2026-09-13",
        genre: "coulisses",
        fr: "Les places sont comptées. Quatre semaines sans venir et ton compte se met en pause : sa place retourne au pot, mais tes decks et tes campagnes t'attendent tant que personne ne l'a prise. Écris-moi, je te la rends.",
        en: "Seats are limited. Four weeks without visiting and your account goes on hold: its seat returns to the pool, but your decks and campaigns wait for you until someone takes it. Write to me and I will give it back.",
    },
    {
        date: "2026-09-13",
        genre: "jeu",
        fr: "Sur l'écran d'accueil, chaque mode dit ce qu'il fait quand tu passes la souris dessus. Sur téléphone, la phrase est affichée en permanence sous la tuile.",
        en: "On the home screen, each mode now explains itself when you hover over it. On a phone, the sentence is shown under the tile at all times.",
    },
    {
        date: "2026-09-13",
        genre: "correction",
        fr: "Sur téléphone, la fenêtre de choix des ressources se rouvrait toute seule dès qu'on la fermait : impossible de payer avec les cartes posées sur la table. Elle reste fermée tant que tu ne la rappelles pas.",
        en: "On a phone, the resource picker reopened by itself as soon as you closed it, making it impossible to pay with the cards already on the table. It now stays closed until you call it back.",
    },
    {
        date: "2026-09-13",
        genre: "correction",
        fr: "Une carte qui réduisait un coût de plusieurs ressources n'en valait qu'une au moment de payer. Les réductions comptent maintenant pour leur vraie valeur.",
        en: "A card reducing a cost by several resources only counted as one when paying. Reductions are now worth their real value.",
    },
    {
        date: "2026-09-13",
        genre: "correction",
        fr: "L'extension des Spider-Man s'appelle Sinistres Motivations, et non Intentions Sinistres.",
        en: "The Spider-Man expansion is called Sinister Motives.",
    },
    {
        date: "2026-09-12",
        genre: "jeu",
        fr: "La barre du haut s'allège : Annuler, Sauver, Bug, un bouton Réglages qui range tout le reste (historique, options, journal, musique, langue), et Fin du tour, qui revient aussi en bas de l'écran. Le dessin des cartes ressources se choisit désormais à l'étape des decks.",
        en: "The top bar slims down: Undo, Save, Bug, a Settings button holding everything else (history, options, log, music, language), and End turn, which also returns at the bottom of the screen. The resource cards’ artwork is now picked at the decks step.",
    },
    {
        date: "2026-09-12",
        genre: "jeu",
        fr: "Les cartes d'état (Tenace, Sonné, Désorienté) sont de vrais scans, nets en grand, en français comme en anglais.",
        en: "Status cards (Tough, Stunned, Confused) are now real scans, sharp when enlarged, in French and in English.",
    },
    {
        date: "2026-09-12",
        genre: "jeu",
        fr: "Le tchat quitte le jeu : le bouton « Joueurs & tchat » disparaît de la préparation et de la partie.",
        en: "The chat leaves the game: the “Players & chat” button is gone from the setup screens and from the board.",
    },
    {
        date: "2026-09-12",
        genre: "jeu",
        fr: "Le plateau du téléphone change : quatre bandes qu'on fait glisser du doigt (méchant, manigances, engagés, ton héros), avec de vraies cartes lisibles. Ta main se range derrière l'encoche de droite et sort d'un swipe ou toute seule quand le jeu te demande une carte ; les piles sont derrière l'encoche de gauche. Fin du tour et le menu « … » sont dans le bandeau du haut.",
        en: "The phone board changes: four strips you swipe through (villain, schemes, engaged, your hero), with real, readable cards. Your hand tucks behind the right-hand notch and slides out with a swipe, or by itself when the game asks for a card; the piles sit behind the left-hand notch. End turn and the “…” menu live in the top bar.",
    },
    {
        date: "2026-09-12",
        genre: "heros",
        fr: "Les héros fan-made dont l'auteur n'a pas publié de deck n'ont plus de deck de départ inventé pour eux. À la place, tous les paquets d'aspect du tableur (Brutish Aggression, Evasive Justice…) sont proposés à tous les héros, les conseillés en tête. Les decks fournis par leur auteur (Yondu, Hellcat, Venompool, Lockjaw, Moon Knight…) ne changent pas.",
        en: "Fan-made heroes whose author did not publish a deck no longer get a made-up starter deck. Instead, every aspect package from the spreadsheet (Brutish Aggression, Evasive Justice…) is offered to every hero, recommended ones first. Decks provided by their author (Yondu, Hellcat, Venompool, Lockjaw, Moon Knight…) are unchanged.",
    },
    {
        date: "2026-09-12",
        genre: "jeu",
        fr: "Sur téléphone, le bouton Retour referme la feuille ouverte (menu, historique, carte en grand) au lieu de quitter la partie. Et dans l'assistant, le premier tap sur un héros ouvre sa fiche : portrait, biographie, ses cartes, avant de le choisir.",
        en: "On a phone, the Back button now closes the open sheet (menu, history, enlarged card) instead of leaving the game. And in the assistant, the first tap on a hero opens their profile: portrait, biography, their cards, before you pick them.",
    },
    {
        date: "2026-09-12",
        genre: "jeu",
        fr: "Sur téléphone, les menus du plateau (Options, Historique, le menu « … », le journal du héros, les questions du jeu) s'ouvrent en feuille depuis le bas de l'écran, avec des boutons faits pour le doigt. Le plateau passe en plein écran au premier tap, et la fenêtre de choix du héros tient dans l'écran.",
        en: "On a phone, the board menus (Options, History, the “…” menu, the hero log, the game's questions) open as a sheet from the bottom of the screen, with finger-sized buttons. The board goes full screen on the first tap, and the hero options window fits the screen.",
    },
    {
        date: "2026-09-12",
        genre: "jeu",
        fr: "Quand une carte peut réagir (« Objection ! » de Jennifer Walters avant la menace, Spider-Sense avant une attaque…), le panneau dit qui peut réagir, montre la carte et le texte de la capacité, en français officiel. Plus besoin de survoler pour comprendre.",
        en: "When a card can react (Jennifer Walters' “I Object!” before threat is placed, Spider-Sense before an attack…), the panel says who can react, shows the card and the ability text. No more hovering to understand.",
    },
    {
        date: "2026-09-12",
        genre: "correction",
        fr: "Dans le déroulé de la phase du méchant, survoler une carte de la scène l'affiche de nouveau en grand. Et une carte qui garde de la menace sans être une manigance (Policière en Patrouille, Détective Privé, l'Armure d'Howard…) montre enfin combien elle en porte.",
        en: "In the villain phase walkthrough, hovering a card in the scene shows it large again. And a card that holds threat without being a scheme (Beat Cop, Private Investigator, Howard's Iron Suit…) finally shows how much it carries.",
    },
    {
        date: "2026-09-12",
        genre: "correction",
        fr: "En mode Détaillé, une carte à jouer « quand la menace va être placée » ouvrait une question sans aucun bouton au tout début de la phase du méchant, et la partie restait bloquée. La question s'affiche maintenant, avec Passer.",
        en: "In Detailed mode, a card playable “when threat would be placed” opened a question with no button at the very start of the villain phase, and the game stayed stuck. The question now shows up, with Pass.",
    },
    {
        date: "2026-09-12",
        genre: "jeu",
        fr: "Un sbire qui entre en jeu en pleine phase du méchant (un Drone mis en jeu par l'attaque d'Ultron, un Gobelin sorti par un boost) a maintenant sa propre étape dans le déroulé, avant son attaque, avec ce qui l'a fait entrer.",
        en: "A minion that enters play in the middle of the villain phase (a Drone put into play by Ultron's attack, a Goblin brought out by a boost) now gets its own step in the walkthrough, before its attack, with what brought it in.",
    },
    {
        date: "2026-09-11",
        genre: "correction",
        fr: "Jackpot! (Yondu) fait enfin son travail : la carte dépensée juste après elle vaut bien le double de ses ressources.",
        en: "Jackpot! (Yondu) finally does its job: the card spent right after it is really worth double its resources.",
    },
    {
        date: "2026-09-11",
        genre: "jeu",
        fr: "Crisis Averted et On the Prowl sous une Crise : si tu t'apprêtes à les payer sans la ressource mentale qu'elles exigent, le jeu te prévient avant d'envoyer ton coup, au lieu de laisser la carte partir sans rien retirer.",
        en: "Crisis Averted and On the Prowl under a Crisis: if you are about to pay them without the mental resource they require, the game warns you before your play is sent, instead of letting the card go for nothing.",
    },
    {
        date: "2026-09-11",
        genre: "jeu",
        fr: "Une seule tuile par héros : au clic, une fenêtre propose ce que ce héros a de particulier (version du deck, identité alternative, art de la carte, collection de ressources) et s'en souvient d'une partie à l'autre. Hellcat avec Iron Man ou Miss Hulk, Superior Spider-Man avec Peter Parker ou Elliot Tolliver.",
        en: "One tile per hero: clicking it opens a window with what this hero has to offer (deck version, alternate identity, card art, resource collection), remembered from game to game. Hellcat with Iron Man or She-Hulk, Superior Spider-Man with Peter Parker or Elliot Tolliver.",
    },
    {
        date: "2026-09-11",
        genre: "heros",
        fr: "Hellcat (Patsy Walker), héroïne fan-made de jakxin : elle accroche à son identité les événements à ressource mentale qu'elle joue et les convertit en ressources. Deux decks de départ (Iron Man ou Miss Hulk en allié signature), set némésis à deux sbires, et six cartes custom du deck imprimé (Firestar, Monica Rambeau, Green Hell, Hell-Iron, Divas, un reskin de Chase Them Down).",
        en: "Hellcat (Patsy Walker), a fan-made hero by jakxin: she attaches the mental-resource events she plays to her identity and turns them into resources. Two starter decks (Iron Man or She-Hulk as signature ally), a two-minion nemesis set, and six custom cards from the printed deck (Firestar, Monica Rambeau, Green Hell, Hell-Iron, Divas, a Chase Them Down reskin).",
    },
    {
        date: "2026-09-11",
        genre: "correction",
        fr: "Les cartes de statut (Stunned, Confused, Tough) sont enfin nettes en grand : elles étaient affichées à partir d'une image de 149 pixels étirée quatre fois. Merci à Manu pour le signalement.",
        en: "Status cards (Stunned, Confused, Tough) are finally sharp when enlarged: they were drawn from a 149-pixel image stretched four times. Thanks to Manu for reporting it.",
    },
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
