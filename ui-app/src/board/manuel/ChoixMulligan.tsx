// ChoixMulligan.tsx — « Mulligan Hand » d'OCTGN (lot 6 du 06/10/2026) : on
// coche les cartes de la main à changer, puis le moteur les défausse et en
// repioche autant, en UNE commande (`Puzzle.Mulligan`). Patron de
// `ChoixCibleAmelioration.tsx`, mêmes classes, aucune apparence nouvelle.
// Fermer sans confirmer n'envoie rien.
import { useEffect, useState } from 'react'
import { t } from '../langue'

export type CarteDeMain = { id: number; nom: string }

/**
 * Sert aussi à défausser l'excédent de main après F12 (`doEndHeroPhase`
 * d'OCTGN) : autre titre, autre bouton, et pas plus de `maximum` cartes.
 */
export function ChoixMulligan({
  main,
  onConfirmer,
  onFermer,
  titre = t('Mulligan'),
  consigne = t('Quelles cartes changer ?'),
  libelle = t('Changer'),
  maximum,
}: {
  main: CarteDeMain[]
  onConfirmer: (ids: number[]) => void
  onFermer: () => void
  titre?: string
  consigne?: string
  libelle?: string
  maximum?: number
}) {
  const [cochees, setCochees] = useState<ReadonlySet<number>>(new Set())

  useEffect(() => {
    const surEchap = (evenement: KeyboardEvent) => {
      if (evenement.key === 'Escape') onFermer()
    }
    document.addEventListener('keydown', surEchap)
    return () => document.removeEventListener('keydown', surEchap)
  }, [onFermer])

  const basculer = (id: number) =>
    setCochees((avant) => {
      const apres = new Set(avant)
      if (apres.has(id)) apres.delete(id)
      else if (maximum === undefined || apres.size < maximum) apres.add(id)
      return apres
    })

  return (
    <div className="pile-triche-voile" onPointerDown={onFermer}>
      <section
        className="pile-triche choix-reprise"
        role="dialog"
        aria-label={titre}
        onPointerDown={(evenement) => evenement.stopPropagation()}
      >
        <header className="pile-triche-entete">
          <h2>{titre}</h2>
          <button type="button" onClick={onFermer}>
            {t('Annuler')}
          </button>
        </header>
        <p className="choix-reprise-aide">{consigne}</p>
        <ul className="choix-reprise-liste">
          {main.map((carte) => (
            <li key={carte.id}>
              <label>
                <input type="checkbox" checked={cochees.has(carte.id)} onChange={() => basculer(carte.id)} />{' '}
                <strong>{carte.nom}</strong>
              </label>
            </li>
          ))}
        </ul>
        <button
          type="button"
          disabled={cochees.size === 0}
          onClick={() => onConfirmer(main.filter((carte) => cochees.has(carte.id)).map((carte) => carte.id))}
        >
          {`${libelle} ${cochees.size}`}
        </button>
      </section>
    </div>
  )
}
