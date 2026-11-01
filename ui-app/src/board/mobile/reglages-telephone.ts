// LES REGLAGES DU TELEPHONE (zone 3 de la refonte du 09/10/2026,
// .planning/todos/2026-10-09-mode-telephone-refonte.md, « Plateau ») :
// taille du texte a trois niveaux, vibrations, verrou portrait.
//
// Retenus sur CET appareil (localStorage), comme les languettes (Encoche.tsx) :
// ce sont des preferences du telephone, pas du joueur. Un changement est
// annonce par un evenement de fenetre, pour que le plateau ouvert suive sans
// rechargement (`useReglagesTelephone`).
import { useEffect, useState } from 'react'
import { COLONNES_PAR_DEFAUT, type ColonnesZones, type NbColonnes } from './ronds/disposition-ronds'

export type TailleTexte = 'normal' | 'grand' | 'tres-grand'

export type PlateauTelephone = 'cartes' | 'ronds'

export type ReglagesTelephone = {
  /** La forme de la table au telephone : les cartes en bandes (d'origine) ou les ronds (essai, 24/10/2026). */
  plateau: PlateauTelephone
  /** Le joueur a coche « garder ce choix » : on ne lui repose plus la question au debut de chaque partie. */
  plateauMemorise: boolean
  /** La visite guidee des ronds s'ouvre a la prochaine partie (une seule fois : elle se coupe en se fermant). */
  aideDebut: boolean
  /** La nouveaute « cartes empilees » de la visite (26/10/2026) n'a pas encore ete vue : un joueur qui a deja fait la visite ne la voit qu'elle, une seule fois. */
  visitePiles: boolean
  /** Les colonnes de chaque zone de la table en ronds (26/10/2026) : 1 a 4, ou 0 = Auto. */
  colonnesZones: ColonnesZones
  tailleTexte: TailleTexte
  vibrations: boolean
  verrouPortrait: boolean
}

export const CLES_TELEPHONE = {
  plateau: 'marvel-tel-plateau',
  plateauMemorise: 'marvel-tel-plateau-memorise',
  aideDebut: 'marvel-tel-aide-debut',
  visitePiles: 'marvel-tel-visite-piles',
  colonnesZones: 'marvel-tel-colonnes-zones',
  tailleTexte: 'marvel-tel-taille-texte',
  vibrations: 'marvel-tel-vibrations',
  verrouPortrait: 'marvel-tel-verrou-portrait',
} as const

export const EVENEMENT_REGLAGES_TELEPHONE = 'marvel:reglages-telephone'

export const DEFAUTS_TELEPHONE: ReglagesTelephone = {
  plateau: 'cartes',
  plateauMemorise: false,
  aideDebut: true,
  visitePiles: true,
  colonnesZones: COLONNES_PAR_DEFAUT,
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

/** L'ordre des zones dans la valeur enregistree : « manigances,allies,sbires,enJeu » (par exemple « 3,3,3,4 »). */
const ZONES_COLONNES = ['manigances', 'allies', 'sbires', 'enJeu'] as const
export type ZoneAColonnes = (typeof ZONES_COLONNES)[number]

function lireColonnes(): ColonnesZones {
  const brut = (lire(CLES_TELEPHONE.colonnesZones) ?? '').split(',')
  const sortie = { ...COLONNES_PAR_DEFAUT }
  ZONES_COLONNES.forEach((zone, i) => {
    const v = Number(brut[i])
    if (brut[i] !== undefined && brut[i] !== '' && Number.isInteger(v) && v >= 0 && v <= 4) sortie[zone] = v as NbColonnes
  })
  return sortie
}

/** Choisit le nombre de colonnes d'UNE zone (0 = Auto) et le retient sur cet appareil. */
export function ecrireColonnesZone(zone: ZoneAColonnes, valeur: NbColonnes): void {
  const actuelles = lireColonnes()
  actuelles[zone] = valeur
  try {
    window.localStorage.setItem(CLES_TELEPHONE.colonnesZones, ZONES_COLONNES.map((z) => actuelles[z]).join(','))
  } catch {
    // Stockage indisponible (navigation privee) : le reglage reste a son defaut.
  }
  window.dispatchEvent(new CustomEvent(EVENEMENT_REGLAGES_TELEPHONE))
}

/** Le joueur a-t-il deja choisi la forme de la table ? Sinon on lui propose les ronds en premier (plus adaptes au telephone, 26/10/2026). */
export function plateauDejaChoisi(): boolean {
  const v = lire(CLES_TELEPHONE.plateau)
  return v === 'ronds' || v === 'cartes'
}

export function lireReglagesTelephone(): ReglagesTelephone {
  const taille = lire(CLES_TELEPHONE.tailleTexte)
  return {
    plateau: lire(CLES_TELEPHONE.plateau) === 'ronds' ? 'ronds' : 'cartes',
    plateauMemorise: lire(CLES_TELEPHONE.plateauMemorise) === 'oui',
    aideDebut: lire(CLES_TELEPHONE.aideDebut) !== 'non',
    visitePiles: lire(CLES_TELEPHONE.visitePiles) !== 'non',
    colonnesZones: lireColonnes(),
    tailleTexte: taille === 'grand' || taille === 'tres-grand' ? taille : 'normal',
    vibrations: lire(CLES_TELEPHONE.vibrations) !== 'non',
    verrouPortrait: lire(CLES_TELEPHONE.verrouPortrait) === 'oui',
  }
}

export function ecrireReglageTelephone<K extends Exclude<keyof ReglagesTelephone, 'colonnesZones'>>(cle: K, valeur: ReglagesTelephone[K]): void {
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
