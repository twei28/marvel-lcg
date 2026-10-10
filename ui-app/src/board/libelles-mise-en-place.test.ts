import { afterEach, describe, expect, it } from 'vitest'
import { libelleTypeDemande } from './DemandeCentrale'
import { libellePhase } from './etat-partie'
import type { Demande } from './ask'
import type { World } from './world'

const demande = (ability_type: string): Demande =>
  ({ ability_type, event_name: 'WhenGameBeginSetup', prompt_text: '' }) as unknown as Demande

const monde = (phase: string): World =>
  ({ render_id: 1, round_id: 0, phase, prompt: '', players: [] }) as unknown as World

afterEach(() => window.localStorage.removeItem('marvel-langue'))

describe('surtitre d’une question « Normal » (question Starting, n°70)', () => {
  it('en français : « À toi de jouer »', () => {
    expect(libelleTypeDemande(demande('Normal'))).toBe('À toi de jouer')
  })

  it('en anglais : « Your move », plus jamais « Normal »', () => {
    window.localStorage.setItem('marvel-langue', 'en')
    expect(libelleTypeDemande(demande('Normal'))).toBe('Your move')
  })
})

describe('phase « Initialize » de la mise en place', () => {
  it('traduite dans les deux langues', () => {
    expect(libellePhase(monde('Initialize'))).toBe('Initialisation')
    window.localStorage.setItem('marvel-langue', 'en')
    expect(libellePhase(monde('Initialize'))).toBe('Setting up')
  })
})
