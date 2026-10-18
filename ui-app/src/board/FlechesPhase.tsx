// Les flèches de la phase du méchant (refonte, lot 3, essai, 12/10/2026).
//
// ⚠ CE COMPOSANT NE DÉCIDE RIEN : `fleches-phase.ts` dit quelles flèches
// l'étape appelle et comment les tracer. Ici on retrouve les rectangles à
// l'écran, on recadre la table si une cible est hors de vue (décision 25), et
// on dessine dans une couche fixe qui ne capte aucun clic.
//
// Une flèche dont un bout n'est pas à l'écran n'est PAS dessinée : un boost ★
// qui n'est pas entré en jeu n'a pas de place sur la table, et une carte morte
// a quitté l'index du monde. On ne tire jamais vers un point inventé.
import { useEffect, useLayoutEffect, useMemo, useRef, useState, type CSSProperties } from 'react'
import { createPortal } from 'react-dom'
import type { CadreJoueur } from './couleur-joueur'
import type { EtapeDeroule } from './deroule-phase'
import { flechesDeLEtape, traceEntre, type BoutFleche, type Rect, type TraceFleche } from './fleches-phase'
import './fleches-phase.css'

type Dessin = { cle: string; couleur: string; trace: TraceFleche }

export function rect(el: Element | null | undefined): Rect | undefined {
  if (!el) return undefined
  const r = el.getBoundingClientRect()
  if (r.width === 0 || r.height === 0) return undefined
  return { x: r.left, y: r.top, w: r.width, h: r.height }
}

/**
 * La carte de la table, jamais sa copie dans la boîte de phase, ni une carte
 * FACE CACHÉE : une carte rencontre distribuée attend encore près du méchant,
 * ce n'est pas sa place (mesuré le 12/10/2026 sur Trafiquant d'Armes).
 */
export function carteDeLaTable(id: number): HTMLElement | undefined {
  const candidates = document.querySelectorAll<HTMLElement>(`.plateau-cadre .scan-card[data-card-id="${id}"]`)
  for (const el of candidates) if (!el.closest('.deroule-phase, .rencontre-sur-table') && !el.classList.contains('is-facedown')) return el
  return undefined
}

export function elementDuBout(bout: BoutFleche): Element | undefined {
  if (bout.lieu === 'table') return carteDeLaTable(bout.id)
  // « Sur la table », sans fenêtre : il n'y a plus de boîte d'où partir. Les jetons et les
  // traits partent du MILIEU de la table (`TableSansModale`, `.tsm-depart`).
  const milieu = () => document.querySelector('.tsm-depart') ?? undefined
  const boite = document.querySelector('.deroule-phase.est-essai')
  if (!boite) return milieu()
  if (bout.lieu === 'boite') {
    return boite.querySelector(`.scan-card[data-card-id="${bout.id}"]`) ?? boite.querySelector('.deroule-corps') ?? milieu()
  }
  return boite.querySelector('.deroule-corps') ?? milieu()
}

/** Hors de la fenêtre : il faut recadrer la table avant de tirer la flèche. */
function horsDeVue(r: Rect): boolean {
  return r.x + r.w < 0 || r.y + r.h < 0 || r.x > window.innerWidth || r.y > window.innerHeight
}

export function FlechesPhase({
  etape,
  actif,
  cadres,
  joueurDeCarte,
  boostsMontres,
}: {
  etape: EtapeDeroule | undefined
  actif: boolean
  cadres: CadreJoueur[]
  joueurDeCarte: (id: number | undefined) => number | undefined
  boostsMontres?: number
}) {
  const specs = useMemo(
    () => (actif ? flechesDeLEtape(etape, { cadres, joueurDeCarte, boostsMontres }) : []),
    [actif, etape, cadres, joueurDeCarte, boostsMontres]
  )
  const signature = specs.map((s) => `${s.cle}:${s.couleur}`).join('|')
  const [dessins, setDessins] = useState<Dessin[]>([])
  const [fenetre, setFenetre] = useState({ w: 0, h: 0 })
  const recadree = useRef<string | undefined>(undefined)
  const [tour, setTour] = useState(0)

  useLayoutEffect(() => {
    if (specs.length === 0) {
      setDessins([])
      return
    }
    const mesurer = () => {
      const resultat: Dessin[] = []
      for (const spec of specs) {
        const cible = carteDeLaTable(spec.vers.id)
        const rCible = rect(cible)
        const rSource = rect(elementDuBout(spec.de))
        if (!rCible || !rSource) continue
        // Décision 25 : la table se recadre, puis la flèche se trace (une fois par étape).
        if (horsDeVue(rCible) && cible && recadree.current !== `${etape?.cle}>${spec.vers.id}`) {
          recadree.current = `${etape?.cle}>${spec.vers.id}`
          cible.scrollIntoView({ block: 'nearest', inline: 'nearest' })
          window.requestAnimationFrame(() => setTour((n) => n + 1))
          continue
        }
        resultat.push({ cle: spec.cle, couleur: spec.couleur, trace: traceEntre(rSource, rCible) })
      }
      setFenetre({ w: window.innerWidth, h: window.innerHeight })
      setDessins(resultat)
    }
    mesurer()
    window.addEventListener('resize', mesurer)
    window.addEventListener('scroll', mesurer, true)
    return () => {
      window.removeEventListener('resize', mesurer)
      window.removeEventListener('scroll', mesurer, true)
    }
    // `specs` change d'objet a chaque rendu du parent : sa signature suffit.
  }, [signature, etape?.cle, tour])

  // Les cartes de l'étape arrivent parfois encore (vol, rétrécissement de la
  // boîte) au premier rendu : deux mesures au repos.
  useEffect(() => {
    if (specs.length === 0) return
    const a = window.setTimeout(() => setTour((n) => n + 1), 260)
    const b = window.setTimeout(() => setTour((n) => n + 1), 720)
    return () => {
      window.clearTimeout(a)
      window.clearTimeout(b)
    }
  }, [signature, etape?.cle])

  if (!actif || dessins.length === 0 || typeof document === 'undefined') return null
  return createPortal(
    <svg
      key={`${etape?.cle ?? ''}|${etape?.etat ?? ''}|${signature}`}
      className="fleches-phase est-animee"
      viewBox={`0 0 ${fenetre.w} ${fenetre.h}`}
      width={fenetre.w}
      height={fenetre.h}
      aria-hidden="true"
      data-fleches={dessins.length}
    >
      {dessins.map(({ cle, couleur, trace }) => (
        <g
          key={cle}
          className="fleche-phase"
          data-fleche={cle}
          data-depart={`${Math.round(trace.depart.x)},${Math.round(trace.depart.y)}`}
          data-arrivee={`${Math.round(trace.arrivee.x)},${Math.round(trace.arrivee.y)}`}
          style={{ '--fleche-couleur': couleur, '--l': trace.longueur } as CSSProperties}
        >
          <path className="fleche-ombre" d={trace.d} />
          <path className="fleche-trait" d={trace.d} />
          <path className="fleche-pointe" d={trace.pointe} />
        </g>
      ))}
    </svg>,
    document.body
  )
}
