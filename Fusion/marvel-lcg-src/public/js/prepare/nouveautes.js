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
// LEVE depuis : le plateau portrait a ete valide le 13/09/2026, et la refonte
// du telephone (09/10/2026) s'annonce comme le reste.
export const NOUVEAUTES = [
    {
        date: "2026-10-28",
        genre: "jeu",
        fr: "En rejoignant par un lien d'invitation, tu peux maintenant te connecter à ton compte depuis l'écran de choix pour retrouver tes decks sauvegardés (s'ils ne s'affichent pas déjà parce que tu es connecté).",
        en: "When joining from an invitation link, you can now log into your account from the pick screen to get your saved decks back (if they aren't already shown because you're logged in).",
    },
    {
        date: "2026-10-28",
        genre: "jeu",
        fr: "Quand tu rejoins une partie par un lien d'invitation, l'écran de choix de héros montre maintenant les images des cartes et les mêmes filtres que l'assistant (recherche, vagues, fan-made séparé de l'officiel).",
        en: "When you join a game from an invitation link, the hero-picking screen now shows the card images and the same filters as the main wizard (search, waves, fan-made kept apart from official).",
    },
    {
        date: "2026-10-28",
        genre: "jeu",
        fr: "Campagne en ligne : tu peux désormais inviter tes amis pendant la composition de l'équipe, chacun choisit son propre héros et son propre deck depuis son écran avant que la partie se lance.",
        en: "Online campaign: you can now invite your friends while building the team, and each of them picks their own hero and deck from their screen before the game starts.",
    },
    {
        date: "2026-10-28",
        genre: "correction",
        fr: "Quand le jeu te propose plusieurs choix (un rôle, une manigance à mettre en jeu), survoler une option montre enfin la bonne carte, et non la manigance principale.",
        en: "When the game offers you several choices (a role, a scheme to put into play), hovering an option now shows the right card instead of the main scheme.",
    },
    {
        date: "2026-10-28",
        genre: "correction",
        fr: "À la victoire d'un scénario de campagne, le bouton « Valider » n'est plus coupé sous l'écran : la carte des récompenses tient entièrement à l'écran.",
        en: "On a campaign scenario victory, the “Validate” button is no longer cut off below the screen: the rewards card now fits fully on screen.",
    },
    {
        date: "2026-10-27",
        genre: "jeu",
        fr: "Dans le choix des héros, cliquer sur l'un d'eux fige sa fiche à gauche : survoler les autres ne la fait plus changer avant d'avoir lu ses cartes ou sa biographie.",
        en: "In hero selection, clicking a hero now locks its card in place on the left: hovering over others no longer swaps it out before you've read its cards or bio.",
    },
    {
        date: "2026-10-27",
        genre: "correction",
        fr: "She-Hulk (variante Why Not) inflige bien ses 2 dégâts fixes en plus du bonus par icône d'Accélération, et non l'un ou l'autre.",
        en: "She-Hulk (Why Not variant) now deals her 2 fixed damage on top of the Acceleration-icon bonus, instead of only one or the other.",
    },
    {
        date: "2026-10-27",
        genre: "heros",
        fr: "Le scénario fan-made « The Hunger Core » (thème Marvel Zombies) commence son arrivée : le vilain, sa manigance, et les premiers héros zombifiés du Horde deck sont en place.",
        en: "The fan-made scenario \"The Hunger Core\" (Marvel Zombies theme) starts rolling out: the villain, its scheme, and the first zombified heroes of the Horde deck are in place.",
    },
    {
        date: "2026-10-26",
        genre: "heros",
        fr: "Cinquante cartes d'aspect Starjammers (Agressivité, Justice, Leadership, Protection et Basic) de Phenexian et Mysteltainn arrivent dans le deck-builder : Cyclops, Havok, Polaris, Lilandra, Korvus Rook'shir, Kalyx et leur équipement. Elles sont encore en rodage : dis-nous ce qui cloche.",
        en: "Fifty Starjammers aspect cards (Aggression, Justice, Leadership, Protection and Basic) by Phenexian and Mysteltainn arrive in the deck-builder: Cyclops, Havok, Polaris, Lilandra, Korvus Rook'shir, Kalyx and their gear. They are still being tested: tell us what looks off.",
    },
    {
        date: "2026-10-26",
        genre: "heros",
        fr: "Quinze héros fan-made rejoignent le roster : Batman et Batgirl (ES), Wasp / Hank Pym (JackHKP), Corsair, Hepzibah, Raza, Ch'od et les Warriors Three (Phenexian et Mysteltainn), Smasher (Phenexian), Marvel Girl (Rachel Summers), Sunspot et le nouveau Winter Soldier (Dipsome), Roz Solomon (jakxin), U.S. Agent (DesignHacker) et Spider-Punisher (T-Wrecks). Ils sont encore en rodage : dis-nous ce qui cloche.",
        en: "Fifteen fan-made heroes join the roster: Batman and Batgirl (ES), Wasp / Hank Pym (JackHKP), Corsair, Hepzibah, Raza, Ch'od and the Warriors Three (Phenexian and Mysteltainn), Smasher (Phenexian), Marvel Girl (Rachel Summers), Sunspot and the new Winter Soldier (Dipsome), Roz Solomon (jakxin), U.S. Agent (DesignHacker) and Spider-Punisher (T-Wrecks). They are still being tested: tell us what looks off.",
    },
    {
        date: "2026-10-25",
        genre: "jeu",
        fr: "Sur téléphone, les cartes à plusieurs faces s'affichent l'une sous l'autre sans défilement, et dans le plateau en ronds, les lieux et les environnements d'un scénario comme La ville ne dort jamais sont regroupés en deux ronds. La phase du méchant montre toujours la carte en entier.",
        en: "On phone, multi-face cards now stack without scrolling, and in the round-token board the locations and environments of a scenario like The City Never Sleeps are grouped into two tokens. The villain phase always shows the whole card.",
    },
    {
        date: "2026-10-25",
        genre: "correction",
        fr: "Un deck sauvegardé n'apparaît plus en double, les decks s'affichent plus vite, la roue du choix au hasard tourne de nouveau sur téléphone, et le filtre Fan-made du choix du méchant est disponible sur téléphone.",
        en: "A saved deck no longer shows up twice, decks load faster, the random-pick wheel spins again on phone, and the Fan-made filter of the villain choice is available on phone.",
    },
    {
        date: "2026-10-24",
        genre: "jeu",
        fr: "Puzzles (bêta) : crée ta propre position de départ en huit étapes depuis le bouton Puzzles, publie-la pour obtenir un code, et résous celui d'un autre en tapant son code. Un panneau rappelle l'énoncé, donne les indices un par un et peut montrer la solution écrite.",
        en: "Puzzles (beta): build your own starting position in eight steps from the Puzzles button, publish it to get a code, and solve someone else's by typing their code. A panel recalls the brief, gives hints one by one and can show the written solution.",
    },
    {
        date: "2026-10-23",
        genre: "jeu",
        fr: "Shadowland (paquet officiel MC65) : trois nouveaux scénarios, Shadows in the Night, Shadow Labyrinth et Heart of Shadow, en standard et en expert, avec Ninja Swarm en module recommandé. La mini-campagne en trois scénarios est jouable, d'après le livret officiel en français (Corruption Insidieuse, Sombres Protégés retirés, cartes inscrites au registre), et le paquet de pièges suit le livret.",
        en: "Shadowland (official pack MC65): three new scenarios, Shadows in the Night, Shadow Labyrinth and Heart of Shadow, in standard and expert, with Ninja Swarm as the recommended modular set. The three-scenario mini-campaign is playable, following the official French booklet (Creeping Corruption, removed Dark Protégés, cards recorded in the log), and the trap deck follows the booklet.",
    },
    {
        date: "2026-10-23",
        genre: "correction",
        fr: "La ville ne dort jamais : la table ne montre plus que le lieu où l'on se trouve (les autres restent dans l'onglet Ville), The City et Never Sleeps s'affichent en une seule image continue, les méchants des autres territoires sont grisés, et les agrandissements de l'onglet Ville sont traduits. Les boîtes Galactic Storm et La ville ne dort jamais ont leur pochette, et la fenêtre de choix du vilain est plus compacte.",
        en: "The City Never Sleeps: the table now shows only the location you are in (the others stay in the City tab), The City and Never Sleeps display as one continuous picture, villains from other turfs are greyed out, and the enlarged cards in the City tab are translated. The Galactic Storm and The City Never Sleeps boxes now have their cover art, and the villain choice window is more compact.",
    },
    {
        date: "2026-10-23",
        genre: "heros",
        fr: "Les cartes d'aspect des paquets officiels Iron Fist et Elektra Natchios sont jouables : Shang-Chi, Black Cat, Moon Knight, Moondragon, The Defenders, Double-Cross et bien d'autres. Les anciennes versions Tortues Ninja de plusieurs de ces cartes restent disponibles en art alternatif.",
        en: "The aspect cards of the official Iron Fist and Elektra Natchios packs are now playable: Shang-Chi, Black Cat, Moon Knight, Moondragon, The Defenders, Double-Cross and many more. The older Ninja Turtles versions of several of these cards remain available as an alternate art.",
    },
    {
        date: "2026-10-20",
        genre: "heros",
        fr: "Nouvelle campagne fan-made Tempête Galactique (Galactic Storm, de Kajislav), en cinq scénarios : Sentinelle Kree, Verdict de la Majestrix, Ultimatum d'Hala, La Terre assiégée et Suprême Intelligence. Chaque joueur incarne trois identités différentes au fil de la campagne. Binary et Quasar rejoignent le roster, et des alliés de campagne (Rick Jones, Gladiator, Lauri-Ell, les Starjammers...) se recrutent au fil des victoires.",
        en: "New fan-made campaign Galactic Storm (by Kajislav), in five scenarios: Kree Sentry, Majestrix's Verdict, Hala Ultimatum, Earth Under Siege and Supreme Intelligence. Each player plays three different heroes across the campaign. Binary and Quasar join the roster, and campaign allies (Rick Jones, Gladiator, Lauri-Ell, the Starjammers...) are recruited along the way.",
    },
    {
        date: "2026-10-20",
        genre: "jeu",
        fr: "38 cartes d'aspect existent maintenant en version pleine illustration, proposée comme art alternatif à l'assignation d'un deck. Full Art Reprints : MC/DC 2026 (Jonah, Marvin, Scott, Tim).",
        en: "38 aspect cards now exist in a full-art version, offered as an alternate art when a deck is assigned. Full Art Reprints: MC/DC 2026 (Jonah, Marvin, Scott, Tim).",
    },
    {
        date: "2026-10-19",
        genre: "jeu",
        fr: "Tout le monde repart sur le nouvel affichage Normal à sa prochaine connexion. L'ancien se retrouve dans les options sous le nom Coloré, et ton choix ensuite est respecté.",
        en: "Everyone starts again on the new Normal display at their next login. The old one is still in the options under the name Colourful, and your choice after that is respected.",
    },
    {
        date: "2026-10-19",
        genre: "jeu",
        fr: "Au choix du méchant, on ne voit d'abord que les boîtes officielles. Le bouton Fan-made montre à lui seul les boîtes fan-made, comme pour les héros.",
        en: "When choosing the villain, you first see only the official boxes. The Fan-made button shows the fan-made boxes alone, as it does for heroes.",
    },
    {
        date: "2026-10-19",
        genre: "heros",
        fr: "Les Tortues Ninja arrivent : Leonardo, Michelangelo, Raphael, Donatello, Casey Jones, Jennika, Alopex et Venus, avec les méchants Shredder, Bebop et Rocksteady et Baxter Stockman.",
        en: "The Teenage Mutant Ninja Turtles arrive: Leonardo, Michelangelo, Raphael, Donatello, Casey Jones, Jennika, Alopex and Venus, with the villains Shredder, Bebop and Rocksteady and Baxter Stockman.",
    },
    {
        date: "2026-10-19",
        genre: "jeu",
        fr: "Plus de 230 cartes d'aspect aux couleurs des Tortues. Quand seule l'image change, c'est un art alternatif de la carte officielle, proposé quand tu assignes un deck. Les autres cartes sont réservées aux héros TMNT.",
        en: "Over 230 aspect cards in the Turtles' colours. When only the picture changes, it is an alternate art of the official card, offered when you assign a deck. The other cards are reserved for TMNT heroes.",
    },
    {
        date: "2026-10-19",
        genre: "jeu",
        fr: "Le pack Shinobi pour les héros TMNT : onze Paths à choisir en construisant ton deck, 80 cartes Bushido, Kuji-Kiri, Ninjutsu et Taijutsu, et 12 cartes duales.",
        en: "The Shinobi pack for TMNT heroes: eleven Paths to pick when building your deck, 80 Bushido, Kuji-Kiri, Ninjutsu and Taijutsu cards, and 12 dual cards.",
    },
    {
        date: "2026-10-19",
        genre: "jeu",
        fr: "L'affichage Épuré, sombre, devient celui d'ouverture pour tout le monde, avec un accueil aux couleurs bleues du jeu.",
        en: "The dark Clean display is now the opening display for everyone, with a home screen in the game's blue.",
    },
    {
        date: "2026-10-18",
        genre: "jeu",
        fr: "Sur ordinateur, les mises à jour ont leur propre page, classée par famille : les trois dernières de chacune, et un clic pour tout voir. L'accueil range ses tuiles en quatre rangées, avec une tuile Puzzle qui arrive bientôt.",
        en: "On computer, updates now have their own page, sorted by family: the three latest of each, and one click to see everything. The home screen lays its tiles out in four rows, with a Puzzle tile coming soon.",
    },
    {
        date: "2026-10-18",
        genre: "jeu",
        fr: "L'éditeur de deck se choisit son héros dans la page, avec une fenêtre de portraits et une recherche. Au choix du méchant, les boîtes et les cartes de scénario remplissent la place disponible, et les Défis et Weekly Challenges n'y sont plus proposés.",
        en: "The deck builder now picks its hero in the page, with a portrait window and a search. When choosing the villain, the boxes and scenario cards fill the space available, and Challenges and Weekly Challenges are no longer offered there.",
    },
    {
        date: "2026-10-18",
        genre: "jeu",
        fr: "À la mise en place et pendant ton tour, une recherche dans le deck ou la défausse s'ouvre en cliquant la pile concernée, qui s'allume avec ce qu'on y fait, au lieu d'une fenêtre qui surgit toute seule.",
        en: "During setup and your turn, a search in your deck or discard pile now opens by clicking the pile, which lights up with what you do there, instead of a window that pops up by itself.",
    },
    {
        date: "2026-10-18",
        genre: "correction",
        fr: "Sur une réaction, le bouton de refus nomme la capacité (« Ne pas utiliser la Réponse ») et non la carte, pour qu'on ne croie plus annuler sa mise en jeu. La fenêtre Cartes regardées ne s'ouvre plus pour une carte seulement connue (Récup'), la répartition des dégâts indirects n'affiche plus le texte de la carte qui la porte, et une ressource qui s'incline elle-même n'est plus proposée pour payer un coût qui exige de l'incliner (Nebula's Ship).",
        en: "On a reaction, the refuse button now names the ability (\"Do not use the Response\") rather than the card, so it no longer looks like cancelling the card being played. The Looked-at cards window no longer opens for a card that is merely known (Salvage), indirect damage assignment no longer shows the text of the card carrying it, and a resource that exhausts itself is no longer offered to pay a cost that requires exhausting it (Nebula's Ship).",
    },
    {
        date: "2026-10-18",
        genre: "coulisses",
        fr: "Les anciennes pages du moteur d'origine (crédits, éditeur de decks, liste des cartes, ancien plateau, rapport de bug) ne sont plus accessibles : elles renvoient à l'accueil.",
        en: "The old pages of the original engine (credits, deck editor, card list, old board, bug report) are no longer reachable: they send you back to the home page.",
    },
    {
        date: "2026-10-16",
        genre: "heros",
        fr: "La campagne fan-made Menace Skrull (de Kajislav) arrive en cinq scénarios : Skrull Empire, Super-Skrull, Paibok, Skrull Pantheon et Secret Invasion, avec sa zone de coopération et ses Élites. Hulkling et Lyja rejoignent le roster.",
        en: "The fan-made Skrull Menace campaign (by Kajislav) arrives in five scenarios: Skrull Empire, Super-Skrull, Paibok, Skrull Pantheon and Secret Invasion, with its cooperation zone and Elites. Hulkling and Lyja join the roster.",
    },
    {
        date: "2026-10-16",
        genre: "jeu",
        fr: "Importer un deck : en plus des liens MarvelCDB, les liens MC4DB et les fichiers OCTGN (.o8d). L'éditeur de deck a maintenant sa tuile sur l'accueil.",
        en: "Importing a deck: besides MarvelCDB links, MC4DB links and OCTGN files (.o8d) now work. The deck builder now has its own tile on the home screen.",
    },
    {
        date: "2026-10-16",
        genre: "correction",
        fr: "Plusieurs corrections d'affichage sur iPhone, et un joueur éliminé en pleine phase ne reçoit plus de carte rencontre.",
        en: "Several display fixes on iPhone, and a player eliminated mid-phase no longer receives an encounter card.",
    },
    {
        date: "2026-10-12",
        genre: "correction",
        fr: "Les cartes Team-Up (par exemple Ne vois et n'entends aucun mal) se jouent sans devoir désigner les deux personnages. Déferlement : les dégâts en trop sur un sbire vont directement au méchant, sans question.",
        en: "Team-Up cards (for example See No Evil, Hear No Evil) are played without having to pick the two characters. Overkill: excess damage on a minion goes straight to the villain, with no question.",
    },
    {
        date: "2026-10-12",
        genre: "correction",
        fr: "En mode « D'un coup », la phase du méchant ne reste plus bloquée quand le jeu te pose une question (défendre, réagir). Swarmed by Rats ne se paie plus qu'avec deux cartes de ta main, et n'est plus proposé si tu en as moins. Quelques cartes ne proposent plus de mauvaises cibles (Mister Fantastic, cartes Determination).",
        en: "In \"All at once\" mode, the villain phase no longer gets stuck when the game asks you something (defend, respond). Swarmed by Rats is only paid with two cards from your hand, and is no longer offered if you have fewer. A few cards no longer offer wrong targets (Mister Fantastic, Determination cards).",
    },
    {
        date: "2026-10-12",
        genre: "correction",
        fr: "Le bouton « Fin de phase » est maintenant jaune et plus grand. Pendant la phase du méchant, les dégâts subis par un allié qui défend s'affichent sur lui, et le nom de la carte qui donne un Renfort est traduit. Sur l'accueil, un merci à Irefrixs, auteur du moteur d'origine.",
        en: "The \"End phase\" button is now yellow and larger. During the villain phase, damage taken by a defending ally shows on that ally, and the name of the card giving a Surge is translated. On the home screen, a thank-you to Irefrixs, author of the original engine.",
    },
    {
        date: "2026-10-11",
        genre: "correction",
        fr: "Quand tu as déjà le maximum d'exemplaires d'une carte en jeu, le jeu te le dit au lieu de « Aucune cible possible ». En multi, au début de la phase du méchant, les autres joueurs voient que l'hôte est en train de choisir.",
        en: "When you already have the maximum number of copies of a card in play, the game now says so instead of \"No legal target\". In multiplayer, at the start of the villain phase, the other players see that the host is choosing.",
    },
    {
        date: "2026-10-11",
        genre: "correction",
        fr: "La phase du méchant « Étape par étape » reprend sa présentation habituelle. Et une carte jouable ne s'affiche plus « Injouable » à cause d'une autre carte (vu sur Réponse Immédiate).",
        en: "The \"Step by step\" villain phase is back to its usual look. And a playable card no longer shows \"Unplayable\" because of another card (seen on Rapid Response).",
    },
    {
        date: "2026-10-11",
        genre: "correction",
        fr: "Écran de fin : sur l'onglet Stats, l'image DEFEAT ou VICTORY ne cache plus les onglets ni le bas du bilan. Tu peux de nouveau revenir sur Résultat pour quitter.",
        en: "End screen: on the Stats tab, the DEFEAT or VICTORY image no longer hides the tabs or the bottom of the summary. You can go back to Result to leave again.",
    },
    {
        date: "2026-10-11",
        genre: "correction",
        fr: "Daredevil revu carte par carte. Focus the Senses déplace aussi tes améliorations Sens, Deposition ne t'oblige plus à jouer un Sens, The Man Without Fear et Sensory Overload blessent Daredevil et plus un allié, et le Stolen Sai de Bullseye rend bien ses attaques perçantes.",
        en: "Daredevil reviewed card by card. Focus the Senses now also moves your Sense upgrades, Deposition no longer forces you to play a Sense, The Man Without Fear and Sensory Overload damage Daredevil instead of an ally, and Bullseye's Stolen Sai now makes attacks piercing.",
    },
    {
        date: "2026-10-11",
        genre: "correction",
        fr: "MaGog : avec Crime Scene Investigation en jeu, Melee in the Mojo-seum ne peut plus retirer sa menace, donc la manigance se complète et la partie est perdue (ruling officiel de FFG). Power Struggle porte une icône Amplify.",
        en: "MaGog: with Crime Scene Investigation in play, Melee in the Mojo-seum can no longer remove its threat, so the scheme completes and the game is lost (official FFG ruling). Power Struggle carries an Amplify icon.",
    },
    {
        date: "2026-10-11",
        genre: "correction",
        fr: "Sonic Boom et les choix des cartes rencontre suivent le Rules Reference 1.8 : tu peux choisir de dépenser des ressources même si tu ne peux pas tout payer, et tu paies ce que tu as. Avant, la carte ne faisait parfois rien. Quand une seule option reste possible, elle est surlignée et le jeu explique pourquoi.",
        en: "Sonic Boom and other encounter card choices now follow Rules Reference 1.8: you can choose to spend resources even if you cannot pay them all, and you pay what you have. Before, the card sometimes did nothing. When only one option is possible, it is highlighted and the game tells you why.",
    },
    {
        date: "2026-10-11",
        genre: "jeu",
        fr: "Tu peux supprimer un deck sauvegardé (bouton « Supprimer » dans la liste des decks). Et coller le lien d'un deck MarvelCDB ne risque plus d'importer une autre liste portant le même numéro.",
        en: "You can delete a saved deck (Delete button in the deck list). And pasting a MarvelCDB deck link no longer risks importing a different list with the same number.",
    },
    {
        date: "2026-10-10",
        genre: "jeu",
        fr: "Phase du méchant « Sur la table » refaite. Une bulle déplaçable porte les onglets de la phase, le calcul en pastilles et un gros bouton Suivant (touche Espace). Elle s'efface quand tu survoles une carte. La carte qui agit s'allume, la carte touchée montre sa jauge qui bouge et le nombre qui s'envole. Les boosts se retournent un par clic, la question de défense se pose dans la bulle, et le bilan se lit sur deux colonnes.",
        en: "The On the table villain phase is redone. A movable bubble holds the phase tabs, the calculation as badges and a big Next button (Space key). It fades when you hover a card. The acting card lights up, the card that is hit shows its gauge moving and the number flying off. Boosts flip one click at a time, the defense question is asked in the bubble, and the summary reads in two columns.",
    },
    {
        date: "2026-10-10",
        genre: "correction",
        fr: "Storm : Torrential Rain permet de répartir ses 3 menaces entre plusieurs manigances, et Flash Freeze donne aussi -3 ATQ aux sbires qui s'engagent avec toi plus tard dans la phase.",
        en: "Storm: Torrential Rain lets you split its 3 threat among several schemes, and Flash Freeze also gives -3 ATK to minions that engage you later in the phase.",
    },
    {
        date: "2026-10-10",
        genre: "correction",
        fr: "Luke Cage revu carte par carte. Power Man fait bien piocher, le Bracelet métallique protège avant que le Tenace ne parte, Jessica Jones gagne +1 Contre par Tenace et Misty Knight perd son bonus avec son Tenace. Cruisin' for a Bruisin', Take a Stand, Black Belt, Augmented Jaws et Sidewinder fonctionnent comme imprimé.",
        en: "Luke Cage reviewed card by card. Power Man now draws, Metal Bracer reduces damage before a tough card is lost, Jessica Jones gets +1 THW per tough card and Misty Knight loses her bonus with her tough card. Cruisin' for a Bruisin', Take a Stand, Black Belt, Augmented Jaws and Sidewinder now work as printed.",
    },
    {
        date: "2026-10-19",
        genre: "jeu",
        fr: "La phase du méchant se choisit entre trois façons : « Guidée », « Plateau animé » et « Accéléré ». Les anciennes présentations « Étape par étape » passent sur « Guidée ». La fenêtre de choix se pose une dernière fois à chacun, le choix déjà fait y est conservé.",
        en: "The villain phase now comes in three ways: “Guided”, “Animated Board” and “Fast Forward”. The former “Step by step” presentations move to “Guided”. The choice window appears one last time for everyone, with the choice already made kept in it.",
    },
    {
        date: "2026-10-10",
        genre: "jeu",
        fr: "Quand une action te fait choisir des cartes hors de la table, comme le Contrôle climatique de Storm ou une recherche dans ton deck, une seule fenêtre s'ouvre avec les cartes. Tu touches celle que tu veux, puis Valider.",
        en: "When an action makes you choose cards that are not on the table, like Storm's Weather Control or a search in your deck, a single window opens with the cards. Tap the one you want, then Confirm.",
    },
    {
        date: "2026-10-10",
        genre: "jeu",
        fr: "La phase du méchant n'a plus qu'une présentation « Étape par étape », celle qui s'appelait Bis. La mise en place se montre aussi carte par carte, manigances d'abord, puis les méchants.",
        en: "The villain phase now has a single Step by step presentation, the one called Bis. Setup is also shown card by card, main schemes first, then the villains.",
    },
    {
        date: "2026-10-10",
        genre: "correction",
        fr: "Les statistiques de fin de partie comptent aussi le coup qui gagne ou perd la partie, et les dégâts subis par un allié vaincu.",
        en: "End-of-game statistics now also count the blow that wins or loses the game, and the damage taken by a defeated ally.",
    },
    {
        date: "2026-10-10",
        genre: "jeu",
        fr: "L'écran de fin de partie a un onglet Stats : tours, temps, dégâts infligés, menace retirée, puis pour chaque héros les dégâts au méchant et aux sbires, la menace retirée, les dégâts évités et subis, les attaques défendues, les cartes jouées et les ressources dépensées. Il montre aussi tes 3 cartes les plus jouées et les 3 cartes piochées mais peu jouées. En multijoueur, les héros sont côte à côte dans un tableau.",
        en: "The end-of-game screen has a Stats tab: turns, time, damage dealt, threat removed, then for each hero damage to the villain and minions, threat removed, damage prevented and taken, attacks defended, cards played and resources spent. It also shows your 3 most played cards and the 3 cards you drew but rarely played. In multiplayer, heroes sit side by side in a table.",
    },
    {
        date: "2026-10-10",
        genre: "correction",
        fr: "La mise en place suit l'ordre du livret : tu vois la manigance principale avant tout ce qu'elle met en jeu. Dans Tower Defense, les deux manigances apparaissent avant le choix de dégâts de l'Assaillant de l'Ordre Noir.",
        en: "Setup follows the rulebook order: you see the main scheme before anything it puts into play. In The Tower Defense, both main schemes now appear before the Black Order Besieger damage choice.",
    },
    {
        date: "2026-10-10",
        genre: "jeu",
        fr: "Sur ordinateur, une action commencée s'annule d'un coup : la touche Échap ou la petite croix de la question remet la partie avant le choix de la carte, même après le paiement.",
        en: "On a computer, an action you started can be cancelled in one go: Esc or the small cross on the question puts the game back to before you chose the card, even after paying.",
    },
    {
        date: "2026-10-10",
        genre: "jeu",
        fr: "Sur téléphone, le plateau se joue mieux : touche une carte puis « Jouer », un bandeau « Annuler » après chaque action, la taille du texte, les vibrations et le verrou portrait dans les réglages, et l'écran reste allumé pendant la partie.",
        en: "Better board on phones: tap a card then “Play”, an “Undo” banner after each action, text size, vibrations and portrait lock in the settings, and the screen stays on during the game.",
    },
    {
        date: "2026-10-10",
        genre: "correction",
        fr: "Les cartes Starting se prennent au choix : le jeu te demande avant la pioche si tu veux la mettre dans ta main de départ, et l'éditeur refuse un deck qui en compte plus d'une.",
        en: "Starting cards are now optional: before you draw, the game asks whether to put it in your opening hand, and the deck editor rejects a deck with more than one.",
    },
    {
        date: "2026-10-10",
        genre: "correction",
        fr: "Phase du méchant plus lisible : quand une carte en annule une autre et en révèle une nouvelle (Stepford Cuckoos, Black Widow) ou qu'un Renfort arrive, toute la chaîne s'affiche, carte annulée comprise.",
        en: "Clearer villain phase: when a card cancels another and reveals a new one (Stepford Cuckoos, Black Widow) or a Surge comes in, the whole chain is shown, canceled card included.",
    },
    {
        date: "2026-10-10",
        genre: "jeu",
        fr: "Les autres pages suivent sur téléphone. L'accueil s'ouvre sur un gros bouton « Jouer », la galerie a ses filtres en pastilles et trois colonnes, le livre de campagne se tourne du doigt. Connexion, statistiques et administration se lisent en cartes, et le bouton Retour referme ce qui est ouvert.",
        en: "The other pages follow on phones. The home screen opens on a big “Play” button, the gallery has tap-to-pick filters and three columns, and the campaign book turns with a swipe. Sign-in, statistics and admin read as cards, and the Back button closes whatever is open.",
    },
    {
        date: "2026-10-09",
        genre: "jeu",
        fr: "La préparation de partie est pensée pour le téléphone : en-tête avec menu, étapes cliquables, héros en bandeau et grille à trois colonnes. Touche un héros pour le voir, puis « Choisir ». Le bouton Retour de ton téléphone revient à l'étape d'avant.",
        en: "Game setup is now designed for phones: a slim header with a menu, tappable steps, the hero in a banner and a three-column grid. Tap a hero to preview it, then “Choose”. Your phone's Back button returns to the previous step.",
    },
    {
        date: "2026-10-09",
        genre: "jeu",
        fr: "L'éditeur de deck est refait : filtres à gauche, cartes au centre, ton deck toujours visible à droite avec l'aperçu, la courbe des coûts et sa validité. Nouveau : un simulateur de pioche, des statistiques, des filtres par trait, pack et caractéristiques, et une recherche courte comme « t:avenger c:2 ».",
        en: "The deck builder is redone: filters on the left, cards in the middle, your deck always visible on the right with the preview, the cost curve and whether it is valid. New: a draw simulator, statistics, filters by trait, pack and stats, and a short search syntax such as “t:avenger c:2”.",
    },
    {
        date: "2026-10-09",
        genre: "jeu",
        fr: "L'écran de l'invité reprend l'habillage de l'assistant : héros à gauche, grille à droite, puis choix du deck. Une fois prêt, tu vois l'équipe se former (qui est assis où, et contre quel méchant) en attendant le lancement.",
        en: "The guest screen now matches the setup wizard: hero on the left, grid on the right, then deck choice. Once ready, you watch the team take shape (who sits where, and against which villain) while waiting for the host to start.",
    },
    {
        date: "2026-10-09",
        genre: "jeu",
        fr: "L'affichage sobre s'applique maintenant à toutes les pages (préparation, campagne, éditeur de deck, galerie…) : plus de trame BD ni d'ombres colorées, des gris neutres, et l'illustration du héros adoucie.",
        en: "Muted display now applies to every page (setup, campaign, deck builder, gallery…): no comic halftone or coloured shadows, neutral greys, and a softened hero illustration.",
    },
    {
        date: "2026-10-09",
        genre: "jeu",
        fr: "Préparation de partie : la scène du héros prend moins de place et la grille s'élargit, avec des vignettes plus grandes. On voit bien plus de héros d'un coup, et les étapes Decks et Méchant profitent de la même place.",
        en: "Game setup: the hero scene takes less room and the grid is wider, with bigger tiles. You see many more heroes at once, and the Decks and Villain steps get the same extra space.",
    },
    {
        date: "2026-10-09",
        genre: "jeu",
        fr: "En-tête plus fin, sur une seule ligne : les outils (Reprendre, Revoir, Stats, Signaler un bug, Documents…) deviennent des icônes avec leur nom au survol, et les étapes de la préparation sont numérotées.",
        en: "Slimmer, single-line header: tools (Resume, Replay, Stats, Report a bug, Documents…) become icons with their name on hover, and the setup steps are numbered.",
    },
    {
        date: "2026-10-09",
        genre: "jeu",
        fr: "La traduction posée sur les cartes s'affiche aussi sur les grandes cartes au centre (mise en place, cartes révélées) et sur les arts alternatifs des héros, y compris dans la fenêtre de choix de l'art. Le son de survol des boutons est plus discret.",
        en: "Translations laid over cards now also show on the big cards in the middle (setup, revealed cards) and on alternate hero art, including in the art picker. The button hover sound is quieter.",
    },
    {
        date: "2026-10-09",
        genre: "jeu",
        fr: "Écran de campagne : les pages du livret s'ouvrent comme un livre, en double page qu'on tourne avec les flèches (ou le clavier, ou d'un glissement du doigt sur téléphone). Le bouton pour lancer le scénario reste visible sans défiler.",
        en: "Campaign screen: booklet pages now open like a book, in a two-page spread turned with the arrows (or the keyboard, or a swipe on a phone). The button to start the scenario stays visible without scrolling.",
    },
    {
        date: "2026-10-09",
        genre: "jeu",
        fr: "Campagne Hunting Season : les pages du livret s'affichent à l'écran de campagne, en français quand le jeu est en français. La traduction posée sur les cartes couvre aussi le verso et les manigances.",
        en: "Hunting Season campaign: the booklet pages now show on the campaign screen, in French when the game is in French. Translations laid over cards now also cover the back side and schemes.",
    },
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
