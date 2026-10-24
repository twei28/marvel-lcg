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

export type PlateauTelephone = 'cartes' | 'ronds'

export type ReglagesTelephone = {
  /** La forme de la table au telephone : les cartes en bandes (d'origine) ou les ronds (essai, 24/10/2026). */
  plateau: PlateauTelephone
  /** Le joueur a coche « garder ce choix » : on ne lui repose plus la question au debut de chaque partie. */
  plateauMemorise: boolean
  /** La visite guidee des ronds s'ouvre a la prochaine partie (une seule fois : elle se coupe en se fermant). */
  aideDebut: boolean
  tailleTexte: TailleTexte
  vibrations: boolean
  verrouPortrait: boolean
}

export const CLES_TELEPHONE = {
  plateau: 'marvel-tel-plateau',
  plateauMemorise: 'marvel-tel-plateau-memorise',
  aideDebut: 'marvel-tel-aide-debut',
  tailleTexte: 'marvel-tel-taille-texte',
  vibrations: 'marvel-tel-vibrations',
  verrouPortrait: 'marvel-tel-verrou-portrait',
} as const

export const EVENEMENT_REGLAGES_TELEPHONE = 'marvel:reglages-telephone'

export const DEFAUTS_TELEPHONE: ReglagesTelephone = {
  plateau: 'cartes',
  plateauMemorise: false,
  aideDebut: true,
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
    plateau: lire(CLES_TELEPHONE.plateau) === 'ronds' ? 'ronds' : 'cartes',
    plateauMemorise: lire(CLES_TELEPHONE.plateauMemorise) === 'oui',
    aideDebut: lire(CLES_TELEPHONE.aideDebut) !== 'non',
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
