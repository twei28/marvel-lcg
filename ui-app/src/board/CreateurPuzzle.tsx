// Le CREATEUR de puzzle sur le plateau (24/10/2026) : un petit panneau orange « Création de puzzle » avec « Enregistrer le puzzle ».
//
// Visible seulement quand la table porte la regle `mode_createur_puzzle` (mode « Puzzle » de la preparation). Le clic capture le
// plateau tel qu'il est (`GET /puzzle_capture`), ouvre la fenetre des details (titre, histoire, difficulte, objectifs, indices,
// solution, phase de depart, premier joueur), puis publie sur le site. La logique est dans `createur-puzzle.ts`.
import { useState } from 'react'
import { t } from './langue'
import {
  DETAILS_VIDES,
  MAX_INDICES,
  MAX_OBJECTIFS,
  MAX_PSEUDO,
  assemblerPuzzle,
  capturerLePlateau,
  erreursDesDetails,
  memoriserMonPuzzle,
  publierSurLeSite,
  type Capture,
  type DetailsPuzzle,
  type GenreObjectif,
  type Objectif,
  type Publication,
  type PhaseDeDepart,
} from './createur-puzzle'

const CLE_PSEUDO = 'mc-puzzle-pseudo'

function pseudoMemorise(): string {
  try {
    return window.localStorage.getItem(CLE_PSEUDO) ?? ''
  } catch {
    return ''
  }
}

export type CreateurPuzzleProps = {
  actif: boolean
  /** Les heros de la table (pour choisir le premier joueur). */
  nomsDesJoueurs?: readonly string[]
  capturer?: () => Promise<Capture>
  publier?: (puzzle: Record<string, unknown>, pseudo: string) => Promise<Publication>
}

