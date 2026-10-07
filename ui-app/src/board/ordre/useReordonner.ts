// Alt + glisser une carte vers sa nouvelle place dans la meme rangee (ou la
// meme pile d'ameliorations). Geste a part du glisser-deposer : il ne parle
// jamais au moteur et ne touche que l'affichage (voir ordre-cartes.ts).
import { useCallback, useEffect, useRef, useState } from 'react'
import type { PointerEvent as ReactPointerEvent } from 'react'
import { SEUIL_GLISSER } from '../glisser/useGlisser'
import { cleDePile, deplacer, placeVisee, type Ordres, type Voisine } from './ordre-cartes'

export type GesteOrdre = {
  sourceId: number
  x: number
  y: number
  /** Repere d'insertion, en coordonnees ecran. */
  repere?: { gauche: number; haut: number; hauteur: number; pile: boolean; cibleId: number }
}

type Depart = {
  sourceId: number
  cle: string
  pile: boolean
  racine: HTMLElement
  x: number
  y: number
  pointerId: number
  element: HTMLElement
}

const idDe = (element: Element | null | undefined): number | undefined => {
  const id = Number((element as HTMLElement | null | undefined)?.dataset?.cardId)
  return Number.isFinite(id) ? id : undefined
}

/** Les cartes de la rangee (ou de la pile) du depart, dans l'ordre du DOM. */
function voisinesDe(depart: Depart): { id: number; element: HTMLElement }[] {
  const resultat: { id: number; element: HTMLElement }[] = []
  if (depart.pile) {
    for (const carte of depart.racine.querySelectorAll<HTMLElement>(':scope > .est-attachee > .scan-card')) {
      const id = idDe(carte)
      if (id !== undefined) resultat.push({ id, element: carte })
    }
  } else {
    for (const unite of depart.racine.querySelectorAll<HTMLElement>(':scope > .plateau-unite:not(.pile-vide)')) {
      if (unite.dataset.pile) continue
      const carte = unite.querySelector<HTMLElement>(':scope > .scan-card')
      const id = idDe(carte)
      if (carte && id !== undefined) resultat.push({ id, element: carte })
    }
  }
  return resultat
}

// Les ids de cartes n'ont de sens que dans UNE partie : l'ordre est etiquete
// par la partie, garde au rechargement, jete des qu'une autre partie arrive.
const CLE_ORDRES = 'marvel-ordre-cartes'

function lireOrdres(partieId?: string): Ordres {
  if (partieId === undefined) return {}
  try {
    const brut = window.sessionStorage.getItem(CLE_ORDRES)
    const objet = brut ? (JSON.parse(brut) as { partieId?: string; ordres?: Ordres }) : undefined
    return objet?.partieId === partieId && objet.ordres && typeof objet.ordres === 'object' ? objet.ordres : {}
  } catch {
    return {}
  }
}

