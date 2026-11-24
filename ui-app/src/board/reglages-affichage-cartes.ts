// TROIS REGLAGES D'AFFICHAGE DES CARTES, gardes dans le navigateur (decisions du 28/10/2026,
// zoom ajoute le 05/11/2026 -- demande de Feyli, "la carte affichee au survol, je la trouve un
// peu petite") :
//  - les pastilles de traits du heros (tous / seulement les changements / aucun) ;
//  - le chevauchement des ameliorations derriere leur porteur (moitie / quart / collees / espacees) ;
//  - le zoom de l'apercu agrandi au survol (70% a 150% de la taille de depart).
// Meme patron que `cote-ameliorations.ts` : un evenement previent le plateau ouvert, sans rechargement.
import { useEffect, useState } from 'react'
import type { ModeTraits } from './traits-heros'

export type ChevauchementAmeliorations = 'moitie' | 'quart' | 'collees' | 'espacees'

export const CLE_TRAITS_PASTILLES = 'mc_traits_pastilles'
export const CLE_CHEVAUCHEMENT = 'mc_ameliorations_chevauchement'
export const CLE_ZOOM_APERCU = 'mc_apercu_zoom'
const EVENEMENT = 'mc-reglages-affichage-cartes-change'

const MODES_TRAITS: readonly ModeTraits[] = ['tous', 'changements', 'aucun']
const CHEVAUCHEMENTS: readonly ChevauchementAmeliorations[] = ['moitie', 'quart', 'collees', 'espacees']

/** Plage du curseur de zoom (point discute avec l'utilisateur, 05/11/2026) : les deux sens,
 * pour reduire aussi bien qu'agrandir la taille de depart de l'apercu. */
export const ZOOM_APERCU_MIN = 0.7
export const ZOOM_APERCU_MAX = 1.5
export const ZOOM_APERCU_DEFAUT = 1

/** Largeur d'une carte attachee (board.css : `.est-attachee .scan-card { --card-w: 127px }`). */
const LARGEUR_CARTE = 127

/** Le cran d'une amelioration a la suivante, en px : la part de la carte laissee VISIBLE. */
export const PAS_PAR_CHEVAUCHEMENT: Readonly<Record<ChevauchementAmeliorations, number>> = {
  moitie: 63, // l'existant : la moitie cachee
  quart: Math.round(LARGEUR_CARTE * 0.75), // un quart cache, les trois quarts visibles
  collees: LARGEUR_CARTE, // bord a bord, rien de cache
  espacees: LARGEUR_CARTE + 8, // un petit trou, comme les autres zones
}

function lire<T extends string>(cle: string, valides: readonly T[], defaut: T): T {
  try {
    const valeur = window.localStorage.getItem(cle)
    return valides.find((v) => v === valeur) ?? defaut
  } catch {
    return defaut
  }
}

function ecrire(cle: string, valeur: string): void {
  try {
    window.localStorage.setItem(cle, valeur)
  } catch {
    /* stockage indisponible : le choix vaut jusqu'au rechargement */
  }
  window.dispatchEvent(new Event(EVENEMENT))
}

function useReglage<T>(lireValeur: () => T): T {
  const [valeur, setValeur] = useState(lireValeur)
  useEffect(() => {
    const relire = () => setValeur(lireValeur)
    window.addEventListener(EVENEMENT, relire)
    window.addEventListener('storage', relire)
    return () => {
      window.removeEventListener(EVENEMENT, relire)
      window.removeEventListener('storage', relire)
    }
  }, [lireValeur])
  return valeur
}

export const lireModeTraits = (): ModeTraits => lire(CLE_TRAITS_PASTILLES, MODES_TRAITS, 'changements')
export const ecrireModeTraits = (mode: ModeTraits): void => ecrire(CLE_TRAITS_PASTILLES, mode)
export const useModeTraits = (): ModeTraits => useReglage(lireModeTraits)

export const lireChevauchement = (): ChevauchementAmeliorations => lire(CLE_CHEVAUCHEMENT, CHEVAUCHEMENTS, 'moitie')
export const ecrireChevauchement = (valeur: ChevauchementAmeliorations): void => ecrire(CLE_CHEVAUCHEMENT, valeur)
export const useChevauchement = (): ChevauchementAmeliorations => useReglage(lireChevauchement)

export function lireZoomApercu(): number {
  try {
    const brut = window.localStorage.getItem(CLE_ZOOM_APERCU)
    if (brut === null) return ZOOM_APERCU_DEFAUT
    const valeur = Number(brut)
    return Number.isFinite(valeur) ? Math.min(ZOOM_APERCU_MAX, Math.max(ZOOM_APERCU_MIN, valeur)) : ZOOM_APERCU_DEFAUT
  } catch {
    return ZOOM_APERCU_DEFAUT
  }
}
export const ecrireZoomApercu = (valeur: number): void =>
  ecrire(CLE_ZOOM_APERCU, String(Math.min(ZOOM_APERCU_MAX, Math.max(ZOOM_APERCU_MIN, valeur))))
export const useZoomApercu = (): number => useReglage(lireZoomApercu)

/**
 * Pose `--zoom-apercu` sur la racine tant que le plateau est monte (meme patron que
 * `useInversionPiles`) : `.carte-apercu` (board.css) la lit pour sa largeur. A appeler UNE FOIS,
 * depuis le plateau -- jamais depuis le panneau de reglages lui-meme, qui n'est pas toujours monte.
 */
export function useZoomApercuSync(): void {
  const zoom = useZoomApercu()
  useEffect(() => {
    document.documentElement.style.setProperty('--zoom-apercu', String(zoom))
    return () => { document.documentElement.style.removeProperty('--zoom-apercu') }
  }, [zoom])
}
