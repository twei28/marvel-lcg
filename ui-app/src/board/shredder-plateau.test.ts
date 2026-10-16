// Shredder (TMNT, `ts`) : ce que le plateau DESSINE une fois les cartes resolues.
//
// `tools/cas/tmnt_shredder.py` prouve ce que le moteur FAIT ; ce fichier prouve ce que le joueur REGARDE
// (PROCESSUS-CARTE.md, etape 8 bis). On pose a la main l'etat d'arrivee que le moteur publie, et on affirme sur
// `dessinee(...)`. La regle des PLUSIEURS cartes Cloaked sur Shredder (2, 3 ou 4 selon le stade) est le point
// neuf : chaque carte d'etat doit etre dessinee, pas seulement la premiere.
import { describe, expect, it } from 'vitest'
import { carteSurTable as carte, dessinee, siege, tableAvec } from './plateau-de-test'

const IDENTITE = 1
const VILAIN = 70
const identite = () => carte(IDENTITE, '01001a', 'Hero', 'Spider-Man')

describe('ts001-ts003 Shredder : plusieurs cartes Cloaked sur le vilain', () => {
  const monde = () =>
    tableAvec(siege({ area_hero: [identite()] }), {
      area_villain: [
        carte(VILAIN, 'ts003', 'EncounterVillain', 'Shredder'),
        carte(71, 'cloaked', 'StatusCard', 'Cloaked', { bind_object_id: VILAIN }),
        carte(72, 'cloaked', 'StatusCard', 'Cloaked', { bind_object_id: VILAIN }),
        carte(73, 'cloaked', 'StatusCard', 'Cloaked', { bind_object_id: VILAIN }),
        carte(74, 'cloaked', 'StatusCard', 'Cloaked', { bind_object_id: VILAIN }),
      ],
    })

  it('les QUATRE cartes Cloaked de Shredder III sont dessinees, portees par le vilain', () => {
    for (const id of [71, 72, 73, 74]) {
      const vue = dessinee(monde(), id)
      expect(vue).toBeDefined()
      expect(vue?.kind).toBe('status')
      expect(vue?.codeCarte).toBe('cloaked')
      expect(vue?.portePar).toBe(VILAIN)
    }
  })
})

describe('ts006 Bladed Armor, ts007 Kuro Kabuto : attaches au vilain', () => {
  const monde = () =>
    tableAvec(siege({ area_hero: [identite()] }), {
      area_villain: [
        carte(VILAIN, 'ts002', 'EncounterVillain', 'Shredder'),
        carte(80, 'ts006', 'Attachment', 'Bladed Armor', { bind_object_id: VILAIN }),
        carte(81, 'ts007', 'Attachment', 'Kuro Kabuto', { bind_object_id: VILAIN }),
        carte(82, 'cloaked', 'StatusCard', 'Cloaked', { bind_object_id: VILAIN }),
      ],
    })

  it('les deux attachements et la carte d\'etat sont tous dessines sur Shredder', () => {
    for (const id of [80, 81, 82]) {
      expect(dessinee(monde(), id)).toBeDefined()
      expect(dessinee(monde(), id)?.portePar).toBe(VILAIN)
    }
    expect(dessinee(monde(), 80)?.kind).toBe('attachment')
  })
})

describe('ts103 Kira no Ken : attachee a Karai (sbire), qui est elle-meme Cloaked', () => {
  const monde = () =>
    tableAvec(
      siege({
        area_hero: [identite()],
        engaged_enemies: [
          carte(60, 'ts101', 'Minion', 'Karai'),
          carte(61, 'ts103', 'Attachment', 'Kira no Ken', { bind_object_id: 60 }),
          carte(62, 'cloaked', 'StatusCard', 'Cloaked', { bind_object_id: 60 }),
        ],
      }),
      { area_villain: [carte(VILAIN, 'ts001', 'EncounterVillain', 'Shredder')] }
    )

  it('Kira no Ken et la carte Cloaked sont dessinees sous Karai', () => {
    expect(dessinee(monde(), 61)?.portePar).toBe(60)
    expect(dessinee(monde(), 62)?.portePar).toBe(60)
    expect(dessinee(monde(), 62)?.kind).toBe('status')
  })
})

describe('ts201 Bebop, ts205 Rocksteady : boost « deal this card to the first player »', () => {
  const monde = () =>
    tableAvec(
      siege({
        area_hero: [identite()],
        dealt_encounter_cards: [
          carte(64, 'ts201', 'Minion', 'Bebop', { is_face_up: false, visible_for_players: [] }),
          carte(65, 'ts205', 'Minion', 'Rocksteady', { is_face_up: false, visible_for_players: [] }),
        ],
      }),
      { area_villain: [carte(VILAIN, 'ts001', 'EncounterVillain', 'Shredder')] }
    )

  it('les deux sbires donnes face cachee ne montrent que le dos (aucun nom de carte)', () => {
    for (const id of [64, 65]) {
      const vue = dessinee(monde(), id)
      expect(vue).toBeDefined()
      expect(vue?.facedown).toBe(true)
      expect(vue?.codeCarte).toBeUndefined()
    }
  })
})
