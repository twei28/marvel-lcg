// L'ENONCE d'un puzzle (E8, 23/10/2026) : l'ecran d'introduction (titre, histoire, difficulte, objectifs), puis un panneau
// repliable en haut a droite avec l'histoire, les indices devoiles UN PAR UN, et « Recommencer » (meme puzzle, meme depart).
// En ORANGE, comme les autres panneaux de puzzle. Vide hors puzzle de format 2 : le moteur n'envoie alors aucun enonce.
// Les deux memoires (introduction deja vue, indices devoiles) vivent dans `sessionStorage`, par puzzle : un rechargement de la
// page, ou « Recommencer », ne renvoie ni l'introduction ni les indices deja lus.
import { useState } from 'react'
import { t } from './langue'
import { libelleObjectif, type ObjectifPuzzle } from './PanneauObjectifs'

export type EnoncePuzzle = {
  title?: string
  description?: string
  difficulty?: number
  hints?: string[]
  author?: string
  /** Solution de reference ecrite par le createur (vide si aucune) et QUAND on peut la voir : after (partie finie), always, never. */
  solution_text?: string
  solution_visibility?: string
}

const CLE_PUZZLE_COURANT = 'mc-puzzle-courant'

function signature(info: EnoncePuzzle): string {
  return `${info.title ?? ''}|${info.description ?? ''}`
}

function lire(cle: string): string | null {
  try {
    return window.sessionStorage.getItem(cle)
  } catch {
    return null
  }
}

function ecrire(cle: string, valeur: string): void {
  try {
    window.sessionStorage.setItem(cle, valeur)
  } catch {
    /* le stockage peut etre bloque : l'ecran marche sans */
  }
}

/** Relance le puzzle courant : le meme fichier, renvoye au moteur, puis la page se recharge. Rend faux si on ne le retrouve pas. */
export async function recommencerPuzzle(): Promise<boolean> {
  let puzzle: string | null = null
  try {
    puzzle = window.localStorage.getItem(CLE_PUZZLE_COURANT)
  } catch {
    puzzle = null
  }
  if (!puzzle) return false
  const reponse = await fetch('/new_puzzle', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: puzzle })
  if (!reponse.ok) return false
  window.location.reload()
  return true
}

export function PanneauEnonce({
  info,
  objectifs,
  recommencer = recommencerPuzzle,
  termine = false,
}: {
  info?: EnoncePuzzle
  objectifs?: readonly ObjectifPuzzle[]
  recommencer?: () => unknown
  /** La partie est finie (gagnee ou perdue) : la solution « after » devient visible. */
  termine?: boolean
}) {
  const sig = info ? signature(info) : ''
  const [intro, setIntro] = useState(() => lire(`mc-enonce-vu:${sig}`) !== '1')
  const [ouvert, setOuvert] = useState(false)
  const [indices, setIndices] = useState(() => Math.max(0, Number(lire(`mc-enonce-indices:${sig}`)) || 0))
  const [sur, setSur] = useState(false)
  const [solutionVue, setSolutionVue] = useState(false)
  if (!info || (!info.title && !info.description && !(info.hints && info.hints.length))) return null
  const hints = info.hints ?? []
  const visibilite = info.solution_visibility ?? 'after'
  const solutionPermise = Boolean(info.solution_text) && (visibilite === 'always' || (visibilite === 'after' && termine))
  const etoiles = info.difficulty ? '★'.repeat(info.difficulty) + '☆'.repeat(Math.max(0, 5 - info.difficulty)) : ''

  const commencer = () => {
    ecrire(`mc-enonce-vu:${sig}`, '1')
    setIntro(false)
  }
  const indiceSuivant = () => {
    const n = Math.min(hints.length, indices + 1)
    ecrire(`mc-enonce-indices:${sig}`, String(n))
    setIndices(n)
  }

  return (
    <>
      {intro ? (
        <div className="enonce-fond" role="dialog" aria-modal="true" aria-label={t('Énoncé du puzzle')}>
          <div className="enonce-boite">
            <h2>{info.title || t('Puzzle')}</h2>
            {etoiles ? <div className="enonce-difficulte" aria-label={`${t('Difficulté')} ${info.difficulty}/5`}>{etoiles}</div> : null}
            {info.author ? <div className="enonce-auteur">{t('par')} {info.author}</div> : null}
            {info.description ? <p className="enonce-histoire">{info.description}</p> : null}
            {objectifs && objectifs.length > 0 ? (
              <>
                <h3>{t('Objectifs')}</h3>
                <ul className="enonce-objectifs">
                  {objectifs.map((o, i) => <li key={i}>{libelleObjectif(o)}</li>)}
                </ul>
              </>
            ) : null}
            <button type="button" className="enonce-commencer" onClick={commencer}>{t('Commencer')}</button>
          </div>
        </div>
      ) : null}
      <aside className={`panneau-enonce${ouvert ? ' est-ouvert' : ''}`} aria-label={t('Énoncé du puzzle')}>
        <button type="button" className="panneau-enonce-titre" aria-expanded={ouvert} onClick={() => setOuvert(!ouvert)}>
          {t('Énoncé')}
        </button>
        {ouvert ? (
          <div className="panneau-enonce-corps">
            {info.title ? <strong>{info.title}</strong> : null}
            {info.description ? <p>{info.description}</p> : null}
            {hints.length > 0 ? (
              <div className="panneau-enonce-indices">
                {hints.slice(0, indices).map((h, i) => (
                  <p key={i} className="indice">💡 {h}</p>
                ))}
                {indices < hints.length ? (
                  <button type="button" onClick={indiceSuivant}>
                    {t('Indice suivant')} ({indices}/{hints.length})
                  </button>
                ) : null}
              </div>
            ) : null}
            {solutionPermise ? (
              <div className="panneau-enonce-solution">
                {solutionVue ? (
                  <>
                    <strong>{t('Solution de référence')}</strong>
                    <p>{info.solution_text}</p>
                  </>
                ) : (
                  <button type="button" onClick={() => setSolutionVue(true)}>{t('Voir la solution')}</button>
                )}
              </div>
            ) : null}
            <div className="panneau-enonce-actions">
              <button type="button" onClick={() => setIntro(true)}>{t('Relire l’introduction')}</button>
              {sur ? (
                <button type="button" className="danger" onClick={() => recommencer()}>{t('Oui, recommencer')}</button>
              ) : (
                <button type="button" onClick={() => setSur(true)}>{t('Recommencer')}</button>
              )}
            </div>
          </div>
        ) : null}
      </aside>
    </>
  )
}
