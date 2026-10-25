// Le vocabulaire que le MOTEUR fabrique lui-même, en français.
//
// Le reste du client est écrit en français et traduit vers l'anglais par `t()`.
// Ces chaînes-là font le trajet inverse : elles naissent en anglais dans le
// moteur Python et arrivent telles quelles dans les boutons de décision. D'où
// le « RESOLVE MULLIGANS » signalé en jeu, au milieu d'une interface française.
//
// D'où viennent-elles exactement (mesuré, pas supposé) :
//
//   • `option.name` = `Effect.GetDisplayName(remove_space=True)`
//     (`src/game/effect/effect.py:425`). Les espaces y sont remplacés par des
//     soulignés ; `nomLisible` les remet avant de nous appeler. Quand la carte
//     n'a pas nommé sa capacité, le moteur retombe sur un mot générique
//     (`Play`, `Choose`, `Resource`…), sur la valeur de l'`AbilityType`
//     (`src/game/ability/ability_type.py:30`), ou sur le nom de la règle
//     déclenchée (`src/game/effect/rule.py`).
//   • `demande.ability_type` = le nom du `TimingPriority`
//     (`src/engine/controller/controller.py:232`).
//
// CE QU'ON NE TRADUIT PAS : le nom d'une capacité écrit sur la carte. Il est
// absent de la table, donc rendu tel quel — et c'est voulu. Les scans affichés
// sont anglais : traduire le bouton alors que la carte sous les yeux dit autre
// chose ferait perdre le lien entre les deux.
//
// Termes officiels FFG/Asmodee, alignés sur `mots-cles.ts` (Coup Rapide,
// Riposte, Renfort, Ténacité, Collaboration, Incitation).

import { langueActuelle } from './langue'
import { TRAITS_FR } from './traits-fr'

/**
 * Anglais du moteur → français officiel.
 *
 * Les clés sont écrites AVEC leurs espaces : `nomLisible` a déjà défait les
 * soulignés quand la recherche a lieu.
 */
