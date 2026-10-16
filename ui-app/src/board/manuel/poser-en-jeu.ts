// poser-en-jeu.ts — où va une carte qu'on pose sur la table en mode manuel.
//
// Comme sur OCTGN, lâcher une carte sur la table la met en jeu (spec du
// 06/10/2026, `docs/superpowers/specs/2026-10-06-mode-manuel-comme-octgn-design.md`
// §D.3). Notre moteur ne connaît que des piles : cette table traduit le lâcher
// en UNE commande, sans vérifier aucune règle (coût, limite, cible).
//
// Fonction PURE : ni DOM ni réseau. Le glisser (`glisser-manuel.ts`) et le
// double-clic en main (`CoucheTriche.tsx`) l'appellent tous les deux, pour
// que les deux gestes posent la carte exactement au même endroit.
//
// ⚠ UNE GATE, PAS UN REPLI : un type absent de la table est refusé avec une
// raison nommée, jamais posé « quelque part ».
import { nomAffiche } from '../noms-cartes-fr'
import type { World, WorldCard } from '../world'

export type CibleAmelioration = { id: number; nom: string }

export type ContexteDePose = {
  /** Le siège du joueur chez qui la carte arrive (index dans `world.players`). */
  siege: number
  identite?: CibleAmelioration
  /** Les cartes en jeu de ce joueur qui peuvent porter une amélioration. */
  ciblesAmelioration: CibleAmelioration[]
}

export type Pose =
  | { genre: 'deplacer'; zone: string; siege?: number }
  | { genre: 'attacher'; cible: number }
  | { genre: 'choisir'; cibles: CibleAmelioration[] }
  | { genre: 'refus'; raison: string }

type Destination = { zone: string; duJoueur: boolean } | { refus: string } | 'amelioration'

const REFUS_RESSOURCE = 'Une ressource se défausse pour payer : Suppr, ou glisse-la sur ta défausse'
const REFUS_ACCOMPAGNE = 'Lâche-la sur la carte qu’elle accompagne'
const REFUS_TABLE = 'Cette carte ne se pose pas sur la table : glisse-la sur une pile ou fais Déplacer vers'

/**
 * Les types FINAUX du moteur (`card_type` = nom de la classe,
 * `game/card/face/base/final_type.py`), relevés le 06/10/2026.
 */
const TABLE: Record<string, Destination> = {
  Ally: { zone: 'AlliesArea', duJoueur: true },
  Support: { zone: 'SupportsArea', duJoueur: true },
  // La Voie (type imprime PATH, tj011) vit dans l'aire de soutien du joueur.
  Path: { zone: 'SupportsArea', duJoueur: true },
  Upgrade: 'amelioration',
  // Question 4 : à côté de son héros, en cours de résolution, puis Suppr.
  Event: { zone: 'PlayerProcessingArea', duJoueur: true },
  Minion: { zone: 'EngagedEnemiesArea', duJoueur: true },
  PlayerMinion: { zone: 'EngagedEnemiesArea', duJoueur: true },
  Obligation: { zone: 'ObligationsArea', duJoueur: true },
  Environment: { zone: 'EnvironmentArea', duJoueur: false },
  PlayerSideScheme: { zone: 'SideSchemesArea', duJoueur: false },
  EncounterSideScheme: { zone: 'SideSchemesArea', duJoueur: false },
  Treachery: { zone: 'ProcessingArea', duJoueur: false },
  Resource: { refus: REFUS_RESSOURCE },
  // Sans carte hôte, une pièce jointe (le dessus du deck Rencontre glissé sur
  // la table) attend en résolution, comme après Ctrl+D ; on la glisse ensuite
  // sur la carte qu'elle accompagne (06/10/2026).
  Attachment: { zone: 'ProcessingArea', duJoueur: false },
  Evidence: { refus: REFUS_ACCOMPAGNE },
  Hero: { refus: REFUS_TABLE },
  AlterEgo: { refus: REFUS_TABLE },
  EncounterVillain: { refus: REFUS_TABLE },
  Leader: { refus: REFUS_TABLE },
  MainScheme: { refus: REFUS_TABLE },
  StatusCard: { refus: REFUS_TABLE },
  Insert: { refus: REFUS_TABLE },
  Challenge: { refus: REFUS_TABLE },
}

