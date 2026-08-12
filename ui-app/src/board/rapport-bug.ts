// Le rapport de bug : ce que le plateau sait, mis sous une forme qu'on peut
// coller dans une conversation ou joindre à un fichier.
//
// Deux règles de conception, toutes les deux payées par l'expérience :
//
// 1. LE RAPPORT NE NETTOIE RIEN. Le panneau « H » efface les identifiants
//    avant d'afficher, parce qu'il est écrit pour être LU. Ici c'est l'inverse :
//    l'object id (« c48 ») est la seule façon fiable de viser une carte depuis
//    la console. Par nom, l'étoile des cartes uniques (« * Blockbuster ») fait
//    tout échouer en silence. Par card_id, une carte ABSENTE du jeu est
//    fabriquée dans la zone mise de côté.
//
// 2. LE RAPPORT DIT CE QU'IL NE SAIT PAS. Un journal plafonné qui se lit comme
//    complet est pire qu'un journal absent : il fait chercher au mauvais
//    endroit. D'où le drapeau `tronque`.
//
// Module PUR : ni DOM, ni réseau, ni horloge. L'horodatage arrive par le
// contexte, ce qui le rend testable.
import { MAX_ENTREES, type EntreeHistorique } from './HistoriquePartie'
import type { Demande, Option } from './ask'
import type { World, WorldCard } from './world'

export type PorteeRapport = 'recent' | 'tour' | 'partie'

/** Combien d'entrées rend la portée « recent ». */
const ENTREES_RECENTES = 20

export type ContexteRapport = {
  /** Date de la capture, en ISO. Passée de l'extérieur : le module reste pur. */
  horodatage: string
  /** Siège depuis lequel le rapport est pris. */
  siege?: number
  campagne?: { id: string; scenario: string }
  decouverte?: boolean
  /** Erreurs console relevées, de la plus ancienne à la plus récente. */
  erreurs?: string[]
  url?: string
}

export type CarteBug = {
  /** Object id sous la forme que la console attend : « c48 ». */
  objet: string
  card_id: string
  nom: string
  type: string
  zone: string
  joueur?: number
  vie?: number
  menace?: number
  /** false = engagée. */
  prete: boolean
  /** false = face cachée. */
  visible: boolean
  /** Renseigné quand la carte est attachée à une autre. */
  attacheeA?: string
}

export type OptionBug = {
  id: number
  nom: string
  /** Carte porteuse de l'option, ou null si aucune. */
  porteePar: string | null
  cibles: string[]
  nombreDeCibles: [number, number]
  cout: string
  /** La raison donnée par le moteur, ou null si l'option est jouable. */
  injouable: string | null
}

export type DemandeBug = {
  intitule: string
  evenement: string
  type: string
  annulable: boolean
  options: OptionBug[]
}

export type EntreeBug = {
  round: number
  phase: string
  type: string
  /** Le texte BRUT quand il existe, sinon le texte affiché. */
  texte: string
  detail?: string
  cible?: string
}

export type ContexteBug = {
  horodatage: string
  scenario: string | null
  vilain: string | null
  heros: string[]
  sieges: number
  siege?: number
  round: number
  phase: string
  render_id: number
  sandbox: boolean
  decouverte: boolean
  campagne?: { id: string; scenario: string }
  fin?: string
  erreurs: string[]
  url?: string
}

export type TableBug = {
  cartes: CarteBug[]
  /** Ressources disponibles annoncées par le moteur, par siège. */
  ressources: string[]
  encounter_deck: number
  encounter_discard: number
}

export type RapportBug = {
  /** Version du format. Un rapport ancien doit rester identifiable. */
  format: 1
  contexte: ContexteBug
  demande: DemandeBug | null
  table: TableBug
  journal: EntreeBug[]
  /** Vrai quand le journal a pu perdre son début. */
  tronque: boolean
}

const UNIT_TYPES = new Set(['Ally', 'Minion', 'EncounterVillain', 'Hero', 'AlterEgo'])
const SCHEME_TYPES = new Set(['MainScheme', 'EncounterSideScheme', 'PlayerSideScheme'])

function objet(id: number): string {
  return `c${id}`
}

function nombre(carte: WorldCard, cle: string): number | undefined {
  const valeur = carte.info[cle]
  return typeof valeur === 'number' ? valeur : undefined
}

function decrire(carte: WorldCard, zone: string, joueur?: number): CarteBug {
  return {
    objet: objet(carte.id),
    card_id: carte.card_id,
    nom: carte.name,
    type: carte.card_type,
    zone,
    joueur,
    vie: UNIT_TYPES.has(carte.card_type) ? nombre(carte, 'health') : undefined,
    menace: SCHEME_TYPES.has(carte.card_type) ? nombre(carte, 'k_threat') : undefined,
    prete: carte.is_ready,
    visible: carte.is_face_up,
    attacheeA: carte.bind_object_id ? objet(carte.bind_object_id) : undefined,
  }
}

function ajouter(
  sortie: CarteBug[],
  cartes: readonly WorldCard[] | undefined,
  zone: string,
  joueur?: number
): void {
  if (!Array.isArray(cartes)) return
  for (const carte of cartes) sortie.push(decrire(carte, zone, joueur))
}

/**
 * Les entrées que la portée retient.
 *
 * Le journal est stocké du PLUS RÉCENT AU PLUS ANCIEN. « Les 20 dernières » se
 * prend donc AU DÉBUT du tableau : un slice(-20) rendrait le début de la partie
 * en se lisant comme la fin.
 */
