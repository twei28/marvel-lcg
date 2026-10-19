// Les jetons des coups de la phase du mechant (essai, 13/10/2026).
//
// Demande de l'utilisateur : la table montre les compteurs d'AVANT l'ecran
// (`coups-sur-table.ts`). Pour chaque coup, UN jeton, le vrai jeton du jeu
// (triangle de menace, jeton de degats), en grand, portant son nombre, attend
// au debut du trait des que l'ecran parait. Au clic sur Continuer, il suit la
// courbe du trait jusqu'a la carte, et le compteur change a son arrivee.
//
// ⚠ LE VRAI JETON, PAS UN ROND : premiere version, des disques jaunes, un par
// point. Retour : « que ce soit le bon token triangulaire et qu'on voie dans le
// token le nombre ». Meme lecon que le 14/09/2026 (`JetonMenaceVolant.tsx`).
//
// Un nouvel ecran termine les vols d'un coup, comme pour les cartes (decision
// 53). Sobre, sans animations ou mouvement reduit : pas de jeton, les compteurs
// sont tout de suite a jour.
import { useEffect, useLayoutEffect, useMemo, useRef, useState } from 'react'
import jetonAccelerationImage from '../components/jetons/acceleration.png'
import jetonDegatsImage from '../components/jetons/degats.png'
import jetonMenaceImage from '../components/jetons/menace.png'
import { coupsDeLEtape, JETON_DEGATS_VOLANT, pointDeLaCourbe, type Coup, type Fige, type GenreCoup } from './coups-sur-table'
import type { EtapeDeroule } from './deroule-phase'
import { carteDeLaTable, elementDuBout, rect } from './FlechesPhase'
import { traceEntre, type TraceFleche } from './fleches-phase'
import { jouerSon } from './sons'
import { animationsCoupees } from './TrajetsPhase'
import { DUREE_TRAJET_MS } from './trajets-phase'
import './jetons-coups.css'

/** Le trait du coup : de sa source (boite, carte de la boite, carte de la table) a la carte touchee. */
function traceDu(c: Coup): TraceFleche | undefined {
  const rCible = rect(carteDeLaTable(c.cibleId))
  const rSource = rect(elementDuBout(c.depuis))
  if (!rCible || !rSource) return undefined
  const trace = traceEntre(rSource, rCible)
  if (c.genre !== 'menace') return trace
  // 16/10/2026 : le jeton de menace se POSE sur le jeton de la manigance (le triangle), pas au
  // bord de la carte. S'il n'existe pas encore (compteur à 0), on vise sa place habituelle.
  const triangle = rect(carteDeLaTable(c.cibleId)?.querySelector('.jeton-menace'))
  const arrivee = triangle
    ? { x: triangle.x + triangle.w / 2, y: triangle.y + triangle.h / 2 }
    : { x: rCible.x + rCible.w * 0.82, y: rCible.y + rCible.h * 0.24 }
  return { ...trace, arrivee }
}

/**
 * Le jeton de MENACE est grand au repos (16/10/2026, « trois fois plus grand ») et rétrécit en
 * volant. Les dégâts et l'accélération gardent leur taille normale : « tu peux le laisser aux
 * dégâts normaux ».
 */
function echelles(genre: GenreCoup): { repos: number; arrivee: number } {
  return genre === 'menace' ? { repos: 3, arrivee: 0.45 } : { repos: 1, arrivee: 1 }
}

function placer(el: HTMLElement, x: number, y: number, genre: GenreCoup) {
  el.style.transform = `translate(${x}px, ${y}px) translate(-50%, -50%) scale(${echelles(genre).repos})`
}

function creerJeton(c: Coup): HTMLElement {
  const el = document.createElement('div')
  el.className = `jeton-coup est-${c.genre}`
  const image = c.genre === 'menace' ? jetonMenaceImage : c.genre === 'acceleration' ? jetonAccelerationImage : jetonDegatsImage
  // Les dégâts : un badge plat, dessiné en CSS (`.jeton-coup.est-degats`), pas l'ancienne boule brillante.
  if (c.genre !== 'degats') el.style.backgroundImage = `url(${image})`
  el.style.visibility = 'hidden'
  el.textContent = c.genre === 'degats' ? `-${c.montant}` : c.genre === 'acceleration' ? '' : `${c.montant}`
  el.setAttribute('aria-hidden', 'true')
  document.body.append(el)
  return el
}

type EnAttente = { el: HTMLElement; coup: Coup }

const AUCUN: Fige[] = []

/**
 * Les compteurs que la table doit figer : ceux de l'ecran affiche (valeur
 * d'avant), puis, pendant les vols qui suivent le clic, ceux des coups encore
 * en l'air.
 */
