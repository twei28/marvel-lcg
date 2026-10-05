// Le TIROIR des piles, derriere l'encoche de gauche (spec du 12/09/2026) :
// un panneau lateral, une pile par ligne (dos ou derniere carte, nom,
// compte). Un tap sur une pile consultable l'etale dans la modale « cartes
// regardees » du plateau PC. Deck, defausse, rencontre, nemesis, cartes
// ecartees, deck special : tout ce qu'on ne regarde presque jamais.
//
// Les piles sont reperees par leur CLE (zones.ts), jamais par leur nom : le
// nom d'une pile est celui de sa carte du dessus (« Rhino »...).
import type { ReactElement } from 'react'
import { ScanCard, type ScanCardProps } from '../../components/ScanCard'
import { t } from '../langue'
import type { GroupeDePile } from '../zones'
import type { PileAffichee } from './bandes-portrait'

const LIBELLES: Record<string, string> = {
  'joueur-deck': 'Ton deck',
  'joueur-defausse': 'Ta défausse',
  'rencontre-encounter-deck': 'Deck rencontre',
  'rencontre-encounter-discard': 'Défausse rencontre',
  'nemesis-set': 'Némésis',
  'annexes-visibles': 'Cartes visibles',
  'annexes-cachees': 'Cartes cachées',
  'soutien-deck': 'Deck spécial',
  'soutien-defausse': 'Défausse spéciale',
}

export function libelleDePile(pile: PileAffichee): string {
  const connu = LIBELLES[pile.cle]
  return connu ? t(connu) : pile.titre
}

export function TiroirPiles({
  piles,
  ouvert,
  onFermer,
  onOuvrirPile,
}: {
  piles: PileAffichee[]
  ouvert: boolean
  onFermer: () => void
  /** Étaler une pile publique pour la consulter. */
  onOuvrirPile: (titre: string, cartes: ScanCardProps[], groupes?: GroupeDePile[]) => void
}): ReactElement | null {
  if (!ouvert) return null
  return (
    <>
      <div className="tiroir-voile" onPointerDown={onFermer} />
      <aside className="tiroir" aria-label={t('Piles')}>
        <h2 className="tiroir-titre">{t('Piles')}</h2>
        {piles.length === 0 ? <p className="portrait-vide">{t('Aucune pile')}</p> : null}
        <ul className="tiroir-liste">
          {piles.map((pile) => {
            const contenu = pile.unite.pileContenu
            const consultable =
              contenu !== undefined &&
              (contenu.length > 0 || pile.unite.pileGroupes?.some((groupe) => groupe.masque !== undefined) === true)
            const libelle = libelleDePile(pile)
            return (
              <li key={pile.cle}>
                <button
                  type="button"
                  className="tiroir-pile"
                  data-tactile="pile"
                  disabled={!consultable}
                  onClick={() => {
                    if (!consultable) return
                    onOuvrirPile(pile.unite.pileTitre ?? libelle, contenu, pile.unite.pileGroupes)
                    onFermer()
                  }}
                >
                  <span className="tiroir-pile-vignette">
                    <ScanCard {...pile.unite.carte} onSelect={undefined} highlight={false} pileCount={undefined} masquerType />
                  </span>
                  <span className="tiroir-pile-nom">{libelle}</span>
                  {pile.compte !== undefined ? <span className="tiroir-pile-compte">{pile.compte}</span> : null}
                </button>
              </li>
            )
          })}
        </ul>
        <button type="button" className="tiroir-fermer" onClick={onFermer}>
          {t('Fermer')}
        </button>
      </aside>
    </>
  )
}
