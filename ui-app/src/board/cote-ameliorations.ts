// LE COTE DES AMELIORATIONS (decision du 07/10/2026) : a droite de la carte qui
// les porte (comme toujours), ou a gauche pour qui en a l'habitude. Un seul
// reglage pour toutes les cartes (heros, allies, mechant, sbires), garde dans
// le navigateur. C'est le cote PAR DEFAUT : Alt + glisser pose une amelioration
// precise de l'autre cote (ordre/ordre-cartes.ts, `poserDuCote`), et ce choix-la
// reste meme si le reglage change.
import { useEffect, useState } from 'react'

export type CoteAmeliorations = 'droite' | 'gauche'

export const CLE_COTE_AMELIORATIONS = 'mc_ameliorations_cote'
const EVENEMENT = 'mc-cote-ameliorations-change'

export function lireCoteAmeliorations(): CoteAmeliorations {
  try {
    return window.localStorage.getItem(CLE_COTE_AMELIORATIONS) === 'gauche' ? 'gauche' : 'droite'
  } catch {
    return 'droite'
  }
}

export function ecrireCoteAmeliorations(cote: CoteAmeliorations): void {
  try {
    window.localStorage.setItem(CLE_COTE_AMELIORATIONS, cote)
  } catch {
    /* stockage indisponible : le choix vaut jusqu'au rechargement */
  }
  window.dispatchEvent(new Event(EVENEMENT))
}

export function useCoteAmeliorations(): CoteAmeliorations {
  const [cote, setCote] = useState(lireCoteAmeliorations)
  useEffect(() => {
    const relire = () => setCote(lireCoteAmeliorations())
    window.addEventListener(EVENEMENT, relire)
    window.addEventListener('storage', relire)
    return () => {
      window.removeEventListener(EVENEMENT, relire)
      window.removeEventListener('storage', relire)
    }
  }, [])
  return cote
}
