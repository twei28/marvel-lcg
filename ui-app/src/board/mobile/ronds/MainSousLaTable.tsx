// LA MAIN, posee SOUS les zones (decision du 24/10/2026, questions 32, 33 et 73) : une rangee de cartes qui defile de cote,
// jamais par-dessus la table. Quand les zones grandissent, la table defile au-dessus et la main rapetisse (hauteur en vh).
// Repliable par la languette « Main » (l'encoche de droite) ; elle se rouvre toute seule quand le moteur demande une carte
// de la main (PlateauPortrait). Meme geste que la feuille de la main : toucher une carte jouable la choisit, « Jouer » la joue.
import { useEffect, useState, type ReactElement } from 'react'
import { t } from '../../langue'
import type { UniteAffichee } from '../../zones'
import { CarteMainPortrait } from '../MainPortrait'
import './ronds.css'

export function MainSousLaTable({
  unites,
  onOuvrir,
  onJouer,
  jouable,
  onReplier,
  enPaiement = false,
  enJeuPayants = [],
}: {
  unites: UniteAffichee[]
  onOuvrir: (unite: UniteAffichee) => void
  onJouer: (unite: UniteAffichee) => void
  jouable: (unite: UniteAffichee) => boolean
  onReplier: () => void
  /** Le moteur demande de payer : un toucher choisit la carte, sans passer par sa fiche. */
  enPaiement?: boolean
  /** Les cartes DE LA TABLE qui peuvent payer (soutiens producteurs de ressources) : dans la rangee, apres « EN JEU ». */
  enJeuPayants?: UniteAffichee[]
}): ReactElement {
  const [cleChoisie, setCleChoisie] = useState<string | undefined>()
  const choisie = cleChoisie === undefined ? undefined : unites.find((u) => u.cle === cleChoisie)
  const choisieValide = choisie && jouable(choisie) ? choisie : undefined
  useEffect(() => {
    if (cleChoisie !== undefined && !choisieValide) setCleChoisie(undefined)
  }, [cleChoisie, choisieValide])
  return (
    <section className="main-dock" aria-label={t('Ta main')}>
      <header className="main-dock-entete">
        <h2 className="ronds-titre">
          {t('Main')} · {unites.length}
        </h2>
        <span className="main-dock-boutons">
          {choisieValide ? (
            <>
              <button type="button" className="main-dock-lire" onClick={() => onOuvrir(choisieValide)}>
                {t('Lire')}
              </button>
              <button
                type="button"
                className="main-dock-jouer"
                data-tactile="jouer"
                onClick={() => {
                  setCleChoisie(undefined)
                  onJouer(choisieValide)
                }}
              >
                {t('Jouer')}
              </button>
            </>
          ) : null}
          <button type="button" className="main-dock-replier" onClick={onReplier} aria-label={t('Replier la main')}>
            ▼
          </button>
        </span>
      </header>
      {unites.length === 0 ? (
        <p className="portrait-vide">{t('Ta main est vide')}</p>
      ) : (
        <div className="main-portrait defile main-dock-rangee">
          {unites.map((unite) => (
            <CarteMainPortrait
              key={unite.cle}
              unite={unite}
              choisie={choisieValide?.cle === unite.cle}
              onChoisir={jouable(unite) ? (u) => setCleChoisie((avant) => (avant === u.cle ? undefined : u.cle)) : undefined}
              onOuvrir={onOuvrir}
              paiement={enPaiement}
              onAgir={
                jouable(unite)
                  ? (u) => {
                      setCleChoisie(undefined)
                      onJouer(u)
                    }
                  : undefined
              }
            />
          ))}
          {enJeuPayants.length > 0 ? (
            <>
              <span className="main-dock-separation" role="separator">
                <b>{t('EN JEU')}</b>
              </span>
              {enJeuPayants.map((unite) => (
                <CarteMainPortrait key={unite.cle} unite={unite} choisie={false} onOuvrir={onOuvrir} paiement />
              ))}
            </>
          ) : null}
        </div>
      )}
    </section>
  )
}
