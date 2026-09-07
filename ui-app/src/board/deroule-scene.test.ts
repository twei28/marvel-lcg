// Ce qu'une etape montre dans la scene centrale : quelles cartes, dans quel
// ordre, avec ou sans fleche, et faut-il assombrir la table derriere.
//
// Module PUR, sans DOM : la decision se teste ici, la pose se fait ailleurs
// (useDerouleScene.ts pour le voile, DeroulePhase.tsx pour les cartes).
import { describe, expect, it } from 'vitest'
import { sceneDe } from './deroule-scene'
import type { EtapeDeroule } from './deroule-phase'

const etape = (extra: Partial<EtapeDeroule> = {}): EtapeDeroule => ({
  cle: 'k',
  temps: 'sbires',
  titre: 'attaque',
  regle: 'regle:activations',
  boosts: [],
  ...extra,
})

describe('les cartes de la scene', () => {
  it('une activation : l auteur, ses boosts, une fleche, la cible', () => {
    const scene = sceneDe(
      etape({
        carteId: 7,
        cibleId: 9,
        boosts: [
          { cle: 'b1', nom: 'Photographic Reflexes', cibleId: 31, apport: 2 },
          { cle: 'b2', nom: 'Whip', cibleId: 32, apport: 1 },
        ],
      })
    )
    expect(scene.cartes).toEqual([
      { role: 'auteur', id: 7 },
      { role: 'boost', id: 31 },
      { role: 'boost', id: 32 },
      { role: 'cible', id: 9 },
    ])
    expect(scene.fleche).toBe(true)
    expect(scene.voile).toBe(true)
  })

  it('une activation annoncee : pas encore de boost, mais deja la fleche', () => {
    const scene = sceneDe(etape({ carteId: 7, cibleId: 9, etat: 'annonce' }))
    expect(scene.cartes).toEqual([
      { role: 'auteur', id: 7 },
      { role: 'cible', id: 9 },
    ])
    expect(scene.fleche).toBe(true)
  })

  it('un auteur qui est sa propre cible : une seule carte, pas de fleche', () => {
    const scene = sceneDe(etape({ carteId: 7, cibleId: 7 }))
    expect(scene.cartes).toEqual([{ role: 'auteur', id: 7 }])
    expect(scene.fleche).toBe(false)
  })

  it('la menace : la manigance seule, sans auteur ni fleche', () => {
    const scene = sceneDe(etape({ temps: 'menace', titre: 'menace', cibleId: 12 }))
    expect(scene.cartes).toEqual([{ role: 'cible', id: 12 }])
    expect(scene.fleche).toBe(false)
    expect(scene.voile).toBe(true)
  })

  it('la distribution : un dos de carte, le moteur ne dit pas laquelle', () => {
    const scene = sceneDe(etape({ temps: 'distribution', titre: 'distribution' }))
    expect(scene.cartes).toEqual([{ role: 'dos' }])
    expect(scene.fleche).toBe(false)
  })

  it('la distribution de deux cartes : deux dos', () => {
    const scene = sceneDe(etape({ temps: 'distribution', titre: 'distribution', montant: 2 }))
    expect(scene.cartes).toEqual([{ role: 'dos' }, { role: 'dos' }])
  })

  it('la revelation : la carte revelee, face visible', () => {
    const scene = sceneDe(etape({ temps: 'revelation', titre: 'revelation', carteId: 40 }))
    expect(scene.cartes).toEqual([{ role: 'revelee', id: 40 }])
    expect(scene.fleche).toBe(false)
  })

  it('le bilan : aucune carte, et rien a assombrir', () => {
    const scene = sceneDe(etape({ temps: 'bilan', titre: 'bilan', bilan: [] }))
    expect(scene.cartes).toEqual([])
    expect(scene.voile).toBe(false)
  })

  it('une etape sans aucune carte connue ne montre rien', () => {
    const scene = sceneDe(etape({}))
    expect(scene.cartes).toEqual([])
    expect(scene.voile).toBe(false)
  })
})