const MOTEUR_FR: Record<string, string> = {
  // — Pouvoirs de base et gestes de tour —
  Attack: 'Attaquer',
  Defense: 'Défendre',
  Thwart: 'Contrer',
  Recover: 'Récupérer',
  'Change Form': 'Changer de forme',
  Play: 'Jouer',
  Choose: 'Choisir',
  Ask: 'Demander',
  Resource: 'Ressource',
  Discard: 'Défausser',
  // Le choix facultatif d'un script (`MayChooseOneAbility`) : l'option de
  // refus s'appelle « Cancel », et l'intitule du choix est le `prompt` du
  // script. Signalement Yarro n43 (03/10/2026) : « je n'arrive pas a jouer la
  // capa de Ben Urich », devant deux boutons anglais dont aucun ne disait
  // « defausser ».
  Cancel: 'Annuler',
  'Discard one': 'En défausser une',
  // Robbie Robertson 60156 : meme defaut, meme correctif (04/10/2026).
  'Discard it and deal another': 'La défausser et en distribuer une autre',
  // Mot-clé Starting (60038, 61034, 61036, 61037), signalement Yarro n°70.
  'Add this card to your starting hand': 'Ajouter cette carte à ta main de départ',

  // — Étapes de jeu rendues comme des options —
  'Resolve Mulligans': 'Résoudre les mulligans',
  'End Phase': 'Fin de phase',
  'Select Main Scheme': 'Choisir la manigance principale',
  'Forced abilities would initiate at the same moment':
    'Des capacités forcées se déclenchent en même temps',

  // — Règles du moteur (`src/game/effect/rule.py`) —
  'Game Rule': 'Règle du jeu',
  Ties: 'Égalité',
  'Main Scheme Phase Place Threat': 'Menace de la phase du Méchant',
  'Unique Minion Revealed': 'Sbire unique révélé',
  Activate: 'Activer',
  Retaliate: 'Riposte',
  Consequential: 'Conséquence',
  Quickstrike: 'Coup Rapide',
  Teamwork: 'Collaboration',
  Modifier: 'Modificateur',
  Scheme: 'Manigancer',
  Incite: 'Incitation',
  Toughness: 'Ténacité',
  Reset: 'Réinitialiser',
  Surge: 'Renfort',
  Advance: 'Avancer',
  'Debug Rule': 'Règle de débogage',

  // — Types de capacité (`AbilityType`), utilisés quand la carte n'a pas nommé
  //   la sienne, et affichés en surtitre du panneau de décision —
  Action: 'Action',
  // The City (pu005, 22/10/2026) : UNE action « se déplacer », puis le choix du coût.
  Move: 'Se déplacer',
  // Kingsfall multi-tables (assemblées) : l'Action de Longue vie / À bas.
  'Pod Action': 'Action d’assemblée',
  'Exhaust a character you control': 'Épuiser un personnage que vous contrôlez',
  'Spend 1 resource of any type': 'Dépenser 1 ressource de n’importe quel type',
  'Forced Action': 'Action forcée',
  'Hero Action': 'Action de héros',
  'Alter-Ego Action': 'Action d’alter ego',
  'First Player Action': 'Action du premier joueur',
  Interrupt: 'Interruption',
  'Forced Interrupt': 'Interruption forcée',
  'Forced Interrupt (Hero)': 'Interruption forcée (héros)',
  'Hero Interrupt': 'Interruption de héros',
  'Alter-Ego Interrupt': 'Interruption d’alter ego',
  'First Player Interrupt': 'Interruption du premier joueur',
  Response: 'Réponse',
  'Forced Response': 'Réponse forcée',
  'Hero Response': 'Réponse de héros',
  'Alter-Ego Response': 'Réponse d’alter ego',
  'Hero Resource': 'Ressource de héros',
  'Alter-Ego Resource': 'Ressource d’alter ego',
  Setup: 'Mise en place',
  Special: 'Spécial',
  Preparation: 'Préparation',
  'When Defeated': 'Quand vaincu',
  'When Revealed': 'Quand révélée',
  'When Complete': 'Quand achevée',
  'Basic Power': 'Pouvoir de base',
  'Turn Option': 'Option de tour',
  'Delay Ability': 'Capacité différée',
  Challenge: 'Défi',
  Statistics: 'Statistiques',
  Scenario: 'Scénario',
  Campaign: 'Campagne',
  Status: 'État',
  Rule: 'Règle',
  Constant: 'Constant',

  // — Noms de `TimingPriority`, vus seulement en surtitre —
  Normal: 'À toi de jouer',
  End: 'Fin',

  // — Fins de partie (`src/game/world/game_over.py`) —
  // Le surtitre de la derniere narration : `GameOver_Text` decoupe par
  // libelleEvenement (DemandeCentrale) s'affichait brut, « GAME OVER_TEXT ».
  'Game Over_Text': 'Fin de partie',
  'Players Won': 'Victoire des joueurs',
  'Players Lost': 'Défaite des joueurs',
  'There were no cards in either the encounter deck or the encounter discard pile':
    'Le deck Rencontre et sa défausse sont vides',
  'All players were eliminated': 'Tous les joueurs ont été éliminés',
  'The Final Stage of the Villain was Defeated':
    'Le dernier stade du Méchant a été vaincu',
  'The Final Stage of the Main Scheme was Completed':
    'Le dernier stade de la manigance principale a été achevé',
  'The Main Scheme was Completed': 'La manigance principale a été achevée',
  // — Fin d'un puzzle (`src/game/puzzle/puzzle_objectives.py`) —
  'The Puzzle Objectives were not Met': 'Le round est fini et les objectifs du puzzle ne sont pas atteints',
  // — Fins d'une partie en mode Bataille (`src/game/world/competitive.py`) —
  'The Registration Team Won': 'Le camp Registration l’emporte',
  'The Resistance Team Won': 'Le camp Résistance l’emporte',
  'Both Teams Lost': 'Les deux camps ont perdu',
  'The Game is a Tie': 'Égalité parfaite',

  // — NOMS D'ÉVÉNEMENT DU MOTEUR, en surtitre de la narration centrale —
  //
  // ⚠ D'OÙ VIENT CETTE LISTE, ET POURQUOI ELLE EST ENTIÈRE. Mesure du
  // 15/09/2026, en vraie partie française : le surtitre de `EvenementCentrale`
  // affichait « Scheme Place Threat », « Card Un Apply_Text », « Cards Moved To
  // Revealing Area_Text » — du moteur brut, au milieu d'un écran français.
  // Constat de l'utilisateur, le même jour : « quand je joue en français tout
  // doit être en français, je comprends pas que tu me poses encore la
  // question ».
  //
  // `libelleEvenement` (DemandeCentrale.tsx) découpe le nom de classe du
  // message : `AfterCardsMovedToRevealingArea_Text` devient « Cards Moved To
  // Revealing Area_Text ». Les clés sont donc écrites SOUS CETTE FORME, suffixe
  // `_Text` compris.
  //
  // ⚠ ET ELLE COUVRE TOUT LE MOTEUR, pas les cinq que la mesure a vus. Les 214
  // noms sont relevés dans les sources Python (`Message.<Nom>`) et verrouillés
  // par `vocabulaire-evenements.test.ts` : un message ajouté au moteur sans
  // traduction rend la gate rouge, au lieu de ressortir en anglais le jour où
  // un joueur tombe dessus.

  'Ally Take Consequential Damage': 'L’allié subit ses dégâts de conséquence',
  'Ally Would Take Consequential Damage': 'L’allié va subir ses dégâts de conséquence',
  'Attack Ends Before Damage Dealt': 'L’attaque s’arrête avant les dégâts',
  'Attack Gain Keyword': 'L’attaque gagne un mot-clé',
  'Boost Card Turned Face Up': 'Carte de boost retournée',
  'Boost Card Would Turned Face Up': 'Une carte de boost va être retournée',
  'Boost Icons Would Be Count': 'Décompte des icônes de boost',
  'Calc Deal Excess Damage': 'Calcul des dégâts en excès',
  'Calculate Effect Cost': 'Calcul du coût de l’effet',
  'Campaign Setup': 'Mise en place de la campagne',
  'Campaign Setup After Mulligans': 'Mise en place de campagne après les mulligans',
  'Cannot Prevent Unpreventable Damage_Text': 'Ces dégâts ne peuvent pas être évités',
  'Cards Paid Order_Text': 'Ordre de paiement',
  'Card Apply_Text': 'Carte appliquée',
  'Card Attach To': 'Carte attachée',
  'Card Be Created': 'Carte créée',
  'Card Be Spend As Resource': 'Carte dépensée comme ressource',
  'Card Become Boost': 'Carte devenue boost',
  'Card Defeating_Text': 'Carte en train d’être vaincue',
  'Card Detach From': 'Carte détachée',
  'Card Discard': 'Carte défaussée',
  'Card Enter Hand': 'Carte entrée en main',
  'Card Enter Play': 'Carte entrée en jeu',
  'Card Exhausted': 'Carte engagée',
  'Card Flip': 'Carte retournée',
  'Card Gain Boost Icons_Text': 'Icônes de boost gagnées',
  'Card Gain Trait': 'Trait gagné',
  'Card Gain Upgrade Ability': 'Capacité d’amélioration gagnée',
  'Card Keyword Updated': 'Mot-clé mis à jour',
  'Card Leave Play': 'Carte sortie du jeu',
  'Card Lose Trait': 'Trait perdu',
  'Card Lost Upgrade Ability': 'Capacité d’amélioration perdue',
  'Card Moved': 'Carte déplacée',
  'Card Moved To Deck_Text': 'Carte remise dans le deck',
  'Card Placed Counter': 'Compteur posé',
  'Card Placed Token': 'Jeton posé',
  'Card Put Into Play': 'Carte mise en jeu',
  'Card Ready': 'Carte dégagée',
  'Card Remove From Game': 'Carte retirée de la partie',
  'Card Removed Counter': 'Compteur retiré',
  'Card Removed Token': 'Jeton retiré',
  'Card Reset Keyword': 'Mots-clés réinitialisés',
  'Card Reset_Text': 'Carte réinitialisée',
  'Card Resolve Ability': 'Capacité de la carte résolue',
  'Card Revealed': 'Carte révélée',
  'Card Revealed End': 'Fin de la révélation',
  'Card Set As': 'Carte considérée comme',
  'Card Setup': 'Mise en place de la carte',
  'Card Treat As If Blank': 'Carte considérée comme vierge',
  'Card Un Apply_Text': 'Carte retirée du jeu en cours',
  'Card Update Trait_Text': 'Traits mis à jour',
  'Card Would Attach To': 'Une carte va être attachée',
  'Card Would Be Placed Counter': 'Un compteur va être posé',
  'Card Would Be Placed Token': 'Un jeton va être posé',
  'Card Would Detach From': 'Une carte va être détachée',
  'Card Would Discard': 'Une carte va être défaussée',
  'Card Would Flip': 'Une carte va être retournée',
  'Card Would Gain Boost Icons_Text': 'Des icônes de boost vont être gagnées',
  'Card Would Leave Play': 'Une carte va sortir du jeu',
  'Card Would Move To Area': 'Une carte va changer de zone',
  'Card Would Ready': 'Une carte va être dégagée',
  'Card Would Remove From Game': 'Une carte va être retirée de la partie',
  'Card Would Removed Counter': 'Un compteur va être retiré',
  'Card Would Removed Token': 'Un jeton va être retiré',
  'Card Would Reveal': 'Une carte va être révélée',
  'Card Would Treat As If Blank': 'Une carte va être considérée comme vierge',
  'Card Would Update Keyword_Text': 'Un mot-clé va changer',
  'Cards Be Spend As Resource': 'Cartes dépensées comme ressources',
  'Cards Discard_Text': 'Cartes défaussées',
  'Cards Exhaust_Text': 'Cartes engagées',
  'Cards Flip All_Text': 'Cartes retournées',
  'Cards Generated_Text': 'Cartes créées',
  'Cards Moved': 'Cartes déplacées',
  'Cards Moved To Boosting Area_Text': 'Cartes passées en zone de boost',
  'Cards Moved To Revealing Area_Text': 'Cartes passées en zone de révélation',
  'Cards Moved_Text': 'Cartes déplacées',
  'Cards Place On Table_Text': 'Cartes posées sur la table',
  'Cards Readied_Text': 'Cartes dégagées',
  'Cards Remove_Text': 'Cartes retirées',
  'Cards Return To Hand_Text': 'Cartes reprises en main',
  'Cards Set Aside_Text': 'Cartes mises de côté',
  'Cards Shuffle To Deck_Text': 'Cartes mélangées au deck',
  'Cards Swap Deck_Text': 'Decks échangés',
  'Counting Resources On Cards': 'Décompte des ressources',
  'Damage Be Prevented': 'Dégâts évités',
  'Damage Is Zero_Text': 'Aucun dégât',
  'Damage Updated_Text': 'Dégâts recalculés',
  'Deck Created_Text': 'Deck constitué',
  'Deck Reset': 'Deck reconstitué',
  'Deck Run Out': 'Deck épuisé',
  'Deck Shuffle': 'Deck mélangé',
  'Effect Be Cancel': 'Effet annulé',
  'Effect Resolved': 'Effet résolu',
  'Effect Would Resolve': 'Un effet va se résoudre',
  'Enemy Activate Against You': 'Un ennemi s’active contre toi',
  'Enemy Activation End': 'Fin de l’activation des ennemis',
  'Enemy Given Boost Card': 'Carte de boost donnée à l’ennemi',
  'Enemy Scheme And Place Threat': 'L’ennemi manigance et pose de la menace',
  'Enemy Would Activate': 'Un ennemi va s’activer',
  'Enemy Would Be Given Boost Cards': 'Un ennemi va recevoir des cartes de boost',
  'Face Deal Damage': 'Dégâts infligés',
  'Face Would Deal Damage': 'Des dégâts vont être infligés',
  'Game Area Add Card': 'Carte ajoutée à la zone de jeu',
  'Game Area Add Player': 'Joueur ajouté à la partie',
  'Game Begin Setup': 'Début de la mise en place',
  'Game Initialize': 'Initialisation de la partie',
  'Game Over': 'Fin de partie',
  'Game Would Begin': 'La partie va commencer',
  'Icons Activate_Text': 'Icônes déclenchées',
  'Ignore Keyword On Card': 'Mot-clé ignoré',
  'In Your Play Turn': 'Pendant ton tour',
  'Last Threat Remove From This Scheme': 'Dernière menace retirée de cette manigance',
  'Look At_Text': 'Cartes regardées',
  'Main Scheme Advanced': 'Manigance principale avancée',
  'Main Scheme Completed': 'Manigance principale achevée',
  'Main Scheme Phase End': 'Fin de l’étape de la manigance principale',
  'Main Scheme Phase Start': 'Début de l’étape de la manigance principale',
  'Main Scheme Stage Completed': 'Stade de la manigance principale achevé',
  'Main Scheme Stage Would Be Completed': 'Un stade de la manigance principale va être achevé',
  'Main Scheme Would Advance': 'La manigance principale va avancer',
  'Message Be Instead': 'Effet remplacé',
  'Ally Limit': 'Limite d’alliés',
  'Minion Activates Order': 'Ordre d’activation des sbires',
  'Minion Engage Player': 'Sbire engagé contre un joueur',
  'Minion Would Engage Player': 'Un sbire va s’engager contre un joueur',
  'Obligation Give To Player': 'Obligation remise au joueur',
  'Phase Begin': 'Début de phase',
  'Phase End': 'Fin de phase',
  'Choose Ability Only Option_Text': 'Seul choix possible',
  'Player Choose Ability': 'Choix d’une capacité',
  'Player Deal Encounter Card': 'Carte rencontre distribuée',
  'Player Drew Cards': 'Cartes piochées',
  'Player Resolve Flow': 'Flow résolu',
  'Player Eliminated': 'Joueur éliminé',
  'Player End Phase': 'Fin de la phase du joueur',
  'Player Moved In City': 'Déplacement en ville',
  'Player Would Enter Location': 'Entrée dans un lieu',
  'Player Would Leave Location': 'Sortie d’un lieu',
  'Player Gain Cards_Text': 'Cartes gagnées',
  'Player In Turn': 'Tour du joueur',
  'Player Like In Turn': 'Considéré comme son tour',
  'Player On Event_Text': 'Événement de jeu',
  'Player Paying Resources': 'Paiement des ressources',
  'Player Play Card': 'Le joueur joue une carte',
  'Player Played Card': 'Carte jouée',
  'Player Resolve Mulligans': 'Mulligans résolus',
  'Player Reveal Card': 'Le joueur révèle une carte',
  'Player Searching Deck Cards_Text': 'Recherche dans le deck',
  'Player Select Hero': 'Choix du héros',
  'Player Select Hero End': 'Choix du héros terminé',
  'Player Turn Begin': 'Début du tour du joueur',
  'Player Turn End': 'Fin du tour du joueur',
  'Player Would Be Dealt Encounter Card': 'Une carte rencontre va être distribuée',
  'Player Would Draw Card': 'Le joueur va piocher',
  'Player Would Play Card': 'Le joueur va jouer une carte',
  'Players Order Change': 'L’ordre des joueurs change',
  'Recalculate Attack Damage': 'Dégâts d’attaque recalculés',
  'Calculating Attack Damage': 'Calcul des dégâts d’attaque',
  'Recalculate Scheme Value': 'Valeur de manigance recalculée',
  'Resolve Preparation Ability': 'Résolution d’une capacité de préparation',
  'Resolve Special Ability': 'Résolution d’une capacité spéciale',
  'Resolve Villain Phase Step': 'Étape de la phase du Méchant',
  'Round End': 'Fin du round',
  'Round Start': 'Début du round',
  'Scenario Event': 'Événement du scénario',
  'Scheme Be Defeated': 'Manigance déjouée',
  'Scheme Being Scheme': 'Manigance en cours',
  'Scheme Being Thwart': 'Manigance contrée',
  'Scheme Place Threat': 'Menace posée sur une manigance',
  'Scheme Remove Threat': 'Menace retirée d’une manigance',
  'Scheme Would Be Defeated': 'Une manigance va être déjouée',
  'Scheme Would Place Threat': 'De la menace va être posée',
  'Scheme Would Remove Threat': 'De la menace va être retirée',
  'Status Card Place On': 'Carte d’état posée',
  'Status Discard From': 'Carte d’état défaussée',
  'Status Would Card Place On': 'Une carte d’état va être posée',
  'Status Would Card Place On Again': 'Une carte d’état va être posée une seconde fois',
  'Surge Would Be Resolved': 'Déferlement à résoudre',
  'The Last Counter Is Removed From Here': 'Le dernier compteur est retiré d’ici',
  'This Revealed': 'Cette carte est révélée',
  'Threat Be Prevented': 'Menace évitée',
  'Unit Attack End': 'Fin de l’attaque',
  'Unit Attack Unit': 'Attaque d’un personnage',
  'Unit Attack You': 'Tu es attaqué',
  'Unit Be Attacked': 'Personnage attaqué',
  'Unit Be Defeated': 'Personnage vaincu',
  'Unit Become Defender': 'Personnage devenu défenseur',
  'Unit Being Attack': 'Personnage en train d’être attaqué',
  'Unit Change Form': 'Changement de forme',
  'Unit Change Form End': 'Fin du changement de forme',
  'Unit Defeated Scheme': 'Manigance déjouée par un personnage',
  'Unit Defeated Unit': 'Personnage vaincu par un autre',
  'Unit Defend Against Attack': 'Défense contre une attaque',
  'Unit Defend End': 'Fin de la défense',
  'Unit Defense Internal': 'Défense en cours',
  'Unit Gain Face Down Boost Cards_Text': 'Cartes de boost face cachée gagnées',
  'Unit Heal Health': 'Points de vie rendus',
  'Unit Hit Point Reset': 'Points de vie réinitialisés',
  'Unit Hit Point Set': 'Points de vie fixés',
  'Unit Like Being Attack': 'Traité comme une attaque',
  'Unit Loss Health': 'Points de vie perdus',
  'Unit Loss Health Helper': 'Perte de points de vie',
  'Unit Make Key Word Attack': 'Attaque avec mot-clé',
  'Unit Recovery': 'Récupération',
  'Unit Scheme Against': 'Manigance contre une manigance',
  'Unit Scheme End': 'Fin de la manigance',
  'Unit Thwart End': 'Fin du contre',
  'Unit Thwart Scheme': 'Manigance contrée par un personnage',
  'Unit Took Damage': 'Dégâts subis',
  'Unit Use Basic Power': 'Pouvoir de base utilisé',
  'Unit Would Attack': 'Un personnage va attaquer',
  'Unit Would Attack Unit': 'Un personnage va en attaquer un autre',
  'Unit Would Be Attacked': 'Un personnage va être attaqué',
  'Unit Would Be Defeated': 'Un personnage va être vaincu',
  'Unit Would Change Form': 'Un personnage va changer de forme',
  'Unit Would Defend': 'Un personnage va défendre',
  'Unit Would Recovery': 'Un personnage va récupérer',
  'Unit Would Scheme': 'Un personnage va manigancer',
  'Unit Would Take Damage': 'Un personnage va subir des dégâts',
  'Unit Would Thwart': 'Un personnage va contrer',
  'Villain Advance': 'Le Méchant progresse',
  'Villain Advanced': 'Méchant avancé',
  'Villain Phase Step Start': 'Début d’une étape de la phase du Méchant',
  'Villain Would Advance': 'Le Méchant va progresser',
}

