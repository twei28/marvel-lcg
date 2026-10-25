import { describe, expect, it } from 'vitest'
import { detecterZoneTexte, detecterZoneTextePaysage, prolongerVersLeHaut, texteEnHtml, zoneDansLeCadre, type ZoneTexte } from './traduction-posee'

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

describe('detecterZoneTexte : texte sous un filet de séparation', () => {
  /** Comme carteFactice, mais un filet sombre (y 354..355) coupe la zone et une ligne « Boost » s'écrit dessous. */
  function carteAvecBoost(avecTexteDessous: boolean): Uint8ClampedArray {
    const px = carteFactice()
    for (let y = 354; y <= 355; y += 1) for (let x = 30; x <= 269; x += 1) px.set([40, 40, 40, 255], (y * 300 + x) * 4)
    if (avecTexteDessous) {
      for (let y = 362; y < 370; y += 1) for (let x = 45; x <= 250; x += 1) if (x % 7 < 2) px.set([20, 20, 20, 255], (y * 300 + x) * 4)
    }
    return px
  }

  it('descend sous le filet jusqu\'à la ligne de texte qui s\'y écrit', () => {
    const zone = detecterZoneTexte(carteAvecBoost(true), 300, 420)!
    expect(zone.y1 * 420).toBeGreaterThan(369)
    expect(zone.y1 * 420).toBeLessThan(375)
  })

  it('ne descend pas quand rien n\'est écrit sous le filet', () => {
    const zone = detecterZoneTexte(carteAvecBoost(false), 300, 420)!
    expect(zone.y1 * 420).toBeLessThan(358)
  })
})

describe('prolongerVersLeHaut', () => {
  const l = 100
  const h = 200
  /** Une image claire dont les rangées de `sombres` sont du texte noir clairsemé, et les rangées de `bords` une bordure sombre pleine. */
  function image(sombres: number[], bords: number[] = []) {
    const px = new Uint8ClampedArray(l * h * 4).fill(255)
    const clair = new Uint8Array(l * h).fill(1)
    const peindre = (y: number, plein: boolean) => {
      for (let x = 0; x < l; x += 1) {
        if (!plein && x % 8 >= 2) continue
        px.set([10, 10, 10, 255], (y * l + x) * 4)
        clair[y * l + x] = 0
      }
    }
    sombres.forEach((y) => peindre(y, false))
    bords.forEach((y) => peindre(y, true))
    return { px, clair }
  }

  it('monte sur la ligne de traits écrite sous la bordure du cadre, au-dessus de la zone', () => {
    const { px, clair } = image([93, 94, 95], [89])
    expect(prolongerVersLeHaut(px, clair, l, h, 5, 95, 100)).toBe(92)
  })

  it('ne franchit pas la bordure : le titre au-dessus reste visible', () => {
    const { px, clair } = image([80, 81, 93, 94], [89, 90])
    expect(prolongerVersLeHaut(px, clair, l, h, 5, 95, 100)).toBe(92)
  })

  it('ne monte pas sans frontière dans la limite : c\'est l\'illustration', () => {
    const { px, clair } = image([88, 90, 92, 94, 96])
    expect(prolongerVersLeHaut(px, clair, l, h, 5, 95, 100)).toBe(100)
  })
})

describe('zoneDansLeCadre', () => {
  const zone: ZoneTexte = { x0: 0.1, y0: 0.5, x1: 0.9, y1: 0.9, fond: [255, 255, 255], bords: [[0.1, 0.9], [0.2, 0.8]] }
  // Le cadre d'une carte : 176 / 127 de haut en large.
  const cadre = { largeur: 300, hauteur: 416 }

  it('ne change rien quand le scan a le rapport du cadre', () => {
    expect(zoneDansLeCadre(zone, { largeur: 300, hauteur: 416 }, cadre)).toBe(zone)
  })

  it('un scan plus haut que le cadre est rogné en haut et en bas : le bas de la zone descend dans le cadre', () => {
    // 615 x 882 -> 300 x 430,2 : 7 px rognés en haut et en bas.
    const vue = zoneDansLeCadre(zone, { largeur: 615, hauteur: 882 }, cadre)
    expect(vue.y1 * 416).toBeCloseTo((0.9 * 430.24 - 7.12), 1)
    expect(vue.y1).toBeGreaterThan(zone.y1)
    expect(vue.y0).toBeCloseTo(zone.y0, 2)
    expect(vue.x0).toBe(zone.x0)
    expect(vue.bords).toEqual(zone.bords)
  })

  it('un scan plus large que le cadre est rogné à gauche et à droite', () => {
    const vue = zoneDansLeCadre(zone, { largeur: 450, hauteur: 600 }, cadre)
    expect(vue.x0).toBeLessThan(zone.x0)
    expect(vue.x1).toBeGreaterThan(zone.x1)
    expect(vue.y0).toBe(zone.y0)
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
