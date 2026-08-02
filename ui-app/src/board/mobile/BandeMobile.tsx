// Une bande de la vue d'etat : un titre, des tuiles condensees, et une pastille
// « +N » quand le budget ne suffit pas. La pastille ouvre la bande en focus :
// c'est la seule facon d'atteindre ce qui est replie, elle n'est jamais decorative.

import { t } from '../langue'
import type { ScanCardProps } from '../../components/ScanCard'
import type { BandeAffichee } from './bandes'
import { condenser, type BudgetBande } from './condensation'
import { TuileCondensee } from './TuileCondensee'
import './mobile.css'

export type BandeMobileProps = {
  bande: BandeAffichee
  budget: BudgetBande
  onOuvrirBande: () => void
  onOuvrirCarte: (carte: ScanCardProps) => void
}

export function BandeMobile({
  bande,
  budget,
  onOuvrirBande,
  onOuvrirCarte,
}: BandeMobileProps) {
  const unites = bande.emplacements.flatMap((emplacement) => emplacement.groupes.flat())
  const { tuiles, restantes, taille } = condenser(unites, budget)

  return (
    <section className="bande" aria-label={bande.titre}>
      <h2 className="bande-titre">{bande.titre}</h2>
      <div className="bande-tuiles">
        {tuiles.map((unite) => (
          <TuileCondensee
            key={unite.cle}
            carte={unite.carte}
            taille={taille}
            onOuvrir={() => onOuvrirCarte(unite.carte)}
          />
        ))}
        {restantes > 0 ? (
          <button
            type="button"
            className="bande-surplus"
            onClick={onOuvrirBande}
            data-tactile="surplus"
            aria-label={`+${restantes} ${t('autres')}`}
          >
            +{restantes}
          </button>
        ) : null}
      </div>
    </section>
  )
}
