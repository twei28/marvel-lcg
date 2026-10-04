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
  /** Ce que le navigateur a réellement posé pour les piles du joueur
   *  (`sonde-affichage.ts`). */
  affichage?: string[]
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
  /**
   * TOUT le reste de `info`, sauf ce que la ligne rend déjà (`health`,
   * `k_threat`). C'est là que vivent les compteurs : pouvoir, tous usages,
   * accélération, charges d'une amélioration… Les clés varient selon le type
   * de carte, et une capacité maison en invente de nouvelles : on ne peut donc
   * pas dresser la liste de ce qui compte, et un rapport qui trierait
   * tairait justement le compteur du jour.
   *
   * Ajouté le 02/09/2026 : sans lui, un bug sur « Power Syphon » (dd001a place
   * un compteur de pouvoir, maximum 3) était indiagnosticable — le rapport ne
   * disait pas combien de compteurs portait le héros.
   */
  compteurs?: Record<string, number>
  /** Mots-clés temporaires posés par un effet (villainous, stalwart…). */
  buffs?: Record<string, string>
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
  manuel: boolean
  decouverte: boolean
  campagne?: { id: string; scenario: string }
  fin?: string
  erreurs: string[]
  url?: string
  /** Constat d'affichage des piles du joueur : voir `sonde-affichage.ts`. */
  affichage?: string[]
  /**
   * La TRACE (tâche 2) : au moins une intervention manuelle a eu lieu au
   * cours de cette partie, posée une fois pour toutes et jamais éteinte.
   *
   * DISTINCTE de `manuel` juste au-dessus, qui lit `mode_manuel` (la RÈGLE :
   * cette partie EST manuelle dès sa création). Une partie ordinaire, jamais
   * déclarée manuelle, peut très bien porter cette marque si elle a subi une
   * pause corrective un soir de bug — c'est justement le cas que ce champ
   * doit signaler à l'auteur du jeu, avant même qu'il ne lise le reste.
   */
  corrigeeALaMain: boolean
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
  /**
   * Les gestes manuels, et EUX SEULS, regroupés en fin de rapport pour qu'on
   * les audite d'un coup d'œil (tâche 6).
   *
   * Reprend les mêmes entrées que le journal, sous leur forme chronologique
   * habituelle — on ne les déplace pas, on les DUPLIQUE ici.
   *
   * ⚠ VISE TOUJOURS LA PARTIE ENTIÈRE, quelle que soit la `portee` demandée
   * pour le journal ci-dessus : on ne filtre PAS sur `retenues`. Une portée
   * « recent » ou « tour » existe pour ne pas noyer le lecteur dans un long
   * journal, mais un geste manuel posé plus tôt dans la partie reste une
   * intervention à auditer (voir tâche 6, décision documentée dans le
   * rapport de tâche).
   *
   * Cette visée n'est PAS une garantie d'exhaustivité, pour DEUX raisons
   * distinctes :
   *
   * — le tampon source (`entrees`) est lui-même plafonné à `MAX_ENTREES`, en
   *   amont de ce module. Un geste manuel plus ancien que le tampon a déjà
   *   disparu avant que cette fonction ne le voie. Voir
   *   `gestesManuelsIncomplets`, qui dit quand ce risque est réel ;
   *
   * — I3 (revue finale, 20/09/2026) : le journal est LOCAL AU NAVIGATEUR qui
   *   prend le rapport. Sur une table EN LIGNE, les gestes posés depuis les
   *   autres sièges n'y sont jamais entrés, et rien ici ne les agrège (c'est
   *   un autre chantier). La version texte le DIT en tête de section, sous
   *   le titre — une limite tue ferait conclure à l'absence d'intervention.
   */
  gestesManuels: EntreeBug[]
  /**
   * Correction 1 (revue) : le tampon source de `gestesManuels` est-il plein,
   * au point qu'on ne peut plus AFFIRMER couvrir toute la partie ?
   *
   * DISTINCT de `tronque` juste en dessous : `tronque` ne s'allume que pour
   * `portee === 'partie'`, parce que le journal affiché à une portée courte
   * ne prétend décrire que sa fenêtre — rien à y signaler. `gestesManuels`,
   * lui, prétend TOUJOURS couvrir toute la partie, quelle que soit la
   * `portee` choisie : ce champ doit donc s'allumer sur le même critère
   * (tampon plein), INDÉPENDAMMENT de `portee`.
   *
   * ⚠ Le cas dangereux n'est pas un cas de bord : un rapport pris à chaud,
   * en portée courte, sur une partie longue dont le tampon a déjà évincé un
   * vieux geste, affiche sinon une section propre et silencieuse sur sa
   * propre incomplétude — ce qui fait précisément conclure à tort à
   * l'absence d'intervention manuelle.
   */
  gestesManuelsIncomplets: boolean
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