/**
 * Quand une carte offre DEUX fois la même capacité, le moteur numérote la
 * seconde : `Attack_1` (`effect.py`, « Fix replay for 10029 »). `nomLisible`
 * nous la passe en « Attack 1 ». On isole ce suffixe pour pouvoir traduire le
 * mot, puis on le rend sous une forme lisible : « Attaquer (2) », en comptant
 * à partir de 1 comme le ferait un humain.
 */
const SUFFIXE_INDEX = /^(.*?) (\d+)$/

/** « Action 1 » -> « Action » : retire l'index interne du moteur d'un type de capacité (Action, Hero Action, Interrupt...). */
export function sansIndexDeCapacite(libelle: string): string {
  const m = /^((?:.+ )?(?:Action|Interrupt|Response))[ _]\d+$/.exec(libelle)
  return m ? m[1]! : libelle
}

const degats = (n: string) => `${n} ${Number(n) > 1 ? 'dégâts' : 'dégât'}`
const menaces = (n: string) => `${n} ${Number(n) > 1 ? 'menaces' : 'menace'}`

/**
 * Les CHOIX que les scripts de cartes impriment en anglais (`ForChoiceAbility
 * ("Take 2 damage", ...)`, 589 libellés distincts dans les scripts) : leurs
 * formes les plus courantes, avec le nombre. Une forme absente reste en
 * anglais, comme un nom de capacité : le texte de la carte en grand est le
 * repère.
 */
