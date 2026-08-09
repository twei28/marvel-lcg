// Les 11 emplacements de zones.ts, ranges en rangees de medaillons.
//
// C'est une TABLE, pas une logique. Ajouter un emplacement dans zones.ts, c'est
// ajouter une entree ici : le test verifie qu'aucun ne reste orphelin.
//
// L'ordre est celui de LECTURE du plateau (la menace d'abord, ta main en
// dernier), pas celui dans lequel zones.ts les produit.
//
// Deux changements par rapport au decoupage d'origine :
//   - la ligne joueur est SEPAREE en deux, comme sur le plateau PC : la ligne de
//     combat (allies, sbires engages, environnement) au-dessus, puis la ligne
//     personnelle (heros, ameliorations, soutiens) juste au-dessus de la main ;
//   - les PILES (decks, defausses, victoire, mises de cote) sortent du plateau
//     pour le tiroir de gauche : deux zones entieres rendues aux medaillons.

import { t } from '../langue'
import type { CleEmplacement, EmplacementAffiche, Plateau } from '../zones'

export type CleBande =
  | 'vilain'
  | 'complots'
  | 'terrain'
  | 'heros'
  | 'main'
  /** Hors plateau : tiroir de gauche en portrait, colonne visible en paysage. */
  | 'piles'

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
  {
    cle: 'heros',
    titre: () => t('Ton héros'),
    // La Réserve (pack Brawn) suit le héros, à la même place que le deck
    // spécial d'un Doctor Strange : c'est sa zone personnelle.
    emplacements: ['terrain-soutien', 'deck-special', 'reserve', 'nemesis'],
  },
  { cle: 'main', titre: () => t('Ta main'), emplacements: ['main'] },
  {
    cle: 'piles',
    titre: () => t('Piles'),
    emplacements: ['piles-rencontre', 'piles-joueur', 'annexes'],
  },
]

/** Les rangees dessinees SUR le plateau, dans l'ordre, hors main et piles. */
export const BANDES_PLATEAU: CleBande[] = ['vilain', 'complots', 'terrain', 'heros']

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
