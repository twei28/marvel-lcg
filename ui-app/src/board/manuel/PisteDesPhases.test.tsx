import { fireEvent, render, screen } from '@testing-library/react'
import { readFileSync } from 'node:fs'
import { beforeEach, describe, expect, it } from 'vitest'
import { CLE_PISTE_PHASES, PisteDesPhases } from './PisteDesPhases'
import { ETAPES_MANUEL, etapeSuivante } from './phases-manuel'

beforeEach(() => window.sessionStorage.clear())

const courante = () => document.querySelector('[aria-current="step"]')?.textContent

describe('piste des phases (mode manuel)', () => {
  it('montre toujours toutes les étapes, la phase des héros en cours au départ', () => {
    render(<PisteDesPhases round={3} />)
    expect(screen.getByText('Round 3')).toBeTruthy()
    expect(screen.getByText('Phase du méchant')).toBeTruthy()
    for (const e of ETAPES_MANUEL) expect(screen.getByRole('button', { name: e.libelle })).toBeTruthy()
    expect(ETAPES_MANUEL.map((e) => e.libelle)).toEqual([
      'Phase des héros',
      '1. Menace',
      '2. Activation du méchant',
      '3. Activation des sbires',
      '4. Carte de rencontre',
      '5. Révélation',
      'Fin du round',
    ])
    expect(courante()).toBe('Phase des héros')
  })

  it('un clic place sur l’étape, « Étape suivante » avance, la fin du round ouvre le round suivant', () => {
    render(<PisteDesPhases round={1} />)
    fireEvent.click(screen.getByRole('button', { name: '3. Activation des sbires' }))
    expect(courante()).toBe('3. Activation des sbires')
    fireEvent.click(screen.getByRole('button', { name: /Étape suivante/ }))
    expect(courante()).toBe('4. Carte de rencontre')
    fireEvent.click(screen.getByRole('button', { name: 'Fin du round' }))
    fireEvent.click(screen.getByRole('button', { name: /Étape suivante/ }))
    expect(screen.getByText('Round 2')).toBeTruthy()
    expect(courante()).toBe('Phase des héros')
  })

  it('se souvient de l’étape et du round après un rechargement (sessionStorage)', () => {
    const { unmount } = render(<PisteDesPhases round={1} />)
    fireEvent.click(screen.getByRole('button', { name: '5. Révélation' }))
    unmount()
    expect(window.sessionStorage.getItem(CLE_PISTE_PHASES)).toBe(JSON.stringify({ round: 1, index: 5 }))
    render(<PisteDesPhases round={1} />)
    expect(courante()).toBe('5. Révélation')
  })

  it('transition pure : après la fin du round, round suivant et phase des héros', () => {
    expect(etapeSuivante({ round: 4, index: ETAPES_MANUEL.length - 1 })).toEqual({ round: 5, index: 0 })
  })

  it('téléphone : la piste défile sur UNE ligne, round et « Étape suivante » restent en vue (CSS)', () => {
    const css = readFileSync(`${process.cwd()}/src/board/manuel/PisteDesPhases.css`, 'utf8')
    const mobile = css.slice(css.indexOf('@media (max-width: 767px)'))
    expect(mobile).toContain('flex-wrap: nowrap')
    expect(mobile).toContain('overflow-x: auto')
    expect(mobile).toMatch(/\.piste-phases-suivant[^}]*position: sticky/s)
    expect(mobile).toMatch(/\.piste-phases-round,\s*\.piste-phases-suivant\s*\{[^}]*position: sticky/s)
    // jamais de pilule, ni de bord arrondi hors des ~4 px du reste du site
    expect(mobile).not.toMatch(/border-radius:\s*(9{3}|[5-9]\d|\d{3,})px/)
  })

  it('recentre l’étape courante quand la piste déborde (défilement du téléphone)', () => {
    const { container } = render(<PisteDesPhases round={1} />)
    const piste = container.querySelector('.piste-phases') as HTMLElement
    Object.defineProperty(piste, 'scrollWidth', { configurable: true, value: 900 })
    Object.defineProperty(piste, 'clientWidth', { configurable: true, value: 390 })
    const cible = screen.getByRole('button', { name: '4. Carte de rencontre' })
    Object.defineProperty(cible, 'offsetLeft', { configurable: true, value: 600 })
    Object.defineProperty(cible, 'offsetWidth', { configurable: true, value: 100 })
    fireEvent.click(cible)
    expect(piste.scrollLeft).toBe(600 - (390 - 100) / 2)
  })

  it('bureau : sans débordement, la piste ne défile jamais', () => {
    const { container } = render(<PisteDesPhases round={1} />)
    const piste = container.querySelector('.piste-phases') as HTMLElement
    Object.defineProperty(piste, 'scrollWidth', { configurable: true, value: 390 })
    Object.defineProperty(piste, 'clientWidth', { configurable: true, value: 390 })
    fireEvent.click(screen.getByRole('button', { name: '5. Révélation' }))
    expect(piste.scrollLeft).toBe(0)
  })
})
