// FinManuelle.test.tsx — déclarer la fin d'une partie manuelle (tâche 7).
//
// Le moteur ne surveille plus rien en mode manuel : personne d'autre que le
// joueur ne peut constater qu'un vilain est vaincu ou qu'un complot a
// débordé.
//
// ⚠ CORRECTION (ronde 1) : ce geste SE RATTRAPE (le Ctrl+Z rejoue la partie
// moins la fin déclarée — voir `CoucheTriche.test.tsx`, describe « le
// Ctrl+Z défait aussi une fin de partie déclarée »). La confirmation ne
// protège donc pas d'un geste irréversible ; elle évite seulement de
// déclencher par mégarde le rejeu complet (une à deux secondes) qui permet
// d'y revenir.
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

  it('un rappel dit, pendant la confirmation, qu’on peut revenir en arrière avec Ctrl+Z', () => {
    render(<FinManuelle onDeclarer={() => {}} />)
    fireEvent.click(screen.getByText('Défaite'))
    expect(screen.getByText(/Ctrl\+Z/)).toBeTruthy()
  })
})
