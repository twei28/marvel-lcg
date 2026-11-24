// LES CHOIX QU'UNE CARTE PROPOSE MAIS QUI N'ONT PAS DE CIBLE (bug 129, 12/11/2026).
//
// Nick Fury : « retirer 2 menaces / piocher 3 cartes / infliger 4 dégâts ». Sans menace nulle part, le moteur
// ecartait le premier choix et le plateau n'en montrait que deux : on croyait a un bug de la carte. Le moteur
// joint maintenant ces choix au canal des refus (`Controller.RendreLesRefus(choix=True)`) ; ici on les rend
// AFFICHABLES : grises, avec la raison. Ils ne rejoignent JAMAIS `demande.options` (voir ask.ts) : on ne peut
// ni les cliquer ni les viser au clavier.

import type { Demande, Option } from './ask'
import { t } from './langue'
import { phraseDuRefus } from './raisons-refus'

/** La raison, en clair. « Pas de cible » ne dit rien d'un retrait de menace : on nomme ce qui manque. */
function raisonDuChoix(refus: Option): string {
  if (/threat/i.test(refus.name)) return t('Aucune menace à retirer pour le moment')
  return phraseDuRefus(refus.failure_reason) ?? t('Aucune cible possible en ce moment')
}

/**
 * Les choix refuses de la question, prets a etre montres grises a la suite des vrais.
 * `failure_reason` porte la PHRASE (plus le code) ; l'identifiant est negatif pour ne croiser aucune vraie option.
 */
export function choixRefuses(demande: Demande | undefined): Option[] {
  if (!demande || demande.event_name !== 'WhenPlayerChooseAbility') return []
  return demande.refus
    .filter((refus) => refus.is_text_choice)
    .map((refus, rang) => ({ ...refus, id: -(rang + 1), failure_reason: raisonDuChoix(refus) }))
}
