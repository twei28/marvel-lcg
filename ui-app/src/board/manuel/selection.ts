// LA MULTI-SELECTION DU MODE MANUEL (lot 5 du 07/10/2026), comme OCTGN :
// Ctrl+clic ajoute ou retire une carte, un rectangle trace sur une zone vide
// selectionne les cartes qu'il touche, un clic simple ailleurs vide tout. Une
// action faite sur une carte SELECTIONNEE s'applique a toute la selection (une
// `cardaction` d'OCTGN est jouee pour chaque carte selectionnee). Locale a cet
// ecran, comme dans OCTGN : personne d'autre ne voit ma selection.
import { useEffect, useState } from 'react'

let courante: ReadonlySet<number> = new Set()
const ECOUTEURS = new Set<(s: ReadonlySet<number>) => void>()

function publier(suivante: ReadonlySet<number>): void {
  courante = suivante
  for (const ecouteur of ECOUTEURS) ecouteur(courante)
}

export const selection = {
  lire: (): ReadonlySet<number> => courante,
  contient: (id: number): boolean => courante.has(id),
  basculer(id: number): void {
    const suivante = new Set(courante)
    if (suivante.has(id)) suivante.delete(id)
    else suivante.add(id)
    publier(suivante)
  },
  remplacer(ids: Iterable<number>): void {
    publier(new Set(ids))
  },
  vider(): void {
    if (courante.size > 0) publier(new Set())
  },
}

/** Les cartes sur lesquelles agit un geste fait sur `id` : toute la selection si elle la contient. */
export function cartesDuGeste(id: number): number[] {
  return courante.has(id) && courante.size > 1 ? [...courante] : [id]
}

export function useSelection(): ReadonlySet<number> {
  const [vue, setVue] = useState(courante)
  useEffect(() => {
    ECOUTEURS.add(setVue)
    setVue(courante)
    return () => {
      ECOUTEURS.delete(setVue)
    }
  }, [])
  return vue
}
