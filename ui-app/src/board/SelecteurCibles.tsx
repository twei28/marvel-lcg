// Le selecteur de cibles hors table.
//
// Certaines capacites ciblent des cartes que la table ne montre pas : une
// recherche dans le deck, une pioche mise de cote, la defausse. La table n'en
// dessine que le dessus, avec un compteur ; il faut donc un endroit pour voir et
// designer ces cartes-la.
//
// C'est le seul panneau qui se pose par-dessus la table, et seulement le temps
// d'un choix. L'ancien plateau fait la meme chose en « ouvrant » le deck.

import { useEffect } from 'react'
import { ScanCard, type ScanCardProps } from '../components/ScanCard'
import { useApercuSurvol } from './apercu-survol'
import type { CibleHorsTable } from './interaction'
import { t } from './langue'

export type SelecteurCiblesProps = {
  cibles: CibleHorsTable[]
  /** Titre de l'action en cours, pour savoir ce qu'on choisit. */
  titre: string
  /** Survol d'une carte : la montrer dans l'apercu lateral (comme la table). */
  survoler?: (carte: ScanCardProps | undefined) => void
}

export function SelecteurCibles({ cibles, titre, survoler }: SelecteurCiblesProps) {
  // Survol ecoute sur le CONTENEUR, agrandissement DERIVE de `cibles` : la
  // regle commune, expliquee dans `apercu-survol.ts`. Ici l'agrandissement
  // n'est pas monte par ce panneau mais remonte a la table (`survoler`), d'ou
  // l'effet qui repercute `regardee` a chaque changement.
  const { regardee, survol, quitter, viser } = useApercuSurvol(cibles, (cible) => cible.props.id)
  const remonter = survoler
  useEffect(() => {
    remonter?.(regardee?.props)
  }, [regardee, remonter])
  // Le panneau ferme emporte l'agrandissement : sans cela le dernier survol
  // resterait affiche par-dessus la table apres le choix.
  useEffect(() => () => remonter?.(undefined), [remonter])

  if (cibles.length === 0) return null

  return (
    <div
      className="plateau-selecteur"
      role="group"
      aria-label={`${t('Cibles possibles :')} ${titre}`}
      onMouseOver={survol}
      onMouseLeave={quitter}
    >
      <div className="plateau-selecteur-entete">
        <span className="plateau-eyebrow">{t('Cibles hors table')}</span>
        <strong>
          {titre} · {cibles.length} {cibles.length > 1 ? t('cartes') : t('carte')}
        </strong>
      </div>
      <div className="plateau-selecteur-cartes">
        {cibles.map((cible) => (
          <span
            key={cible.props.id}
            className="plateau-selecteur-carte"
            // Le clavier n'a pas de pointeur : il vise explicitement.
            onFocus={() => viser(cible.props.id)}
            onBlur={() => viser(undefined)}
          >
            <ScanCard
              {...cible.props}
              state={cible.choisie ? 'selected' : 'targetable'}
              onSelect={cible.agir}
              spentCount={cible.fois}
            />
          </span>
        ))}
      </div>
    </div>
  )
}
