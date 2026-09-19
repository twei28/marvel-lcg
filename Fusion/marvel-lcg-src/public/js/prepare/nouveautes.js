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
