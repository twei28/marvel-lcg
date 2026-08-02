// Les couches ouvertes par-dessus la vue d'etat, de la plus ancienne a la plus
// recente. Le retour d'Android ferme la couche du SOMMET, une a la fois : c'est
// pour cela qu'on tient une pile et pas un booleen par couche.
//
// La partie pure est ici et testee ; le hook ci-dessous la relie a l'historique
// du navigateur.

import { useCallback, useEffect, useState } from 'react'
import type { CleBande } from './bandes'

export type Couche =
  | { sorte: 'focus'; bande: CleBande }
  | { sorte: 'carte'; id: string }

function memeCouche(a: Couche, b: Couche): boolean {
  if (a.sorte !== b.sorte) return false
  if (a.sorte === 'focus' && b.sorte === 'focus') return a.bande === b.bande
  if (a.sorte === 'carte' && b.sorte === 'carte') return a.id === b.id
  return false
}

export function sommet(pile: Couche[]): Couche | undefined {
  return pile[pile.length - 1]
}

/** Empiler la couche deja au sommet ne fait rien : un double tap ne cree pas deux feuilles. */
export function empiler(pile: Couche[], couche: Couche): Couche[] {
  const haut = sommet(pile)
  if (haut && memeCouche(haut, couche)) return pile
  return [...pile, couche]
}

export function depiler(pile: Couche[]): Couche[] {
  return pile.slice(0, -1)
}

/**
 * Relie la pile a l'historique du navigateur : une entree par couche ouverte,
 * pour que le bouton retour d'Android ferme la feuille du dessus au lieu de
 * quitter la partie.
 *
 * Les effets de bord sur history NE VIVENT PAS dans les fonctions passees a
 * setPile. En StrictMode (developpement), React invoque deux fois la fonction
 * d'un setState fonctionnel pour verifier sa purete ; un pushState() loge la
 * dedans partirait donc deux fois pour une seule ouverture, et la pile se
 * desynchroniserait de l'historique (le mal que cette pile existe pour
 * eviter). On lit donc l'etat courant depuis le closure du gestionnaire
 * d'evenement (rendu a chaque changement de pile), on calcule la pile
 * suivante avec les fonctions pures ci-dessus, on effectue l'effet de bord
 * une seule fois, puis on pose la valeur deja calculee dans setPile.
 */
export function useCouches(): {
  pile: Couche[]
  ouvrir: (couche: Couche) => void
  fermer: () => void
  toutFermer: () => void
} {
  const [pile, setPile] = useState<Couche[]>([])

  const ouvrir = useCallback(
    (couche: Couche) => {
      const suivante = empiler(pile, couche)
      if (suivante === pile) return
      window.history.pushState({ couche: suivante.length }, '')
      setPile(suivante)
    },
    [pile]
  )

  // Fermer se fait TOUJOURS par history.back() : le gestionnaire de popstate
  // ci-dessous est alors le seul endroit qui retire une couche, et la pile ne
  // peut pas se desynchroniser de l'historique.
  const fermer = useCallback(() => {
    window.history.back()
  }, [])

  const toutFermer = useCallback(() => {
    if (pile.length > 0) window.history.go(-pile.length)
  }, [pile])

  useEffect(() => {
    const surRetour = () => setPile((precedente) => depiler(precedente))
    window.addEventListener('popstate', surRetour)
    return () => window.removeEventListener('popstate', surRetour)
  }, [])

  return { pile, ouvrir, fermer, toutFermer }
}
