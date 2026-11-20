// Piocher au doigt (17/11/2026) : en mode manuel, le tiroir des piles du telephone propose « Piocher » sur le deck du joueur et
// « Sortir en résolution » sur le deck rencontre ; hors mode manuel, rien de tel.
import { describe, expect, it, vi } from 'vitest'
import { fireEvent, render, screen } from '@testing-library/react'
import { TiroirPiles } from './TiroirPiles'
import type { PileAffichee } from './bandes-portrait'

const pile = (cle: string, compte: number) =>
  ({ cle, titre: cle, compte, unite: { carte: { id: 1, name: 'x', pic_id: 'x' }, pileContenu: [] } }) as unknown as PileAffichee

const PILES = [pile('joueur-deck', 34), pile('joueur-defausse', 0), pile('rencontre-encounter-deck', 31)]

describe('le tiroir des piles : piocher au doigt', () => {
  it('propose Piocher sur le deck, Sortir en resolution sur le deck rencontre, et rien sur la defausse', () => {
    const onPiocher = vi.fn()
    render(<TiroirPiles piles={PILES} ouvert onFermer={() => {}} onOuvrirPile={() => {}} onPiocher={onPiocher} />)
    fireEvent.click(screen.getByRole('button', { name: 'Piocher' }))
    expect(onPiocher).toHaveBeenLastCalledWith('PlayerDeck', 1)
    fireEvent.click(screen.getByRole('button', { name: 'Sortir en résolution' }))
    expect(onPiocher).toHaveBeenLastCalledWith('EncounterDeck', 1)
    fireEvent.click(screen.getByRole('button', { name: 'Piocher plusieurs…' }))
    expect(onPiocher).toHaveBeenLastCalledWith('PlayerDeck')
    expect(screen.getAllByRole('button', { name: /^(Piocher|Sortir)/ })).toHaveLength(4)
  })

  it('hors mode manuel (pas de onPiocher), aucun bouton de pioche', () => {
    render(<TiroirPiles piles={PILES} ouvert onFermer={() => {}} onOuvrirPile={() => {}} />)
    expect(screen.queryByRole('button', { name: 'Piocher' })).toBeNull()
  })

  it('un deck vide ne propose pas de piocher', () => {
    render(<TiroirPiles piles={[pile('joueur-deck', 0)]} ouvert onFermer={() => {}} onOuvrirPile={() => {}} onPiocher={() => {}} />)
    expect(screen.queryByRole('button', { name: 'Piocher' })).toBeNull()
  })
})
