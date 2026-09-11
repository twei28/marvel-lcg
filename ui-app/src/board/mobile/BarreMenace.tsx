// La menace en CASES, pas en pourcentage.
//
// Releve sur play.marvelsimulator.com : une barre decoupee en autant de cases
// que le seuil, et le chiffre geant a cote. On lit « il reste cinq coups » d'un
// coup d'oeil, la ou « 16,7 % » demande un calcul.
import type { ReactElement } from 'react'
import { t } from '../langue'

export function BarreMenace({ pose, total }: { pose: number; total: number }): ReactElement | null {
  // Sans seuil connu, une barre de zero case serait un trait vide : on se tait.
  if (total <= 0) return null
  const remplies = Math.min(pose, total)
  return (
    <div className="barre-menace-bloc">
      <div
        className="barre-menace"
        role="meter"
        aria-valuenow={pose}
        aria-valuemin={0}
        aria-valuemax={total}
        aria-label={t('Menace')}
      >
        {Array.from({ length: total }, (_, index) => (
          <span className={`barre-menace-case${index < remplies ? ' est-pose' : ''}`} key={index} />
        ))}
      </div>
      <span className="barre-menace-compte">
        <b>{pose}</b>
        <small>/{total}</small>
        <em>{t('Menace')}</em>
      </span>
    </div>
  )
}
