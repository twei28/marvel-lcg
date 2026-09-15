// LA TABLE SE TAIT PENDANT QUE LA SCÈNE RACONTE.
//
// ⚠ DEUX RÉCITS EN MÊME TEMPS, ET C'ÉTAIT LE DÉFAUT. Constat de l'utilisateur,
// 15/09/2026 : « ça se passe dans la fenêtre et ça bouge aussi derrière la
// fenêtre, justement parce que le moteur fait les actions. Ça rend tout très
// confus parce qu'on doit se focus sur la fenêtre, mais en même temps, derrière,
// il y a des choses qui se passent. »
//
// En mode Détaillé, la scène EST le récit : elle montre la carte qui agit, sa
// cible, ce qu'elle fait. Pendant ce temps, le plateau derrière rejouait le même
// événement en mouvement (une carte qui vole, une charge d'attaque). Deux fois
// la même chose, à deux endroits, en même temps.
//
// Sa demande, dans ses mots : « qu'il n'y ait pas les animations du moteur, et
// que quand on passe à Suivant, la carte soit automatiquement au bon endroit,
// les dégâts automatiquement mis ».
//
// ⚠ SEULEMENT EN MODE DÉTAILLÉ. Le mode « Sur la table » n'a pas de scène : son
// récit se joue justement SUR la table, et lui couper ses animations le viderait
// de sa raison d'être. Le mode Instantané n'a rien à raconter.
//
// Même raisonnement que la garde déjà en place sur `CoucheRevelation`, posée
// après un constat jumeau : « il montre quand même encore la dernière carte en
// grand, en dehors de la modale ».
//
// Module PUR : une règle, pas de DOM, testable sans navigateur.

export type EtatDesAnimations = {
  /** Le réglage du joueur : il a le dernier mot, toujours. */
  reglage: boolean
  /** Mode « Détaillé » : la phase du méchant se joue dans une scène centrale. */
  sceneCentrale: boolean
  /** Le moteur est dans une des quatre phases du méchant. */
  phaseMechantEnCours: boolean
}

/**
 * Le plateau anime-t-il ses cartes en ce moment ?
 *
 * ⚠ LE RÉGLAGE DU JOUEUR PASSE AVANT TOUT : qui a coupé les animations ne les
 * voit revenir dans aucun mode. Cette règle ne fait qu'en RETIRER, jamais en
 * ajouter.
 */
export function animationsDuPlateau(etat: EtatDesAnimations): boolean {
  if (!etat.reglage) return false
  return !(etat.sceneCentrale && etat.phaseMechantEnCours)
}
