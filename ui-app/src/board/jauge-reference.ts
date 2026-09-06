// La reference d'une jauge de MENACE quand le complot n'en donne pas.
//
// Le complot PRINCIPAL a une cible imprimee (`target_threat`) : sa jauge monte
// vers elle, et rien n'est a memoriser. Un complot ANNEXE n'en a pas — il arrive
// avec sa menace et on la fait descendre a zero pour le vaincre. Sa bande n'a
// donc de sens que rapportee a la plus haute menace vue sur LUI : pleine a
// l'arrivee, elle se vide a mesure qu'on le contre.
//
// La cle est l'identifiant d'OBJET de partie (WorldCard.id), jamais le
// `card_id` : deux exemplaires du meme complot partagent le second, et le plus
// avance ferait passer le nouveau venu pour a moitie contre.
//
// Une Map de module, comme le `dernierRender` de halo-statut.ts : la donnee est
// purement visuelle et ne survit pas au rechargement de la page. Elle n'a pas
// besoin d'etre purgee en cours de route : quitter une partie passe toujours par
// `window.location.href = '/prepare.html'` (retourMenu dans board.tsx), donc par
// un rechargement complet. `oublierReferencesMenace` existe pour les tests, et
// pour le jour ou une partie s'enchainerait sans recharger la page.

const references = new Map<number, number>()

/** Enregistre la menace courante et rend la plus haute vue sur cette carte. */
export function referenceMenace(objectId: number, courante: number): number {
  const connue = references.get(objectId) ?? 0
  const reference = Math.max(connue, courante)
  references.set(objectId, reference)
  return reference
}

/** Nouvelle partie : les identifiants d'objet sont reattribues, on repart a zero. */
export function oublierReferencesMenace(): void {
  references.clear()
}
