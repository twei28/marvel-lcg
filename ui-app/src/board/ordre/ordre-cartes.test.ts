import { describe, expect, it } from 'vitest'
import { cleDeRangee, deplacer, placeVisee, ranger } from './ordre-cartes'

describe('ranger', () => {
  const id = (n: number) => n
  it('sans ordre choisi, garde l ordre naturel', () => {
    expect(ranger([1, 2, 3], id, undefined)).toEqual([1, 2, 3])
  })
  it('suit l ordre choisi', () => {
    expect(ranger([1, 2, 3], id, [3, 1, 2])).toEqual([3, 1, 2])
  })
  it('met a la fin les cartes arrivees depuis, et ignore les parties', () => {
    expect(ranger([1, 2, 3, 4], id, [3, 9, 1])).toEqual([3, 1, 2, 4])
  })
})

describe('deplacer', () => {
  it('pose avant la cible', () => {
    expect(deplacer([1, 2, 3, 4], 4, 2, false)).toEqual([1, 4, 2, 3])
  })
  it('pose apres la cible', () => {
    expect(deplacer([1, 2, 3, 4], 1, 3, true)).toEqual([2, 3, 1, 4])
  })
  it('ne change rien si la place est deja la bonne', () => {
    const ids = [1, 2, 3]
    expect(deplacer(ids, 2, 3, false)).toBe(ids)
    expect(deplacer(ids, 3, 2, true)).toBe(ids)
  })
  it('refuse une carte ou une cible inconnue, ou soi-meme', () => {
    const ids = [1, 2]
    expect(deplacer(ids, 9, 1, true)).toBe(ids)
    expect(deplacer(ids, 1, 9, true)).toBe(ids)
    expect(deplacer(ids, 1, 1, true)).toBe(ids)
  })
})

describe('placeVisee', () => {
  const voisines = [
    { id: 1, cx: 100, cy: 50 },
    { id: 2, cx: 200, cy: 50 },
  ]
  it('vise la voisine la plus proche, cote gauche', () => {
    expect(placeVisee(voisines, 190, 50)).toEqual({ cibleId: 2, apres: false })
  })
  it('cote droit', () => {
    expect(placeVisee(voisines, 230, 50)).toEqual({ cibleId: 2, apres: true })
  })
  it('rien a viser sans voisine', () => {
    expect(placeVisee([], 0, 0)).toBeUndefined()
  })
})

describe('cleDeRangee', () => {
  it('distingue deux rangees d un meme emplacement', () => {
    expect(cleDeRangee('terrain-combat', 0, 1, 'x')).not.toBe(cleDeRangee('terrain-combat', 1, 1, 'x'))
  })
})
