// Quel emplacement de la table va dans quel bloc du portrait.
//
// Isole du rendu, et pur : c'est la seule chose qu'on peut se tromper sans
// qu'un test de composant ne le voie. Les six blocs sont TOUJOURS rendus, meme
// vides : le portrait ne defile pas, sa hauteur doit donc etre previsible d'un
// tour a l'autre — un bloc qui apparait ferait sauter tous les autres.
import type { CleEmplacement, Plateau, UniteAffichee } from '../zones'

export type CleBloc = 'vilain' | 'complot' | 'rencontre' | 'engages' | 'heros' | 'main'

export type BlocPortrait = {
  cle: CleBloc
  titre: string
  unites: UniteAffichee[]
}

/**
 * L'ordre est celui de l'ecran, de haut en bas.
 *
 * Verifie contre `construirePlateau` (zones.ts) le 11/09/2026 : c'etait la
 * source du defaut majeur ou le mechant ne s'affichait NULLE PART. `vilain`
 * pointait vers `terrain-combat` (en realite les allies/sbires/environnement)
 * et `rencontre` pointait vers l'emplacement `rencontre` qui est en realite
 * `airesVilains(world)` — LE MECHANT. Les deux etaient inverses.
 *
 * `terrain-soutien` n'est PAS une cle morte (contrairement a ce qu'un plan
 * anterieur affirmait) : zones.ts la construit bel et bien, avec l'identite
 * du heros (`area_hero`), ses soutiens et ses obligations. C'est elle qui
 * porte la carte d'identite.
 *
 * `terrain-combat` n'apparait dans AUCUNE ligne ci-dessous : c'est le seul
 * emplacement de zones.ts qui melange deux camps (allies du joueur ET sbires
 * ennemis engages, plus l'environnement) dans les MEMES groupes — voir son
 * commentaire dans zones.ts. Il se demele plus bas, carte par carte, sur son
 * `kind` : un allie va avec le heros, le reste (sbire, environnement) reste
 * avec les engages.
 */
const BLOCS: Array<{ cle: CleBloc; titre: string; emplacements: CleEmplacement[] }> = [
  { cle: 'vilain', titre: 'Méchant', emplacements: ['rencontre'] },
  { cle: 'complot', titre: 'Manigances', emplacements: ['complot-principal', 'complots-secondaires'] },
  { cle: 'rencontre', titre: 'Rencontre', emplacements: ['piles-rencontre'] },
  { cle: 'engages', titre: 'Engagés', emplacements: ['nemesis', 'annexes'] },
  {
    cle: 'heros',
    titre: 'Ton héros',
    // `deck-special` (Invocation de Strange...) se pose a cote du heros sur la
    // vraie table (zones.ts, commentaire de l'emplacement) : il n'a rien a
    // faire dans « Rencontre », ou il finissait ignore (PlateauPortrait ne
    // lit de ce bloc que les deux compteurs de pile de rencontre).
    emplacements: ['terrain-soutien', 'deck-special', 'reserve', 'piles-joueur'],
  },
  { cle: 'main', titre: 'Ta main', emplacements: ['main'] },
]

export function repartirEnBlocs(plateau: Plateau): BlocPortrait[] {
  const parEmplacement = (cle: CleEmplacement): UniteAffichee[] =>
    plateau.emplacements
      .filter((emplacement) => emplacement.cle === cle)
      .flatMap((emplacement) => emplacement.groupes.flat())

  // Demelage de terrain-combat : seule la pastille `kind` de la carte dit
  // encore de quel camp elle vient une fois les groupes aplatis.
  const combat = parEmplacement('terrain-combat')
  const alliesDuHeros = combat.filter((unite) => unite.carte.kind === 'ally')
  const sbiresEtEnvironnement = combat.filter((unite) => unite.carte.kind !== 'ally')

  return BLOCS.map(({ cle, titre, emplacements }) => ({
    cle,
    titre,
    unites: [
      ...emplacements.flatMap(parEmplacement),
      ...(cle === 'heros' ? alliesDuHeros : []),
      ...(cle === 'engages' ? sbiresEtEnvironnement : []),
    ],
  }))
}
