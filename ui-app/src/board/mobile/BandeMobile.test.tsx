import { describe, expect, it, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import { BandeMobile } from './BandeMobile'
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
})
