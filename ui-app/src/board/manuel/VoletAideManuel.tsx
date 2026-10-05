import { t } from '../langue'
import './VoletAideManuel.css'

type Raccourci = { touches: string; effet: string }

const SUR_UNE_CARTE: Raccourci[] = [
  { touches: 'Double-clic', effet: 'Incliner / redresser ; sur le méchant, révéler la carte d’amplification' },
  { touches: '↑  ↓', effet: 'Un dégât en plus / en moins (menace sur une manigance)' },
  { touches: '→  ←', effet: 'Un jeton générique en plus / en moins' },
  { touches: 'Suppr', effet: 'Défausser dans la bonne pile' },
  { touches: 'Clic droit', effet: 'Tous les jetons, un par un' },
]

const PARTOUT: Raccourci[] = [
  { touches: 'Clic droit sur la table', effet: 'Faire apparaître une carte, vaincre ce stade, manigance terminée, terminer la partie' },
]

function Tableau({ titre, lignes }: { titre: string; lignes: Raccourci[] }) {
  return (
    <section className="aide-manuel-groupe">
      <h3>{t(titre)}</h3>
      <dl>
        {lignes.map((ligne) => (
          <div key={ligne.touches} className="aide-manuel-ligne">
            <dt>
              <kbd>{t(ligne.touches)}</kbd>
            </dt>
            <dd>{t(ligne.effet)}</dd>
          </div>
        ))}
      </dl>
    </section>
  )
}

export function VoletAideManuel({
  ouvert,
  ouvrir,
  fermer,
}: {
  ouvert: boolean
  ouvrir: () => void
  fermer: () => void
}) {
  return (
    <>
      <button
        type="button"
        className={`volet-aide-languette${ouvert ? ' est-ouvert' : ''}`}
        aria-expanded={ouvert}
        aria-controls="volet-aide-manuel"
        title={ouvert ? t('Refermer l’aide du mode manuel') : t('Ouvrir l’aide du mode manuel')}
        onClick={ouvert ? fermer : ouvrir}
      >
        <span>{t('Aide')}</span>
      </button>
      {ouvert ? (
        <aside id="volet-aide-manuel" className="volet-aide" role="dialog" aria-label={t('Aide du mode manuel')}>
          <header className="volet-aide-tete">
            <h2>{t('Aide du mode manuel')}</h2>
            <button type="button" className="reglages-fermer" onClick={fermer} title={t('Fermer')}>
              ×
            </button>
          </header>
          <div className="volet-aide-contenu">
            <p className="aide-manuel-intro">
              {t('Le moteur se tait. Les touches agissent sur ce que la souris survole.')}
            </p>
            <Tableau titre="Sur une carte" lignes={SUR_UNE_CARTE} />
            <Tableau titre="Partout" lignes={PARTOUT} />
            <p className="aide-manuel-intro">
              {t('Pour rendre la main au moteur, clique sur Auto en haut de l’écran.')}
            </p>
          </div>
        </aside>
      ) : null}
    </>
  )
}
