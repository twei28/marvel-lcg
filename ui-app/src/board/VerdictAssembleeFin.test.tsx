// Le verdict de l'assemblée sur l'écran de fin : rien hors assemblée, l'attente tant qu'un groupe joue, puis le verdict.
import { render, screen } from '@testing-library/react'
import { describe, expect, it, vi } from 'vitest'
import { VerdictAssembleeFin } from './VerdictAssembleeFin'
import type { World } from './world'

vi.mock('./sources', () => ({ chargerAssemblee: () => new Promise(() => {}) }))

const monde = (plus: Record<string, unknown> | null) =>
  ({ assemblee: plus === null ? {} : {
    code: 'KING-7F3A', table: 'p1', organisateur: 'p1', total_jetons: 5, seuil: 12, retournee: false, degats: 2, menace: 1, joueurs: 4,
    groupes: [
      { tab: 'p1', joueurs: 2, noms: 'A', etat: 1, recus: 0 },
      { tab: 'p2', joueurs: 2, noms: 'B', etat: 0, recus: 0 },
    ],
    terminee: false, gagnee: false, ...plus,
  } }) as unknown as World

describe('VerdictAssembleeFin', () => {
  it('hors assemblée : rien', () => {
    const { container } = render(<VerdictAssembleeFin monde={monde(null)} siege={0} />)
    expect(container.textContent).toBe('')
  })
  it('un groupe joue encore : on attend', () => {
    render(<VerdictAssembleeFin monde={monde({})} siege={0} />)
    expect(screen.getByRole('status').textContent).toMatch(/attend les autres groupes/)
    expect(screen.getByRole('status').textContent).toMatch(/Un groupe joue encore/)
  })
  it('toutes les tables finies : le verdict', () => {
    const { rerender } = render(<VerdictAssembleeFin monde={monde({ terminee: true, gagnee: true })} siege={0} />)
    expect(screen.getByRole('status').textContent).toMatch(/gagne/)
    rerender(<VerdictAssembleeFin monde={monde({ terminee: true, gagnee: false })} siege={0} />)
    expect(screen.getByRole('status').textContent).toMatch(/perd/)
  })
})
