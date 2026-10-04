// UN EFFET REFUSÉ DOIT SE VOIR, SUR LA CARTE QUI L'A REFUSÉ.
//
// Signalement Phocéa n°33 (30/09/2026) : Tentacules Agrippants payé en
// physique, « le méchant n'est pas sonné ». Ce n'était pas un bug : Drang
// portait sa Lance, qui le rend Robuste (Stalwart). Le moteur refusait le
// statut sans un mot, et le joueur a cru à une panne. Le moteur publie
// désormais chaque refus (`refus_effets`) ; ici, une bulle sur la carte visée,
// quelques secondes. La ligne de journal, elle, vient du moteur.
import { useEffect, useRef, useState } from 'react'
import { createPortal } from 'react-dom'
import { t } from './langue'
import { libelleDeStatut } from './deroule-textes'
import { nomAffiche } from './noms-cartes-fr'
import type { RefusEffet } from './world'

export const DUREE_BULLE_REFUS = 4500

/** « Pas sonné : Robuste (Lance de Drang) », dans la langue du plateau. */
export function phraseRefusEffet(refus: RefusEffet): string {
  const statut = libelleDeStatut(refus.statut).toLowerCase()
  const source = refus.source ? nomAffiche({ name: refus.source, card_id: refus.source_code }) : ''
  // La source n'apprend rien quand c'est la carte elle-même (Stalwart imprimé).
  const avecSource = (raison: string) =>
    source && refus.source_code !== refus.cible_code ? `${raison} (${source})` : raison
  const raisons: Record<RefusEffet['motif'], () => string> = {
    robuste: () => avecSource(t('Robuste')),
    deja: () => t('déjà {statut}').replace('{statut}', statut),
    immunite: () => avecSource(t('immunisé')),
  }
  return t('Pas {statut} : {raison}').replace('{statut}', statut).replace('{raison}', raisons[refus.motif]())
}

/** Les refus que le plateau n'a pas encore montrés. */
export function refusNouveaux(liste: RefusEffet[], dernierVu: number): RefusEffet[] {
  return liste.filter((r) => r.n > dernierVu)
}

type Bulle = { n: number; texte: string; x: number; y: number }

export function CoucheRefusEffets({ refus }: { refus: RefusEffet[] | undefined }) {
  // `null` jusqu'au premier rendu : on ne rejoue pas, au chargement ou en
  // rejoignant la table, les refus d'avant notre arrivée.
  const dernierVu = useRef<number | null>(null)
  const minuteurs = useRef<number[]>([])
  const [bulles, setBulles] = useState<Bulle[]>([])

  useEffect(() => {
    const liste = refus ?? []
    const max = liste.reduce((m, r) => Math.max(m, r.n), 0)
    // Une annulation ou un rechargement renumérote depuis plus bas.
    if (dernierVu.current === null || max < dernierVu.current) {
      dernierVu.current = max
      return
    }
    const nouveaux = refusNouveaux(liste, dernierVu.current)
    dernierVu.current = max
    if (nouveaux.length === 0) return
    const ajout = nouveaux.map((r) => {
      const boite = document.querySelector(`[data-card-id="${r.cible_id}"]`)?.getBoundingClientRect()
      return {
        n: r.n,
        texte: phraseRefusEffet(r),
        x: boite ? boite.left + boite.width / 2 : window.innerWidth / 2,
        y: boite ? boite.top + boite.height / 3 : 96,
      }
    })
    setBulles((avant) => [...avant, ...ajout])
    const numeros = new Set(ajout.map((b) => b.n))
    minuteurs.current.push(
      window.setTimeout(() => setBulles((avant) => avant.filter((b) => !numeros.has(b.n))), DUREE_BULLE_REFUS)
    )
  }, [refus])

  useEffect(() => () => minuteurs.current.forEach((m) => window.clearTimeout(m)), [])

  if (bulles.length === 0) return null
  return createPortal(
    <div className="couche-refus-effets" aria-live="polite">
      {bulles.map((b) => (
        <div key={b.n} className="bulle-refus-effet" style={{ left: `${b.x}px`, top: `${b.y}px` }} role="status">
          <span className="bulle-refus-effet-icone" aria-hidden="true">
            ⊘
          </span>
          {b.texte}
        </div>
      ))}
    </div>,
    document.body
  )
}