export function CreateurPuzzle({
  actif,
  nomsDesJoueurs = [],
  capturer = () => capturerLePlateau(),
  publier = (puzzle, pseudo) => publierSurLeSite(puzzle, pseudo),
}: CreateurPuzzleProps) {
  const [capture, setCapture] = useState<Capture | null>(null)
  const [details, setDetails] = useState<DetailsPuzzle>({ ...DETAILS_VIDES, pseudo: pseudoMemorise() })
  const [occupe, setOccupe] = useState(false)
  const [message, setMessage] = useState('')
  const [erreurs, setErreurs] = useState<string[]>([])
  const [resultat, setResultat] = useState<{ code: string; cle: string } | null>(null)
  if (!actif) return null

  const nombreDeJoueurs = Math.max(1, nomsDesJoueurs.length)
  const modifier = (suite: Partial<DetailsPuzzle>) => setDetails((d) => ({ ...d, ...suite }))
  const modifierObjectif = (i: number, suite: Partial<Objectif>) =>
    modifier({ objectifs: details.objectifs.map((o, k) => (k === i ? { ...o, ...suite } : o)) })

  const enregistrer = async () => {
    setMessage('')
    setOccupe(true)
    try {
      setCapture(await capturer())
      setResultat(null)
      setErreurs([])
    } catch (e) {
      setMessage(e instanceof Error ? e.message : String(e))
    } finally {
      setOccupe(false)
    }
  }

  const publierLePuzzle = async () => {
    if (!capture) return
    const trouvees = erreursDesDetails(details, nombreDeJoueurs)
    setErreurs(trouvees)
    if (trouvees.length > 0) return
    setOccupe(true)
    setMessage('')
    try {
      const pseudo = details.pseudo.trim().slice(0, MAX_PSEUDO)
      try {
        window.localStorage.setItem(CLE_PSEUDO, pseudo)
      } catch {
        /* le pseudo ne sera simplement pas retenu */
      }
      const pub = await publier(assemblerPuzzle(capture.puzzle, details), pseudo)
      memoriserMonPuzzle({ code: pub.code, cle: pub.cle, titre: details.titre.trim(), expire_le: pub.expire_le })
      setResultat({ code: pub.code, cle: pub.cle })
    } catch (e) {
      setMessage(e instanceof Error ? e.message : String(e))
    } finally {
      setOccupe(false)
    }
  }

  const fermer = () => {
    setCapture(null)
    setResultat(null)
    setMessage('')
    setErreurs([])
  }

  return (
    <>
      <aside className="createur-puzzle" aria-label={t('Création de puzzle')}>
        <strong>{t('Création de puzzle')}</strong>
        <button type="button" onClick={enregistrer} disabled={occupe}>
          {t('Enregistrer le puzzle')}
        </button>
        {message && !capture ? (
          <p className="createur-puzzle-erreur" role="alert">
            {t(message)}
          </p>
        ) : null}
      </aside>
      {capture ? (
        <div className="enonce-fond" role="dialog" aria-modal="true" aria-label={t('Enregistrer le puzzle')}>
          <div className="enonce-boite createur-puzzle-boite">
            {resultat ? (
              <>
                <h2>{t('Puzzle publié')}</h2>
                <p>{t('Donne ce code à ceux qui doivent le résoudre :')}</p>
                <p className="createur-puzzle-code">{resultat.code}</p>
                <p>{t('Ta clé d’édition (garde-la, elle ne sera plus montrée) :')}</p>
                <p className="createur-puzzle-code">{resultat.cle}</p>
                <button type="button" className="enonce-commencer" onClick={fermer}>
                  {t('Fermer')}
                </button>
              </>
            ) : (
              <>
                <h2>{t('Enregistrer le puzzle')}</h2>
                <label className="createur-puzzle-champ">
                  {t('Titre')}
                  <input value={details.titre} maxLength={80} onChange={(e) => modifier({ titre: e.target.value })} />
                </label>
                <label className="createur-puzzle-champ">
                  {t('Histoire')}
                  <textarea rows={3} value={details.histoire} onChange={(e) => modifier({ histoire: e.target.value })} />
                </label>
                <label className="createur-puzzle-champ">
                  {t('Difficulté')}
                  <select value={details.difficulte} onChange={(e) => modifier({ difficulte: Number(e.target.value) })}>
                    <option value={0}>{t('Non précisée')}</option>
                    {[1, 2, 3, 4, 5].map((n) => (
                      <option key={n} value={n}>
                        {'★'.repeat(n)}
                      </option>
                    ))}
                  </select>
                </label>
                <h3>{t('Objectifs')}</h3>
                {details.objectifs.map((o, i) => (
                  <div key={i} className="createur-puzzle-ligne">
                    <select
                      aria-label={t('Genre d’objectif')}
                      value={o.kind}
                      onChange={(e) => modifierObjectif(i, { kind: e.target.value as GenreObjectif })}
                    >
                      <option value="defeat_villain">{t('Vaincre le méchant')}</option>
                      <option value="survive">{t('Survivre jusqu’à la fin du round')}</option>
                      <option value="complete_scheme">{t('Terminer une manigance')}</option>
                      <option value="free_text">{t('Objectif libre')}</option>
                    </select>
                    {o.kind === 'complete_scheme' ? (
                      <input
                        aria-label={t('Identifiant du complot visé')}
                        placeholder={t('Identifiant du complot visé')}
                        value={o.target}
                        onChange={(e) => modifierObjectif(i, { target: e.target.value })}
                      />
                    ) : null}
                    {o.kind === 'free_text' ? (
                      <input
                        aria-label={t('Texte de l’objectif')}
                        placeholder={t('Texte de l’objectif')}
                        value={o.text}
                        onChange={(e) => modifierObjectif(i, { text: e.target.value })}
                      />
                    ) : null}
                    <button type="button" aria-label={t('Retirer')} onClick={() => modifier({ objectifs: details.objectifs.filter((_, k) => k !== i) })}>
                      ✕
                    </button>
                  </div>
                ))}
                {details.objectifs.length < MAX_OBJECTIFS ? (
                  <button type="button" onClick={() => modifier({ objectifs: [...details.objectifs, { kind: 'defeat_villain', target: '', text: '' }] })}>
                    {t('Ajouter un objectif')}
                  </button>
                ) : null}
                {details.objectifs.length > 1 ? (
                  <label className="createur-puzzle-champ">
                    {t('Pour réussir')}
                    <select value={details.modeObjectifs} onChange={(e) => modifier({ modeObjectifs: e.target.value as 'all' | 'any' })}>
                      <option value="all">{t('Tous les objectifs')}</option>
                      <option value="any">{t('Un seul objectif')}</option>
                    </select>
                  </label>
                ) : null}
                <h3>{t('Indices')}</h3>
                {details.indices.map((indice, i) => (
                  <div key={i} className="createur-puzzle-ligne">
                    <input
                      aria-label={`${t('Indice')} ${i + 1}`}
                      value={indice}
                      onChange={(e) => modifier({ indices: details.indices.map((x, k) => (k === i ? e.target.value : x)) })}
                    />
                    <button type="button" aria-label={t('Retirer')} onClick={() => modifier({ indices: details.indices.filter((_, k) => k !== i) })}>
                      ✕
                    </button>
                  </div>
                ))}
                {details.indices.length < MAX_INDICES ? (
                  <button type="button" onClick={() => modifier({ indices: [...details.indices, ''] })}>
                    {t('Ajouter un indice')}
                  </button>
                ) : null}
                <h3>{t('Départ')}</h3>
                <label className="createur-puzzle-champ">
                  {t('Phase de départ')}
                  <select value={details.phaseDeDepart} onChange={(e) => modifier({ phaseDeDepart: e.target.value as PhaseDeDepart })}>
                    <option value="">{t('Début de la phase des joueurs')}</option>
                    <option value="villain">{t('Phase du méchant')}</option>
                    <option value="end_round">{t('Fin du round')}</option>
                  </select>
                </label>
                {nomsDesJoueurs.length > 1 ? (
                  <label className="createur-puzzle-champ">
                    {t('Premier joueur')}
                    <select value={details.premierJoueur} onChange={(e) => modifier({ premierJoueur: Number(e.target.value) })}>
                      {nomsDesJoueurs.map((nom, i) => (
                        <option key={i} value={i}>
                          {nom}
                        </option>
                      ))}
                    </select>
                  </label>
                ) : null}
                <h3>{t('Solution (facultative)')}</h3>
                <label className="createur-puzzle-champ">
                  {t('Solution de référence')}
                  <textarea rows={3} value={details.solution} onChange={(e) => modifier({ solution: e.target.value })} />
                </label>
                <label className="createur-puzzle-champ">
                  {t('Visible pour le joueur')}
                  <select
                    value={details.visibiliteSolution}
                    onChange={(e) => modifier({ visibiliteSolution: e.target.value as 'after' | 'always' | 'never' })}
                  >
                    <option value="after">{t('Une fois la partie finie')}</option>
                    <option value="always">{t('Toujours')}</option>
                    <option value="never">{t('Jamais')}</option>
                  </select>
                </label>
                <label className="createur-puzzle-champ">
                  {t('Ton pseudo (affiché avec le puzzle)')}
                  <input value={details.pseudo} maxLength={MAX_PSEUDO} placeholder={t('Anonyme')} onChange={(e) => modifier({ pseudo: e.target.value })} />
                </label>
                {capture.avertissements.length > 0 ? (
                  <div className="createur-puzzle-avertissements">
                    <strong>{t('Ce que la capture n’a pas pu garder :')}</strong>
                    <ul>
                      {capture.avertissements.map((a, i) => (
                        <li key={i}>{a}</li>
                      ))}
                    </ul>
                  </div>
                ) : null}
                {erreurs.length > 0 ? (
                  <ul className="createur-puzzle-erreur" role="alert">
                    {erreurs.map((e, i) => (
                      <li key={i}>{t(e)}</li>
                    ))}
                  </ul>
                ) : null}
                {message ? (
                  <p className="createur-puzzle-erreur" role="alert">
                    {t(message)}
                  </p>
                ) : null}
                <div className="panneau-enonce-actions">
                  <button type="button" className="enonce-commencer" onClick={publierLePuzzle} disabled={occupe}>
                    {t('Publier le puzzle')}
                  </button>
                  <button type="button" onClick={fermer}>
                    {t('Annuler')}
                  </button>
                </div>
              </>
            )}
          </div>
        </div>
      ) : null}
    </>
  )
}
