import { t } from '../langue'
import './VoletAideManuel.css'

type Raccourci = { touches: string; effet: string }

// Lot 3 du 06/10/2026 (spec §D.12) : comment jouer une carte, en tête, comme
// sur OCTGN. Aucune aide au paiement (question 9) : on dit seulement comment
// payer à la main.
const JOUER_UNE_CARTE: Raccourci[] = [
  { touches: 'Paie', effet: 'Survole une carte de ta main et appuie sur Suppr, ou glisse-la sur ta défausse. F7 ou un double-clic incline une carte en jeu.' },
  { touches: 'Pose', effet: 'Glisse la carte de ta main et lâche-la n’importe où sur la table : un allié va dans Alliés, un soutien dans Soutiens, un événement à côté de ton héros (résous-le, puis Suppr). Un double-clic sur la carte fait pareil.' },
  { touches: 'Amélioration', effet: 'Lâchée sur la table, elle va sous ton héros s’il est le seul à pouvoir la recevoir ; sinon tu choisis la carte.' },
  { touches: 'Lâche sur une carte', effet: 'Y attacher une amélioration.' },
  { touches: 'Lâche sur une pile', effet: 'La mettre dessus, ou dessous avec Maj.' },
  { touches: 'Maj en glissant', effet: 'Sur la table : la poser face cachée.' },
  { touches: 'Maj + glisser une carte en jeu', effet: 'Sur une autre carte en jeu : tracer une flèche vers elle (la refaire l’efface)' },
  { touches: 'Clic droit sur une carte', effet: 'Poser en jeu (carte de ta main), Déplacer vers…' },
  { touches: 'Clic droit sur une carte en main', effet: 'Échanger avec le dessus du deck' },
  { touches: 'Glisser dans sa rangée', effet: 'Lâchée entre deux cartes de sa rangée (alliés, sbires, manigances…), la carte s’y range ; Alt + glisser aussi' },
  { touches: 'Glisser une amélioration', effet: 'Lâchée près de son personnage, elle change de rang ou de côté et reste attachée' },
]

const SUR_UNE_CARTE: Raccourci[] = [
  { touches: 'Double-clic', effet: 'Incliner / redresser ; face cachée : retourner ; sur le méchant : carte boost, face cachée à côté de lui' },
  { touches: 'F7', effet: 'Incliner / redresser' },
  { touches: 'Ctrl + F', effet: 'Retourner la carte' },
  { touches: 'Suppr', effet: 'Défausser ; sur le méchant : vaincre le stade ; sur la manigance principale : manigance terminée ; une carte Permanente refuse ; une carte « Victoire » va à la pile de victoire (question si elle n’a pas été vaincue)' },
  { touches: 'Ctrl + V', effet: 'Envoyer dans la pile de victoire' },
  { touches: 'Ctrl + I', effet: 'Fiche de la carte (et ses mots-clés), fixe jusqu’à Échap ou un clic' },
  { touches: 'Ctrl + A', effet: 'Sur un méchant : le marquer méchant actif (repère vert)' },
  { touches: 'Clic droit', effet: 'Aussi : Sous le deck du héros, Sous le deck Rencontre' },
  { touches: 'Maj + clic', effet: 'Cibler / décibler la carte (à ta couleur, vu de tous)' },
  { touches: 'Pavé num. 1 à 7', effet: 'Surligner : 1 bleu, 2 orange, 3 vert, 4 violet, 5 rouge, 6 noir, 7 blanc' },
  { touches: 'Pavé num. 0', effet: 'Retirer le surlignage' },
  { touches: '↑  ↓', effet: '↑ +1 PV, ↓ −1 PV (héros, méchant) ; ↑ +1 dégât, ↓ −1 dégât (allié, sbire) ; menace (manigance), sinon marqueur' },
  { touches: '→  ←', effet: 'Un marqueur générique en plus / en moins' },
  { touches: 'F3  Maj + F3', effet: 'Un dégât en plus / en moins' },
  { touches: 'F5  Maj + F5', effet: 'Une menace en plus / en moins sur une manigance' },
  { touches: 'F4  Maj + F4', effet: 'Un jeton d’accélération en plus / en moins' },
  { touches: 'Alt + S', effet: 'Poser Sonné' },
  { touches: 'Alt + C', effet: 'Poser Désorienté' },
  { touches: 'Alt + T', effet: 'Poser Tenace' },
  { touches: 'Ctrl + Alt + S', effet: 'Retirer Sonné' },
  { touches: 'Ctrl + Alt + C', effet: 'Retirer Désorienté' },
  { touches: 'Ctrl + Alt + T', effet: 'Retirer Tenace' },
  { touches: 'F1', effet: 'Choisir un marqueur (ouvre le menu de la carte)' },
  { touches: 'Maj + F1', effet: 'Effacer les marqueurs de la carte' },
  { touches: 'Menu  Maj + F10', effet: 'Ouvrir le menu de la carte survolée' },
  { touches: 'F', effet: 'Retourner (en plus d’OCTGN)' },
  { touches: 'Q', effet: 'Incliner (en plus d’OCTGN)' },
  { touches: '1 à 9', effet: 'Poser ce nombre de dégâts, de menace ou de compteurs (en plus d’OCTGN)' },
]

