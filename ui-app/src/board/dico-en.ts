// dico-en.ts — dictionnaire français -> anglais du plateau.
//
// Rempli à la main, écran par écran. Les clés sont les textes FRANÇAIS exacts
// passés à t() (voir langue.ts) ; les valeurs reprennent le vocabulaire
// OFFICIEL anglais du jeu (Villain, Thwart, Scheme, Tough/Stunned/Confused,
// Surge, Overkill, Piercing, victory display, encounter deck, boost...).
// Une clé absente laisse le texte en français : rien ne casse.

export const DICO_EN_BASE: Record<string, string> = {
  // ---- Partagé (boutons, libellés courts) ----
  'autres': 'others',
  'Fermer': 'Close',
  'Annuler': 'Cancel',
  'Confirmer': 'Confirm',
  'Passer': 'Pass',
  'Retour': 'Back',
  'Abandonner': 'Cancel',
  'Continuer': 'Continue',
  'Carte': 'Card',
  'carte': 'card',
  'cartes': 'cards',
  'Cible': 'Target',
  'Cibles': 'Targets',
  'Menace': 'Threat',
  'menace': 'threat',
  'PV': 'HP',
  'Sauver': 'Save',
  'Charger': 'Load',
  'Exporter': 'Export',
  'Vide': 'Empty',
  'Fichier': 'File',
  'Joueur': 'Player',

  // ---- board.tsx : barre du haut, sauvegardes, relecture, connexion, fin ----
  'Cartes regardées': 'Cards being looked at',
  'Cibles possibles': 'Possible targets',
  'Cibles possibles :': 'Possible targets:',
  'Mode d’affichage des actions': 'Action display mode',
  'Détaillé': 'Detailed',
  'Emplacements de sauvegarde, chargement, export': 'Save slots, loading, export',
  'Charger la sauvegarde': 'Load save',
  'La partie en cours sera remplacée.': 'The current game will be replaced.',
  'Télécharger cette partie en .json': 'Download this game as .json',
  'Contrôles de relecture': 'Replay controls',
  'Relecture': 'Replay',
  'Retour au début': 'Back to the start',
  'Pas suivant': 'Next step',
  'Aller à la fin': 'Go to the end',
  'Connexion perdue': 'Connection lost',
  'nouvel essai dans': 'retrying in',
  'reconnexion...': 'reconnecting...',
  'essai': 'attempt',
  'Reconnecter maintenant': 'Reconnect now',
  'Chargement...': 'Loading...',
  'Aucune partie derrière cette vue : rien à jouer. Retire « ?etat= » de l’adresse pour revenir à la partie.':
    'Nothing is being played behind this view. Remove « ?etat= » from the address to go back to the game.',
  'Victoire': 'Victory',
  'Défaite': 'Defeat',
  'Les héros l’emportent !': 'The heroes win!',
  'Les héros sont vaincus': 'The heroes are defeated',
  'Retour au menu': 'Back to the menu',
  'Annuler la dernière action': 'Undo the last action',
  'Animations activées — cliquer pour couper': 'Animations on — click to turn them off',
  'Animations coupées — cliquer pour activer': 'Animations off — click to turn them on',
  'Sons activés — cliquer pour couper': 'Sounds on — click to turn them off',
  'Sons coupés — cliquer pour activer': 'Sounds off — click to turn them on',
  'Sons': 'Sounds',
  'Présentation des cartes révélées coupée — cliquer pour un affichage court':
    'Revealed cards presentation off — click for a short display',
  'Cartes révélées montrées 2,6 s — cliquer pour un affichage long':
    'Revealed cards shown for 2.6 s — click for a long display',
  'Cartes révélées montrées 5 s — cliquer pour couper':
    'Revealed cards shown for 5 s — click to turn it off',
  'Révélé': 'Revealed',
  'Révélé+': 'Revealed+',
  'Quel héros est affiché (plateau et main)': 'Which hero is displayed (board and hand)',
  'Vue': 'View',
  'Suivre celui qui doit agir': 'Follow whoever must act',
  'Revenir au menu principal': 'Back to the main menu',
  'Plus rien n’est jouable — termine ton tour': 'Nothing left to play — end your turn',
  'Terminer ton tour': 'End your turn',
  'Fin du tour': 'End turn',

  // ---- board/Board.tsx : entête, stades, aperçu ----
  'Stades': 'Stages',
  'Voir les': 'See the',
  'stades': 'stages',
  'Autre face': 'Other side',
  'entrée(s) inattendue(s)': 'unexpected entry(ies)',

  // ---- board/zones.ts : titres de zones ----
  'Deck Rencontre': 'Encounter deck',
  'Défausse Rencontre': 'Encounter discard',
  'Méchant': 'Villain',
  'Manigance principale': 'Main scheme',
  'Manigances annexes': 'Side schemes',
  'Alliés, sbires et environnement': 'Allies, minions and environment',
  'Héros et soutiens': 'Hero and supports',
  'Deck du héros': 'Hero deck',
  'Pile de défausse': 'Discard pile',
  'Mises de côté / autres piles': 'Set aside / other piles',
  'Pile de victoire': 'Victory display',
  'Retirées de la partie': 'Removed from the game',
  'Némésis': 'Nemesis',
  'Ta main': 'Your hand',
  'Ta réserve': 'Your reserve',
  'Deck spécial': 'Special deck',
  'Stades du Méchant': 'Villain stages',
  'Méchants à venir': 'Upcoming villains',

  // ---- board/card-model.ts ----
  'Carte face cachée': 'Facedown card',

  // ---- components/ScanCard.tsx : types de cartes et badges ----
  'Héros': 'Hero',
  'Allié': 'Ally',
  'Sbire': 'Minion',
  'Manigance annexe': 'Side scheme',
  'manigance annexe': 'side scheme',
  'Attachement': 'Attachment',
  'Traîtrise': 'Treachery',
  'Alter ego': 'Alter-Ego',
  'Soutien': 'Support',
  'Amélioration': 'Upgrade',
  'Événement': 'Event',
  'Ressource': 'Resource',
  'Environnement': 'Environment',
  'État': 'Status',
  'En attente': 'Waiting',
  'Actif': 'Active',
  'Accroché': 'Latched',
  'Mordu': 'Bitten',
  'Défausse': 'Discard',
  'cartes dans la pile': 'cards in the pile',
  'Dépensée': 'Spent',
  'fois': 'time(s)',
  'Points de vie :': 'Hit points:',
  'Menace :': 'Threat:',
  'MEN': 'THR',
  'Compteurs': 'Counters',
  'Appartient à': 'Belongs to',

  // ---- board/MenuActionsCarte.tsx ----
  'Attaque': 'Attack',
  'Contre': 'Thwart',
  'Récupération': 'Recovery',
  'Défense': 'Defense',
  'Manigance': 'Scheme',
  'cible': 'target',
  'ennemi': 'enemy',
  'manigance': 'scheme',
  'personnage': 'character',
  'possibles': 'possible',
  'Cible :': 'Target:',
  'Crise': 'Crisis',
  'Aléa': 'Hazard',
  'Amplification': 'Amplify',
  'accélération': 'acceleration',
  'MNG': 'SCH',
  'ATQ': 'ATK',
  'CTR': 'THW',
  'sur': 'on',
  'Bloquée par': 'Blocked by',
  "Pas légale dans l'état actuel de la partie": 'Not legal in the current game state',
  'Aucune menace à retirer pour le moment': 'No threat to remove right now',
  "Pas une cible légale dans l'état actuel de la partie":
    'Not a legal target in the current game state',
  'Aucune action de contre utilisable pour le moment': 'No thwart action usable right now',
  "Aucune action d'attaque utilisable pour le moment": 'No attack action usable right now',
  'Aucun personnage redressé ne peut contrer pour le moment (mauvaise phase, incliné, ou désorienté)':
    'No readied character can thwart right now (wrong phase, exhausted, or confused)',
  'Aucun personnage redressé ne peut attaquer pour le moment (mauvaise phase, incliné, sonné, ou non engagé)':
    'No readied character can attack right now (wrong phase, exhausted, stunned, or not engaged)',
  "Pas disponible dans l'état actuel de la partie": 'Not available in the current game state',
  'Coût': 'Cost',
  'Actions générales': 'General actions',
  'Actions de': 'Actions of',
  'Aucune action': 'No action',
  'Peut être contrée': 'Can be thwarted',
  'Ne peut pas être contrée': 'Cannot be thwarted',
  'Peut être attaqué': 'Can be attacked',
  'Ne peut pas être attaqué': 'Cannot be attacked',
  'Aucune action disponible': 'No action available',
  'Manigances pas légales maintenant': 'Schemes not legal right now',
  'Pas légal maintenant': 'Not legal right now',

  // ---- board/CoucheCoach.tsx + lecons.ts : mode Découverte ----
  'Coach': 'Coach',
  'Leçon': 'Lesson',
  'Bien joué !': 'Well done!',
  'Replier': 'Collapse',
  'Passer cette leçon': 'Skip this lesson',
  'J’ai compris': 'Got it',
  'Quitter le tutoriel': 'Quit the tutorial',
  'Garde ta main de départ': 'Keep your opening hand',
  'Le jeu commence par un « mulligan » : tu peux défausser autant de cartes que tu veux de ta main, et en repiocher le même nombre. Pour cette partie guidée, garde tout, et surtout « Coup de pied volant » : c’est la carte que le tutoriel te fera jouer. Valide sans rien sélectionner.':
    'The game opens with a "mulligan": you may discard as many cards from your hand as you like, then draw back the same number. For this guided game, keep everything, and above all "Swinging Web Kick": that is the card the tutorial will have you play. Confirm without selecting anything.',
  'Deviens Spider-Man': 'Become Spider-Man',
  'Tu commences en Peter Parker, ton identité civile. En civil on récupère et on prépare, mais on ne se bat pas. Clique sur ta carte d’identité, puis choisis de changer de forme.':
    'You start as Peter Parker, your civilian identity. In alter-ego you recover and prepare, but you do not fight. Click your identity card, then choose to change form.',
  'Joue ta première carte': 'Play your first card',
  'Joue « Coup de pied volant ». Pour la payer, tu défausses d’autres cartes de ta main : chaque carte vaut une ressource, quelle qu’elle soit. Tout se paie comme ça dans ce jeu.':
    'Play "Swinging Web Kick". To pay for it you discard other cards from your hand: every card is worth one resource, whichever it is. Everything is paid for that way in this game.',
  'Frappe Rhino': 'Hit Rhino',
  'Ton héros peut attaquer une fois par tour. Clique sur Spider-Man, choisis Attaque, puis Rhino. Ta carte s’incline : c’est le signe qu’elle a déjà servi ce tour-ci.':
    'Your hero can attack once per turn. Click Spider-Man, choose Attack, then Rhino. Your card exhausts: that is the sign it has already been used this turn.',
  'Retire 2 menaces': 'Remove 2 threat',
  'La manigance principale monte à chaque tour. Si elle se remplit, la partie est perdue, même si Rhino est au plus mal. Contre-la pour faire redescendre la menace.':
    'The main scheme rises every turn. If it fills up the game is lost, even if Rhino is nearly beaten. Thwart it to bring the threat back down.',
  'Termine ton tour': 'End your turn',
  'Regarde bien ce qui suit : Rhino t’attaque, la manigance monte, et une carte Rencontre t’est distribuée. C’est la phase du méchant, et elle arrive à chaque tour.':
    'Watch what follows: Rhino attacks you, the scheme rises, and an encounter card is dealt to you. That is the villain phase, and it comes every turn.',
  'Appelle un allié': 'Call an ally',
  'Les alliés attaquent et contrent à ta place, sans t’incliner. Ils encaissent un dégât chaque fois qu’ils agissent : ils sont là pour être dépensés, pas pour être gardés.':
    'Allies attack and thwart in your place, without exhausting you. They take a damage each time they act: they are there to be spent, not saved.',
  'Reprends ton souffle': 'Catch your breath',
  'Repasse en Peter Parker et récupère des points de vie. Tu ne pourras plus attaquer ce tour-ci, mais Rhino ne t’attaquera pas non plus : il ira comploter à la place.':
    'Switch back to Peter Parker and recover hit points. You will not be able to attack this turn, but Rhino will not attack you either: he will scheme instead.',
  'Lis une carte': 'Read a card',
  'Survole n’importe quelle carte : elle s’agrandit sur le côté, avec ses mots-clés expliqués. Garde, Renfort, Déferlement : tout y est défini, tu n’as rien à retenir par cœur.':
    'Hover any card: it grows on the side, with its keywords explained. Guard, Surge, Overkill: everything is defined there, you have nothing to memorise.',
  'Le panneau ⚙': 'The ⚙ panel',
  'En haut à droite : animations, sons, musique, ambiance, succès. Tout est débrayable, rien ne t’est imposé.':
    'Top right: animations, sounds, music, ambience, achievements. Everything can be turned off, nothing is forced on you.',
  'Annuler une erreur': 'Undo a mistake',
  'La touche U annule le dernier coup. Tu peux essayer sans crainte : rien n’est définitif tant que tu n’as pas terminé ton tour.':
    'The U key undoes the last move. You can experiment freely: nothing is final until you end your turn.',
  'L’historique': 'The history',
  'En bas, tout ce qui s’est passé est rejoué ligne à ligne. Quand tu ne comprends pas pourquoi quelque chose est arrivé, la réponse est là.':
    'At the bottom, everything that happened is replayed line by line. When you do not understand why something happened, the answer is there.',

  // ---- board/interaction.ts : assistant pas-à-pas ----
  'Choisir une action': 'Choose an action',
  'Choisir les cartes du mulligan': 'Choose the mulligan cards',
  'à défausser puis repiocher · tu peux n’en choisir aucune': 'to discard then redraw · you may pick none',
  'Choisir la seule cible': 'Choose the only target',
  'Choisir la cible': 'Choose the target',
  'Payer le coût': 'Pay the cost',
  'Prêt à valider': 'Ready to confirm',
  'sélectionnée(s) · nombre au choix': 'selected · any number',
  'requise(s)': 'required',
  'possible(s)': 'possible',
  'Choisir jusqu’à': 'Choose up to',
  cibles: 'targets',
  'attribuée(s)': 'assigned',
  minimum: 'minimum',
  'carte(s) ciblable(s)': 'targetable card(s)',
  'Une même carte peut être choisie plusieurs fois (1 clic = 1 attribution)':
    'The same card can be chosen several times (1 click = 1 assignment)',
  'Choisis les cibles': 'Choose the targets',
  'payé': 'paid',
  'Appuyer sur Valider quand tout est correct': 'Press Confirm when everything is right',

  // ---- board/BarreAction.tsx ----
  'pile de boost': 'boost pile',
  'deck de rencontre': 'encounter deck',
  'deck du joueur': 'player deck',
  'une carte face cachée': 'a facedown card',
  'Connexion à la partie perdue.': 'Connection to the game lost.',
  'La partie ne peut pas avancer tant que ce plateau n’accuse pas réception. Reconnexion en cours.':
    'The game cannot move forward until this board acknowledges the render. Reconnecting.',
  'En attente du jeu.': 'Waiting for the game.',
  'Rien à décider pour le moment.': 'Nothing to decide right now.',
  'Étape 1 - choisis la cible': 'Step 1 - choose the target',
  'Étape 2 - paie en cliquant les cartes surlignées ou un générateur de ressources':
    'Step 2 - pay by clicking the highlighted cards or a resource generator',
  'Dernière étape - confirme': 'Last step - confirm',
  'Cette carte': 'This card',
  'aucune action': 'no action',
  'choisis une action': 'choose an action',
  'Clique une carte pour agir, ou choisis ci-dessous': 'Click a card to act, or choose below',
  'Légende des surbrillances': 'Highlight legend',
  'Jouable': 'Playable',
  'Choisie': 'Chosen',
  'À toi de jouer': 'Your move',
  'Choisis une action': 'Choose an action',
  'Coût payé': 'Cost paid',

  // ---- board/AssistantAction.tsx ----
  'coût': 'cost',
  'choisir la cible': 'choose the target',
  'payer le coût': 'pay the cost',
  'confirmer': 'confirm',
  'Choisis la cible': 'Choose the target',
  'Paie': 'Pay',
  'Dépense autant de ressources que tu veux, puis confirme':
    'Spend as many resources as you like, then confirm',
  'Paie le coût': 'Pay the cost',
  'Coût à payer': 'Cost to pay',

  // ---- board/DemandeCentrale.tsx ----
  'Choisis une réponse': 'Choose a response',
  'Décision': 'Decision',
  'choisis une option': 'choose an option',
  'Événement de jeu': 'Game event',

  // ---- board/HistoriquePartie.tsx ----
  'joué': 'played',
  'défaussé': 'discarded',
  'révélée': 'revealed',
  'subit': 'takes',
  'dégât(s)': 'damage',
  'PV restants': 'HP left',
  'soigne': 'heals',
  'menace retirée de': 'threat removed from',
  'menace restante': 'threat left',
  'gagne': 'gains',
  'Dégâts': 'Damage',
  'Soin': 'Heal',
  // Attribution des entrees chiffrees (board/causalite.ts).
  'par': 'by',
  'via': 'via',
  'Historique de la partie': 'Game history',
  // Deroule detaille de la phase du mechant.
  'Menace sur la manigance principale': 'Threat on the main scheme',
  // Pluriels du deroule : le francais accorde, l'anglais garde le meme mot.
  // ('menace' et 'dégâts' sont deja definis ailleurs dans ce fichier.)
  'menaces': 'threat',
  'dégât': 'damage',
  // Cle a trous : « sur » seul se traduit deja par « on » plus haut, et
  // « 1 on 3 » ne veut rien dire.
  '%1 sur %2': '%1 of %2',
  'complote contre': 'schemes against',
  // Les DEUX TEMPS d'une activation. Le premier est au futur proche : c'est
  // l'intention, la fenetre ou le joueur peut encore defendre ou repondre.
  'va attaquer': 'is about to attack',
  'va comploter contre': 'is about to scheme against',
  'dégât annoncé': 'damage announced',
  'dégâts annoncés': 'damage announced',
  'menace annoncée': 'threat announced',
  'menaces annoncées': 'threat announced',
  'tu peux défendre ou répondre': 'you can defend or respond',
  'L\'attaque n\'a pas lieu.': 'The attack does not happen.',
  'La manigance n\'a pas lieu.': 'The scheme does not happen.',
  'Point 1 : chaque joueur ajoute 1 menace à la manigance principale.':
    'Step 1: each player adds 1 threat to the main scheme.',
  'Point 2 : chaque ennemi s\'active contre le héros engagé avec lui.':
    'Step 2: each enemy activates against the hero engaged with it.',
  'Point 3 : chaque joueur reçoit une carte rencontre, face cachée.':
    'Step 3: each player is dealt an encounter card, facedown.',
  'Point 4 : chaque joueur révèle sa carte rencontre et en applique l\'effet.':
    'Step 4: each player reveals their encounter card and resolves it.',
  // Titre d'une etape de distribution : « Colossus reçoit sa carte rencontre ».
  // La carte est face cachee : on ne la nomme pas.
  'reçoit sa carte rencontre': 'is dealt an encounter card',
  'Carte rencontre distribuée': 'Encounter card dealt',
  // Le mode Heroique en distribue plusieurs par joueur : « Colossus reçoit
  // 2 cartes rencontre ».
  'reçoit': 'is dealt',
  'cartes rencontre': 'encounter cards',
  'cartes rencontre distribuées': 'encounter cards dealt',
  // Cartouche du deroule (DeroulePhase.tsx). 'Menace', 'Méchant' (zones.ts) et
  // 'Phase du méchant' sont deja definis plus haut, pour le bilan de fin de
  // phase et le splash de tour.
  'Sbires': 'Minions',
  'Distribution': 'Dealing',
  'Révélation': 'Reveal',
  // Titre d'une etape de revelation : « Colossus révèle Bombe à retardement ».
  'révèle': 'reveals',
  'Précédent': 'Previous',
  'Suivant': 'Next',
  'La suite arrive…': 'More coming…',
  // Multijoueur : le moteur n'avance qu'une fois TOUS les clients a jour, et
  // il n'interroge qu'un joueur a la fois. Dire lequel vaut mieux qu'un
  // plateau fige et muet (voir attente-table.ts).
  'En attente de %1': 'Waiting for %1',
  'En attente d\'un autre joueur': 'Waiting for another player',
  // Le filet anti-blocage va relacher la phase : on le dit avant, pour qu'elle
  // ne reparte pas toute seule sans explication.
  'La phase reprend dans %1 s': 'The phase resumes in %1 s',
  // Le cartouche replie devant une question du moteur : c'est le joueur qu'on
  // attend, pas le moteur.
  'Le moteur attend ta réponse': 'The game is waiting for your answer',
  'la règle': 'the rule',
  // Bilan de fin de phase, derniere etape du cartouche. ('À toi de jouer' est
  // deja defini plus haut, pour l'assistant d'action.)
  'Fin de la phase du méchant': 'End of the villain phase',
  'a pris': 'took',
  'a gagné': 'gained',
  'Aucun dégât, aucune menace.': 'No damage, no threat.',
  // Un heros tombe : le deroule s'arrete net sur cette etape.
  // ('Continuer' est deja defini plus haut, pour la demande centrale.)
  '%1 est vaincu': '%1 is defeated',
  'La phase s\'arrête ici.': 'The phase stops here.',
  // Tchat sur la table (PanneauSalon).
  'Tchat': 'Chat',
  'Parler aux autres joueurs': 'Talk to the other players',
  'Ton message': 'Your message',
  'Envoyer': 'Send',
  'Rien encore. Dis quelque chose.': 'Nothing yet. Say something.',
  'Tchat déconnecté': 'Chat disconnected',
  'Réessayer': 'Retry',
  'Historique': 'History',
  'Aucune entrée pour le moment': 'No entries yet',
  'Effacer': 'Clear',

  // ---- Campagne a plusieurs ----
  'à remplir par': 'to be filled by',
  'Envoyer mes champs': 'Send my fields',
  'Renvoyer mes champs': 'Send my fields again',
  'Envoi…': 'Sending…',
  "L'hôte valide les récompenses pour la table.": 'The host validates the rewards for the table.',
  "Envoyé. L'hôte valide les récompenses pour la table.": 'Sent. The host validates the rewards for the table.',

  // ---- Rapport de bug (panneau H) ----
  'Profondeur': 'Depth',
  '20 dernières': 'Last 20',
  'Ce tour': 'This round',
  'Toute la partie': 'Whole game',
  'Copier': 'Copy',
  'Télécharger': 'Download',
  'Copier un rapport de bug': 'Copy a bug report',
  'Rapport envoyé': 'Report sent',
  'Signaler un bug': 'Report a bug',
  'Signaler un bug, avec le journal de la partie': 'Report a bug, with the game log',
  'Bug': 'Bug',
  'Ton nom': 'Your name',
  'Pour pouvoir te répondre': 'So I can get back to you',
  "Qu'est-ce qui s'est passé ?": 'What happened?',
  'Ce que tu faisais, ce que tu attendais, ce qui est arrivé à la place.':
    'What you were doing, what you expected, what happened instead.',
  "Capture d'écran": 'Screenshot',
  'Colle une image avec Ctrl+V, ou choisis un fichier.':
    'Paste an image with Ctrl+V, or pick a file.',
  "Retirer l'image": 'Remove image',
  'Le journal de toute la partie part avec le rapport, tu n’as rien à joindre.':
    'The whole game log goes with the report, you have nothing to attach.',
  'Envoi...': 'Sending...',
  "Merci, c'est envoyé.": "Thanks, it's on its way.",
  "L'envoi a échoué :": 'Sending failed:',
  'Il faut un nom et une description.': 'A name and a description are required.',
  'Image illisible': 'Unreadable image',
  'trop de rapports, reessaie plus tard': 'too many reports, try again later',
  'site injoignable': 'site unreachable',
  'description vide': 'empty description',
  'Télécharger le rapport complet': 'Download the full report',
  'Log': 'Log',
  'Instantané': 'Instant',
  'Rythme de la phase du méchant': 'Villain phase pacing',
  'Avance toute seule': 'Play automatically',
  'Chaque étape se termine seule après un délai, sans attendre un clic':
    'Each step finishes on its own after a delay, without waiting for a click',
  'Vitesse du déroulé': 'Playback speed',
  'Temps d’affichage de chaque étape': 'How long each step stays on screen',
  'En pause': 'Paused',
  'Clic : suite · Espace : pause': 'Click: next · Space: pause',
  'Reprendre': 'Resume',
  'Pause': 'Pause',
  'Tout passer': 'Skip all',
  'Télécharger tout le déroulé de la partie en fichier texte':
    'Download the whole game log as a text file',
  'Rapport copié': 'Report copied',
  'Rapport téléchargé': 'Report downloaded',
  'Copie refusée par le navigateur': 'Copy refused by the browser',

  'Payer': 'Pay',
  'Main': 'Hand',

  // ---- board/mobile/CarteOuverte.tsx ----
  'Utiliser cette carte': 'Use this card',

  // ---- Mode Bac a sable ----
  'Bac à sable': 'Sandbox',
  'Triche': 'Cheat',
  'Clic droit sur une carte ou une pile': 'Right-click a card or a pile',
  'Soigner': 'Heal',
  'Infliger des dégâts': 'Deal damage',
  'Poser de la menace': 'Place threat',
  'Retirer de la menace': 'Remove threat',
  'Fixer la menace à': 'Set threat to',
  'Redresser': 'Ready',
  'Incliner': 'Exhaust',
  'Rendre désorienté': 'Confuse',
  'Rendre sonné': 'Stun',
  'Rendre coriace': 'Make tough',
  'Ajouter des compteurs': 'Add counters',
  'Défausser': 'Discard',
  'Retirer de la partie': 'Remove from game',
  'Appliquer': 'Apply',
  'refusé': 'refused',
  'En main': 'To hand',
  'Mettre en jeu': 'Put into play',
  'Révéler': 'Reveal',
  'Ajoutée à la main': 'Added to hand',
  'Mise en jeu': 'Put into play',
  // « Révélée » est déjà traduit plus bas : ne pas le redéclarer ici.
  'Cette pile est vide': 'This pile is empty',
  'Choisis une carte pour l’ajouter à ta main': 'Pick a card to add it to your hand',
  'Choisis une carte pour la mettre en jeu': 'Pick a card to put it into play',
  'Couper la musique': 'Mute the music',
  'Remettre la musique (nécessite un fichier dans assets/sounds)':
    'Unmute the music (needs a file in assets/sounds)',
  'Maintenir pour jouer': 'Hold to play',
  'Maintenir pour utiliser': 'Hold to use',

  // ---- board/BandeauAbsent.tsx ----
  'est déconnecté': 'is disconnected',
  'Sa reprise dure jusqu’à la fin de son tour.':
    'The takeover lasts until the end of their turn.',
  'Jouer pour lui': 'Play for them',

  // ---- board/JournalHeros.tsx ----
  'Journal': 'Log',
  'Journal du héros': 'Hero log',
  'Rien encore.': 'Nothing yet.',

  // ---- board/RecapPhaseMechant.tsx et mode rapide ----
  // (« Révélé » est déjà défini plus haut, pour le réglage de présentation.)
  'Bilan de la phase du méchant': 'Villain phase summary',
  // Les étapes du bilan reprennent les intitulés de la carte de référence du
  // jeu : on garde ses mots plutôt qu'une traduction littérale du français.
  // (« Cartes révélées » est déjà défini plus bas, pour le panneau d'options.)
  'Menace sur la manigance': 'Threat on the main scheme',
  'Activations': 'Enemy activations',
  'Cartes distribuées': 'Encounter cards dealt',
  'carte(s)': 'card(s)',
  // Les verbes d'une activation : le jeu dit « attacks » / « schemes ».
  'attaque': 'attacks',
  'manigance sur': 'schemes against',
  'boost': 'boost',
  'de base': 'base',
  'de boost': 'from boost',
  'de défense': 'defended',
  'déclenché par': 'triggered by',
  'Voir le déroulé complet du moteur': 'Show the engine’s full sequence',
  'Phase du méchant rapide': 'Fast villain phase',
  'Enchaîne la phase sans « Continue », puis affiche un bilan':
    'Runs the phase without "Continue", then shows a summary',
  'Validation courte': 'Short confirm',
  'Supprime le « Valider » quand la cible est unique et le coût couvert':
    'Drops "Confirm" when the target is the only one and the cost is covered',
  'Entrées retenues sur le total du journal': 'Entries kept out of the whole log',

  // ---- board/CoucheHautsFaits.tsx et récapitulatif de fin de partie ----
  'Haut fait': 'Achievement',
  'Hauts faits débloqués': 'Achievements unlocked',

  // ---- board/SplashTour.tsx ---- ('Joueur' est deja defini plus haut)
  'Round': 'Round',
  'Phase du méchant': 'Villain phase',

  // ---- board/SelecteurCibles.tsx ----
  'Cibles hors table': 'Off-table targets',

  // ---- board/CoucheRevelation.tsx ----
  'Révélée': 'Revealed',

  // ---- board/mots-cles.ts : noms officiels des mots-clés ----
  'Garde': 'Guard',
  'Patrouille': 'Patrol',
  'Accélération': 'Acceleration',
  'Péril': 'Peril',
  'Renfort': 'Surge',
  'Ténacité': 'Toughness',
  'Solide': 'Steady',
  'Robuste': 'Stalwart',
  'Coup Rapide': 'Quickstrike',
  'Riposte': 'Retaliate',
  'Vilenie': 'Villainous',
  'Incitation': 'Incite',
  'Restreint': 'Restricted',
  'Entrave': 'Hinder',
  'Mise en place': 'Setup',
  'Collaboration': 'Teamwork',
  'Perçant': 'Piercing',
  'Déferlement': 'Overkill',
  'À Distance': 'Ranged',
  'Utilisations': 'Uses',

  // ---- board/mots-cles.ts : définitions ----
  'Tant que ce sbire est engagé avec vous, vous ne pouvez pas attaquer le Méchant.':
    'While this minion is engaged with you, you cannot attack the villain.',
  'Tant que ce sbire est engagé avec vous, vous ne pouvez pas contrer la manigance principale.':
    'While this minion is engaged with you, you cannot thwart the main scheme.',
  'Tant que cette manigance annexe est en jeu, les joueurs ne peuvent pas retirer de menace de la manigance principale.':
    'While this side scheme is in play, players cannot remove threat from the main scheme.',
  'Pendant la phase du Méchant, une carte Rencontre supplémentaire est attribuée par icône d’aléa en jeu.':
    'During the villain phase, one additional encounter card is dealt per hazard icon in play.',
  'Ajoute de la menace supplémentaire sur la manigance principale pendant la phase du Méchant.':
    'Adds additional threat to the main scheme during the villain phase.',
  'Chaque carte de boost retournée pendant une activation ennemie gagne une icône de boost par icône d’amplification en jeu.':
    'Each boost card flipped during an enemy activation gains one boost icon per amplify icon in play.',
  'En résolvant cette carte, vous ne pouvez pas demander l’aide des autres joueurs : résolvez-la seul.':
    'While resolving this card, you cannot ask the other players for help: resolve it alone.',
  'Après avoir résolu cette carte, le joueur s’attribue une carte Rencontre supplémentaire.':
    'After resolving this card, the player deals themselves an additional encounter card.',
  'Entre en jeu avec une carte d’état Tenace (les prochains dégâts sont prévenus).':
    'Enters play with a Tough status card (the next damage is prevented).',
  'Il faut DEUX cartes d’état du même type à ce personnage pour être réellement sonné ou désorienté.':
    'This character needs TWO status cards of the same type to actually be stunned or confused.',
  'Ce personnage ne peut être ni sonné ni désorienté.':
    'This character cannot be stunned or confused.',
  'Cet ennemi attaque le joueur dès qu’il s’engage avec lui (si ce joueur est en forme de héros).':
    'This enemy attacks the player as soon as it engages them (if that player is in hero form).',
  'Après que ce personnage a été attaqué, il inflige X dégâts à l’attaquant.':
    'After this character is attacked, it deals X damage to the attacker.',
  'Quand ce sbire s’active, donnez-lui une carte de boost, comme au Méchant.':
    'When this minion activates, deal it a boost card, like the villain.',
  'Retournée comme carte de boost, ajoute X menaces sur la manigance principale.':
    'Flipped as a boost card, adds X threat to the main scheme.',
  'Un joueur ne peut contrôler que deux cartes Restreint à la fois.':
    'A player can only control two Restricted cards at a time.',
  'Commence en jeu et ne peut pas quitter le jeu.':
    'Begins in play and cannot leave play.',
  'Une fois vaincue/déjouée, cette carte rejoint la pile de victoire et vaut ses points de victoire.':
    'Once defeated/thwarted, this card goes to the victory display and is worth its victory points.',
  'Entre en jeu avec X menaces par joueur posées dessus.':
    'Enters play with X threat per player placed on it.',
  'Commence la partie en jeu.': 'Begins the game in play.',
  'Deux personnages désignés peuvent s’incliner ensemble pour déclencher cette capacité.':
    'Two designated characters can exhaust together to trigger this ability.',
  'N’importe quel joueur peut aider à payer cette carte.':
    'Any player can help pay for this card.',
  'Cette attaque défausse TOUTES les cartes Tenace de la cible avant d’infliger les dégâts.':
    'This attack discards ALL Tough status cards from the target before dealing damage.',
  'Les dégâts en excès de cette attaque sont infligés au Méchant (depuis un sbire) ou à votre identité (depuis un allié).':
    'Excess damage from this attack is dealt to the villain (from a minion) or to your identity (from an ally).',
  'Cette attaque ignore Riposte.': 'This attack ignores Retaliate.',
  'Entre en jeu avec X jetons ; quand le dernier est dépensé, défaussez cette carte.':
    'Enters play with X tokens; when the last one is spent, discard this card.',

  // --- Météo, musique, écran de fin (vague 8) ---
  'Ambiance': 'Ambience',
  'Ambiance coupée': 'Ambience off',
  'Aperçu d’ambiance': 'Ambience preview',
  'Force ces effets à l écran pour les voir, sans partie ni carte': 'Forces these effects on screen so you can see them, with no game and no card',
  'Auto': 'Auto',
  'Aucun': 'None',
  // Le libelle de l'apercu se construit par concatenation (« 3 effets ») :
  // chaque compte possible a donc besoin de son entree. Il y a quinze
  // effets, donc quatorze comptes a partir de deux.
  '2 effets': '2 effects',
  '3 effets': '3 effects',
  '4 effets': '4 effects',
  '5 effets': '5 effects',
  '6 effets': '6 effects',
  '7 effets': '7 effects',
  '8 effets': '8 effects',
  '9 effets': '9 effects',
  '10 effets': '10 effects',
  '11 effets': '11 effects',
  '12 effets': '12 effects',
  '13 effets': '13 effects',
  '14 effets': '14 effects',
  '15 effets': '15 effects',
  'Pluie': 'Rain',
  'Orage': 'Storm',
  'Neige': 'Snow',
  'Brume': 'Fog',
  'Étoiles': 'Stars',
  'Braises': 'Embers',
  'Poussière': 'Dust',
  'Néons': 'Neon',
  'Jungle': 'Jungle',
  'Noir et blanc': 'Black and white',
  'Horreur': 'Horror',
  'Cyber': 'Cyber',
  'Sitcom': 'Sitcom',
  'Sépia': 'Sepia',
  'Tempête de sable': 'Sandstorm',
  // --- board/ModaleAmbiance.tsx : « une ambiance s'allume, tu la gardes ? » ---
  // Le nom de la carte n'est PAS traduit : il vient du moteur, qui le donne
  // deja dans la langue des scans.
  'Une ambiance s’allume': 'An ambience is coming on',
  'change l’atmosphère du plateau': 'changes the mood of the board',
  'Tu peux la garder, la couper, ou en choisir une autre à tout moment dans Options › Aperçu d’ambiance.':
    'You can keep it, turn it off, or pick another one at any time from Options › Ambience preview.',
  'Ne plus me montrer ça': 'Do not show me this again',
  // « Oui » et « Non » seuls sont deja pris par le panneau d'options, ou ils
  // valent « On » et « Off ». Des libelles entiers evitent la collision et se
  // lisent mieux comme reponses.
  'Non, couper': 'No, turn it off',
  'Oui, garder': 'Yes, keep it',
  'Demande d’ambiance': 'Ambience prompt',
  'Demander': 'Ask',
  'Toujours': 'Always',
  'Jamais': 'Never',
  'Quand une carte allume une ambiance : poser la question, la garder sans demander, ou la couper sans demander':
    'When a card brings on an ambience: ask the question, keep it without asking, or turn it off without asking',

  'Météo de Storm affichée : cliquer pour la couper': 'Storm weather shown: click to turn it off',
  'Météo coupée : cliquer pour afficher pluie/orage/neige': 'Weather off: click to show rain/storm/snow',
  'Musique d’ambiance active : cliquer pour couper': 'Ambient music on: click to mute',
  'contre': 'vs',
  'round(s)': 'round(s)',

  // --- Panneau d'options (vague 9) ---
  'Options': 'Options',
  'Oui': 'On',
  'Non': 'Off',
  'Animations': 'Animations',
  'Cartes révélées': 'Revealed cards',
  '2,6 s': '2.6 s',
  '5 s': '5 s',
  'Tous les réglages du plateau (animations, sons, ambiance, révélation)':
    'All board settings (animations, sounds, ambience, reveal)',
  'Déplacements de cartes, secousse d’impact, halo de statut':
    'Card movement, impact shake, status halo',
  'Effets sonores du moteur': 'Engine sound effects',
  'Météo, décor ou traitement de l’image, selon les cartes en jeu':
    'Weather, setting or image treatment, driven by the cards in play',
  'Présentation au centre des cartes révélées par la Rencontre':
    'Center presentation of cards revealed from the encounter deck',
  'Raccourcis : E = fin du tour, U = annuler': 'Shortcuts: E = end turn, U = undo',
  'Auto-ciblage': 'Auto-target',
  'Sélectionne d’office la cible quand une seule est légale':
    'Automatically selects the target when only one is legal',
  'Curseurs des autres joueurs': 'Other players’ cursors',
  'Carte de héros': 'Hero card',
  'Art alternatif — mêmes valeurs de jeu': 'Alternate art \u2014 same game values',
  'En multijoueur, montre où pointent les autres': 'In multiplayer, shows where the others are pointing',
  'Scans en français': 'French card scans',
  'Images des cartes en français quand elles existent':
    'French card images where available',
  'Textes marvelcdb (réseau)': 'marvelcdb texts (network)',
  'Texte officiel FR sous l’aperçu des cartes, via fr.marvelcdb.com':
    'Official card text under the preview, from marvelcdb.com',
  'Voir sur marvelcdb': 'View on marvelcdb',
  'français': 'French',
  'Succès': 'Achievements',
  'Bannière quand un exploit est réalisé (Premier sang, Double K.O. ...)':
    'Banner when a feat is accomplished (First blood, Double kill...)',
  'Premier sang': 'First blood',
  'Double K.O.': 'Double kill',
  'Triple K.O.': 'Triple kill',
  'Quadruple K.O.': 'Ultra kill',
  'Déchaînement': 'Rampage',

  // ---- board/mobile : reglage de disposition (vague 12) ----
  'Disposition': 'Layout',
  'Rendu du plateau : automatique selon l’appareil, ou forcer la table complète':
    'Board rendering: automatic based on the device, or force the full table',
  'Automatique': 'Automatic',
  'Mobile': 'Mobile',
  'Ordinateur': 'Desktop',

  // ---- board : narration centrale des effets (ecrite par le client) ----
  // ('subit', 'PV', 'gagne' et 'menace' sont deja definis plus haut)
  'dégâts': 'damage',
  'récupère': 'heals',
  'perd': 'loses',
  'Connexion à la partie…': 'Connecting to the game…',

  // ---- board : fenetre de confirmation du jeu (remplace window.confirm) ----
  // ('Annuler', 'Confirmer', 'Charger' et 'La partie en cours sera remplacée.'
  //  sont deja definis plus haut)
  'Confirmation': 'Confirmation',
  'Quitter': 'Quit',
  'Revenir au menu principal ?': 'Back to the main menu?',
  'La partie en cours sera perdue si tu ne l’as pas sauvegardée.':
    'The current game will be lost if you have not saved it.',

  // ---- board/mobile : vue d'etat degradee et marquage des cibles ----
  // ('cartes' et 'Actif' sont deja definis plus haut)
  'cibles ici': 'targets here',
}
