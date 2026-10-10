import { describe, expect, it } from 'vitest'
import { render } from '@testing-library/react'
import { DeroulePhase } from './DeroulePhase'
import type { EtapeDeroule } from './deroule-phase'

const etapes: EtapeDeroule[] = [
  { cle: 'a', temps: 'menace', titre: 'menace', regle: 'regle:menace', boosts: [] },
  {
    cle: 'b',
    temps: 'mechant',
    titre: 'attaque',
    regle: 'regle:activations',
    carteId: 50,
    cibleId: 12,
    auteurNom: 'Ultron',
    cibleNom: 'Shuri',
    boosts: [],
  },
]

describe('la phase du méchant en essai, sur téléphone', () => {
  it('prend le nouveau cartouche (feuille basse, cartouche-essai-tel.css)', () => {
    const { container } = render(<DeroulePhase telephone essai etapes={etapes} onTerminer={() => {}} />)
    expect(container.ownerDocument.querySelector('.deroule-phase.est-scene.est-essai')).not.toBeNull()
  })

  it('sans l essai, le téléphone garde le rendu d avant', () => {
    const { container } = render(<DeroulePhase telephone etapes={etapes} onTerminer={() => {}} />)
    expect(container.ownerDocument.querySelector('.deroule-phase.est-essai')).toBeNull()
    expect(container.ownerDocument.querySelector('.deroule-phase.est-scene')).toBeNull()
  })
})
