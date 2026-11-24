// LA MAIN, posee SOUS les zones (decision du 24/10/2026, questions 32, 33 et 73) : une rangee de cartes qui defile de cote,
// jamais par-dessus la table. Quand les zones grandissent, la table defile au-dessus et la main rapetisse (hauteur en vh).
// Repliable par la languette « Main » (l'encoche de droite) ; elle se rouvre toute seule quand le moteur demande une carte
// de la main (PlateauPortrait). Toucher une carte l'OUVRE en grand avec « Jouer » / « Fermer » (24/10/2026 : les petits
// boutons « Lire » / « Jouer » au-dessus de la main etaient trop durs a viser) ; glisser vers le haut la joue toujours.
import type { ReactElement } from 'react'
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
  return (
    <section className="main-dock" aria-label={t('Ta main')}>
      <header className="main-dock-entete">
        <h2 className="ronds-titre">
          {t('Main')} · {unites.length}
        </h2>
        <span className="main-dock-boutons">
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
              choisie={false}
              onOuvrir={onOuvrir}
              paiement={enPaiement}
              onAgir={jouable(unite) ? onJouer : undefined}
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
