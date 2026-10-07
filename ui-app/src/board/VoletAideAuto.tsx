// L'AIDE DU MODE AUTO (demande du 07/10/2026) : la meme languette que l'aide
// du mode manuel, pour les gestes qu'on ne devine pas (« Alt + glisser » pour
// ranger ses cartes, le double-clic pour renommer une zone). Fermee par defaut.
import { t } from './langue'
import './manuel/VoletAideManuel.css'

type Raccourci = { touches: string; effet: string }

const PENDANT_LA_PARTIE: Raccourci[] = [
  { touches: 'E  Espace', effet: 'Finir ton tour' },
  { touches: 'Entrée  Espace', effet: 'Étape suivante pendant le déroulé d’une phase' },
  { touches: 'U', effet: 'Annuler' },
]

const RANGER_SES_CARTES: Raccourci[] = [
  { touches: 'Alt + glisser', effet: 'Changer la place d’une carte dans sa rangée (soutiens, alliés…) : un trait jaune montre où elle se pose. Ton ordre est gardé pendant la partie, et seul toi le vois.' },
  { touches: 'Alt + glisser une amélioration', effet: 'Changer l’ordre des améliorations d’une même carte' },
]

const LA_TABLE: Raccourci[] = [
  { touches: 'Réglages › Apparence', effet: '« Modifier la table » : glisse une zone pour la déplacer, ses poignées règlent sa place et la taille de ses cartes' },
  { touches: 'Double-clic sur le titre', effet: 'Dans « Modifier la table » : renommer la zone (laisse vide pour reprendre le titre d’origine)' },
  { touches: 'Réglages › Jeu', effet: '« Améliorations » : à gauche ou à droite de la carte qui les porte' },
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

export function VoletAideAuto({ ouvert, ouvrir, fermer }: { ouvert: boolean; ouvrir: () => void; fermer: () => void }) {
  return (
    <>
      <button
        type="button"
        className={`volet-aide-languette${ouvert ? ' est-ouvert' : ''}`}
        aria-expanded={ouvert}
        aria-controls="volet-aide-auto"
        title={ouvert ? t('Refermer l’aide') : t('Ouvrir l’aide')}
        onClick={ouvert ? fermer : ouvrir}
      >
        <span>{t('Aide')}</span>
      </button>
      {ouvert ? (
        <aside id="volet-aide-auto" className="volet-aide" role="dialog" aria-label={t('Aide')}>
          <header className="volet-aide-tete">
            <h2>{t('Aide')}</h2>
            <button type="button" className="reglages-fermer" onClick={fermer} title={t('Fermer')}>
              ×
            </button>
          </header>
          <div className="volet-aide-contenu">
            <Tableau titre="Pendant la partie" lignes={PENDANT_LA_PARTIE} />
            <Tableau titre="Ranger tes cartes" lignes={RANGER_SES_CARTES} />
            <Tableau titre="La table" lignes={LA_TABLE} />
          </div>
        </aside>
      ) : null}
    </>
  )
}
