// Le niveau 2 : une bande ouverte en feuille par-dessus la vue d'etat, cartes a
// 149 px de large. C'est la qu'on lit et qu'on agit.
//
// 149 px vient du calcul de la spec : a 480 px de large, (480 - 20 de marges
// - 12 d'ecarts) / 3 = 149. Trois cartes par rangee, chacune tres au-dessus des
// 44 px de cible tactile.

import { t } from '../langue'
import { ScanCard, type ScanCardProps } from '../../components/ScanCard'
import type { BandeAffichee } from './bandes'
import './mobile.css'

export type ZoneFocusProps = {
  bande: BandeAffichee
  onFermer: () => void
  onOuvrirCarte: (carte: ScanCardProps) => void
}

export function ZoneFocus({ bande, onFermer, onOuvrirCarte }: ZoneFocusProps) {
  return (
    <div className="focus-voile" onPointerDown={onFermer}>
      <section
        className="focus"
        role="dialog"
        aria-label={bande.titre}
        onPointerDown={(evenement) => evenement.stopPropagation()}
      >
        <header className="focus-entete">
          <span className="focus-poignee" aria-hidden="true" />
          <h2>{bande.titre}</h2>
          <button type="button" className="focus-fermer" onClick={onFermer} data-tactile="fermer">
            {t('Fermer')}
          </button>
        </header>
        <div className="focus-cartes">
          {bande.emplacements.flatMap((emplacement) =>
            emplacement.groupes.flat().map((unite) => (
              <ScanCard
                key={unite.cle}
                {...unite.carte}
                onSelect={() => onOuvrirCarte(unite.carte)}
              />
            ))
          )}
        </div>
      </section>
    </div>
  )
}
