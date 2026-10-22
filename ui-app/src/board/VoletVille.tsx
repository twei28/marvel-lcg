/**
 * L'onglet « VILLE » (campagne MC×DC 2026 « La ville ne dort jamais »), tire depuis le bord droit comme le Journal et l'Aide.
 *
 * Decisions de l'utilisateur du 22/10/2026 (.planning/mcdc-punisher/decisions-interface-ville.md) :
 *   1. le panneau s'ouvre PAR-DESSUS la table, comme un tiroir ;
 *   2. ferme, l'onglet montre une MINI-CARTE 3×3 (cases, pions) ;
 *   3. ouvert, la carte montre toutes les rangees, la mienne en surbrillance ; un clic sur le pion d'un coequipier affiche sa rangee en lecture seule ;
 *   4. se deplacer : un clic sur une case verte, puis le choix du cout (epuiser / 1 ressource) que pose le moteur ; l'Action de la carte The City reste ;
 *   5. le survol d'une case montre la carte agrandie, A GAUCHE du volet (jamais sur la zone de jeu), centree verticalement ;
 *   6. chaque case montre les pions, la pastille de sbire attache, les compteurs de piste et « capacite deja utilisee ce round ».
 */
import { useEffect, useMemo, useState } from 'react'
import { createPortal } from 'react-dom'
import { ScanCard, type ScanCardProps } from '../components/ScanCard'
import type { Option } from './ask'
import type { Catalogue } from './catalogue'
import { toScanCard } from './card-model'
import { t } from './langue'
import {
  casesAtteignables,
  casesDeLaLigne,
  lignesOrdonnees,
  positionDuJoueur,
  resumeCompteurs,
} from './ville-etat'
import type { VilleCase, VilleExport } from './world'
import './VoletVille.css'

const COULEURS_PIONS = ['#f3c623', '#e8ecf3', '#4fb0ff', '#e07bd0']
export const couleurDuPion = (playerId: number): string => COULEURS_PIONS[playerId % COULEURS_PIONS.length]!

/** Une carte du jeu montree par son seul identifiant (le lieu, le CAPO) : jamais une carte du monde, donc identifiant negatif. */
function carteParId(cardId: string, playerId: number, catalogue: Catalogue, type: string): ScanCardProps {
  return toScanCard(
    {
      id: -Math.abs(cardId.split('').reduce((somme, c) => somme * 31 + c.charCodeAt(0), 7)),
      is_ready: true,
      is_face_up: true,
      visible_for_players: [playerId],
      bind_object_id: 0,
      name: cardId,
      info: {},
      traits: {},
      buffs: {},
      card_id: cardId,
      pic_id: cardId,
      down_card_ids: [],
      card_type: catalogue.type(cardId) ?? type,
      cost: 0,
      resources: [],
    },
    { playerId, actives: new Set(), catalogue }
  )
}

