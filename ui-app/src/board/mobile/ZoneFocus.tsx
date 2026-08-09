// Le niveau 2 : une bande ouverte en feuille par-dessus la vue d'etat, cartes a
// 149 px de large. C'est la qu'on lit et qu'on agit.
//
// 149 px vient du calcul de la spec : a 480 px de large, (480 - 20 de marges
// - 12 d'ecarts) / 3 = 149. Trois cartes par rangee, chacune tres au-dessus des
// 44 px de cible tactile.
//
// La bande Heros se decoupe PAR JOUEUR, comme dans la vue d'etat (spec S7) :
// aplatie, elle donnait une grille indifferenciee des identites, allies,
// ameliorations et soutiens de tout le monde, sans dire a qui appartient quoi.

import { t } from '../langue'
import { ScanCard, type ScanCardProps } from '../../components/ScanCard'
import type { UniteAffichee } from '../zones'
import type { BandeAffichee } from './bandes'

import { carteIdentite, groupesParJoueur, ordreDAffichage } from './joueurs'
import './mobile.css'

export type ZoneFocusProps = {
  bande: BandeAffichee
  /** Siege regarde : sa section vient en premier, comme dans la vue d'etat. */
  playerId: number
  onFermer: () => void
  onOuvrirCarte: (carte: ScanCardProps) => void
}

/** Une section titree de la feuille. Sans titre, les cartes sont posees a plat. */
type Section = { titre?: string; unites: UniteAffichee[] }

/**
 * Les sections de la feuille. Pour la bande Heros, une section par joueur :
 * son terrain-soutien, et pour le siege regarde ses emplacements propres
 * (deck special, piles, nemesis, annexes), que zones.ts ne produit que pour lui.
 * Pour toutes les autres bandes, une seule section sans titre : le titre de la
 * feuille suffit deja.
 */
export function sections(bande: BandeAffichee, playerId: number): Section[] {
  const soutien = bande.emplacements.find((emplacement) => emplacement.cle === 'terrain-soutien')
  const propres = bande.emplacements
    .filter((emplacement) => emplacement.cle !== 'terrain-soutien')
    .flatMap((emplacement) => emplacement.groupes.flat())

  if (bande.cle !== 'heros' || !soutien) {
    return [{ unites: [...propres, ...(soutien?.groupes.flat() ?? [])] }]
  }

  const parProprietaire = groupesParJoueur(soutien)
  return ordreDAffichage([...parProprietaire.keys()], playerId).map((joueur) => {
    const groupes = parProprietaire.get(joueur) ?? []
    const identite = carteIdentite(groupes)
    return {
      titre: identite?.name ?? `${t('Joueur')} ${joueur}`,
      unites: [...groupes.flat(), ...(joueur === playerId ? propres : [])],
    }
  })
}

export function ZoneFocus({ bande, playerId, onFermer, onOuvrirCarte }: ZoneFocusProps) {
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
        <div className="focus-corps">
          {sections(bande, playerId).map((section, index) => (
            <section className="focus-section" key={section.titre ?? `section-${index}`}>
              {section.titre ? <h3 className="focus-section-titre">{section.titre}</h3> : null}
              <div className="focus-cartes">
                {section.unites.map((unite) => (
                  <ScanCard
                    key={unite.cle}
                    {...unite.carte}
                    onSelect={() => onOuvrirCarte(unite.carte)}
                  />
                ))}
              </div>
            </section>
          ))}
        </div>
      </section>
    </div>
  )
}
