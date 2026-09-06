// Le cartouche du deroule detaille : une etape a la fois.
//
// FIXE en bas au centre, il ne bouge jamais d'une etape a l'autre : l'oeil sait
// ou lire et la main ou cliquer des le deuxieme tour. Un cartouche colle a la
// carte concernee aurait deplace le bouton a chaque clic.
//
// « Precedent » RELIT, il ne rejoue rien : le monde du moteur ne recule pas.
// C'est « Annuler la derniere action » qui fait cela, et il reste disponible.

import { useEffect, useState } from 'react'
import type { EtapeDeroule, TempsPhase } from './deroule-phase'
import { regleEtape, titreEtape } from './deroule-textes'
import { t } from './langue'

/** Les quatre temps de la carte de reference, dans l'ordre. */
const TEMPS: { cle: TempsPhase; libelle: string }[] = [
  { cle: 'menace', libelle: 'Menace' },
  { cle: 'activations', libelle: 'Activations' },
  { cle: 'distribution', libelle: 'Distribution' },
  { cle: 'revelation', libelle: 'Révélation' },
]

export function DeroulePhase({
  etapes,
  noms,
  onTerminer,
}: {
  etapes: EtapeDeroule[]
  noms: (id: number) => string
  /** Appele une fois la derniere etape validee. */
  onTerminer: () => void
}) {
  const [index, setIndex] = useState(0)

  // Une nouvelle phase repart de sa premiere etape.
  useEffect(() => {
    setIndex(0)
  }, [etapes])

  const etape = etapes[index]
  if (!etape) return null

  const avancer = () => {
    if (index + 1 >= etapes.length) {
      onTerminer()
      return
    }
    setIndex(index + 1)
  }

  return (
    <section className="deroule-phase" role="dialog" aria-label={t('Phase du méchant')}>
      <ol className="deroule-temps">
        {TEMPS.map((temps) => (
          <li key={temps.cle} className={temps.cle === etape.temps ? 'est-courant' : ''}>
            {t(temps.libelle)}
          </li>
        ))}
      </ol>

      <p className="deroule-titre">{titreEtape(etape, noms)}</p>
      <p className="deroule-regle">{regleEtape(etape)}</p>
      {etape.brut ? <p className="deroule-brut">{etape.brut}</p> : null}

      <div className="deroule-boutons">
        {index > 0 ? (
          <button type="button" className="bh-bouton" onClick={() => setIndex(index - 1)}>
            {t('Précédent')}
          </button>
        ) : null}
        <button type="button" className="bh-bouton deroule-suivant" onClick={avancer}>
          {t('Suivant')}
        </button>
      </div>
    </section>
  )
}
