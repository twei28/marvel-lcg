import { render, screen } from '@testing-library/react'
import { describe, expect, it } from 'vitest'
import { CompteursPortrait } from './CompteursPortrait'

describe('CompteursPortrait', () => {
  it('affiche un gros chiffre par compteur, avec son libelle', () => {
    render(
      <CompteursPortrait
        compteurs={[
          { valeur: 33, libelle: 'Rencontre' },
          { valeur: 0, libelle: 'Défausse' },
        ]}
      />
    )
    expect(screen.getByText('33')).toBeInTheDocument()
    expect(screen.getByText('Rencontre')).toBeInTheDocument()
    expect(screen.getByText('0')).toBeInTheDocument()
    expect(screen.getByText('Défausse')).toBeInTheDocument()
  })

  it('sans compteur, n affiche rien', () => {
    const { container } = render(<CompteursPortrait compteurs={[]} />)
    expect(container.querySelector('.portrait-compteurs')).toBeNull()
  })
})
