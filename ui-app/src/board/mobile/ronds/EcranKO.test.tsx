import { describe, expect, it } from 'vitest'
import { fireEvent, render, screen } from '@testing-library/react'
import { EcranKO } from './EcranKO'

describe('EcranKO (decision Q65)', () => {
  it('ne montre rien tant que le heros tient', () => {
    const { container } = render(<EcranKO elimine={false} nom="Spider-Man" />)
    expect(container.firstChild).toBeNull()
  })
  it('montre K.O. et le nom du heros eliminé, puis se ferme au toucher', () => {
    render(<EcranKO elimine nom="Spider-Man" />)
    expect(screen.getByRole('alertdialog')).toBeTruthy()
    expect(screen.getByText('Spider-Man')).toBeTruthy()
    fireEvent.click(screen.getByRole('button'))
    expect(screen.queryByRole('alertdialog')).toBeNull()
  })
})
