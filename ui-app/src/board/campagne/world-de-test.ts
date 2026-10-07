// Le monde minimal que les tests de campagne ont besoin de construire.
//
// Créé pour `PanneauRecompenses.multi.test.tsx`, qui rend le panneau entier.
// Les tests plus anciens gardent leurs propres gabarits : les déplacer ici
// serait un risque gratuit pour un gain de forme.
import type { World, WorldCard, WorldPlayer } from '../world'

const ZONES = {
  area_schemes_main: [],
  main_schemes_deck: [],
  area_schemes_side: [],
  additional_decks: [],
  additional_discard_piles: [],
  area_villain: [],
  villain_deck: [],
  encounter_deck: [],
  encounter_discard_pile: [],
  area_boost: [],
  area_environment: [],
  area_evidence: [],
  area_rule: [],
  area_processing: [],
  area_revealing: [],
  area_resources: [],
  area_removed: [],
  area_insert: [],
  area_set_aside: [],
  victory_display: [],
  area_status_cards: [],
  active_card_ids: [],
}

export function carteDeTest(
  id: number,
  nom: string,
  cardId: string,
  type: string,
  info: Record<string, number> = {}
): WorldCard {
  return {
    id,
    is_ready: true,
    is_face_up: true,
    visible_for_players: [0],
    bind_object_id: 0,
    name: nom,
    info,
    traits: {},
    buffs: {},
    card_id: cardId,
    pic_id: cardId,
    down_card_ids: [],
    card_type: type,
    cost: 0,
    resources: [],
  }
}

export function siegeDeTest(surcharge: Partial<WorldPlayer> = {}): WorldPlayer {
  return {
    area_hero: [],
    allies: [],
    supports: [],
    player_deck: [],
    player_discard_pile: [],
    dealt_encounter_cards: [],
    hand_cards: [],
    engaged_enemies: [],
    set_aside_nemesis_sets: [],
    set_aside_deck: [],
    additional_deck: [],
    additional_discard_pile: [],
    obligations_area: [],
    environment_area: [],
    resources: '',
    is_eliminated: false,
    ...surcharge,
  }
}

/** Une table à deux héros, partie gagnée, rien de particulier en jeu. */
export function mondeDeTest(surcharge: Partial<World> = {}): World {
  return {
    render_id: 12,
    round_id: 4,
    phase: 'End Round',
    prompt: '',
    event_name: 'PlayerOnEvent_Text',
    // Les tests de ce dossier jouent une partie de campagne ; ceux d'une partie
    // ordinaire passent `mode_campaign: false`.
    mode_campaign: true,
    ...ZONES,
    players: [
      siegeDeTest({ area_hero: [carteDeTest(1, 'Spider-Man', '01001a', 'Hero', { health: 10 })] }),
      siegeDeTest({ area_hero: [carteDeTest(2, 'She-Hulk', '04001a', 'Hero', { health: 20 })] }),
    ],
    ...surcharge,
  }
}