export function entreesDeLaPortee(
  entrees: EntreeHistorique[],
  portee: PorteeRapport,
  roundCourant: number
): EntreeHistorique[] {
  if (portee === 'partie') return [...entrees]
  if (portee === 'tour') return entrees.filter((e) => e.round === roundCourant)
  return entrees.slice(0, ENTREES_RECENTES)
}

function decrireOption(option: Option): OptionBug {
  // Le moteur préfixe ses options techniques par « p_ » et soude les mots par
  // des underscores : « p_Play », « Discard_a_status_card ». On rend le nom
  // lisible SANS le traduire : le rapport parle au développeur, et le nom
  // moteur est ce qu'on retrouvera dans le code.
  const brut = option.name.startsWith('p_') ? option.name.slice(2) : option.name
  // La clé 0 de target_payment est le coût quand il n'y a pas de cible ; sinon
  // on prend celui de la première cible légale, faute de mieux.
  const paiement = option.target_payment[0] ?? option.target_payment[option.all_legal_targets[0] ?? -1]
  return {
    id: option.id,
    nom: brut.replaceAll('_', ' ').trim(),
    porteePar: option.bind_id ? objet(option.bind_id) : null,
    cibles: option.all_legal_targets.map(objet),
    nombreDeCibles: option.target_num_range,
    cout: paiement?.cost ?? '',
    injouable: option.failure_reason ? option.failure_reason : null,
  }
}

function decrireTable(monde: World): TableBug {
  const cartes: CarteBug[] = []
  ajouter(cartes, monde.area_schemes_main, 'complot principal')
  ajouter(cartes, monde.area_schemes_side, 'complot annexe')
  ajouter(cartes, monde.area_villain, 'vilain')
  ajouter(cartes, monde.area_environment, 'environnement')
  ajouter(cartes, monde.area_boost, 'boost')
  ajouter(cartes, monde.area_revealing, 'en révélation')
  ajouter(cartes, monde.area_processing, 'en résolution')
  ajouter(cartes, monde.area_status_cards, 'statut')
  ajouter(cartes, monde.area_evidence, 'preuve')
  ajouter(cartes, monde.area_set_aside, 'mise de côté')
  ajouter(cartes, monde.area_removed, 'retirée du jeu')
  ajouter(cartes, monde.victory_display, 'zone de victoire')
  ajouter(cartes, monde.encounter_discard_pile, 'défausse rencontre')

  for (const [place, joueur] of (monde.players ?? []).entries()) {
    ajouter(cartes, joueur.area_hero, 'identité', place)
    ajouter(cartes, joueur.allies, 'alliés', place)
    ajouter(cartes, joueur.supports, 'soutiens', place)
    ajouter(cartes, joueur.engaged_enemies, 'ennemis engagés', place)
    ajouter(cartes, joueur.obligations_area, 'obligations', place)
    ajouter(cartes, joueur.environment_area, 'environnement joueur', place)
    ajouter(cartes, joueur.hand_cards, 'main', place)
    ajouter(cartes, joueur.reserve, 'réserve', place)
    ajouter(cartes, joueur.player_discard_pile, 'défausse', place)
    ajouter(cartes, joueur.dealt_encounter_cards, 'rencontre attribuée', place)
    ajouter(cartes, joueur.additional_deck, 'deck supplémentaire', place)
    ajouter(cartes, joueur.additional_discard_pile, 'défausse supplémentaire', place)
    ajouter(cartes, joueur.set_aside_deck, 'mise de côté joueur', place)
  }

  return {
    cartes,
    ressources: (monde.players ?? []).map((joueur) => joueur.resources),
    encounter_deck: monde.encounter_deck?.length ?? 0,
    encounter_discard: monde.encounter_discard_pile?.length ?? 0,
  }
}

export function construireRapport(
  monde: World,
  demande: Demande | undefined,
  entrees: EntreeHistorique[],
  portee: PorteeRapport,
  contexte: ContexteRapport
): RapportBug {
  const retenues = entreesDeLaPortee(entrees, portee, monde.round_id)

  return {
    format: 1,
    contexte: {
      horodatage: contexte.horodatage,
      scenario: monde.area_schemes_main?.[0]?.name ?? null,
      vilain: monde.area_villain?.[0]?.name ?? null,
      heros: (monde.players ?? []).map((joueur) => joueur.area_hero?.[0]?.name ?? '?'),
      sieges: (monde.players ?? []).length,
      siege: contexte.siege,
      round: monde.round_id,
      phase: monde.phase,
      render_id: monde.render_id,
      sandbox: monde.mode_sandbox === true,
      decouverte: contexte.decouverte === true,
      campagne: contexte.campagne,
      fin: monde.game_over ? (monde.game_over_reason ?? 'partie terminée') : undefined,
      erreurs: contexte.erreurs ?? [],
      url: contexte.url,
    },
    demande: demande
      ? {
          intitule: demande.prompt_text,
          evenement: demande.event_name,
          type: demande.ability_type,
          annulable: demande.show_cancel,
          options: demande.options.map(decrireOption),
        }
      : null,
    table: decrireTable(monde),
    journal: retenues.map((e) => ({
      round: e.round,
      phase: e.phase,
      type: e.type,
      texte: e.brut && e.brut.length > 0 ? e.brut : e.titre,
      detail: e.detail,
      cible: e.cibleId !== undefined ? objet(e.cibleId) : undefined,
    })),
    // Le tampon plein signifie que des entrées ont été jetées par le bas. La
    // question ne se pose que sur « toute la partie » : une portée courte ne
    // prétend rien couvrir d'autre qu'elle-même.
    tronque: portee === 'partie' && entrees.length >= MAX_ENTREES,
  }
}
