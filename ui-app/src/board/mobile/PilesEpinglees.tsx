// Les piles au bout d'une rangee : deck et defausse, en dos de carte reduit.
//
// Elles sont EPINGLEES a droite, hors du defilement de la rangee : on sait
// toujours ou elles sont, et ce qu'il reste dedans. Une pile consultable (la
// defausse, la victoire) s'etale au tap ; un deck reste secret et ne repond
// pas, sans pour autant disparaitre : son compte est une information de jeu.

import type { KeyboardEvent } from 'react'
import { ScanCard, type ScanCardProps } from '../../components/ScanCard'
import type { UniteAffichee } from '../zones'
import './paysage.css'

export type PilesEpingleesProps = {
  piles: UniteAffichee[]
  onOuvrirPile: (titre: string, cartes: ScanCardProps[]) => void
}

function compteDe(unite: UniteAffichee): number {
  return unite.carte.pileCount ?? unite.pileContenu?.length ?? 0
}

export function PilesEpinglees({ piles, onOuvrirPile }: PilesEpingleesProps) {
  return (
    <div className="piles-epinglees">
      {piles.map((unite) => {
        const titre = unite.pileTitre ?? unite.carte.name
        const contenu = unite.pileContenu
        const consultable = contenu !== undefined && contenu.length > 0
        const ouvrir = () => {
          if (consultable) onOuvrirPile(titre, contenu)
        }
        const auClavier = (evenement: KeyboardEvent<HTMLDivElement>) => {
          if (evenement.key === 'Enter' || evenement.key === ' ') {
            evenement.preventDefault()
            ouvrir()
          }
        }
        // pileCount n'est pas transmis a ScanCard : le compte affiche est
        // celui de .pile-epinglee-compte ci-dessous, pas le badge interne de
        // ScanCard (double affichage sinon, voir PilesEpinglees.test.tsx).
        const { onSelect: _onSelect, pileCount: _pileCount, ...carte } = unite.carte
        return (
          <div
            className={`pile-epinglee${consultable ? '' : ' est-secrete'}`}
            role="button"
            tabIndex={0}
            aria-disabled={consultable ? undefined : true}
            aria-label={`${titre}, ${compteDe(unite)}`}
            data-tactile="pile"
            key={unite.cle}
            onClick={ouvrir}
            onKeyDown={auClavier}
          >
            <ScanCard {...carte} />
            <span className="pile-epinglee-compte">{compteDe(unite)}</span>
            <span className="pile-epinglee-nom">{titre}</span>
          </div>
        )
      })}
    </div>
  )
}
