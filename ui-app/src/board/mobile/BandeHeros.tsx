// La bande Heros : contrairement aux cinq autres bandes, un seul joueur y est
// deplie a la fois (spec S7). Seul terrain-soutien se decoupe par proprietaire
// (les aires de tous les joueurs y sont aplaties par zones.ts) ; les autres
// emplacements de la bande (deck special, piles, nemesis, annexes) n'existent
// que pour le siege regarde et restent toujours affiches sous le joueur
// deplie, quel qu'il soit.

import { useState } from 'react'
import { t } from '../langue'
import type { ScanCardProps } from '../../components/ScanCard'
import type { UniteAffichee } from '../zones'
import type { BandeAffichee } from './bandes'
import { condenser, type BudgetBande } from './condensation'
import { groupesParJoueur, ordreDAffichage } from './joueurs'
import { TuileCondensee } from './TuileCondensee'
import './mobile.css'

export type BandeHerosProps = {
  bande: BandeAffichee
  budget: BudgetBande
  /** Siege regarde : c'est le joueur deplie par defaut. */
  playerId: number
  onOuvrirBande: () => void
  onOuvrirCarte: (carte: ScanCardProps) => void
}

/**
 * La carte d'identite d'un joueur : la premiere unite de ses groupes dont le
 * type est hero ou alter-ego. Absente si aucune ne correspond (bandeau replie
 * de secours, voir plus bas).
 */
function carteIdentite(groupes: UniteAffichee[][]): ScanCardProps | undefined {
  for (const groupe of groupes) {
    for (const unite of groupe) {
      if (unite.carte.kind === 'hero' || unite.carte.kind === 'alter-ego') return unite.carte
    }
  }
  return undefined
}

export function BandeHeros({ bande, budget, playerId, onOuvrirBande, onOuvrirCarte }: BandeHerosProps) {
  const [joueurDeplie, setJoueurDeplie] = useState(playerId)

  const soutien = bande.emplacements.find((emplacement) => emplacement.cle === 'terrain-soutien')
  const groupesParProprietaire = soutien
    ? groupesParJoueur(soutien)
    : new Map<number, UniteAffichee[][]>()
  const joueurs = [...groupesParProprietaire.keys()]
  const ordre = ordreDAffichage(joueurs, joueurDeplie)
  const autresJoueurs = ordre.filter((joueur) => joueur !== joueurDeplie)

  const unitesTerrainSoutien = (groupesParProprietaire.get(joueurDeplie) ?? []).flat()
  const unitesAutresEmplacements = bande.emplacements
    .filter((emplacement) => emplacement.cle !== 'terrain-soutien')
    .flatMap((emplacement) => emplacement.groupes.flat())
  const unites = [...unitesTerrainSoutien, ...unitesAutresEmplacements]

  const { tuiles, restantes, taille } = condenser(unites, budget)

  return (
    <section className="bande" aria-label={bande.titre}>
      <button
        type="button"
        className="bande-titre"
        onClick={onOuvrirBande}
        data-tactile="titre-bande"
      >
        {bande.titre}
      </button>
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
      {autresJoueurs.map((joueur) => {
        const identite = carteIdentite(groupesParProprietaire.get(joueur) ?? [])
        const nom = identite?.name ?? `${t('Joueur')} ${joueur}`
        return (
          <button
            key={joueur}
            type="button"
            className="bandeau-joueur"
            data-tactile="joueur-replie"
            onClick={() => setJoueurDeplie(joueur)}
          >
            <span className="bandeau-joueur-nom">{nom}</span>
            {identite?.allyHp ? <span className="bandeau-joueur-pv">{identite.allyHp}</span> : null}
            {(identite?.counters ?? []).map((compteur) => (
              <span className="bandeau-joueur-compteur" key={compteur.label}>
                {compteur.label} {compteur.value}
              </span>
            ))}
          </button>
        )
      })}
    </section>
  )
}
