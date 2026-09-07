// Le voile sur la table pendant qu'une etape est a l'ecran.
//
// Imperatif, sur le body, comme halo-statut.ts : une classe posee, une classe
// retiree. La scene centrale (DeroulePhase) montre les cartes elle-meme, a
// partir de l'index du monde ; ce hook ne touche plus aux cartes de la table,
// qui n'est plus a lire pendant la phase (voir la spec du 7 septembre 2026,
// docs/superpowers/specs/2026-09-07-scene-phase-mechant-design.md).

import { useEffect } from 'react'
import type { EtapeDeroule } from './deroule-phase'
import { sceneDe } from './deroule-scene'

const VOILE = 'deroule-voile'

export function useDerouleScene(etape: EtapeDeroule | undefined, actif: boolean): void {
  // Dependre de la CLE de l'etape, jamais de l'objet : la liste d'etapes est
  // recreee a chaque trame, l'etape courante aussi, et un effet qui en
  // dependrait retirerait et reposerait le voile a chaque rendu.
  const cle = etape?.cle
  const voile = etape !== undefined && sceneDe(etape).voile
  useEffect(() => {
    if (!actif || !voile) return
    document.body.classList.add(VOILE)
    return () => {
      document.body.classList.remove(VOILE)
    }
  }, [cle, actif, voile])
}
