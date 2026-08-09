// Le médaillon : une carte POSÉE, vue de téléphone.
//
// Ce n'est pas une carte en miniature. Les jeux de cartes qui tiennent sur un
// petit écran (Hearthstone, MTG Arena, Gwent) changent la FORME d'une carte
// quand elle arrive sur la table : elle devient un jeton réduit à ce qui décide.
// Garder le format carte gaspille la hauteur — c'est l'erreur que ce composant
// remplace, dans les deux sens : la version d'origine réduisait la carte à une
// vignette de 34 px illisible, la suivante gardait la carte entière et ne
// tenait plus à l'écran.
//
// Ce qu'un médaillon porte, et rien d'autre :
//   - l'illustration, recadrée PAR LE HAUT (le visage y est presque toujours) ;
//   - UNE pastille cerclée qui déborde : les PV, ou la menace d'une manigance ;
//   - les états (coriace, sonné, désorienté) en petites icônes sur le bord ;
//   - les améliorations attachées en jetons décalés en bas à droite, comme
//     elles se glissent derrière leur porteur sur le plateau PC.
//
// Tout le reste — attaque, contre, défense, texte de règles — s'affiche quand on
// ouvre la carte. C'est un choix assumé : deux chiffres de plus rendaient le
// médaillon illisible à cette taille.

import type { CardEffectDelta, ScanCardProps } from '../../components/ScanCard'
import { t } from '../langue'
import './mobile.css'

/** Les états que le moteur pose en cartes attachées sur le personnage. */
const ETATS: Record<string, { lettre: string; classe: string; nom: string }> = {
  tough: { lettre: 'T', classe: 'est-coriace', nom: 'Coriace' },
  stunned: { lettre: 'S', classe: 'est-sonne', nom: 'Sonné' },
  confused: { lettre: 'C', classe: 'est-desoriente', nom: 'Désorienté' },
}

function etatDe(carte: ScanCardProps) {
  return ETATS[carte.name.trim().toLowerCase()]
}

export type MedaillonProps = {
  carte: ScanCardProps
  /** Cartes que le moteur a posées sur celle-ci : statuts ET améliorations. */
  attachees?: ScanCardProps[]
  /** « grand » pour la manigance principale, qui décide de la défaite. */
  taille?: 'normal' | 'grand'
  /** Variation de compteur en cours : le nombre qui s'envole. */
  effet?: CardEffectDelta
  onOuvrir: (carte: ScanCardProps) => void
}

export function Medaillon({
  carte,
  attachees = [],
  taille = 'normal',
  effet,
  onOuvrir,
}: MedaillonProps) {
  const etats = attachees.map(etatDe).filter((etat): etat is NonNullable<typeof etat> => !!etat)
  const ameliorations = attachees.filter((attachee) => !etatDe(attachee))
  // Une seule pastille : les PV d'un personnage, ou la menace d'une manigance.
  const pastille = carte.allyHp ?? carte.schemeThreat

  const classes = [
    'medaillon',
    `medaillon-${taille}`,
    carte.state ? `state-${carte.state}` : '',
    carte.exhausted ? 'est-incline' : '',
    carte.facedown ? 'est-cachee' : '',
  ]
    .filter(Boolean)
    .join(' ')

  return (
    <button
      type="button"
      className={classes}
      onClick={() => onOuvrir(carte)}
      data-card-id={carte.id}
      data-tactile="medaillon"
      aria-label={`${carte.name}${pastille ? ` — ${pastille}` : ''}`}
    >
      <span className="medaillon-art" aria-hidden="true">
        {carte.facedown ? null : (
          <img
            src={carte.imageUrl}
            alt=""
            // Une manigance se pose en PAYSAGE, mais son scan est fourni en
            // portrait : sans ce quart de tour, on la lit couchée dans le
            // médaillon. Le plateau PC applique exactement la même règle
            // (classe scan-a-tourner de ScanCard.css).
            className={carte.isLandscape && carte.scanIsPortrait ? 'est-a-tourner' : undefined}
          />
        )}
      </span>

      {pastille ? <span className="medaillon-pastille">{pastille}</span> : null}

      {/* Le nombre qui s'envole. Sans lui, en phase du méchant accélérée, on
          voit la pastille changer sans savoir QUI a encaissé ni COMBIEN. La clé
          porte la valeur : deux coups successifs rejouent l'animation au lieu
          de la figer sur le premier. */}
      {effet ? (
        <span className={`medaillon-envol est-${effet.kind}`} key={`${effet.kind}:${effet.value}`}>
          {effet.value > 0 ? `+${effet.value}` : effet.value}
        </span>
      ) : null}

      {etats.length > 0 ? (
        <span className="medaillon-etats">
          {etats.map((etat) => (
            <span className={`medaillon-etat ${etat.classe}`} key={etat.lettre} title={t(etat.nom)}>
              {etat.lettre}
            </span>
          ))}
        </span>
      ) : null}

      {ameliorations.length > 0 ? (
        <span className="medaillon-attaches" aria-label={`${ameliorations.length} ${t('Amélioration')}`}>
          {/* Trois jetons au plus : au-delà, le compte suffit et la pile reste
              lisible. Le détail s'obtient en ouvrant le porteur. */}
          {ameliorations.slice(0, 3).map((attachee) => (
            <span className="medaillon-attache" key={attachee.id}>
              <img src={attachee.imageUrl} alt="" />
            </span>
          ))}
          {ameliorations.length > 3 ? (
            <span className="medaillon-attache est-compte">+{ameliorations.length - 3}</span>
          ) : null}
        </span>
      ) : null}
    </button>
  )
}
