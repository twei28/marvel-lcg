import { describe, expect, it } from 'vitest'
import { prochaineOuverte } from './geste-carte'

describe('prochaineOuverte : tap ouvre, re-tap ferme', () => {
  it('ouvre une carte quand rien n est ouvert', () => {
    expect(prochaineOuverte(undefined, 'quinjet')).toBe('quinjet')
  })

  it('FERME la carte quand on retape la meme', () => {
    expect(prochaineOuverte('quinjet', 'quinjet')).toBeUndefined()
  })

  it('passe a l autre carte quand on en tape une differente', () => {
    expect(prochaineOuverte('quinjet', 'backflip')).toBe('backflip')
  })
})
