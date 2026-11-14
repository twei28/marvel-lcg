// LA TABLETTE (chantier du 24/10/2026, .planning/todos/2026-10-24-mode-tablette.md) :
// le plateau PC, en paysage, joue AU DOIGT. Pas de souris : ni survol, ni clic
// droit, ni petites zones.
//
// Ce fichier ne fait que DIRE si l'on est en tablette (decision 10) :
//  - automatiquement : un ecran tactile SANS souris (`pointer: coarse` et
//    `hover: none`), assez grand pour le plateau PC (768 px de large au moins,
//    et pas un telephone couche, qui a sa propre regle a 500 px de haut :
//    `REQUETE_TELEPHONE`) ;
//  - ou force par le reglage « Jeu au doigt : Auto / Oui / Non » (un PC a
//    ecran tactile, un iPad avec une souris).
//
// Le resultat est pose sur <html data-tablette> : les feuilles de style du
// plateau s'en servent (cibles de 44 px, languettes larges, bouton flottant
// retire), le code le lit par `useEstTablette`.
import { useEffect, useState } from 'react'
import './tablette.css'

export type ReglageDoigt = 'auto' | 'oui' | 'non'

export const CLE_JEU_AU_DOIGT = 'marvel-jeu-au-doigt'
export const EVENEMENT_JEU_AU_DOIGT = 'marvel:jeu-au-doigt'

/** Tactile sans souris, assez grand pour le plateau PC (un telephone couche reste un telephone). */
export const REQUETE_TABLETTE = '(pointer: coarse) and (hover: none) and (min-width: 768px) and (min-height: 501px)'

export function lireReglageDoigt(): ReglageDoigt {
  try {
    const brut = window.localStorage.getItem(CLE_JEU_AU_DOIGT)
    return brut === 'oui' || brut === 'non' ? brut : 'auto'
  } catch {
    return 'auto'
  }
}

export function ecrireReglageDoigt(reglage: ReglageDoigt): void {
  try {
    window.localStorage.setItem(CLE_JEU_AU_DOIGT, reglage)
  } catch {
    // Navigation privee : le reglage reste sur Auto.
  }
  window.dispatchEvent(new CustomEvent(EVENEMENT_JEU_AU_DOIGT))
}

function appareilTablette(): boolean {
  try {
    return window.matchMedia(REQUETE_TABLETTE).matches
  } catch {
    return false
  }
}

/** La regle, PURE : le reglage l'emporte, Auto suit l'appareil. */
export function tabletteEffective(reglage: ReglageDoigt, appareil: boolean): boolean {
  if (reglage === 'oui') return true
  if (reglage === 'non') return false
  return appareil
}

export function estTablette(): boolean {
  // `?tablette` dans l'adresse la force, pour l'eprouver depuis un PC (comme `?mobile`).
  try {
    if (new URLSearchParams(window.location.search).has('tablette')) return true
  } catch {
    /* pas d'adresse lisible */
  }
  return tabletteEffective(lireReglageDoigt(), appareilTablette())
}

export function useEstTablette(): boolean {
  const [oui, setOui] = useState(estTablette)
  useEffect(() => {
    const suivre = () => setOui(estTablette())
    let liste: MediaQueryList | undefined
    try {
      liste = window.matchMedia(REQUETE_TABLETTE)
      liste.addEventListener('change', suivre)
    } catch {
      /* matchMedia absent : seul le reglage compte */
    }
    window.addEventListener(EVENEMENT_JEU_AU_DOIGT, suivre)
    return () => {
      liste?.removeEventListener('change', suivre)
      window.removeEventListener(EVENEMENT_JEU_AU_DOIGT, suivre)
    }
  }, [])
  return oui
}

/** Pose <html data-tablette> tant que la tablette est active (les feuilles de style le lisent). */
export function useMarqueTablette(tablette: boolean): void {
  useEffect(() => {
    const racine = document.documentElement
    if (!tablette) {
      racine.removeAttribute('data-tablette')
      return
    }
    racine.setAttribute('data-tablette', '')
    // Decision 7 : pas de zoom du navigateur (il casse la mise en page du plateau).
    // Safari ignore `user-scalable=no` : son geste de pincement est aussi coupe.
    const meta = document.querySelector<HTMLMetaElement>('meta[name="viewport"]')
    const avant = meta?.content
    if (meta) meta.content = 'width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no'
    const pincement = (evenement: Event) => evenement.preventDefault()
    document.addEventListener('gesturestart', pincement)
    return () => {
      racine.removeAttribute('data-tablette')
      if (meta && avant !== undefined) meta.content = avant
      document.removeEventListener('gesturestart', pincement)
    }
  }, [tablette])
}

/** La tablette tenue debout : le plateau PC demande le paysage (decision 0). */
export function useTabletteDebout(tablette: boolean): boolean {
  const [debout, setDebout] = useState(() => {
    try {
      return window.matchMedia('(orientation: portrait)').matches
    } catch {
      return false
    }
  })
  useEffect(() => {
    let liste: MediaQueryList
    try {
      liste = window.matchMedia('(orientation: portrait)')
    } catch {
      return
    }
    const suivre = (evenement: MediaQueryListEvent) => setDebout(evenement.matches)
    liste.addEventListener('change', suivre)
    return () => liste.removeEventListener('change', suivre)
  }, [])
  return tablette && debout
}
