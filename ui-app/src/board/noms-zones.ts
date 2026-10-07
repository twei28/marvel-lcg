// LES NOMS DONNES AUX ZONES DE LA TABLE (decision du 07/10/2026) : un nom libre
// par zone, pour ce joueur, toutes ses parties, sur ce navigateur. Garde A PART
// de la disposition : celle-ci a un format compact que le compte valide, et un
// nom n'a rien a y faire. La zone est reconnue par son ancre (sa premiere
// brique), comme partout ailleurs ; un nom vide rend le titre automatique.
import { useEffect, useState } from 'react'

export const CLE_NOMS_ZONES = 'mc_noms_zones_v1'
const EVENEMENT = 'mc-noms-zones-change'
export const LONGUEUR_MAX_NOM = 40

export function lireNomsZones(): Record<string, string> {
  try {
    const brut = JSON.parse(window.localStorage.getItem(CLE_NOMS_ZONES) ?? '{}')
    if (!brut || typeof brut !== 'object' || Array.isArray(brut)) return {}
    return Object.fromEntries(
      Object.entries(brut as Record<string, unknown>).filter(
        (e): e is [string, string] => typeof e[1] === 'string' && e[1].trim() !== ''
      )
    )
  } catch {
    return {}
  }
}

export function nommerZone(ancre: string, nom: string): void {
  const noms = lireNomsZones()
  const propre = nom.trim().slice(0, LONGUEUR_MAX_NOM)
  if (propre) noms[ancre] = propre
  else delete noms[ancre]
  try {
    window.localStorage.setItem(CLE_NOMS_ZONES, JSON.stringify(noms))
  } catch {
    /* stockage indisponible : le nom vaut jusqu'au rechargement */
  }
  window.dispatchEvent(new Event(EVENEMENT))
}

export function useNomsZones(): Record<string, string> {
  const [noms, setNoms] = useState(lireNomsZones)
  useEffect(() => {
    const relire = () => setNoms(lireNomsZones())
    window.addEventListener(EVENEMENT, relire)
    window.addEventListener('storage', relire)
    return () => {
      window.removeEventListener(EVENEMENT, relire)
      window.removeEventListener('storage', relire)
    }
  }, [])
  return noms
}
