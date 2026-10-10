// LES REGLAGES DU TELEPHONE (zone 3 de la refonte du 09/10/2026,
// .planning/todos/2026-10-09-mode-telephone-refonte.md, « Plateau ») :
// taille du texte a trois niveaux, vibrations, verrou portrait.
//
// Retenus sur CET appareil (localStorage), comme les languettes (Encoche.tsx) :
// ce sont des preferences du telephone, pas du joueur. Un changement est
// annonce par un evenement de fenetre, pour que le plateau ouvert suive sans
// rechargement (`useReglagesTelephone`).
import { useEffect, useState } from 'react'

export type TailleTexte = 'normal' | 'grand' | 'tres-grand'

export type ReglagesTelephone = {
  tailleTexte: TailleTexte
  vibrations: boolean
  verrouPortrait: boolean
}

export const CLES_TELEPHONE = {
  tailleTexte: 'marvel-tel-taille-texte',
  vibrations: 'marvel-tel-vibrations',
  verrouPortrait: 'marvel-tel-verrou-portrait',
} as const

export const EVENEMENT_REGLAGES_TELEPHONE = 'marvel:reglages-telephone'

export const DEFAUTS_TELEPHONE: ReglagesTelephone = {
  tailleTexte: 'normal',
  vibrations: true,
  verrouPortrait: false,
}

function lire(cle: string): string | null {
  try {
    return window.localStorage.getItem(cle)
  } catch {
    return null
  }
}

export function lireReglagesTelephone(): ReglagesTelephone {
  const taille = lire(CLES_TELEPHONE.tailleTexte)
  return {
    tailleTexte: taille === 'grand' || taille === 'tres-grand' ? taille : 'normal',
    vibrations: lire(CLES_TELEPHONE.vibrations) !== 'non',
    verrouPortrait: lire(CLES_TELEPHONE.verrouPortrait) === 'oui',
  }
}

export function ecrireReglageTelephone<K extends keyof ReglagesTelephone>(cle: K, valeur: ReglagesTelephone[K]): void {
  const brut = typeof valeur === 'boolean' ? (valeur ? 'oui' : 'non') : String(valeur)
  try {
    window.localStorage.setItem(CLES_TELEPHONE[cle], brut)
  } catch {
    // Stockage indisponible (navigation privee) : le reglage reste a son defaut.
  }
  window.dispatchEvent(new CustomEvent(EVENEMENT_REGLAGES_TELEPHONE))
}

export function useReglagesTelephone(): ReglagesTelephone {
  const [reglages, setReglages] = useState(lireReglagesTelephone)
  useEffect(() => {
    const suivre = () => setReglages(lireReglagesTelephone())
    window.addEventListener(EVENEMENT_REGLAGES_TELEPHONE, suivre)
    return () => window.removeEventListener(EVENEMENT_REGLAGES_TELEPHONE, suivre)
  }, [])
  return reglages
}
