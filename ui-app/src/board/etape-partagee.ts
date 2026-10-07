// L'etape du cartouche de la phase du mechant que le joueur LIT, partagee avec
// le spectateur (POST /set_etape, GET /get_etapes). Le monde ne suffit pas :
// une trame retenue peut porter deux etapes, et seul le joueur sait laquelle
// il regarde.
import { useEffect, useState } from 'react'

export type EtapesLues = Record<string, { cle: string; t: number }>

export const DELAI_LECTURE_ETAPES_MS = 700

export function publierEtape(siege: number, cle: string | undefined): void {
  void fetch('/set_etape', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ p: siege, cle: cle ?? '' }),
  }).catch(() => undefined)
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

export function useEtapeSuivie(actif: boolean): string | undefined {
  const [cle, setCle] = useState<string>()
  useEffect(() => {
    if (!actif) return
    let vivant = true
    const lire = () =>
      fetch('/get_etapes', { cache: 'no-store' })
        .then((reponse) => (reponse.ok ? reponse.json() : {}))
        .then((donnees: EtapesLues) => {
          if (vivant) setCle(cleLaPlusRecente(donnees))
        })
        .catch(() => undefined)
    void lire()
    const minuteur = window.setInterval(() => void lire(), DELAI_LECTURE_ETAPES_MS)
    return () => {
      vivant = false
      window.clearInterval(minuteur)
    }
  }, [actif])
  return cle
}
