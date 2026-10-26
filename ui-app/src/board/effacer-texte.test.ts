import { describe, expect, it } from 'vitest'
import { inflateSync } from 'node:zlib'
import { BANDES_DROITE, cadreDesLettres, effacerTexte } from './effacer-texte'
import { BG001A_TIRET, SY024_TRAIT, SZ004_GUILLEMET } from './effacer-texte.fixtures'

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

/** Les vrais pixels d'une région de scan (fixtures), décompressés. */
function pixelsDe(f: { largeur: number; hauteur: number; deflate: string }) {
  return new Uint8ClampedArray(inflateSync(Buffer.from(f.deflate, 'base64')))
}
const lum = (rgba: Uint8ClampedArray, largeur: number, x: number, y: number) => {
  const i = (y * largeur + x) * 4
  return (rgba[i] + rgba[i + 1] + rgba[i + 2]) / 3
}
/** Réglages de TraductionPosee.fondNettoye pour une carte de 593 × 850. */
const REGLAGES = { margeHaut: 10, margeBas: 10, margeCote: 14 }

describe('effacerTexte sur de vrais scans (26/10/2026)', () => {
  it('bg001a : le tiret « — » anglais entre deux mots est effacé (il restait sous le français)', () => {
    const f = BG001A_TIRET
    const rgba = pixelsDe(f)
    expect(lum(rgba, f.largeur, 80, 24)).toBeLessThan(140) // le tiret (26 × 2 px) est bien là au départ
    effacerTexte(rgba, f.largeur, f.hauteur, { largeurCarte: f.largeurCarte, hauteurCarte: f.hauteurCarte, ...REGLAGES })
    expect(lum(rgba, f.largeur, 80, 24)).toBeGreaterThan(190)
  })

  it('sy024 : le trait de la première lettre de la dernière ligne, collée au bord du cadre, est effacé', () => {
    const f = SY024_TRAIT
    const rgba = pixelsDe(f)
    // Le trait vertical (3 × 19 px) du scan : x 23-25, y 30-49 dans la fixture (x 53-55, y 255-274 de la région).
    expect(lum(rgba, f.largeur, 24, 40)).toBeLessThan(120)
    effacerTexte(rgba, f.largeur, f.hauteur, { largeurCarte: f.largeurCarte, hauteurCarte: f.hauteurCarte, ...REGLAGES })
    expect(lum(rgba, f.largeur, 24, 40)).toBeGreaterThan(190)
  })

  it('sz004 : le guillemet anglais isolé au bout d\'une ligne, près du bord droit du cadre, est effacé', () => {
    const f = SZ004_GUILLEMET
    const rgba = pixelsDe(f)
    // Les deux petits traits du guillemet fermant : x 520-525, y 73-79 de la région, soit x 520-525, y 43-49 de la fixture (région découpée de la ligne 30 à la ligne 140).
    const sombre = () => Math.min(...[520, 521, 523, 524, 525].flatMap((x) => [44, 46, 48].map((y) => lum(rgba, f.largeur, x, y))))
    expect(sombre()).toBeLessThan(150)
    effacerTexte(rgba, f.largeur, f.hauteur, { largeurCarte: f.largeurCarte, hauteurCarte: f.hauteurCarte, ...REGLAGES })
    expect(sombre()).toBeGreaterThan(190)
  })
})

describe('effacerTexte : bord gauche des lignes (cadre en pente, 26/10/2026)', () => {
  /** Des lignes de lettres (pavés 4×7, pas de 8) qui commencent à `departs[i]`, une ligne tous les 15 px à partir de y = 15. */
  function lignesEn(departs: number[]) {
    const largeur = 200
    const hauteur = 100
    const rgba = new Uint8ClampedArray(largeur * hauteur * 4).fill(255)
    departs.forEach((debut, i) => {
      const y = 15 + 15 * i
      for (let x = debut; x < 150; x += 8) for (let yy = y; yy < y + 7; yy += 1) for (let xx = x; xx < x + 4; xx += 1) rgba.set([20, 20, 20, 255], (yy * largeur + xx) * 4)
    })
    return { rgba, largeur, hauteur }
  }
  const bande = (y: number, hauteur = 100) => Math.floor((y / hauteur) * BANDES_DROITE)

  it('rend, par bande, où commencent les lignes : le haut commence plus à droite quand le cadre penche', () => {
    const r = lignesEn([50, 46, 42, 38, 34])
    const cadre = effacerTexte(r.rgba, r.largeur, r.hauteur, { largeurCarte: 300, hauteurCarte: 420 })!
    expect(cadre.gauche).toHaveLength(BANDES_DROITE)
    expect(cadre.gauche[bande(18)]).toBeGreaterThan(cadre.gauche[bande(78)] + 0.04)
    expect(Math.min(...cadre.gauche)).toBeCloseTo(cadre.x0, 2)
  })

  it('des lignes qui commencent toutes au même endroit ne laissent aucun décalage', () => {
    const r = lignesEn([40, 40, 40, 40, 40])
    const cadre = effacerTexte(r.rgba, r.largeur, r.hauteur, { largeurCarte: 300, hauteurCarte: 420 })!
    expect(Math.max(...cadre.gauche) - Math.min(...cadre.gauche)).toBeLessThan(0.005)
  })

  it('des départs irréguliers (retrait de première ligne, ligne en gras) ne sont pas une pente : aucun décalage', () => {
    const r = lignesEn([52, 52, 40, 40, 40])
    const cadre = effacerTexte(r.rgba, r.largeur, r.hauteur, { largeurCarte: 300, hauteurCarte: 420 })!
    expect(Math.max(...cadre.gauche) - Math.min(...cadre.gauche)).toBeLessThan(0.005)
  })
})

