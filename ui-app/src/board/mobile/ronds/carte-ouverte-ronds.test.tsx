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
  it('montre les deux faces, sans bouton « Autre face »', () => {
    const { baseElement } = render(
      <CarteOuverte carte={carte({ autresFaces: [{ url: '/scan/b.jpg' }] })} onFermer={() => {}} detail />
    )
    expect(baseElement.querySelectorAll('.carte-ouverte-scan .scan-card').length).toBe(2)
    expect(screen.queryByRole('button', { name: 'Autre face' })).toBeNull()
  })
  it('trois faces : classe a-faces-3 (deux puis une), toutes visibles, pas de miniatures', () => {
    const { baseElement } = render(
      <CarteOuverte carte={carte({ autresFaces: [{ url: '/scan/b.jpg' }, { url: '/scan/c.jpg' }] })} onFermer={() => {}} detail />
    )
    expect(baseElement.querySelector('.carte-ouverte-scan.a-faces-3')).toBeTruthy()
    expect(baseElement.querySelectorAll('.carte-ouverte-scan .scan-card').length).toBe(3)
    expect(baseElement.querySelector('.carte-ouverte-miniatures')).toBeNull()
  })
  it('quatre faces et plus : une grande, les autres en miniatures, un toucher change la grande', () => {
    const { baseElement } = render(
      <CarteOuverte
        carte={carte({ autresFaces: [{ url: '/scan/b.jpg' }, { url: '/scan/c.jpg' }, { url: '/scan/d.jpg' }] })}
        onFermer={() => {}}
        detail
      />
    )
    expect(baseElement.querySelector('.carte-ouverte-scan.a-faces-plus')).toBeTruthy()
    expect(baseElement.querySelectorAll('.carte-ouverte-scan .scan-card').length).toBe(1)
    const miniatures = baseElement.querySelectorAll('.carte-ouverte-miniature')
    expect(miniatures.length).toBe(3)
    fireEvent.click(miniatures[0] as Element)
    // La face touchee devient la grande ; la face en jeu rejoint les miniatures.
    expect(baseElement.querySelectorAll('.carte-ouverte-miniature').length).toBe(3)
    expect(baseElement.querySelector('.carte-ouverte-scan.est-autre-face')).toBeTruthy()
  })
  it('deux faces : l\'une sous l\'autre (classe a-faces-2)', () => {
    const { baseElement } = render(
      <CarteOuverte carte={carte({ autresFaces: [{ url: '/scan/b.jpg' }] })} onFermer={() => {}} detail />
    )
    expect(baseElement.querySelector('.carte-ouverte-scan.a-faces-2')).toBeTruthy()
  })
  it('l\'apercu tenu n\'a pas de boutons et se ferme au relacher', () => {
    const fermer = vi.fn()
    render(<CarteOuverte carte={carte({ onSelect: () => {} })} onFermer={fermer} detail apercuSeul />)
    expect(screen.queryByRole('button', { name: 'Fermer' })).toBeNull()
    fireEvent.pointerUp(window)
    expect(fermer).toHaveBeenCalled()
  })
})
