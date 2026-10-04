// Le journal COMPACT de la console : une ligne de texte par fait, les rounds en
// separateurs, sans les lignes de phase qui disent trois fois la meme chose.
//
// Choix de l'utilisateur (03/10/2026, questions une a une) : « faits + phases,
// sans doublons », « une ligne de texte compacte ». Le moteur ecrit, pour un
// meme moment, « Round 2 / Start Round », « === Debut du round 2 === » et
// « Phase : Player » : on n'en garde qu'une trace, le separateur du round.
import type { EntreeHistorique } from './HistoriquePartie'

export type LigneJournal =
  | { genre: 'round'; cle: string; round: number }
  | { genre: 'fait'; cle: string; texte: string; detail?: string; type: EntreeHistorique['type'] }

/** Narration technique du moteur, que le separateur de round dit deja. */
const TECHNIQUE = [
  /^={2,}/,
  /^-{2,}/,
  /^Phase\s*:/i,
  /^Fin de phase\s*:/i,
  /^Fin du round\b/i,
  // La plomberie des paquets (« EncounterDeck<31> va être mélangé », « AsideDeck<0> créé »).
  /\w+<\d+>/,
]
/** Details de phase en anglais technique (le separateur de round les remplace). */
const PHASES_MUETTES = new Set(['Start Round', 'End Round', 'Fin de phase', 'Mulligans'])

function texteDe(entree: EntreeHistorique): { texte: string; detail?: string } | undefined {
  const titre = entree.titre.trim()
  if (entree.type === 'phase') {
    // « Round 2 » + « Tour de Domino » : seul le detail apprend quelque chose.
    const detail = entree.detail?.trim()
    if (!detail || PHASES_MUETTES.has(detail)) return undefined
    return { texte: detail }
  }
  if (TECHNIQUE.some((motif) => motif.test(titre))) return undefined
  return { texte: titre, detail: entree.detail?.trim() || undefined }
}

/**
 * Les lignes a afficher, dans l'ORDRE DU JOURNAL (le plus recent d'abord). Un
 * separateur « Round N » ouvre chaque round, au-dessus de ses faits ; deux
 * lignes identiques qui se suivent n'en font qu'une.
 */
export function lignesCompactes(entrees: EntreeHistorique[]): LigneJournal[] {
  const lignes: LigneJournal[] = []
  let roundCourant: number | undefined
  let dernierTexte: string | undefined
  for (const entree of entrees) {
    if (entree.round !== roundCourant) {
      roundCourant = entree.round
      dernierTexte = undefined
      lignes.push({ genre: 'round', cle: `round:${entree.round}:${entree.cle}`, round: entree.round })
    }
    const ligne = texteDe(entree)
    if (!ligne) continue
    const cleTexte = `${ligne.texte}|${ligne.detail ?? ''}`
    if (cleTexte === dernierTexte) continue
    dernierTexte = cleTexte
    lignes.push({ genre: 'fait', cle: entree.cle, texte: ligne.texte, detail: ligne.detail, type: entree.type })
  }
  // Un round sans aucun fait affichable ne laisse pas de separateur orphelin.
  return lignes.filter((ligne, i) => ligne.genre === 'fait' || lignes[i + 1]?.genre === 'fait')
}
