// Le bug d'origine, en une phrase : le panneau de décision se posait au centre
// du viewport, et le centre du viewport, c'est là que la table met la manigance
// principale. Ces tests verrouillent la règle qui le remplace.
//
// Les dimensions viennent d'un cas réel (capture du 07/08/2026) : fenêtre de
// 1382x757, panneau `.demande-centrale` de 660x150 au plus, carte de manigance
// agrandie à ~470x330 au centre gauche.
import { describe, expect, it } from 'vitest'
import type { Boite } from './boites'
import { CANDIDATS_PAR_DEFAUT, chevauchement, placer } from './placer'

const VIEWPORT = { w: 1382, h: 757 }
const PANNEAU = { w: 660, h: 150 }

/** Le rectangle qu'occuperait le panneau à cette position. */
const boiteDu = (p: { x: number; y: number }, taille = PANNEAU): Boite => ({ ...p, ...taille })

describe('chevauchement', () => {
  it('rend 0 pour deux rectangles disjoints', () => {
    expect(chevauchement({ x: 0, y: 0, w: 10, h: 10 }, { x: 20, y: 0, w: 10, h: 10 })).toBe(0)
  })

  it('rend 0 pour deux rectangles qui se touchent sans se recouvrir', () => {
    expect(chevauchement({ x: 0, y: 0, w: 10, h: 10 }, { x: 10, y: 0, w: 10, h: 10 })).toBe(0)
  })

  it("rend l'aire commune", () => {
    expect(chevauchement({ x: 0, y: 0, w: 10, h: 10 }, { x: 5, y: 5, w: 10, h: 10 })).toBe(25)
  })

  it('rend la surface du plus petit quand il est entièrement dedans', () => {
    expect(chevauchement({ x: 0, y: 0, w: 100, h: 100 }, { x: 10, y: 10, w: 5, h: 4 })).toBe(20)
  })
})

describe('placer — rien à éviter', () => {
  it('pose le panneau à sa position préférée', () => {
    const p = placer({ taille: PANNEAU, aEviter: [], viewport: VIEWPORT })
    expect(p.ancre).toBe('centre')
    expect(p.genant).toBe(false)
    // Centré horizontalement, à 45 % de la hauteur.
    expect(p.x).toBe((VIEWPORT.w - PANNEAU.w) / 2)
    expect(p.y).toBe(VIEWPORT.h * 0.45 - PANNEAU.h / 2)
  })

  it('respecte une préférence autre que le centre', () => {
    const p = placer({ taille: PANNEAU, aEviter: [], viewport: VIEWPORT, preferee: 'droite' })
    expect(p.ancre).toBe('droite')
    expect(p.x).toBe(VIEWPORT.w - PANNEAU.w - 12)
  })
})

describe('placer — le cas signalé', () => {
  // La manigance principale, agrandie, en plein sur la position préférée.
  const MANIGANCE: Boite = { x: 360, y: 300, w: 470, h: 330 }

  it('ne recouvre plus la carte dont le panneau parle', () => {
    const p = placer({ taille: PANNEAU, aEviter: [MANIGANCE], viewport: VIEWPORT })
    expect(chevauchement(boiteDu(p), MANIGANCE)).toBe(0)
    expect(p.genant).toBe(false)
  })

  it('reste dans la fenêtre', () => {
    const p = placer({ taille: PANNEAU, aEviter: [MANIGANCE], viewport: VIEWPORT })
    expect(p.x).toBeGreaterThanOrEqual(0)
    expect(p.y).toBeGreaterThanOrEqual(0)
    expect(p.x + PANNEAU.w).toBeLessThanOrEqual(VIEWPORT.w)
    expect(p.y + PANNEAU.h).toBeLessThanOrEqual(VIEWPORT.h)
  })

  it("prend la position libre la plus proche du centre, pas n'importe laquelle", () => {
    const p = placer({ taille: PANNEAU, aEviter: [MANIGANCE], viewport: VIEWPORT })
    // 'bas' vient avant 'haut' dans la liste : à recouvrement nul égal, c'est
    // l'ordre qui tranche, et il est stable.
    expect(CANDIDATS_PAR_DEFAUT.indexOf(p.ancre)).toBeLessThanOrEqual(
      CANDIDATS_PAR_DEFAUT.indexOf('droite')
    )
  })
})

describe('placer — évite aussi les autres panneaux', () => {
  it("contourne un panneau déjà posé au centre", () => {
    const dejaPose: Boite = { x: (VIEWPORT.w - 660) / 2, y: 265, w: 660, h: 150 }
    const p = placer({ taille: { w: 400, h: 200 }, aEviter: [dejaPose], viewport: VIEWPORT })
    expect(chevauchement(boiteDu(p, { w: 400, h: 200 }), dejaPose)).toBe(0)
  })
})

describe('placer — quand tout est occupé', () => {
  // Une carte par position candidate : aucune issue.
  const PARTOUT: Boite[] = [{ x: 0, y: 0, w: VIEWPORT.w, h: VIEWPORT.h }]

  it('signale la gêne au lieu de sortir de la fenêtre', () => {
    const p = placer({ taille: PANNEAU, aEviter: PARTOUT, viewport: VIEWPORT })
    expect(p.genant).toBe(true)
    expect(p.x).toBeGreaterThanOrEqual(0)
    expect(p.y + PANNEAU.h).toBeLessThanOrEqual(VIEWPORT.h)
  })

  it('retombe alors sur la position préférée', () => {
    const p = placer({ taille: PANNEAU, aEviter: PARTOUT, viewport: VIEWPORT })
    expect(p.ancre).toBe('centre')
  })

  it('choisit le MOINDRE recouvrement quand ils diffèrent', () => {
    // Le centre est largement couvert, le bas seulement effleuré.
    const aEviter: Boite[] = [
      { x: 0, y: 200, w: VIEWPORT.w, h: 300 },
      { x: 0, y: VIEWPORT.h - 20, w: VIEWPORT.w, h: 20 },
    ]
    const p = placer({ taille: PANNEAU, aEviter, viewport: VIEWPORT })
    const recouvrement = aEviter.reduce((t, b) => t + chevauchement(boiteDu(p), b), 0)
    const auCentre = boiteDu({ x: (VIEWPORT.w - PANNEAU.w) / 2, y: VIEWPORT.h * 0.45 - PANNEAU.h / 2 })
    const recouvrementCentre = aEviter.reduce((t, b) => t + chevauchement(auCentre, b), 0)
    expect(recouvrement).toBeLessThan(recouvrementCentre)
  })
})

