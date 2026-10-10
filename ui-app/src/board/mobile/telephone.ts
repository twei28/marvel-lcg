// LE TELEPHONE PENDANT UNE PARTIE (zone 3 de la refonte du 09/10/2026) :
// ecran maintenu allume, vibrations sur trois moments, verrou portrait.
//
// Monte par la page de partie (board.tsx), sur les DEUX rendus : un telephone
// couche joue sur le plateau PC reduit, et doit garder son ecran allume comme
// debout. Sur un ordinateur rien ne s'allume (`REQUETE_TELEPHONE` ne
// correspond pas) : le PC reste exactement ce qu'il etait.
import { useEffect, useRef, useState } from 'react'
import { EVENEMENT_REPONSE_ENVOYEE } from '../moteur'
import type { World } from '../world'
import { lireReglagesTelephone } from './reglages-telephone'

/**
 * Un telephone, debout (etroit) ou couche (bas ET tactile). Une fenetre de PC
 * etroite compte aussi : elle a le plateau en bandes, elle a donc ses reglages.
 */
export const REQUETE_TELEPHONE = '(max-width: 767px), (pointer: coarse) and (max-height: 500px)'

export function estTelephone(): boolean {
  try {
    return window.matchMedia(REQUETE_TELEPHONE).matches
  } catch {
    return false
  }
}

export function useEstTelephone(): boolean {
  const [oui, setOui] = useState(estTelephone)
  useEffect(() => {
    let liste: MediaQueryList
    try {
      liste = window.matchMedia(REQUETE_TELEPHONE)
    } catch {
      return
    }
    const suivre = (evenement: MediaQueryListEvent) => setOui(evenement.matches)
    liste.addEventListener('change', suivre)
    return () => liste.removeEventListener('change', suivre)
  }, [])
  return oui
}

/* ------------------------------------------------------------ le geste -- */

/**
 * Le dernier geste du joueur (doigt, souris, clavier). Une reponse envoyee
 * au moteur sans geste recent est une reponse AUTOMATIQUE (cible unique,
 * paiement seul, fin de tour auto) : elle ne vibre pas et ne propose pas
 * « Annuler ».
 */
let dernierGeste = 0
let suiviInstalle = false

export const DELAI_GESTE_MS = 2500

export function installerSuiviDuGeste(): void {
  if (suiviInstalle || typeof document === 'undefined') return
  suiviInstalle = true
  const noter = () => {
    dernierGeste = Date.now()
  }
  document.addEventListener('pointerdown', noter, true)
  document.addEventListener('keydown', noter, true)
}

export function gesteRecent(maintenant = Date.now()): boolean {
  return dernierGeste > 0 && maintenant - dernierGeste <= DELAI_GESTE_MS
}

/** Pour les tests : oublie le dernier geste. */
export function oublierGeste(): void {
  dernierGeste = 0
}

/* -------------------------------------------------------- les vibrations -- */

export type MomentVibrant = 'tour' | 'attaque' | 'validation'

/** Courtes et distinctes : deux tapes pour ton tour, une longue pour un coup. */
export const MOTIFS: Record<MomentVibrant, number | number[]> = {
  tour: [60, 80, 60],
  attaque: 180,
  validation: 15,
}

/** Vibre si le reglage le permet et si l'appareil sait le faire. Ne leve jamais. */
export function vibrer(moment: MomentVibrant): boolean {
  if (!lireReglagesTelephone().vibrations) return false
  if (typeof navigator === 'undefined' || typeof navigator.vibrate !== 'function') return false
  try {
    return navigator.vibrate(MOTIFS[moment])
  } catch {
    return false
  }
}

/** « C'est ton tour » : la phase devient celle de ce siege (`Player N Turn`, N a partir de 1). */
export function estMonTour(monde: World | undefined, siege: number): boolean {
  return monde?.phase === `Player ${siege + 1} Turn`
}

/** Les PV restants de l'identite de ce siege, s'ils sont connus. */
export function pvDuHeros(monde: World | undefined, siege: number): number | undefined {
  const pv = monde?.players?.[siege]?.area_hero?.[0]?.info?.health
  return typeof pv === 'number' && Number.isFinite(pv) ? pv : undefined
}

/**
 * Les trois moments : ton tour commence, ton heros perd des PV, une reponse
 * part apres un geste. Le premier etat recu ne vibre pas (un rechargement de
 * page en plein tour n'est pas un nouveau tour).
 */
