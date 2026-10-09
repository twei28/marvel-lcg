import { describe, expect, it } from 'vitest'
import { detecterZoneTexte, texteEnHtml } from './traduction-posee'

/**
 * Une carte 300 x 420 sombre, avec une zone claire (240,236,228) de x 30..269,
 * y 240..374, des lignes de texte noires, et en option un badge orange plein
 * (PV d'un sbire) qui mord sur son coin haut droit.
 */
function carteFactice(avecZone = true, avecBadge = false): Uint8ClampedArray {
  const l = 300
  const h = 420
  const px = new Uint8ClampedArray(l * h * 4)
  for (let y = 0; y < h; y += 1) {
    for (let x = 0; x < l; x += 1) {
      const dedans = avecZone && x >= 30 && x <= 269 && y >= 240 && y <= 374
      const lettre = dedans && x >= 45 && x <= 250 && (y - 250) % 14 < 6 && y >= 250 && y <= 350 && x % 7 < 2
      const badge = avecBadge && (x - 255) ** 2 + (y - 240) ** 2 <= 22 ** 2
      const [r, g, b] = badge ? [230, 120, 30] : lettre ? [20, 20, 20] : dedans ? [240, 236, 228] : [60, 40, 90]
      px.set([r, g, b, 255], (y * l + x) * 4)
    }
  }
  return px
}

describe('detecterZoneTexte', () => {
  it('trouve la zone claire et sa couleur de fond', () => {
    const zone = detecterZoneTexte(carteFactice(), 300, 420)
    expect(zone).not.toBeNull()
    expect(zone!.x0).toBeCloseTo(30 / 300, 1)
    expect(zone!.x1).toBeCloseTo(270 / 300, 1)
    expect(zone!.y0).toBeCloseTo(240 / 420, 1)
    expect(zone!.y1).toBeCloseTo(375 / 420, 1)
    expect(zone!.fond).toEqual([240, 236, 228])
  })

  it('renonce sur une carte sans zone claire', () => {
    expect(detecterZoneTexte(carteFactice(false), 300, 420)).toBeNull()
  })

  it('laisse le badge hors du cache : le bord droit rentre sous lui, pas ailleurs', () => {
    const zone = detecterZoneTexte(carteFactice(true, true), 300, 420)!
    const ligne = (y: number) => zone.bords[Math.round(y - zone.y0 * 420)]
    // Sous le badge (y = 250, il commence à x = 235,4), le bord droit s'arrête avant lui.
    expect(ligne(250)[1] * 300).toBeLessThanOrEqual(236)
    // Plus bas (y = 320), la zone retrouve toute sa largeur.
    expect(ligne(320)[1] * 300).toBeGreaterThan(265)
  })
})

describe('texteEnHtml', () => {
  it('garde le gras, rend les icones et les traits, retire le reste', () => {
    const html = texteEnHtml('<b>Action</b> : [energy] → <script>x</script>[[AÉRIEN]]\nSuite [inconnu]')
    expect(html).toContain('<b>Action</b>')
    expect(html).toContain('<span class="tp-icone tp-icone-energy">E</span>')
    expect(html).toContain('<span class="tp-trait">AÉRIEN</span>')
    expect(texteEnHtml('[[DEFENDER]]')).toContain('DÉFENSEUR')
    expect(html).toContain('→')
    expect(html).not.toContain('<script>')
    expect(html).toContain('<br />Suite [inconnu]')
  })
})
