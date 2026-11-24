import { beforeEach, describe, expect, it, vi } from 'vitest'
import { adresseCompteurPhase, reinitialiserCompteurPhase, signalerModePhase, valeurCompteurPhase } from './compteur-phase'

describe('valeurCompteurPhase', () => {
  it('compte le telephone a part, quel que soit le reglage', () => {
    expect(valeurCompteurPhase('instantane', 'tris', true)).toBe('telephone')
  })
  it('traduit les trois choix visibles', () => {
    expect(valeurCompteurPhase('detaille', 'tris', false)).toBe('guidee')
    expect(valeurCompteurPhase('sur-table', 'tris', false)).toBe('plateau_anime')
    expect(valeurCompteurPhase('instantane', 'tris', false)).toBe('accelere')
  })
  it("garde l'ancien « etape par etape » a part", () => {
    expect(valeurCompteurPhase('detaille', 'etape', false)).toBe('etape')
  })
})

describe('signalerModePhase', () => {
  beforeEach(() => reinitialiserCompteurPhase())
  const play = { origin: 'https://play.exemple.org', hostname: 'play.exemple.org' }
  it("n'envoie qu'une fois, vers le site principal, une valeur seule", () => {
    const envoyer = vi.fn()
    expect(signalerModePhase('guidee', play, envoyer)).toBe(true)
    expect(signalerModePhase('accelere', play, envoyer)).toBe(false)
    expect(envoyer).toHaveBeenCalledTimes(1)
    expect(envoyer).toHaveBeenCalledWith('https://exemple.org/compteur_phase_play', '{"phase":"guidee"}')
  })
  it('ne fait rien hors play', () => {
    const envoyer = vi.fn()
    expect(signalerModePhase('guidee', { origin: 'http://127.0.0.1:1', hostname: '127.0.0.1' }, envoyer)).toBe(false)
    expect(envoyer).not.toHaveBeenCalled()
    expect(adresseCompteurPhase('http://x', 'localhost')).toBeNull()
  })
  it('ne bloque jamais si l\'envoi echoue', () => {
    expect(signalerModePhase('guidee', play, () => { throw new Error('non') })).toBe(false)
  })
})
