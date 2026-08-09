// Qui possede quoi dans l'emplacement `terrain-soutien`.
//
// zones.ts y aplatit les aires de TOUS les joueurs en groupes successifs, parce
// que le plateau PC les pose cote a cote. Sur un telephone, un seul joueur est
// deplie a la fois : il faut donc pouvoir recoudre les groupes par joueur.

import type { ScanCardProps } from '../../components/ScanCard'
import type { EmplacementAffiche, UniteAffichee } from '../zones'

/**
 * Les groupes ranges par joueur, dans l'ordre ou zones.ts les a produits.
 * Sans le champ `proprietaires` (partie solo, ou emplacement d'un autre type),
 * tout revient au joueur 0 : le comportement reste celui d'avant.
 */
export function groupesParJoueur(
  emplacement: EmplacementAffiche
): Map<number, UniteAffichee[][]> {
  const par = new Map<number, UniteAffichee[][]>()
  emplacement.groupes.forEach((groupe, index) => {
    const joueur = emplacement.proprietaires?.[index] ?? 0
    const deja = par.get(joueur)
    if (deja) deja.push(groupe)
    else par.set(joueur, [groupe])
  })
  return par
}

/** Le joueur actif d'abord, les autres dans leur ordre d'origine. */
export function ordreDAffichage(joueurs: number[], actif: number): number[] {
  if (!joueurs.includes(actif)) return joueurs
  return [actif, ...joueurs.filter((joueur) => joueur !== actif)]
}

/**
 * La carte d'identite d'un joueur : la premiere unite de ses groupes dont le
 * type est heros ou alter-ego. Absente si aucune ne correspond.
 *
 * Vivait dans BandeHeros, supprime avec le modele de condensation. ZoneFocus
 * etiquette ses sections de joueur avec exactement cette regle.
 */
export function carteIdentite(groupes: UniteAffichee[][]): ScanCardProps | undefined {
  for (const groupe of groupes) {
    for (const unite of groupe) {
      if (unite.carte.kind === 'hero' || unite.carte.kind === 'alter-ego') return unite.carte
    }
  }
  return undefined
}
