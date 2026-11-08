import { beforeEach, describe, expect, it } from 'vitest'
import { feuilletsDeLaPartie } from './feuillets'

beforeEach(() => window.localStorage.clear())

describe('feuilletsDeLaPartie', () => {
  it('donne le feuillet Dazzler quand Dazzler est dans la partie (en francais)', () => {
    window.localStorage.setItem('marvel-langue', 'fr')
    expect(feuilletsDeLaPartie(['bl001a', 'dz001a']).map((f) => f.titre)).toEqual(['Dazzler'])
  })
  it('ne donne rien sans heros a feuillet', () => {
    window.localStorage.setItem('marvel-langue', 'fr')
    expect(feuilletsDeLaPartie(['bl001a', undefined])).toEqual([])
  })
  it('ne donne rien en anglais : le feuillet est en francais', () => {
    window.localStorage.setItem('marvel-langue', 'en')
    expect(feuilletsDeLaPartie(['dz001a'])).toEqual([])
  })
})
