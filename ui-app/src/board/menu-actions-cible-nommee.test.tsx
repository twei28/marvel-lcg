// Rapports n87 et n88 (Yarro, tablette, 16/10/2026) : toucher la cible NOMMÉE dans une
// action du menu la choisit directement. Avant, le toucher remontait à l'action, qui
// rouvrait la fenêtre « Choisir la cible » à 0/1.
import type { ComponentProps } from 'react'
import { cleanup, fireEvent, render } from '@testing-library/react'
import { afterEach, describe, expect, it, vi } from 'vitest'
import { MenuActionsCarte } from './MenuActionsCarte'

class ResizeObserverBouchon {
  observe() {}
  unobserve() {}
  disconnect() {}
}
;(globalThis as { ResizeObserver?: unknown }).ResizeObserver = ResizeObserverBouchon

afterEach(cleanup)

function monter(extra: Record<string, unknown> = {}) {
  const choisirOption = vi.fn()
  const option = {
    id: 7,
    bind_id: 0,
    bind_player_id: 1,
    name: 'Thwart',
    failure_reason: '',
    target_num_range: [1, 1],
    all_legal_targets: [10, 11],
    target_payment: {},
    is_search: false,
    ...extra,
  }
  const rendu = render(
    <MenuActionsCarte
      {...({
        carte: { id: '1', name: 'Rocket Raccoon', kind: 'hero' },
        options: [option],
        cartesParId: new Map(),
        catalogue: {},
        choisirOption,
        fermer: () => {},
        playerId: 1,
        idsAffiches: new Set([10, 11]),
        affichage: 'detailed',
      } as unknown as ComponentProps<typeof MenuActionsCarte>)}
    />
  )
  return { choisirOption, option, rendu }
}

describe('le menu des actions : une cible nommée se choisit d’un toucher', () => {
  it('toucher la cible envoie l’action AVEC cette cible, désignée par geste', () => {
    const { choisirOption, option, rendu } = monter()
    const puces = rendu.container.querySelectorAll('button.ma-cible')
    expect(puces).toHaveLength(2)
    fireEvent.click(puces[1]!)
    expect(choisirOption).toHaveBeenCalledTimes(1)
    expect(choisirOption).toHaveBeenCalledWith(option, [11], true)
  })

  it('toucher l’action elle-même garde la fenêtre de choix (aucune cible imposée)', () => {
    const { choisirOption, rendu } = monter()
    fireEvent.click(rendu.container.querySelector('.ma-action')!)
    expect(choisirOption).toHaveBeenCalledTimes(1)
    expect(choisirOption.mock.calls[0]![1]).toBeUndefined()
  })

  it('une action indisponible ne propose pas de cibles à toucher', () => {
    const { rendu } = monter({ failure_reason: 'Pas assez de ressources' })
    expect(rendu.container.querySelectorAll('button.ma-cible')).toHaveLength(0)
  })
})
