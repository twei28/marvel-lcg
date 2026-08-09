// Une rangée du mini-plateau : son libellé, puis ses médaillons.
//
// Les médaillons sont CENTRÉS tant qu'ils tiennent — c'est ce qui fait lire une
// table plutôt qu'une liste. Quand ils débordent, et seulement alors, la rangée
// devient balayable et s'aligne à gauche pour que le bord du médaillon suivant
// dépasse : ce bord est le seul signal qui dit qu'il y a une suite.
//
// Aucune autre rangée ne bouge. C'est la différence avec la version d'origine,
// qui repliait les bandes les moins urgentes dès que la place manquait — et
// vidait l'écran entier en paysage, où aucune n'avait la place.

import { Medaillon } from './Medaillon'
import type { CardEffectDelta, ScanCardProps } from '../../components/ScanCard'
import type { UniteAffichee } from '../zones'
import { t } from '../langue'
import './mobile.css'

export type RangeeProps = {
  titre: string
  unites: UniteAffichee[]
  /** « grand » pour la rangée qui porte la manigance principale. */
  taille?: 'normal' | 'grand'
  /** Nombre de cibles légales ici pendant un ciblage. */
  cibles?: number
  /** Variations de compteurs en cours, par identifiant de carte. */
  effets?: Map<number, CardEffectDelta>
  onOuvrirCarte: (carte: ScanCardProps) => void
}

export function RangeeMedaillons({
  titre,
  unites,
  taille = 'normal',
  cibles,
  effets,
  onOuvrirCarte,
}: RangeeProps) {
  return (
    <section className="rangee" aria-label={titre}>
      <div className="rangee-titre">
        <span className="rangee-nom">{titre}</span>
        {cibles ? (
          <span className="rangee-cibles" aria-label={`${cibles} ${t('cibles ici')}`}>
            {cibles}
          </span>
        ) : null}
      </div>
      <div className="rangee-medaillons">
        {unites.length === 0 ? (
          <span className="rangee-vide">{t('Vide')}</span>
        ) : (
          unites.map((unite) => (
            <Medaillon
              key={unite.cle}
              carte={unite.carte}
              attachees={unite.attachees}
              taille={taille}
              effet={effets?.get(Number(unite.carte.id))}
              onOuvrir={onOuvrirCarte}
            />
          ))
        )}
      </div>
    </section>
  )
}