export function useReordonner(partieId?: string) {
  const [ordres, setOrdres] = useState<Ordres>(() => lireOrdres(partieId))
  const partieVue = useRef(partieId)
  useEffect(() => {
    if (partieVue.current === partieId) return
    partieVue.current = partieId
    setOrdres(lireOrdres(partieId))
  }, [partieId])
  useEffect(() => {
    if (partieId === undefined || partieVue.current !== partieId) return
    try {
      window.sessionStorage.setItem(CLE_ORDRES, JSON.stringify({ partieId, ordres }))
    } catch {
      /* stockage indisponible : l'ordre vit en memoire */
    }
  }, [ordres, partieId])
  const [geste, setGeste] = useState<GesteOrdre | null>(null)
  const depart = useRef<Depart | null>(null)
  const commence = useRef(false)

  const oublier = useCallback(() => {
    const debut = depart.current
    if (debut) {
      try {
        debut.element.releasePointerCapture(debut.pointerId)
      } catch {
        /* rien a rendre */
      }
    }
    depart.current = null
    commence.current = false
    setGeste(null)
  }, [])

  /** `true` si l'appui est pris par ce geste (Alt + souris sur une carte rangeable). */
  const surAppui = useCallback((evenement: ReactPointerEvent<HTMLElement>): boolean => {
    if (!evenement.altKey || evenement.pointerType === 'touch' || evenement.pointerType === 'pen' || evenement.button !== 0) return false
    const sous = evenement.target
    if (!(sous instanceof HTMLElement)) return false
    const carte = sous.closest<HTMLElement>('.scan-card')
    const sourceId = idDe(carte)
    if (!carte || sourceId === undefined) return false
    const attachee = carte.closest<HTMLElement>('.est-attachee')
    let racine: HTMLElement | null
    let cle: string
    if (attachee) {
      racine = attachee.closest<HTMLElement>('.plateau-unite')
      const porteurId = idDe(racine?.querySelector(':scope > .scan-card'))
      if (!racine || porteurId === undefined) return false
      cle = cleDePile(porteurId)
    } else {
      racine = carte.closest<HTMLElement>('.plateau-groupe')
      const unite = carte.parentElement
      if (!racine || !unite?.classList.contains('plateau-unite') || unite.dataset.pile) return false
      cle = racine.dataset.rangee ?? ''
      if (!cle) return false
    }
    depart.current = {
      sourceId,
      cle,
      pile: attachee !== null,
      racine,
      x: evenement.clientX,
      y: evenement.clientY,
      pointerId: evenement.pointerId,
      element: evenement.currentTarget,
    }
    commence.current = false
    return true
  }, [])

  const surDeplacement = useCallback((evenement: ReactPointerEvent<HTMLElement>): boolean => {
    const debut = depart.current
    if (!debut) return false
    if (!commence.current) {
      if (Math.hypot(evenement.clientX - debut.x, evenement.clientY - debut.y) < SEUIL_GLISSER) return true
      commence.current = true
      try {
        window.getSelection()?.removeAllRanges()
        debut.element.setPointerCapture(debut.pointerId)
      } catch {
        /* pas de capture : on suit le pointeur sans */
      }
    }
    const voisines = voisinesDe(debut)
    const mesurees: (Voisine & { rect: DOMRect })[] = voisines.map(({ id, element }) => {
      const rect = element.getBoundingClientRect()
      return { id, cx: rect.left + rect.width / 2, cy: rect.top + rect.height / 2, rect }
    })
    const visee = placeVisee(
      mesurees.filter((v) => v.id !== debut.sourceId),
      evenement.clientX,
      evenement.clientY
    )
    const cible = visee && mesurees.find((v) => v.id === visee.cibleId)
    setGeste({
      sourceId: debut.sourceId,
      x: evenement.clientX,
      y: evenement.clientY,
      repere:
        visee && cible
          ? {
              gauche: visee.apres ? cible.rect.right : cible.rect.left,
              haut: cible.rect.top,
              hauteur: cible.rect.height,
              pile: debut.pile,
              cibleId: visee.cibleId,
            }
          : undefined,
    })
    return true
  }, [])

  /** `true` si ce geste vient de s'achever : l'appelant n'enchaine pas le clic. */
  const surRelache = useCallback(
    (evenement: ReactPointerEvent<HTMLElement>): boolean => {
      const debut = depart.current
      if (!debut) return false
      const aBouge = commence.current
      if (aBouge) {
        const voisines = voisinesDe(debut)
        const mesurees: Voisine[] = voisines
          .filter((v) => v.id !== debut.sourceId)
          .map(({ id, element }) => {
            const rect = element.getBoundingClientRect()
            return { id, cx: rect.left + rect.width / 2, cy: rect.top + rect.height / 2 }
          })
        const visee = placeVisee(mesurees, evenement.clientX, evenement.clientY)
        if (visee) {
          const ids = voisines.map((v) => v.id)
          setOrdres((courant) => {
            // L'ordre affiche fait foi : on repart de lui, pas d'un ancien choix.
            const suivant = deplacer(ids, debut.sourceId, visee.cibleId, visee.apres)
            return suivant === ids ? courant : { ...courant, [debut.cle]: suivant }
          })
        }
      }
      oublier()
      return aBouge
    },
    [oublier]
  )

  return { ordres, geste, gestes: { surAppui, surDeplacement, surRelache, annuler: oublier } }
}
