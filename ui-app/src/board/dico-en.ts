// dico-en.ts — dictionnaire français -> anglais du plateau.
//
// Rempli à la main, écran par écran. Les clés sont les textes FRANÇAIS exacts
// passés à t() (voir langue.ts) ; les valeurs reprennent le vocabulaire
// OFFICIEL anglais du jeu (Villain, Thwart, Scheme, Tough/Stunned/Confused,
// Surge, Overkill, Piercing, victory display, encounter deck, boost...).
// Une clé absente laisse le texte en français : rien ne casse.

export const DICO_EN_BASE: Record<string, string> = {
  // ---- Partagé (boutons, libellés courts) ----
  'Fermer': 'Close',
  'Annuler': 'Cancel',
  'Confirmer': 'Confirm',
  'Passer': 'Pass',
  'Retour': 'Back',
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
  'État affiché': 'Displayed state',
  'Partie en cours': 'Live game',
  'Joueur affiché': 'Displayed player',
  'Mode d’affichage des actions': 'Action display mode',
  'Détaillé': 'Detailed',
  'Ancien plateau': 'Legacy board',
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
  'Aucune partie derrière cette vue : rien à jouer. Choisis « Partie en cours » pour agir.':
    'No game behind this view: nothing to play. Pick "Live game" to act.',
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

  // ---- board/interaction.ts : assistant pas-à-pas ----
  'Choisir une action': 'Choose an action',
  'Choisir les cartes du mulligan': 'Choose the mulligan cards',
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
  'Étape 2 - paie avec des cartes de ta main ou des générateurs de ressources':
    'Step 2 - pay with cards from your hand or resource generators',
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
  'Historique': 'History',
  'Aucune entrée pour le moment': 'No entries yet',
  'Effacer': 'Clear',

  // ---- board/JournalHeros.tsx ----
  'Journal': 'Log',
  'Journal du héros': 'Hero log',
  'Rien encore.': 'Nothing yet.',

  // ---- board/RecapPhaseMechant.tsx et mode rapide ----
  // (« Révélé » est déjà défini plus haut, pour le réglage de présentation.)
  'Bilan de la phase du méchant': 'Villain phase summary',
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
  'Météo': 'Weather',
  'Météo de Storm affichée : cliquer pour la couper': 'Storm weather shown: click to turn it off',
  'Météo coupée : cliquer pour afficher pluie/orage/neige': 'Weather off: click to show rain/storm/snow',
  'Musique': 'Music',
  'Musique d’ambiance active : cliquer pour couper': 'Ambient music on: click to mute',
  'Musique coupée : déposer musique-<méchant>.mp3 dans assets/sounds puis activer':
    'Music off: drop musique-<villain>.mp3 into assets/sounds then enable',
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
  'Tous les réglages du plateau (animations, sons, musique, météo, révélation)':
    'All board settings (animations, sounds, music, weather, reveal)',
  'Déplacements de cartes, secousse d’impact, halo de statut':
    'Card movement, impact shake, status halo',
  'Effets sonores du moteur': 'Engine sound effects',
  'Pluie, orage ou neige quand un Soutien météo de Storm est en jeu':
    'Rain, storm or snow while one of Storm\'s weather supports is in play',
  'Présentation au centre des cartes révélées par la Rencontre':
    'Center presentation of cards revealed from the encounter deck',
  'Raccourcis : E = fin du tour, U = annuler': 'Shortcuts: E = end turn, U = undo',
  'Auto-ciblage': 'Auto-target',
  'Sélectionne d’office la cible quand une seule est légale':
    'Automatically selects the target when only one is legal',
  'Curseurs des autres joueurs': 'Other players\u2019 cursors',
  'Carte de héros': 'Hero card',
  'Art alternatif — mêmes valeurs de jeu': 'Alternate art \u2014 same game values',
  'En multijoueur, montre où pointent les autres': 'In multiplayer, shows where the others are pointing',
  'Textes marvelcdb (réseau)': 'marvelcdb texts (network)',
  'Texte officiel FR sous l’aperçu des cartes, via fr.marvelcdb.com':
    'Official card text under the preview, from marvelcdb.com',
  'Voir sur marvelcdb': 'View on marvelcdb',
  'Succès': 'Achievements',
  'Bannière quand un exploit est réalisé (Premier sang, Double K.O. ...)':
    'Banner when a feat is accomplished (First blood, Double kill...)',
  'Premier sang': 'First blood',
  'Double K.O.': 'Double kill',
  'Triple K.O.': 'Triple kill',
  'Quadruple K.O.': 'Ultra kill',
  'Déchaînement': 'Rampage',
}
