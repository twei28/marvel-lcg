// Portrait ou paysage ?
//
// La question n'est pas cosmétique : les deux orientations n'ont pas la même
// COMPOSITION. En portrait, quatre rangées empilées et les piles dans un tiroir.
// En paysage, la hauteur s'effondre mais la largeur s'ouvre : on repasse aux
// trois colonnes du plateau PC, et les piles y gagnent une colonne visible.
//
// C'est donc une décision de rendu, pas une media query : ce n'est pas la même
// arborescence qu'on dessine.

import { useEffect, useState } from 'react'

export const REQUETE_PAYSAGE = '(orientation: landscape)'

export function useOrientation(): 'portrait' | 'paysage' {
  const [paysage, setPaysage] = useState(
    () => typeof window !== 'undefined' && window.matchMedia(REQUETE_PAYSAGE).matches
  )

  useEffect(() => {
    const liste = window.matchMedia(REQUETE_PAYSAGE)
    const surChangement = (evenement: MediaQueryListEvent) => setPaysage(evenement.matches)
    liste.addEventListener('change', surChangement)
    return () => liste.removeEventListener('change', surChangement)
  }, [])

  return paysage ? 'paysage' : 'portrait'
}
