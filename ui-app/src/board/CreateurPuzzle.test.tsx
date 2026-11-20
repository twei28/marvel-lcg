// Le panneau « Creation de puzzle » : invisible hors du mode, capture puis fenetre de details, refus clairs, publication.
import { cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { CreateurPuzzle } from './CreateurPuzzle'

const CAPTURE = { puzzle: { format: 2, players: [{}, {}] }, avertissements: ['joueur 0 : ressources en reserve non capturees'] }

describe('CreateurPuzzle', () => {
  beforeEach(() => window.localStorage.clear())
  afterEach(cleanup)

  it('ne montre rien hors du mode Puzzle', () => {
    const { container } = render(<CreateurPuzzle actif={false} />)
    expect(container.firstChild).toBeNull()
  })

  it('« Enregistrer le puzzle » capture le plateau et ouvre la fenetre, avertissements compris', async () => {
    const capturer = vi.fn().mockResolvedValue(CAPTURE)
    render(<CreateurPuzzle actif capturer={capturer} />)
    fireEvent.click(screen.getByRole('button', { name: 'Enregistrer le puzzle' }))
    const fenetre = await screen.findByRole('dialog')
    expect(capturer).toHaveBeenCalledTimes(1)
    expect(fenetre.textContent).toContain('ressources en reserve non capturees')
  })

  it('une capture refusee affiche la raison sans ouvrir la fenetre', async () => {
    render(<CreateurPuzzle actif capturer={vi.fn().mockRejectedValue(new Error('Le moteur a refusé la capture du plateau.'))} />)
    fireEvent.click(screen.getByRole('button', { name: 'Enregistrer le puzzle' }))
    expect((await screen.findByRole('alert')).textContent).toContain('refusé la capture')
    expect(screen.queryByRole('dialog')).toBeNull()
  })

  it('refuse de publier sans titre, puis publie avec le titre et montre le code', async () => {
    const publier = vi.fn().mockResolvedValue({ code: 'PZ-ABCD', cle: 'cle-secrete' })
    render(<CreateurPuzzle actif capturer={vi.fn().mockResolvedValue(CAPTURE)} publier={publier} />)
    fireEvent.click(screen.getByRole('button', { name: 'Enregistrer le puzzle' }))
    await screen.findByRole('dialog')
    fireEvent.click(screen.getByRole('button', { name: 'Publier le puzzle' }))
    expect(publier).not.toHaveBeenCalled()
    expect(screen.getByRole('alert').textContent).toContain('titre')
    fireEvent.change(screen.getByLabelText('Titre'), { target: { value: 'Sauve Peter' } })
    fireEvent.click(screen.getByRole('button', { name: 'Publier le puzzle' }))
    await waitFor(() => expect(publier).toHaveBeenCalledTimes(1))
    expect(publier.mock.calls[0][0]).toMatchObject({ format: 2, title: 'Sauve Peter' })
    expect((await screen.findByRole('dialog')).textContent).toContain('PZ-ABCD')
    expect(JSON.parse(window.localStorage.getItem('mc-puzzles-crees') ?? '[]')[0].code).toBe('PZ-ABCD')
  })

  it('le bouton est grise tant que la mise en place n\'est pas finie', () => {
    render(<CreateurPuzzle actif pret={false} />)
    expect((screen.getByRole('button', { name: 'Enregistrer le puzzle' }) as HTMLButtonElement).disabled).toBe(true)
  })

  it('le choix du premier joueur n\'apparait qu\'avec plusieurs heros', async () => {
    const un = render(<CreateurPuzzle actif nomsDesJoueurs={['Spider-Man']} capturer={vi.fn().mockResolvedValue(CAPTURE)} />)
    fireEvent.click(screen.getByRole('button', { name: 'Enregistrer le puzzle' }))
    await screen.findByRole('dialog')
    expect(screen.queryByLabelText('Premier joueur')).toBeNull()
    un.unmount()
    render(<CreateurPuzzle actif nomsDesJoueurs={['Spider-Man', 'Iron Man']} capturer={vi.fn().mockResolvedValue(CAPTURE)} />)
    fireEvent.click(screen.getByRole('button', { name: 'Enregistrer le puzzle' }))
    await screen.findByRole('dialog')
    expect(screen.getByLabelText('Premier joueur')).toBeTruthy()
  })
})
