// BandeauPause.test.tsx — le bandeau de pause manuelle EN COURS DE PARTIE
// (tâche 3). Quatre comportements, donnés par le brief :
//   1. ne s'affiche pas hors pause
//   2. s'affiche en pause
//   3. nomme qui a mis en pause (ou « quelqu'un » à défaut)
//   4. appelle `onReprendre`
import { describe, expect, it, vi } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/react'
import { BandeauPause } from './BandeauPause'

describe('le bandeau de pause', () => {
  it('ne s\'affiche pas hors pause', () => {
    const { container } = render(
      <BandeauPause
        enPause={{ actif: false, par: '', depuis: '' }}
        onReprendre={() => {}}
        onPasser={() => {}}
      />
    )
    expect(container.querySelector('.bandeau-pause')).toBeNull()
  })

  it('s\'affiche en pause', () => {
    const { container } = render(
      <BandeauPause
        enPause={{ actif: true, par: '', depuis: '' }}
        onReprendre={() => {}}
        onPasser={() => {}}
      />
    )
    expect(container.querySelector('.bandeau-pause')).not.toBeNull()
  })

  it('nomme qui a mis en pause', () => {
    render(
      <BandeauPause
        enPause={{ actif: true, par: 'Nick Fury', depuis: '2026-09-20 14-30' }}
        onReprendre={() => {}}
        onPasser={() => {}}
      />
    )
    expect(screen.getByText(/Nick Fury/)).toBeTruthy()
  })

  it('dit « quelqu\'un » quand aucun pseudo n\'a voyagé', () => {
    render(
      <BandeauPause
        enPause={{ actif: true, par: '', depuis: '' }}
        onReprendre={() => {}}
        onPasser={() => {}}
      />
    )
    expect(screen.getByText(/Quelqu.un/)).toBeTruthy()
  })

  it('appelle onReprendre au clic sur Reprendre', () => {
    const reprendre = vi.fn()
    render(
      <BandeauPause
        enPause={{ actif: true, par: '', depuis: '' }}
        onReprendre={reprendre}
        onPasser={() => {}}
      />
    )
    fireEvent.click(screen.getByText('Reprendre'))
    expect(reprendre).toHaveBeenCalled()
  })
})
