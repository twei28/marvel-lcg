import { describe, expect, it } from 'vitest'
import { repriseDeCampagne, type RegleReprise } from './reprise-campagne'

const REGLE: RegleReprise = {
  quand: 'partie_perdue',
  standard_seulement: true,
  titre: 'L’enquête repart de zéro',
  texte: 'Nouvelle taupe, nouvelle enveloppe.',
}

const faits = (o: Partial<Parameters<typeof repriseDeCampagne>[0]> = {}) =>
  repriseDeCampagne({ final: true, regle: REGLE, gagne: false, expert: false, perdue: false, ...o })

describe('Reprise du dernier scénario après une défaite', () => {
  it('Perdu en standard au dernier scénario : la reprise s’applique', () => {
    const r = faits()
    expect(r.applicable).toBe(true)
    expect(r.titre).toBe('L’enquête repart de zéro')
    expect(r.texte).toContain('Nouvelle taupe')
  })

  it('Gagné : rien à re-préparer', () => {
    expect(faits({ gagne: true }).applicable).toBe(false)
  })

  it('En expert, le même encart perd la campagne : pas de reprise', () => {
    // Les deux règles sont le miroir l'une de l'autre ; les laisser s'appliquer
    // ensemble proposerait de rejouer une campagne qui vient de s'arrêter.
    expect(faits({ expert: true }).applicable).toBe(false)
  })

  it('Campagne déjà perdue : le verdict de défaite prime', () => {
    expect(faits({ perdue: true }).applicable).toBe(false)
  })

  it('Scénario intermédiaire : il se rejoue tel quel, sans rien re-préparer', () => {
    expect(faits({ final: false }).applicable).toBe(false)
  })

  it('Boîte sans règle de reprise : rien', () => {
    expect(faits({ regle: null }).applicable).toBe(false)
    expect(faits({ regle: undefined }).applicable).toBe(false)
  })
})