export function VoletVille({
  ville,
  moi,
  nomsJoueurs,
  optionDeplacement,
  seDeplacer,
  catalogue,
  ouvert,
  ouvrir,
  fermer,
}: {
  ville: VilleExport
  /** Le siege de ce joueur (`playerId`). */
  moi: number
  nomsJoueurs: Readonly<Record<number, string>>
  /** L'option « Move » du moteur quand elle est offerte, sinon `undefined` (les cases ne sont alors pas cliquables). */
  optionDeplacement: Option | undefined
  /** Choisit « Move » avec cette carte de lieu pour cible ; le moteur pose ensuite la question du cout. */
  seDeplacer: (option: Option, objetLieu: number) => void
  catalogue: Catalogue
  ouvert: boolean
  ouvrir: () => void
  fermer: () => void
}) {
  // La rangee regardee : la mienne, ou celle d'un coequipier dont on a clique le pion (lecture seule).
  const [regardeJoueur, setRegardeJoueur] = useState<number | undefined>(undefined)
  const [survol, setSurvol] = useState<string | undefined>(undefined)

  useEffect(() => {
    if (!ouvert) {
      setRegardeJoueur(undefined)
      setSurvol(undefined)
      return
    }
    const surTouche = (e: KeyboardEvent) => {
      if (e.key === 'Escape') fermer()
    }
    document.addEventListener('keydown', surTouche)
    return () => document.removeEventListener('keydown', surTouche)
  }, [ouvert, fermer])

  const maPosition = positionDuJoueur(ville, moi)
  const atteignables = useMemo(() => new Set(casesAtteignables(ville, optionDeplacement).map((c) => c.objet)), [ville, optionDeplacement])
  const lignes = lignesOrdonnees(ville)
  const ligneRegardee = regardeJoueur !== undefined ? positionDuJoueur(ville, regardeJoueur)?.ligne : maPosition?.ligne

  const pions = (c: VilleCase) =>
    c.joueurs.map((pid) => (
      <button
        key={pid}
        type="button"
        className={`ville-pion${pid === moi ? ' est-moi' : ''}`}
        style={{ background: couleurDuPion(pid) }}
        title={nomsJoueurs[pid] ?? `${t('Joueur')} ${pid + 1}`}
        aria-label={nomsJoueurs[pid] ?? `${t('Joueur')} ${pid + 1}`}
        onClick={(e) => {
          e.stopPropagation()
          if (pid !== moi) setRegardeJoueur(pid)
          else setRegardeJoueur(undefined)
        }}
      >
        {(nomsJoueurs[pid] ?? `${pid + 1}`).slice(0, 1).toUpperCase()}
      </button>
    ))

  const carteSurvolee = survol ? carteParId(survol, moi, catalogue, 'Environment') : undefined

  return (
    <>
      <button
        type="button"
        className={`volet-ville-languette${ouvert ? ' est-ouvert' : ''}`}
        aria-expanded={ouvert}
        aria-controls="volet-ville"
        title={ouvert ? t('Refermer la ville') : t('Ouvrir la ville')}
        aria-label={ouvert ? t('Refermer la ville') : t('Ouvrir la ville')}
        onClick={() => (ouvert ? fermer() : ouvrir())}
      >
        <span className="volet-ville-languette-texte">{t('Ville')}</span>
        {/* La mini-carte de l'onglet ferme : neuf cases, un point par joueur, ma case cerclee. */}
        <span className="ville-mini" aria-hidden="true">
          {lignes.map((l) =>
            casesDeLaLigne(ville, l.ligne).map((c) => (
              <span
                key={`${c.ligne}-${c.colonne}`}
                className={`ville-mini-case${maPosition && c.ligne === maPosition.ligne && c.colonne === maPosition.colonne ? ' est-ici' : ''}${
                  atteignables.has(c.objet) ? ' est-atteignable' : ''
                }`}
              >
                {c.joueurs.slice(0, 2).map((pid) => (
                  <i key={pid} style={{ background: couleurDuPion(pid) }} />
                ))}
              </span>
            ))
          )}
        </span>
      </button>
      {ouvert ? (
        <>
          <aside id="volet-ville" className="volet-ville" role="dialog" aria-label={t('Ville')}>
            <header className="volet-ville-tete">
              <h2>{t('La ville')}</h2>
              <button type="button" className="reglages-fermer" onClick={fermer} title={t('Fermer')}>
                ×
              </button>
            </header>
            <p className="volet-ville-aide">
              {regardeJoueur !== undefined
                ? `${t('Vous regardez la rangée de')} ${nomsJoueurs[regardeJoueur] ?? ''}. ${t('Cliquez votre pion pour revenir à la vôtre.')}`
                : optionDeplacement
                  ? t('Cliquez une case verte pour vous y déplacer.')
                  : t('Vous pourrez vous déplacer à votre tour.')}
            </p>
            <div className="ville-grille" onMouseLeave={() => setSurvol(undefined)}>
              {lignes.map((l) => (
                <div key={l.ligne} className={`ville-rangee${l.ligne === ligneRegardee ? ' est-regardee' : ''}`}>
                  <div className="ville-capo" onMouseEnter={() => l.capo_card_id && setSurvol(l.capo_card_id)}>
                    {l.capo_card_id ? (
                      <ScanCard {...carteParId(l.capo_card_id, moi, catalogue, 'Villain')} state="ready" highlight={false} masquerType />
                    ) : null}
                  </div>
                  {casesDeLaLigne(ville, l.ligne).map((c) => {
                    const atteignable = regardeJoueur === undefined && atteignables.has(c.objet) && optionDeplacement !== undefined
                    const ici = maPosition?.ligne === c.ligne && maPosition?.colonne === c.colonne
                    const compteurs = resumeCompteurs(c.piste?.compteurs)
                    return (
                      <div
                        key={c.colonne}
                        className={`ville-case${ici ? ' est-ici' : ''}${atteignable ? ' est-atteignable' : ''}`}
                        role={atteignable ? 'button' : undefined}
                        tabIndex={atteignable ? 0 : undefined}
                        aria-label={atteignable ? `${t('Se déplacer')} (${c.ligne + 1}, ${c.colonne + 1})` : undefined}
                        onMouseEnter={() => setSurvol(c.card_id)}
                        onFocus={() => setSurvol(c.card_id)}
                        onClick={() => {
                          if (atteignable && optionDeplacement) seDeplacer(optionDeplacement, c.objet)
                        }}
                        onKeyDown={(e) => {
                          if (atteignable && optionDeplacement && (e.key === 'Enter' || e.key === ' ')) {
                            e.preventDefault()
                            seDeplacer(optionDeplacement, c.objet)
                          }
                        }}
                      >
                        <ScanCard {...carteParId(c.card_id, moi, catalogue, 'Environment')} state="ready" highlight={false} masquerType />
                        <span className="ville-pions">{pions(c)}</span>
                        {c.sbires_attaches.length > 0 ? (
                          <span className="ville-badge est-sbire" title={t('Sbire attaché à ce lieu')}>
                            {c.sbires_attaches.length}
                          </span>
                        ) : null}
                        {compteurs ? (
                          <span className="ville-badge est-piste" title={t('Compteurs de la piste posée ici')}>
                            {t('Piste')} {compteurs}
                          </span>
                        ) : null}
                        {c.limite_utilisee ? (
                          <span className="ville-badge est-utilise" title={t('Capacité de ce lieu déjà utilisée ce round')}>
                            {t('Utilisé')}
                          </span>
                        ) : null}
                      </div>
                    )
                  })}
                </div>
              ))}
            </div>
          </aside>
          {carteSurvolee
            ? createPortal(
                <div className="ville-apercu" aria-hidden="true">
                  <ScanCard {...carteSurvolee} state="ready" highlight={false} masquerType />
                </div>,
                document.body
              )
            : null}
        </>
      ) : null}
    </>
  )
}
