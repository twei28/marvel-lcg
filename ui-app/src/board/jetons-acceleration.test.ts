// Signalement Yarro n°45 (03/10/2026) : « Quand il est révélé, il n'y a pas
// d'acceleration token de placé dessus » (60200 Ivan Banionis, « When Revealed:
// Place 1 acceleration token here »). Le moteur posait bien le jeton (journal :
// « Ivan Banionis placed 1 'acceleration_token' token », etat
// `k_acceleration_token=1`) et le compte dans la menace de la phase du mechant ;
// le plateau, lui, ne lisait que les compteurs `c_...` : le jeton n'etait dessine
// nulle part, ni sur un sbire ni sur une manigance.
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

describe('les jetons d acceleration poses sur une carte', () => {
  it('Ivan Banionis montre son jeton d acceleration', () => {
    const ivan = carteSurTable(78, '60200', 'Minion', 'Ivan Banionis', {
      info: { k_acceleration_token: 1, max_health: 5, health: 5 },
    })
    const world = tableAvec(siege({ engaged_enemies: [ivan] }))
    expect(compteursDe(world, 78)).toContainEqual(expect.objectContaining({ cle: 'acceleration', value: 1 }))
  })

  it('plusieurs jetons : le nombre est porte par le compteur', () => {
    const ivan = carteSurTable(78, '60200', 'Minion', 'Ivan Banionis', {
      info: { k_acceleration_token: 3, max_health: 5, health: 5 },
    })
    const world = tableAvec(siege({ engaged_enemies: [ivan] }))
    expect(compteursDe(world, 78)).toContainEqual(expect.objectContaining({ cle: 'acceleration', value: 3 }))
  })

  it('zero jeton : rien a montrer', () => {
    const ivan = carteSurTable(78, '60200', 'Minion', 'Ivan Banionis', {
      info: { k_acceleration_token: 0, max_health: 5, health: 5 },
    })
    const world = tableAvec(siege({ engaged_enemies: [ivan] }))
    expect(compteursDe(world, 78).find((c) => c.cle === 'acceleration')).toBeUndefined()
  })
})
