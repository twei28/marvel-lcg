// Les numéros d'activation des sbires sur la table (essai, 13/10/2026, encadré ⑩).
//
// Décision de l'utilisateur : pendant l'étape 2B, chaque sbire porte son numéro
// d'ordre (1, 2, 3) sur la table ; un sbire déjà passé a son numéro barré. Le
// rang vient du moteur (`rang_sbire` / `total_sbires`), jamais d'une déduction.
// Une couche fixe, sans clic, posée sur les cartes comme les flèches.
import { useEffect, useLayoutEffect, useState } from 'react'
import { createPortal } from 'react-dom'
import type { EtapeDeroule } from './deroule-phase'
import { carteDeLaTable, rect } from './FlechesPhase'
import './numeros-sbires.css'

export type NumeroSbire = { carteId: number; rang: number; passe: boolean }

/** Les sbires numérotés de l'étape 2B, vus depuis l'étape affichée. */
export function numerosDesSbires(etapes: readonly EtapeDeroule[], cle: string | undefined): NumeroSbire[] {
  const affichee = etapes.find((e) => e.cle === cle)
  if (!affichee || affichee.temps !== 'sbires') return []
  const parCarte = new Map<number, NumeroSbire>()
  for (const e of etapes) {
    if (e.temps !== 'sbires' || e.carteId === undefined || e.rangSbire === undefined) continue
    if ((e.totalSbires ?? 0) < 2 || parCarte.has(e.carteId)) continue
    parCarte.set(e.carteId, { carteId: e.carteId, rang: e.rangSbire, passe: e.rangSbire < (affichee.rangSbire ?? 0) })
  }
  return [...parCarte.values()]
}

type Pose = NumeroSbire & { x: number; y: number }

export function NumerosSbires({ etapes, cle, actif }: { etapes: readonly EtapeDeroule[]; cle: string | undefined; actif: boolean }) {
  const numeros = actif ? numerosDesSbires(etapes, cle) : []
  const signature = numeros.map((n) => `${n.carteId}:${n.rang}:${n.passe}`).join('|')
  const [poses, setPoses] = useState<Pose[]>([])
  const [tour, setTour] = useState(0)

  useLayoutEffect(() => {
    const mesurer = () => {
      const resultat: Pose[] = []
      for (const n of numeros) {
        const r = rect(carteDeLaTable(n.carteId))
        if (r) resultat.push({ ...n, x: r.x + r.w, y: r.y })
      }
      setPoses(resultat)
    }
    mesurer()
    window.addEventListener('resize', mesurer)
    window.addEventListener('scroll', mesurer, true)
    return () => {
      window.removeEventListener('resize', mesurer)
      window.removeEventListener('scroll', mesurer, true)
    }
    // `numeros` change d'objet a chaque rendu : sa signature suffit.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [signature, tour])

  // La table bouge encore au premier rendu (trajets, recadrage) : deux mesures au repos.
  useEffect(() => {
    if (!signature) return
    const a = window.setTimeout(() => setTour((n) => n + 1), 300)
    const b = window.setTimeout(() => setTour((n) => n + 1), 800)
    return () => {
      window.clearTimeout(a)
      window.clearTimeout(b)
    }
  }, [signature])

  if (poses.length === 0 || typeof document === 'undefined') return null
  return createPortal(
    <div className="numeros-sbires" aria-hidden="true">
      {poses.map((p) => (
        <span
          key={p.carteId}
          className={`numero-sbire${p.passe ? ' est-passe' : ''}`}
          data-card-id={p.carteId}
          style={{ left: `${p.x}px`, top: `${p.y}px` }}
        >
          {p.rang}
        </span>
      ))}
    </div>,
    document.body
  )
}
