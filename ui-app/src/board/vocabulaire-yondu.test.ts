import { describe, expect, it, beforeEach } from 'vitest'
import { traduireMoteur } from './vocabulaire-moteur'

describe('choix de la flèche de Yondu en français', () => {
  beforeEach(() => { try { localStorage.setItem('marvel-langue', 'fr') } catch { /* sans stockage */ } })
  it.each([
    ['Attach Yaka Arrow to an enemy', 'Attacher la Flèche Yaka à un ennemi'],
    ['Attach Yaka Arrow to your identity', 'Attacher la Flèche Yaka à ton identité'],
    ['Add Yaka Arrow to your hand', 'Ajouter la Flèche Yaka à ta main'],
  ])('%s', (anglais, francais) => {
    expect(traduireMoteur(anglais)).toBe(francais)
  })
})
