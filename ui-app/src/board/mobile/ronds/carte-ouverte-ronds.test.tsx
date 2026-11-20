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
  it('plusieurs faces : une seule carte a la fois, des fleches pour les autres', () => {
    const { baseElement } = render(
      <CarteOuverte
        carte={carte({ onSelect: () => {}, autresFaces: [{ url: '/scan/b.jpg' }, { url: '/scan/c.jpg' }] })}
        onFermer={() => {}}
        detail
      />
    )
    expect(baseElement.querySelectorAll('.carte-ouverte-scan .scan-card').length).toBe(1)
    expect(screen.queryByRole('button', { name: 'Autre face' })).toBeNull()
    expect(screen.getByText('1 / 3')).toBeTruthy()
    expect((screen.getByRole('button', { name: 'Carte précédente' }) as HTMLButtonElement).disabled).toBe(true)
    // La forme en jeu : le bouton d'action est la.
    expect(baseElement.querySelector('.carte-ouverte-agir')).toBeTruthy()
    fireEvent.click(screen.getByRole('button', { name: 'Carte suivante' }))
    expect(screen.getByText('2 / 3')).toBeTruthy()
    expect(baseElement.querySelector('.carte-ouverte-scan.est-autre-face')).toBeTruthy()
    // Une autre forme : rien a utiliser.
    expect(baseElement.querySelector('.carte-ouverte-agir')).toBeNull()
    fireEvent.click(screen.getByRole('button', { name: 'Carte suivante' }))
    expect(screen.getByText('3 / 3')).toBeTruthy()
    expect((screen.getByRole('button', { name: 'Carte suivante' }) as HTMLButtonElement).disabled).toBe(true)
    fireEvent.click(screen.getByRole('button', { name: 'Carte précédente' }))
    fireEvent.click(screen.getByRole('button', { name: 'Carte précédente' }))
    expect(baseElement.querySelector('.carte-ouverte-agir')).toBeTruthy()
  })
  it('une seule face : pas de fleches', () => {
    render(<CarteOuverte carte={carte()} onFermer={() => {}} detail />)
    expect(screen.queryByRole('button', { name: 'Carte suivante' })).toBeNull()
  })
  it('l\'apercu tenu n\'a pas de boutons et se ferme au relacher', () => {
    const fermer = vi.fn()
    render(<CarteOuverte carte={carte({ onSelect: () => {} })} onFermer={fermer} detail apercuSeul />)
    expect(screen.queryByRole('button', { name: 'Fermer' })).toBeNull()
    fireEvent.pointerUp(window)
    expect(fermer).toHaveBeenCalled()
  })
})
