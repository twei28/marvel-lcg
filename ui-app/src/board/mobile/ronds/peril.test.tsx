import { afterEach, describe, expect, it } from 'vitest'
import { act, render, renderHook, screen } from '@testing-library/react'
import { OngletsJoueurs } from '../OngletsJoueurs'
import { usePerilJoueur } from './useDroitDeReponse'

afterEach(() => delete document.documentElement.dataset.perilJoueur)

describe('Peril en multijoueur (Q68)', () => {
  it('l\'onglet de l\'autre joueur est verrouille pendant la carte', () => {
    render(
      <OngletsJoueurs joueurs={[{ id: 0, nom: 'J1' }, { id: 1, nom: 'J2' }]} actif={0} choisir={() => {}} verrouilles={[1]} />
    )
    const j2 = screen.getByRole('tab', { name: /J2/ }) as HTMLButtonElement
    expect(j2.disabled).toBe(true)
    expect(j2.textContent).toContain('🔒')
    expect((screen.getByRole('tab', { name: 'J1' }) as HTMLButtonElement).disabled).toBe(false)
  })
  it('lit le joueur du Peril pose sur <html> et suit ses changements', async () => {
    const { result } = renderHook(() => usePerilJoueur())
    expect(result.current).toBeUndefined()
    await act(async () => {
      document.documentElement.dataset.perilJoueur = '1'
      await Promise.resolve()
    })
    expect(result.current).toBe(1)
  })
})
