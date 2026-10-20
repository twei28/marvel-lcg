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
  { touches: 'B', effet: 'Copier le rapport de bug (les 20 dernières entrées du journal), sans ouvrir de panneau' },
  { touches: '1 à 9', effet: 'Choisir l’option portant ce numéro dans le cartouche du bas' },
  { touches: 'Échap  ×', effet: 'Annuler l’action en cours : la partie revient avant le choix de la carte' },
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

// LE TELEPHONE (10/10/2026) : les touches et le glisser-Alt n'existent pas au
// doigt. Chaque ligne decrit le geste tel que le code le fait (mobile/).
const TEL_LE_PLATEAU: Raccourci[] = [
  { touches: 'Glisser vers le haut ou le bas', effet: 'Passer d’une bande à l’autre : méchant, manigances, ennemis engagés, ton héros' },
  { touches: 'Glisser de côté sur une bande', effet: 'Faire défiler ses cartes. Le méchant, la manigance principale et ton identité restent au bord.' },
  { touches: 'Toucher une carte', effet: 'L’ouvrir en grand pour la lire' },
  { touches: 'Appui long sur une carte', effet: 'Agir avec elle (attaquer, contrer, utiliser son effet)' },
]

const TEL_TA_MAIN: Raccourci[] = [
  { touches: 'Languette de droite', effet: 'Ouvrir ta main (toucher, ou glisser vers la gauche). Elle s’ouvre seule quand une question porte sur une carte en main.' },
  { touches: 'Toucher une carte jouable', effet: 'La choisir : « Lire » et « Jouer » apparaissent en bas. Toucher encore la repose.' },
  { touches: 'Toucher une autre carte', effet: 'L’ouvrir en grand pour la lire' },
  { touches: 'Appui long sur une carte', effet: 'La jouer tout de suite si elle est jouable, sinon l’ouvrir en grand' },
  { touches: 'Défausse de fin de tour', effet: 'Un toucher coche ou décoche la carte' },
  { touches: 'Fermer la main', effet: 'Toucher le fond, glisser vers la droite ou « Fermer »' },
]

const TEL_PILES: Raccourci[] = [
  { touches: 'Languette de gauche', effet: 'Ouvrir les piles : ton deck, ta défausse, le deck rencontre, le némésis…' },
  { touches: 'Toucher une pile', effet: 'Voir ses cartes' },
  { touches: 'Appui long sur une languette', effet: 'La monter ou la descendre du doigt. Sa place est gardée.' },
]

const TEL_PENDANT_LA_PARTIE: Raccourci[] = [
  { touches: 'Bouton du bandeau', effet: 'L’action du moment, comme « Fin du tour »' },
  { touches: 'Menu « … »', effet: 'Annuler, sauver, historique, réglages, journal, quitter' },
  { touches: 'Bandeau « Annuler »', effet: 'Pendant 5 secondes après ton action, il la défait' },
  { touches: 'Phase du méchant', effet: 'Le panneau montre chaque carte révélée. « Suivant » avance, « Continuer » termine.' },
  { touches: 'Retour d’Android', effet: 'Fermer la fenêtre ouverte au lieu de quitter la partie' },
]

const TEL_REGLAGES: Raccourci[] = [
  { touches: 'Réglages › Apparence', effet: '« Taille du texte » (normale, grande, très grande) et « Verrou portrait »' },
  { touches: 'Réglages › Son', effet: '« Vibrations » : ton tour, attaque subie, action validée' },
  { touches: 'Menu « … »', effet: '« Installer l’application » : le jeu en plein écran, avec une icône. Seulement si ton navigateur le permet.' },
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

export function VoletAideAuto({
  ouvert,
  ouvrir,
  fermer,
  telephone = false,
}: {
  ouvert: boolean
  ouvrir: () => void
  fermer: () => void
  /** Plateau en bandes : l'aide des gestes du doigt, pas celle du clavier. */
  telephone?: boolean
}) {
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
            {telephone ? (
              <>
                <Tableau titre="Le plateau" lignes={TEL_LE_PLATEAU} />
                <Tableau titre="Ta main" lignes={TEL_TA_MAIN} />
                <Tableau titre="Les piles" lignes={TEL_PILES} />
                <Tableau titre="Pendant la partie" lignes={TEL_PENDANT_LA_PARTIE} />
                <Tableau titre="Réglages du téléphone" lignes={TEL_REGLAGES} />
              </>
            ) : (
              <>
                <Tableau titre="Pendant la partie" lignes={PENDANT_LA_PARTIE} />
                <Tableau titre="Ranger tes cartes" lignes={RANGER_SES_CARTES} />
                <Tableau titre="La table" lignes={LA_TABLE} />
              </>
            )}
          </div>
        </aside>
      ) : null}
    </>
  )
}
