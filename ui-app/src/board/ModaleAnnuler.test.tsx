// Ce que ces cas protègent : le joueur sait ce que fait « Annuler » AVANT de
// l'envoyer au moteur, et la case « ne plus me montrer ça » ne ment pas.
//
// Le piège : la case est un renseignement sur la FENÊTRE, pas sur le choix.
// Cochée puis « Garder mon coup », elle doit quand même être mémorisée, et
// jamais envoyer `/undo` sans que le joueur l'ait demandé.
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { act, render, screen } from '@testing-library/react'
import { ModaleAnnuler } from './ModaleAnnuler'
import { CLE_ANNULER_EXPLIQUE, lireAnnulerExplique } from './moteur'

function poser() {
  const onConfirmer = vi.fn()
  const onFermer = vi.fn()
  render(<ModaleAnnuler onConfirmer={onConfirmer} onFermer={onFermer} />)
  return { onConfirmer, onFermer }
}

const cliquer = async (nom: string) => {
  await act(async () => {
    screen.getByRole('button', { name: nom }).click()
  })
}

describe('ModaleAnnuler', () => {
  beforeEach(() => window.localStorage.clear())
  afterEach(() => window.localStorage.clear())

  it('explique avant d’agir, et n’annule rien tant qu’on n’a pas répondu', () => {
    const { onConfirmer, onFermer } = poser()
    expect(screen.getByRole('alertdialog')).toBeInTheDocument()
    expect(screen.getByText(/instantané/i)).toBeInTheDocument()
    expect(onConfirmer).not.toHaveBeenCalled()
    expect(onFermer).not.toHaveBeenCalled()
  })

  it('« Oui, annuler » confirme, sans rien mémoriser si la case reste vide', async () => {
    const { onConfirmer, onFermer } = poser()
    await cliquer('Oui, annuler')
    expect(onConfirmer).toHaveBeenCalledTimes(1)
    expect(onFermer).not.toHaveBeenCalled()
    expect(lireAnnulerExplique()).toBe(false)
  })

  it('« Garder mon coup » ferme sans annuler', async () => {
    const { onConfirmer, onFermer } = poser()
    await cliquer('Garder mon coup')
    expect(onFermer).toHaveBeenCalledTimes(1)
    expect(onConfirmer).not.toHaveBeenCalled()
  })

  it('la case cochée mémorise le réglage, même avec « Garder mon coup »', async () => {
    const { onConfirmer } = poser()
    await act(async () => {
      screen.getByRole('checkbox').click()
    })
    await cliquer('Garder mon coup')
    expect(window.localStorage.getItem(CLE_ANNULER_EXPLIQUE)).toBe('1')
    expect(lireAnnulerExplique()).toBe(true)
    expect(onConfirmer).not.toHaveBeenCalled()
  })

  it('la case cochée puis « Oui, annuler » mémorise ET annule', async () => {
    const { onConfirmer } = poser()
    await act(async () => {
      screen.getByRole('checkbox').click()
    })
    await cliquer('Oui, annuler')
    expect(lireAnnulerExplique()).toBe(true)
    expect(onConfirmer).toHaveBeenCalledTimes(1)
  })

  it('Échap ferme sans annuler', async () => {
    const { onConfirmer, onFermer } = poser()
    await act(async () => {
      window.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape', bubbles: true }))
    })
    expect(onFermer).toHaveBeenCalledTimes(1)
    expect(onConfirmer).not.toHaveBeenCalled()
  })
})