export function useVibrationsDePartie(monde: World | undefined, siege: number, actif: boolean): void {
  const precedent = useRef<{ tour: boolean; pv: number | undefined } | undefined>(undefined)
  useEffect(() => {
    if (!monde) return
    const maintenant = { tour: estMonTour(monde, siege), pv: pvDuHeros(monde, siege) }
    const avant = precedent.current
    precedent.current = maintenant
    if (!actif || !avant) return
    if (maintenant.tour && !avant.tour) vibrer('tour')
    else if (avant.pv !== undefined && maintenant.pv !== undefined && maintenant.pv < avant.pv) vibrer('attaque')
  }, [monde, siege, actif])

  useEffect(() => {
    if (!actif) return
    installerSuiviDuGeste()
    const surReponse = () => {
      if (gesteRecent()) vibrer('validation')
    }
    window.addEventListener(EVENEMENT_REPONSE_ENVOYEE, surReponse)
    return () => window.removeEventListener(EVENEMENT_REPONSE_ENVOYEE, surReponse)
  }, [actif])
}

/* ------------------------------------------------- l'ecran reste allume -- */

type VerrouEcran = { release: () => Promise<void>; addEventListener?: (type: 'release', f: () => void) => void }
type NavigateurAvecVerrou = Navigator & { wakeLock?: { request: (type: 'screen') => Promise<VerrouEcran> } }

/**
 * L'ecran ne s'eteint pas pendant une partie (Screen Wake Lock). Le systeme
 * relache le verrou quand la page passe en arriere-plan : on le redemande au
 * retour. Un refus (batterie faible, navigateur sans l'API) n'est pas une
 * erreur : l'ecran s'eteindra comme d'habitude.
 */
export function useEcranAllume(actif: boolean): void {
  useEffect(() => {
    const api = (navigator as NavigateurAvecVerrou).wakeLock
    if (!actif || !api) return
    let verrou: VerrouEcran | undefined
    let fini = false
    const demander = () => {
      if (fini || document.visibilityState !== 'visible' || verrou) return
      api
        .request('screen')
        .then((obtenu) => {
          if (fini) {
            void obtenu.release().catch(() => undefined)
            return
          }
          verrou = obtenu
          obtenu.addEventListener?.('release', () => {
            verrou = undefined
          })
        })
        .catch(() => undefined)
    }
    demander()
    document.addEventListener('visibilitychange', demander)
    return () => {
      fini = true
      document.removeEventListener('visibilitychange', demander)
      if (verrou) void verrou.release().catch(() => undefined)
      verrou = undefined
    }
  }, [actif])
}

/* -------------------------------------------------- le verrou portrait -- */

type OrientationVerrouillable = ScreenOrientation & {
  lock?: (orientation: 'portrait') => Promise<void>
  unlock?: () => void
}

/**
 * Le verrou portrait (reglage, desactive par defaut). Le navigateur ne fige
 * l'orientation qu'en plein ecran ou en application installee : on le demande
 * a chaque entree en plein ecran. Quand il refuse (iOS, navigateur classique),
 * `tourner` dit au plateau de demander qu'on remette le telephone debout.
 */
export function useVerrouPortrait(actif: boolean, verrou: boolean): { tourner: boolean } {
  const [couche, setCouche] = useState(() => {
    try {
      return window.matchMedia('(orientation: landscape)').matches
    } catch {
      return false
    }
  })
  useEffect(() => {
    let liste: MediaQueryList
    try {
      liste = window.matchMedia('(orientation: landscape)')
    } catch {
      return
    }
    const suivre = (evenement: MediaQueryListEvent) => setCouche(evenement.matches)
    liste.addEventListener('change', suivre)
    return () => liste.removeEventListener('change', suivre)
  }, [])

  useEffect(() => {
    const orientation = (typeof screen !== 'undefined' ? screen.orientation : undefined) as
      | OrientationVerrouillable
      | undefined
    if (!actif || !orientation?.lock) return
    const appliquer = () => {
      if (verrou) orientation.lock?.('portrait').catch(() => undefined)
      else {
        try {
          orientation.unlock?.()
        } catch {
          // Rien de verrouille : rien a relacher.
        }
      }
    }
    appliquer()
    document.addEventListener('fullscreenchange', appliquer)
    return () => document.removeEventListener('fullscreenchange', appliquer)
  }, [actif, verrou])

  return { tourner: actif && verrou && couche }
}
