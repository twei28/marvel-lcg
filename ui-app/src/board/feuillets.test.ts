import { beforeEach, describe, expect, it } from 'vitest'
import { feuilletsDeLaPartie, pagesDansLaLangue } from './feuillets'

beforeEach(() => window.localStorage.clear())

describe('feuilletsDeLaPartie', () => {
  it('donne le feuillet Dazzler quand Dazzler est dans la partie (en francais)', () => {
    window.localStorage.setItem('marvel-langue', 'fr')
    expect(feuilletsDeLaPartie(['bl001a', 'dz001a']).map((f) => f.titre)).toEqual(['Dazzler'])
  })
  it('donne le feuillet Moon Knight quand une de ses faces d\'identite est en jeu, et les deux si les deux heros sont la', () => {
    window.localStorage.setItem('marvel-langue', 'fr')
    expect(feuilletsDeLaPartie(['mk001b']).map((f) => f.titre)).toEqual(['Moon Knight'])
    expect(feuilletsDeLaPartie(['mk001a', 'dz001a']).map((f) => f.titre)).toEqual(['Dazzler', 'Moon Knight'])
  })
  it('ne donne rien sans heros a feuillet', () => {
    window.localStorage.setItem('marvel-langue', 'fr')
    expect(feuilletsDeLaPartie(['bl001a', undefined])).toEqual([])
  })
  it('montre quand meme le feuillet francais en anglais quand il n\'y a que lui', () => {
    window.localStorage.setItem('marvel-langue', 'en')
    expect(feuilletsDeLaPartie(['dz001a']).map((f) => f.titre)).toEqual(['Dazzler'])
  })
  it('montre l\'insert anglais en francais quand il n\'y a que lui, dans les deux langues', () => {
    for (const langue of ['fr', 'en']) {
      window.localStorage.setItem('marvel-langue', langue)
      expect(feuilletsDeLaPartie(['bw001a']).map((f) => f.titre)).toEqual(['Brawn'])
    }
  })
  it('garde toutes les pages d\'un feuillet recto-verso, dans l\'ordre', () => {
    window.localStorage.setItem('marvel-langue', 'en')
    expect(feuilletsDeLaPartie(['ok001a'])[0].pages).toHaveLength(2)
    expect(feuilletsDeLaPartie(['65001a'])[0].titre).toBe('Wave')
  })
})

describe('feuillets de scenario', () => {
  it('se declenche sur l\'id exact du vilain ou du complot, jamais sur un autre id du meme pack', () => {
    window.localStorage.setItem('marvel-langue', 'en')
    expect(feuilletsDeLaPartie(['bl001a', 'gs076']).map((f) => f.titre)).toEqual(['Kree Sentry'])
    expect(feuilletsDeLaPartie(['gs161a']).map((f) => f.titre)).toEqual(['Earth Under Siege'])
    expect(feuilletsDeLaPartie(['gs0761', 'gs077', 'gs160'])).toEqual([])
  })
  it('met a la suite l\'insert du modulaire ou la page commune', () => {
    window.localStorage.setItem('marvel-langue', 'fr')
    expect(feuilletsDeLaPartie(['gs161a'])[0].pages).toHaveLength(3)
    expect(feuilletsDeLaPartie(['sk189a'])[0].pages).toHaveLength(2)
  })
})

describe('pagesDansLaLangue', () => {
  it('prefere la langue du joueur, sinon prend l\'autre, et rien sans feuillet', () => {
    expect(pagesDansLaLangue('dz', 'fr')).toHaveLength(1)
    expect(pagesDansLaLangue('dz', 'en')).toHaveLength(1)
    expect(pagesDansLaLangue('bw', 'fr')).toHaveLength(1)
    expect(pagesDansLaLangue('zz', 'fr')).toBeNull()
  })
})
