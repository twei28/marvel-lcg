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

/** Ou en est la lecture : les cartes arrivent, se lisent, partent. `aucune` : rien a lire. */
export type PhaseLecture = 'entree' | 'lecture' | 'depart' | 'termine' | 'aucune'

type CarteLue = { id: number; props: ScanCardProps; boost: boolean }
type Props = {
  etape: EtapeDeroule | undefined
  boostsMontres: number
  carteScene?: (id: number, faceVisible: boolean) => ScanCardProps | undefined
  dosRencontre?: ScanCardProps
  actif: boolean
  controle?: Ref<ControleRencontre>
  /** Annonce chaque changement de phase : le bandeau n'annonce les degats qu'une fois les boosts lisibles. */
  surPhase?: (phase: PhaseLecture) => void
}

export function CoucheRencontreSurTable({ etape, boostsMontres, carteScene, actif, controle, surPhase }: Props) {
  const cartes: CarteLue[] = []
  if (actif && etape) {
    for (const c of sceneDe(etape, true).cartes) {
      if (c.role !== 'boost' && c.role !== 'revelee') continue
      if (c.role === 'boost' && cartes.filter((p) => p.boost).length >= boostsMontres) continue
      const props = carteScene?.(c.id, true)
      if (props) cartes.push({ id: c.id, props, boost: c.role === 'boost' })
    }
  }
  // Une entrée enrichie en révélation conserve exactement la même lecture.
  const identite = cartes.map((c) => `${c.boost ? 'boost' : 'carte'}:${c.id}`).join(',')
  const apport = etape?.boosts.slice(0, boostsMontres).reduce((s, b) => s + (b.apport ?? 0), 0) ?? 0
  const rienALire = cartes.length === 0
  const boostsEnAttente = Boolean(etape && boostsMontres < etape.boosts.length &&
    etape.boosts.some((b) => carteScene?.(b.cibleId, true)))
  useEffect(() => {
    if (actif && rienALire && !boostsEnAttente) surPhase?.('aucune')
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [actif, rienALire, boostsEnAttente, etape?.cle])
  return <LectureRencontre key={identite} cartes={cartes} apport={apport} auteurId={etape?.carteId} controle={controle} surPhase={surPhase} />
}

function LectureRencontre({ cartes, apport, auteurId, controle, surPhase }: { cartes: CarteLue[]; apport: number; auteurId?: number; controle?: Ref<ControleRencontre>; surPhase?: (phase: PhaseLecture) => void }) {
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
  useEffect(() => {
    if (cartes.length > 0) surPhase?.(phase)
  }, [phase, cartes.length, surPhase])
  const elements = () => Array.from(couche.current?.querySelectorAll<HTMLElement>('.rencontre-sortie') ?? [])

  // Les transformations portent sur une boîte aux dimensions de LECTURE,
  // sans modifier --card-w au départ : aucune double mise à l'échelle.
  const animer = (el: HTMLElement, de: Boite, vers: Boite, duree: number, delai = 0, destination?: () => Boite | undefined) => {
    const c = cadreDuPlateau()
    const r = el.getBoundingClientRect()
    const origine = { x: r.left - (c?.origine.left ?? 0), y: r.top - (c?.origine.top ?? 0), w: r.width, h: r.height }
    // Lire la géométrie de base une fois : aucune lecture de layout dans les keyframes.
    const base = el.offsetWidth > 0 ? { x: el.offsetLeft, y: el.offsetTop, w: el.offsetWidth, h: el.offsetHeight } : origine
    const pose = (b: Boite) =>
      `translate3d(${b.x - base.x}px, ${b.y - base.y}px, 0) scale(${b.w / Math.max(1, base.w)}, ${b.h / Math.max(1, base.h)})`
    if (animationsCoupees() || !el.animate) return Promise.resolve()
    const a = el.animate([{ transform: pose(de) }, { transform: pose(vers) }], {
      duration: duree, delay: delai, fill: 'both', easing: 'cubic-bezier(0.25, 0.7, 0.3, 1)',
    })
    vols.current.push(a)
    if (destination) {
      let image = 0
      let arrete = false
      let derniere = vers
      const echeance = performance.now() + duree + delai
      const suivre = () => {
        image = 0
        if (arrete) return
        const cible = destination()
        if (!cible || Math.max(Math.abs(cible.x - derniere.x), Math.abs(cible.y - derniere.y), Math.abs(cible.w - derniere.w), Math.abs(cible.h - derniere.h)) < 0.5) return
        derniere = cible
        const r = el.getBoundingClientRect()
        const c = cadreDuPlateau()
        const courant = { x: r.left - (c?.origine.left ?? 0), y: r.top - (c?.origine.top ?? 0), w: r.width, h: r.height }
        // Repartir de la pose réellement affichée, sans déplacer le début de
        // la courbe déjà parcourue. Une destination mobile ne crée pas de saut.
        const effet = a.effect as KeyframeEffect | null
        effet?.setKeyframes([{ transform: pose(courant) }, { transform: pose(cible) }])
        effet?.updateTiming?.({ duration: Math.max(16, echeance - performance.now()), delay: 0 })
        a.currentTime = 0
      }
      const demander = () => { if (!arrete && !image) image = window.requestAnimationFrame(suivre) }
      // Les animations natives n'ont pas besoin d'un recalcul JS à 60 Hz.
      // Relever la destination seulement quand la disposition peut changer.
      const observateur = typeof MutationObserver === 'undefined' ? undefined : new MutationObserver((mutations) => {
        if (mutations.some((m) => !(m.target instanceof Element) || !m.target.closest('.rencontre-sur-table, [class*="tsm-"], .trait-phase, .jeton-coup, .trajet-copie'))) demander()
      })
      if (c) observateur?.observe(c.element, { childList: true, subtree: true, attributes: true, attributeFilter: ['class', 'style'] })
      const tailles = typeof ResizeObserver === 'undefined' ? undefined : new ResizeObserver(demander)
      if (c) tailles?.observe(c.element)
      window.addEventListener('resize', demander)
      const arreter = () => {
        arrete = true
        window.cancelAnimationFrame(image)
        observateur?.disconnect()
        tailles?.disconnect()
        window.removeEventListener('resize', demander)
      }
      suivis.current.push(arreter)
      demander()
      void a.finished.then(arreter, arreter)
    }
    return a.finished
  }

  useLayoutEffect(() => {
    if (!ancres || etat.current !== 'entree') return
    const numero = ++generation.current
    const els = elements()
    const lancer = () => {
      if (generation.current !== numero) return
      for (const el of els) el.style.visibility = 'visible'
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
      }).catch(() => { /* Une autre phase ou partie annule cette entrée. */ })
    }
    // Décoder les grands scans avant le mouvement évite une rasterisation
    // lourde au milieu du vol. Un scan défaillant ne bloque jamais la phase.
    const images = els.flatMap((el) => Array.from(el.querySelectorAll<HTMLImageElement>('.scan-frame img')))
      .filter((img) => !img.complete && typeof img.decode === 'function')
    if (!images.length) lancer()
    else {
      let minuteur = 0
      void Promise.race([
        Promise.all(images.map((img) => { img.loading = 'eager'; return img.decode().catch(() => {}) })),
        new Promise<void>((resolve) => { minuteur = window.setTimeout(resolve, 800) }),
      ]).then(() => { window.clearTimeout(minuteur); lancer() })
    }
    // Seule l'arrivée des ancres déclenche l'entrée, jamais un enrichissement de l'étape.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [Boolean(ancres)])

  commande.current = {
    valider: (suite) => {
      if (!ancres || !cartes.length || etat.current === 'termine') return false
      if (etat.current === 'entree') {
        // Un clic trop tôt ne doit jamais supprimer la lecture au centre.
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
          visibility: phase === 'entree' || phase === 'termine' ? 'hidden' : undefined,
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
