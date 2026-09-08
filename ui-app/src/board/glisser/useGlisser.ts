/**
 * Le geste : prendre une carte, la promener, la lacher.
 *
 * ⚠ POINTER EVENTS, JAMAIS L'API HTML5 DE GLISSER-DEPOSER. L'ancien plateau
 * (`public/js/marvel/draggable.js`) tenait sur `mousedown` seul, ce qui le
 * rendait inerte au tactile ; l'API HTML5, elle, ne marche pas du tout au
 * doigt et impose son image fantome. Les Pointer Events couvrent les deux avec
 * le meme code, le jour ou le tactile viendra.
 *
 * ⚠ LE CLIC DOIT SURVIVRE INTACT. C'est la condition posee au chantier : le
 * glisser s'ajoute, il ne remplace rien. D'ou le SEUIL : tant que le pointeur
 * n'a pas franchi quelques pixels, il ne se passe RIEN, et le clic part comme
 * avant. Et quand le glisser a bien eu lieu, `onPointerUp` rend `true` pour
 * que l'appelant n'enchaine pas le clic par-dessus.
 */
import { useCallback, useRef, useState } from 'react'
import type { PointerEvent as ReactPointerEvent } from 'react'

/** Distance a franchir avant qu'un appui devienne un glisser, en pixels. */
export const SEUIL_GLISSER = 6

/** Ce qui se trouve sous le pointeur : une carte, une zone du plateau, rien. */
export type CibleSurvolee = { carteId?: number; zone?: string }

export type EtatGlisser = {
  sourceId: number
  /** Position du pointeur, en coordonnees ecran. */
  x: number
  y: number
  cible: CibleSurvolee
}

type Reglages = {
  /** Cette carte peut-elle etre soulevee ? */
  estSource: (id: number) => boolean
  /** Ce qui se trouve sous ce point de l'ecran. */
  cibleSous: (x: number, y: number) => CibleSurvolee
  /** Appele au lacher, seulement si un glisser a vraiment eu lieu. */
  onDepot: (sourceId: number, cible: CibleSurvolee, point: { x: number; y: number }) => void
}

export function useGlisser({ estSource, cibleSous, onDepot }: Reglages) {
  const [glisse, setGlisse] = useState<EtatGlisser | null>(null)
  const depart = useRef<{
    id: number
    x: number
    y: number
    pointerId: number
    element: HTMLElement
  } | null>(null)
  const commence = useRef(false)

  const oublier = useCallback(() => {
    const debut = depart.current
    if (debut) {
      // La capture peut avoir ete refusee ou deja rendue : on ne bruite pas.
      try {
        debut.element.releasePointerCapture(debut.pointerId)
      } catch {
        /* rien a rendre */
      }
    }
    depart.current = null
    commence.current = false
    setGlisse(null)
  }, [])

  const onPointerDown = useCallback(
    (evenement: ReactPointerEvent<HTMLElement>) => {
      // Bouton droit et bouton du milieu ne prennent pas de carte.
      if (evenement.pointerType === 'mouse' && evenement.button !== 0) return
      const sous = evenement.target
      if (!(sous instanceof HTMLElement)) return
      // Un bouton posé SUR une carte garde son clic : les piles, les tiroirs.
      if (sous.closest('button, a, input, select, textarea')) return
      const element = sous.closest<HTMLElement>('.scan-card')
      const id = Number(element?.dataset.cardId)
      if (!element || !Number.isFinite(id) || !estSource(id)) return
      depart.current = {
        id,
        x: evenement.clientX,
        y: evenement.clientY,
        pointerId: evenement.pointerId,
        element: evenement.currentTarget,
      }
      commence.current = false
    },
    [estSource]
  )

  const onPointerMove = useCallback(
    (evenement: ReactPointerEvent<HTMLElement>) => {
      const debut = depart.current
      if (!debut) return
      const dx = evenement.clientX - debut.x
      const dy = evenement.clientY - debut.y
      if (!commence.current) {
        if (Math.hypot(dx, dy) < SEUIL_GLISSER) return
        commence.current = true
        // ⚠ ON EFFACE LA SELECTION DU NAVIGATEUR. Bouton enfonce, le navigateur
        // SELECTIONNE ce qu'il survole, exactement comme sur une page de texte,
        // et peint les images et les mots en bleu. C'est ce bleu-la que
        // l'utilisateur a signale trois fois le 08/09/2026, et il n'avait rien
        // a voir avec les couleurs du plateau : « comme si il selectionnait les
        // images et le texte quand on reste appuye ».
        //
        // Le `user-select: none` pose sur le cadre (glisser.css) empeche les
        // selections SUIVANTES ; celle-ci a pu commencer pendant les six pixels
        // du seuil, avant qu'on sache que c'etait un glisser. On la retire donc
        // ici, une fois, au moment ou le geste est reconnu.
        try {
          window.getSelection()?.removeAllRanges()
        } catch {
          /* pas de selection a effacer */
        }
        // La capture garde le geste vivant quand le pointeur sort du cadre :
        // sans elle, sortir du plateau relachait la carte en silence.
        try {
          debut.element.setPointerCapture(debut.pointerId)
        } catch {
          /* le navigateur refuse : on suit le pointeur sans capture */
        }
      }
      setGlisse({
        sourceId: debut.id,
        x: evenement.clientX,
        y: evenement.clientY,
        cible: cibleSous(evenement.clientX, evenement.clientY),
      })
    },
    [cibleSous]
  )

  /** Rend `true` si un glisser s'achevait : l'appelant n'enchaine pas le clic. */
  const onPointerUp = useCallback(
    (evenement: ReactPointerEvent<HTMLElement>): boolean => {
      const debut = depart.current
      const aGlisse = commence.current
      const cible = aGlisse ? cibleSous(evenement.clientX, evenement.clientY) : undefined
      const source = debut?.id
      const point = { x: evenement.clientX, y: evenement.clientY }
      oublier()
      if (!aGlisse || source === undefined || !cible) return false
      onDepot(source, cible, point)
      return true
    },
    [cibleSous, oublier, onDepot]
  )

  return {
    glisse,
    gestes: { onPointerDown, onPointerMove, onPointerUp, onPointerCancel: oublier },
  }
}

/**
 * Ce qui se trouve sous un point de l'ecran : la carte d'abord, sa zone sinon.
 *
 * ⚠ `elementFromPoint` ET NON UN CALCUL DE RECTANGLES : le navigateur connait
 * deja l'empilement, les chevauchements de cartes et l'echelle de la scene.
 * La couche visuelle interne d'une carte (`.scan-visuel`) est en
 * `pointer-events: none`, donc c'est bien `.scan-card` qui est touchee, a sa
 * taille normale et non a son agrandissement au survol.
 */
export function cibleSousLePoint(x: number, y: number): CibleSurvolee {
  const sous = document.elementFromPoint(x, y)
  if (!(sous instanceof HTMLElement)) return {}
  const carte = sous.closest<HTMLElement>('.scan-card')
  const id = Number(carte?.dataset.cardId)
  const zone = sous.closest<HTMLElement>('[data-zone]')?.dataset.zone
  return {
    carteId: carte && Number.isFinite(id) ? id : undefined,
    zone: zone || undefined,
  }
}
