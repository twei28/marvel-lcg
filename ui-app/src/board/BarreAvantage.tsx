// LA BARRE D'AVANTAGE (22/10/2026, backlog n°3) : une barre tres fine collee au bord gauche de l'ecran, qui monte quand
// les heros dominent et descend quand la partie tourne mal. Option des Reglages, DESACTIVEE par defaut. Le detail
// s'affiche au survol (ou au clavier). Voir barre-avantage.ts : c'est une estimation, jamais une probabilite.
import { useEffect, useMemo, useState } from 'react'
import { t } from './langue'
import { estimerAvantage } from './barre-avantage'
import { EVENEMENT_BARRE_AVANTAGE, lireBarreAvantage } from './barre-avantage-reglage'
import type { World } from './world'
import './barre-avantage.css'

function useBarreActive(): boolean {
  const [actif, setActif] = useState(lireBarreAvantage)
  useEffect(() => {
    const relire = () => setActif(lireBarreAvantage())
    window.addEventListener(EVENEMENT_BARRE_AVANTAGE, relire)
    window.addEventListener('storage', relire)
    return () => {
      window.removeEventListener(EVENEMENT_BARRE_AVANTAGE, relire)
      window.removeEventListener('storage', relire)
    }
  }, [])
  return actif
}

export function BarreAvantage({ monde }: { monde: World | undefined }) {
  const actif = useBarreActive()
  const avantage = useMemo(() => (actif ? estimerAvantage(monde) : null), [actif, monde])
  if (!actif || !avantage || avantage.etat === 'masque') return null

  if (avantage.etat === 'indisponible') {
    return (
      <div className="barre-avantage est-indisponible" role="img" aria-label={t('Estimation indisponible')} tabIndex={0}>
        <div className="barre-avantage-haut" style={{ height: '50%' }} />
        <div className="barre-avantage-bas" style={{ height: '50%' }} />
        <div className="barre-avantage-detail">
          <strong>{t('Estimation indisponible')}</strong>
          <span>{t('Ce scénario a des règles que l’estimation ne sait pas encore lire.')}</span>
        </div>
      </div>
    )
  }

  const titre =
    avantage.valeur > 0.6 ? t('Les héros dominent') : avantage.valeur < 0.4 ? t('La partie tourne mal') : t('Partie équilibrée')
  const haut = Math.round(avantage.valeur * 100)
  return (
    <div className="barre-avantage" role="img" aria-label={titre} tabIndex={0}>
      <div className="barre-avantage-haut" style={{ height: `${haut}%` }} />
      <div className="barre-avantage-bas" style={{ height: `${100 - haut}%` }} />
      <div className="barre-avantage-milieu" />
      <div className="barre-avantage-detail">
        <strong>{titre}</strong>
        <ul>
          {avantage.tours !== null ? (
            <li>
              {t('Défaite dans environ')} <b>{avantage.tours}</b> {avantage.tours > 1 ? t('tours') : t('tour')}
            </li>
          ) : null}
          {avantage.mechantPct !== null ? (
            <li>
              {t('Méchant à')} <b>{avantage.mechantPct} %</b> {t('de ses PV')}
            </li>
          ) : null}
          {avantage.herosPct !== null ? (
            <li>
              {t('Héros à')} <b>{avantage.herosPct} %</b> {t('de leurs PV')}
            </li>
          ) : null}
          {avantage.sbires > 0 ? (
            <li>
              <b>{avantage.sbires}</b> {avantage.sbires > 1 ? t('sbires engagés') : t('sbire engagé')}
            </li>
          ) : null}
        </ul>
        <small>{t('Estimation, pas une probabilité')}</small>
      </div>
    </div>
  )
}