const SUR_UNE_PILE: Raccourci[] = [
  { touches: 'Ctrl + S', effet: 'Mélanger la pile' },
  { touches: 'Ctrl + D', effet: 'Piocher une carte' },
  { touches: 'Ctrl + Maj + D', effet: 'Piocher plusieurs cartes (le nombre est demandé)' },
  { touches: 'Clic droit', effet: 'Ouvrir la pile : choisir une carte, mélanger, remélanger la défausse dans le deck' },
  { touches: '1 à 9', effet: 'Piocher ce nombre de cartes (en plus d’OCTGN)' },
  { touches: 'R', effet: 'Mélanger la pile (en plus d’OCTGN)' },
  { touches: 'Ctrl + F', effet: 'Retourner la carte du dessus' },
  { touches: 'Ctrl + U', effet: 'Piocher une carte face cachée' },
  { touches: 'Ctrl + Maj + U', effet: 'Piocher plusieurs cartes face cachée' },
]

const PARTOUT: Raccourci[] = [
  { touches: 'Alt + Entrée', effet: 'Carte boost : la carte du dessus du deck Rencontre, face cachée, à côté du méchant' },
  { touches: 'Ctrl + Q', effet: 'Tout redresser' },
  { touches: 'F12', effet: 'Fin de phase des héros, pour tous les héros : tout redresser, défausser l’excédent de main, piocher jusqu’à la taille de main (la défausse est remélangée si le deck est vide)' },
  { touches: 'Ctrl + Z', effet: 'Annuler le dernier geste' },
  { touches: 'Échap', effet: 'Fermer le catalogue ; sinon décibler toutes tes cartes et effacer tes flèches (aussi à la fin de phase des héros, F12)' },
  { touches: 'C', effet: 'Chercher une carte dans tout le catalogue pour la poser' },
  { touches: 'Clic droit sur la table', effet: 'Faire apparaître une carte, Vaincre ce stade, Manigance terminée, Tout redresser, Fin de phase des héros, Carte boost, Pile ou face, Nombre au hasard, Joueur au hasard, Fin du round, Défausser une carte au hasard, Mulligan, Mis de côté vers le deck Rencontre (tout, ou un set choisi), Terminer la partie' },
]

const SELECTION: Raccourci[] = [
  { touches: 'Ctrl + clic', effet: 'Ajouter ou retirer la carte de la sélection' },
  { touches: 'Glisser sur la table vide', effet: 'Tracer un rectangle : les cartes qu’il touche sont sélectionnées (Ctrl pour ajouter)' },
  { touches: 'Clic simple', effet: 'Ailleurs : vider la sélection' },
  { touches: 'Sur une carte sélectionnée', effet: 'Touches, double-clic, menu et glisser valent pour toute la sélection ; un seul Ctrl+Z annule tout' },
]

const SANS_OBJET: Raccourci[] = [
  { touches: 'Ctrl + H, Ctrl + V sur la table', effet: 'Charger un héros ou un méchant : la préparation de la partie le fait' },
  { touches: 'F8', effet: 'Prendre le contrôle des cartes : notion propre à OCTGN, chacun bouge déjà ses cartes' },
  { touches: 'F10, molette, Espace', effet: 'Caméra d’OCTGN : la table s’adapte seule à l’écran' },
  { touches: 'Get Position, Toggle Debug', effet: 'Outils de développeur d’OCTGN' },
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

/**
 * Les écrans où l'aide ne s'ouvre PAS seule au passage en manuel (06/10/2026).
 * Mesuré au passage navigateur du lot 7 : à 1024 px le volet couvre le tiers
 * droit, main comprise, et à 390 px tout l'écran ; à 1280 et 1920 px il laisse
 * la table jouable. Le pointeur grossier attrape une grande tablette.
 */
export const ECRAN_SANS_AIDE_AUTO = '(max-width: 1099px), (pointer: coarse)'

/** L'aide s'ouvre-t-elle seule ? Oui sur PC ; sinon la languette suffit. */
export function aideSOuvreSeule(): boolean {
  try {
    return !window.matchMedia(ECRAN_SANS_AIDE_AUTO).matches
  } catch {
    return true
  }
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
            <Tableau titre="Jouer une carte" lignes={JOUER_UNE_CARTE} />
            <Tableau titre="Sur une carte" lignes={SUR_UNE_CARTE} />
            <Tableau titre="Sur une pile" lignes={SUR_UNE_PILE} />
            <Tableau titre="Partout" lignes={PARTOUT} />
            <Tableau titre="Plusieurs cartes à la fois" lignes={SELECTION} />
            <Tableau titre="Sans objet ici" lignes={SANS_OBJET} />
            <p className="aide-manuel-intro">
              {t('Pour rendre la main au moteur, clique sur Auto en haut de l’écran.')}
            </p>
          </div>
        </aside>
      ) : null}
    </>
  )
}
