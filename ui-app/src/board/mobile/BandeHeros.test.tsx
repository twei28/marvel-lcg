import { describe, expect, it } from 'vitest'
import { fireEvent, render, screen } from '@testing-library/react'
import { BandeHeros } from './BandeHeros'
import type { BandeAffichee } from './bandes'
import type { ScanCardProps } from '../../components/ScanCard'

function carte(id: number, overrides: Partial<ScanCardProps> = {}): ScanCardProps {
  return { id: String(id), name: `Carte ${id}`, kind: 'ally', imageUrl: '', ...overrides }
}

// terrain-soutien porte deux groupes, un par joueur (identite + un allie chacun) ;
// les autres emplacements de la bande n'appartiennent qu'au siege regarde.
function bandeDeuxJoueurs(): BandeAffichee {
  return {
    cle: 'heros',
    titre: 'Heros',
    emplacements: [
      {
        cle: 'terrain-soutien',
        titre: 'Heros et soutiens',
        nombreSurLaLigne: 4,
        groupes: [
          [
            {
              cle: 'h0',
              carte: carte(0, { name: 'Captain Marvel', kind: 'hero', allyHp: '10/10' }),
              attachees: [],
            },
          ],
          [
            {
              cle: 'h1',
              carte: carte(1, { name: 'Iron Man', kind: 'hero', allyHp: '8/9' }),
              attachees: [],
            },
          ],
        ],
        proprietaires: [0, 1],
      },
    ],
  }
}

function bandeUnJoueur(): BandeAffichee {
  return {
    cle: 'heros',
    titre: 'Heros',
    emplacements: [
      {
        cle: 'terrain-soutien',
        titre: 'Heros et soutiens',
        nombreSurLaLigne: 2,
        groupes: [
          [{ cle: 'h0', carte: carte(0, { name: 'Captain Marvel', kind: 'hero' }), attachees: [] }],
        ],
        proprietaires: [0],
      },
    ],
  }
}

const BUDGET = { largeur: 464, hauteur: 200 }

describe('BandeHeros', () => {
  it('a deux joueurs, montre les unites de playerId et replie les autres', () => {
    render(
      <BandeHeros
        bande={bandeDeuxJoueurs()}
        budget={BUDGET}
        playerId={0}
        onOuvrirBande={() => {}}
        onOuvrirCarte={() => {}}
      />
    )

    expect(screen.getByRole('button', { name: /Captain Marvel/ })).toHaveAttribute(
      'data-tactile',
      'tuile'
    )

    const nomsIronMan = screen.getAllByText('Iron Man')
    expect(nomsIronMan).toHaveLength(1)
    expect(nomsIronMan[0].closest('[data-tactile="joueur-replie"]')).not.toBeNull()
  })

  it('un appui sur le bandeau replie deplie l\'autre joueur et replie playerId', () => {
    render(
      <BandeHeros
        bande={bandeDeuxJoueurs()}
        budget={BUDGET}
        playerId={0}
        onOuvrirBande={() => {}}
        onOuvrirCarte={() => {}}
      />
    )

    fireEvent.click(screen.getByRole('button', { name: /Iron Man/ }))

    expect(screen.getByRole('button', { name: /Iron Man/ })).toHaveAttribute(
      'data-tactile',
      'tuile'
    )
    const nomsCaptain = screen.getAllByText('Captain Marvel')
    expect(nomsCaptain).toHaveLength(1)
    expect(nomsCaptain[0].closest('[data-tactile="joueur-replie"]')).not.toBeNull()
  })

  it('a un seul joueur, aucun bandeau replie n\'est rendu', () => {
    const { container } = render(
      <BandeHeros
        bande={bandeUnJoueur()}
        budget={BUDGET}
        playerId={0}
        onOuvrirBande={() => {}}
        onOuvrirCarte={() => {}}
      />
    )

    expect(container.querySelectorAll('[data-tactile="joueur-replie"]')).toHaveLength(0)
  })

  it('le bandeau replie affiche les points de vie de l\'identite qu\'il represente', () => {
    render(
      <BandeHeros
        bande={bandeDeuxJoueurs()}
        budget={BUDGET}
        playerId={0}
        onOuvrirBande={() => {}}
        onOuvrirCarte={() => {}}
      />
    )

    const bandeau = screen.getByRole('button', { name: /Iron Man/ })
    expect(bandeau).toHaveTextContent('8/9')
  })
})
