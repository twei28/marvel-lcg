// Animation de CHARGE : la carte qui attaque (ou thwart) fonce jusqu'a sa
// cible, marque un temps, puis revient a sa place.
//
// Transposition de l'animation du client original (public/js/marvel/
// card_animation.ts, animation_attack_thwart) : le moteur cite les cartes de
// l'evenement en cours dans active_card_ids — [0] la cible, [1] l'agissante —
// et l'evenement donne le sens :
//   WhenUnitWouldTakeDamage / WhenDamageIsZero_Text -> attaque (voile rouge)
//   WhenSchemeWouldRemoveThreat                     -> thwart  (voile bleu)
//   WhenSchemeWouldPlaceThreat                      -> scheme  (voile bleu)
//
// Meme principe que CoucheAnimations (et memes garde-fous) : on lit le DOM
// (`.scan-card[data-card-id]`), on fait voler une carte fantome pendant que la
// vraie est masquee, et si quoi que ce soit manque on n'anime pas.

import { useEffect, useRef, useState } from 'react'
// Meme mesure que le placement des panneaux : une seule definition de boite
// d'ecran pour tout le plateau (voir placement/boites.ts).
import { boiteDe, type Boite } from './placement/boites'

const ALLER = 320
const PAUSE = 220
const RETOUR = 320
const MARGE = 80

/** evenement moteur -> type de charge (= classe CSS de teinte). */
const EVENEMENTS: Record<string, string> = {
  WhenUnitWouldTakeDamage: 'attaque',
  WhenDamageIsZero_Text: 'attaque',
  WhenSchemeWouldRemoveThreat: 'thwart',
  WhenSchemeWouldPlaceThreat: 'scheme',
}

type Charge = {
  cle: string
  type: string
  src: string
  depart: Boite
  /** translate/rotate d'arrivee, calcules une fois. */
  dx: number
  dy: number
  deg: number
  /** Ligne de visee : du centre de l'agissante au centre de la cible. */
  ligne: { x: number; y: number; longueur: number; deg: number }
}


/**
 * Inclinaison de la carte pendant le trajet : elle « pique » vers la cible,
 * mais sans jamais se retourner tete en bas (angle ramene dans [-90, 90]).
 */
function inclinaison(dx: number, dy: number): number {
  let deg = (Math.atan2(dy, dx) * 180) / Math.PI + 90
  while (deg > 180) deg -= 360
  while (deg < -180) deg += 360
  if (deg > 90) deg -= 180
  else if (deg < -90) deg += 180
  return deg
}

/** Meme memoire de module que CoucheAnimations, memes raisons (remontages). */
let dernierRender = -1
/**
 * Signature de la derniere charge jouee (evenement + cartes). Le moteur peut
 * garder le meme event_name sur plusieurs rendus consecutifs : sans ce garde,
 * la meme charge se rejouerait a chaque rendu. Deux vraies attaques successives
 * sont toujours separees par d'autres evenements (application des degats...),
 * qui remettent la signature a zero.
 */
let derniereSignature = ''

/** Le fantome : depart -> cible (aller), pause, retour, en pur CSS transition. */
function CarteChargeante({ charge }: { charge: Charge }) {
  const [phase, setPhase] = useState<'depart' | 'aller' | 'retour'>('depart')
  useEffect(() => {
    const t1 = window.setTimeout(() => setPhase('aller'), 20)
    const t2 = window.setTimeout(() => setPhase('retour'), 20 + ALLER + PAUSE)
    return () => {
      window.clearTimeout(t1)
      window.clearTimeout(t2)
    }
  }, [])

  const b = charge.depart
  const transform =
    phase === 'aller'
      ? `translate(${b.x + charge.dx}px, ${b.y + charge.dy}px) rotate(${charge.deg}deg) scale(1.06)`
      : `translate(${b.x}px, ${b.y}px)`
  return (
    <>
      <div
        className={`ligne-cible charge-${charge.type}`}
        style={{
          left: `${charge.ligne.x}px`,
          top: `${charge.ligne.y}px`,
          width: phase === 'aller' ? `${charge.ligne.longueur}px` : '0px',
          transform: `rotate(${charge.ligne.deg}deg)`,
        }}
      />
      <div
        className={`charge-carte charge-${charge.type}`}
        style={{ width: `${b.w}px`, height: `${b.h}px`, transform }}
      >
        <img src={charge.src} alt="" />
      </div>
    </>
  )
}

