// Le cadre doré d'une carte INCLINEE doit s'incliner avec elle (18/10/2026, « le carré qui entoure la carte,
// quand la carte est inclinée, reste normal et pas incliné »). Une carte epuisee tourne de 8 degres ; son
// rectangle mesure (getBoundingClientRect) est la boite qui l'englobe, droite et plus grande qu'elle.
import { describe, expect, it } from 'vitest'
import { redresserBoite } from './mesures-plateau'

/** La boite englobante d'un rectangle w x h tourne de `deg` degres autour de son centre (cx, cy). */
function englobante(cx: number, cy: number, w: number, h: number, deg: number) {
  const a = (deg * Math.PI) / 180
  const W = w * Math.abs(Math.cos(a)) + h * Math.abs(Math.sin(a))
  const H = w * Math.abs(Math.sin(a)) + h * Math.abs(Math.cos(a))
  return { x: cx - W / 2, y: cy - H / 2, w: W, h: H }
}

describe('redresserBoite', () => {
  it('rend la taille de la carte, son centre et son angle, a partir de la boite englobante', () => {
    const b = redresserBoite(englobante(300, 200, 100, 140, 8), 100, 140, 8)
    expect(b.w).toBeCloseTo(100, 1)
    expect(b.h).toBeCloseTo(140, 1)
    expect(b.x + b.w / 2).toBeCloseTo(300, 1)
    expect(b.y + b.h / 2).toBeCloseTo(200, 1)
    expect(b.angle).toBeCloseTo(8, 5)
  })

  it('tient aussi quand le plateau est mis a l echelle (la carte mesure moins que sa taille de mise en page)', () => {
    const b = redresserBoite(englobante(300, 200, 50, 70, 8), 100, 140, 8)
    expect(b.w).toBeCloseTo(50, 1)
    expect(b.h).toBeCloseTo(70, 1)
  })

  it('une carte droite garde sa boite, sans angle', () => {
    const b = redresserBoite({ x: 10, y: 20, w: 100, h: 140 }, 100, 140, 0)
    expect(b).toEqual({ x: 10, y: 20, w: 100, h: 140 })
  })
})
