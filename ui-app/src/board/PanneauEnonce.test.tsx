// L'enonce d'un puzzle (E8) : introduction une seule fois, indices un par un, « Recommencer » en deux temps.
import { cleanup, fireEvent, render, screen } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { PanneauEnonce } from './PanneauEnonce'

const INFO = { title: 'Sauve Peter', description: 'Rhino arrive.', difficulty: 3, hints: ['Pense au Stun', 'Regarde la defausse'], author: 'Moi' }

describe('enonce du puzzle', () => {
  beforeEach(() => window.sessionStorage.clear())
  afterEach(cleanup)

  it('ne montre rien sans enonce', () => {
    const { container } = render(<PanneauEnonce info={{}} />)
    expect(container.firstChild).toBeNull()
    const sans = render(<PanneauEnonce />)
    expect(sans.container.firstChild).toBeNull()
  })

  it('ouvre l introduction : titre, etoiles, auteur, histoire, objectifs', () => {
    render(<PanneauEnonce info={INFO} objectifs={[{ kind: 'defeat_villain', text: '', target: '', done: false }]} />)
    const intro = screen.getByRole('dialog')
    expect(intro.textContent).toContain('Sauve Peter')
    expect(intro.textContent).toContain('★★★☆☆')
    expect(intro.textContent).toContain('Moi')
    expect(intro.textContent).toContain('Rhino arrive.')
    expect(intro.textContent).toContain('Vaincre le méchant')
  })

  it('Commencer ferme l introduction et elle ne revient pas apres un rechargement', () => {
    const premier = render(<PanneauEnonce info={INFO} />)
    fireEvent.click(screen.getByText('Commencer'))
    expect(screen.queryByRole('dialog')).toBeNull()
    premier.unmount()
    render(<PanneauEnonce info={INFO} />)
    expect(screen.queryByRole('dialog')).toBeNull()
  })

  it('les indices se devoilent un par un et restent devoiles apres rechargement', () => {
    window.sessionStorage.setItem(`mc-enonce-vu:${INFO.title}|${INFO.description}`, '1')
    const premier = render(<PanneauEnonce info={INFO} />)
    fireEvent.click(screen.getByText('Énoncé'))
    expect(screen.queryByText(/Pense au Stun/)).toBeNull()
    fireEvent.click(screen.getByText(/Indice suivant/))
    expect(screen.getByText(/Pense au Stun/)).toBeTruthy()
    expect(screen.queryByText(/Regarde la defausse/)).toBeNull()
    fireEvent.click(screen.getByText(/Indice suivant/))
    expect(screen.getByText(/Regarde la defausse/)).toBeTruthy()
    expect(screen.queryByText(/Indice suivant/)).toBeNull()
    premier.unmount()
    render(<PanneauEnonce info={INFO} />)
    fireEvent.click(screen.getByText('Énoncé'))
    expect(screen.getByText(/Regarde la defausse/)).toBeTruthy()
  })

  it('Recommencer demande confirmation avant d agir', () => {
    window.sessionStorage.setItem(`mc-enonce-vu:${INFO.title}|${INFO.description}`, '1')
    const recommencer = vi.fn()
    render(<PanneauEnonce info={INFO} recommencer={recommencer} />)
    fireEvent.click(screen.getByText('Énoncé'))
    fireEvent.click(screen.getByText('Recommencer'))
    expect(recommencer).not.toHaveBeenCalled()
    fireEvent.click(screen.getByText('Oui, recommencer'))
    expect(recommencer).toHaveBeenCalledTimes(1)
  })

  it('relire l introduction la rouvre', () => {
    window.sessionStorage.setItem(`mc-enonce-vu:${INFO.title}|${INFO.description}`, '1')
    render(<PanneauEnonce info={INFO} />)
    fireEvent.click(screen.getByText('Énoncé'))
    fireEvent.click(screen.getByText('Relire l’introduction'))
    expect(screen.getByRole('dialog')).toBeTruthy()
  })

  describe('solution de reference', () => {
    const AVEC = (visibilite: string) => ({ ...INFO, solution_text: 'Etourdis Rhino puis attaque.', solution_visibility: visibilite })
    const ouvrir = (info: typeof INFO & { solution_text?: string; solution_visibility?: string }, termine: boolean) => {
      window.sessionStorage.setItem(`mc-enonce-vu:${info.title}|${info.description}`, '1')
      render(<PanneauEnonce info={info} termine={termine} />)
      fireEvent.click(screen.getByText('Énoncé'))
    }

    it('« after » : cachee pendant la partie, visible une fois la partie finie', () => {
      ouvrir(AVEC('after'), false)
      expect(screen.queryByText('Voir la solution')).toBeNull()
      cleanup()
      ouvrir(AVEC('after'), true)
      fireEvent.click(screen.getByText('Voir la solution'))
      expect(screen.getByText(/Etourdis Rhino/)).toBeTruthy()
    })

    it('« always » : disponible tout de suite, mais derriere un clic', () => {
      ouvrir(AVEC('always'), false)
      expect(screen.queryByText(/Etourdis Rhino/)).toBeNull()
      fireEvent.click(screen.getByText('Voir la solution'))
      expect(screen.getByText(/Etourdis Rhino/)).toBeTruthy()
    })

    it('« never » : jamais, meme partie finie', () => {
      ouvrir(AVEC('never'), true)
      expect(screen.queryByText('Voir la solution')).toBeNull()
    })

    it('pas de solution ecrite : pas de bouton', () => {
      ouvrir({ ...INFO, solution_text: '', solution_visibility: 'always' }, true)
      expect(screen.queryByText('Voir la solution')).toBeNull()
    })
  })
})
