import { describe, expect, it } from 'vitest'
import { estimerAvantage } from './barre-avantage'
import type { World, WorldCard } from './world'

const carte = (info: Record<string, number | boolean>, face = true): WorldCard =>
  ({ id: 1, is_ready: true, is_face_up: face, visible_for_players: [], bind_object_id: 0, name: 'x', info, traits: {}, buffs: {}, card_id: 'x', pic_id: 'x', down_card_ids: [], card_type: 'x', cost: 0, resources: [] }) as unknown as WorldCard

function monde(p: { menace?: number; seuil?: number; mechant?: [number, number]; heros?: [number, number][]; sbires?: number; extra?: Partial<World> }): World {
  const heros = p.heros ?? [[10, 10]]
  return {
    area_schemes_main: p.seuil === undefined ? [] : [carte({ k_threat: p.menace ?? 0, target_threat: p.seuil })],
    area_villain: p.mechant ? [carte({ health: p.mechant[0], max_health: p.mechant[1] })] : [],
    players: heros.map(([pv, max], i) => ({
      area_hero: [carte({ health: pv, max_health: max })],
      engaged_enemies: i === 0 ? Array.from({ length: p.sbires ?? 0 }, () => carte({})) : [],
      is_eliminated: false,
    })),
    ...p.extra,
  } as unknown as World
}

describe('estimerAvantage', () => {
  it('rien du tout sans monde, partie finie, mode manuel ou Bataille', () => {
    expect(estimerAvantage(undefined)).toEqual({ etat: 'masque' })
    expect(estimerAvantage(monde({ seuil: 10, extra: { game_over: true } }))).toEqual({ etat: 'masque' })
    expect(estimerAvantage(monde({ seuil: 10, extra: { manuel_actif: true } }))).toEqual({ etat: 'masque' })
    expect(estimerAvantage(monde({ seuil: 10, extra: { teams: [0, 1] } }))).toEqual({ etat: 'masque' })
  })

  it('indisponible sans manigance a seuil : jamais un chiffre invente', () => {
    expect(estimerAvantage(monde({ mechant: [10, 10] }))).toEqual({ etat: 'indisponible' })
  })

  it('les heros dominent : menace loin du seuil, mechant presque vaincu, heros en forme', () => {
    const r = estimerAvantage(monde({ menace: 1, seuil: 20, mechant: [3, 20], heros: [[10, 10]] }))
    expect(r.etat).toBe('ok')
    if (r.etat === 'ok') {
      expect(r.valeur).toBeGreaterThan(0.75)
      expect(r.mechantPct).toBe(15)
      expect(r.herosPct).toBe(100)
    }
  })

  it('la partie tourne mal : menace au bord du seuil, mechant intact, heros blesses, sbires engages', () => {
    const r = estimerAvantage(monde({ menace: 19, seuil: 20, mechant: [20, 20], heros: [[2, 10]], sbires: 4 }))
    expect(r.etat).toBe('ok')
    if (r.etat === 'ok') {
      expect(r.valeur).toBeLessThan(0.15)
      expect(r.tours).toBe(1)
      expect(r.sbires).toBe(4)
    }
  })

  it('la barre monte quand le mechant perd des PV, toutes choses egales', () => {
    const a = estimerAvantage(monde({ menace: 5, seuil: 20, mechant: [20, 20] }))
    const b = estimerAvantage(monde({ menace: 5, seuil: 20, mechant: [5, 20] }))
    if (a.etat === 'ok' && b.etat === 'ok') expect(b.valeur).toBeGreaterThan(a.valeur)
    else throw new Error('attendu : ok')
  })

  it('une menace au-dessus du seuil donne 0 tour ; des PV infinis sont ignores', () => {
    const m = monde({ menace: 25, seuil: 20, mechant: [10, 10] })
    ;(m.area_villain[0].info as Record<string, number | boolean>).is_infinite_health = true
    const r = estimerAvantage(m)
    if (r.etat === 'ok') {
      expect(r.tours).toBe(0)
      expect(r.mechantPct).toBeNull()
    } else throw new Error('attendu : ok')
  })
})
