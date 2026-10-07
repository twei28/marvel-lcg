// LES MARQUES DU MODE MANUEL (lots 3 et 4 du 07/10/2026), comme OCTGN : une
// carte CIBLEE (Maj+clic), une FLECHE d'une carte vers une autre (Maj+glisser),
// un SURLIGNAGE de couleur (pave numerique). Vues de tous les joueurs : le
// serveur les garde (`/set_marque`, `/get_marques`, server_get.py), et rien ne
// touche au moteur. Le spectateur les voit, n'en pose pas.
import { useCallback, useEffect, useState } from 'react'
import { estSpectateur } from '../moteur'
import type { CouleurSurlignage } from './clavier'

export { COULEURS_PAVE, couleurDuPave, type CouleurSurlignage } from './clavier'

export type Marques = {
  cibles: Record<string, number>
  fleches: { de: number; a: number; p: number }[]
  surlignages: Record<string, CouleurSurlignage>
}

export const MARQUES_VIDES: Marques = { cibles: {}, fleches: [], surlignages: {} }

export type DemandeMarque =
  | { genre: 'cibler'; id: number }
  | { genre: 'fleche'; de: number; a: number }
  | { genre: 'decibler'; tous?: boolean }
  | { genre: 'surligner'; id: number; couleur: CouleurSurlignage | null }

function lireMarques(brut: unknown): Marques {
  const o = (brut && typeof brut === 'object' ? brut : {}) as Partial<Marques>
  return {
    cibles: o.cibles && typeof o.cibles === 'object' ? o.cibles : {},
    fleches: Array.isArray(o.fleches) ? o.fleches : [],
    surlignages: o.surlignages && typeof o.surlignages === 'object' ? o.surlignages : {},
  }
}

const ECOUTEURS = new Set<(m: Marques) => void>()

/** Envoie une marque au nom de ce siege ; tous les ecrans la verront a leur prochaine lecture. */
export async function envoyerMarque(siege: number, demande: DemandeMarque): Promise<void> {
  if (estSpectateur()) return
  const corps =
    demande.genre === 'decibler'
      ? { p: demande.tous ? -1 : siege, genre: 'decibler' }
      : { p: siege, ...demande }
  try {
    const reponse = await fetch('/set_marque', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(corps),
    })
    if (!reponse.ok) return
    const marques = lireMarques(await reponse.json())
    for (const ecouteur of ECOUTEURS) ecouteur(marques)
  } catch {
    /* cosmetique : une marque perdue ne bloque rien */
  }
}

export const DELAI_LECTURE_MARQUES_MS = 700

/** Les marques de la table, relues regulierement (et tout de suite apres un envoi d'ici). */
export function useMarques(actif: boolean): Marques {
  const [marques, setMarques] = useState<Marques>(MARQUES_VIDES)
  const recevoir = useCallback((m: Marques) => setMarques(m), [])
  useEffect(() => {
    if (!actif) {
      setMarques(MARQUES_VIDES)
      return
    }
    ECOUTEURS.add(recevoir)
    let vivant = true
    const lire = () =>
      fetch('/get_marques', { cache: 'no-store' })
        .then((reponse) => (reponse.ok ? reponse.json() : MARQUES_VIDES))
        .then((brut: unknown) => {
          if (vivant) setMarques(lireMarques(brut))
        })
        .catch(() => undefined)
    void lire()
    const minuteur = window.setInterval(() => void lire(), DELAI_LECTURE_MARQUES_MS)
    return () => {
      vivant = false
      ECOUTEURS.delete(recevoir)
      window.clearInterval(minuteur)
    }
  }, [actif, recevoir])
  return marques
}
