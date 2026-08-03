import { describe, expect, it, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import { BandeMobile, BandeResume } from './BandeMobile'
import type { BandeAffichee } from './bandes'
import type { ScanCardProps } from '../../components/ScanCard'

function carte(id: number): ScanCardProps {
  return { id: String(id), name: `Allié ${id}`, kind: 'ally', imageUrl: '' }
}

function bande(nombre: number): BandeAffichee {
  return {
    cle: 'terrain',
    titre: 'Terrain',
    emplacements: [
      {
        cle: 'terrain-combat',
        titre: 'Terrain',
        nombreSurLaLigne: nombre,
        groupes: [
          Array.from({ length: nombre }, (_, index) => ({
            cle: `u${index}`,
            carte: carte(index),
            attachees: [],
          })),
        ],
      },
    ],
  }
}

describe('BandeMobile', () => {
  it('montre son titre et ses tuiles', () => {
    render(
      <BandeMobile
        bande={bande(2)}
        budget={{ largeur: 464, hauteur: 200 }}
        onOuvrirBande={() => {}}
        onOuvrirCarte={() => {}}
      />
    )
    expect(screen.getByText('Terrain')).toBeInTheDocument()
    expect(screen.getByText('Allié 0')).toBeInTheDocument()
  })

  it('replie le surplus dans une pastille qui ouvre la bande', () => {
    const ouvrir = vi.fn()
    render(
      <BandeMobile
        bande={bande(30)}
        budget={{ largeur: 464, hauteur: 72 }}
        onOuvrirBande={ouvrir}
        onOuvrirCarte={() => {}}
      />
    )
    const pastille = screen.getByRole('button', { name: /\+\d+/ })
    pastille.click()
    expect(ouvrir).toHaveBeenCalledOnce()
  })

  it('ouvre la carte touchee, pas la bande', () => {
    const ouvrirBande = vi.fn()
    const ouvrirCarte = vi.fn()
    render(
      <BandeMobile
        bande={bande(2)}
        budget={{ largeur: 464, hauteur: 200 }}
        onOuvrirBande={ouvrirBande}
        onOuvrirCarte={ouvrirCarte}
      />
    )
    screen.getByRole('button', { name: /Allié 1/ }).click()
    expect(ouvrirCarte).toHaveBeenCalledOnce()
    expect(ouvrirBande).not.toHaveBeenCalled()
  })

  it('affiche le compte de cibles pendant un ciblage', () => {
    render(
      <BandeMobile
        bande={bande(2)}
        budget={{ largeur: 464, hauteur: 200 }}
        cibles={3}
        onOuvrirBande={() => {}}
        onOuvrirCarte={() => {}}
      />
    )
    expect(screen.getByRole('button', { name: /Terrain/ })).toHaveTextContent('3')
  })
})

describe('BandeResume : la bande degradee', () => {
  it('ne rend AUCUNE tuile, donc rien qui puisse etre coupe', () => {
    const { container } = render(
      <BandeResume bande={bande(30)} onOuvrirBande={() => {}} />
    )
    expect(container.querySelector('.bande-tuiles')).toBeNull()
    expect(container.querySelectorAll('[data-tactile="tuile"]')).toHaveLength(0)
  })

  it('reste une cible tactile qui ouvre la bande en focus', () => {
    const ouvrir = vi.fn()
    render(<BandeResume bande={bande(30)} onOuvrirBande={ouvrir} />)
    const ligne = screen.getByRole('button', { name: /Terrain/ })
    expect(ligne).toHaveAttribute('data-tactile', 'titre-bande')
    ligne.click()
    expect(ouvrir).toHaveBeenCalledOnce()
  })

  it('dit combien de cartes la bande contient', () => {
    render(<BandeResume bande={bande(30)} onOuvrirBande={() => {}} />)
    expect(screen.getByRole('button', { name: /Terrain/ })).toHaveTextContent('30')
  })
})
