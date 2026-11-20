// Les fleches de la phase visent aussi les ronds du plateau telephone (24/10/2026).
import { describe, expect, it } from 'vitest'
import { carteDeLaTable } from './FlechesPhase'

describe('carteDeLaTable sur le plateau en ronds', () => {
  it('trouve le rond de la carte, pas son rond face cachee', () => {
    document.body.innerHTML = `<div class="plateau-cadre">
      <div class="rond est-cachee" data-card-id="7"></div>
      <div class="rond" data-card-id="7" id="bon"></div>
    </div>`
    expect(carteDeLaTable(7)?.id).toBe('bon')
  })
  it('ignore la copie dans le panneau de phase', () => {
    document.body.innerHTML = `<div class="plateau-cadre"><div class="deroule-phase"><div class="rond" data-card-id="3"></div></div></div>`
    expect(carteDeLaTable(3)).toBeUndefined()
  })
})
