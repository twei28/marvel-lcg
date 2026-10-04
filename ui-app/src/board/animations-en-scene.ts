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
  /**
   * La mise en place automatique (mains distribuées, decks posés, manigance
   * et première carte de rencontre révélées) n'est le geste de PERSONNE :
   * personne n'a demandé chaque carte une par une. Constat de l'utilisateur,
   * 24/09/2026 : « ça fait beaucoup de bruit pour rien ». Seule la manigance
   * principale garde sa présentation (CoucheRevelation, `seulementManigance`).
   */
  enMiseEnPlace: boolean
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
  if (etat.enMiseEnPlace) return false
  return !(etat.sceneCentrale && etat.phaseMechantEnCours)
}

/**
 * Une resynchronisation massive (Undo, reconnexion, remelange...) a-t-elle
 * eu lieu entre ces deux rendus ?
 *
 * ⚠ « GameSession.Undo » (Fusion/marvel-lcg-src/src/game/game_run/
 * game_session.py) ne defait pas UN geste : il relance toute la partie et
 * rejoue l'historique depuis zero jusqu'a un point de reprise. Le client
 * recoit alors un etat entierement neuf, un `render_id` reparti bien plus
 * bas que celui deja affiche — indiscernable d'une vraie nouveaute, donc
 * toutes les animations d'entree (statut, revelation, retournement de
 * carte...) semblaient rejouer d'un coup. Constat de l'utilisateur,
 * 28/09/2026 : « le reclaquement de cartes... ça perturbe les gens ».
 *
 * Seule une BAISSE du `render_id` compte : une hausse, meme un grand saut
 * (le moteur avance par dizaines a chaque mise a jour), reste un rendu
 * normal — c'est deja la regle que `CoucheAnimations.tsx` applique aux
 * cartes de la main (MAX_VOLS), transposee ici a tout le plateau.
 */
export function estResynchronisation(
  renderIdActuel: number | undefined,
  renderIdPrecedent: number | undefined
): boolean {
  if (renderIdActuel === undefined || renderIdPrecedent === undefined) return false
  return renderIdActuel < renderIdPrecedent
}
