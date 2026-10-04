// La roue de couleurs du fond : clavier, curseur, couleur d'origine.
import { fireEvent, render, screen } from '@testing-library/react'
import { describe, expect, it, vi } from 'vitest'
import { RoueTeinte } from './RoueTeinte'

describe('RoueTeinte', () => {
  it('au clavier : droite tourne la teinte, haut augmente la saturation (bornee)', () => {
    const changer = vi.fn()
    render(<RoueTeinte valeur={{ h: 350, s: 18, l: 20 }} changer={changer} reinitialiser={vi.fn()} />)
    const roue = screen.getByRole('slider', { name: 'Teinte du fond' })
    fireEvent.keyDown(roue, { key: 'ArrowRight' })
    expect(changer).toHaveBeenLastCalledWith({ h: 355, s: 18, l: 20 })
    fireEvent.keyDown(roue, { key: 'ArrowRight', shiftKey: true })
    expect(changer).toHaveBeenLastCalledWith({ h: 5, s: 18, l: 20 })
    fireEvent.keyDown(roue, { key: 'ArrowUp' })
    expect(changer).toHaveBeenLastCalledWith({ h: 350, s: 18, l: 20 })
  })

  it('le curseur regle la luminosite', () => {
    const changer = vi.fn()
    render(<RoueTeinte valeur={{ h: 120, s: 6, l: 20 }} changer={changer} reinitialiser={vi.fn()} />)
    fireEvent.change(screen.getByLabelText('Luminosité du fond'), { target: { value: '55' } })
    expect(changer).toHaveBeenLastCalledWith({ h: 120, s: 6, l: 55 })
  })

  it('« Couleur d’origine » : grise sans choix, efface le choix sinon', () => {
    const reinitialiser = vi.fn()
    const { rerender } = render(<RoueTeinte valeur={undefined} changer={vi.fn()} reinitialiser={reinitialiser} />)
    expect(screen.getByRole('button', { name: 'Couleur d’origine' })).toBeDisabled()
    rerender(<RoueTeinte valeur={{ h: 10, s: 4, l: 30 }} changer={vi.fn()} reinitialiser={reinitialiser} />)
    fireEvent.click(screen.getByRole('button', { name: 'Couleur d’origine' }))
    expect(reinitialiser).toHaveBeenCalledTimes(1)
  })
})
