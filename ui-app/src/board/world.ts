// Le contrat de /get_world, releve sur les 34 etats enregistres du jeu
// (public/js/fixtures/) et sur le runtime historique qui les consomme
// (public/js/marvel/descriptor.js). Rien n'est suppose ici.
//
// Ces types ne decrivent pas tout le descripteur : seulement ce que le plateau
// lit. Les champs absents restent absents, pas devines.

/** Une carte, telle que le moteur la decrit. Meme forme dans toutes les zones. */
export type WorldCard = {
  /** Identifiant d'objet de partie (« object_id » cote runtime). */
  id: number
  /** false = carte engagee (le runtique la penche). */
  is_ready: boolean
  /** false = posee face cachee sur la table (ou en main). */
  is_face_up: boolean
  /** Numeros de joueurs autorises a voir la face. Vide = personne. */
  visible_for_players: number[]
  /** != 0 : cette carte est attachee a la carte portant cet id. */
  bind_object_id: number
  name: string
  /** Compteurs et statistiques courants. Cles variables selon le type. */
  info: Partial<Record<string, number>>
  traits: Partial<Record<string, number>>
  buffs: Partial<Record<string, string>>
  card_id: string
  /** Identifiant d'image. Voir scanUrl() dans card-model.ts. */
  pic_id: string
  /** Images de dos possibles. Le runtime n'utilise que la premiere. */
  down_card_ids: string[]
  card_type: string
  cost: number
  /**
   * Identifiants des effets de RESSOURCE que porte cette carte. C'est par eux
   * qu'on paie : une option d'action liste les effets de ressource acceptes
   * (EffectDescriptor.target_payment[cible].payment), et cliquer une carte qui
   * porte l'un d'eux le depense. Voir ask.ts.
   */
  resources: number[]
}

/** Les zones qui appartiennent a un joueur. */
export type WorldPlayer = {
  /** Identite (Hero ou AlterEgo) puis ses ameliorations attachees. */
  area_hero: WorldCard[]
  allies: WorldCard[]
  supports: WorldCard[]
  player_deck: WorldCard[]
  player_discard_pile: WorldCard[]
  dealt_encounter_cards: WorldCard[]
  hand_cards: WorldCard[]
  engaged_enemies: WorldCard[]
  set_aside_nemesis_sets: WorldCard[]
  set_aside_deck: WorldCard[]
  additional_deck: WorldCard[]
  additional_discard_pile: WorldCard[]
  obligations_area: WorldCard[]
  environment_area: WorldCard[]
  /** Chaine, et non liste : mesure faite sur une partie reelle (valeur ''). */
  resources: string
  is_eliminated: boolean
}

export type World = {
  /** Change a chaque rendu du moteur : sert a ne redessiner que si besoin. */
  render_id: number
  round_id: number
  phase: string
  /** Texte de l'evenement en cours, avec des references « [(id,card_id) Nom] ». */
  prompt: string
  prompt_last_text?: string
  sound_name?: string
  event_name: string
  area_schemes_main: WorldCard[]
  main_schemes_deck: WorldCard[]
  area_schemes_side: WorldCard[]
  /**
   * ATTENTION, au pluriel ce sont des LISTES DE DECKS, pas des listes de cartes :
   * une entree = un deck supplementaire entier. Les 34 etats enregistres avaient
   * tous ces deux zones vides, le piege ne s'y voit pas. Mesure faite sur une
   * partie reelle (scenario a decks supplementaires) : additional_decks[0] est un
   * tableau de 3 cartes.
   * Les equivalents SINGULIERS cote joueur (additional_deck,
   * additional_discard_pile) sont, eux, de simples listes de cartes.
   */
  additional_decks: WorldCard[][]
  additional_discard_piles: WorldCard[][]
  area_villain: WorldCard[]
  villain_deck: WorldCard[]
  encounter_deck: WorldCard[]
  encounter_discard_pile: WorldCard[]
  area_boost: WorldCard[]
  area_environment: WorldCard[]
  area_evidence: WorldCard[]
  area_rule: WorldCard[]
  area_processing: WorldCard[]
  area_revealing: WorldCard[]
  area_resources: WorldCard[]
  area_removed: WorldCard[]
  area_insert: WorldCard[]
  area_set_aside: WorldCard[]
  victory_display: WorldCard[]
  area_status_cards: WorldCard[]
  players: WorldPlayer[]
  /** Cartes citees par l'evenement en cours : le runtime les met en avant. */
  active_card_ids: number[]
  /** Partie terminee par une vraie victoire/defaite (pas Exit/Undo). */
  game_over?: boolean
  players_won?: boolean
  /** Texte du moteur : « The Final Stage of the Villain was Defeated »... */
  game_over_reason?: string
}

/** Familles de types, reprises telles quelles de descriptor.js. */
const UNIT_TYPES = ['Ally', 'Minion', 'EncounterVillain', 'Hero', 'AlterEgo']
const SCHEME_TYPES = ['MainScheme', 'EncounterSideScheme', 'PlayerSideScheme']

/**
 * Est-ce bien une carte ?
 *
 * Le contrat de /get_world n'est connu que par mesure, et il reserve des
 * surprises : `additional_decks` contient des DECKS la ou tout le reste contient
 * des cartes. Une zone d'une forme inattendue ne doit pas vider le plateau
 * entier, juste manquer a l'appel, et se compter (voir Plateau.nombreIgnore).
 */
export function estUneCarte(valeur: unknown): valeur is WorldCard {
  if (typeof valeur !== 'object' || valeur === null) return false
  const carte = valeur as Partial<WorldCard>
  return (
    typeof carte.id === 'number' &&
    typeof carte.card_type === 'string' &&
    typeof carte.pic_id === 'string' &&
    Array.isArray(carte.visible_for_players) &&
    Array.isArray(carte.down_card_ids)
  )
}

/** Un personnage : il a des points de vie. */
export function isUnit(card: WorldCard): boolean {
  return UNIT_TYPES.includes(card.card_type)
}

/** Un complot : il porte de la menace, et se pose en paysage. */
export function isScheme(card: WorldCard): boolean {
  return SCHEME_TYPES.includes(card.card_type)
}

/**
 * Avons-nous le droit de voir la face de cette carte ?
 * Reprend isVisible() du runtime, sans les reglages de debogage (siege partage,
 * mode spectateur, « montrer toutes les mains ») qui n'existent pas ici.
 */
export function isVisibleFor(card: WorldCard, playerId: number): boolean {
  return card.visible_for_players.includes(playerId)
}
