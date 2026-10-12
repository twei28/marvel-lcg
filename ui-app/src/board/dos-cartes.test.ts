import { afterEach, describe, expect, it } from 'vitest'
import { CLE_DOS_CARTES, dosPicId, ecrireDosCartes, lireDosCartes } from './dos-cartes'
import { scanUrl } from './card-model'

afterEach(() => window.localStorage.removeItem(CLE_DOS_CARTES))

describe('dos de cartes', () => {
  it('officiels par defaut, sans rien en memoire', () => {
    expect(lireDosCartes()).toBe('officiels')
    expect(scanUrl('player')).toBe('/scan/player')
  })

  it('le choix est retenu et relu', () => {
    ecrireDosCartes('narwhal')
    expect(window.localStorage.getItem(CLE_DOS_CARTES)).toBe('narwhal')
    expect(lireDosCartes()).toBe('narwhal')
    ecrireDosCartes('officiels')
    expect(lireDosCartes()).toBe('officiels')
  })

  it('une valeur inconnue en memoire retombe sur les officiels', () => {
    window.localStorage.setItem(CLE_DOS_CARTES, 'autre')
    expect(lireDosCartes()).toBe('officiels')
  })

  it.each(['player', 'encounter', 'villain'])('le dos %s suit le choix', (camp) => {
    expect(dosPicId(camp, 'officiels')).toBe(camp)
    expect(dosPicId(camp, 'narwhal')).toBe(`${camp}-narwhal`)
    ecrireDosCartes('narwhal')
    expect(scanUrl(camp)).toBe(`/scan/${camp}-narwhal`)
  })

  it('une carte face visible n est jamais touchee', () => {
    ecrireDosCartes('narwhal')
    expect(dosPicId('01001a', 'narwhal')).toBe('01001a')
    expect(scanUrl('01001a')).not.toContain('narwhal')
  })
})
