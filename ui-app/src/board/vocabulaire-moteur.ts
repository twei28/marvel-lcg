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
  // — Fins d'une partie en mode Bataille (`src/game/world/competitive.py`) —
  'The Registration Team Won': 'Le camp Registration l’emporte',
  'The Resistance Team Won': 'Le camp Résistance l’emporte',
  'Both Teams Lost': 'Les deux camps ont perdu',
  'The Game is a Tie': 'Égalité parfaite',
}

/**
 * Quand une carte offre DEUX fois la même capacité, le moteur numérote la
 * seconde : `Attack_1` (`effect.py`, « Fix replay for 10029 »). `nomLisible`
 * nous la passe en « Attack 1 ». On isole ce suffixe pour pouvoir traduire le
 * mot, puis on le rend sous une forme lisible : « Attaquer (2) », en comptant
 * à partir de 1 comme le ferait un humain.
 */
const SUFFIXE_INDEX = /^(.*?) (\d+)$/

/**
 * Rend le libellé du moteur en français. Une chaîne absente de la table est
 * rendue INCHANGÉE : c'est le cas des noms de capacités imprimés sur les
 * cartes, qui doivent rester alignés sur le scan affiché.
 */
export function traduireMoteur(libelle: string): string {
  if (langueActuelle() !== 'fr') return libelle

  const direct = MOTEUR_FR[libelle]
  if (direct) return direct

  const numerote = SUFFIXE_INDEX.exec(libelle)
  if (numerote) {
    const base = MOTEUR_FR[numerote[1]!]
    if (base) return `${base} (${Number(numerote[2]) + 1})`
  }

  return libelle
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
