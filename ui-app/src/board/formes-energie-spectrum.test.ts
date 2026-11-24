import { describe, expect, it } from 'vitest'
import { catalogueVide } from './catalogue'
import { toScanCard } from './card-model'
import { carteSurTable } from './plateau-de-test'

const contexte = { playerId: 0, actives: new Set<number>(), catalogue: catalogueVide }
const formes = ['21002', '21003', '21004']
const forme = (code: string, active: boolean) => carteSurTable(Number(code), code, 'Upgrade', code, {
  is_face_up: active, visible_for_players: [0], down_card_ids: ['player'],
})

describe('formes Énergie de Spectrum', () => {
  it('les trois formes inactives montrent leur dos même si leur identité est connue', () => {
    for (const code of formes) {
      const vue = toScanCard(forme(code, false), contexte)
      expect(vue.facedown).toBe(true)
      expect(vue.imageUrl).toContain('/player')
      expect(vue.peeking).not.toBe(true)
      expect(vue.stats).toBeUndefined()
    }
  })
  it('seule la forme active devient face visible, puis retrouve son dos au retour en alter ego', () => {
    for (const active of formes) {
      expect(formes.map(code => toScanCard(forme(code, code === active), contexte).facedown === true))
        .toEqual(formes.map(code => code !== active))
    }
    expect(formes.every(code => toScanCard(forme(code, false), contexte).facedown)).toBe(true)
  })
  it('conserve le fonctionnement des autres cartes connues face cachée', () => {
    const autre = carteSurTable(4, '01079', 'Upgrade', 'Web-Shooter', { is_face_up: false, down_card_ids: ['player'] })
    const vue = toScanCard(autre, contexte)
    expect(vue.peeking).toBe(true)
    expect(vue.facedown).not.toBe(true)
  })
})
