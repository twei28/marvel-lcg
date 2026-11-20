/**
 * Redimensionner une fenetre flottante a la poignee (coin bas-droit), avec
 * memoire de la taille choisie — jumeau de `useGlisserPanneau` (deplacement)
 * et du couple `lireRatio`/`ecrireRatio` de `mobile/Encoche.tsx` (memoire),
 * pour le volet du tchat detache (chantier du 06/11/2026).
 *
 * ⚠ POINTER EVENTS, PAS LE `resize` CSS NATIF : le CSS ne marche pas au
 * doigt, meme convention que `useGlisserPanneau.ts`.
 */
import { useCallback, useEffect, useRef, useState } from 'react'
import type { CSSProperties, PointerEvent as ReactPointerEvent } from 'react'

export type Taille = { largeur: number; hauteur: number }

function bornee(taille: Taille, min: Taille, max: Taille): Taille {
  return {
    largeur: Math.min(max.largeur, Math.max(min.largeur, taille.largeur)),
    hauteur: Math.min(max.hauteur, Math.max(min.hauteur, taille.hauteur)),
  }
}

function lireTaille(memoire: string, defaut: Taille, min: Taille, max: Taille): Taille {
  try {
    const brut = JSON.parse(window.localStorage.getItem(memoire) ?? 'null') as Partial<Taille> | null
    if (brut && Number.isFinite(brut.largeur) && Number.isFinite(brut.hauteur)) {
      return bornee({ largeur: Number(brut.largeur), hauteur: Number(brut.hauteur) }, min, max)
    }
  } catch {
    /* stockage refuse ou valeur abimee : le defaut */
  }
  return defaut
}

export function useFenetreFlottante(memoire: string, defaut: Taille, min: Taille, max: Taille) {
  const [taille, setTaille] = useState<Taille>(() => lireTaille(memoire, defaut, min, max))

  useEffect(() => {
    try {
      window.localStorage.setItem(memoire, JSON.stringify(taille))
    } catch {
      /* stockage refuse : la taille vaut pour la session */
    }
  }, [memoire, taille])

  const depart = useRef<{ x: number; y: number; base: Taille; pointerId: number; element: HTMLElement } | null>(null)

  const onPointerDown = useCallback(
    (evenement: ReactPointerEvent<HTMLElement>) => {
      if (evenement.pointerType === 'mouse' && evenement.button !== 0) return
      depart.current = {
        x: evenement.clientX,
        y: evenement.clientY,
        base: taille,
        pointerId: evenement.pointerId,
        element: evenement.currentTarget,
      }
      try {
        evenement.currentTarget.setPointerCapture(evenement.pointerId)
      } catch {
        /* le navigateur refuse : on suit le pointeur sans capture */
      }
    },
    [taille]
  )

  const onPointerMove = useCallback(
    (evenement: ReactPointerEvent<HTMLElement>) => {
      const debut = depart.current
      if (!debut) return
      const dx = evenement.clientX - debut.x
      const dy = evenement.clientY - debut.y
      setTaille(bornee({ largeur: debut.base.largeur + dx, hauteur: debut.base.hauteur + dy }, min, max))
    },
    [min, max]
  )

  const finir = useCallback((evenement: ReactPointerEvent<HTMLElement>) => {
    const debut = depart.current
    if (debut) {
      try {
        debut.element.releasePointerCapture(debut.pointerId)
      } catch {
        /* capture deja rendue ou jamais posee */
      }
    }
    depart.current = null
  }, [])

  return {
    taille,
    poignee: { onPointerDown, onPointerMove, onPointerUp: finir, onPointerCancel: finir },
  }
}

/** Applique `taille` a un style de fenetre flottante. */
export function styleAvecTaille(style: CSSProperties, taille: Taille): CSSProperties {
  return { ...style, width: taille.largeur, height: taille.hauteur }
}
