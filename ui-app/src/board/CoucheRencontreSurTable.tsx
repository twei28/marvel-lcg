// Une seule lecture par identité de carte : paquet → centre → clic → destination.
// Le parent garde son étape tant que valider() n'a pas terminé les trajets.
import { useEffect, useImperativeHandle, useLayoutEffect, useRef, useState, type CSSProperties, type Ref } from 'react'
import type { ScanCardProps } from '../components/ScanCard'
import { ScanCardTraduite } from './traduction-carte'
import type { EtapeDeroule } from './deroule-phase'
import { sceneDe } from './deroule-scene'
import { t } from './langue'
import { boiteDeCarte, boiteDuDeckRencontre, cadreDuPlateau, destinationDeLaCarte } from './mesures-plateau'
import { placesDeLecture, placesDesBoosts, type Boite } from './places-rencontre'
import { animationsCoupees } from './TrajetsPhase'
import './rencontre-sur-table.css'

export const DUREE_VOL_MS = 2000
export const DUREE_ENTREE_MS = 900

export type ControleRencontre = {
  /** Consomme le clic pendant l'entrée ou le départ ; rappelle suite à l'arrivée. */
  valider: (suite: () => void) => boolean
}

type CarteLue = { id: number; props: ScanCardProps; boost: boolean }
type Props = {
  etape: EtapeDeroule | undefined
  boostsMontres: number
  carteScene?: (id: number, faceVisible: boolean) => ScanCardProps | undefined
  dosRencontre?: ScanCardProps
  actif: boolean
  controle?: Ref<ControleRencontre>
}

export function CoucheRencontreSurTable({ etape, boostsMontres, carteScene, actif, controle }: Props) {
  const cartes: CarteLue[] = []
  if (actif && etape) {
    for (const c of sceneDe(etape).cartes) {
      if (c.role !== 'boost' && c.role !== 'revelee') continue
      if (c.role === 'boost' && cartes.filter((p) => p.boost).length >= boostsMontres) continue
      const props = carteScene?.(c.id, true)
      if (props) cartes.push({ id: c.id, props, boost: c.role === 'boost' })
    }
  }
  // Une entrée enrichie en révélation conserve exactement la même lecture.
  const identite = cartes.map((c) => `${c.boost ? 'boost' : 'carte'}:${c.id}`).join(',')
  const apport = etape?.boosts.slice(0, boostsMontres).reduce((s, b) => s + (b.apport ?? 0), 0) ?? 0
  return <LectureRencontre key={identite} cartes={cartes} apport={apport} auteurId={etape?.carteId} controle={controle} />
}

