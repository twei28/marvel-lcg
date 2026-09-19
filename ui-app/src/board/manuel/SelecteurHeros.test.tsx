// SelecteurHeros.test.tsx — le sélecteur de héros du mode manuel (tâche 7 bis).
//
// Trois cas du brief : un bouton par héros, celui qu'on regarde est marqué,
// un clic sur un autre appelle `onRegarder` avec son index. Plus un cas
// limite explicite du brief : à un seul héros, le sélecteur ne montre rien
// (même garde que `OngletsJoueurs`, dont il reprend l'idée pour le mode
// manuel : voir board/mobile/OngletsJoueurs.tsx).
import { fireEvent, render, screen } from '@testing-library/react'
import { describe, expect, it, vi } from 'vitest'
import { SelecteurHeros } from './SelecteurHeros'

describe('SelecteurHeros', () => {
  it('un bouton par héros', () => {
    render(
      <SelecteurHeros
        joueurs={[
          { id: 0, nom: 'Spider-Man' },
          { id: 1, nom: 'Iron Man' },
        ]}
        regarde={0}
        onRegarder={() => {}}
      />
    )
    expect(screen.getByRole('tab', { name: 'Spider-Man' })).toBeInTheDocument()
    expect(screen.getByRole('tab', { name: 'Iron Man' })).toBeInTheDocument()
  })

  it('celui qu on regarde est marqué', () => {
    render(
      <SelecteurHeros
        joueurs={[
          { id: 0, nom: 'Spider-Man' },
          { id: 1, nom: 'Iron Man' },
        ]}
        regarde={1}
        onRegarder={() => {}}
      />
    )
    expect(screen.getByRole('tab', { name: 'Iron Man' })).toHaveAttribute('aria-selected', 'true')
    expect(screen.getByRole('tab', { name: 'Spider-Man' })).toHaveAttribute('aria-selected', 'false')
  })

  it('un clic sur un autre héros appelle onRegarder avec son index', () => {
    const onRegarder = vi.fn()
    render(
      <SelecteurHeros
        joueurs={[
          { id: 0, nom: 'Spider-Man' },
          { id: 1, nom: 'Iron Man' },
        ]}
        regarde={0}
        onRegarder={onRegarder}
      />
    )
    fireEvent.click(screen.getByRole('tab', { name: 'Iron Man' }))
    expect(onRegarder).toHaveBeenCalledWith(1)
  })

  it('ne montre rien à un seul héros : un sélecteur à une entrée n’apprend rien', () => {
    const { container } = render(
      <SelecteurHeros joueurs={[{ id: 0, nom: 'Spider-Man' }]} regarde={0} onRegarder={() => {}} />
    )
    expect(container.firstChild).toBeNull()
  })
})
