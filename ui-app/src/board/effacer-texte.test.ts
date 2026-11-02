import { describe, expect, it } from 'vitest'
import { inflateSync } from 'node:zlib'
import { BANDES_DROITE, boitesDesMotsCollés, cadreDesLettres, cadrePencheNet, effacerTexte } from './effacer-texte'
import { HF041_BARRE, HF342_GRAS, HF114_BORD, BG001A_TIRET, SY024_TRAIT, SZ004_GUILLEMET } from './effacer-texte.fixtures'

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

describe('effacerTexte : séparateur du Boost sous des lignes de mots-clés (02/11/2026)', () => {
  /** Deux lignes de lettres, un filet noir plein de 3 px (séparateur du Boost), deux lignes de lettres dessous. */
  function carteAvecFilet() {
    const largeur = 300
    const hauteur = 240
    const rgba = new Uint8ClampedArray(largeur * hauteur * 4).fill(245)
    const peindre = (x0: number, y0: number, x1: number, y1: number, v = 20) => {
      for (let y = y0; y < y1; y += 1) for (let x = x0; x < x1; x += 1) rgba.set([v, v, v, 255], (y * largeur + x) * 4)
    }
    for (const y of [20, 40]) for (let x = 30; x < 230; x += 9) peindre(x, y, x + 5, y + 12)
    peindre(0, 70, largeur, 73) // filet : rangée entièrement sombre, fine
    for (const y of [90, 110]) for (let x = 30; x < 230; x += 9) peindre(x, y, x + 5, y + 12)
    return { rgba, largeur, hauteur, lum: (x: number, y: number) => rgba[(y * largeur + x) * 4] }
  }
  it('un filet fin ne passe pas pour le haut du cadre : les lignes au-dessus sont effacées aussi', () => {
    const r = carteAvecFilet()
    effacerTexte(r.rgba, r.largeur, r.hauteur, { largeurCarte: 593, hauteurCarte: 850 })
    expect(r.lum(32, 25)).toBeGreaterThan(200) // 1re ligne (au-dessus du filet)
    expect(r.lum(32, 45)).toBeGreaterThan(200)
    expect(r.lum(32, 95)).toBeGreaterThan(200) // sous le filet : toujours effacée
  })
})

describe('effacerTexte : liseré du cadre au bout d\'une ligne (02/11/2026)', () => {
  it('hf114 : le liseré argenté et le noir du cadre ne sont pas effacés comme des lettres collées', () => {
    const f = HF114_BORD
    const rgba = pixelsDe(f)
    const avant = new Uint8ClampedArray(rgba)
    effacerTexte(rgba, f.largeur, f.hauteur, { largeurCarte: f.largeurCarte, hauteurCarte: f.hauteurCarte, ...REGLAGES })
    // Colonnes du cadre en haut de la fixture (x 207-229, y 5-30 = 537-559, 110-135 de la région) : inchangées, hors tolérance de quelques pixels.
    let change = 0
    for (let y = 5; y < 30; y += 1) for (let x = 207; x < 229; x += 1) if (Math.abs(lum(rgba, f.largeur, x, y) - lum(avant, f.largeur, x, y)) > 30) change += 1
    expect(change).toBe(0)
  })
})

describe('effacerTexte : lettres en gras (02/11/2026)', () => {
  it('hf342 : la ligne de traits imprimée en gras (« ILLUSION. PSIONIC. ») est effacée en entier, pas à moitié', () => {
    const f = HF342_GRAS
    const rgba = pixelsDe(f)
    // Le « S » de ILLUSION (x 255-273, y 23-47 de la région, soit x 155-173 de la fixture) : noir au départ.
    expect(lum(rgba, f.largeur, 164, 35)).toBeLessThan(80)
    effacerTexte(rgba, f.largeur, f.hauteur, { largeurCarte: f.largeurCarte, hauteurCarte: f.hauteurCarte, ...REGLAGES })
    for (const x of [150, 164, 190, 212]) expect(lum(rgba, f.largeur, x, 38)).toBeGreaterThan(130)
  })
})

