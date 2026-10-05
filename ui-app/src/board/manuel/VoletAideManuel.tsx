import { t } from '../langue'
import './VoletAideManuel.css'

type Raccourci = { touches: string; effet: string }

const SUR_UNE_CARTE: Raccourci[] = [
  { touches: 'Double-clic', effet: 'Incliner / redresser ; face cachée : retourner ; sur le méchant : amplification' },
  { touches: 'F7', effet: 'Incliner / redresser' },
  { touches: 'Ctrl + F', effet: 'Retourner la carte' },
  { touches: 'Suppr', effet: 'Défausser ; sur le méchant : vaincre le stade ; sur la manigance principale : manigance terminée' },
  { touches: 'Ctrl + V', effet: 'Envoyer dans la pile de victoire' },
  { touches: '↑  ↓', effet: 'Points de vie (héros, méchant), dégâts (sbire, allié), menace (manigance), sinon marqueur' },
  { touches: '→  ←', effet: 'Un marqueur générique en plus / en moins' },
  { touches: 'F3  Maj + F3', effet: 'Un dégât en plus / en moins' },
  { touches: 'F5  Maj + F5', effet: 'Une menace en plus / en moins sur une manigance' },
  { touches: 'F4  Maj + F4', effet: 'Un jeton d’accélération en plus / en moins' },
  { touches: 'Alt + S', effet: 'Poser Étourdi' },
  { touches: 'Alt + C', effet: 'Poser Confus' },
  { touches: 'Alt + T', effet: 'Poser Coriace' },
  { touches: 'Ctrl + Alt + S', effet: 'Retirer Étourdi' },
  { touches: 'Ctrl + Alt + C', effet: 'Retirer Confus' },
  { touches: 'Ctrl + Alt + T', effet: 'Retirer Coriace' },
]

const SUR_UNE_PILE: Raccourci[] = [
  { touches: 'Ctrl + S', effet: 'Mélanger la pile' },
  { touches: 'Ctrl + D', effet: 'Piocher une carte' },
  { touches: 'Ctrl + Maj + D', effet: 'Piocher plusieurs cartes (le nombre est demandé)' },
  { touches: 'Clic droit', effet: 'Ouvrir la pile : choisir une carte, mélanger, remélanger la défausse dans le deck' },
  { touches: '1 à 9', effet: 'Piocher ce nombre de cartes (en plus d’OCTGN)' },
]

const PARTOUT: Raccourci[] = [
  { touches: 'Alt + Entrée', effet: 'Amplification : sortir la carte du dessus du deck Rencontre' },
  { touches: 'Ctrl + Q', effet: 'Tout redresser' },
  { touches: 'F12', effet: 'Fin de phase des héros : tout redresser, puis piocher jusqu’à la taille de main' },
  { touches: 'Ctrl + Z', effet: 'Annuler le dernier geste' },
  { touches: 'Clic droit sur la table', effet: 'Faire apparaître une carte, pile ou face, nombre ou joueur au hasard, terminer la partie' },
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
            <Tableau titre="Sur une pile" lignes={SUR_UNE_PILE} />
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
