import { describe, expect, it } from 'vitest'
import { render, screen } from '@testing-library/react'
import { EcranPortrait } from './EcranPortrait'

describe('EcranPortrait', () => {
  it('est un dialogue modal qui demande de tourner le telephone', () => {
    render(<EcranPortrait />)
    const voile = screen.getByRole('dialog', { name: 'Tourne ton téléphone' })
    expect(voile).toHaveAttribute('aria-modal', 'true')
    expect(voile).toHaveClass('ecran-portrait')
    expect(screen.getByText('Le plateau se joue en paysage.')).toBeInTheDocument()
  })
})
