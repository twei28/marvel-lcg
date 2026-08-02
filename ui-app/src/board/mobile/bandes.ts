// Les 11 emplacements de zones.ts, ranges en 6 bandes lisibles sur un telephone.
//
// C'est une TABLE, pas une logique. Ajouter un emplacement dans zones.ts, c'est
// ajouter une entree ici : le test verifie qu'aucun ne reste orphelin.
//
// L'ordre des bandes est l'ordre de LECTURE du plateau (la menace d'abord, ta
// main en dernier), pas l'ordre dans lequel zones.ts les produit.

import { t } from '../langue'
import type { CleEmplacement, EmplacementAffiche, Plateau } from '../zones'

export type CleBande = 'vilain' | 'complots' | 'terrain' | 'rencontre' | 'heros' | 'main'

export const BANDES: Array<{
  cle: CleBande
  titre: () => string
  emplacements: CleEmplacement[]
}> = [
  { cle: 'vilain', titre: () => t('Méchant'), emplacements: ['rencontre'] },
  {
    cle: 'complots',
    titre: () => t('Manigances'),
    emplacements: ['complot-principal', 'complots-secondaires'],
  },
  { cle: 'terrain', titre: () => t('Terrain'), emplacements: ['terrain-combat'] },
  { cle: 'rencontre', titre: () => t('Rencontre'), emplacements: ['piles-rencontre'] },
  {
    cle: 'heros',
    titre: () => t('Héros'),
    emplacements: ['terrain-soutien', 'deck-special', 'piles-joueur', 'nemesis', 'annexes'],
  },
  { cle: 'main', titre: () => t('Ta main'), emplacements: ['main'] },
]

export type BandeAffichee = {
  cle: CleBande
  titre: string
  emplacements: EmplacementAffiche[]
}

/** Les bandes reellement peuplees, dans l'ordre de lecture. */
export function repartir(plateau: Plateau): BandeAffichee[] {
  const parCle = new Map<CleEmplacement, EmplacementAffiche>()
  for (const emplacement of plateau.emplacements) parCle.set(emplacement.cle, emplacement)

  return BANDES.map((bande) => ({
    cle: bande.cle,
    titre: bande.titre(),
    emplacements: bande.emplacements
      .map((cle) => parCle.get(cle))
      .filter((emplacement): emplacement is EmplacementAffiche => emplacement !== undefined),
  })).filter((bande) => bande.emplacements.length > 0)
}
