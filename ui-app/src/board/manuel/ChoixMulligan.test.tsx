// La fenêtre du mulligan (« Mulligan Hand » d'OCTGN, lot 6 du 06/10/2026) :
// on coche les cartes de la main à changer, on confirme.
import { fireEvent, render } from '@testing-library/react'
import { describe, expect, it, vi } from 'vitest'
import { ChoixMulligan } from './ChoixMulligan'

const MAIN = [
  { id: 30, nom: 'Héliporteur' },
  { id: 31, nom: 'Uppercut' },
  { id: 32, nom: 'Black Cat' },
]

describe('le mulligan', () => {
  it('rend les cartes cochées, dans l’ordre de la main', () => {
    const onConfirmer = vi.fn()
    const { getByRole } = render(<ChoixMulligan main={MAIN} onConfirmer={onConfirmer} onFermer={vi.fn()} />)
    fireEvent.click(getByRole('checkbox', { name: 'Black Cat' }))
    fireEvent.click(getByRole('checkbox', { name: 'Héliporteur' }))
    fireEvent.click(getByRole('button', { name: /Changer 2/ }))
    expect(onConfirmer).toHaveBeenCalledWith([30, 32])
  })

  it('rien de coché : le bouton reste grisé', () => {
    const onConfirmer = vi.fn()
    const { getByRole } = render(<ChoixMulligan main={MAIN} onConfirmer={onConfirmer} onFermer={vi.fn()} />)
    const bouton = getByRole('button', { name: /Changer 0/ }) as HTMLButtonElement
    expect(bouton.disabled).toBe(true)
  })

  it('fermer sans confirmer n’envoie rien (bouton ou Échap)', () => {
    const onConfirmer = vi.fn()
    const onFermer = vi.fn()
    const { getByRole } = render(<ChoixMulligan main={MAIN} onConfirmer={onConfirmer} onFermer={onFermer} />)
    fireEvent.click(getByRole('button', { name: 'Annuler' }))
    fireEvent.keyDown(document, { key: 'Escape' })
    expect(onFermer).toHaveBeenCalledTimes(2)
    expect(onConfirmer).not.toHaveBeenCalled()
  })
})