export const TYPES_CONNUS: ReadonlySet<string> = new Set(Object.keys(TABLE))

/** Les types qui s'attachent quand on les lâche sur une carte (question 2). */
export const TYPES_QUI_S_ATTACHENT: ReadonlySet<string> = new Set(['Upgrade', 'Attachment'])

/** Les manigances : seules cartes que les zones de manigance acceptent. */
export const TYPES_MANIGANCE: ReadonlySet<string> = new Set(['MainScheme', 'PlayerSideScheme', 'EncounterSideScheme'])

export function poserEnJeu(carte: { id: number; type: string }, contexte: ContexteDePose): Pose {
  const destination = TABLE[carte.type]
  if (destination === undefined) return { genre: 'refus', raison: REFUS_TABLE }
  if (destination === 'amelioration') {
    // Question 3 : une seule cible (l'identité) = attache directe ; plusieurs
    // = le joueur choisit ; aucune = refus.
    const cibles = contexte.ciblesAmelioration
    if (cibles.length === 0) return { genre: 'refus', raison: 'Aucune carte en jeu ne peut recevoir cette amélioration' }
    if (cibles.length === 1) return { genre: 'attacher', cible: cibles[0].id }
    return { genre: 'choisir', cibles }
  }
  if ('refus' in destination) return { genre: 'refus', raison: destination.refus }
  return destination.duJoueur
    ? { genre: 'deplacer', zone: destination.zone, siege: contexte.siege }
    : { genre: 'deplacer', zone: destination.zone }
}

const cibleDe = (carte: WorldCard): CibleAmelioration => ({ id: Number(carte.id), nom: nomAffiche(carte) })

/** Le contexte du joueur assis au siège `siege`, lu dans la trame. */
export function contexteDePose(world: World | undefined, siege: number): ContexteDePose {
  const joueur = world?.players?.[siege]
  const identiteCarte = joueur?.area_hero?.find((carte) => carte.card_type === 'Hero' || carte.card_type === 'AlterEgo')
  const identite = identiteCarte ? cibleDe(identiteCarte) : undefined
  const allies = (joueur?.allies ?? []).filter((carte) => carte.card_type === 'Ally').map(cibleDe)
  // Les ennemis aussi (décision du 06/10/2026) : une amélioration peut viser
  // le méchant ou un sbire (Pris dans la Toile, Spider-Traceur). Le méchant
  // étant toujours là, la fenêtre de choix s'ouvre pour toute amélioration.
  const ennemis = [
    ...(world?.area_villain ?? []).filter((carte) => TYPES_MECHANT.has(carte.card_type)),
    ...(world?.players ?? []).flatMap((autre) =>
      (autre.engaged_enemies ?? []).filter((carte) => TYPES_SBIRE.has(carte.card_type))
    ),
  ].map(cibleDe)
  const duJoueur = identite ? [identite, ...allies] : allies
  return { siege, identite, ciblesAmelioration: [...duJoueur, ...ennemis] }
}

const TYPES_MECHANT: ReadonlySet<string | undefined> = new Set(['EncounterVillain', 'Leader'])
const TYPES_SBIRE: ReadonlySet<string | undefined> = new Set(['Minion', 'PlayerMinion'])

export type Origine = 'main' | 'resolution' | 'pile' | 'jeu'

const contient = (pile: WorldCard[] | undefined, id: number) => (pile ?? []).some((carte) => Number(carte.id) === id)

/**
 * D'où vient la carte : de la main, d'une zone de résolution, d'une pile
 * (deck, défausse, mises de côté...) ou déjà du jeu. `undefined` si la trame
 * ne la connaît pas.
 */
