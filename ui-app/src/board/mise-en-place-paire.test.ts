import { describe, expect, it } from 'vitest'
import { etapesNouvelles, paireEnTete, sansMoitiesDejaMontrees, type EtapeMiseEnPlace } from './mise-en-place-pas-a-pas'
import { carteSurTable } from './plateau-de-test'
import type { World } from './world'

describe('paire jumelle en tete de la mise en place (The City + Never Sleeps)', () => {
  // `genre: 'arrivee'` comme les vraies arrivees (etapesNouvelles), sinon le test passe a cote du cas reel.
  const e = (code: string, id: number, genre: 'arrivee' | 'degats' = 'arrivee'): EtapeMiseEnPlace => ({
    cle: code, carteId: id, picId: code, codeCarte: code, type: 'Environment', traits: [], legende: 'Environnement', paysage: false, genre,
  })
  it('les deux arrivees se montrent ensemble, la 1re a gauche, quel que soit leur ordre', () => {
    expect(paireEnTete([e('pu006', 6), e('pu034', 34), e('pu005', 5)])).toEqual({ gauche: e('pu005', 5), droite: e('pu006', 6) })
  })
  it("la soeur pas encore arrivee est montree d'apres son code", () => {
    const paire = paireEnTete([e('pu005', 5), e('pu034', 34)])
    expect(paire?.gauche.carteId).toBe(5)
    expect(paire?.droite).toMatchObject({ codeCarte: 'pu006', picId: 'pu006', carteId: -1 })
  })
  it('une carte hors paire en tete : rien', () => {
    expect(paireEnTete([e('pu034', 34), e('pu005', 5), e('pu006', 6)])).toBeUndefined()
  })
  it("l'arrivee d'une moitie deja montree est ecartee, pas ses degats", () => {
    const montrees = new Set(['pu005', 'pu006'])
    expect(sansMoitiesDejaMontrees([e('pu006', 6), e('pu034', 34), e('pu006', 6, 'degats')], montrees).map((x) => [x.codeCarte, x.genre])).toEqual([
      ['pu034', 'arrivee'],
      ['pu006', 'degats'],
    ])
  })
})

describe('traits de la mise en place', () => {
  it("retire le prefixe « t_ » des clefs du moteur (sinon « T_LOCATION. » s'affiche)", () => {
    const carte = carteSurTable(1, 'zz001', 'Environment', 'Test', { traits: { t_LOCATION: 1, t_DARK_ELF: 1 } })
    const { etapes } = etapesNouvelles(new Map(), { area_environment: [carte], players: [] } as unknown as World, { panneauPrincipale: false, panneauAnnexe: false })
    expect(etapes[0]?.traits).toEqual(['LOCATION', 'DARK ELF'])
  })
})
