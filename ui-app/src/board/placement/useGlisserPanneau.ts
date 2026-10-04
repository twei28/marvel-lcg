/**
 * Déplacer un panneau de décision à la poignée, à la souris ou au doigt.
 *
 * Demande de l'utilisateur (relayée depuis Yarro, 28/09/2026) : deux
 * décisions qui arrivent coup sur coup posent deux panneaux l'un sur
 * l'autre, et rien ne permet d'écarter celui du dessus pour voir ce qu'il
 * cache. `usePlacement` esquive déjà les CARTES automatiquement ; il ne
 * bouge jamais les PANNEAUX entre eux par choix assumé (voir son
 * commentaire : un panneau qui saute tout seul est pire qu'un panneau fixe).
 * Ce hook ne change rien à ce choix — il ajoute un déplacement volontaire,
 * à la main, par-dessus la position calculée.
 *
 * ⚠ POINTER EVENTS, MEME CONVENTION QUE `useGlisser.ts` (glisser de cartes) :
 * couvre souris et tactile avec le meme code, jamais l'API HTML5 de
 * glisser-deposer qui ne marche pas au doigt. Meme seuil avant de considerer
 * que le geste est un glisser plutot qu'un clic — utile ici aussi si jamais
 * la poignee finit par porter un bouton.
 */
import { useCallback, useEffect, useRef, useState } from 'react'
import type { CSSProperties } from 'react'
import type { PointerEvent as ReactPointerEvent } from 'react'

const SEUIL_GLISSER = 6

export type Decalage = { dx: number; dy: number }

const REPOS: Decalage = { dx: 0, dy: 0 }

/**
 * Applique `decalage` par-dessus un `style` deja calcule (par `usePlacement`,
 * ou une position CSS fixe) : factorise le `calc()` repete dans chaque
 * panneau glissable (demande de l'utilisateur, 28/09/2026 -- « toutes les
 * fenetres, tous les panneaux »). N'ecrit rien quand le panneau n'a pas
 * bouge, pour ne pas poser un style inline la ou le CSS suffit.
 */
export function styleAvecDecalage(style: CSSProperties, decalage: Decalage): CSSProperties {
  if (decalage.dx === 0 && decalage.dy === 0) return style
  return {
    ...style,
    left: style.left !== undefined ? `calc(${style.left} + ${decalage.dx}px)` : style.left,
    top: style.top !== undefined ? `calc(${style.top} + ${decalage.dy}px)` : style.top,
  }
}

/**
 * Variante pour un panneau centre par son PARENT (`display: grid/flex;
 * place-items: center`), sans `left`/`top` propres : le decalage se pose en
 * `transform`, qui ne perturbe pas le calcul de mise en page du parent.
 * Ne pose rien tant que le panneau n'a pas bouge, comme `styleAvecDecalage`.
 */
export function transformDecalage(decalage: Decalage): CSSProperties | undefined {
  if (decalage.dx === 0 && decalage.dy === 0) return undefined
  return { transform: `translate(${decalage.dx}px, ${decalage.dy}px)` }
}

export function useGlisserPanneau(signature: string) {
  const [decalage, setDecalage] = useState<Decalage>(REPOS)
  const depart = useRef<{
    x: number
    y: number
    base: Decalage
    pointerId: number
    element: HTMLElement
  } | null>(null)
  const commence = useRef(false)

  // Une position gardee par-dessus une decision qui n'existe plus deroute
  // plus qu'elle n'aide : on repart du placement calcule a chaque nouvelle
  // decision, jamais de la derniere position choisie a la main.
  useEffect(() => {
    setDecalage(REPOS)
  }, [signature])

  // ⚠ LE SUIVI SE FAIT SUR LA FENETRE, PAS SEULEMENT SUR LA POIGNEE (01/10/2026).
  // La capture du pointeur ne se pose qu'APRES le seuil de 6 px, dans
  // `onPointerMove` de la poignee. Une poignee mince (le bandeau rouge d'un
  // cartouche fait une trentaine de pixels) est quittee par la souris avant
  // ce seuil : les mouvements vont alors a l'element dessous, la poignee ne
  // les voit plus et la fenetre ne bouge pas. Les tests qui appelaient les
  // gestionnaires a la main ne pouvaient pas le voir ; mesure dans un vrai
  // navigateur avec une vraie souris.
  const ecouteurs = useRef<{ pointermove: (e: PointerEvent) => void; fin: () => void } | null>(null)

  const retirerEcouteurs = useCallback(() => {
    const courants = ecouteurs.current
    if (!courants) return
    window.removeEventListener('pointermove', courants.pointermove)
    window.removeEventListener('pointerup', courants.fin)
    window.removeEventListener('pointercancel', courants.fin)
    ecouteurs.current = null
  }, [])

  const oublier = useCallback(() => {
    const debut = depart.current
    if (debut) {
      try {
        debut.element.releasePointerCapture(debut.pointerId)
      } catch {
        /* capture deja rendue ou jamais posee : rien a faire */
      }
    }
    depart.current = null
    commence.current = false
    retirerEcouteurs()
  }, [retirerEcouteurs])

  useEffect(() => retirerEcouteurs, [retirerEcouteurs])

  const suivre = useCallback((clientX: number, clientY: number) => {
    const debut = depart.current
    if (!debut) return
    const dx = clientX - debut.x
    const dy = clientY - debut.y
    if (!commence.current) {
      if (Math.hypot(dx, dy) < SEUIL_GLISSER) return
      commence.current = true
      try {
        window.getSelection()?.removeAllRanges()
      } catch {
        /* pas de selection a effacer */
      }
      try {
        debut.element.setPointerCapture(debut.pointerId)
      } catch {
        /* le navigateur refuse : on suit le pointeur sans capture */
      }
    }
    setDecalage({ dx: debut.base.dx + dx, dy: debut.base.dy + dy })
  }, [])

  const onPointerDown = useCallback(
    (evenement: ReactPointerEvent<HTMLElement>) => {
      if (evenement.pointerType === 'mouse' && evenement.button !== 0) return
      retirerEcouteurs()
      depart.current = {
        x: evenement.clientX,
        y: evenement.clientY,
        base: decalage,
        pointerId: evenement.pointerId,
        element: evenement.currentTarget,
      }
      commence.current = false
      const pointermove = (e: PointerEvent) => suivre(e.clientX, e.clientY)
      ecouteurs.current = { pointermove, fin: oublier }
      window.addEventListener('pointermove', pointermove)
      window.addEventListener('pointerup', oublier)
      window.addEventListener('pointercancel', oublier)
    },
    [decalage, retirerEcouteurs, suivre, oublier]
  )

  const onPointerMove = useCallback(
    (evenement: ReactPointerEvent<HTMLElement>) => suivre(evenement.clientX, evenement.clientY),
    [suivre]
  )

  const onPointerUp = useCallback(
    (_evenement: ReactPointerEvent<HTMLElement>) => {
      oublier()
    },
    [oublier]
  )

  return {
    decalage,
    aBouge: decalage.dx !== 0 || decalage.dy !== 0,
    gestes: { onPointerDown, onPointerMove, onPointerUp, onPointerCancel: oublier },
  }
}
