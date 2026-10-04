// La teinte du fond : bornes, lecture, couleurs derivees, roue.
// ⚠ Les valeurs attendues de `variablesDeTeinte` sont COPIEES dans
// tools/tests-lanceur/teinte-choix.test.mjs (le jumeau de la preparation) :
// les deux doivent rendre exactement les memes couleurs.
import { describe, expect, it } from 'vitest'
import {
  bornerTeinte,
  ecrireTeinteEnTexte,
  hslVersRgb,
  lireTeinte,
  pointDeLaTeinte,
  teinteDuCompte,
  teinteDuPoint,
  variablesDeTeinte,
} from './teinte'

describe('la teinte du fond reste terne et lisible', () => {
  it('lit « h,s,l » dans les bornes, refuse le reste', () => {
    expect(lireTeinte('210,12,18')).toEqual({ h: 210, s: 12, l: 18 })
    for (const mauvaise of ['210,40,18', '400,10,18', '210,10,90', '210,10,3', 'rouge', '210,10', 12, null, '-1,0,10'])
      expect(lireTeinte(mauvaise)).toBeUndefined()
  })

  it('borne toute teinte : saturation 18 % max, luminosite 6-62 %', () => {
    expect(bornerTeinte({ h: 370, s: 80, l: 95 })).toEqual({ h: 10, s: 18, l: 62 })
    expect(ecrireTeinteEnTexte({ h: -30, s: 3.4, l: 1 })).toBe('330,3,6')
  })

  it('conversion HSL -> RGB exacte sur des reperes', () => {
    expect(hslVersRgb(0, 0, 50)).toBe('128 128 128')
    expect(hslVersRgb(0, 100, 50)).toBe('255 0 0')
  })

  it('table sombre : bandeau et panneaux derives, titres clairs', () => {
    expect(variablesDeTeinte({ h: 210, s: 12, l: 18 })).toEqual({
      '--teinte-table': 'hsl(210 12% 18%)',
      '--teinte-table-rgb': '40 46 51',
      '--teinte-bandeau': 'hsl(210 12% 14%)',
      '--teinte-bandeau-rgb': '31 36 40',
      '--teinte-panneau': 'hsl(210 12% 20%)',
      '--teinte-panneau-rgb': '45 51 57',
      '--teinte-cadre': 'hsl(210 16% 30%)',
      '--teinte-texte-table': 'rgba(226, 232, 240, 0.78)',
    })
  })

  it('table gris clair : bandeau et panneaux restent sombres, titres en fonce', () => {
    const v = variablesDeTeinte({ h: 40, s: 6, l: 60 })
    expect(v['--teinte-table']).toBe('hsl(40 6% 60%)')
    expect(v['--teinte-bandeau']).toBe('hsl(40 6% 26%)')
    expect(v['--teinte-panneau']).toBe('hsl(40 6% 24%)')
    expect(v['--teinte-texte-table']).toBe('#1b1d21')
  })

  it('la roue : angle = teinte (0 en haut), rayon = saturation, aller-retour', () => {
    expect(teinteDuPoint(0, -100, 100, 20)).toEqual({ h: 0, s: 18, l: 20 })
    expect(teinteDuPoint(100, 0, 100, 20)).toEqual({ h: 90, s: 18, l: 20 })
    expect(teinteDuPoint(0, 0, 100, 20).s).toBe(0)
    const p = pointDeLaTeinte({ h: 90, s: 9, l: 20 })
    expect(p.x).toBeCloseTo(0.5)
    expect(p.y).toBeCloseTo(0)
  })

  it('le compte : sa teinte fait foi, son absence vaut couleur d origine', () => {
    expect(teinteDuCompte({ compte: true, existe: true, preferences: { teinte: '10,5,30' } })).toEqual({ h: 10, s: 5, l: 30 })
    expect(teinteDuCompte({ compte: true, existe: true, preferences: {} })).toBeNull()
    expect(teinteDuCompte({ compte: false, existe: false, preferences: {} })).toBeUndefined()
  })
})
