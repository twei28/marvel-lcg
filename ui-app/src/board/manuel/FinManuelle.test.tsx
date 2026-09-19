// FinManuelle.test.tsx — déclarer la fin d'une partie manuelle (tâche 7).
//
// Le moteur ne surveille plus rien en mode manuel : personne d'autre que le
// joueur ne peut constater qu'un vilain est vaincu ou qu'un complot a
// débordé. Deux boutons qu'un clic malheureux déclencherait seraient une
// faute, parce que ce geste est le seul de tout le mode qui ne se rattrape
// pas (le Ctrl+Z annule un geste sur la table, pas une fin de partie) : il
// exige donc une confirmation, jamais un déclenchement au premier clic.
import { describe, expect, it, vi } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/react'
import { FinManuelle } from './FinManuelle'

describe('declarer la fin d une partie manuelle', () => {
  it('propose victoire et defaite', () => {
    render(<FinManuelle onDeclarer={() => {}} />)
    expect(screen.getByText('Victoire')).toBeTruthy()
    expect(screen.getByText('Défaite')).toBeTruthy()
  })

  it('previent avant de declarer', () => {
    const declarer = vi.fn()
    render(<FinManuelle onDeclarer={declarer} />)
    fireEvent.click(screen.getByText('Victoire'))
    expect(declarer).not.toHaveBeenCalled()
    fireEvent.click(screen.getByText('Confirmer'))
    expect(declarer).toHaveBeenCalledWith(true)
  })

  it('declare une defaite, distincte de la victoire', () => {
    const declarer = vi.fn()
    render(<FinManuelle onDeclarer={declarer} />)
    fireEvent.click(screen.getByText('Défaite'))
    fireEvent.click(screen.getByText('Confirmer'))
    expect(declarer).toHaveBeenCalledWith(false)
  })

  it('annuler revient au choix, sans jamais avoir declare', () => {
    const declarer = vi.fn()
    render(<FinManuelle onDeclarer={declarer} />)
    fireEvent.click(screen.getByText('Victoire'))
    fireEvent.click(screen.getByText('Annuler'))
    expect(declarer).not.toHaveBeenCalled()
    // Le choix revient : les deux boutons initiaux sont de nouveau proposés.
    expect(screen.getByText('Victoire')).toBeTruthy()
    expect(screen.getByText('Défaite')).toBeTruthy()
    expect(screen.queryByText('Confirmer')).toBeNull()
  })

  it('un rappel dit que la decision est definitive, pendant la confirmation', () => {
    render(<FinManuelle onDeclarer={() => {}} />)
    fireEvent.click(screen.getByText('Défaite'))
    expect(screen.getByText(/ne se reprend pas/)).toBeTruthy()
  })
})
