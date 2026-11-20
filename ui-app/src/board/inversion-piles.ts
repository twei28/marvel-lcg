// L'INVERSION DES PILES (demande d'un joueur, 03/11/2026) : « choisir de quel cote le deck et de quel cote la defausse ».
// Une case dans Reglages, Apparence, DESACTIVEE par defaut : elle echange la place du deck et de la defausse partout
// sur le plateau (le joueur, la rencontre, le deck special). Un seul reglage, garde dans le navigateur, pour toutes
// les parties du joueur.
//
// ⚠ LE PLATEAU NE CHANGE PAS : le reglage ne passe QUE par un attribut de <html> (`data-piles-inversees`), que lit
// board.css (`order` sur la premiere pile d'un groupe). Rien n'est recalcule dans zones.ts, donc rien ne bouge
// pour le glisser-deposer, le mode manuel ni la sauvegarde des positions.
import { useEffect, useState } from 'react'

export const CLE_INVERSION_PILES = 'mc_piles_inversees'
const EVENEMENT = 'mc-piles-inversees-change'

export function lireInversionPiles(): boolean {
  try {
    return window.localStorage.getItem(CLE_INVERSION_PILES) === 'oui'
  } catch {
    return false
  }
}

export function ecrireInversionPiles(actif: boolean): void {
  try {
    window.localStorage.setItem(CLE_INVERSION_PILES, actif ? 'oui' : 'non')
  } catch {
    /* stockage indisponible : le choix vaut jusqu'au rechargement */
  }
  window.dispatchEvent(new Event(EVENEMENT))
}

/** Pose (ou retire) l'attribut que lit la feuille de style. */
export function appliquerInversionPiles(actif: boolean, racine: HTMLElement = document.documentElement): void {
  if (actif) racine.dataset.pilesInversees = 'oui'
  else delete racine.dataset.pilesInversees
}

/** Le reglage, tenu a jour quand on le bascule ; pose l'attribut tant que le plateau est monte. */
export function useInversionPiles(): boolean {
  const [actif, setActif] = useState(lireInversionPiles)
  useEffect(() => {
    const relire = () => setActif(lireInversionPiles())
    window.addEventListener(EVENEMENT, relire)
    window.addEventListener('storage', relire)
    return () => {
      window.removeEventListener(EVENEMENT, relire)
      window.removeEventListener('storage', relire)
    }
  }, [])
  useEffect(() => {
    appliquerInversionPiles(actif)
    return () => appliquerInversionPiles(false)
  }, [actif])
  return actif
}