describe('effacerTexte : pictogrammes colorés (02/11/2026)', () => {
  it('une icône rouge (boost) au bout d\'une ligne n\'est pas effacée comme une lettre', () => {
    const largeur = 220
    const hauteur = 100
    const rgba = new Uint8ClampedArray(largeur * hauteur * 4).fill(245)
    const peindre = (x0: number, y0: number, x1: number, y1: number, r: number, g = r, b = r) => {
      for (let y = y0; y < y1; y += 1) for (let x = x0; x < x1; x += 1) rgba.set([r, g, b, 255], (y * largeur + x) * 4)
    }
    for (const y of [20, 38, 56]) for (let x = 20; x < 120; x += 9) peindre(x, y, x + 5, y + 10, 20)
    peindre(130, 21, 142, 31, 205, 30, 55) // petite icône rouge dans la ligne, sans aplat sombre
    effacerTexte(rgba, largeur, hauteur, { largeurCarte: 593, hauteurCarte: 850 })
    expect(rgba[(25 * largeur + 135) * 4 + 1]).toBeLessThan(90) // toujours rouge (vert bas)
    expect(rgba[(25 * largeur + 22) * 4]).toBeGreaterThan(200) // une lettre : effacée
  })
})

describe('cadrePencheNet : cadre penché reconnu sans liste (02/11/2026)', () => {
  const ligne = (y: number, x0: number) => Array.from({ length: 12 }, (_, k) => ({ x0: x0 + k * 14, x1: x0 + k * 14 + 8, y0: y, y1: y + 12 }))
  it('dix lignes dont le départ glisse régulièrement vers la gauche : un cadre qui penche', () => {
    const lettres = Array.from({ length: 10 }, (_, i) => ligne(40 + i * 25, 60 - i * 2.5)).flat()
    expect(cadrePencheNet(lettres, 850, 593)).toBe(true)
  })
  it('des départs à la même place, ou avec un retrait de citation et un gras : pas un cadre qui penche', () => {
    const plat = Array.from({ length: 10 }, (_, i) => ligne(40 + i * 25, 60)).flat()
    expect(cadrePencheNet(plat, 850, 593)).toBe(false)
    const retraits = Array.from({ length: 10 }, (_, i) => ligne(40 + i * 25, [60, 70, 60, 60, 74, 60, 60, 60, 66, 60][i])).flat()
    expect(cadrePencheNet(retraits, 850, 593)).toBe(false)
  })
  it('une ligne isolée au départ aberrant (éclat contre le bord) n\'empêche pas de reconnaître la pente', () => {
    const lettres = Array.from({ length: 11 }, (_, i) => ligne(40 + i * 25, i === 6 ? 13 : 60 - i * 2.5)).flat()
    expect(cadrePencheNet(lettres, 850, 593)).toBe(true)
  })
  it('quatre lignes seulement : trop peu pour l\'affirmer', () => {
    const lettres = Array.from({ length: 4 }, (_, i) => ligne(40 + i * 25, 60 - i * 6)).flat()
    expect(cadrePencheNet(lettres, 850, 593)).toBe(false)
  })
})

describe('effacerTexte : morceau de cadre haut comme trois lettres (02/11/2026)', () => {
  it('hf041 : la barre du cadre à gauche des lignes (47 px de haut) ne tire pas le bord gauche du texte', () => {
    const f = HF041_BARRE
    const rgba = pixelsDe(f)
    const cadre = effacerTexte(rgba, f.largeur, f.hauteur, { largeurCarte: f.largeurCarte, hauteurCarte: f.hauteurCarte, ...REGLAGES })
    expect(cadre).not.toBeNull()
    // Les lignes commencent vers x 30 ; la barre est à x 13-22.
    expect(cadre!.x0 * f.largeur).toBeGreaterThan(26)
  })
})

describe('effacerTexte : dernière lettre d\'une ligne coupée par le bord de la région (02/11/2026)', () => {
  it('une lettre qui touche le bord droit de la région, au bout d\'une ligne, est effacée avec elle', () => {
    const largeur = 190
    const hauteur = 100
    const rgba = new Uint8ClampedArray(largeur * hauteur * 4).fill(245)
    const peindre = (x0: number, y0: number, x1: number, y1: number, v = 20) => {
      for (let y = y0; y < y1; y += 1) for (let x = x0; x < x1; x += 1) rgba.set([v, v, v, 255], (y * largeur + x) * 4)
    }
    for (const y of [20, 38, 56]) for (let x = 20; x < 170; x += 9) peindre(x, y, x + 5, y + 10)
    peindre(181, 21, 190, 31) // la dernière lettre de la première ligne, coupée par le bord de la région
    effacerTexte(rgba, largeur, hauteur, { largeurCarte: 593, hauteurCarte: 850, margeCote: 14 })
    expect(rgba[(25 * largeur + 185) * 4]).toBeGreaterThan(200)
  })
})

