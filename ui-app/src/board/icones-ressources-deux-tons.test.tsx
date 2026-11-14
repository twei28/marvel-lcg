import { describe, expect, it } from 'vitest'
import { render } from '@testing-library/react'
import { avecIcones, TONS_RESSOURCES } from './icones-ressources'

// Les icones de ressources en deux tons (20/10/2026) : fond de la couleur de
// la ressource, picto dans une teinte voisine, comme imprimees sur les cartes.
const ATTENDU = {
  P: { cle: 'physical', fond: '#9f2115', picto: '#f0a590' },
  M: { cle: 'mental', fond: '#5c63a5', picto: '#d0d5ec' },
  E: { cle: 'energy', fond: '#e6bf4f', picto: '#6b5a14' },
  W: { cle: 'wild', fond: '#296329', picto: '#78c872' },
  L: { cle: 'lightning', fond: '#2a7fc0', picto: '#d6f0ff' },
} as const

describe('les icones de ressources en deux tons', () => {
  for (const [marqueur, att] of Object.entries(ATTENDU)) {
    it(`${att.cle} recoit son fond et son picto`, () => {
      const { container } = render(<span>{avecIcones(`⟦${marqueur}⟧`)}</span>)
      const icone = container.querySelector('i.icone-res') as HTMLElement
      expect(icone.classList.contains('deux-tons')).toBe(true)
      expect(icone.classList.contains(`res-${att.cle}`)).toBe(true)
      expect(icone.style.getPropertyValue('--res-fond')).toBe(att.fond)
      expect(icone.style.getPropertyValue('--res-picto')).toBe(att.picto)
    })
  }

  it("garde l'eclair distinct de l'energie, et chaque ressource distincte", () => {
    const fonds = Object.values(TONS_RESSOURCES).map((t) => t.fond)
    expect(new Set(fonds).size).toBe(5)
  })

  it('le picto reste lisible sur son fond (contraste >= 3)', () => {
    const lum = (h: string) => {
      const c = [1, 3, 5]
        .map((i) => parseInt(h.slice(i, i + 2), 16) / 255)
        .map((x) => (x <= 0.03928 ? x / 12.92 : ((x + 0.055) / 1.055) ** 2.4))
      return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]
    }
    for (const { fond, picto } of Object.values(TONS_RESSOURCES)) {
      const [a, b] = [lum(fond), lum(picto)].sort((x, y) => y - x)
      expect((a + 0.05) / (b + 0.05)).toBeGreaterThanOrEqual(3)
    }
  })
})