/** Le reste de `info`, une fois retiré ce que la ligne rend déjà en clair.
 *  On ne retire `health` / `k_threat` que s'ils SONT rendus : sur une carte
 *  d'un autre type ils passent par `compteurs`, où ils valent mieux que rien. */
function compteurs(carte: WorldCard, rendus: string[]): Record<string, number> | undefined {
  const sortie: Record<string, number> = {}
  for (const [cle, valeur] of Object.entries(carte.info)) {
    if (rendus.includes(cle)) continue
    if (typeof valeur !== 'number' || valeur === 0) continue
    sortie[cle] = valeur
  }
  return Object.keys(sortie).length > 0 ? sortie : undefined
}

function decrire(carte: WorldCard, zone: string, joueur?: number): CarteBug {
  const estUnite = UNIT_TYPES.has(carte.card_type)
  const estManigance = SCHEME_TYPES.has(carte.card_type)
  const rendus = [
    ...(estUnite ? ['health'] : []),
    ...(estManigance ? ['k_threat'] : []),
  ]
  // `buffs` est un Partial : une clé peut porter `undefined`. On filtre donc
  // au lieu d'étaler, sinon le type promis (Record<string, string>) ment.
  const buffsRetenus: Record<string, string> = {}
  for (const [cle, valeur] of Object.entries(carte.buffs)) {
    if (typeof valeur === 'string' && valeur !== '') buffsRetenus[cle] = valeur
  }
  const buffs = Object.keys(buffsRetenus).length > 0 ? buffsRetenus : undefined
  return {
    objet: objet(carte.id),
    card_id: carte.card_id,
    nom: carte.name,
    type: carte.card_type,
    zone,
    joueur,
    vie: estUnite ? nombre(carte, 'health') : undefined,
    menace: estManigance ? nombre(carte, 'k_threat') : undefined,
    prete: carte.is_ready,
    visible: carte.is_face_up,
    attacheeA: carte.bind_object_id ? objet(carte.bind_object_id) : undefined,
    compteurs: compteurs(carte, rendus),
    buffs,
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

/** Une entrée d'historique, sous la forme qu'attend le rapport (journal ou gestes manuels). */
function decrireEntree(e: EntreeHistorique): EntreeBug {
  return {
    round: e.round,
    phase: e.phase,
    type: e.type,
    texte: e.brut && e.brut.length > 0 ? e.brut : e.titre,
    detail: e.detail,
    cible: e.cibleId !== undefined ? objet(e.cibleId) : undefined,
  }
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
      manuel: monde.mode_manuel === true,
      decouverte: contexte.decouverte === true,
      campagne: contexte.campagne,
      fin: monde.game_over ? (monde.game_over_reason ?? 'partie terminée') : undefined,
      erreurs: contexte.erreurs ?? [],
      url: contexte.url,
      affichage: contexte.affichage,
      corrigeeALaMain: monde.corrigee_a_la_main === true,
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
    journal: retenues.map(decrireEntree),
    // Toujours filtré sur TOUTES les entrées, jamais sur `retenues` : voir le
    // commentaire du champ `gestesManuels` (tâche 6).
    gestesManuels: entrees.filter((e) => e.type === 'manuel').map(decrireEntree),
    // Correction 1 : même critère que `tronque` (tampon plein), mais SANS la
    // condition `portee === 'partie'` — `gestesManuels` vise toute la partie
    // quelle que soit la portée demandée, donc le risque d'incomplétude
    // existe quelle que soit cette portée.
    gestesManuelsIncomplets: entrees.length >= MAX_ENTREES,
    // Le tampon plein signifie que des entrées ont été jetées par le bas. La
    // question ne se pose que sur « toute la partie » : une portée courte ne
    // prétend rien couvrir d'autre qu'elle-même.
    tronque: portee === 'partie' && entrees.length >= MAX_ENTREES,
  }
}

/**
 * Le rappel qui accompagne chaque rapport. Il ne coûte que trois lignes et il
 * évite la perte de temps la mieux documentée du projet : viser une carte
 * autrement que par son object id.
 */
const RAPPEL =
  'Une commande de console se vise par object id (« c48 »). Par nom, ' +
  "l'étoile des cartes uniques fait tout échouer en silence ; par card_id, une " +
  'carte absente du jeu est fabriquée dans la zone mise de côté.'

function ligneCarte(carte: CarteBug): string {
  const etats = [
    carte.vie !== undefined ? `${carte.vie} PV` : undefined,
    carte.menace !== undefined ? `${carte.menace} menace` : undefined,
    carte.prete ? undefined : 'engagée',
    carte.visible ? undefined : 'face cachée',
    carte.attacheeA ? `attachée à ${carte.attacheeA}` : undefined,
    carte.compteurs
      ? Object.entries(carte.compteurs)
          .map(([cle, valeur]) => `${cle}=${valeur}`)
          .join(' ')
      : undefined,
    carte.buffs
      ? Object.entries(carte.buffs)
          .map(([cle, valeur]) => `buff:${cle}=${valeur}`)
          .join(' ')
      : undefined,
  ].filter((e): e is string => e !== undefined)
  const place = carte.joueur !== undefined ? ` P${carte.joueur + 1}` : ''
  const suffixe = etats.length > 0 ? ` [${etats.join(', ')}]` : ''
  // La ZONE etait collectee depuis le premier jour et n'etait jamais ecrite.
  // Sans elle, deux cartes du meme nom sont indiscernables et, surtout, on ne
  // peut pas dire si un sbire est ENGAGE ou au REBUT — c'est pourtant ce qui
  // decide si sa capacite continue s'applique encore (dd015 Mister Fantastic,
  // qui convertit le mental en physique tant qu'il est engage).
  return `  ${carte.objet} ${carte.nom} (${carte.card_id}, ${carte.type}, ${carte.zone})${place}${suffixe}`
}

function ligneOption(option: OptionBug): string {
  const morceaux = [
    option.porteePar ? `portée par ${option.porteePar}` : undefined,
    option.cibles.length > 0
      ? `cibles ${option.nombreDeCibles[0]}..${option.nombreDeCibles[1]} parmi ${option.cibles.join(' ')}`
      : undefined,
    option.cout ? `coût ${option.cout}` : undefined,
    option.injouable ? `INJOUABLE : ${option.injouable}` : undefined,
  ].filter((m): m is string => m !== undefined)
  return `  [${option.id}] ${option.nom}${morceaux.length > 0 ? ' / ' + morceaux.join(' ; ') : ''}`
}

export function rapportEnTexte(rapport: RapportBug): string {
  const c = rapport.contexte
  const lignes: string[] = []

  lignes.push('=== RAPPORT DE BUG / Marvel Champions ===')
  // La marque passe AVANT le reste, y compris « Pris le » : c'est ce qui doit
  // sauter aux yeux avant même de lire le corps du rapport (tâche 6). Le
  // détail (mode manuel ou non, campagne...) reste dans la ligne « Mode » du
  // contexte, plus bas ; ceci n'est qu'un signal d'alerte immédiat.
  if (c.corrigeeALaMain) {
    lignes.push('/!\\ PARTIE CORRIGÉE À LA MAIN : au moins une intervention manuelle a eu lieu.')
  }
  lignes.push(`Pris le ${c.horodatage}`)
  lignes.push('')
  lignes.push('--- CONTEXTE ---')
  lignes.push(`Scénario : ${c.scenario ?? '?'}${c.vilain ? ` (vilain : ${c.vilain})` : ''}`)
  lignes.push(
    `Héros : ${c.heros.length > 0 ? c.heros.map((h, i) => `P${i + 1} ${h}`).join(', ') : 'aucun'}`
  )
  lignes.push(`Round ${c.round}, phase « ${c.phase} », render_id ${c.render_id}`)
  const modes = [
    `${c.sieges} siège(s)`,
    c.siege !== undefined ? `rapport pris depuis P${c.siege + 1}` : undefined,
    c.sandbox ? 'bac à sable' : undefined,
    c.manuel ? 'mode manuel' : undefined,
    c.decouverte ? 'mode Découverte' : undefined,
    c.campagne ? `campagne ${c.campagne.id}, scénario ${c.campagne.scenario}` : undefined,
    c.fin ? `PARTIE TERMINÉE : ${c.fin}` : undefined,
  ].filter((m): m is string => m !== undefined)
  lignes.push(`Mode : ${modes.join(' ; ')}`)
  if (c.url) lignes.push(`Page : ${c.url}`)
  if (c.erreurs.length > 0) {
    lignes.push(`Erreurs console (${c.erreurs.length}) :`)
    for (const erreur of c.erreurs) lignes.push(`  ${erreur}`)
  }
  if (c.affichage && c.affichage.length > 0) {
    lignes.push('Affichage des piles du joueur :')
    for (const ligne of c.affichage) lignes.push(`  ${ligne}`)
  }

  lignes.push('')
  lignes.push('--- DEMANDE EN COURS ---')
  if (rapport.demande === null) {
    lignes.push('Aucune demande en cours : le moteur ne nous attend pas.')
  } else {
    const d = rapport.demande
    lignes.push(`Intitulé : ${d.intitule || '(vide)'}`)
    lignes.push(
      `Type ${d.type || '?'}, événement ${d.evenement || '?'}, annulable : ${d.annulable ? 'oui' : 'non'}`
    )
    lignes.push(d.options.length > 0 ? 'Options :' : 'Aucune option proposée.')
    for (const option of d.options) lignes.push(ligneOption(option))
  }

  lignes.push('')
  lignes.push('--- TABLE ---')
  lignes.push(
    `Deck rencontre : ${rapport.table.encounter_deck} cartes ; défausse rencontre : ${rapport.table.encounter_discard}`
  )
  rapport.table.ressources.forEach((ressources, place) => {
    lignes.push(`Ressources P${place + 1} : ${ressources || '(aucune)'}`)
  })
  for (const carte of rapport.table.cartes) lignes.push(ligneCarte(carte))

  lignes.push('')
  lignes.push(
    `--- JOURNAL (${rapport.journal.length} entrées, de la plus récente à la plus ancienne) ---`
  )
  for (const ligne of rapport.journal) {
    const cible = ligne.cible ? ` {${ligne.cible}}` : ''
    const detail = ligne.detail ? ` / ${ligne.detail}` : ''
    lignes.push(`R${ligne.round} [${ligne.type}]${cible} ${ligne.texte}${detail}`)
  }
  if (rapport.tronque) {
    lignes.push('')
    lignes.push(
      `/!\\ Journal TRONQUÉ : le tampon est plafonné à ${MAX_ENTREES} entrées, le début de la partie a été perdu.`
    )
  }

  lignes.push('')
  lignes.push('--- À SAVOIR ---')
  lignes.push(RAPPEL)
  lignes.push(
    'Ce rapport contient les mains de tous les sièges : il décrit la table entière, pas seulement ce que ce siège joue.'
  )

  // En fin de document, et SEULEMENT s'il y a quelque chose à montrer : une
  // section vide laisserait croire à une intervention qui n'a pas eu lieu
  // (tâche 6). Toujours la partie entière, jamais limitée à la portée
  // choisie pour le journal ci-dessus — voir le commentaire du champ
  // `gestesManuels`.
  //
  // Correction 1 : la section s'affiche AUSSI quand la liste est vide mais
  // que `gestesManuelsIncomplets` est vrai — c'est le cas dangereux qu'une
  // liste vide « propre » masquerait : on ne peut plus dire s'il n'y a
  // vraiment eu aucun geste manuel, ou si le tampon en a évincé un.
  if (rapport.gestesManuels.length > 0 || rapport.gestesManuelsIncomplets) {
    lignes.push('')
    const compte = rapport.gestesManuels.length > 0 ? ` (${rapport.gestesManuels.length})` : ''
    lignes.push(`--- GESTES MANUELS${compte}, pour audit rapide ---`)
    // I3 (revue finale, 20/09/2026) : LA PORTEE REELLE, DITE PLUTOT QUE TUE.
    // Le journal source vit dans le NAVIGATEUR qui prend le rapport, et nulle
    // part ailleurs : sur une table EN LIGNE, un geste manuel posé depuis un
    // autre siège n'y a jamais figuré. Rien ici n'agrège les journaux des
    // autres clients — c'est un autre chantier — mais une section qui promet
    // « pour audit rapide » sans le dire fait conclure à l'absence
    // d'intervention, exactement comme une liste vide sur un tampon plein
    // (voir `gestesManuelsIncomplets` juste en dessous). Une limite dite est
    // acceptable ; une limite muette ne l'est pas.
    lignes.push(
      'Portée : les gestes de CE navigateur seulement. Le journal est local au siège qui prend le rapport — un geste posé depuis un autre siège n’y figure pas.'
    )
    if (rapport.gestesManuelsIncomplets) {
      // Symbole ⚠ et formulation volontairement différents de l'avertissement
      // du JOURNAL (« /!\ Journal TRONQUÉ ») juste au-dessus : les deux
      // signalent des incomplétudes différentes, il ne faut pas les confondre.
      lignes.push(
        `⚠ Liste peut-être incomplète : le tampon de journal (${MAX_ENTREES} entrées) est plein, un geste manuel plus ancien a pu en être évincé avant ce relevé.`
      )
    }
    for (const geste of rapport.gestesManuels) {
      const cible = geste.cible ? ` {${geste.cible}}` : ''
      const detail = geste.detail ? ` / ${geste.detail}` : ''
      lignes.push(`R${geste.round}${cible} ${geste.texte}${detail}`)
    }
  }

  return lignes.join('\n')
}

/**
 * Nom du fichier téléchargé. Le scénario et le round suffisent à distinguer
 * deux rapports pris dans la même soirée, et évitent le « rapport (3).json »
 * du navigateur.
 */
export function nomFichierRapport(rapport: RapportBug, extension: 'json' | 'txt' = 'json'): string {
  const base = (rapport.contexte.scenario ?? 'partie')
    .toLowerCase()
    .normalize('NFD')
    .replace(/[̀-ͯ]/g, '')
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-|-$/g, '')
  return `rapport-${base || 'partie'}-r${rapport.contexte.round}.${extension}`
}
