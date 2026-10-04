// Signalement Yarro n°44 (03/10/2026) : « Quand tu descends les PV de Mary à 0,
// cela ne rajoute pas de tokens ». Le moteur posait bien le jeton (journal :
// « Disturbed Psyche placed 1 'damage' token », état `k_damage=1`), mais le
// plateau ne montrait les dégâts QUE par la jauge de PV des personnages : sur
// une carte sans PV (l'environnement 60112 Disturbed Psyche, dont 3 jetons font
// gagner la partie), ils n'apparaissaient nulle part.
import { describe, expect, it } from 'vitest'
import { construirePlateau } from './zones'
import { catalogueVide } from './catalogue'
import { carteSurTable, siege, tableAvec } from './plateau-de-test'
import type { World } from './world'

function compteursDe(world: World, id: number) {
  const plateau = construirePlateau(world, { playerId: 0, catalogue: catalogueVide })
  for (const e of plateau.emplacements)
    for (const g of e.groupes)
      for (const u of g) if (Number(u.carte.id) === id) return u.carte.counters ?? []
  throw new Error(`carte ${id} absente du plateau`)
}

describe('les jetons de degats sur une carte sans PV', () => {
  it('Disturbed Psyche montre son jeton de degats', () => {
    const psyche = carteSurTable(50, '60112', 'Environment', 'Disturbed Psyche', { info: { k_damage: 1 } })
    const world = tableAvec(siege(), { area_environment: [psyche] } as Partial<World>)
    expect(compteursDe(world, 50)).toContainEqual(expect.objectContaining({ cle: 'damage', value: 1 }))
  })

  it('un personnage garde sa jauge, sans jeton de degats en double', () => {
    const allie = carteSurTable(25, '21014', 'Ally', 'Kaluu', { info: { k_damage: 1, max_health: 2, health: 1 } })
    const world = tableAvec(siege({ allies: [allie] }))
    expect(compteursDe(world, 25).find((c) => c.cle === 'damage')).toBeUndefined()
  })

  it('zero jeton : rien a montrer', () => {
    const psyche = carteSurTable(50, '60112', 'Environment', 'Disturbed Psyche', { info: { k_damage: 0 } })
    const world = tableAvec(siege(), { area_environment: [psyche] } as Partial<World>)
    expect(compteursDe(world, 50).find((c) => c.cle === 'damage')).toBeUndefined()
  })
})
