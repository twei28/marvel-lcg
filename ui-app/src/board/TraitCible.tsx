// Le trait qui relie l'attaquant a sa cible.
//
// Un SVG en position fixe par-dessus le plateau, jamais un dessin dans les
// cartes : il doit traverser la table sans etre rogne par les cadres, qui ont
// tous `overflow: hidden`.
//
// Les positions viennent de getBoundingClientRect au moment du rendu de
// l'etape. C'est suffisant : le plateau ne bouge pas pendant qu'une etape est
// affichee, et le trait disparait des que l'etape change.

import { useEffect, useState } from 'react'
import type { EtapeDeroule } from './deroule-phase'
import { sceneDe } from './deroule-scene'

type Segment = { x1: number; y1: number; x2: number; y2: number }

function centreDe(id: number): { x: number; y: number } | undefined {
  const el = document.querySelector<HTMLElement>(
    `.plateau-scene .scan-card[data-card-id="${id}"]`
  )
  if (!el) return undefined
  const r = el.getBoundingClientRect()
  return { x: r.left + r.width / 2, y: r.top + r.height / 2 }
}

export function TraitCible({
  etape,
  actif,
}: {
  etape: EtapeDeroule | undefined
  actif: boolean
}) {
  const [segment, setSegment] = useState<Segment | undefined>(undefined)

  // On depend de la CLE, pas de l'objet `etape` : cet objet est reconstruit a
  // chaque trame du moteur, meme quand rien n'a change. Meme piege deja
  // corrige dans pas-a-pas.ts et useDerouleScene.ts.
  const cle = etape?.cle
  useEffect(() => {
    if (!actif || !etape) {
      setSegment(undefined)
      return
    }
    const scene = sceneDe(etape)
    if (!scene.trait || scene.carteEnAvant === undefined || scene.cible === undefined) {
      setSegment(undefined)
      return
    }
    const depart = centreDe(scene.carteEnAvant)
    const arrivee = centreDe(scene.cible)
    // Une carte a pu quitter la table entre le fait et son affichage : on ne
    // trace pas un trait vers le vide.
    if (!depart || !arrivee) {
      setSegment(undefined)
      return
    }
    setSegment({ x1: depart.x, y1: depart.y, x2: arrivee.x, y2: arrivee.y })
    // eslint-disable-next-line react-hooks/exhaustive-deps -- `cle` suffit,
    // voir le commentaire ci-dessus.
  }, [cle, actif])

  if (!segment) return null

  return (
    <svg className="deroule-trait" aria-hidden="true">
      <defs>
        <marker
          id="deroule-pointe"
          markerWidth="8"
          markerHeight="8"
          refX="7"
          refY="4"
          orient="auto"
        >
          <path d="M0,0 L8,4 L0,8 z" fill="#F0131E" />
        </marker>
      </defs>
      <line
        x1={segment.x1}
        y1={segment.y1}
        x2={segment.x2}
        y2={segment.y2}
        markerEnd="url(#deroule-pointe)"
      />
    </svg>
  )
}
