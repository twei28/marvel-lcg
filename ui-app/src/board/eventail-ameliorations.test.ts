// T14 : l'eventail des ameliorations a cliquer se pose a cote de leur porteur, entierement dans la table, sans
// recouvrir le porteur ni le bandeau ni la place de l'apercu.
import { describe, expect, it } from 'vitest'
import { placerEventail } from './TableSansModale'

const cadre = { w: 1280, h: 720 }
const croise = (a: { x: number; y: number; w: number; h: number }, b: { x: number; y: number; w: number; h: number }) =>
  a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y

describe('placerEventail', () => {
  const total3 = { w: 3 * 112 + 16, h: 155 + 38 }

  it('se pose a droite de la pile quand la place existe', () => {
    const pile = { x: 215, y: 420, w: 210, h: 135 }
    const r = placerEventail(pile, total3, cadre, [])
    expect(r.x).toBeGreaterThanOrEqual(pile.x + pile.w)
    expect(r.y + r.h).toBeLessThanOrEqual(cadre.h)
  })

  it('ne recouvre pas le porteur, meme sans place a droite', () => {
    const pile = { x: 900, y: 420, w: 210, h: 135 }
    const r = placerEventail(pile, total3, cadre, [])
    expect(croise(r, pile)).toBe(false)
    expect(r.x + r.w).toBeLessThanOrEqual(cadre.w)
  })

  it('evite le bandeau et la place de l\'apercu', () => {
    const pile = { x: 215, y: 420, w: 210, h: 135 }
    const bandeau = { x: 8, y: 84, w: 198, h: 300 }
    const apercu = { x: 900, y: 0, w: 380, h: 720 }
    const r = placerEventail(pile, total3, cadre, [bandeau, apercu])
    expect(croise(r, bandeau)).toBe(false)
    expect(croise(r, apercu)).toBe(false)
    expect(croise(r, pile)).toBe(false)
  })

  it('reste dans le cadre pour une pile collee au bas de la table', () => {
    const pile = { x: 215, y: 640, w: 210, h: 70 }
    const r = placerEventail(pile, total3, cadre, [])
    expect(r.y + r.h).toBeLessThanOrEqual(cadre.h)
    expect(r.y).toBeGreaterThanOrEqual(0)
  })
})
