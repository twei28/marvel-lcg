import { act, fireEvent, render, screen } from '@testing-library/react'
import { afterEach, describe, expect, it, vi } from 'vitest'
import { BandeauPortrait } from './BandeauPortrait'
import { URL_MANIFESTE, preparerInstallation, retenirDemandePourTest, type DemandeInstallation } from './installation'

const demande = (outcome: 'accepted' | 'dismissed' = 'accepted') => {
  const prompt = vi.fn(() => Promise.resolve())
  return {
    prompt,
    evenement: Object.assign(new Event('beforeinstallprompt'), {
      prompt,
      userChoice: Promise.resolve({ outcome }),
    }) as DemandeInstallation,
  }
}

describe('installer le jeu comme une application (zone 3)', () => {
  afterEach(() => {
    act(() => retenirDemandePourTest(undefined))
  })

  it('pose le manifeste une seule fois, et retient la demande du navigateur sans bandeau', () => {
    preparerInstallation()
    preparerInstallation()
    const liens = document.querySelectorAll('link[rel="manifest"]')
    expect(liens).toHaveLength(1)
    expect(liens[0]).toHaveAttribute('href', URL_MANIFESTE)
    const { evenement } = demande()
    const empecher = vi.spyOn(evenement, 'preventDefault')
    act(() => {
      window.dispatchEvent(evenement)
    })
    expect(empecher).toHaveBeenCalled()
  })

  it('le bouton discret n apparait dans le menu « … » que si le navigateur accepte', async () => {
    render(<BandeauPortrait monde={undefined} menu={<button type="button">Menu PC</button>} />)
    fireEvent.click(screen.getByRole('button', { name: 'Menu' }))
    expect(screen.queryByRole('button', { name: /Installer l’application/ })).toBeNull()
    const { evenement, prompt } = demande()
    act(() => retenirDemandePourTest(evenement))
    fireEvent.click(screen.getByRole('button', { name: /Installer l’application/ }))
    await act(async () => {})
    expect(prompt).toHaveBeenCalledTimes(1)
    // Une demande ne sert qu'une fois : le bouton disparait.
    fireEvent.click(screen.getByRole('button', { name: 'Menu' }))
    expect(screen.queryByRole('button', { name: /Installer l’application/ })).toBeNull()
  })
})
