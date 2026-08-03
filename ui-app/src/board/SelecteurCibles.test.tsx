import { describe, expect, it, vi } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/react'
import { SelecteurCibles } from './SelecteurCibles'
import type { CibleHorsTable } from './interaction'

function cibleDeTest(agir = vi.fn()): CibleHorsTable {
  return {
    props: { id: '7', name: 'Iron Man', kind: 'ally', imageUrl: '/scan.jpg' },
    choisie: false,
    agir,
  }
}

describe('SelecteurCibles', () => {
  it('previent le survol quand la carte recoit le focus (tap ou tabulation)', () => {
    const survoler = vi.fn()
    render(
      <SelecteurCibles cibles={[cibleDeTest()]} titre="Choisis une cible" survoler={survoler} />
    )
    const carte = screen.getByRole('button', { name: /Iron Man/ })

    fireEvent.focus(carte)
    expect(survoler).toHaveBeenCalledWith({ id: '7', name: 'Iron Man', kind: 'ally', imageUrl: '/scan.jpg' })

    fireEvent.blur(carte)
    expect(survoler).toHaveBeenLastCalledWith(undefined)
  })

  it('le focus ne declenche pas le choix de la cible : agir() reste reserve au clic', () => {
    const agir = vi.fn()
    render(
      <SelecteurCibles cibles={[cibleDeTest(agir)]} titre="Choisis une cible" survoler={() => {}} />
    )
    const carte = screen.getByRole('button', { name: /Iron Man/ })

    fireEvent.focus(carte)
    expect(agir).not.toHaveBeenCalled()

    fireEvent.click(carte)
    expect(agir).toHaveBeenCalledOnce()
  })
})
