// DEUX REGLAGES D'AFFICHAGE DES CARTES, gardes dans le navigateur (decisions du 28/10/2026) :
//  - les pastilles de traits du heros (tous / seulement les changements / aucun) ;
//  - le chevauchement des ameliorations derriere leur porteur (moitie / quart / collees / espacees).
// Meme patron que `cote-ameliorations.ts` : un evenement previent le plateau ouvert, sans rechargement.
import { useEffect, useState } from 'react'
import type { ModeTraits } from './traits-heros'

export type ChevauchementAmeliorations = 'moitie' | 'quart' | 'collees' | 'espacees'

export const CLE_TRAITS_PASTILLES = 'mc_traits_pastilles'
export const CLE_CHEVAUCHEMENT = 'mc_ameliorations_chevauchement'
const EVENEMENT = 'mc-reglages-affichage-cartes-change'

const MODES_TRAITS: readonly ModeTraits[] = ['tous', 'changements', 'aucun']
const CHEVAUCHEMENTS: readonly ChevauchementAmeliorations[] = ['moitie', 'quart', 'collees', 'espacees']

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
