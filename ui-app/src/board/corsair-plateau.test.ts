// Corsair (Starjammers, cr001a) et Slave Pits of Chandilar (cr014) : ce que la table DESSINE (étape 8 bis de
// PROCESSUS-CARTE, leçon Contingency Plan).
//
// Pocket Universe Gems, Corsair's Rapier et Pulse Blaster GLISSENT des cartes SOUS L'IDENTITÉ de Corsair ; Slave Pits
// glisse FACE CACHÉE un allié ou un soutien PERSONA de chaque joueur sous la manigance annexe. Le joueur doit voir ce
// qu'il peut rejouer (Corsair) et ce qui est retenu en prison (Slave Pits). Le moteur émet les cartes glissées à la
// suite de leur hôte, liées par `bind_object_id` : `area_hero` pour l'identité (modèle `echo-photographic-reflexes`,
// glissée face cachée mais lisible par son propriétaire), `area_schemes_side` pour la manigance (modèle
// `mere-de-la-nuit-cartes-dessous`).
import { describe, expect, it } from 'vitest'
import { carteSurTable, cartesDessinees, dessinee, siege, tableAvec } from './plateau-de-test'

const CORSAIR = 1
const RAPIER = 2
const BLASTER = 3
const PITS = 40
const ALLIE = 41
const SOUTIEN = 42

const monde = () =>
  tableAvec(
    siege({
      area_hero: [
        carteSurTable(CORSAIR, 'cr001a', 'Hero', 'Corsair'),
        carteSurTable(RAPIER, 'cr003', 'Upgrade', "Corsair's Rapier", {
          bind_object_id: CORSAIR,
          is_face_up: false,
          visible_for_players: [0],
        }),
        carteSurTable(BLASTER, 'cr004', 'Upgrade', 'Pulse Blaster', {
          bind_object_id: CORSAIR,
          is_face_up: false,
          visible_for_players: [0],
        }),
      ],
    }),
    {
      area_schemes_side: [
        carteSurTable(PITS, 'cr014', 'SideScheme', 'Slave Pits of Chandilar'),
        carteSurTable(ALLIE, '01083', 'Ally', 'Mockingbird', {
          bind_object_id: PITS,
          is_face_up: false,
          visible_for_players: [],
        }),
        carteSurTable(SOUTIEN, '01026', 'Support', 'Superhuman Law Division', {
          bind_object_id: PITS,
          is_face_up: false,
          visible_for_players: [],
        }),
      ],
    }
  )

describe('Corsair, cartes glissées sous son identité', () => {
  it('dessine Corsair', () => {
    expect(dessinee(monde(), CORSAIR)).toBeDefined()
  })

  it('dessine les cartes glissées, portées par Corsair', () => {
    expect(dessinee(monde(), RAPIER)).toBeDefined()
    expect(dessinee(monde(), BLASTER)).toBeDefined()
    expect(dessinee(monde(), RAPIER)?.portePar).toBe(CORSAIR)
    expect(dessinee(monde(), BLASTER)?.portePar).toBe(CORSAIR)
  })

  it('les montre lisibles par leur propriétaire (face cachée, mais « peeking »), juste derrière Corsair', () => {
    const vues = cartesDessinees(monde())
    const rang = (id: number) => vues.findIndex((c) => c.id === id)
    expect(rang(RAPIER)).toBe(rang(CORSAIR) + 1)
    expect(rang(BLASTER)).toBe(rang(CORSAIR) + 2)
    expect(dessinee(monde(), RAPIER)?.peeking).toBe(true)
    expect(dessinee(monde(), RAPIER)?.facedown).toBe(false)
  })
})

describe('Slave Pits of Chandilar, cartes glissées dessous', () => {
  it('dessine la manigance et les cartes retenues, portées par elle', () => {
    expect(dessinee(monde(), PITS)).toBeDefined()
    expect(dessinee(monde(), ALLIE)).toBeDefined()
    expect(dessinee(monde(), SOUTIEN)).toBeDefined()
    expect(dessinee(monde(), ALLIE)?.portePar).toBe(PITS)
    expect(dessinee(monde(), SOUTIEN)?.portePar).toBe(PITS)
  })

  it('les montre face cachée, juste derrière la manigance', () => {
    const vues = cartesDessinees(monde())
    const rang = (id: number) => vues.findIndex((c) => c.id === id)
    expect(rang(ALLIE)).toBe(rang(PITS) + 1)
    expect(rang(SOUTIEN)).toBe(rang(PITS) + 2)
    expect(dessinee(monde(), ALLIE)?.facedown).toBe(true)
  })
})
