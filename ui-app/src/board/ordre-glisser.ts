// PERMUTER LES CARTES D'UNE SELECTION ORDONNEE AU GLISSER-DEPOSER.
//
// Demande de Yarro (nice-to-have du 28/09/2026, fiche 2026-09-28-nice-to-have-
// yarro.md), vue sur Felt Table et Flesh and Blood. Decision de l'utilisateur du
// 28/09 : EN PLUS des pastilles numerotees et des boutons « ← »/« → », pas a
// leur place. Les deux gestes passent par la meme `permuterCibles` de
// `interaction.ts` : lacher une carte choisie sur une autre carte choisie les
// echange, comme les boutons le font avec le voisin.
//
// ⚠ GLISSER-DEPOSER NATIF DU NAVIGATEUR, pas le glisser du plateau (`glisser/`) :
// ici on echange deux cartes d'une RANGEE de selection, il n'y a ni zone ni
// cible de jeu. Le clic reste le clic (le navigateur n'en emet pas apres un
// glisser).
//
// Seules les cartes qui portent `permuterAvec` participent : il n'existe que
// pour une carte DEJA choisie d'une selection dont l'ordre compte.

import { useCallback, useState, type DragEvent } from 'react'

/** Ce que la rangee pose sur l'enveloppe d'une carte. */
export type PropsOrdreGlisser = {
  className: string
  draggable?: true
  onDragStart?: (e: DragEvent) => void
  onDragOver?: (e: DragEvent) => void
  onDragLeave?: () => void
  onDrop?: (e: DragEvent) => void
  onDragEnd?: () => void
}

export function useOrdreGlisser(): (
  id: string,
  permuterAvec: ((autreId: number) => void) | undefined,
  classeDeBase: string
) => PropsOrdreGlisser {
  const [source, setSource] = useState<string | undefined>()
  const [dessus, setDessus] = useState<string | undefined>()
  const fin = useCallback(() => {
    setSource(undefined)
    setDessus(undefined)
  }, [])

  return (id, permuterAvec, classeDeBase) => {
    if (!permuterAvec) return { className: classeDeBase }
    const classes = [classeDeBase, 'est-permutable']
    if (source === id) classes.push('est-glisse')
    if (dessus === id && source !== undefined && source !== id) classes.push('est-depot')
    return {
      className: classes.join(' '),
      draggable: true,
      onDragStart: (e) => {
        e.dataTransfer.effectAllowed = 'move'
        // Firefox ne lance pas le glisser sans une donnee.
        e.dataTransfer.setData('text/plain', id)
        setSource(id)
      },
      onDragOver: (e) => {
        if (source === undefined || source === id) return
        e.preventDefault()
        e.dataTransfer.dropEffect = 'move'
        setDessus(id)
      },
      onDragLeave: () => setDessus((actuel) => (actuel === id ? undefined : actuel)),
      onDrop: (e) => {
        e.preventDefault()
        const autre = Number(source)
        fin()
        if (source !== undefined && source !== id && Number.isFinite(autre)) permuterAvec(autre)
      },
      onDragEnd: fin,
    }
  }
}