export function CoucheCharge({
  renderId,
  eventName,
  activeIds,
  actif,
}: {
  renderId: number
  eventName: string
  activeIds: number[]
  actif: boolean
}) {
  const [charges, setCharges] = useState<Charge[]>([])
  const compteur = useRef(0)

  useEffect(() => {
    if (renderId === dernierRender) return
    dernierRender = renderId

    if (!actif) return
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return

    const type = EVENEMENTS[eventName]
    if (!type || activeIds.length < 2) {
      derniereSignature = ''
      return
    }
    const [cibleId, agissantId] = [activeIds[0], activeIds[1]]
    if (cibleId === agissantId) return
    const signature = `${eventName}:${cibleId}:${agissantId}`
    if (signature === derniereSignature) return
    derniereSignature = signature

    const scene = document.querySelector('.plateau-scene')
    if (!scene) return
    const elAgissant = scene.querySelector<HTMLElement>(`.scan-card[data-card-id="${agissantId}"]`)
    const elCible = scene.querySelector<HTMLElement>(`.scan-card[data-card-id="${cibleId}"]`)
    if (!elAgissant || !elCible) return
    const img = elAgissant.querySelector('img')
    if (!(img instanceof HTMLImageElement) || !img.src) return

    const depart = boiteDe(elAgissant)
    const cible = boiteDe(elCible)
    // Direction : du centre de l'agissante vers le centre de la cible...
    let dx = cible.x + cible.w / 2 - (depart.x + depart.w / 2)
    let dy = cible.y + cible.h / 2 - (depart.y + depart.h / 2)
    // Ligne de visee : centre a centre, comme UI.drawLine du client original.
    const ligne = {
      x: depart.x + depart.w / 2,
      y: depart.y + depart.h / 2,
      longueur: Math.hypot(dx, dy),
      deg: (Math.atan2(dy, dx) * 180) / Math.PI,
    }
    // ... mais on s'arrete au POINT DE CONTACT, au bord de la cible, sans la
    // recouvrir : elle doit rester lisible pendant le coup — c'est sur elle que
    // s'affichent les degats subis ou la menace retiree (card-effect-delta).
    const distance = Math.hypot(dx, dy)
    if (distance > 1) {
      const recul = Math.min(distance, cible.h / 2 + depart.h * 0.2)
      const facteur = (distance - recul) / distance
      dx *= facteur
      dy *= facteur
    }

    const charge: Charge = {
      cle: `c${compteur.current++}`,
      type,
      src: img.src,
      depart,
      dx,
      dy,
      deg: inclinaison(dx, dy),
      ligne,
    }

    // La vraie carte disparait pendant le vol du fantome, comme CoucheAnimations.
    elAgissant.style.visibility = 'hidden'
    const total = 20 + ALLER + PAUSE + RETOUR + MARGE
    window.setTimeout(() => {
      elAgissant.style.visibility = ''
    }, total)

    setCharges((c) => [...c, charge])
    window.setTimeout(() => {
      setCharges((c) => c.filter((x) => x.cle !== charge.cle))
    }, total)
  }, [renderId, eventName, activeIds, actif])

  if (charges.length === 0) return null
  return (
    <div className="couche-animations couche-charges" aria-hidden="true">
      {charges.map((charge) => (
        <CarteChargeante key={charge.cle} charge={charge} />
      ))}
    </div>
  )
}
