// Le tirage manuel (rapport 131) : le plateau reconnaît les options « dos à tirer » du moteur, mélange une seconde,
// puis laisse choisir une carte sans jamais afficher de nom.
import { act, fireEvent, render, screen } from '@testing-library/react'
import { afterEach, describe, expect, it, vi } from 'vitest'
import type { Option } from './ask'
import { SelecteurTirageCache } from './SelecteurTirageCache'
import { DUREE_MELANGE_MS, estTirageCache, PREFIXE_TIRAGE_CACHE } from './tirage-cache'

const opt = (id: number, rang: number): Option => ({ id, name: `${PREFIXE_TIRAGE_CACHE}${rang}` }) as Option

describe('estTirageCache', () => {
  it('reconnaît des options portant le préfixe moteur', () => {
    expect(estTirageCache([opt(1, 1), opt(2, 2)])).toBe(true)
  })
  it('refuse une option seule, un nom de carte ou un mélange', () => {
    expect(estTirageCache([opt(1, 1)])).toBe(false)
    expect(estTirageCache([{ name: 'Moon Knight' }, { name: 'Black Cat' }])).toBe(false)
    expect(estTirageCache([opt(1, 1), { name: 'Moon Knight' }])).toBe(false)
  })
})

describe('SelecteurTirageCache', () => {
  afterEach(() => vi.useRealTimers())

  it("ne laisse rien valider pendant la seconde de mélange, puis permet de choisir", () => {
    vi.useFakeTimers()
    const choisir = vi.fn()
    const { container } = render(<SelecteurTirageCache titre="Tire" options={[opt(7, 1), opt(8, 2), opt(9, 3)]} choisir={choisir} />)
    const cartes = container.querySelector('.tirage-cache-cartes')!
    expect(cartes.getAttribute('data-melange')).toBe('oui')
    expect((screen.getByText('Valider') as HTMLButtonElement).disabled).toBe(true)
    act(() => {
      vi.advanceTimersByTime(DUREE_MELANGE_MS)
    })
    expect(cartes.getAttribute('data-melange')).toBe('non')
    const cases = container.querySelectorAll('.tirage-cache-case .est-agissante')
    expect(cases.length).toBe(3)
    fireEvent.click(cases[1])
    fireEvent.click(screen.getByText('Valider'))
    expect(choisir).toHaveBeenCalledTimes(1)
    expect(choisir.mock.calls[0][0].id).toBe(8)
  })

  it("n'affiche aucun nom de carte (ni le préfixe moteur)", () => {
    const { container } = render(<SelecteurTirageCache titre="Tire" options={[opt(7, 1), opt(8, 2)]} choisir={() => {}} dureeMelangeMs={0} />)
    expect(container.textContent).not.toContain('tirage-cache')
  })
})
