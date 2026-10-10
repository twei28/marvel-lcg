// L'etape du cartouche de la phase du mechant que le joueur LIT, partagee avec
// le spectateur (POST /set_etape, GET /get_etapes). Le monde ne suffit pas :
// une trame retenue peut porter deux etapes, et seul le joueur sait laquelle
// il regarde.
import { useEffect, useState } from 'react'
import { lecteurActif } from './relecture/lecteur'
import type { ModePhaseMechant } from './moteur'

export type EtapesLues = Record<string, { cle: string; t: number; mode?: string }>

/** Ce que le spectateur suit du joueur : l'etape qu'il lit, son mode de phase, et s'il a referme le cartouche. */
export type Suivi = { cle?: string; mode?: ModePhaseMechant; ferme?: boolean }

const MODES: readonly string[] = ['detaille', 'detaille-bis', 'sur-table', 'instantane']
export const modeLu = (mode: string | undefined): ModePhaseMechant | undefined =>
  mode && MODES.includes(mode) ? (mode as ModePhaseMechant) : undefined

export const DELAI_LECTURE_ETAPES_MS = 700

export function publierEtape(siege: number, cle: string | undefined, mode?: ModePhaseMechant): void {
  void fetch('/set_etape', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ p: siege, cle: cle ?? '', mode: mode ?? '' }),
  }).catch(() => undefined)
}

/** Le suivi du joueur le plus recent : son etape (non vide) et son mode (le dernier publie). */
export function suiviLePlusRecent(etapes: EtapesLues): Suivi {
  let recent: { cle: string; t: number; mode?: string } | undefined
  for (const etape of Object.values(etapes)) {
    if (!recent || etape.t > recent.t) recent = etape
  }
  return { cle: cleLaPlusRecente(etapes), mode: modeLu(recent?.mode), ferme: recent !== undefined && !recent.cle }
}

/** La cle lue le plus recemment, tous joueurs confondus : celui qui vient de cliquer. */
export function cleLaPlusRecente(etapes: EtapesLues): string | undefined {
  let meilleure: { cle: string; t: number } | undefined
  for (const etape of Object.values(etapes)) {
    if (!etape.cle) continue
    if (!meilleure || etape.t > meilleure.t) meilleure = etape
  }
  return meilleure?.cle
}

/** Rang de l'etape a montrer au spectateur : celle du joueur, sinon la derniere connue. */
export function indexSpectateur(cles: string[], cleSuivie: string | undefined): number {
  const rang = cleSuivie === undefined ? -1 : cles.indexOf(cleSuivie)
  return rang !== -1 ? rang : Math.max(0, cles.length - 1)
}

export function useSuiviDuJoueur(actif: boolean): Suivi {
  const [suivi, setSuivi] = useState<Suivi>({})
  useEffect(() => {
    if (!actif) return
    const changer = (neuf: Suivi) =>
      setSuivi((ancien) =>
        ancien.cle === neuf.cle && ancien.mode === neuf.mode && ancien.ferme === neuf.ferme ? ancien : neuf
      )
    const lecteur = lecteurActif()
    if (lecteur) {
      const minuteur = window.setInterval(() => {
        const t = lecteur.tempsCourant()
        changer({ cle: lecteur.etapeA(t), mode: modeLu(lecteur.modeA(t)), ferme: lecteur.cartoucheFermeA(t) })
      }, 100)
      return () => window.clearInterval(minuteur)
    }
    let vivant = true
    const lire = () =>
      fetch('/get_etapes', { cache: 'no-store' })
        .then((reponse) => (reponse.ok ? reponse.json() : {}))
        .then((donnees: EtapesLues) => {
          if (vivant) changer(suiviLePlusRecent(donnees))
        })
        .catch(() => undefined)
    void lire()
    const minuteur = window.setInterval(() => void lire(), DELAI_LECTURE_ETAPES_MS)
    return () => {
      vivant = false
      window.clearInterval(minuteur)
    }
  }, [actif])
  return suivi
}
