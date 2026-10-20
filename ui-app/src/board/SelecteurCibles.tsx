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
import './selecteur-fenetre.css'

/**
 * LA FENETRE DE CHOIX (rapport n76, Yarro, 10/10/2026). Quand TOUTES les
 * cibles sont hors table (Controle climatique de Storm, une recherche dans le
 * deck...), le selecteur ne cohabite plus avec le panneau central qui le
 * recouvrait : il devient une fenetre, les cartes puis Annuler / Valider.
 */
export type FenetreChoix = {
  choisies: number
  minimum: number
  maximum: number
  valider: () => void
  annuler: () => void
}

/**
 * LE BANDEAU COLLE (fiche du 07/10/2026, « le bouton qui valide se colle au-dessus de la modale, et quand on bouge
 * l'un ou l'autre, les deux bougent »). Quand des cibles sont aussi sur la table, la table doit rester cliquable :
 * pas de fenetre modale. Le panneau d'action (titre, consigne, Annuler, bouton qui valide) ne flotte plus a cote du
 * selecteur : il devient le haut du selecteur, meme largeur, aucun ecart, et une seule poignee deplace l'ensemble.
 */
export type BandeauColle = {
  surtitre: string
  consigne: string
  phrase?: string
  libelleValider: string
  prete: boolean
  valider: () => void
  annuler: () => void
}

export type SelecteurCiblesProps = {
  cibles: CibleHorsTable[]
  /** Titre de l'action en cours, pour savoir ce qu'on choisit. */
  titre: string
  /** Survol d'une carte : la montrer dans l'apercu lateral (comme la table). */
  survoler?: (carte: ScanCardProps | undefined) => void
  /** Present : le selecteur est une fenetre modale avec ses propres boutons. */
  fenetre?: FenetreChoix
  /** Present (et pas de fenetre) : le panneau d'action est colle au-dessus du selecteur, les deux ne font qu'un. */
  bandeau?: BandeauColle
}

export function SelecteurCibles({ cibles, titre, survoler, fenetre, bandeau }: SelecteurCiblesProps) {
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

  const pret = fenetre ? fenetre.choisies >= Math.max(1, fenetre.minimum) : false
  const panneau = (
    <div
      className={`plateau-selecteur${fenetre ? ' est-fenetre' : ''}${bandeau && !fenetre ? ' avec-bandeau' : ''}`}
      role={fenetre ? 'dialog' : 'group'}
      aria-modal={fenetre ? true : undefined}
      aria-label={fenetre ? titre : `${t('Cibles possibles :')} ${titre}`}
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
      {bandeau && !fenetre ? (
        <div className="plateau-selecteur-bandeau">
          <div
            className="plateau-selecteur-bandeau-texte poignee-glisser"
            onPointerDown={gestesGlisser.onPointerDown}
            onPointerMove={gestesGlisser.onPointerMove}
            onPointerUp={gestesGlisser.onPointerUp}
            onPointerCancel={gestesGlisser.onPointerCancel}
          >
            <span className="plateau-eyebrow">{bandeau.surtitre}</span>
            <strong>{bandeau.consigne}</strong>
            {bandeau.phrase ? <span className="plateau-selecteur-compte">{bandeau.phrase}</span> : null}
          </div>
          <div className="plateau-selecteur-boutons">
            <button type="button" className="plateau-selecteur-annuler" onClick={bandeau.annuler}>
              {t('Annuler')}
            </button>
            <button
              type="button"
              className="plateau-selecteur-valider"
              disabled={!bandeau.prete}
              onClick={() => {
                if (bandeau.prete) bandeau.valider()
              }}
            >
              {bandeau.libelleValider}
            </button>
          </div>
        </div>
      ) : null}
      <div
        className="plateau-selecteur-entete poignee-glisser"
        onPointerDown={gestesGlisser.onPointerDown}
        onPointerMove={gestesGlisser.onPointerMove}
        onPointerUp={gestesGlisser.onPointerUp}
        onPointerCancel={gestesGlisser.onPointerCancel}
      >
        {fenetre ? (
          <>
            <strong>{titre}</strong>
            <span className="plateau-selecteur-compte">
              {fenetre.maximum > 1
                ? `${t('Choisis jusqu’à')} ${fenetre.maximum} ${t('cartes')} · ${fenetre.choisies}/${fenetre.maximum}`
                : t('Choisis une carte')}
            </span>
          </>
        ) : (
          <>
            <span className="plateau-eyebrow">{t('Cibles hors table')}</span>
            <strong>
              {titre} · {cibles.length} {cibles.length > 1 ? t('cartes') : t('carte')}
            </strong>
          </>
        )}
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
      {fenetre ? (
        <div className="plateau-selecteur-boutons">
          <button type="button" className="plateau-selecteur-annuler" onClick={fenetre.annuler}>
            {t('Annuler')}
          </button>
          <button
            type="button"
            className="plateau-selecteur-valider"
            disabled={!pret}
            onClick={() => {
              if (pret) fenetre.valider()
            }}
          >
            {t('Valider')}
          </button>
        </div>
      ) : null}
    </div>
  )
  return fenetre ? <div className="plateau-selecteur-voile">{panneau}</div> : panneau
}
