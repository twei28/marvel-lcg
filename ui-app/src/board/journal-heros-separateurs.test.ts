import { describe, expect, it } from 'vitest'
import { avecSeparateurs } from './JournalHeros'
import type { EntreeHistorique } from './HistoriquePartie'

const e = (cle: string, round: number, phase: string): EntreeHistorique =>
  ({ cle, round, phase, type: 'damage', titre: cle, renderId: 1 }) as EntreeHistorique

const lire = (lignes: ReturnType<typeof avecSeparateurs>) =>
  lignes.map((l) => (l.genre === 'round' ? `-- R${l.round}` : l.genre === 'phase' ? `== ${l.famille}` : `${l.famille ?? '?'} ${l.entree.cle}`))

describe('le journal du heros, separe par round et par phase', () => {
  it('une barre par round, un bandeau a chaque changement de phase', () => {
    expect(
      lire(avecSeparateurs([e('a', 1, 'Player 1 Turn'), e('b', 1, 'Enemy Activation'), e('c', 1, 'Enemy Activation'), e('d', 2, 'Player 1 Turn')]))
    ).toEqual(['-- R1', '== joueurs', 'joueurs a', '== mechant', 'mechant b', 'mechant c', '-- R2', '== joueurs', 'joueurs d'])
  })

  it('une phase inconnue garde la famille precedente, sans bandeau', () => {
    expect(lire(avecSeparateurs([e('a', 1, 'Player 1 Turn'), e('b', 1, 'End Round')]))).toEqual(['-- R1', '== joueurs', 'joueurs a', 'joueurs b'])
  })

  it('sans phase connue en debut de round, ni bandeau ni liseré', () => {
    expect(lire(avecSeparateurs([e('a', 3, '')]))).toEqual(['-- R3', '? a'])
  })

  it('rien a separer quand le journal est vide', () => {
    expect(avecSeparateurs([])).toEqual([])
  })
})
