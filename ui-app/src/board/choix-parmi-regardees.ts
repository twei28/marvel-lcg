// choix-parmi-regardees.ts — choisir parmi des cartes qu'on vient de REGARDER, sans détour.
//
// Rapport nicodede62 du 18/11/2026 (Tony Stark, « Futuriste » : « regardez les 3 cartes du dessus, ajoutez-en 1 à votre main ») :
//  1. la fenêtre « Cartes regardées » montrait les 3 cartes ;
//  2. un bouton « FUTURIST » se posait PAR-DESSUS, comme s'il fallait rechoisir le pouvoir ;
//  3. le cliquer cachait les cartes et demandait d'aller « Chercher dans le deck » pour les retrouver.
// Trois fenêtres pour un seul choix. Quand la question n'a qu'UNE option jouable et que TOUTES ses cibles sont des cartes déjà
// regardées, l'option se lance d'office et le sélecteur s'ouvre directement sur ces cartes (PC compris).
import type { Option } from './ask'

/** L'option à lancer d'office, ou `undefined` quand le joueur doit choisir lui-même. */
export function optionParmiRegardees(options: readonly Option[], regardees: ReadonlySet<number>): Option | undefined {
  if (regardees.size === 0) return undefined
  const jouables = options.filter((option) => option.failure_reason === '')
  if (jouables.length !== 1) return undefined
  const option = jouables[0]!
  const cibles = option.all_legal_targets
  if (cibles.length === 0 || option.target_num_range[1] === 0) return undefined
  return cibles.every((id) => regardees.has(id)) ? option : undefined
}

/** Les cibles d'une recherche sont-elles toutes des cartes déjà regardées ? Alors la pile s'ouvre d'office, même sur PC. */
export function ciblesDejaRegardees(cibles: readonly number[], regardees: ReadonlySet<number>): boolean {
  return cibles.length > 0 && cibles.every((id) => regardees.has(id))
}

/**
 * UNE seule option jouable, qui ne sert qu'à DÉSIGNER des cartes : son bouton n'était qu'une étape de plus avant le sélecteur.
 *  - rapport nicodede62 #158 (19/11/2026) : le pouvoir de Captain America ouvrait un bouton jaune « PAY COST DISCARD », puis le
 *    choix de la carte à défausser ;
 *  - rapport #153 (Magneto, « Factory Online ») : le bouton portait le nom de la manigance, et le joueur n'a pas compris qu'il
 *    fallait le cliquer pour choisir la M-Type Sentinel.
 * Le sélecteur s'ouvre directement ; le joueur valide toujours lui-même, et « Annuler » rend le bouton (une fois par question).
 * Jamais pour une carte à JOUER (paiement), ni quand on peut ne rien désigner (minimum 0 : le bouton seul est une réponse).
 */
export function optionACiblesSeule(options: readonly Option[]): Option | undefined {
  const jouables = options.filter((option) => option.failure_reason === '')
  if (jouables.length !== 1) return undefined
  const option = jouables[0]!
  if (option.name === 'Play' || Object.keys(option.target_payment ?? {}).length > 0) return undefined
  if (option.all_legal_targets.length === 0 || option.target_num_range[0] < 1) return undefined
  return option
}
