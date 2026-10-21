// InterrupteurFacon.test.tsx — le bouton « Auto / Manuel » de la barre du haut.
//
// Cas ajouté le 21/10/2026 : passer en manuel PENDANT qu'une question est
// ouverte (mulligan…) reproduisait un défaut où la reprise pouvait reposer
// la question sans que l'écran suive (voir
// .planning/todos/2026-10-07-manuel-100-pourcent-octgn.md). Plutôt que de
// corriger l'affichage après coup, le bouton « Manuel » se grise tant que
// `questionOuverte` est vrai.
import { fireEvent, render, screen } from '@testing-library/react'
import { describe, expect, it, vi } from 'vitest'
import { InterrupteurFacon } from './InterrupteurFacon'

function props(partiel: Partial<Parameters<typeof InterrupteurFacon>[0]> = {}) {
  return {
    manuel: false,
    commenceEnManuel: false,
    onManuel: vi.fn().mockResolvedValue(true),
    onReprendre: vi.fn().mockResolvedValue(true),
    onReprendreA: vi.fn().mockResolvedValue({ ok: true }),
    ...partiel,
  }
}

describe('InterrupteurFacon', () => {
  it('question ouverte : « Manuel » est grisé, le clic ne fait rien', () => {
    const onManuel = vi.fn().mockResolvedValue(true)
    render(<InterrupteurFacon {...props({ questionOuverte: true, onManuel })} />)
    const bouton = screen.getByRole('button', { name: 'Mode manuel' })
    expect(bouton).toBeDisabled()
    fireEvent.click(bouton)
    expect(onManuel).not.toHaveBeenCalled()
  })

  it('pas de question ouverte : « Manuel » reste cliquable', () => {
    const onManuel = vi.fn().mockResolvedValue(true)
    render(<InterrupteurFacon {...props({ questionOuverte: false, onManuel })} />)
    const bouton = screen.getByRole('button', { name: 'Mode manuel' })
    expect(bouton).not.toBeDisabled()
    fireEvent.click(bouton)
    expect(onManuel).toHaveBeenCalledTimes(1)
  })

  it('question ouverte mais déjà en manuel : « Auto » reste cliquable (la garde ne vise que le passage en manuel)', () => {
    const onReprendre = vi.fn().mockResolvedValue(true)
    render(<InterrupteurFacon {...props({ manuel: true, questionOuverte: true, onReprendre })} />)
    const bouton = screen.getByRole('button', { name: 'Mode automatique' })
    expect(bouton).not.toBeDisabled()
    fireEvent.click(bouton)
    expect(onReprendre).toHaveBeenCalledTimes(1)
  })
})
