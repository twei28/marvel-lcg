// Une carte POSEE sur la table, vue de telephone en paysage.
//
// C'est une vraie carte (ScanCard), pas un medaillon : a 95 px et plus, le nom,
// le cout et les bulles de stats se lisent. Le texte de regles, lui, ne se lit
// pas a cette taille : le tap ouvre la carte en grand (CarteOuverte), et c'est
// de la qu'on agit. La carte ne recoit donc PAS son onSelect ici, mais garde
// son etat (cible, jouable, choisie) pour que le CSS l'allume ou l'eteigne.
//
// Ce qui s'attache a la carte :
//   - les ETATS (coriace, sonne, desoriente) en pastilles lettrees au coin :
//     une carte glissee derriere ne se lirait pas a cette taille ;
//   - les AMELIORATIONS glissees derriere le porteur, decalees vers la DROITE
//     de 14 px chacune. Vers le bas, elles sortiraient d'une rangee dont la
//     hauteur est fixe. La bande visible de chacune repond au tap.

import type { CSSProperties, KeyboardEvent } from 'react'
import { ScanCard, type CardEffectDelta, type ScanCardProps } from '../../components/ScanCard'
import type { UniteAffichee } from '../zones'
import { t } from '../langue'
import { separerAttachees } from './etats'
import './paysage.css'

export type CartePoseeProps = {
  unite: UniteAffichee
  /** Variation de compteur en cours : le nombre qui s'envole, rendu par ScanCard. */
  effet?: CardEffectDelta
  onOuvrir: (carte: ScanCardProps) => void
}

/** La carte telle qu'on la DESSINE : sans action directe, le tap ouvre d'abord. */
function sansAction(carte: ScanCardProps, effet?: CardEffectDelta): ScanCardProps {
  const { onSelect: _onSelect, ...reste } = carte
  return effet ? { ...reste, effectDelta: effet } : reste
}

export function CartePosee({ unite, effet, onOuvrir }: CartePoseeProps) {
  const { etats, ameliorations } = separerAttachees(unite.attachees)
  const carte = unite.carte
  const pastille = carte.allyHp ?? carte.schemeThreat

  const auClavier = (evenement: KeyboardEvent<HTMLDivElement>) => {
    if (evenement.key === 'Enter' || evenement.key === ' ') {
      evenement.preventDefault()
      onOuvrir(carte)
    }
  }

  return (
    <div
      className="carte-posee"
      role="button"
      tabIndex={0}
      data-tactile="carte"
      aria-label={`${carte.name}${pastille ? `, ${pastille}` : ''}`}
      style={{ '--nb': ameliorations.length } as CSSProperties}
      onClick={() => onOuvrir(carte)}
      onKeyDown={auClavier}
    >
      {ameliorations.map((amelioration, index) => (
        <span
          className="carte-posee-attachee"
          key={amelioration.id}
          style={{ '--i': index + 1 } as CSSProperties}
          onClick={(evenement) => {
            evenement.stopPropagation()
            onOuvrir(amelioration)
          }}
        >
          <ScanCard {...sansAction(amelioration)} />
        </span>
      ))}

      <ScanCard {...sansAction(carte, effet)} />

      {etats.length > 0 ? (
        <span className="carte-posee-etats">
          {etats.map((etat, index) => (
            <span className={`carte-posee-etat ${etat.classe}`} key={`${etat.classe}-${index}`} title={t(etat.nom)}>
              {etat.lettre}
            </span>
          ))}
        </span>
      ) : null}
    </div>
  )
}