export function origineDe(world: World | undefined, id: number): Origine | undefined {
  if (!world) return undefined
  const joueurs = world.players ?? []
  if (joueurs.some((joueur) => contient(joueur.hand_cards, id))) return 'main'
  if (
    contient(world.area_processing, id) ||
    contient(world.area_revealing, id) ||
    joueurs.some((joueur) => contient(joueur.area_processing, id))
  ) {
    return 'resolution'
  }
  const pilesDuMonde: (WorldCard[] | undefined)[] = [
    world.encounter_deck, world.encounter_discard_pile, world.villain_deck, world.main_schemes_deck,
    world.area_removed, world.area_set_aside, world.victory_display, world.area_boost,
    ...(world.additional_decks ?? []), ...(world.additional_discard_piles ?? []),
  ]
  const pilesDesJoueurs = joueurs.flatMap((joueur) => [
    joueur.player_deck, joueur.player_discard_pile, joueur.set_aside_nemesis_sets, joueur.set_aside_deck,
    joueur.additional_deck, joueur.additional_discard_pile, joueur.reserve, joueur.rising_tide,
  ])
  if ([...pilesDuMonde, ...pilesDesJoueurs].some((pile) => contient(pile, id))) return 'pile'
  const enJeuDuMonde: (WorldCard[] | undefined)[] = [
    world.area_schemes_main, world.area_schemes_side, world.area_villain, world.area_environment,
    world.area_evidence, world.area_rule, world.area_resources, world.area_insert, world.area_status_cards,
  ]
  const enJeuDesJoueurs = joueurs.flatMap((joueur) => [
    joueur.area_hero, joueur.allies, joueur.supports, joueur.engaged_enemies, joueur.obligations_area,
    joueur.environment_area, joueur.dealt_encounter_cards,
  ])
  if ([...enJeuDuMonde, ...enJeuDesJoueurs].some((pile) => contient(pile, id))) return 'jeu'
  return undefined
}

/** La carte de la trame, pour son type et son nom. */
export function carteDeLaTrame(world: World | undefined, id: number): WorldCard | undefined {
  if (!world) return undefined
  const toutes: (WorldCard[] | undefined)[] = [
    world.area_schemes_main, world.main_schemes_deck, world.area_schemes_side, world.area_villain, world.villain_deck,
    world.encounter_deck, world.encounter_discard_pile, world.area_boost, world.area_environment, world.area_evidence,
    world.area_rule, world.area_processing, world.area_revealing, world.area_resources, world.area_removed,
    world.area_insert, world.area_set_aside, world.victory_display, world.area_status_cards,
    ...(world.additional_decks ?? []), ...(world.additional_discard_piles ?? []),
    ...(world.players ?? []).flatMap((joueur) => [
      joueur.area_hero, joueur.allies, joueur.supports, joueur.player_deck, joueur.player_discard_pile,
      joueur.dealt_encounter_cards, joueur.hand_cards, joueur.reserve, joueur.rising_tide, joueur.area_processing,
      joueur.engaged_enemies, joueur.set_aside_nemesis_sets, joueur.set_aside_deck, joueur.additional_deck,
      joueur.additional_discard_pile, joueur.obligations_area, joueur.environment_area,
    ]),
  ]
  for (const pile of toutes) {
    const trouvee = (pile ?? []).find((carte) => Number(carte.id) === id)
    if (trouvee) return trouvee
  }
  return undefined
}

/**
 * La carte est-elle cachée au joueur qui la manipule ? Face cachée ET hors de
 * la main : la trame marque aussi `is_face_up: false` les cartes EN MAIN, que
 * leur propriétaire voit pourtant (constaté le 06/10/2026 sur une partie
 * basculée : Black Cat en main annoncée « carte face cachée »).
 */
export function estCacheePourLeJoueur(world: World | undefined, id: number): boolean {
  const carte = carteDeLaTrame(world, id)
  return carte?.is_face_up === false && origineDe(world, id) !== 'main'
}

