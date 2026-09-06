// La BANDE de jauge posee au bord de la carte : PV pour les personnages,
// menace pour les complots.
//
// Elle double la pastille chiffree, qui reste : le chiffre dit la valeur exacte,
// la bande donne l'etat d'un coup d'oeil sur un plateau entier. Ce fichier ne
// teste que le CALCUL (card-model) ; le rendu est teste dans
// components/ScanCard.jauge.test.tsx.
//
// Trois regles portent tout :
//   - `remplissage` (0 -> 1) est la part de bande peinte ;
//   - `genre` dit dans quel sens lire le remplissage (plein = bon pour les PV,
//     plein = perdu pour la menace) ;
//   - `alarme` dit si la carte a le DROIT de pulser. Un vilain a l'agonie est
//     une bonne nouvelle : il ne pulse pas.
import { beforeEach, describe, expect, it } from 'vitest'
import { toScanCard, type ContexteCarte } from './card-model'
import { catalogueVide, type Catalogue } from './catalogue'
import { oublierReferencesMenace } from './jauge-reference'
import type { WorldCard } from './world'

function carte(type: string, info: Record<string, number>, id = 7): WorldCard {
  return {
    id,
    bind_object_id: 0,
    name: 'Une carte',
    info,
    traits: {},
    buffs: {},
    card_id: '01002',
    pic_id: '01002',
    down_card_ids: [],
    card_type: type,
    is_face_up: true,
    is_ready: true,
    visible_for_players: [0],
  } as unknown as WorldCard
}

const contexte = (cat: Catalogue = catalogueVide): ContexteCarte => ({
  playerId: 0,
  actives: new Set<number>(),
  catalogue: cat,
})

beforeEach(() => {
  oublierReferencesMenace()
})

describe('jauge de points de vie', () => {
  it('remplit la bande a la part de PV restants', () => {
    const c = toScanCard(carte('Ally', { health: 5, max_health: 10 }), contexte())
    expect(c.jauge).toEqual({ remplissage: 0.5, genre: 'pv', alarme: true })
  })

  it('donne une bande pleine a un personnage intact', () => {
    const c = toScanCard(carte('Hero', { health: 12, max_health: 12 }), contexte())
    expect(c.jauge?.remplissage).toBe(1)
  })

  it('refuse l alarme aux ennemis : un vilain mourant est une bonne nouvelle', () => {
    const c = toScanCard(carte('EncounterVillain', { health: 1, max_health: 20 }), contexte())
    expect(c.jauge?.alarme).toBe(false)
  })

  it('ne pose aucune bande sans maximum fiable, comme la pastille', () => {
    const c = toScanCard(carte('Ally', { health: 2 }), contexte())
    expect(c.jauge).toBeUndefined()
  })

  it('ne pose aucune bande sur des PV infinis, qui ne se jaugent pas', () => {
    const c = toScanCard(
      carte('Ally', { health: 4, max_health: 0, is_infinite_health: 1 }),
      contexte()
    )
    expect(c.jauge).toBeUndefined()
  })

  it('ne depasse jamais la bande pleine, meme sur-soigne', () => {
    const c = toScanCard(carte('Ally', { health: 9, max_health: 5 }), contexte())
    expect(c.jauge?.remplissage).toBe(1)
  })

  it('ne divulgue rien sur une carte face cachee', () => {
    const cachee = carte('Ally', { health: 1, max_health: 10 })
    const c = toScanCard({ ...cachee, is_face_up: false, visible_for_players: [] }, contexte())
    expect(c.jauge).toBeUndefined()
  })
})

describe('jauge de menace', () => {
  it('monte vers la cible du complot principal', () => {
    const c = toScanCard(carte('MainScheme', { k_threat: 9, target_threat: 12 }), contexte())
    expect(c.jauge).toEqual({ remplissage: 0.75, genre: 'menace', alarme: true })
  })

  it('plafonne a la bande pleine quand la menace deborde la cible', () => {
    const c = toScanCard(carte('MainScheme', { k_threat: 15, target_threat: 12 }), contexte())
    expect(c.jauge?.remplissage).toBe(1)
  })

  it('part pleine sur un complot annexe, faute de cible a atteindre', () => {
    const c = toScanCard(carte('EncounterSideScheme', { k_threat: 4 }), contexte())
    expect(c.jauge).toEqual({ remplissage: 1, genre: 'menace', alarme: true })
  })

  it('vide la bande d un complot annexe a mesure qu on le contre', () => {
    const arrivee = carte('EncounterSideScheme', { k_threat: 4 })
    toScanCard(arrivee, contexte())
    const contre = toScanCard(carte('EncounterSideScheme', { k_threat: 1 }), contexte())
    expect(contre.jauge?.remplissage).toBe(0.25)
  })

  it('garde une reference par carte POSEE, non par carte du catalogue', () => {
    // Deux exemplaires du meme complot : le premier monte a 4, le second arrive
    // a 2. Une reference tenue par card_id ferait passer le second pour a moitie
    // contre alors qu'il vient d'entrer en jeu.
    toScanCard(carte('EncounterSideScheme', { k_threat: 4 }, 7), contexte())
    const second = toScanCard(carte('EncounterSideScheme', { k_threat: 2 }, 8), contexte())
    expect(second.jauge?.remplissage).toBe(1)
  })

  it('remonte la reference si la menace repart a la hausse', () => {
    toScanCard(carte('EncounterSideScheme', { k_threat: 4 }), contexte())
    const remontee = toScanCard(carte('EncounterSideScheme', { k_threat: 6 }), contexte())
    expect(remontee.jauge?.remplissage).toBe(1)
  })

  it('refuse l alarme a un complot du JOUEUR, dont la menace n est pas un danger', () => {
    const c = toScanCard(carte('PlayerSideScheme', { k_threat: 3 }), contexte())
    expect(c.jauge?.alarme).toBe(false)
  })

  it('ne pose aucune bande sur un complot vide de menace et de reference', () => {
    const c = toScanCard(carte('EncounterSideScheme', { k_threat: 0 }), contexte())
    expect(c.jauge).toBeUndefined()
  })
})
