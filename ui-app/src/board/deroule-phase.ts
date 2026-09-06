// La phase du mechant, decoupee en ETAPES a valider une par une.
//
// Deux sources, et aucune n'est une relecture du monde :
//
// 1. `FaitMechant` — les activations que le moteur a deja resolues. Lui seul
//    connait la composition d'un coup (base, boost, defense) ; une deduction
//    verrait le resultat sans jamais pouvoir dire « 5 = 3 + 2 », et compterait
//    plusieurs fois ce que le moteur rend plusieurs fois autour d'une seule
//    resolution.
// 2. Les entrees du journal, pour ce que les faits ne couvrent pas : la menace
//    posee, les cartes revelees.
//
// Ce module est PUR : aucun DOM, aucune traduction. Il rend des cles de texte
// que le composant met en langue. C'est ce qui le rend testable sans navigateur
// et verifiable dans les deux langues.

import type { EntreeHistorique } from './HistoriquePartie'
import type { FaitMechant } from './world'

export type TempsPhase =
  | 'menace'
  | 'activations'
  | 'distribution'
  | 'revelation'
  | 'premier-joueur'

/** Ordre des quatre temps de la carte de reference. */
const ORDRE: TempsPhase[] = [
  'menace',
  'activations',
  'distribution',
  'revelation',
  'premier-joueur',
]

/** Phase du moteur -> temps de la carte de reference. */
const TEMPS_PAR_PHASE: Record<string, TempsPhase> = {
  'Main Scheme Place Threat': 'menace',
  'Enemy Activation': 'activations',
  'Deal Encounter Cards': 'distribution',
  'Reveal Encounter Cards': 'revelation',
}

export type BoostDeroule = {
  cle: string
  nom: string
  cibleId: number
  apport: number
}

export type EtapeDeroule = {
  /** Identifiant stable, pour la cle React et le « Precedent ». */
  cle: string
  temps: TempsPhase
  /** Deja mis en phrase par le composant : ici, le texte brut de l'action. */
  titre: string
  /** Rappel de la regle appliquee. */
  regle: string
  /** Carte a mettre en avant sur le plateau. */
  carteId?: number
  /** Cible de l'action, pour le trait de la livraison 2. */
  cibleId?: number
  boosts: BoostDeroule[]
  consequences: { cle: string; texte: string }[]
  /** Texte du moteur quand on ne sait pas mettre le fait en phrase. */
  brut?: string
}

function tempsDe(phase: string | undefined): TempsPhase | undefined {
  return phase ? TEMPS_PAR_PHASE[phase] : undefined
}

/**
 * Les etapes de la phase, dans l'ordre de la carte de reference.
 *
 * Un fait porte SA phase : un vilain qu'une carte revelee fait frapper une
 * seconde fois se range sous la revelation, pas sous les activations, sans quoi
 * il paraissait attaquer deux fois sans raison.
 */
export function etapesDeroule(
  faits: FaitMechant[],
  entrees: EntreeHistorique[]
): EtapeDeroule[] {
  const etapes: EtapeDeroule[] = []

  const menace = entrees.filter(
    (e) => tempsDe(e.phase) === 'menace' && e.type === 'threat'
  )
  if (menace.length > 0) {
    etapes.push({
      cle: 'menace',
      temps: 'menace',
      titre: 'menace',
      regle: 'regle:menace',
      boosts: [],
      consequences: menace.map((e) => ({ cle: e.cle, texte: e.titre })),
    })
  }

  faits.forEach((fait, index) => {
    const temps = tempsDe(fait.phase) ?? 'activations'
    etapes.push({
      cle: `fait:${index}:${fait.auteur_id}`,
      temps,
      titre: fait.genre === 'attaque' ? 'attaque' : 'manigance',
      regle: temps === 'activations' ? 'regle:activations' : 'regle:revelation',
      carteId: fait.auteur_id,
      cibleId: fait.cible_id,
      boosts: fait.boosts.map((boost, rang) => ({
        cle: `boost:${rang}:${boost.id}`,
        nom: boost.nom,
        cibleId: boost.id,
        apport: boost.apport,
      })),
      consequences: [],
    })
  })

  return etapes.sort((a, b) => ORDRE.indexOf(a.temps) - ORDRE.indexOf(b.temps))
}
