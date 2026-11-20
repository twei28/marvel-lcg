// L'ETAT DE LA VILLE pour l'onglet « Ville » : fonctions PURES, sans React. Decisions de l'utilisateur du 22/10/2026 :
// .planning/mcdc-punisher/decisions-interface-ville.md.
import type { Option } from './ask'
import type { VilleCase, VilleExport, VilleJoueur, VilleLigne, World } from './world'

/** La ville exportee, ou `undefined` hors de la campagne (le champ est un dictionnaire vide). */
export function villeDuMonde(monde: World | undefined): VilleExport | undefined {
  const v = monde?.ville
  if (!v || !v.cases || v.cases.length === 0) return undefined
  return { lignes: v.lignes ?? [], cases: v.cases, joueurs: v.joueurs ?? [] }
}

/** Les rangees dans l'ordre d'affichage : Uptown (-1) au-dessus, puis 0, 1, 2. */
export function lignesOrdonnees(ville: VilleExport): VilleLigne[] {
  return [...ville.lignes].sort((a, b) => a.ligne - b.ligne)
}

export function casesDeLaLigne(ville: VilleExport, ligne: number): VilleCase[] {
  return ville.cases.filter((c) => c.ligne === ligne).sort((a, b) => a.colonne - b.colonne)
}

export function positionDuJoueur(ville: VilleExport, playerId: number): VilleJoueur | undefined {
  return ville.joueurs.find((j) => j.player_id === playerId)
}

/** L'option « Move » (se deplacer) du moteur, quand elle est offerte au joueur : `undefined` hors de son tour. */
export function optionSeDeplacer(options: readonly Option[] | undefined): Option | undefined {
  return options?.find((o) => o.name.replaceAll('_', ' ').trim() === 'Move' && !o.failure_reason)
}

/** Les cases ou le joueur peut se deplacer MAINTENANT : celles que le moteur donne comme cibles legales de « Move ». */
export function casesAtteignables(ville: VilleExport, option: Option | undefined): VilleCase[] {
  if (!option) return []
  const legales = new Set(option.all_legal_targets)
  return ville.cases.filter((c) => legales.has(c.objet))
}

/** Les compteurs d'une piste, ecrits « 2 » ou « 2 + 1 » quand il y en a de plusieurs sortes. Rien sans compteur. */
export function resumeCompteurs(compteurs: Record<string, number> | undefined): string {
  const valeurs = Object.values(compteurs ?? {}).filter((n) => n > 0)
  return valeurs.join(' + ')
}

/** Un lieu de La ville (carte `pu…` portant le trait LOCATION). Sert AVANT que le moteur n'ait installe la grille (la mise en place pose
 *  les neuf lieux un a un, l'etat `ville` n'arrive qu'a la fin) : tant qu'on ne sait pas ou est le joueur, aucun lieu ne se montre. */
const estUnLieuDeLaVille = (carte: { card_id?: string; traits?: Partial<Record<string, number>> }): boolean =>
  /^pu/.test(carte.card_id ?? '') && Object.entries(carte.traits ?? {}).some(([cle, valeur]) => cle.toLowerCase() === 't_location' && Boolean(valeur))

/** Les cartes d'environnement posees sur la table d'UN joueur. Dans la ville, les neuf lieux sont des environnements : la table ne montre que
 *  celui qu'il occupe (les autres se lisent dans l'onglet « Ville »). Hors de la ville, la liste est rendue telle quelle. */
export function environnementVisible<T extends { id: number; card_id?: string; traits?: Partial<Record<string, number>> }>(
  monde: World | undefined,
  placeDuJoueur: number,
  environnement: readonly T[] | undefined
): T[] {
  const cartes = environnement ?? []
  const ville = villeDuMonde(monde)
  if (!ville) return cartes.filter((carte) => !estUnLieuDeLaVille(carte))
  const position = positionDuJoueur(ville, placeDuJoueur)
  const lieux = new Set(ville.cases.map((c) => c.objet))
  const occupe = position ? ville.cases.find((c) => c.ligne === position.ligne && c.colonne === position.colonne)?.objet : undefined
  return cartes.filter((carte) => (!lieux.has(carte.id) && !estUnLieuDeLaVille(carte)) || carte.id === occupe)
}

/** Le vilain (CAPO) d'une AUTRE rangee que celle du joueur : dans la ville, chaque rangee est le territoire de son CAPO, et on ne peut
 *  interagir qu'avec les vilains de son propre territoire. Faux hors de la ville ou pour un vilain sans rangee. */
export function vilainDUnAutreTerritoire(monde: World | undefined, placeDuJoueur: number, idVilain: number): boolean {
  const ville = villeDuMonde(monde)
  if (!ville) return false
  const sienne = positionDuJoueur(ville, placeDuJoueur)?.ligne
  const sa = ville.lignes.find((l) => l.capo === idVilain)?.ligne
  return sienne !== undefined && sa !== undefined && sa !== sienne
}
