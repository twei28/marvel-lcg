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
  onToutDerouler,
}: {
  etapes: EtapeDeroule[]
  noms: (id: number) => string
  /** Appele une fois la derniere etape validee. */
  onTerminer: () => void
  /** « Tout derouler » : les etapes restantes defilent sans attendre. */
  onToutDerouler?: () => void
}) {
  const [index, setIndex] = useState(0)

  // Une nouvelle phase repart de sa premiere etape.
  useEffect(() => {
    setIndex(0)
  }, [etapes])

  const etape = etapes[index]

  const avancer = () => {
    // Hors phase du mechant, etapes est vide et il n'y a rien a avancer : une
    // touche pressee ne doit alors rien declencher.
    if (!etape) return
    if (index + 1 >= etapes.length) {
      onTerminer()
      return
    }
    setIndex(index + 1)
  }

  useEffect(() => {
    const auClavier = (evenement: KeyboardEvent) => {
      // On ecrit peut-etre ailleurs : le tchat est a portee de main pendant la
      // phase, et un espace tape dedans ne doit pas la faire avancer.
      const cible = evenement.target
      if (
        cible instanceof HTMLElement &&
        (cible.tagName === 'INPUT' || cible.tagName === 'TEXTAREA' || cible.isContentEditable)
      ) {
        return
      }
      if (evenement.key === 'Enter' || evenement.key === ' ') {
        evenement.preventDefault()
        avancer()
        return
      }
      if (evenement.key === 'Escape' && onToutDerouler) {
        evenement.preventDefault()
        onToutDerouler()
      }
    }
    document.addEventListener('keydown', auClavier)
    return () => document.removeEventListener('keydown', auClavier)
  })

  // Le `return null` vient APRES tous les hooks, jamais avant : React exige
  // le meme nombre de hooks, dans le meme ordre, a chaque rendu. Ce composant
  // est monte des que le mode "detaille" est actif, donc hors phase du
  // mechant avec `etapes` vide, puis se remplit sans etre demonte quand la
  // phase commence. Un `return null` place plus haut sauterait le second
  // useEffect a un rendu et le rajouterait au suivant, ce que React refuse.
  if (!etape) return null

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
