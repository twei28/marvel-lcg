import { describe, expect, it } from 'vitest'
import { VOILE_UNI, ZONES_MANUELLES, corrigerZone } from './zones-corrections'

// Zones relevées à la main le 26/10/2026 sur Smasher (sz), Sunspot Hellfire (so), Silver Surfer (sv) et She-Hulk « Why Not » (wn).
const CODES = ['so014', 'sz012', 'sz013', 'sz003', 'sz006', 'sv007', 'sv011', 'sv015', 'wn001a', 'wn001b', 'wn002', 'wn003', 'wn004', 'wn006', 'wn009', 'wn010']
// She-Hulk « Why Not » : bandes adhésives manuscrites DANS le cadre de texte, que l'effacement des lettres ne peut pas rendre propre.
const AVEC_ADHESIF = ['wn001a', 'wn001b', 'wn002', 'wn003', 'wn004', 'wn006', 'wn009', 'wn010']

describe('zones relevées : Smasher, Sunspot, Silver Surfer, She-Hulk « Why Not »', () => {
  it.each(CODES)('%s : une zone manuelle dans l\'image, sans rien à détecter', (code) => {
    const m = ZONES_MANUELLES[code]
    expect(m).toBeDefined()
    expect(m!.x0).toBeGreaterThanOrEqual(0)
    expect(m!.x1).toBeLessThanOrEqual(1)
    expect(m!.x0).toBeLessThan(m!.x1)
    expect(m!.y0).toBeLessThan(m!.y1)
    expect(corrigerZone(code, null)).not.toBeNull()
  })

  it('la zone de so014 laisse libre le bandeau du bas (« SUNSPOT NEMESIS ») et les pictogrammes de menace', () => {
    expect(ZONES_MANUELLES.so014!.y1).toBeLessThanOrEqual(0.92)
  })

  it('la manigance couchée sz012 garde son titre et son onglet « SIDE SCHEME » hors du voile', () => {
    expect(ZONES_MANUELLES.sz012!.y0).toBeGreaterThan(0.25)
  })

  it.each(AVEC_ADHESIF)('%s : voile uni (adhésif manuscrit dans le cadre)', (code) => {
    expect(VOILE_UNI.has(code)).toBe(true)
  })
})
