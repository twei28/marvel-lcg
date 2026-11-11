import { render, screen } from '@testing-library/react'
import { describe, expect, it } from 'vitest'
import { PisteDesPhases } from './PisteDesPhases'
import { indexDepuisMoteur } from './phases-manuel'

const courante = () => document.querySelector('[aria-current="step"]')?.textContent

describe('piste des phases en lecture (Plateau animé, Accéléré)', () => {
  it('suit l’étape donnée par le moteur, sans boutons ni « Étape suivante »', () => {
    render(<PisteDesPhases round={4} lecture={{ round: 4, index: 2 }} />)
    expect(screen.getByText('Round 4')).toBeTruthy()
    expect(courante()).toBe('2. Activation du méchant')
    expect(screen.queryByRole('button', { name: 'Étape suivante ›' })).toBeNull()
    expect(screen.queryByRole('button', { name: '1. Menace' })).toBeNull()
  })

  it('aucune étape marquée quand la phase n’en a pas', () => {
    render(<PisteDesPhases round={1} lecture={{ round: 1, index: null }} />)
    expect(courante()).toBeUndefined()
  })

  it('traduit les phases du moteur en étapes', () => {
    expect(indexDepuisMoteur('Player 2 Turn')).toBe(0)
    expect(indexDepuisMoteur('Player Turn End')).toBe(0)
    expect(indexDepuisMoteur('Main Scheme Place Threat')).toBe(1)
    expect(indexDepuisMoteur('Enemy Activation')).toBe(2)
    expect(indexDepuisMoteur('Deal Encounter Cards')).toBe(4)
    expect(indexDepuisMoteur('Reveal Encounter Cards')).toBe(5)
    expect(indexDepuisMoteur('Resolve Mulligans')).toBeNull()
    expect(indexDepuisMoteur(undefined)).toBeNull()
  })
})
