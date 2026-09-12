// Quand le moteur attend une CIBLE, elle s'allume dans sa bande — mais la
// bande peut etre defilee, ou la table plus bas que l'ecran : rien ne le
// disait (point 4 de la relecture du 12/09/2026). A chaque nouvelle question
// de ciblage, la table defile jusqu'a la premiere cible allumee de la table.
// Une seule fois par question : on ne se bat pas contre le doigt du joueur.
import { useEffect } from 'react'
import type { EtatInteractif } from '../interaction'

/** La signature d'une question de ciblage : ses cibles, triees. */
export function cleDesCibles(interactifs: Map<number, EtatInteractif> | undefined): string {
  if (!interactifs) return ''
  const ids: number[] = []
  for (const [id, etat] of interactifs) if (etat.role === 'cible') ids.push(id)
  return ids.sort((a, b) => a - b).join(',')
}

export function useDefilerVersLaCible(interactifs: Map<number, EtatInteractif> | undefined): void {
  const cle = cleDesCibles(interactifs)
  useEffect(() => {
    if (!cle) return
    const demande = window.requestAnimationFrame(() => {
      const cible = document.querySelector<HTMLElement>('.portrait-table .scan-card.state-targetable')
      if (!cible || typeof cible.scrollIntoView !== 'function') return
      cible.scrollIntoView({ block: 'nearest', inline: 'nearest', behavior: 'smooth' })
    })
    return () => window.cancelAnimationFrame(demande)
  }, [cle])
}