function LectureRencontre({ cartes, apport, auteurId, controle }: { cartes: CarteLue[]; apport: number; auteurId?: number; controle?: Ref<ControleRencontre> }) {
  const couche = useRef<HTMLDivElement>(null)
  const [ancres, setAncres] = useState<{ deck: Boite; cadre: Boite; auteur?: Boite }>()
  const etat = useRef<'entree' | 'lecture' | 'depart' | 'termine'>('entree')
  const [phase, setPhase] = useState(etat.current)
  const vols = useRef<Animation[]>([])
  const suivis = useRef<Array<() => void>>([])
  const generation = useRef(0)
  const suiteEnAttente = useRef<(() => void) | undefined>(undefined)
  const commande = useRef<ControleRencontre | undefined>(undefined)
  const cartesRef = useRef(cartes)
  cartesRef.current = cartes

  useLayoutEffect(() => {
    if (!cartesRef.current.length) return
    const mesurer = () => {
      const c = cadreDuPlateau()
      const deck = c && boiteDuDeckRencontre(c)
      if (c && deck) setAncres({ deck, cadre: c.boite, auteur: boiteDeCarte(auteurId, c) })
    }
    mesurer()
    window.addEventListener('resize', mesurer)
    return () => window.removeEventListener('resize', mesurer)
  }, [auteurId])

  useEffect(() => () => {
    generation.current++
    for (const arreter of suivis.current) arreter()
    for (const a of vols.current) a.cancel()
    suiteEnAttente.current = undefined
  }, [])

  const changer = (p: typeof phase) => { etat.current = p; setPhase(p) }
  const elements = () => Array.from(couche.current?.querySelectorAll<HTMLElement>('.rencontre-sortie') ?? [])

  // Les transformations portent sur une boîte aux dimensions de LECTURE,
  // sans modifier --card-w au départ : aucune double mise à l'échelle.
  const animer = (el: HTMLElement, de: Boite, vers: Boite, duree: number, delai = 0, destination?: () => Boite | undefined) => {
    const c = cadreDuPlateau()
    const r = el.getBoundingClientRect()
    const origine = { x: r.left - (c?.origine.left ?? 0), y: r.top - (c?.origine.top ?? 0), w: r.width, h: r.height }
    const pose = (b: Boite) => {
      const base = el.offsetWidth > 0 ? { x: el.offsetLeft, y: el.offsetTop, w: el.offsetWidth, h: el.offsetHeight } : origine
      return `translate(${b.x - base.x}px, ${b.y - base.y}px) scale(${b.w / Math.max(1, base.w)}, ${b.h / Math.max(1, base.h)})`
    }
    if (animationsCoupees() || !el.animate) return Promise.resolve()
    const a = el.animate([{ transform: pose(de) }, { transform: pose(vers) }], {
      duration: duree, delay: delai, fill: 'both', easing: 'cubic-bezier(0.25, 0.7, 0.3, 1)',
    })
    vols.current.push(a)
    if (destination) {
      let image = 0
      let arrete = false
      let derniere = vers
      const suivre = () => {
        if (arrete) return
        const cible = destination()
        // La table peut se réorganiser ou être redimensionnée pendant le vol.
        // On conserve sa progression et on actualise seulement sa destination.
        if (cible && (cible.x !== derniere.x || cible.y !== derniere.y || cible.w !== derniere.w || cible.h !== derniere.h)) {
          derniere = cible
          ;(a.effect as KeyframeEffect | null)?.setKeyframes([{ transform: pose(de) }, { transform: pose(cible) }])
        }
        image = window.requestAnimationFrame(suivre)
      }
      const arreter = () => { arrete = true; window.cancelAnimationFrame(image) }
      suivis.current.push(arreter)
      image = window.requestAnimationFrame(suivre)
      void a.finished.then(arreter, arreter)
    }
    return a.finished
  }

  useLayoutEffect(() => {
    if (!ancres || etat.current !== 'entree') return
    const numero = ++generation.current
    const els = elements()
    const arrivees = els.map((el, i) => {
      const r = el.getBoundingClientRect()
      const vers = { x: r.left - (cadreDuPlateau()?.origine.left ?? 0), y: r.top - (cadreDuPlateau()?.origine.top ?? 0), w: r.width, h: r.height }
      // Les boosts arrivent l'un après l'autre, puis restent lisibles ensemble.
      return animer(el, ancres.deck, vers, DUREE_ENTREE_MS, i * DUREE_ENTREE_MS)
    })
    void Promise.all(arrivees).then(() => {
      if (generation.current !== numero) return
      for (const a of vols.current) a.cancel()
      vols.current = []
      changer('lecture')
      const suite = suiteEnAttente.current
      suiteEnAttente.current = undefined
      if (suite) commande.current?.valider(suite)
    }).catch(() => { /* Annulation : une autre phase ou une autre partie a pris la main. */ })
    // Seule l'arrivée des ancres déclenche l'entrée, jamais un enrichissement de l'étape.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [Boolean(ancres)])

  commande.current = {
    valider: (suite) => {
      if (!ancres || !cartes.length || etat.current === 'termine') return false
      if (etat.current === 'entree') {
        suiteEnAttente.current ??= suite
        return true
      }
      if (etat.current !== 'lecture') return true
      changer('depart')
      suiteEnAttente.current = suite
      const numero = ++generation.current
      const c = cadreDuPlateau()
      const els = elements()
      const places = placesDesBoosts(c ? boiteDeCarte(auteurId, c) ?? ancres.deck : ancres.deck, ancres.cadre, cartes.length)
      const trajets = els.map((el, i) => {
        const r = el.getBoundingClientRect()
        const de = { x: r.left - (c?.origine.left ?? 0), y: r.top - (c?.origine.top ?? 0), w: r.width, h: r.height }
        const destination = () => {
          const actuel = cadreDuPlateau()
          const cible = cartes[i].boost
            ? actuel ? placesDesBoosts(boiteDeCarte(auteurId, actuel) ?? ancres.deck, actuel.boite, cartes.length)[i] : places[i]
            : actuel ? destinationDeLaCarte(cartes[i].id, actuel) : undefined
          // Une carte paysage garde son orientation, même si la pile ou
          // l'attaquant qui sert d'ancre est dessiné en portrait.
          const facteur = cible ? Math.min(cible.w / de.w, cible.h / de.h) : 1
          return cible ? { x: cible.x, y: cible.y, w: de.w * facteur, h: de.h * facteur } : undefined
        }
        const vers = destination()
        return vers ? animer(el, de, vers, DUREE_VOL_MS, 0, destination) : Promise.resolve()
      })
      void Promise.all(trajets).then(() => {
        if (generation.current !== numero) return
        changer('termine')
        const continuer = suiteEnAttente.current
        suiteEnAttente.current = undefined
        continuer?.()
      }).catch(() => { /* Une navigation annule aussi la continuation périmée. */ })
      return true
    },
  }
  useImperativeHandle(controle, () => commande.current!)

  if (!ancres || !cartes.length) return null
  const places = placesDeLecture(ancres.cadre, cartes.map((c) => c.props.isLandscape ? 176 / 127 : 127 / 176))
  const ids = cartes.map((c) => c.id)
  return (
    <div ref={couche} className="rencontre-sur-table" data-lecture={phase} aria-hidden="true">
      {/* L'original garde sa place et reste mesurable pendant le voyage. */}
      <style>{phase !== 'termine' ? ids.map((id) => `.plateau-cadre .scan-card[data-card-id="${id}"]:not(.rencontre-sur-table *) { visibility: hidden !important; }`).join('\n') : ''}</style>
      {cartes.map((carte, i) => (
        <div key={carte.id} className={`rencontre-sortie ${carte.boost ? 'est-boost' : 'est-revelee'}`} style={{
          left: places[i].x, top: places[i].y, width: places[i].w, '--lecture-w': `${places[i].w}px`,
          visibility: phase === 'termine' ? 'hidden' : undefined,
        } as CSSProperties}>
          <ScanCardTraduite {...carte.props} taille="grande" state={undefined} exhausted={false} counters={undefined}
            schemeThreat={undefined} allyHp={undefined} stats={undefined} jauge={undefined} jetonMenace={undefined} jetonDegats={undefined}
            labelType={undefined} masquerType camp={undefined} />
        </div>
      ))}
      {cartes.length > 1 && phase === 'lecture' ? <div className="rencontre-total" style={{ left: places[0].x, top: Math.max(...places.map((p) => p.y + p.h)) + 12, width: places.at(-1)!.x + places.at(-1)!.w - places[0].x }}>{t('Boost')} +{apport}</div> : null}
    </div>
  )
}
