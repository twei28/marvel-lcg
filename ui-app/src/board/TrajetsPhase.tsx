// Les trajets des cartes pendant la phase du méchant (refonte, lot 4, essai,
// 12/10/2026, décisions 3, 49 à 53).
//
// La table est calée sur l'écran affiché (`table-calee.ts`) : une carte n'y
// apparaît qu'à l'écran qui raconte son entrée, et n'en disparaît qu'à celui
// qui raconte sa sortie. Ce composant regarde la table changer et met ces
// changements en mouvement :
//  - une carte qui ARRIVE : sa place s'ouvre en pointillés, la carte vole
//    depuis la boîte de phase en 0,6 s, puis s'y pose ;
//  - une carte qui PART : une copie part de sa dernière place vers sa pile
//    (défausse du joueur ou défausse rencontre), sa place se referme.
// Continuer reste cliquable : un nouvel écran termine d'un coup les trajets en
// cours. Sobre, sans animations ou mouvement réduit : rien ne vole.
import { useEffect, useRef } from 'react'
import { changementDeTable, DUREE_TRAJET_MS, pileDeDepart, type Releve } from './trajets-phase'
import './trajets-phase.css'

type Mesure = Releve & { rect: DOMRect; src?: string; dos?: boolean }

/** Le temps de repos de la table avant de comparer (ms). */
const CALME_MS = 150

const VRAIE_PILE = /(deck|defausse|discard|victoire|retirees|mise-de-cote|nemesis|set-aside)/

export function animationsCoupees(): boolean {
  if (typeof window === 'undefined') return true
  if (document.body.classList.contains('plateau-sans-animations')) return true
  if (document.documentElement.getAttribute('data-affichage') === 'sobre') return true
  return window.matchMedia?.('(prefers-reduced-motion: reduce)').matches ?? false
}

function cartesDeLaTable(): Map<number, { el: HTMLElement; mesure: Mesure }> {
  const resultat = new Map<number, { el: HTMLElement; mesure: Mesure }>()
  const cartes = document.querySelectorAll<HTMLElement>('.plateau-cadre .scan-card[data-card-id]')
  for (const el of cartes) {
    if (el.closest('.deroule-phase, .zone-main, [data-zone="main"], .carte-apercu')) continue
    // Les vraies piles (decks, defausses...) ne comptent pas : une rangee FONDUE
    // (les sbires engages, « terrain-combat-engages ») porte aussi `data-pile`.
    if (VRAIE_PILE.test(el.closest('[data-pile]')?.getAttribute('data-pile') ?? '')) continue
    if (el.classList.contains('kind-status')) continue
    // 13/10/2026 (encadré ⑪) : une carte face cachée compte aussi, pour que les
    // dos distribués arrivent du paquet rencontre. Elle ne « part » jamais : sa
    // disparition, c'est sa révélation, pas un trajet vers la défausse.
    const dos = el.classList.contains('is-facedown')
    const id = Number(el.dataset.cardId)
    if (!Number.isFinite(id) || resultat.has(id)) continue
    const rect = el.getBoundingClientRect()
    if (rect.width === 0 || rect.height === 0) continue
    const camp = el.classList.contains('camp-encounter') ? 'encounter' : el.classList.contains('camp-player') ? 'player' : undefined
    resultat.set(id, { el, mesure: { id, camp, rect, dos, src: dos ? undefined : el.querySelector('img')?.getAttribute('src') ?? undefined } })
  }
  return resultat
}

export function copieVolante(src: string | undefined, depart: DOMRect): HTMLElement {
  const copie = document.createElement('div')
  copie.className = 'trajet-copie'
  Object.assign(copie.style, {
    left: `${depart.left}px`,
    top: `${depart.top}px`,
    width: `${depart.width}px`,
    height: `${depart.height}px`,
  })
  if (src) {
    const img = document.createElement('img')
    img.src = src
    img.alt = ''
    copie.append(img)
  }
  document.body.append(copie)
  return copie
}

export function voler(copie: HTMLElement, depart: DOMRect, arrivee: DOMRect, fondu: boolean): Animation {
  const dx = arrivee.left - depart.left
  const dy = arrivee.top - depart.top
  const sx = arrivee.width / Math.max(1, depart.width)
  const sy = arrivee.height / Math.max(1, depart.height)
  return copie.animate(
    [
      { transform: 'translate(0, 0) scale(1, 1)', opacity: 1 },
      { transform: `translate(${dx}px, ${dy}px) scale(${sx}, ${sy})`, opacity: fondu ? 0.15 : 1 },
    ],
    { duration: DUREE_TRAJET_MS, easing: 'cubic-bezier(0.3, 0.7, 0.2, 1)', fill: 'forwards' }
  )
}

