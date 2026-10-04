import { describe, expect, it } from 'vitest'
import { cartesConcernees, regleSurbrillance } from './surbrillance-etape'
import type { EtapeDeroule } from './deroule-phase'

const etape = (extra: Partial<EtapeDeroule>): EtapeDeroule => ({
  cle: 'x',
  temps: 'revelation',
  titre: 'revelation',
  regle: 'regle:revelation',
  boosts: [],
  ...extra,
})

describe('la surbrillance des cartes de l etape', () => {
  it('reunit la carte, sa cible et celles de ses consequences, sans doublon', () => {
    const e = etape({
      carteId: 54,
      consequences: [etape({ titre: 'manigance', carteId: 49, cibleId: 48 }), etape({ titre: 'statut', cibleId: 49 })],
    })
    expect(cartesConcernees(e)).toEqual([54, 49, 48])
  })

  it('ne cible que les cartes de la TABLE, par leur identifiant', () => {
    expect(regleSurbrillance([54])).toContain('.plateau-scene .scan-card[data-card-id="54"] .scan-frame')
    expect(regleSurbrillance([])).toBe('')
    expect(cartesConcernees(undefined)).toEqual([])
  })
})
