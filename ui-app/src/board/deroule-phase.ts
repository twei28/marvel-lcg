// La phase du mechant, decoupee en ETAPES a valider une par une.
//
// Deux sources, et aucune n'est une relecture du monde :
//
// 1. `FaitMechant` : les activations que le moteur a deja resolues. Lui seul
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
  /**
   * Cle de texte ('attaque', 'manigance', 'menace') que le composant traduit
   * en phrase, ou titre deja redige repris tel quel du journal (cartes
   * revelees) quand la source n'est pas un fait du moteur.
   */
  titre: string
  /** Rappel de la regle appliquee. */
  regle: string
  /** Carte a mettre en avant sur le plateau. */
  carteId?: number
  /** Cible de l'action, pour le trait de la livraison 2. */
  cibleId?: number
  /**
   * Noms de l'auteur et de la cible, portes par l'ETAPE elle-meme, pas
   * resolus a l'affichage via l'index du monde courant.
   *
   * `FaitMechant` les porte deja en clair (`auteur`, `cible`) : le moteur les
   * connait au moment du coup. Une carte morte pendant la phase (ex. un
   * minion tue par sa propre cible) a disparu de l'index du monde au moment
   * ou l'etape s'affiche ; y chercher son nom affichait « Ultron attaque #88 »
   * a la place. Meme raison que RecapPhaseMechant, qui fait ce choix pour la
   * meme cause.
   */
  auteurNom?: string
  cibleNom?: string
  boosts: BoostDeroule[]
  consequences: { cle: string; texte: string }[]
  /** Texte du moteur quand on ne sait pas mettre le fait en phrase. */
  brut?: string
  /**
   * Cette etape defile SEULE, sans attendre de validation.
   *
   * Vrai pour la narration technique du moteur (defausses, fins d'activation,
   * « DiscardPile<3> ») : elle ne se lit pas, mais on ne la cache pas pour
   * autant. Constate en partie : 8 etapes de ce genre sur 12, une phase noyee.
   */
  auto?: boolean
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
  entrees: EntreeHistorique[],
  round: number
): EtapeDeroule[] {
  const etapes: EtapeDeroule[] = []

  // `entrees` accumule TOUTE la partie, pas seulement la phase en cours : sans
  // ce filtre sur le round, la phase du round 4 faisait revoir les cartes
  // rencontre des rounds 1 a 3. Et l'historique empile la plus recente EN
  // TETE : sans le `.reverse()`, ces vieilles cartes s'affichaient en plus a
  // l'envers. Meme choix que RecapPhaseMechant.bilanDeLaPhase, qui a le meme
  // besoin.
  const duRound = [...entrees.filter((e) => e.round === round)].reverse()

  // Meme filtre que ci-dessus, mais sur les FAITS : sans lui, un fait du
  // round precedent restait affiche pendant le tour du joueur suivant, avant
  // de ressurgir a la vraie phase du mechant du round 2 (defaut constate en
  // partie reelle). Un fait SANS round_id (moteur ou sauvegarde anterieurs a
  // ce champ) est GARDE quel que soit le round demande : mieux vaut une etape
  // de trop qu'un deroule muet.
  const faitsDuRound = faits.filter((f) => f.round_id === undefined || f.round_id === round)

  const menace = duRound.filter(
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

  faitsDuRound.forEach((fait, index) => {
    const temps = tempsDe(fait.phase) ?? 'activations'
    etapes.push({
      cle: `fait:${index}:${fait.auteur_id}`,
      temps,
      titre: fait.genre === 'attaque' ? 'attaque' : 'manigance',
      regle: temps === 'activations' ? 'regle:activations' : 'regle:revelation',
      carteId: fait.auteur_id,
      cibleId: fait.cible_id,
      // Nettoyage applique partout ailleurs sur les noms de heros (icones,
      // symboles) : sans lui, le deroule affichait des prefixes que personne
      // d'autre n'affiche.
      auteurNom: fait.auteur.replace(/^\W*/, ''),
      cibleNom: fait.cible.replace(/^\W*/, ''),
      boosts: fait.boosts.map((boost, rang) => ({
        cle: `boost:${rang}:${boost.id}`,
        nom: boost.nom,
        cibleId: boost.id,
        apport: boost.apport,
      })),
      consequences: [],
    })
  })

  // Les cartes revelees, que les faits du moteur ne couvrent pas : lui ne rend
  // que les activations resolues.
  for (const e of duRound) {
    if (tempsDe(e.phase) !== 'revelation') continue
    if (e.type === 'card') {
      etapes.push({
        cle: `carte:${e.cle}`,
        temps: 'revelation',
        titre: e.titre,
        regle: 'regle:revelation',
        carteId: e.cibleId,
        boosts: [],
        consequences: [],
      })
      continue
    }
    // Narration que personne n'a su mettre en phrase : on la montre telle
    // quelle plutot que de la taire. Sans `brut`, c'est la narration interne
    // du moteur, qui reste au journal.
    if (e.type === 'text' && e.brut) {
      etapes.push({
        cle: `brut:${e.cle}`,
        temps: 'revelation',
        titre: e.titre,
        regle: 'regle:revelation',
        boosts: [],
        consequences: [],
        brut: e.brut,
        // Narration technique du moteur : elle ne se lit pas, elle defile seule.
        auto: true,
      })
    }
  }

  return etapes.sort((a, b) => ORDRE.indexOf(a.temps) - ORDRE.indexOf(b.temps))
}
