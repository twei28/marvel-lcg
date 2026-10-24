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
import type { UniteAffichee } from '../../zones'
import type { BandesPortrait } from '../bandes-portrait'

export type CleZone = 'vilain' | 'manigances' | 'allies' | 'sbires' | 'heros' | 'enJeu'

export type ZoneRonds = {
  cle: CleZone
  titre: string
  unites: UniteAffichee[]
}

export type RangeeRonds = {
  cle: 'rangee-vilain' | 'rangee-allies' | 'rangee-heros'
  gauche: ZoneRonds
  droite: ZoneRonds
}

/** Les titres sont donnes par l'appelant (traduits par `t`), pour garder cette fonction pure. */
export type TitresRonds = Record<CleZone, string>

const compte = (...zones: Array<UniteAffichee | undefined>): UniteAffichee[] =>
  zones.filter((unite): unite is UniteAffichee => unite !== undefined)

export function repartirEnRonds(bandes: BandesPortrait, titres: TitresRonds): RangeeRonds[] {
  const environnements = bandes.vilain.unites.filter((unite) => unite.carte.kind === 'environment')
  const autresMechants = bandes.vilain.unites.filter((unite) => unite.carte.kind !== 'environment')
  return [
    {
      cle: 'rangee-vilain',
      gauche: { cle: 'vilain', titre: titres.vilain, unites: [...compte(bandes.vilain.epinglee), ...autresMechants] },
      droite: {
        cle: 'manigances',
        titre: titres.manigances,
        unites: [...compte(bandes.manigances.epinglee), ...bandes.manigances.unites, ...environnements],
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
