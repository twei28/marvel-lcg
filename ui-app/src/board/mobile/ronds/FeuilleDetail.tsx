// Ce qui se lit SOUS la grande carte d'un rond (decision Q71, 24/10/2026 : « tout voir, comme sur le PC ») : les valeurs
// AJUSTEES avec leur origine (« ATQ 3 (2 +1) »), les jetons, les mots-cles. Les PV / la menace sont la bande de jauge de la
// carte elle-meme ; les cartes de statut et les ameliorations attachees restent les mini-cartes de `CarteOuverte`, les boutons
// d'action sont les siens.
// Memes mots et memes composants que l'apercu du PC (`FaceCarteApercu`, Board.tsx) : `JetonsCarte` pour les jetons (sous la
// carte, jamais sur le texte) et la liste `apercu-mots-cles` pour les mots-cles avec leur definition.
import type { ReactElement } from 'react'
import { JetonsCarte, type ScanCardProps } from '../../../components/ScanCard'
import { t } from '../../langue'

const NOMS_STAT: Record<string, string> = { ATK: 'ATQ', THW: 'CTR', DEF: 'DÉF', REC: 'REC', SCH: 'MNG', HP: 'PV' }

/** « ATQ 3 (2 +1) » quand la valeur du moteur differe de la valeur imprimee, « ATQ 2 » sinon. Pure : testee. */
export function ligneDeStat(stat: { label: string; value: number; base?: number }): { nom: string; texte: string; sens: 'plus' | 'moins' | 'egal' } {
  const nom = NOMS_STAT[stat.label] ?? stat.label
  if (stat.base === undefined || stat.base === stat.value) return { nom, texte: `${stat.value}`, sens: 'egal' }
  const ecart = stat.value - stat.base
  return { nom, texte: `${stat.value} (${stat.base} ${ecart > 0 ? '+' : '−'}${Math.abs(ecart)})`, sens: ecart > 0 ? 'plus' : 'moins' }
}

export function FeuilleDetail({ carte }: { carte: ScanCardProps }): ReactElement | null {
  const stats = (carte.statsComplets ?? []).filter((s) => s.label !== 'HP')
  const jetons = carte.counters ?? []
  const motsCles = carte.facedown ? [] : (carte.keywords ?? [])
  const aDesJetons = !!carte.jetonMenace || !!carte.jetonDegats || jetons.length > 0
  if (stats.length === 0 && !aDesJetons && motsCles.length === 0) return null
  return (
    <div className="feuille-detail">
      {stats.length > 0 ? (
        <ul className="feuille-stats">
          {stats.map((stat) => {
            const ligne = ligneDeStat(stat)
            return (
              <li key={stat.label} className={`est-${ligne.sens}`}>
                <span>{ligne.nom}</span> {ligne.texte}
              </li>
            )
          })}
        </ul>
      ) : null}
      {aDesJetons ? (
        <div className="feuille-jetons">
          <JetonsCarte menace={carte.jetonMenace} degats={carte.jetonDegats} compteurs={jetons} dessous />
        </div>
      ) : null}
      {motsCles.length > 0 ? (
        <dl className="apercu-mots-cles">
          {motsCles.map((mot) => (
            <div key={mot.nom}>
              <dt>{mot.nom}</dt>
              <dd>{mot.definition}</dd>
            </div>
          ))}
        </dl>
      ) : null}
    </div>
  )
}
