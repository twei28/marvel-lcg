// La repartition de la table en RONDS (decisions du 24/10/2026,
// .planning/todos/2026-10-24-plateau-telephone-ronds.md). Fonction pure : elle part des BANDES du portrait
// (`repartirEnBandes`, qui sait deja ou va chaque carte) et les range en trois rangees de deux zones :
//
//   Mechant      | Manigances (principale, annexes, environnement)
//   Allies       | Sbires
//   Heros        | Cartes en jeu (soutiens, ameliorations restantes)
//
// Rien n'est decide ici sur la taille ou le nombre de lignes : le CSS (ronds.css) laisse chaque zone passer
// a la ligne quand elle est pleine.
import type { ScanCardProps } from '../../../components/ScanCard'
import type { UniteAffichee } from '../../zones'
import type { BandesPortrait } from '../bandes-portrait'

export type CleZone = 'vilain' | 'manigances' | 'allies' | 'sbires' | 'heros' | 'enJeu'

/**
 * Plusieurs cartes d'une meme famille regroupees en UN rond (24/10/2026, The Big Apple sur telephone : la colonne des
 * manigances empilait cinq ronds et poussait le reste de la table hors de l'ecran) :
 * - `ville` : le lieu occupe (les neuf lieux se lisent dans l'onglet « Ville », que le toucher ouvre) ;
 * - `environnements` : les environnements permanents (The City, Never Sleeps), que le toucher etale.
 */
export type GroupeRond = {
  genre: 'ville' | 'environnements'
  titre: string
  cartes: ScanCardProps[]
}

export type UniteRond = UniteAffichee & { groupe?: GroupeRond }

export type ZoneRonds = {
  cle: CleZone
  titre: string
  unites: UniteRond[]
}

export type RangeeRonds = {
  cle: 'rangee-vilain' | 'rangee-allies' | 'rangee-heros'
  gauche: ZoneRonds
  droite: ZoneRonds
}

/** Les titres sont donnes par l'appelant (traduits par `t`), pour garder cette fonction pure. */
export type TitresRonds = Record<CleZone, string>

/** Les noms du rond « La ville » et du rond « Environnements » (donnes par l'appelant, traduits par `t`). */
export type LibellesGroupes = { ville: string; environnements: string }
const LIBELLES_PAR_DEFAUT: LibellesGroupes = { ville: 'La ville', environnements: 'Environnements' }

/** Un lieu de la ville MC×DC (« La ville ne dort jamais ») : un environnement `pu…` qui porte le trait LOCATION. */
function estUnLieu(unite: UniteAffichee): boolean {
  return /^pu/.test(unite.carte.codeCarte ?? '') && (unite.carte.traits ?? []).some((trait) => /^location$/i.test(trait))
}

/** Regroupe les environnements : les lieux en un rond « La ville », les environnements permanents en un rond quand il y en a deux ou plus. */
export function grouperLesEnvironnements(environnements: UniteAffichee[], libelles: LibellesGroupes = LIBELLES_PAR_DEFAUT): UniteRond[] {
  const lieux = environnements.filter(estUnLieu)
  const permanents = environnements.filter((unite) => !estUnLieu(unite))
  const sortie: UniteRond[] = []
  if (permanents.length >= 2) {
    sortie.push({
      ...permanents[0]!,
      cle: 'groupe-environnements',
      attachees: [],
      groupe: { genre: 'environnements', titre: libelles.environnements, cartes: permanents.map((u) => u.carte) },
    })
  } else {
    sortie.push(...permanents)
  }
  if (lieux.length > 0) {
    sortie.push({
      ...lieux[0]!,
      cle: 'groupe-ville',
      attachees: [],
      groupe: { genre: 'ville', titre: libelles.ville, cartes: lieux.map((u) => u.carte) },
    })
  }
  return sortie
}

const compte = (...zones: Array<UniteAffichee | undefined>): UniteAffichee[] =>
  zones.filter((unite): unite is UniteAffichee => unite !== undefined)

export function repartirEnRonds(bandes: BandesPortrait, titres: TitresRonds, libelles?: LibellesGroupes): RangeeRonds[] {
  const environnements = bandes.vilain.unites.filter((unite) => unite.carte.kind === 'environment')
  const autresMechants = bandes.vilain.unites.filter((unite) => unite.carte.kind !== 'environment')
  return [
    {
      cle: 'rangee-vilain',
      gauche: { cle: 'vilain', titre: titres.vilain, unites: [...compte(bandes.vilain.epinglee), ...autresMechants] },
      droite: {
        cle: 'manigances',
        titre: titres.manigances,
        unites: [...compte(bandes.manigances.epinglee), ...bandes.manigances.unites, ...grouperLesEnvironnements(environnements, libelles)],
      },
    },
    {
      cle: 'rangee-allies',
      gauche: { cle: 'allies', titre: titres.allies, unites: bandes.heros.unites },
      droite: { cle: 'sbires', titre: titres.sbires, unites: bandes.engages.unites },
    },
    {
      cle: 'rangee-heros',
      gauche: { cle: 'heros', titre: titres.heros, unites: compte(bandes.heros.epinglee) },
      droite: {
        cle: 'enJeu',
        titre: titres.enJeu,
        unites: [...bandes.soutiens.unites, ...bandes.ameliorations.unites],
      },
    },
  ]
}