describe('placer — fenêtre étroite', () => {
  it('ne sort jamais du viewport, même si le panneau est plus large', () => {
    const petit = { w: 380, h: 620 }
    const p = placer({ taille: { w: 660, h: 150 }, aEviter: [], viewport: petit })
    expect(p.x).toBeGreaterThanOrEqual(0)
    expect(p.y).toBeGreaterThanOrEqual(0)
  })

  it('colle en haut à gauche un panneau plus grand que la fenêtre', () => {
    const p = placer({ taille: { w: 900, h: 900 }, aEviter: [], viewport: { w: 400, h: 400 } })
    expect(p.x).toBe(12)
    expect(p.y).toBe(12)
  })
})

describe('placer — une seule position autorisée', () => {
  // C'est le réglage de l'aperçu au survol : il doit s'ouvrir TOUJOURS au même
  // endroit, quitte à recouvrir. Un agrandissement qui change de coin à chaque
  // survol oblige à le rechercher du regard — signalé en jeu, et corrigé ainsi.
  const seulement = { taille: PANNEAU, viewport: VIEWPORT, preferee: 'droite' as const, candidats: ['droite' as const] }

  it("ne bouge pas, même quand la place est occupée", () => {
    const libre = placer({ ...seulement, aEviter: [] })
    const encombre = placer({ ...seulement, aEviter: [{ x: 0, y: 0, w: VIEWPORT.w, h: VIEWPORT.h }] })
    expect(encombre.x).toBe(libre.x)
    expect(encombre.y).toBe(libre.y)
    expect(encombre.ancre).toBe('droite')
  })

  it('signale quand même la gêne, pour qui voudrait la traiter', () => {
    const p = placer({ ...seulement, aEviter: [{ x: 0, y: 0, w: VIEWPORT.w, h: VIEWPORT.h }] })
    expect(p.genant).toBe(true)
  })

  it('reste borné à la fenêtre', () => {
    const p = placer({ ...seulement, taille: { w: 934, h: 361 }, aEviter: [] })
    expect(p.x + 934).toBeLessThanOrEqual(VIEWPORT.w)
    expect(p.y + 361).toBeLessThanOrEqual(VIEWPORT.h)
  })
})

describe('placer — borne droite', () => {
  // Cas réel : sur une fenêtre de 1909, la colonne des manigances commence à
  // x=1538. Un aperçu d'une seule carte (345 px) doit se ranger entièrement à
  // sa gauche plutôt que s'asseoir dessus.
  const CARTE_SEULE = { w: 345, h: 507 }
  const LARGE = { w: 1909, h: 933 }
  const COLONNE = 1538 - 12

  it("range la carte seule entièrement à gauche de la colonne", () => {
    const p = placer({
      taille: CARTE_SEULE,
      aEviter: [],
      viewport: LARGE,
      preferee: 'droite',
      candidats: ['droite'],
      borneDroite: COLONNE,
    })
    expect(p.x + CARTE_SEULE.w).toBeLessThanOrEqual(COLONNE)
  })

  it('garde le centrage vertical : la borne ne vaut que sur X', () => {
    const p = placer({
      taille: CARTE_SEULE,
      aEviter: [],
      viewport: LARGE,
      preferee: 'droite',
      candidats: ['droite'],
      borneDroite: COLONNE,
    })
    expect(p.y).toBe((LARGE.h - CARTE_SEULE.h) / 2)
  })

  it("sans borne, la carte reste collée au bord droit", () => {
    const p = placer({
      taille: CARTE_SEULE,
      aEviter: [],
      viewport: LARGE,
      preferee: 'droite',
      candidats: ['droite'],
    })
    expect(p.x + CARTE_SEULE.w).toBe(LARGE.w - 12)
  })

  it("ne pousse pas hors écran un panneau trop large pour la borne", () => {
    const p = placer({
      taille: { w: 934, h: 361 },
      aEviter: [],
      viewport: LARGE,
      preferee: 'droite',
      candidats: ['droite'],
      borneDroite: 300,
    })
    expect(p.x).toBeGreaterThanOrEqual(12)
  })
})

describe('placer — déterminisme', () => {
  it('rend exactement la même position pour les mêmes entrées', () => {
    const entree = {
      taille: PANNEAU,
      aEviter: [{ x: 360, y: 300, w: 470, h: 330 }],
      viewport: VIEWPORT,
    }
    expect(placer(entree)).toEqual(placer(entree))
  })

  it("ne dépend pas de l'ordre des obstacles", () => {
    const a: Boite = { x: 360, y: 300, w: 470, h: 330 }
    const b: Boite = { x: 900, y: 100, w: 200, h: 200 }
    const base = { taille: PANNEAU, viewport: VIEWPORT }
    expect(placer({ ...base, aEviter: [a, b] })).toEqual(placer({ ...base, aEviter: [b, a] }))
  })
})
