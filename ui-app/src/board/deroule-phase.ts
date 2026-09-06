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
  | 'mechant'
  | 'sbires'
  | 'distribution'
  | 'revelation'
  | 'premier-joueur'

/** Ordre des cinq temps de la carte de reference. */
const ORDRE: TempsPhase[] = [
  'menace',
  'mechant',
  'sbires',
  'distribution',
  'revelation',
  'premier-joueur',
]

/**
 * Phase du moteur -> temps de la carte de reference, pour les entrees dont le
 * temps ne depend pas de l'auteur (menace, distribution, revelation).
 *
 * « Enemy Activation » n'y figure PAS : le vilain et ses sbires s'activent
 * tous les deux pendant cette meme phase moteur, donc son temps ('mechant' ou
 * 'sbires') se decide sur l'AUTEUR du fait, pas sur son nom de phase. Voir
 * `etapesDeroule`.
 */
const TEMPS_PAR_PHASE: Record<string, TempsPhase> = {
  'Main Scheme Place Threat': 'menace',
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
  /**
   * Le nombre du coup : les degats ou les menaces que la cible a encaisses,
   * les menaces posees pour l'etape de menace.
   *
   * Sur un fait, c'est `subi` et JAMAIS `inflige` : `inflige` est ce qui a ete
   * porte une fois la defense deduite, `subi` ce que la cible a reellement
   * encaisse. Une reduction de degats ou des derniers points de vie depasses
   * separent les deux, et le joueur lit ce qui s'est passe.
   */
  montant?: number
  /**
   * Compteur de la CIBLE apres le coup : ses points de vie restants, ou la
   * menace sur la manigance. Absent quand la source n'en donne pas (le moteur
   * laisse `restant` vide pour une cible qui n'a pas de compteur) : mieux vaut
   * n'afficher aucun compteur qu'un nombre invente.
   */
  restant?: number
  /**
   * Le seuil du compteur, quand la cible en a un : la menace maximale d'une
   * manigance. Les points de vie n'en ont pas, d'ou l'absence frequente.
   */
  plafond?: number
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
 * seconde fois se range sous la revelation, pas sous mechant ou sbires, sans
 * quoi il paraissait attaquer deux fois sans raison.
 *
 * `mechantIds` distingue le vilain de ses sbires pour les activations
 * ordinaires : `etapesDeroule` ne voit pas le monde, seulement les faits et le
 * journal, donc c'est l'appelant (board.tsx, qui lit `cartesMondeParId`) qui
 * lui dit qui est le camp du vilain. Un auteur absent de l'ensemble (inconnu
 * ou deja hors table) se range sous sbires : c'est le cas le plus frequent, et
 * s'y tromper coute une pastille, pas une regle du jeu.
 */
export function etapesDeroule(
  faits: FaitMechant[],
  entrees: EntreeHistorique[],
  round: number,
  mechantIds: Set<number>
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
  // Une etape PAR manigance touchee. Une seule etape suivie de la liste de ses
  // consequences disait deux fois la meme chose : « Menace sur la manigance
  // principale », puis « L'Effraction ! gagne 2 menaces ». Le fait tient en
  // une phrase, et chaque manigance a son propre compteur.
  for (const e of menace) {
    etapes.push({
      cle: `menace:${e.cle}`,
      temps: 'menace',
      titre: 'menace',
      regle: 'regle:menace',
      // Le nom NU de la carte, que l'entree porte deja a cote de sa phrase
      // (voir EntreeHistorique.nomCarte) : le decouper du titre traduit
      // marcherait dans une langue sur deux.
      cibleNom: e.nomCarte,
      // `valeur` est la variation SIGNEE du compteur : seule une POSE de
      // menace se met en phrase ici. Un retrait, qui n'a pas lieu a ce temps
      // de la phase, laisserait « gagne -1 menaces » ; sans montant, le titre
      // se replie sur sa formule generique.
      montant: e.valeur !== undefined && e.valeur > 0 ? e.valeur : undefined,
      restant: e.restant,
      plafond: e.plafond,
      boosts: [],
      consequences: [],
    })
  }

  faitsDuRound.forEach((fait, index) => {
    // Une phase deja connue (distribution, revelation) garde son temps
    // propre. Sinon, c'est une activation ordinaire : son temps depend de
    // l'AUTEUR du coup, pas de son nom de phase, puisque le vilain et ses
    // sbires s'activent tous deux pendant « Enemy Activation ».
    const temps = tempsDe(fait.phase) ?? (mechantIds.has(fait.auteur_id) ? 'mechant' : 'sbires')
    etapes.push({
      cle: `fait:${index}:${fait.auteur_id}`,
      temps,
      titre: fait.genre === 'attaque' ? 'attaque' : 'manigance',
      regle: temps === 'mechant' || temps === 'sbires' ? 'regle:activations' : 'regle:revelation',
      carteId: fait.auteur_id,
      cibleId: fait.cible_id,
      // Nettoyage applique partout ailleurs sur les noms de heros (icones,
      // symboles) : sans lui, le deroule affichait des prefixes que personne
      // d'autre n'affiche.
      auteurNom: fait.auteur.replace(/^\W*/, ''),
      cibleNom: fait.cible.replace(/^\W*/, ''),
      // `subi` et non `inflige` : voir le commentaire de `montant`.
      montant: fait.subi,
      // `restant` vaut `null` quand la cible n'a pas de compteur : on le
      // ramene a l'absence, seul etat que l'affichage sait taire.
      restant: fait.restant ?? undefined,
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

/**
 * Rang de l'etape courante DANS SON TEMPS, et nombre d'etapes de ce temps.
 *
 * Rend `undefined` quand le temps n'en compte qu'une : « 1 sur 1 » n'apprend
 * rien et encombre un cartouche qui tient en quatre lignes. Le joueur doit
 * savoir combien il lui en reste dans ce temps, pas lire un compteur inutile.
 *
 * Le rang se compte par les etapes qui PRECEDENT l'index, pas par un
 * `indexOf` : deux etapes peuvent etre egales sans etre le meme objet.
 */
export function rangDansLeTemps(
  etapes: EtapeDeroule[],
  index: number
): { rang: number; total: number } | undefined {
  const etape = etapes[index]
  if (!etape) return undefined
  const total = etapes.filter((e) => e.temps === etape.temps).length
  if (total < 2) return undefined
  const rang = etapes.slice(0, index + 1).filter((e) => e.temps === etape.temps).length
  return { rang, total }
}
