import { describe, expect, it } from 'vitest'
import { cadreDesLettres, effacerTexte } from './effacer-texte'

/** Une région blanche de 200×100 : des « lettres » (petits pavés noirs) en lignes, et un grand pavé (l'illustration). */
function region() {
  const largeur = 200
  const hauteur = 100
  const rgba = new Uint8ClampedArray(largeur * hauteur * 4).fill(255)
  const peindre = (x0: number, y0: number, x1: number, y1: number, v = 20) => {
    for (let y = y0; y < y1; y += 1) for (let x = x0; x < x1; x += 1) rgba.set([v, v, v, 255], (y * largeur + x) * 4)
  }
  for (const y of [20, 35, 50]) for (let x = 30; x < 150; x += 8) peindre(x, y, x + 4, y + 7)
  peindre(165, 10, 198, 95) // illustration qui mord sur le cadre
  return { rgba, largeur, hauteur, lum: (x: number, y: number) => rgba[(y * largeur + x) * 4] }
}

describe('effacerTexte', () => {
  it('efface les lettres, garde la grande forme, et rend le rectangle du texte', () => {
    const r = region()
    const cadre = effacerTexte(r.rgba, r.largeur, r.hauteur, { largeurCarte: 300, hauteurCarte: 420 })
    expect(r.lum(32, 23)).toBeGreaterThan(200) // une lettre : effacée
    expect(r.lum(180, 50)).toBeLessThan(60) // l'illustration : intacte
    expect(cadre).not.toBeNull()
    expect(cadre!.x0).toBeCloseTo(30 / 200, 1)
    expect(cadre!.y0).toBeCloseTo(20 / 100, 1)
    expect(cadre!.x1).toBeLessThan(165 / 200)
    expect(cadre!.bas).toBeGreaterThan(cadre!.y1)
  })

  it('ne touche pas une région sans texte', () => {
    const r = region()
    const vide = new Uint8ClampedArray(r.rgba.length).fill(240)
    expect(effacerTexte(vide, r.largeur, r.hauteur, { largeurCarte: 300, hauteurCarte: 420 })).toBeNull()
    expect(vide.every((v) => v === 240)).toBe(true)
  })
})

describe('cadreDesLettres', () => {
  it('une tache isolée au bord d\'une ligne (éclat du cadre) ne repousse pas la marge', () => {
    const lettres = [20, 30, 40, 50].flatMap((y) => [40, 50, 60, 70, 80].map((x) => ({ x0: x, x1: x + 6, y0: y, y1: y + 7 })))
    lettres.push({ x0: 2, x1: 5, y0: 30, y1: 37 })
    expect(cadreDesLettres(lettres, 300, 420)!.x0).toBe(40)
  })
})
