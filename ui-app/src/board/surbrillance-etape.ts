// Les cartes concernees par l'etape du deroule, allumees SUR LA TABLE.
//
// Choix de l'utilisateur apres le rapport Yarro n46 (03/10/2026) : pendant une
// etape de la phase du mechant, les cartes en cause (Rhino, la manigance visee,
// la carte revelee et ce qu'elle declenche) prennent un contour sur la table,
// SANS AUCUN MOUVEMENT ; le recit, lui, se lit dans la console.
//
// Une FEUILLE DE STYLE injectee, et non une classe posee sur les cartes : React
// reecrit `className` a chaque rendu de la table, et une classe ajoutee a la
// main disparaitrait au premier rafraichissement.
import { useEffect } from 'react'
import type { EtapeDeroule } from './deroule-phase'

/** Les identifiants des cartes concernees par une etape, consequences comprises. */
export function cartesConcernees(etape: EtapeDeroule | undefined): number[] {
  if (!etape) return []
  const ids = [etape.carteId, etape.cibleId, ...(etape.consequences ?? []).flatMap((c) => [c.carteId, c.cibleId])]
  return [...new Set(ids.filter((id): id is number => typeof id === 'number' && Number.isInteger(id)))]
}

/** La regle CSS qui allume ces cartes (vide sans carte). */
export function regleSurbrillance(ids: number[]): string {
  if (ids.length === 0) return ''
  const selecteurs = ids.map((id) => `.plateau-scene .scan-card[data-card-id="${id}"] .scan-frame`).join(',\n')
  return `${selecteurs} {\n  outline: 3px solid var(--surbrillance-etape, #f0c75e);\n  outline-offset: 3px;\n}`
}

export function useSurbrillanceEtape(ids: number[]): void {
  const cle = ids.join(',')
  useEffect(() => {
    const regle = regleSurbrillance(cle ? cle.split(',').map(Number) : [])
    if (!regle) return
    const feuille = document.createElement('style')
    feuille.dataset.surbrillanceEtape = ''
    feuille.textContent = regle
    document.head.appendChild(feuille)
    return () => feuille.remove()
  }, [cle])
}
