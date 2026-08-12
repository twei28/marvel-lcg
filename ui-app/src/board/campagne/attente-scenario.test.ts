// Quand l'hôte lance le scénario suivant, les distants doivent suivre.
//
// Le signal le moins coûteux est celui qui existe déjà : la route dit quelle
// campagne et quel scénario sont en cours. Dès que le scénario change, une
// nouvelle partie a démarré.
import { describe, expect, it } from 'vitest'
import { scenarioSuivantLance } from './attente-scenario'

describe('le signal du scénario suivant', () => {
  it('dit oui quand le scénario en cours a changé', () => {
    expect(scenarioSuivantLance('crossbones', { id: 'trors-1', scenario: 'absorbing_man' })).toBe(true)
  })

  it("dit non tant que c'est le même scénario", () => {
    expect(scenarioSuivantLance('crossbones', { id: 'trors-1', scenario: 'crossbones' })).toBe(false)
  })

  it("dit non quand la route ne répond rien d'utile", () => {
    expect(scenarioSuivantLance('crossbones', null)).toBe(false)
    expect(scenarioSuivantLance('crossbones', {})).toBe(false)
    expect(scenarioSuivantLance('crossbones', { id: 'trors-1' })).toBe(false)
  })

  it("dit non quand la campagne n'a plus de partie en cours", () => {
    // Entre la validation de l'hôte et son prochain lancement, `partieEnCours`
    // vaut null : la route rend un scénario VIDE. Recharger à ce moment-là
    // renverrait les distants sur un plateau mort.
    expect(scenarioSuivantLance('crossbones', { id: 'trors-1', scenario: '' })).toBe(false)
  })

  it("dit non quand on ne sait pas quel scénario on joue", () => {
    // Sans scénario courant, tout changement paraîtrait en être un : on
    // rechargerait en boucle.
    expect(scenarioSuivantLance('', { id: 'trors-1', scenario: 'crossbones' })).toBe(false)
  })
})
