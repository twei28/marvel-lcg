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
import { useGlisserPanneau } from './placement/useGlisserPanneau'

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
  // Deplacement volontaire, a la poignee -- meme mecanisme que
  // `DemandeCentrale`/`AssistantAction` (demande de l'utilisateur, 28/09/2026,
  // « toutes les fenetres, tous les panneaux » -- c'est CE panneau, precisement,
  // qui restait cache sous `AssistantAction` sans aucun moyen de l'ecarter).
  // Les hooks se declarent AVANT le retour anticipe ci-dessous.
  const { decalage, gestes: gestesGlisser } = useGlisserPanneau(`${titre}|${cibles.length}`)

  if (cibles.length === 0) return null

  return (
    <div
      className="plateau-selecteur"
      role="group"
      aria-label={`${t('Cibles possibles :')} ${titre}`}
      // ⚠ `.plateau-selecteur` centre DEJA avec `transform: translate(-50%,
      // -50%)` en CSS (board.css) : un `transformDecalage` naif ECRASERAIT ce
      // centrage au lieu de s'y ajouter. On compose les deux dans le MEME
      // `translate()`, seul cas du chantier ou le panneau se centre par son
      // PROPRE transform plutot que par celui d'un parent.
      style={
        decalage.dx !== 0 || decalage.dy !== 0
          ? { transform: `translate(calc(-50% + ${decalage.dx}px), calc(-50% + ${decalage.dy}px))` }
          : undefined
      }
      onMouseOver={survol}
      onMouseLeave={quitter}
    >
      <div
        className="plateau-selecteur-entete poignee-glisser"
        onPointerDown={gestesGlisser.onPointerDown}
        onPointerMove={gestesGlisser.onPointerMove}
        onPointerUp={gestesGlisser.onPointerUp}
        onPointerCancel={gestesGlisser.onPointerCancel}
      >
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
              orderNumber={cible.ordre}
              onOrdreReculer={cible.ordreReculer}
              onOrdreAvancer={cible.ordreAvancer}
              onAssignerReste={cible.assignerReste}
              assignerResteQuantite={cible.assignerResteQuantite}
            />
          </span>
        ))}
      </div>
    </div>
  )
}
