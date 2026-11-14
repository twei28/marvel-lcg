// Le selecteur de cibles hors table.
//
// Certaines capacites ciblent des cartes que la table ne montre pas : une
// recherche dans le deck, une pioche mise de cote, la defausse. La table n'en
// dessine que le dessus, avec un compteur ; il faut donc un endroit pour voir et
// designer ces cartes-la.
//
// C'est le seul panneau qui se pose par-dessus la table, et seulement le temps
// d'un choix. L'ancien plateau fait la meme chose en « ouvrant » le deck.

import { Fragment, useEffect } from 'react'
import { ScanCard, type ScanCardProps } from '../components/ScanCard'
import { useApercuSurvol } from './apercu-survol'
import type { CibleHorsTable } from './interaction'
import { t } from './langue'
import { useGlisserPanneau } from './placement/useGlisserPanneau'
import './selecteur-fenetre.css'
import { useOrdreGlisser } from './ordre-glisser'
import './ordre-glisser.css'

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
  /**
   * Present : la fenetre peut etre FERMEE SANS ANNULER l'action (croix, Echap, toucher le voile). L'action reste en attente ;
   * `board.tsx` fait clignoter l'onglet « Piles » et propose de rouvrir (demande du 26/10/2026, telephone).
   */
  reduire?: () => void
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
  /**
   * Present : l'intitule de la pile d'ou vient chaque carte (id -> « Deck », « Défausse »...). Un intitule s'insere devant
   * chaque groupe de cartes qui se suivent (rapport du 26/10/2026, Suit Up : une recherche dans le deck ET la defausse).
   */
  groupes?: ReadonlyMap<number, string>
}

export function SelecteurCibles({ cibles, titre, survoler, fenetre, bandeau, groupes }: SelecteurCiblesProps) {
  // Survol ecoute sur le CONTENEUR, agrandissement DERIVE de `cibles` : la
  // regle commune, expliquee dans `apercu-survol.ts`. Ici l'agrandissement
  // n'est pas monte par ce panneau mais remonte a la table (`survoler`), d'ou
  // l'effet qui repercute `regardee` a chaque changement.
  const { regardee, survol, quitter, viser } = useApercuSurvol(cibles, (cible) => cible.props.id)
  const remonter = survoler
  const glisserOrdre = useOrdreGlisser()
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

  // Echap ferme la fenetre SANS annuler (et seulement quand elle sait se reduire).
  const reduire = fenetre?.reduire
  useEffect(() => {
    if (!reduire) return
    const surTouche = (evenement: KeyboardEvent) => {
      if (evenement.key === 'Escape') reduire()
    }
    document.addEventListener('keydown', surTouche)
    return () => document.removeEventListener('keydown', surTouche)
  }, [reduire])

  if (cibles.length === 0) return null

  const carteDe = (cible: CibleHorsTable) => (
    <span
      key={cible.props.id}
      {...glisserOrdre(cible.props.id, cible.permuterAvec, 'plateau-selecteur-carte')}
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
  )

  // DEUX PILES OU PLUS (Suit Up : deck + defausse) : UNE fenetre, une COLONNE par pile (Deck a gauche, Defausse a droite),
  // chacune avec son en-tete et son nombre de cartes. Un seul compteur, un seul Annuler / Valider (demande du 26/10/2026).
  // Sur telephone, les colonnes s'empilent en sections a en-tete collant (selecteur-fenetre.css).
  const colonnes: { libelle: string; cartes: CibleHorsTable[] }[] = []
  if (groupes) {
    for (const cible of cibles) {
      const libelle = groupes.get(Number(cible.props.id))
      if (libelle === undefined) continue
      const existante = colonnes.find((colonne) => colonne.libelle === libelle)
      if (existante) existante.cartes.push(cible)
      else colonnes.push({ libelle, cartes: [cible] })
    }
  }
  const enColonnes = colonnes.length > 1 && colonnes.reduce((n, colonne) => n + colonne.cartes.length, 0) === cibles.length

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
      {fenetre?.reduire ? (
        // La croix FLOTTE en haut a droite et reste visible quand on defile la liste (demande du 26/10/2026).
        <div className="plateau-selecteur-fermer-colle">
          <button
            type="button"
            className="plateau-selecteur-fermer"
            aria-label={t('Fermer (le choix reste en attente)')}
            title={t('Fermer (le choix reste en attente)')}
            // Un bouton de la poignee : ne pas amorcer un deplacement de la fenetre.
            onPointerDown={(evenement) => evenement.stopPropagation()}
            onClick={fenetre.reduire}
          >
            ×
          </button>
        </div>
      ) : null}
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
      {enColonnes ? (
        <div className="plateau-selecteur-colonnes">
          {colonnes.map((colonne) => (
            <section key={colonne.libelle} className="plateau-selecteur-colonne" aria-label={colonne.libelle}>
              <header className="plateau-selecteur-colonne-entete">
                <h3 className="plateau-selecteur-groupe">{colonne.libelle}</h3>
                <span className="plateau-selecteur-colonne-compte">
                  {colonne.cartes.length} {colonne.cartes.length > 1 ? t('cartes') : t('carte')}
                </span>
              </header>
              <div className="plateau-selecteur-cartes">{colonne.cartes.map(carteDe)}</div>
            </section>
          ))}
        </div>
      ) : (
        <div className="plateau-selecteur-cartes">
          {cibles.map((cible, rang) => {
            const groupe = groupes?.get(Number(cible.props.id))
            const groupeAvant = rang > 0 ? groupes?.get(Number(cibles[rang - 1].props.id)) : undefined
            return (
              <Fragment key={cible.props.id}>
                {groupe !== undefined && (rang === 0 || groupe !== groupeAvant) ? (
                  <h3 className="plateau-selecteur-groupe">{groupe}</h3>
                ) : null}
                {carteDe(cible)}
              </Fragment>
            )
          })}
        </div>
      )}
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
  return fenetre ? (
    <div
      className="plateau-selecteur-voile"
      // Toucher le VOILE (hors de la fenetre) la reduit sans annuler : on ne perd plus l'action par un tap maladroit.
      onPointerDown={(evenement) => {
        if (evenement.target === evenement.currentTarget) fenetre.reduire?.()
      }}
    >
      {panneau}
    </div>
  ) : (
    panneau
  )
}
