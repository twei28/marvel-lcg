// UN CHOIX RESOLU D'OFFICE DOIT SE VOIR.
//
// Signalement BL-Stark n°99 (23/10/2026) : « Dents-de-Sabre Frappe » offre « 1 degat a Robert Kelly OU epuise ton heros pour
// l'empecher ». L'heroine etait en alter ego : la seconde option n'existait pas, la premiere s'est appliquee toute seule, et le joueur a
// cru que la carte n'avait rien fait. Le moteur ecrivait bien « une seule option est possible » au journal, mais personne ne l'ouvre.
// Il publie desormais chaque choix de ce genre (`choix_uniques`) ; ici, une bulle quelques secondes, sur la carte quand elle est encore a
// l'ecran (une traitrise est deja defaussee : la bulle se pose alors en haut de la table).
import { useEffect, useRef, useState } from 'react'
import { createPortal } from 'react-dom'
import { t } from './langue'
import { nomAffiche } from './noms-cartes-fr'
import { traduireMoteur } from './vocabulaire-moteur'
import type { ChoixUnique } from './world'

export const DUREE_BULLE_CHOIX_UNIQUE = 6000

/** « Dents-de-Sabre Frappe : une seule option possible, appliquée d'office : Infliger 1 dégât à Robert Kelly ». */
export function phraseChoixUnique(choix: ChoixUnique, nomCarte?: string): string {
  const carte = nomCarte ?? choix.carte
  // Un avis libre du moteur (« aucun sbire : pas de pioche ») se dit tel quel, traduit, sans « une seule option possible ».
  if (choix.texte) return `${carte} : ${traduireMoteur(choix.texte)}`
  return t('{carte} : une seule option possible, appliquée d’office : {option}')
    .replace('{carte}', carte)
    .replace('{option}', traduireMoteur(choix.option))
}

/** Les choix que le plateau n'a pas encore montrés. */
export function choixNouveaux(liste: ChoixUnique[], dernierVu: number): ChoixUnique[] {
  return liste.filter((c) => c.id > dernierVu)
}

type Bulle = { id: number; texte: string; x: number; y: number }

export function CoucheChoixUniques({ choix }: { choix: ChoixUnique[] | undefined }) {
  // `null` jusqu'au premier rendu : on ne rejoue pas, au chargement ou en rejoignant la table, ceux d'avant notre arrivee.
  const dernierVu = useRef<number | null>(null)
  const minuteurs = useRef<number[]>([])
  const [bulles, setBulles] = useState<Bulle[]>([])

  useEffect(() => {
    const liste = choix ?? []
    const max = liste.reduce((m, c) => Math.max(m, c.id), 0)
    // Une annulation ou un rechargement renumerote depuis plus bas.
    if (dernierVu.current === null || max < dernierVu.current) {
      dernierVu.current = max
      return
    }
    const nouveaux = choixNouveaux(liste, dernierVu.current)
    dernierVu.current = max
    if (nouveaux.length === 0) return
    const ajout = nouveaux.map((c) => {
      const boite = document.querySelector(`[data-card-id="${c.carte_id}"]`)?.getBoundingClientRect()
      return {
        id: c.id,
        texte: phraseChoixUnique(c, nomAffiche({ name: c.carte, card_id: c.carte_code })),
        x: boite ? boite.left + boite.width / 2 : window.innerWidth / 2,
        y: boite ? boite.top + boite.height / 3 : 96,
      }
    })
    setBulles((avant) => [...avant, ...ajout])
    const numeros = new Set(ajout.map((b) => b.id))
    minuteurs.current.push(
      window.setTimeout(() => setBulles((avant) => avant.filter((b) => !numeros.has(b.id))), DUREE_BULLE_CHOIX_UNIQUE)
    )
  }, [choix])

  useEffect(() => () => minuteurs.current.forEach((m) => window.clearTimeout(m)), [])

  if (bulles.length === 0) return null
  return createPortal(
    <div className="couche-refus-effets" aria-live="polite">
      {bulles.map((b) => (
        <div key={b.id} className="bulle-refus-effet bulle-choix-unique" style={{ left: `${b.x}px`, top: `${b.y}px` }} role="status">
          <span className="bulle-refus-effet-icone" aria-hidden="true">
            ⓘ
          </span>
          {b.texte}
        </div>
      ))}
    </div>,
    document.body
  )
}
