// Les cibles que la feuille de choix montre DANS la fenetre (maquette approuvee par l'utilisateur, 26/10/2026) : les memes
// ronds que sur la table, pour les cartes que le moteur propose de CHOISIR.
//
// - une carte au role `cible` entre dans la rangee, choisie ou non (on peut la retirer d'un toucher) ;
// - une amelioration ou un statut a choisir fait entrer sa carte PORTEUSE : le rond l'affiche en petit, comme sur la table ;
// - les apercus (`cible-preview`) ne sont pas des choix ; une carte n'apparait qu'une fois ;
// - une fois le nombre de cibles atteint, les AUTRES cibles legales ne sont plus « choisissables » : elles restent pourtant dans la
//   rangee (`ciblesLegales`, les cibles que le moteur a proposees), pour que le joueur voie ses options jusqu'a la validation ;
// - les cibles qui ne sont pas sur la table (le deck, la defausse) restent au selecteur a deux colonnes, pas ici.
import type { EtatInteractif } from '../interaction'
import type { Plateau, UniteAffichee } from '../zones'

function estUnChoix(id: string, interactifs: Map<number, EtatInteractif>, legales: ReadonlySet<number>): boolean {
  return interactifs.get(Number(id))?.role === 'cible' || legales.has(Number(id))
}

export function ciblesDeLaFeuille(
  plateau: Plateau,
  interactifs: Map<number, EtatInteractif>,
  ciblesLegales: readonly number[] = []
): UniteAffichee[] {
  const legales = new Set(ciblesLegales)
  const vus = new Set<string>()
  const sortie: UniteAffichee[] = []
  for (const emplacement of plateau.emplacements) {
    for (const groupe of emplacement.groupes) {
      for (const unite of groupe) {
        if (vus.has(unite.carte.id)) continue
        if (!estUnChoix(unite.carte.id, interactifs, legales) && !unite.attachees.some((a) => estUnChoix(a.id, interactifs, legales))) continue
        vus.add(unite.carte.id)
        sortie.push(unite)
      }
    }
  }
  return sortie
}
