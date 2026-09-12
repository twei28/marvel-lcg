// La menace posee sur une carte qui n'est PAS un complot.
//
// Beat Cop (10029, « Policiere en Patrouille ») : « move 1 threat from a
// scheme to here ». Le moteur pose des jetons `threat` sur le soutien
// (`Faces.PlaceTokensOn([this], value, 'threat')`), publies en `info.k_threat`
// comme pour un complot. Mais la pastille et le jeton ne se calculaient que
// pour les complots : le joueur ne voyait pas ce que sa policiere avait pris
// (signale en jeu le 12/09/2026, capture a l'appui). Meme famille : Private
// Investigator (jj011), Iron Suit (hd016), Stealth (50035b), Alert Level
// (50090a/b), Supporting Actor (39029, un sbire).
import { describe, expect, it } from 'vitest'
import { toScanCard, type ContexteCarte } from './card-model'
import { catalogueVide } from './catalogue'
import type { WorldCard } from './world'

function carte(type: string, card_id: string, info: Record<string, number>): WorldCard {
  return {
    id: 7,
    bind_object_id: 0,
    name: 'Beat Cop',
    info,
    traits: {},
    buffs: {},
    card_id,
    pic_id: card_id,
    down_card_ids: [],
    card_type: type,
    is_face_up: true,
    visible_for_players: [0],
    resources: [],
    control_by: 0,
  } as unknown as WorldCard
}

const contexte = (): ContexteCarte => ({ playerId: 0, actives: new Set(), catalogue: catalogueVide })

describe('la menace sur une carte qui n’est pas un complot', () => {
  it('Beat Cop montre la menace qu’il a prise, sans cible', () => {
    const c = toScanCard(carte('Support', '10029', { k_threat: 3 }), contexte())
    expect(c.schemeThreat).toBe('3')
    expect(c.jetonMenace).toBe(3)
  })

  it('un soutien sans menace ne montre rien : pas de « 0 » sur chaque carte', () => {
    const c = toScanCard(carte('Support', '10029', { k_threat: 0 }), contexte())
    expect(c.schemeThreat).toBeUndefined()
    expect(c.jetonMenace).toBeUndefined()
    const sans = toScanCard(carte('Support', '10029', {}), contexte())
    expect(sans.schemeThreat).toBeUndefined()
  })

  it('un sbire qui garde de la menace (Supporting Actor) la montre aussi', () => {
    const c = toScanCard(carte('Minion', '39029', { k_threat: 2, health: 3, max_health: 3 }), contexte())
    expect(c.schemeThreat).toBe('2')
  })

  it('un complot garde son rapport courant / cible, zero compris', () => {
    const principal = toScanCard(carte('MainScheme', '01097a', { k_threat: 0, target_threat: 7 }), contexte())
    expect(principal.schemeThreat).toBe('0/7')
    const annexe = toScanCard(carte('EncounterSideScheme', '01098', { k_threat: 0 }), contexte())
    expect(annexe.schemeThreat).toBe('0')
  })
})
