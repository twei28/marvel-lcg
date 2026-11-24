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

  it('téléphone : rien n’est rendu (`?mobile` force le plateau téléphone)', () => {
    window.history.pushState({}, '', '/?mobile')
    try {
      const { container } = render(<PisteDesPhases round={1} />)
      expect(container.querySelector('.piste-phases')).toBeNull()
      expect(screen.queryByText('Round 1')).toBeNull()
    } finally {
      window.history.pushState({}, '', '/')
    }
  })

  it('témoin : sur bureau la piste est rendue', () => {
    const { container } = render(<PisteDesPhases round={1} />)
    expect(container.querySelector('.piste-phases')).not.toBeNull()
    expect(screen.getByText('Round 1')).toBeTruthy()
  })

  it('le CSS ne garde plus aucune règle téléphone (pas de défilement, pas de pilule)', () => {
    const css = readFileSync(`${process.cwd()}/src/board/manuel/PisteDesPhases.css`, 'utf8')
    expect(css).not.toContain('@media (max-width: 767px)')
    expect(css).not.toMatch(/border-radius:\s*(9{3}|[5-9]\d|\d{3,})px/)
  })
})
