// Combien de tuiles tiennent dans une bande, a quelle taille, combien restent.
//
// C'est la regle qui remplace le zoom optique : le niveau 1 ne defile JAMAIS,
// il condense davantage. Par ordre d'application :
//   1. les tuiles rétrécissent jusqu'a leur taille plancher ;
//   2. au-dela, le surplus se replie dans une pastille « +N » touchable ;
//   3. (hors de ce fichier) un seul joueur est deplie a la fois.
//
// Fonction pure : elle ne regarde que le NOMBRE d'unites, jamais leur contenu.

import type { UniteAffichee } from '../zones'

/** Taille d'une tuile condensee, en pixels CSS. */
export const TUILE_CONFORT = { largeur: 140, hauteur: 96 }

/**
 * Plancher de lisibilite. 64 px de haut est la valeur de la spec : en dessous,
 * le nom et les compteurs ne sont plus lisibles, et la cible tactile passe sous
 * les 44 px une fois la marge interne retiree.
 */
export const TUILE_PLANCHER = { largeur: 96, hauteur: 64 }

/** Ecart entre deux tuiles, dans les deux axes. */
export const ECART = 8

export type Taille = 'confort' | 'plancher'

export type BudgetBande = {
  /** Place disponible pour les tuiles, marges de la bande deja retirees. */
  largeur: number
  hauteur: number
}

export type BandeCondensee = {
  /** Les unites reellement dessinees, dans l'ordre recu. */
  tuiles: UniteAffichee[]
  /** Les unites repliees dans la pastille « +N ». Jamais negatif. */
  restantes: number
  taille: Taille
}

/** Combien de tuiles de cette taille tiennent dans ce budget. Au moins 0. */
function capacite(budget: BudgetBande, tuile: { largeur: number; hauteur: number }): number {
  const colonnes = Math.floor((budget.largeur + ECART) / (tuile.largeur + ECART))
  const rangees = Math.floor((budget.hauteur + ECART) / (tuile.hauteur + ECART))
  return Math.max(0, colonnes * rangees)
}

export function condenser(unites: UniteAffichee[], budget: BudgetBande): BandeCondensee {
  if (unites.length === 0) {
    return { tuiles: [], restantes: 0, taille: 'confort' }
  }

  if (unites.length <= capacite(budget, TUILE_CONFORT)) {
    return { tuiles: unites, restantes: 0, taille: 'confort' }
  }

  const placesAuPlancher = capacite(budget, TUILE_PLANCHER)
  if (unites.length <= placesAuPlancher) {
    return { tuiles: unites, restantes: 0, taille: 'plancher' }
  }

  // Une place est reservee a la pastille « +N » : elle ne recouvre pas une tuile.
  const montrees = Math.max(0, placesAuPlancher - 1)
  return {
    tuiles: unites.slice(0, montrees),
    restantes: unites.length - montrees,
    taille: 'plancher',
  }
}
