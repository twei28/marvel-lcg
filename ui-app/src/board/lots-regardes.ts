// QUELLES CARTES REGARDEES L'UTILISATEUR A DEJA FERMEES (rapport du 29/10/2026, Gambit 48021).
//
// La fenetre « Cartes regardees » retenait le LOT EXACT qu'on venait de fermer, dans un etat local du composant. Or ce
// composant n'est monte que lorsqu'aucune fenetre de choix n'est ouverte (`board.tsx`) : chaque choix, chaque cible, le
// demontait et lui faisait perdre sa memoire. Gambit regarde 3 cartes du deck rencontre et en glisse une : les 2 autres
// restent « regardees » (le moteur n'oublie un regard qu'au changement de zone ou au melange), donc la fenetre se rouvrait
// a chaque nouveau choix, avec deux cartes, comme si on devait en rechoisir une.
//
// Deux regles, toutes deux pures :
//  - la memoire vit chez le PARENT, qui reste monte (un choix ne l'efface plus) ;
//  - un lot dont TOUTES les cartes ont deja ete fermees est un lot deja vu, meme s'il est plus petit qu'avant (3 cartes
//    fermees, puis 2 restantes : rien de nouveau a montrer). Une carte jamais montree rouvre la fenetre.

export type CarteRegardeeVue = { id: string }
export type GroupeRegarde = { cartes: readonly CarteRegardeeVue[] }

/** Les identifiants de toutes les cartes des groupes, a plat. */
export function idsRegardes(groupes: readonly GroupeRegarde[]): string[] {
  return groupes.flatMap((groupe) => groupe.cartes.map((carte) => carte.id))
}

/** Rien de nouveau a montrer : le lot est vide, ou chacune de ses cartes a deja ete fermee. */
export function lotDejaVu(ids: readonly string[], vues: ReadonlySet<string>): boolean {
  return ids.every((id) => vues.has(id))
}

/** La memoire apres une fermeture : une NOUVELLE table, l'ancienne n'est pas modifiee. */
export function avecVues(vues: ReadonlySet<string>, ids: readonly string[]): Set<string> {
  const suite = new Set(vues)
  for (const id of ids) suite.add(id)
  return suite
}
