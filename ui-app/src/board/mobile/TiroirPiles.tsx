// Le tiroir des piles, au bord gauche.
//
// Les decks et les défausses occupaient deux zones entières du plateau PC
// (piles-rencontre et piles-joueur). Sur un téléphone, c'est la place de deux
// rangées de médaillons pour une information qu'on consulte rarement. Elles
// vivent donc ici, à un balayage depuis le bord — avec une languette visible,
// parce qu'un geste que rien n'annonce n'est découvert par personne.
//
// En PAYSAGE, le tiroir ne sert pas : la largeur permet une colonne de piles
// visible en permanence, comme sur le plateau PC. PlateauMobile ne monte donc
// ce composant qu'en portrait.

import { useState } from 'react'
import type { ScanCardProps } from '../../components/ScanCard'
import type { UniteAffichee } from '../zones'
import { t } from '../langue'
import './mobile.css'

export type PileAffichee = {
  cle: string
  titre: string
  unite: UniteAffichee
  /** Nombre de cartes, quand le moteur le donne. */
  compte?: number
}

export type TiroirPilesProps = {
  piles: PileAffichee[]
  /** Étaler une pile publique pour la consulter. */
  onOuvrirPile: (titre: string, cartes: ScanCardProps[]) => void
}

export function TiroirPiles({ piles, onOuvrirPile }: TiroirPilesProps) {
  const [ouvert, setOuvert] = useState(false)

  return (
    <>
      <button
        type="button"
        className={`tiroir-languette${ouvert ? ' est-ouvert' : ''}`}
        onClick={() => setOuvert((etat) => !etat)}
        data-tactile="tiroir"
        aria-expanded={ouvert}
        aria-label={t('Piles')}
      >
        <span aria-hidden="true">{ouvert ? '‹' : '›'}</span>
      </button>

      {ouvert ? (
        <>
          <div className="tiroir-voile" onPointerDown={() => setOuvert(false)} />
          <aside className="tiroir" aria-label={t('Piles')}>
            <h2 className="tiroir-titre">{t('Piles')}</h2>
            <ul className="tiroir-liste">
              {piles.map((pile) => {
                const contenu = pile.unite.pileContenu
                const consultable = contenu !== undefined && contenu.length > 0
                return (
                  <li key={pile.cle}>
                    <button
                      type="button"
                      className="tiroir-pile"
                      disabled={!consultable}
                      onClick={() => {
                        if (consultable) onOuvrirPile(pile.unite.pileTitre ?? pile.titre, contenu)
                      }}
                    >
                      <span className="tiroir-pile-nom">{pile.titre}</span>
                      <span className="tiroir-pile-compte">{pile.compte ?? contenu?.length ?? 0}</span>
                    </button>
                  </li>
                )
              })}
            </ul>
          </aside>
        </>
      ) : null}
    </>
  )
}
