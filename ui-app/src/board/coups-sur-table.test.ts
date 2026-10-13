// Les coups qui arrivent sur la table (essai, 13/10/2026).
import { describe, expect, it } from 'vitest'
import { avecCompteursFiges, coupsDeLEtape, pointDeLaCourbe } from './coups-sur-table'
import type { EtapeDeroule } from './deroule-phase'
import type { World } from './world'

const etape = (o: Partial<EtapeDeroule>): EtapeDeroule =>
  ({ cle: 'e', temps: 'menace', titre: 'menace', regle: '', boosts: [], ...o }) as EtapeDeroule
const CORPS = { lieu: 'boite-corps' }

describe('les coups d un ecran', () => {
  it('etape 1 : la menace, de la boite vers la manigance, au niveau d avant', () => {
    expect(coupsDeLEtape(etape({ cibleId: 7, montant: 1, restant: 2 }))).toEqual([
      { genre: 'menace', cibleId: 7, avant: 1, montant: 1, depuis: CORPS },
    ])
  })

  it('manigance du mechant : depuis la boite, avant donne par le moteur', () => {
    const c = coupsDeLEtape(etape({ temps: 'mechant', titre: 'manigance', etat: 'resolu', carteId: 50, cibleId: 7, montant: 3, restant: 5, menaceAvant: 2 }))
    expect(c).toEqual([{ genre: 'menace', cibleId: 7, avant: 2, montant: 3, depuis: CORPS }])
  })

  it('manigance d un sbire : depuis sa carte', () => {
    const c = coupsDeLEtape(etape({ temps: 'sbires', titre: 'manigance', etat: 'resolu', carteId: 70, cibleId: 7, montant: 1, restant: 6 }))
    expect(c[0].depuis).toEqual({ lieu: 'table', id: 70 })
  })

  it('attaque : des degats de l attaquant vers la carte touchee, PV d avant', () => {
    const c = coupsDeLEtape(etape({ temps: 'mechant', titre: 'attaque', etat: 'resolu', carteId: 50, cibleId: 12, montant: 3, restant: 7 }))
    expect(c).toEqual([{ genre: 'degats', cibleId: 12, avant: 10, montant: 3, depuis: { lieu: 'table', id: 50 } }])
  })

  it('attaque suivie d une Riposte : l attaquant reste fige a ses PV d avant, sans jeton', () => {
    const c = coupsDeLEtape(
      etape({ temps: 'sbires', titre: 'attaque', etat: 'resolu', carteId: 70, cibleId: 12, montant: 1, restant: 9, riposte: { degats: 2, restant: 1 } })
    )
    expect(c[1]).toEqual({ genre: 'degats', cibleId: 70, avant: 3, montant: 0, depuis: CORPS })
  })

  it('Riposte : du heros vers le sbire', () => {
    const c = coupsDeLEtape(etape({ temps: 'sbires', titre: 'riposte', etat: 'resolu', carteId: 12, cibleId: 70, montant: 2, restant: 1 }))
    expect(c).toEqual([{ genre: 'degats', cibleId: 70, avant: 3, montant: 2, depuis: { lieu: 'table', id: 12 } }])
  })

  it('carte revelee : un coup par effet chiffre, depuis la carte dans la boite', () => {
    const c = coupsDeLEtape(
      etape({
        temps: 'revelation',
        titre: 'revelation',
        carteId: 99,
        effets: [
          { genre: 'menace', cible: 'M', cible_id: 7, montant: 2, restant: 4 },
          { genre: 'degats', cible: 'H', cible_id: 12, montant: 1, restant: 9 },
          { genre: 'degats', cible: 'X', cible_id: 13, montant: 1, restant: null },
        ],
      })
    )
    expect(c.map((x) => [x.genre, x.cibleId, x.avant])).toEqual([
      ['menace', 7, 2],
      ['degats', 12, 10],
    ])
    expect(c[0].depuis).toEqual({ lieu: 'boite', id: 99 })
  })

  it('une annonce, une annulation ou un coup sans chiffre : rien', () => {
    expect(coupsDeLEtape(etape({ temps: 'mechant', titre: 'attaque', etat: 'annonce', carteId: 50, cibleId: 12, montant: 3, restant: 7 }))).toEqual([])
    expect(coupsDeLEtape(etape({ cibleId: 7, montant: 2, restant: 2, etat: 'annule' }))).toEqual([])
    expect(coupsDeLEtape(etape({ cibleId: 7, restant: 2 }))).toEqual([])
    expect(coupsDeLEtape(undefined)).toEqual([])
  })
})

describe('le monde aux compteurs figes', () => {
  const monde = {
    area_schemes_main: [{ id: 7, info: { k_threat: 2 } }],
    players: [{ area_hero: [{ id: 12, info: { health: 7 } }], allies: [{ id: 13, info: { health: 3 } }] }],
  } as unknown as World
  const lire = (w: World) => w as unknown as { area_schemes_main: Array<{ info: { k_threat: number } }>; players: Array<{ area_hero: Array<{ info: { health: number } }>; allies: Array<{ info: { health: number } }> }> }

  it('fige menace et PV ou que soit la carte, sans toucher au monde recu', () => {
    const fige = lire(avecCompteursFiges(monde, [{ genre: 'menace', cibleId: 7, valeur: 1 }, { genre: 'degats', cibleId: 12, valeur: 10 }]))
    expect(fige.area_schemes_main[0].info.k_threat).toBe(1)
    expect(fige.players[0].area_hero[0].info.health).toBe(10)
    expect(fige.players[0].allies[0].info.health).toBe(3)
    expect(lire(monde).players[0].area_hero[0].info.health).toBe(7)
  })

  it('rien a figer ou carte absente : le meme monde', () => {
    expect(avecCompteursFiges(monde, [])).toBe(monde)
    expect(avecCompteursFiges(monde, [{ genre: 'degats', cibleId: 404, valeur: 1 }])).toBe(monde)
  })
})

describe('la courbe du vol', () => {
  it('part du depart et finit a l arrivee', () => {
    const d = { x: 0, y: 0 }
    const a = { x: 100, y: 50 }
    expect(pointDeLaCourbe(d, { x: 40, y: -30 }, a, 0)).toEqual(d)
    expect(pointDeLaCourbe(d, { x: 40, y: -30 }, a, 1)).toEqual(a)
  })
})
