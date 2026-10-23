// Le panneau des OBJECTIFS d'un puzzle (E3, 23/10/2026).
//
// Choix de l'utilisateur : un petit panneau REPLIABLE en haut a gauche (orange, comme les modales d'edition de puzzle), et NON un bandeau
// permanent : il ne cache aucune carte tant qu'il est replie, et il garde l'enonce du puzzle sous la main. Les objectifs viennent du moteur
// (`monde.puzzle_objectives`) : une coche verte quand l'objectif est atteint. Un objectif LIBRE (`free_text`, que le moteur ne sait pas
// verifier) a une case que le joueur coche lui-meme : elle part vers `/puzzle_objectif`, route dediee (jamais `/sandbox_command`, qui
// ouvrirait toute l'API `Puzzle.*` a celui qui resout un puzzle publie).
import { useState } from 'react'
import { t } from './langue'
import type { World } from './world'

export type ObjectifPuzzle = NonNullable<World['puzzle_objectives']>[number]

/** Le libelle affiche d'un objectif : son texte s'il en a un, sinon la phrase de son type. */
export function libelleObjectif(objectif: ObjectifPuzzle): string {
  if (objectif.text) return objectif.text
  switch (objectif.kind) {
    case 'defeat_villain':
      return t('Vaincre le méchant')
    case 'survive':
      return t('Survivre jusqu’à la fin du round')
    case 'complete_scheme':
      return objectif.target ? `${t('Terminer la manigance')} ${objectif.target}` : t('Terminer la manigance')
    default:
      return t('Objectif libre')
  }
}

export async function cocherObjectifLibre(index: number): Promise<boolean> {
  try {
    const reponse = await fetch('/puzzle_objectif', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ index }),
    })
    return reponse.ok
  } catch {
    return false
  }
}

export function PanneauObjectifs({
  objectifs,
  cocher = cocherObjectifLibre,
}: {
  objectifs?: readonly ObjectifPuzzle[]
  cocher?: (index: number) => unknown
}) {
  const [ouvert, setOuvert] = useState(false)
  if (!objectifs || objectifs.length === 0) return null
  const atteints = objectifs.filter((x) => x.done).length
  return (
    <aside className={`panneau-objectifs${ouvert ? ' est-ouvert' : ''}`} aria-label={t('Objectifs du puzzle')}>
      <button
        type="button"
        className="panneau-objectifs-titre"
        aria-expanded={ouvert}
        onClick={() => setOuvert(!ouvert)}
      >
        {t('Objectifs')} <span className="panneau-objectifs-compte">{atteints}/{objectifs.length}</span>
      </button>
      {ouvert ? (
        <ul className="panneau-objectifs-liste">
          {objectifs.map((objectif, index) => (
            <li key={index} className={objectif.done ? 'est-atteint' : ''}>
              {objectif.kind === 'free_text' ? (
                <label>
                  <input
                    type="checkbox"
                    checked={objectif.done}
                    disabled={objectif.done}
                    onChange={() => cocher(index)}
                  />{' '}
                  {libelleObjectif(objectif)}
                </label>
              ) : (
                <span>
                  <span className="panneau-objectifs-coche" aria-hidden="true">{objectif.done ? '✔' : '○'}</span>{' '}
                  {libelleObjectif(objectif)}
                </span>
              )}
            </li>
          ))}
        </ul>
      ) : null}
    </aside>
  )
}

/** Le bilan de l'ecran de fin : la liste des objectifs, avec coche ou croix (vide hors puzzle a objectifs). */
export function BilanObjectifs({ objectifs }: { objectifs?: readonly ObjectifPuzzle[] }) {
  if (!objectifs || objectifs.length === 0) return null
  return (
    <ul className="bilan-objectifs" aria-label={t('Bilan des objectifs')}>
      {objectifs.map((objectif, index) => (
        <li key={index} className={objectif.done ? 'est-atteint' : 'est-manque'}>
          <span aria-hidden="true">{objectif.done ? '✔' : '✘'}</span> {libelleObjectif(objectif)}
        </li>
      ))}
    </ul>
  )
}
