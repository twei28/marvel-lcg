// L'ASSEMBLEE de Kingsfall multi-tables (onglet « Assemblée ») : fonctions PURES. Decisions : .planning/mcdc-punisher/decisions-multi-tables.md.
import type { AssembleeExport, AssembleeGroupe, World } from './world'

/** L'assemblee exportee par le moteur, ou `undefined` hors assemblee (le champ est un dictionnaire vide). */
export function assembleeDuMonde(monde: World | undefined): AssembleeExport | undefined {
  const a = monde?.assemblee
  if (!a || !a.code || !a.groupes || a.groupes.length === 0) return undefined
  return {
    code: a.code,
    table: a.table ?? '',
    organisateur: a.organisateur ?? '',
    total_jetons: a.total_jetons ?? 0,
    seuil: a.seuil ?? 0,
    retournee: Boolean(a.retournee),
    degats: a.degats ?? 0,
    menace: a.menace ?? 0,
    joueurs: a.joueurs ?? 0,
    groupes: a.groupes,
    terminee: Boolean(a.terminee),
    gagnee: Boolean(a.gagnee),
  }
}

export type EtatGroupe = 'en_cours' | 'victoire' | 'defaite' | 'abandon'
export const ETAT_DU_GROUPE: Readonly<Record<AssembleeGroupe['etat'], EtatGroupe>> = {
  0: 'en_cours',
  1: 'victoire',
  2: 'defaite',
  3: 'abandon',
}

/** La part du seuil de Longue vie atteinte, entre 0 et 1 (1 des que la carte est retournee). */
export function avancementLongueVie(a: AssembleeExport): number {
  if (a.retournee) return 1
  return a.seuil > 0 ? Math.min(1, a.total_jetons / a.seuil) : 0
}

export type Verdict = 'en_attente' | 'gagnee' | 'perdue'
/** « At the end of all games, if damage >= threat, the pod wins ! » : pas de verdict tant qu'une table joue encore. */
export function verdictDeLAssemblee(a: AssembleeExport): Verdict {
  if (!a.terminee) return 'en_attente'
  return a.gagnee ? 'gagnee' : 'perdue'
}

/** Combien de groupes jouent encore. */
export function groupesEnCours(a: AssembleeExport): number {
  return a.groupes.filter((g) => g.etat === 0).length
}

/** Le nom a montrer d'un groupe : ses heros, sinon sa table. */
export function nomDuGroupe(g: AssembleeGroupe): string {
  return (g.noms || '').trim() || g.tab
}
