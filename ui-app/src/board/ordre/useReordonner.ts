// Alt + glisser une carte vers sa nouvelle place dans la meme rangee (ou la
// meme pile d'ameliorations). Geste a part du glisser-deposer : il ne parle
// jamais au moteur et ne touche que l'affichage (voir ordre-cartes.ts).
import { useCallback, useEffect, useRef, useState } from 'react'
import type { PointerEvent as ReactPointerEvent } from 'react'
import { SEUIL_GLISSER } from '../glisser/useGlisser'
import { cleDePile, deplacer, placeVisee, poserDuCote, type Cote, type Ordres, type Voisine } from './ordre-cartes'

export type GesteOrdre = {
  sourceId: number
  x: number
  y: number
  /** Repere d'insertion, en coordonnees ecran. */
  repere?: { gauche: number; haut: number; hauteur: number; pile: boolean; cibleId: number }
  /** Pile d'ameliorations : le porteur, encadre, pour dire a qui elle reste attachee. */
  cadre?: { gauche: number; haut: number; largeur: number; hauteur: number }
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
  /** Pile d'ameliorations : la carte qui les porte. */
  porteurId?: number
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

/**
 * Pile d'ameliorations : le cote vise (par rapport au centre du porteur), la
 * voisine de ce cote la plus proche et si l'on pose « apres » elle (plus loin du
 * porteur), le trait et le cadre a montrer. Le cote se choisit librement : la
 * place d'une amelioration se decide a gauche OU a droite du personnage.
 */
function viseeDansPile(depart: Depart, x: number, y: number) {
  const porteur = depart.racine.querySelector<HTMLElement>(':scope > .scan-card')?.getBoundingClientRect()
  if (!porteur) return undefined
  const cote: Cote = x < porteur.left + porteur.width / 2 ? 'gauche' : 'droite'
  const ici = voisinesDe(depart)
    .filter((v) => v.id !== depart.sourceId)
    .filter((v) => (v.element.parentElement?.classList.contains('est-a-gauche') ? 'gauche' : 'droite') === cote)
    .map(({ id, element }) => ({ id, rect: element.getBoundingClientRect() }))
  let proche: (typeof ici)[number] | undefined
  let distance = Infinity
  for (const v of ici) {
    const d = Math.hypot(v.rect.left + v.rect.width / 2 - x, v.rect.top + v.rect.height / 2 - y)
    if (d < distance) {
      distance = d
      proche = v
    }
  }
  const apres = proche
    ? cote === 'droite'
      ? x > proche.rect.left + proche.rect.width / 2
      : x < proche.rect.left + proche.rect.width / 2
    : false
  const bord = proche
    ? cote === 'droite' === apres
      ? proche.rect.right
      : proche.rect.left
    : cote === 'droite'
      ? porteur.right
      : porteur.left
  return {
    cote,
    cible: proche ? { id: proche.id, apres } : undefined,
    repere: { gauche: bord, haut: porteur.top, hauteur: porteur.height },
    cadre: { gauche: porteur.left, haut: porteur.top, largeur: porteur.width, hauteur: porteur.height },
  }
}

/** Le depart d'un geste de rangement depuis cette carte, ou rien si elle ne se range pas. */
function departDe(carte: HTMLElement, x: number, y: number, pointerId: number, element: HTMLElement): Depart | undefined {
  const sourceId = idDe(carte)
  if (sourceId === undefined) return undefined
  const attachee = carte.closest<HTMLElement>('.est-attachee')
  if (attachee) {
    const racine = attachee.closest<HTMLElement>('.plateau-unite')
    const porteurId = idDe(racine?.querySelector(':scope > .scan-card'))
    if (!racine || porteurId === undefined) return undefined
    return { sourceId, cle: cleDePile(porteurId), pile: true, racine, x, y, pointerId, element, porteurId }
  }
  const racine = carte.closest<HTMLElement>('.plateau-groupe')
  const unite = carte.parentElement
  if (!racine || !unite?.classList.contains('plateau-unite') || unite.dataset.pile) return undefined
  const cle = racine.dataset.rangee ?? ''
  if (!cle) return undefined
  return { sourceId, cle, pile: false, racine, x, y, pointerId, element }
}

/**
 * Le lacher retombe-t-il dans la rangee de la carte (ou, pour une
 * amelioration, tout pres de son personnage) ? Mode manuel : c'est alors un
 * rangement, pas un deplacement (decision du 07/10/2026).
 */
function dansSaRangee(depart: Depart, x: number, y: number): boolean {
  const boite = depart.racine.getBoundingClientRect()
  const marge = depart.pile ? boite.height / 2 : 0
  return x >= boite.left - marge && x <= boite.right + marge && y >= boite.top && y <= boite.bottom
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
    const trouve = carte ? departDe(carte, evenement.clientX, evenement.clientY, evenement.pointerId, evenement.currentTarget) : undefined
    if (!trouve) return false
    depart.current = trouve
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
    if (debut.pile) {
      const visee = viseeDansPile(debut, evenement.clientX, evenement.clientY)
      setGeste({
        sourceId: debut.sourceId,
        x: evenement.clientX,
        y: evenement.clientY,
        repere: visee ? { ...visee.repere, pile: true, cibleId: visee.cible?.id ?? debut.sourceId } : undefined,
        cadre: visee?.cadre,
      })
      return true
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
      if (aBouge && debut.pile && debut.porteurId !== undefined) {
        const visee = viseeDansPile(debut, evenement.clientX, evenement.clientY)
        const porteurId = debut.porteurId
        if (visee) {
          const ids = voisinesDe(debut).map((v) => v.id)
          setOrdres((courant) => {
            const ordre = visee.cible ? deplacer(ids, debut.sourceId, visee.cible.id, visee.cible.apres) : ids
            return poserDuCote({ ...courant, [debut.cle]: ordre }, porteurId, debut.sourceId, visee.cote)
          })
        }
      } else if (aBouge) {
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

  /**
   * MODE MANUEL, GLISSER SIMPLE (decision du 07/10/2026) : une carte lachee dans
   * sa propre rangee s'y range, une amelioration lachee pres de son personnage
   * change de rang ou de cote. Rend `true` quand c'en etait un (l'appelant ne
   * deplace alors rien) ; `appliquer` faux ne fait que montrer le repere.
   */
  const rangerAuGlisser = useCallback((sourceId: number, x: number, y: number, appliquer: boolean): boolean => {
    if (appliquer) setGeste(null)
    const carte = [...document.querySelectorAll<HTMLElement>(`.plateau-scene .scan-card[data-card-id="${sourceId}"]`)].find(
      (c) => !c.closest('.zone-main')
    )
    const debut = carte ? departDe(carte, x, y, 0, carte) : undefined
    if (!debut || !dansSaRangee(debut, x, y)) {
      if (!appliquer) setGeste(null)
      return false
    }
    if (debut.pile && debut.porteurId !== undefined) {
      const visee = viseeDansPile(debut, x, y)
      if (!visee) return false
      if (!appliquer) {
        setGeste({ sourceId, x, y, repere: { ...visee.repere, pile: true, cibleId: visee.cible?.id ?? sourceId }, cadre: visee.cadre })
        return true
      }
      const porteurId = debut.porteurId
      const ids = voisinesDe(debut).map((v) => v.id)
      setOrdres((courant) => {
        const ordre = visee.cible ? deplacer(ids, sourceId, visee.cible.id, visee.cible.apres) : ids
        return poserDuCote({ ...courant, [debut.cle]: ordre }, porteurId, sourceId, visee.cote)
      })
    } else {
      const voisines = voisinesDe(debut)
      const mesurees = voisines.map(({ id, element }) => {
        const rect = element.getBoundingClientRect()
        return { id, cx: rect.left + rect.width / 2, cy: rect.top + rect.height / 2, rect }
      })
      const visee = placeVisee(mesurees.filter((v) => v.id !== sourceId), x, y)
      if (!visee) return false
      const cible = mesurees.find((v) => v.id === visee.cibleId)!
      if (!appliquer) {
        setGeste({
          sourceId,
          x,
          y,
          repere: { gauche: visee.apres ? cible.rect.right : cible.rect.left, haut: cible.rect.top, hauteur: cible.rect.height, pile: false, cibleId: visee.cibleId },
        })
        return true
      }
      const ids = voisines.map((v) => v.id)
      setOrdres((courant) => {
        const suivant = deplacer(ids, sourceId, visee.cibleId, visee.apres)
        return suivant === ids ? courant : { ...courant, [debut.cle]: suivant }
      })
    }
    setGeste(null)
    return true
  }, [])

  return { ordres, geste, rangerAuGlisser, gestes: { surAppui, surDeplacement, surRelache, annuler: oublier } }
}
