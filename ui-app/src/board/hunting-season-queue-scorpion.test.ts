// Hunting Season, Scorpion (hs030) : la Queue (hs036) est attachée au vilain,
// et hs037/hs039/hs040 s'attachent à la Queue. Deux étages sous un vilain.
import { describe, expect, it } from 'vitest'
import { carteSurTable, cartesDessinees, dessinee, siege, tableAvec } from './plateau-de-test'

const SCORPION = 10
const QUEUE = 11
const ARMURE = 12
const LASER = 13

const monde = () =>
  tableAvec(siege(), {
    area_villain: [
      carteSurTable(SCORPION, 'hs030', 'Villain', '* Scorpion'),
      carteSurTable(QUEUE, 'hs036', 'Attachment', 'Scorpion’s Tail', { bind_object_id: SCORPION }),
      carteSurTable(ARMURE, 'hs037', 'Attachment', 'Tail Armor', { bind_object_id: QUEUE }),
      carteSurTable(LASER, 'hs039', 'Attachment', 'Tail Laser', { bind_object_id: QUEUE }),
    ],
  })

describe('Scorpion, sa Queue et les attachements de la Queue', () => {
  it('dessine la Queue et les deux cartes attachées à la Queue', () => {
    expect(dessinee(monde(), QUEUE)).toBeDefined()
    expect(dessinee(monde(), ARMURE)).toBeDefined()
    expect(dessinee(monde(), LASER)).toBeDefined()
  })

  it('les range dans l unité de Scorpion, la Queue d abord', () => {
    const vues = cartesDessinees(monde())
    const rang = (id: number) => vues.findIndex((c) => c.id === id)
    expect(dessinee(monde(), ARMURE)?.portePar).toBe(SCORPION)
    expect(rang(QUEUE)).toBe(rang(SCORPION) + 1)
    expect(rang(ARMURE)).toBeGreaterThan(rang(QUEUE))
    expect(rang(LASER)).toBeGreaterThan(rang(QUEUE))
  })
})
