// La feuille d'une carte en ronds (Q51, Q71, Q72) : apercu tenu au doigt sans boutons, detail sous la carte, deux faces.
import { describe, expect, it, vi } from 'vitest'
import { fireEvent, render, screen } from '@testing-library/react'
import { CarteOuverte } from '../CarteOuverte'
import type { ScanCardProps } from '../../../components/ScanCard'

const carte = (autres: Partial<ScanCardProps> = {}): ScanCardProps => ({
  id: '1',
  name: 'Spider-Man',
  kind: 'hero',
  imageUrl: '/scan/a.jpg',
  statsComplets: [{ label: 'ATK', value: 3, base: 2 }],
  keywords: [{ nom: 'Garde', definition: 'Bloque les attaques.' }],
  ...autres,
})

describe('CarteOuverte en ronds', () => {
  it('montre les valeurs ajustees et les mots-cles comme le PC', () => {
    render(<CarteOuverte carte={carte()} onFermer={() => {}} detail />)
    expect(screen.getByText(/3 \(2 \+1\)/)).toBeTruthy()
    expect(screen.getByText('Garde')).toBeTruthy()
    expect(screen.getByRole('button', { name: 'Fermer' })).toBeTruthy()
  })
  it('met les deux faces cote a cote, sans bouton « Autre face »', () => {
    const { baseElement } = render(
      <CarteOuverte carte={carte({ autresFaces: [{ url: '/scan/b.jpg' }] })} onFermer={() => {}} detail />
    )
    expect(baseElement.querySelectorAll('.carte-ouverte-scan .scan-card').length).toBe(2)
    expect(screen.queryByRole('button', { name: 'Autre face' })).toBeNull()
  })
  it('l\'apercu tenu n\'a pas de boutons et se ferme au relacher', () => {
    const fermer = vi.fn()
    render(<CarteOuverte carte={carte({ onSelect: () => {} })} onFermer={fermer} detail apercuSeul />)
    expect(screen.queryByRole('button', { name: 'Fermer' })).toBeNull()
    fireEvent.pointerUp(window)
    expect(fermer).toHaveBeenCalled()
  })
})
