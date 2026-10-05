// LA MAIN PENDANT LA PHASE DU MECHANT (revirement du 05/10/2026).
//
// Le carre de la phase ne cache plus la main : quand le moteur attend une
// reponse du joueur, elle est visible et cliquable, ses cartes jouables en
// surbrillance (`interactifs`). Le joueur voit ainsi une carte mal
// parametree, qu'il devrait pouvoir jouer, et peut signaler le defaut.

export type EtatDeLaMain = {
  /** Manuel DECLARE (pas une pause) : un seul operateur pour tous les heros. */
  modeManuelDeclare: boolean
  /** Un ciblage est ouvert sur la table. */
  ciblageEnCours: boolean
  etapeAssistant: string | undefined
  /** Le carre est a l'ecran (scene PC) : la phase du mechant, ou la defense « Pendant ton tour ». */
  carreDeLaPhase: boolean
  /** Le moteur attend une reponse du joueur LOCAL. */
  questionAuJoueur: boolean
}

export function mainVisibleForcee(e: EtatDeLaMain): boolean {
  if (e.modeManuelDeclare) return true
  if (e.ciblageEnCours && (e.etapeAssistant === 'target' || e.etapeAssistant === 'payment')) return true
  return e.carreDeLaPhase && e.questionAuJoueur
}
