// Pose la mise en scene d'une etape sur les vraies cartes du plateau.
//
// IMPERATIF, comme halo-statut.ts et pas-a-pas.ts : classes ajoutees puis
// retirees sur l'element reel. Passer par React ferait re-rendre le plateau
// entier a chaque etape pour une decoration transitoire, et le plateau est
// lourd (plusieurs dizaines de cartes).
//
// Le nettoyage est fait a CHAQUE changement d'etape et au demontage : sans
// lui, quitter la phase laisserait une carte agrandie et un plateau assombri
// pour le reste de la partie.

import { useEffect } from 'react'
import type { EtapeDeroule } from './deroule-phase'
import { sceneDe } from './deroule-scene'

const EN_AVANT = 'deroule-en-avant'
const CIBLE = 'deroule-cible'
const VOILE = 'deroule-voile'

function carteDe(id: number): HTMLElement | null {
  return document.querySelector<HTMLElement>(
    `.plateau-scene .scan-card[data-card-id="${id}"]`
  )
}

export function useDerouleScene(etape: EtapeDeroule | undefined, actif: boolean): void {
  useEffect(() => {
    if (!actif || !etape) return
    const scene = sceneDe(etape)

    const auteur = scene.carteEnAvant !== undefined ? carteDe(scene.carteEnAvant) : null
    const cible = scene.cible !== undefined ? carteDe(scene.cible) : null

    auteur?.classList.add(EN_AVANT)
    cible?.classList.add(CIBLE)
    if (scene.voile) document.body.classList.add(VOILE)

    return () => {
      auteur?.classList.remove(EN_AVANT)
      cible?.classList.remove(CIBLE)
      document.body.classList.remove(VOILE)
    }
  }, [etape, actif])
}
