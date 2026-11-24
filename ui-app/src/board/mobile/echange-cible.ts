// Toucher une AUTRE cible legale quand le moteur n'en veut qu'une l'ECHANGE (maquette approuvee, 26/10/2026) : sur la table, il faut
// d'abord retirer la cible choisie ; dans la feuille, un seul toucher suffit. Cette fonction pure dit QUELLE cible retirer.
import type { EtatInteractif } from '../interaction'

export function cibleAEchanger({
  id,
  maximum,
  legales,
  interactifs,
}: {
  /** La carte touchee. */
  id: number
  /** Le nombre maximal de cibles de l'option. */
  maximum: number
  /** Les cibles que le moteur a proposees. */
  legales: readonly number[]
  interactifs: Map<number, EtatInteractif>
}): number | undefined {
  if (maximum !== 1 || !legales.includes(id)) return undefined
  for (const [autre, etat] of interactifs) {
    if (autre !== id && etat.role === 'cible' && etat.choisie && etat.agir) return autre
  }
  return undefined
}