export function useCoupsEnVol(
  etapes: readonly EtapeDeroule[],
  cle: string | undefined,
  actif: boolean,
  /** Faux tant que l'attaque retourne encore ses boosts : le total n'est pas encore dit. */
  pret = true
): Fige[] {
  const [enVol, setEnVol] = useState<Fige[]>(AUCUN)
  const enAttente = useRef<EnAttente[]>([])
  const volants = useRef<Array<{ el: HTMLElement; coup: Coup }>>([])
  const derniereCle = useRef<string | undefined>(undefined)
  const [salve, setSalve] = useState(0)

  // Avant la peinture : le nouvel ecran ne doit jamais montrer le chiffre final une image.
  useLayoutEffect(() => {
    if (derniereCle.current === cle) return
    derniereCle.current = cle
    for (const v of volants.current.splice(0)) v.el.remove()
    const repris = enAttente.current.splice(0).filter((a) => a.el.style.visibility !== 'hidden')
    if (!actif || cle === undefined || repris.length === 0) {
      for (const a of repris) a.el.remove()
      setEnVol(AUCUN)
      return
    }
    volants.current = repris
    setEnVol(repris.map(({ coup }) => ({ genre: coup.genre, cibleId: coup.cibleId, valeur: coup.avant })))
    setSalve((n) => n + 1)
  }, [cle, actif])

  // Les jetons qui attendent, tant que l'ecran est affiche.
  // Les degats ne volent plus (`JETON_DEGATS_VOLANT`) : leur compteur n'est pas fige, il change avec l'ecran.
  // Seul reste fige le coup a 0 (la Riposte, sur l'ecran de l'attaque qu'elle suit).
  const coups = actif ? coupsDeLEtape(etapes.find((e) => e.cle === cle)).filter((c) => JETON_DEGATS_VOLANT || c.genre !== 'degats' || c.montant === 0) : []
  const signature = coups.map((c) => `${c.genre}:${c.cibleId}:${c.avant}:${c.montant}:${JSON.stringify(c.depuis)}`).join('|')
  useEffect(() => {
    if (!pret || cle === undefined || coups.length === 0) return
    if (typeof document === 'undefined' || animationsCoupees()) return
    const mes = coups.filter((c) => c.montant > 0).map((coup) => ({ el: creerJeton(coup), coup }))
    enAttente.current = mes
    // La boite et la table bougent encore au premier rendu : on repose les jetons au repos.
    const poser = () => {
      for (const { el, coup } of mes) {
        if (!enAttente.current.some((a) => a.el === el)) continue
        const trace = traceDu(coup)
        if (!trace) continue
        placer(el, trace.depart.x, trace.depart.y, coup.genre)
        el.style.visibility = ''
      }
    }
    poser()
    const minuteurs = [260, 720].map((ms) => window.setTimeout(poser, ms))
    // « Sur la table », l'intro de la phase peut retarder l'écran : son point de départ
    // n'existe pas encore. On réessaie tant qu'un jeton n'est pas posé (5 s au plus).
    const veille = window.setInterval(() => {
      poser()
      if (mes.every(({ el }) => el.style.visibility !== 'hidden')) window.clearInterval(veille)
    }, 250)
    const finVeille = window.setTimeout(() => window.clearInterval(veille), 5000)
    window.addEventListener('resize', poser)
    return () => {
      for (const m of minuteurs) window.clearTimeout(m)
      window.clearInterval(veille)
      window.clearTimeout(finVeille)
      window.removeEventListener('resize', poser)
      // Repris pour voler (clic sur Continuer) : ce n'est plus a nous de les enlever.
      for (const { el } of mes) {
        if (enAttente.current.some((a) => a.el === el)) el.remove()
      }
      enAttente.current = enAttente.current.filter((a) => !mes.some((m) => m.el === a.el))
    }
    // `coups` est recalcule a chaque rendu : sa signature suffit.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [cle, signature, pret])

  // Les vols, du debut de chaque trait a sa carte.
  useEffect(() => {
    const partis = volants.current
    if (partis.length === 0) return
    const animations: Animation[] = []
    for (const v of partis) {
      const arrivee = () => {
        v.el.remove()
        // 13/10/2026 (encadré ①) : un petit « tac » quand le jeton se pose, le son
        // « token » du moteur (famille jeton), coupé avec les sons du jeu.
        jouerSon('token')
        setEnVol((liste) => {
          const reste = liste.filter((f) => !(f.genre === v.coup.genre && f.cibleId === v.coup.cibleId))
          return reste.length === 0 ? AUCUN : reste
        })
      }
      const trace = traceDu(v.coup)
      if (!trace) {
        arrivee()
        continue
      }
      const cles = Array.from({ length: 13 }, (_, k) => {
        const p = pointDeLaCourbe(trace.depart, trace.controle, trace.arrivee, k / 12)
        const { repos, arrivee: fin } = echelles(v.coup.genre)
        const echelle = repos + (fin - repos) * (k / 12)
        return { transform: `translate(${p.x}px, ${p.y}px) translate(-50%, -50%) scale(${echelle})`, offset: k / 12 }
      })
      const animation = v.el.animate(cles, { duration: DUREE_TRAJET_MS, easing: 'cubic-bezier(0.3, 0.7, 0.2, 1)', fill: 'forwards' })
      animation.onfinish = arrivee
      animations.push(animation)
    }
    return () => {
      for (const a of animations) a.onfinish = null
      for (const v of partis) v.el.remove()
    }
  }, [salve])

  // Ecran affiche : ses coups figes a leur valeur d'avant. Pendant les vols : ceux
  // encore en l'air. Toujours le MEME tableau tant que rien ne change : le plateau
  // entier se reconstruit sur lui.
  const figesEcran = useMemo(
    () => (coups.length === 0 ? AUCUN : coups.map((c) => ({ genre: c.genre, cibleId: c.cibleId, valeur: c.avant }))),
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [signature]
  )
  // Les deux a la fois : l'ecran qui suit le clic fige deja ses propres cartes.
  // Les vols viennent en dernier : sur une meme carte, le jeton en l'air gagne.
  return useMemo(
    () => (enVol.length === 0 ? figesEcran : figesEcran.length === 0 ? enVol : [...figesEcran, ...enVol]),
    [enVol, figesEcran]
  )
}
