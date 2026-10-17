// Arts alternatifs des cartes de deck : l'image suit le choix enregistre, sinon
// la serie du heros (TMNT), sinon l'officielle ; et le plateau dit comme la
// preparation (module pur public/js/prepare/arts-cartes-choix.js).
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'

vi.mock('./arts-cartes-table', () => ({
  ARTS_CARTES: { '56013': ['tmnt'], '01057': ['tmnt'] },
  SERIES_ARTS: {
    tmnt: {
      nom: 'TMNT',
      nom_en: 'TMNT',
      heros_cartes: ['tl001', 'tj001'],
      heros_ids: ['leonardo', 'jennika'],
      sets_exclusifs: ['TMNT Aggression'],
    },
  },
}))

import { picIdCarte, serieDuHeros, lireArtsCartes, oublierArtsCartes, CLE_ARTS_CARTES } from './arts-cartes'
import { picIdAffiche } from './variantes'

const ARTS = { '56013': ['tmnt'], '01057': ['tmnt'] }

describe('arts alternatifs des cartes de deck', () => {
  beforeEach(() => oublierArtsCartes())
  afterEach(() => {
    window.localStorage.clear()
    oublierArtsCartes()
  })

  it('un heros TMNT a l\'art TMNT par defaut, les autres l\'officielle', () => {
    expect(picIdCarte('56013', 'tl001a', {})).toBe('56013_tmnt')
    expect(picIdCarte('56013', 'tj001b', {})).toBe('56013_tmnt')
    expect(picIdCarte('56013', '38001a', {})).toBe('56013')
    expect(picIdCarte('56013', undefined, {})).toBe('56013')
  })

  it('le choix enregistre l\'emporte, « standard » compris', () => {
    expect(picIdCarte('56013', 'tl001a', { '56013': 'standard' })).toBe('56013')
    expect(picIdCarte('56013', '38001a', { '56013': 'tmnt' })).toBe('56013_tmnt')
    expect(picIdCarte('56013', '38001a', { '56013': 'zzz' })).toBe('56013')
  })

  it('une carte sans art alternatif ne change jamais', () => {
    expect(picIdCarte('32043', 'tl001a', { '32043': 'tmnt' })).toBe('32043')
  })

  it('la serie se reconnait a la carte du heros', () => {
    expect(serieDuHeros('tl001a')).toBe('tmnt')
    expect(serieDuHeros('38001a')).toBeNull()
    expect(serieDuHeros(undefined)).toBeNull()
  })

  it('lit la table du navigateur, et survit a un stockage illisible', () => {
    window.localStorage.setItem(CLE_ARTS_CARTES, JSON.stringify({ '56013': 'tmnt' }))
    expect(lireArtsCartes()).toEqual({ '56013': 'tmnt' })
    oublierArtsCartes()
    window.localStorage.setItem(CLE_ARTS_CARTES, '{pas du json')
    expect(lireArtsCartes()).toEqual({})
  })

  it('picIdAffiche applique l\'art de carte avec le heros proprietaire', () => {
    expect(picIdAffiche('56013', undefined, 'tl001a')).toBe('56013_tmnt')
    expect(picIdAffiche('56013', undefined, '38001a')).toBe('56013')
    expect(picIdAffiche('56013', undefined)).toBe('56013')
  })

  it('le plateau dit comme la preparation (module pur) pour toutes les combinaisons', async () => {
    const choix = await import(
      /* @vite-ignore */ '../../../Fusion/marvel-lcg-src/public/js/prepare/arts-cartes-choix.js'
    )
    const series = {
      tmnt: { nom: 'TMNT', nom_en: 'TMNT', heros_cartes: ['tl001', 'tj001'], heros_ids: ['x'], sets_exclusifs: ['x'] },
    }
    for (const id of ['56013', '01057', '32043']) {
      for (const heros of ['tl001a', 'tj001b', '38001a', undefined]) {
        for (const c of [undefined, 'standard', 'tmnt', 'zzz']) {
          const table = c ? { [id]: c } : {}
          const pur = choix.picIdAvecArt(id, choix.codeAffiche(id, table, heros, ARTS, series))
          expect(picIdCarte(id, heros, table), `${id} ${heros} ${c}`).toBe(pur)
        }
      }
    }
  })
})
