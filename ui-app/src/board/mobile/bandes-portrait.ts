// La repartition du plateau en BANDES pour le portrait (spec du 12/09/2026,
// docs/superpowers/specs/2026-09-12-plateau-portrait-en-bandes-design.md).
//
// Quatre bandes de haut en bas (mechant, manigances, engages, mon heros), la
// main a part (elle vit derriere l'encoche de droite) et les piles a part
// (derriere l'encoche de gauche). Fonction pure : aucun rendu ici.
//
// Verifie contre `construirePlateau` (zones.ts) : `rencontre` est LE mechant
// (airesVilains), `terrain-combat` melange allies, sbires engages et
// environnement dans les memes groupes (le seul emplacement a deux camps), et
// `terrain-soutien` porte l'identite, les soutiens et les obligations.
import type { CleEmplacement, EmplacementAffiche, Plateau, UniteAffichee } from '../zones'

export type PileAffichee = {
  /** La cle de l'unite (`joueur-deck`, `rencontre-encounter-discard`...), jamais son nom. */
  cle: string
  titre: string
  unite: UniteAffichee
  compte?: number
}

export type BandePortrait = {
  /** La carte fixe au bord gauche de la bande pendant le defilement. */
  epinglee?: UniteAffichee
  unites: UniteAffichee[]
}

export type BandesPortrait = {
  vilain: BandePortrait
  manigances: BandePortrait
  engages: BandePortrait
  heros: BandePortrait
  main: UniteAffichee[]
  piles: PileAffichee[]
}

const IDENTITES = new Set(['hero', 'alter-ego'])
const EMPLACEMENTS_DE_PILES: CleEmplacement[] = ['piles-joueur', 'piles-rencontre', 'nemesis', 'annexes']
const EMPLACEMENTS_SPECIAUX: CleEmplacement[] = ['deck-special', 'reserve']

/** Une pile : elle se consulte (`pileContenu`) ou au moins se compte (`pileCount`). */
export function estUnePile(unite: UniteAffichee): boolean {
  return unite.pileContenu !== undefined || unite.carte.pileCount !== undefined
}

function versPile(unite: UniteAffichee): PileAffichee {
  return {
    cle: unite.cle,
    titre: unite.pileTitre ?? unite.carte.name,
    unite,
    compte: unite.carte.pileCount ?? unite.pileContenu?.length,
  }
}

export function repartirEnBandes(plateau: Plateau): BandesPortrait {
  const emplacements = (cle: CleEmplacement): EmplacementAffiche[] =>
    plateau.emplacements.filter((emplacement) => emplacement.cle === cle)
  const unites = (cle: CleEmplacement): UniteAffichee[] =>
    emplacements(cle).flatMap((emplacement) => emplacement.groupes.flat())

  const combat = unites('terrain-combat')
  const rencontre = unites('rencontre')
  const soutien = unites('terrain-soutien')
  const identite = soutien.find((unite) => IDENTITES.has(unite.carte.kind))
  const speciaux = EMPLACEMENTS_SPECIAUX.flatMap(unites)

  const piles: PileAffichee[] = [
    ...EMPLACEMENTS_DE_PILES.flatMap(unites).map(versPile),
    ...speciaux.filter(estUnePile).map(versPile),
  ]

  return {
    vilain: {
      epinglee: rencontre[0],
      unites: [...rencontre.slice(1), ...combat.filter((unite) => unite.carte.kind === 'environment')],
    },
    manigances: {
      epinglee: unites('complot-principal')[0],
      unites: unites('complots-secondaires'),
    },
    engages: {
      unites: combat.filter((unite) => unite.carte.kind !== 'ally' && unite.carte.kind !== 'environment'),
    },
    heros: {
      epinglee: identite,
      unites: [
        ...soutien.filter((unite) => unite !== identite),
        ...combat.filter((unite) => unite.carte.kind === 'ally'),
        ...speciaux.filter((unite) => !estUnePile(unite)),
      ],
    },
    main: unites('main'),
    piles,
  }
}
