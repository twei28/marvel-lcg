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

/** L'ordre est celui de l'ecran, de haut en bas. */
const BLOCS: Array<{ cle: CleBloc; titre: string; emplacements: CleEmplacement[] }> = [
  { cle: 'vilain', titre: 'Méchant', emplacements: ['terrain-combat'] },
  { cle: 'complot', titre: 'Manigances', emplacements: ['complot-principal', 'complots-secondaires'] },
  { cle: 'rencontre', titre: 'Rencontre', emplacements: ['piles-rencontre', 'rencontre', 'deck-special'] },
  { cle: 'engages', titre: 'Engagés', emplacements: ['nemesis', 'annexes'] },
  { cle: 'heros', titre: 'Ton héros', emplacements: ['terrain-soutien', 'reserve', 'piles-joueur'] },
  { cle: 'main', titre: 'Ta main', emplacements: ['main'] },
]

export function repartirEnBlocs(plateau: Plateau): BlocPortrait[] {
  return BLOCS.map(({ cle, titre, emplacements }) => ({
    cle,
    titre,
    unites: emplacements.flatMap((voulu) =>
      plateau.emplacements
        .filter((emplacement) => emplacement.cle === voulu)
        .flatMap((emplacement) => emplacement.groupes.flat())
    ),
  }))
}