describe('effacerTexte : filet du Boost qui touche les deux bords (02/11/2026)', () => {
  it('un filet fin d\'un bord à l\'autre, entre deux blocs de lignes, est effacé : le français redessine le sien', () => {
    const largeur = 200
    const hauteur = 160
    const rgba = new Uint8ClampedArray(largeur * hauteur * 4).fill(245)
    const peindre = (x0: number, y0: number, x1: number, y1: number, v = 20) => {
      for (let y = y0; y < y1; y += 1) for (let x = x0; x < x1; x += 1) rgba.set([v, v, v, 255], (y * largeur + x) * 4)
    }
    for (const y of [20, 38, 56]) for (let x = 20; x < 180; x += 9) peindre(x, y, x + 5, y + 10)
    peindre(0, 78, largeur, 80) // le filet : deux pixels, d'un bord à l'autre
    for (const y of [95, 113, 131]) for (let x = 20; x < 180; x += 9) peindre(x, y, x + 5, y + 10)
    effacerTexte(rgba, largeur, hauteur, { largeurCarte: 593, hauteurCarte: 850 })
    expect(rgba[(79 * largeur + 100) * 4]).toBeGreaterThan(200)
  })
  it('un liseré fin d\'un bord à l\'autre avec du texte d\'un seul côté (bas du cadre) reste', () => {
    const largeur = 200
    const hauteur = 120
    const rgba = new Uint8ClampedArray(largeur * hauteur * 4).fill(245)
    const peindre = (x0: number, y0: number, x1: number, y1: number, v = 20) => {
      for (let y = y0; y < y1; y += 1) for (let x = x0; x < x1; x += 1) rgba.set([v, v, v, 255], (y * largeur + x) * 4)
    }
    for (const y of [20, 38, 56]) for (let x = 20; x < 180; x += 9) peindre(x, y, x + 5, y + 10)
    peindre(0, 90, largeur, 92)
    effacerTexte(rgba, largeur, hauteur, { largeurCarte: 593, hauteurCarte: 850 })
    expect(rgba[(91 * largeur + 100) * 4]).toBeLessThan(100)
  })
})

describe('boitesDesMotsCollés : mot en gras collé en deux taches (02/11/2026)', () => {
  it('« PSIONIC. » imprimé en gras (deux taches, 65 px pour 17 de haut) est une ligne à effacer', () => {
    const lettres = [{ x0: 206, x1: 232, y0: 26, y1: 43 }, { x0: 233, x1: 271, y0: 26, y1: 43 }]
    const cadre = { x0: 28, x1: 412, y0: 69, y1: 369 }
    expect(boitesDesMotsCollés(lettres, cadre, 850)).toHaveLength(1)
  })
  it('le mot collé n\'est pas écarté parce qu\'une tache lointaine, à la même hauteur, grossit sa « ligne »', () => {
    const lettres = [{ x0: 40, x1: 50, y0: 143, y1: 153 }, { x0: 52, x1: 84, y0: 143, y1: 156 }, { x0: 400, x1: 410, y0: 144, y1: 155 }, { x0: 440, x1: 450, y0: 144, y1: 155 }]
    const cadre = { x0: 39, x1: 523, y0: 60, y1: 400 }
    expect(boitesDesMotsCollés(lettres, cadre, 850).length).toBeGreaterThanOrEqual(1)
  })
  it('hf404b : « 2A. » et « it. », derniers mots d\'un paragraphe, alignés à gauche sous le bloc de texte', () => {
    const pleines = [60, 90, 120, 150, 180].flatMap((y) => Array.from({ length: 14 }, (_, k) => ({ x0: 20 + k * 22, x1: 20 + k * 22 + 14, y0: y, y1: y + 18 })))
    const cadre = { x0: 20, x1: 320, y0: 60, y1: 198 }
    const courts = [{ x0: 22, x1: 36, y0: 210, y1: 228 }, { x0: 38, x1: 52, y0: 210, y1: 228 }] // « it » sous la dernière ligne
    expect(boitesDesMotsCollés([...pleines, ...courts], cadre, 850).length).toBeGreaterThanOrEqual(1)
    // Une tache isolée, haute comme une lettre mais loin de la marge gauche du texte : pas un mot.
    const loin = [{ x0: 200, x1: 214, y0: 210, y1: 228 }, { x0: 216, x1: 230, y0: 210, y1: 228 }]
    expect(boitesDesMotsCollés([...pleines, ...loin], cadre, 850)).toHaveLength(0)
  })
  it('deux taches proches mais minuscules (poussière) ne forment pas une ligne', () => {
    const lettres = [{ x0: 206, x1: 214, y0: 26, y1: 43 }, { x0: 216, x1: 224, y0: 26, y1: 43 }]
    const cadre = { x0: 28, x1: 412, y0: 69, y1: 369 }
    expect(boitesDesMotsCollés(lettres, cadre, 850)).toHaveLength(0)
  })
})
