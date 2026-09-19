// La règle de sélection d'une option (`select_rule`), appliquée pendant la
// désignation des cibles.
//
// ⚠ PERSONNE NE L'APPLIQUAIT. Le moteur l'envoie dans chaque option
// (`ask.ts`), `SelectorRule.AfterSelectTargets` ne vérifie que le NOMBRE de
// cibles, et le plateau lisait le champ sans jamais s'en servir. Signalé en
// jeu le 18/09/2026 sur « Suit Up » (45017), qui laissait prendre deux
// améliorations au lieu d'un allié et d'une amélioration : le moteur refusait
// le couple APRÈS coup, l'action échouait et la carte partait à la défausse
// sans rien faire.
//
// Deux cartes du dépôt portent une règle de ce genre :
//   - `01042` Ancestral Knowledge : « Choose up to 3 DIFFERENT cards in your
//     discard pile » (`DifferentCards`). Trois exemplaires de la même carte
//     étaient un choix accepté, contre la FAQ citée dans son script ;
//   - `45017` Suit Up portait `DifferentType` ; elle a été réécrite en deux
//     recherches successives et ne s'en sert plus.
//
// La règle est appliquée ICI, à la désignation : une cible qui la casserait
// n'est pas cliquable. Refuser au moment de valider ferait perdre la carte,
// ce qui est précisément le défaut qu'on corrige.

/** Ce qu'il faut savoir d'une cible pour trancher : son identité et son type. */
export type CibleDecrite = {
  /** `card_id` du moteur : deux exemplaires d'une même carte le partagent. */
  card_id?: string
  /** « Ally », « Upgrade », « Event »... */
  card_type?: string
}

/**
 * Cette cible casserait-elle la règle si on l'ajoutait aux cibles déjà
 * choisies ? Une règle inconnue ou vide ne refuse jamais rien : le plateau ne
 * doit pas devenir plus restrictif que le moteur sur les centaines d'options
 * qui n'ont pas de règle.
 */
export function cibleRefuseeParLaRegle(
  regle: string | undefined,
  dejaChoisies: readonly CibleDecrite[],
  candidate: CibleDecrite
): boolean {
  if (regle === 'DifferentCards') {
    // Même titre = même carte (FAQ officielle citée par `01042`). Deux
    // exemplaires partagent leur `card_id` ; sans `card_id` connu on laisse
    // passer plutôt que d'inventer un refus.
    if (candidate.card_id === undefined) return false
    return dejaChoisies.some((choisie) => choisie.card_id === candidate.card_id)
  }
  if (regle === 'DifferentType') {
    if (candidate.card_type === undefined) return false
    return dejaChoisies.some((choisie) => choisie.card_type === candidate.card_type)
  }
  return false
}
