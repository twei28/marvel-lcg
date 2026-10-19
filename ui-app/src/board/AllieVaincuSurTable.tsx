// L'ALLIE VAINCU, « SUR LA TABLE » (T17, 19/10/2026).
//
// Avant : un allie a zero PV disparaissait en defausse sans un mot, et on ne
// l'apprenait qu'au bilan (« Hulk a pris 1 degat 0/5 »). Maintenant, l'etape
// « Hulk est vaincu » vient juste apres le coup : la carte est LUE au centre
// (le temps de la reconnaitre), puis PART EN DEFAUSSE d'un court mouvement, et la
// ligne du bandeau le dit. Le clic de l'etape reste le seul qui avance.
//
// Le HEROS vaincu, lui, garde sa fenetre (« X est vaincu · La phase s'arrete ici »).
import { useEffect, useLayoutEffect, useRef, useState, type CSSProperties } from 'react'
import type { ScanCardProps } from '../components/ScanCard'
import { ScanCardTraduite } from './traduction-carte'
import { cadreDuPlateau } from './mesures-plateau'
import { placesDeLecture, type Boite } from './places-rencontre'
import { animationsCoupees } from './TrajetsPhase'
import './allie-vaincu.css'

/** La carte reste lisible ce temps, puis part. */
export const DUREE_LECTURE_ALLIE_MS = 1300
export const DUREE_VOL_ALLIE_MS = 650

/** Ou la carte est maintenant sur la table : sa place en defausse (le monde est deja a jour). */
function boiteEnDefausse(id: number): Boite | undefined {
  const cadre = cadreDuPlateau()
  if (!cadre) return undefined
  const el = Array.from(cadre.element.querySelectorAll<HTMLElement>(`.scan-card[data-card-id="${id}"]`)).find(
    (e) => !e.closest('.allie-vaincu, .rencontre-sur-table, .carte-apercu, .deroule-phase')
  )
  if (!el) return undefined
  const r = (el.querySelector('.scan-frame') ?? el).getBoundingClientRect()
  if (r.width === 0 || r.height === 0) return undefined
  return { x: r.left - cadre.origine.left, y: r.top - cadre.origine.top, w: r.width, h: r.height }
}

export function AllieVaincuSurTable({ id, props }: { id: number; props: ScanCardProps | undefined }) {
  const [phase, setPhase] = useState<'lecture' | 'depart' | 'fini'>(animationsCoupees() ? 'fini' : 'lecture')
  const [place, setPlace] = useState<Boite | undefined>()
  const noeud = useRef<HTMLDivElement | null>(null)
  const destination = useRef<Boite | undefined>(undefined)

  useLayoutEffect(() => {
    if (phase === 'fini') return
    const cadre = cadreDuPlateau()
    if (!cadre) {
      setPhase('fini')
      return
    }
    destination.current = boiteEnDefausse(id)
    setPlace(placesDeLecture(cadre.boite, [props?.isLandscape ? 176 / 127 : 127 / 176])[0])
    // eslint-disable-next-line react-hooks/exhaustive-deps -- une seule mesure par etape (la cle de l'etape remonte le composant)
  }, [])

  useEffect(() => {
    if (phase !== 'lecture' || !place) return
    const minuterie = window.setTimeout(() => setPhase('depart'), DUREE_LECTURE_ALLIE_MS)
    return () => window.clearTimeout(minuterie)
  }, [phase, place])

  useEffect(() => {
    if (phase !== 'depart') return
    const el = noeud.current
    const vers = destination.current
    const de = place
    if (!el || !de || !vers || !el.animate) {
      setPhase('fini')
      return
    }
    const a = el.animate(
      [
        { transform: 'translate3d(0, 0, 0) scale(1, 1)' },
        { transform: `translate3d(${vers.x - de.x}px, ${vers.y - de.y}px, 0) scale(${vers.w / de.w}, ${vers.h / de.h})` },
      ],
      { duration: DUREE_VOL_ALLIE_MS, easing: 'cubic-bezier(0.5, 0, 0.75, 0.4)', fill: 'forwards' }
    )
    a.finished.then(() => setPhase('fini')).catch(() => setPhase('fini'))
    return () => a.cancel()
  }, [phase, place])

  if (phase === 'fini' || !props || !place) {
    // Rien a montrer (carte inconnue de la scene, animations coupees) : la carte reste en defausse, visible.
    return null
  }
  return (
    <div className="allie-vaincu" data-phase={phase} aria-hidden="true">
      {/* La copie de la table se cache le temps du voyage : la lecture ne la double pas. */}
      <style>{`.plateau-cadre .scan-card[data-card-id="${id}"]:not(.allie-vaincu *) { visibility: hidden !important; }`}</style>
      <div
        ref={noeud}
        className="allie-vaincu-carte"
        style={{ left: place.x, top: place.y, width: place.w, '--lecture-w': `${place.w}px` } as CSSProperties}
      >
        <ScanCardTraduite
          {...props}
          taille="grande"
          state={undefined}
          exhausted={false}
          counters={undefined}
          schemeThreat={undefined}
          allyHp={undefined}
          stats={undefined}
          jauge={undefined}
          jetonMenace={undefined}
          jetonDegats={undefined}
          labelType={undefined}
          masquerType
          camp={undefined}
        />
      </div>
    </div>
  )
}