describe('effacerTexte : dernière ligne faite d\'un mot en italique (26/10/2026)', () => {
  /** Deux lignes de lettres séparées, puis une ligne d'UN mot en italique dont les lettres collées ne font que deux taches (« bestowed. »). */
  function avecMotCollé() {
    const largeur = 200
    const hauteur = 120
    const rgba = new Uint8ClampedArray(largeur * hauteur * 4).fill(255)
    const peindre = (x0: number, y0: number, x1: number, y1: number) => {
      for (let y = y0; y < y1; y += 1) for (let x = x0; x < x1; x += 1) rgba.set([20, 20, 20, 255], (y * largeur + x) * 4)
    }
    for (const y of [20, 35]) for (let x = 30; x < 150; x += 8) peindre(x, y, x + 4, y + 7)
    // Le mot : deux taches larges et basses (lettres collées), à la suite du texte, à gauche de la colonne.
    peindre(30, 52, 52, 60)
    peindre(56, 52, 80, 60)
    // Une tache isolée loin sous le texte (hors de la colonne) : ce n'est pas du texte.
    peindre(120, 108, 150, 116)
    return { rgba, largeur, hauteur, lum: (x: number, y: number) => rgba[(y * largeur + x) * 4] }
  }

  it('efface un mot de deux taches collées qui termine le texte', () => {
    const r = avecMotCollé()
    effacerTexte(r.rgba, r.largeur, r.hauteur, { largeurCarte: 300, hauteurCarte: 420 })
    expect(r.lum(40, 56)).toBeGreaterThan(200)
    expect(r.lum(66, 56)).toBeGreaterThan(200)
  })

  it('laisse une tache isolée loin sous le texte', () => {
    const r = avecMotCollé()
    effacerTexte(r.rgba, r.largeur, r.hauteur, { largeurCarte: 300, hauteurCarte: 420 })
    expect(r.lum(135, 112)).toBeLessThan(60)
  })
})

describe('effacerTexte : dernières lettres d\'une ligne dans la bande de marge (26/10/2026)', () => {
  function lignesJusquAuBord() {
    const largeur = 200
    const hauteur = 100
    const rgba = new Uint8ClampedArray(largeur * hauteur * 4).fill(255)
    const peindre = (x0: number, y0: number, x1: number, y1: number) => {
      for (let y = y0; y < y1; y += 1) for (let x = x0; x < x1; x += 1) rgba.set([20, 20, 20, 255], (y * largeur + x) * 4)
    }
    for (const y of [20, 35, 50]) for (let x = 30; x < 186; x += 8) peindre(x, y, x + 4, y + 7)
    peindre(190, 35, 194, 42) // la dernière lettre de la ligne, dans la bande de marge (x ≥ 200 - 14)
    peindre(192, 65, 194, 67) // un point du pointillé du cadre, loin de toute ligne
    return { rgba, largeur, hauteur, lum: (x: number, y: number) => rgba[(y * largeur + x) * 4] }
  }

  it('efface la dernière lettre d\'une ligne même dans la bande de marge, mais pas un point du cadre', () => {
    const r = lignesJusquAuBord()
    effacerTexte(r.rgba, r.largeur, r.hauteur, { largeurCarte: 300, hauteurCarte: 420, margeCote: 14 })
    expect(r.lum(192, 38)).toBeGreaterThan(200)
    expect(r.lum(193, 66)).toBeLessThan(60)
  })
})