export function TrajetsPhase({ actif }: { actif: boolean }) {
  const releve = useRef<Map<number, Mesure> | undefined>(undefined)
  const enCours = useRef<Array<{ animation: Animation; fin: () => void }>>([])

  useEffect(() => {
    if (!actif || typeof MutationObserver === 'undefined') {
      releve.current = undefined
      return
    }
    const table = document.querySelector('.plateau-cadre')
    if (!table) return

    const terminerTout = () => {
      for (const { animation, fin } of enCours.current.splice(0)) {
        try {
          animation.finish()
        } catch {
          /* deja terminee */
        }
        fin()
      }
    }

    const comparer = () => {
      const maintenant = cartesDeLaTable()
      const apres = new Map([...maintenant].map(([id, { mesure }]) => [id, mesure]))
      const avant = releve.current
      releve.current = apres
      if (!avant || animationsCoupees()) return
      const { arrivees, departs } = changementDeTable(avant, apres)
      if (arrivees.length === 0 && departs.length === 0) return
      // Un nouvel écran : Continuer termine d'un coup les trajets en cours (décision 53).
      terminerTout()
      const boite = document.querySelector<HTMLElement>('.deroule-phase.est-essai')
      for (const id of arrivees) {
        const cible = maintenant.get(id)
        if (!cible) continue
        // Mise en jeu par un boost ★ : elle attend le clic (EtoilesEnAttente.tsx).
        if (cible.el.hasAttribute('data-etoile-attente')) continue
        // Un dos distribué part du paquet rencontre ; une carte révélée, de la boîte.
        const paquet = cible.mesure.dos ? document.querySelector<HTMLElement>('.plateau-cadre [data-pile$="encounter-deck"]') : null
        const source =
          paquet ??
          boite?.querySelector<HTMLElement>(`.scan-card[data-card-id="${id}"]`) ??
          boite?.querySelector<HTMLElement>('.deroule-corps') ??
          boite
        if (!source) continue
        const depart = source.getBoundingClientRect()
        cible.el.classList.add('trajet-arrivee')
        const copie = copieVolante(cible.mesure.src, depart)
        if (cible.mesure.dos) copie.classList.add('est-dos')
        const animation = voler(copie, depart, cible.mesure.rect, false)
        const fin = () => {
          copie.remove()
          cible.el.classList.remove('trajet-arrivee')
        }
        animation.onfinish = () => {
          enCours.current = enCours.current.filter((e) => e.animation !== animation)
          fin()
        }
        enCours.current.push({ animation, fin })
      }
      for (const parti of departs) {
        if (parti.dos) continue
        const pile = document.querySelector<HTMLElement>(`.plateau-cadre ${pileDeDepart(parti.camp)}`)
        const arrivee = pile?.getBoundingClientRect()
        const copie = copieVolante(parti.src, parti.rect)
        copie.classList.add('est-depart')
        const animation = arrivee && arrivee.width > 0
          ? voler(copie, parti.rect, arrivee, true)
          : copie.animate([{ opacity: 1 }, { opacity: 0 }], { duration: DUREE_TRAJET_MS, fill: 'forwards' })
        const fin = () => copie.remove()
        animation.onfinish = () => {
          enCours.current = enCours.current.filter((e) => e.animation !== animation)
          fin()
        }
        enCours.current.push({ animation, fin })
      }
    }

    // On ne compare qu'une table AU REPOS (aucun changement depuis CALME_MS) :
    // une carte qui disparait puis revient le temps d'une question du moteur
    // (la table repasse alors sur le monde reel) ne vole pas pour rien.
    let attente = 0
    const observateur = new MutationObserver(() => {
      if (attente) window.clearTimeout(attente)
      attente = window.setTimeout(() => {
        attente = 0
        comparer()
      }, CALME_MS)
    })
    comparer()
    observateur.observe(table, { childList: true, subtree: true })
    return () => {
      observateur.disconnect()
      if (attente) window.clearTimeout(attente)
      terminerTout()
      releve.current = undefined
    }
  }, [actif])

  return null
}
