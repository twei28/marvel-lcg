import { describe, expect, it } from 'vitest'
import { detecterZoneTexte, detecterZoneTextePaysage, texteEnHtml } from './traduction-posee'

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

/**
 * Une manigance PAYSAGE 420 x 300 : illustration sombre, boîte de texte VERTE
 * pâle (220,240,190) à gauche, x 15..225, y 70..265, sous un onglet noir ; des
 * lignes de texte, un badge plein contre le bord droit en bas (x 200..225,
 * y 200..265), et en option une icône seule sous le texte (x 100..125, y 225..252).
 */
function manigance(avecIcone: boolean): Uint8ClampedArray {
  const l = 420
  const h = 300
  const px = new Uint8ClampedArray(l * h * 4)
  for (let y = 0; y < h; y += 1) {
    for (let x = 0; x < l; x += 1) {
      const boite = x >= 15 && x <= 225 && y >= 70 && y <= 265
      const onglet = y >= 55 && y <= 66 && x >= 15 && x <= 110
      const lettre = boite && x >= 25 && x <= 190 && y >= 80 && y <= 190 && (y - 80) % 14 < 6 && x % 6 < 2
      const badge = x >= 200 && x <= 225 && y >= 200 && y <= 265
      const icone = avecIcone && x >= 100 && x <= 125 && y >= 225 && y <= 252
      const sombre = onglet || lettre || badge || icone
      const [r, g, b] = sombre ? [15, 15, 15] : boite ? [220, 240, 190] : [70 + (x % 40), 40, 110]
      px.set([r, g, b, 255], (y * l + x) * 4)
    }
  }
  return px
}

describe('detecterZoneTextePaysage', () => {
  it('trouve la boîte colorée de la manigance principale, sous son onglet', () => {
    const zone = detecterZoneTextePaysage(manigance(false), 420, 300, 'gauche')!
    expect(zone).not.toBeNull()
    expect(zone.x0 * 420).toBeLessThanOrEqual(18)
    expect(zone.x1 * 420).toBeGreaterThanOrEqual(222)
    expect(zone.y0 * 300).toBeGreaterThanOrEqual(66)
    expect(zone.y0 * 300).toBeLessThanOrEqual(74)
    expect(zone.fond).toEqual([220, 240, 190])
  })

  it('creuse une encoche sous le badge collé au bord, sans toucher au haut', () => {
    const zone = detecterZoneTextePaysage(manigance(false), 420, 300, 'gauche')!
    const ligne = (y: number) => zone.bords[Math.round(y - zone.y0 * 300)]
    expect(ligne(240)[1] * 420).toBeLessThanOrEqual(200)
    expect(ligne(120)[1] * 420).toBeGreaterThan(220)
  })

  it('laisse visible une icône quand plus rien n’est écrit dessous', () => {
    const zone = detecterZoneTextePaysage(manigance(true), 420, 300, 'gauche')!
    expect(zone.y1 * 300).toBeLessThanOrEqual(225)
  })

  it('renonce sans boîte claire', () => {
    const px = manigance(false)
    for (let k = 0; k < px.length; k += 4) px.set([60, 30, 90, 255], k)
    expect(detecterZoneTextePaysage(px, 420, 300, 'gauche')).toBeNull()
  })
})