const TYPES_ZONE_FR: Record<string, string> = {
  Ally: 'allié',
  PlayerSideScheme: 'manigance annexe de joueur',
  Resource: 'ressource',
  Support: 'soutien',
  Path: 'voie',
  Upgrade: 'amélioration',
}

const GABARITS_CHOIX: Array<[RegExp, (m: RegExpExecArray) => string]> = [
  // Changer de forme vers une forme NOMMEE (player_setup.py) : « Change To Spider-Man », ou, pour deux formes du meme
  // nom, le trait qui les distingue (« Change To GIANT » -> « Passer en forme Géant », Ant-Man, 24/10/2026).
  [/^Change To (.+)$/, (m) => `Passer en ${formeNommee(m[1]!)}`],
  // Bebop & Rocksteady (`tk006a`, enemies.py OrdreDesVilainsActives) : le premier
  // joueur choisit, pour chaque joueur, le vilain qui s'active d'abord (Q8, 16/10/2026).
  [/^Choose which villain activates first against (.+)$/,
    (m) => `Choisis le méchant qui s’active d’abord contre ${m[1]}`],
  [/^Choose Bebop or Rocksteady$/, () => 'Choisis Bebop ou Rocksteady'],
  // Build Support (51026, rapport BL-Stark du 23/10/2026) : « Search their deck and discard pile for a support with a cost of 3 or less... ».
  [/^Search (?:their|your) deck and discard pile for an? (support|ally|upgrade) with a cost of (\d+) or less and put it into play$/,
    (m) => `Chercher ${({ support: 'un soutien', ally: 'un allié', upgrade: 'une amélioration' } as Record<string, string>)[m[1]!]} de coût ${m[2]} ou moins dans ton deck ou ta défausse et le mettre en jeu`],
  // Pack TMNT Venus (`venus/__init__.py`, ProposerRetraitDragage) : retrait facultatif de compteurs de dragage.
  [/^Remove (\d+) dredge counters to draw (\d+) cards$/,
    (m) => `Retirer ${m[1]} compteurs de dragage pour piocher ${m[2]} cartes`],
  [/^Remove (\d+) dredge counters to confuse and stun an enemy$/,
    (m) => `Retirer ${m[1]} compteurs de dragage pour désorienter et sonner un ennemi`],
  // Campagne Skrull Menace (`skrull_menace/campaign.py`) : la règle de coopération, la zone, la campagne experte.
  [/^Discard the top card of your deck to place (.+) in the victory display$/,
    (m) => `Défausser le dessus de ton deck pour placer ${m[1]} dans la pile de victoire`],
  [/^Cooperation Area: add a card \((.+)\)$/, (m) => `Zone de coopération : ajouter une carte (${TYPES_ZONE_FR[m[1]!] ?? m[1]})`],
  [/^Place 1 acceleration token on the main scheme to rejoin the team at full hit points$/,
    () => 'Placer 1 jeton Accélération sur la manigance principale pour rejoindre l’équipe avec tous tes points de vie'],
  [/^Place 1 acceleration token on the main scheme to heal to full$/,
    () => 'Placer 1 jeton Accélération sur la manigance principale pour te soigner complètement'],
  // Obligations a deux branches (Need for Speed 14024, Personality Adjustment tj012 de Jennika).
  [/^Place (\d+) threat on the main scheme\. Discard this obligation$/,
    (m) => `Placer ${menaces(m[1]!)} sur la manigance principale. Défausser cette obligation`],
  [/^Exhaust (.+) → remove (.+) from the game$/, (m) => `Incliner ${m[1]} → retirer ${m[2]} de la partie`],
  [/^Take (\d+) indirect damage$/, (m) => `Subir ${m[1]} ${Number(m[1]) > 1 ? 'dégâts indirects' : 'dégât indirect'}`],
  // La repartition des degats indirects (`PlayerAction.AssignDamage`, rapport Yarro n92).
  [/^Assign (\d+) damage$/, (m) => `Répartir ${m[1]} ${Number(m[1]) > 1 ? 'dégâts indirects' : 'dégât indirect'}`],
  [/^Take (\d+) damage$/, (m) => `Subir ${degats(m[1]!)}`],
  [/^Place (\d+) threat on the main scheme$/, (m) => `Placer ${menaces(m[1]!)} sur la manigance principale`],
  // 19/10/2026, options laissees en anglais. Traduites SEULEMENT parce que le texte francais de leur carte existe deja
  // (textes-fr-complets.ts « 01134 » Ultron ; textes-fr-fanmade.ts « tk022 » Lay the Beatdown) : memes mots, a la forme du
  // bouton (infinitif, « ton »).
  [/^Put the top card of your deck into play facedown, engaged with you as a Drone minion$/,
    () => 'Mettre en jeu la carte du dessus de ton deck, face cachée, engagée avec toi en tant que sbire Drone'],
  [/^Deal (\d+) indirect damage to your hero$/, (m) => `Infliger ${m[1]} ${Number(m[1]) > 1 ? 'dégâts indirects' : 'dégât indirect'} à ton héros`],
  [/^Stun your hero$/, () => 'Sonner ton héros'],
  [/^Place (\d+) threat here$/, (m) => `Placer ${menaces(m[1]!)} ici`],
  [/^Remove (\d+) threat from a scheme$/, (m) => `Retirer ${menaces(m[1]!)} d’une manigance`],
  [/^Draw (\d+) cards?$/, (m) => `Piocher ${m[1]} ${Number(m[1]) > 1 ? 'cartes' : 'carte'}`],
  [/^Deal (\d+) damage to an enemy$/, (m) => `Infliger ${degats(m[1]!)} à un ennemi`],
  [/^Deal (\d+) damage to your identity$/, (m) => `Infliger ${degats(m[1]!)} à ton identité`],
  [/^[Dd]eal (\d+) damage to Avengers Tower$/, (m) => `Infliger ${degats(m[1]!)} à la tour des Avengers`],
  [/^(.+) gets \+(\d+) ATK for this attack$/, (m) => `${m[1]} gagne +${m[2]} ATQ pour cette attaque`],
  [/^Heal (\d+) damage from your identity$/, (m) => `Soigner ${degats(m[1]!)} de ton identité`],
  [/^Heal (\d+) damage from an identity$/, (m) => `Soigner ${degats(m[1]!)} d’une identité`],
  [/^Stun an enemy$/, () => 'Rendre un ennemi sonné'],
  [/^Confuse an enemy$/, () => 'Rendre un ennemi désorienté'],
  [/^Stun a minion$/, () => 'Rendre un sbire sonné'],
  [/^Ready your hero$/, () => 'Redresser ton héros'],
  [/^Ready your identity$/, () => 'Redresser ton identité'],
  [/^Exhaust your identity$/, () => 'Engager ton identité'],
  [/^Flip to alter-ego form$/, () => 'Passer en forme alter ego'],
  // Choix « payer un coût » (`ForChoiceAbilityWithCost`, Sonic Boom 01123) : les
  // jetons [[energy]] restent, ils deviennent des icônes à l'affichage.
  [/^Spend (\[\[.+)$/, (m) => `Dépenser ${m[1]}`],
  // Action d'assemblée : « <heros> (<table>) - this table » -> le groupe de cette table.
  [/^(.+) - this table$/, (m) => `${m[1]} (cette table)`],
  [/^Exhaust each character you control$/, () => 'Incliner chacun de tes personnages'],
  // « Combien de fois ce choix ? » (player_action.py, `ChooseAbilities(repeat=...)`).
  [/^(\d+) times?$/, (m) => `${m[1]} fois`],
  [/^No repeat$/, () => 'Aucun'],
]

/**
 * Rend le libellé du moteur en français. Une chaîne absente de la table est
 * rendue INCHANGÉE : c'est le cas des noms de capacités imprimés sur les
 * cartes, qui doivent rester alignés sur le scan affiché.
 */
/** « GIANT » -> « forme Géant » (traits connus, en majuscules) ; un nom de carte reste tel quel. */
function formeNommee(brut: string): string {
  const mots = brut.trim().split(/\s+/)
  const traits = mots.map((mot) => TRAITS_FR[mot.replace(/\.$/, '').toUpperCase()])
  if (mots.every((mot) => mot === mot.toUpperCase()) && traits.every(Boolean)) {
    const fr = traits.map((trait) => trait!.charAt(0) + trait!.slice(1).toLowerCase()).join(' ')
    return `forme ${fr}`
  }
  return brut
}

export function traduireMoteur(libelle: string): string {
  if (langueActuelle() !== 'fr') return libelle

  const direct = MOTEUR_FR[libelle]
  if (direct) return direct

  for (const [motif, rendre] of GABARITS_CHOIX) {
    const trouve = motif.exec(libelle)
    if (trouve) return rendre(trouve)
  }

  // « Action 1 », « Hero Action 2 »... : l'index interne du moteur n'a aucun sens pour un joueur
  // (demande du 22/10/2026 : plus jamais « Action 1 / Action 2 ») ; on garde le nom du type seul.
  const numerote = SUFFIXE_INDEX.exec(libelle)
  if (numerote) {
    const base = MOTEUR_FR[numerote[1]!]
    if (base) return base
  }

  return libelle
}

/**
 * Les deux titres de la question « combien de fois ce choix ? » : la carte, le
 * choix en cause et le reste à faire, sans qu'il faille deviner (signalement
 * Yarro du 05/10/2026). Le nom de carte arrive déjà remis dans la langue du
 * plateau par `sansIdentifiantsEnFrancais` ; le choix, lui, est de l'anglais du
 * moteur et passe par `traduireMoteur`, comme le bouton qu'il désigne.
 * Un texte qui n'a pas cette forme sort inchangé.
 */
export function traduireTitreRepetition(texte: string): string {
  if (langueActuelle() !== 'fr') return texte
  const total = /^(.+): (.+?)\. How many times\? \(1 to (\d+)\)$/.exec(texte)
  if (total) return `${total[1]} : ${traduireMoteur(total[2]!)}. Combien de fois ? (1 à ${total[3]})`
  const auMaximum = /^(.+): no option can be done in full\. Do as much as you can: (.+)$/.exec(texte)
  if (auMaximum) {
    return `${auMaximum[1]} : aucune option n'est faisable en entier, tu dois en faire une au maximum. Celle-ci : ${traduireMoteur(auMaximum[2]!).replace(/^Spend /, 'Dépenser ')}`
  }
  const enPlus = /^(.+): (.+?) done \((\d+) of (\d+)\)\. How many more times\?$/.exec(texte)
  if (enPlus) {
    return `${enPlus[1]} : ${traduireMoteur(enPlus[2]!)} fait (${enPlus[3]} sur ${enPlus[4]}). Combien de fois en plus ?`
  }
  return texte
}

/**
 * Traduit le « par quel effet » que le moteur accroche en fin de narration :
 * « Klaw va comploter (+0) (Advance (When Revealed)) ».
 *
 * ⚠ SEGMENT ENTIER, JAMAIS UN MOT DANS UNE PHRASE. Un remplacement par
 * sous-chaine paraissait tentant — les deux morceaux sont du vocabulaire
 * moteur — mais il aurait abime les noms de cartes. Mesure du 11/09/2026 sur
 * data/cards.json : 28 cartes contiennent le mot « Attack » (« Massive
 * Attack »), 20 le mot « Defense », 5 le mot « Surge », et TROIS cartes
 * s'appellent exactement Advance, Surge et Teamwork. On ne traduit donc qu'un
 * contenu de parenthese entier, avec la meme regle d'egalite exacte que
 * `traduireMoteur` : un libelle absent de la table sort inchange.
 *
 * Deux formes, et elles seules :
 *   « (<fenetre>) »               -> « (Quand révélée) »
 *   « (<capacite> (<fenetre>)) »  -> « (Avancer (Quand révélée)) »
 * Dans la seconde, les deux morceaux se traduisent INDEPENDAMMENT : une carte
 * fan-made garde son nom et voit quand meme sa fenetre en francais.
 */
export function traduireEffets(texte: string): string {
  if (langueActuelle() !== 'fr') return texte

  // Un segment ne se traduit que s'il est EXACTEMENT une entree de la table.
  const segment = (brut: string): string => {
    const libelle = brut.trim()
    return MOTEUR_FR[libelle] ?? libelle
  }

  return (
    texte
      // La forme imbriquee d'abord : sinon la regex simple mangerait la
      // parenthese interieure et laisserait une orpheline.
      .replace(/\(([^()]*?)\s*\(([^()]+)\)\)/g, (_, capacite: string, fenetre: string) =>
        `(${segment(capacite)} (${segment(fenetre)}))`
      )
      .replace(/\(([^()]+)\)/g, (tel, contenu: string) => {
        const traduit = segment(contenu)
        return traduit === contenu.trim() ? tel : `(${traduit})`
      })
  )
}
