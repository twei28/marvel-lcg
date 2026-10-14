// L'ÉQUIPE RESTE ENSEMBLE ENTRE DEUX MANCHES (13/10/2026).
//
// Demande de l'utilisateur : « en fin de partie, que les joueurs qu'on a
// invités restent dans le même lobby, et dès qu'on crée une partie, qu'ils
// aient de nouveau accès à la sélection de personnages ».
//
// Avant, « Retour au choix du héros » envoyait TOUT LE MONDE sur
// `/prepare.html`, c'est-à-dire l'invité sur l'assistant de l'HÔTE, où il n'a
// rien à faire. L'invité retourne désormais à SON salon (son siège, son cookie,
// son choix d'avant pré-coché : `public/js/salon/bascule.js`). Et s'il est
// resté sur l'écran de fin, il y revient tout seul dès que l'hôte rouvre la
// préparation (`/annoncer_preparation` côté moteur, un simple compteur).

import { useEffect } from 'react'
import { atterrir } from './quitter-la-table'

export type Navigateur = { siege: number; multi: boolean; spectateur: boolean }

/** Ce navigateur est-il un invité d'une table répartie (pas l'hôte, pas un spectateur) ? */
export function estInviteDeTable({ siege, multi, spectateur }: Navigateur): boolean {
  return multi && !spectateur && siege > 0
}

/** Où mène « Retour » à la fin d'une partie. */
export function adresseApresPartie(nav: Navigateur): string {
  return estInviteDeTable(nav) ? `/salon.html?p=${nav.siege}` : '/prepare.html'
}

/**
 * L'hôte a-t-il rouvert la préparation depuis la fin de la partie ?
 *
 * Seul le CHANGEMENT du compteur compte : il a pu préparer dix fois avant,
 * la valeur relevée à la fin de la partie sert de point de départ. Une lecture
 * manquée (table muette) ne conclut rien.
 */
export function hoteEnPreparation(depart: number | undefined, actuel: number | undefined): boolean {
  return depart !== undefined && actuel !== undefined && actuel !== depart
}

async function lireCompteur(): Promise<number | undefined> {
  try {
    const reponse = await fetch('/get_preparation', { cache: 'no-store' })
    if (!reponse.ok) return undefined
    const brut: unknown = await reponse.json()
    const n = (brut as { n?: unknown }).n
    return typeof n === 'number' ? n : undefined
  } catch {
    return undefined
  }
}

export const CADENCE_RETOUR_MS = 3000

/** Pendant que l'écran de fin est affiché chez un invité : le ramène au salon dès que l'hôte prépare. */
export function useRetourAuSalon(actif: boolean, siege: number): void {
  useEffect(() => {
    if (!actif) return
    let vivant = true
    let depart: number | undefined
    let minuteur: number | undefined
    const sonder = async () => {
      // Onglet caché : on ne fait pas vivre la table pour rien (même règle que le salon).
      if (!document.hidden) {
        const actuel = await lireCompteur()
        if (!vivant) return
        if (depart === undefined) depart = actuel
        else if (hoteEnPreparation(depart, actuel)) {
          atterrir(`/salon.html?p=${siege}`)
          return
        }
      }
      minuteur = window.setTimeout(() => void sonder(), CADENCE_RETOUR_MS)
    }
    void sonder()
    return () => {
      vivant = false
      if (minuteur !== undefined) window.clearTimeout(minuteur)
    }
  }, [actif, siege])
}
