import { describe, expect, it } from 'vitest'
import { lignesCompactes } from './journal-compact'
import type { EntreeHistorique } from './HistoriquePartie'

const e = (cle: string, round: number, type: EntreeHistorique['type'], titre: string, detail?: string): EntreeHistorique =>
  ({ cle, round, type, titre, detail, renderId: 1, phase: '' }) as EntreeHistorique

describe('le journal compact de la console', () => {
  it('garde les faits et une trace par phase, sans la narration technique ni les doublons', () => {
    const lignes = lignesCompactes([
      e('9', 2, 'phase', 'Round 2', 'Tour de Domino'),
      e('8', 2, 'text', 'Domino entre en jeu'),
      e('7', 2, 'phase', 'Round 2', 'Tour de Neena Thurman'),
      e('6', 2, 'phase', 'Round 2', 'Tour de Neena Thurman'),
      e('5', 2, 'text', 'Phase : Player'),
      e('4', 2, 'text', '=== Début du round 2 ==='),
      e('3', 2, 'phase', 'Round 2', 'Start Round'),
      e('2', 1, 'text', 'Fin du round 1'),
      e('1', 1, 'damage', 'Rhino attaque Domino', '3 dégâts'),
    ])
    expect(lignes.map((l) => (l.genre === 'round' ? `-- R${l.round}` : l.texte))).toEqual([
      '-- R2',
      'Tour de Domino',
      'Domino entre en jeu',
      'Tour de Neena Thurman',
      '-- R1',
      'Rhino attaque Domino',
    ])
  })

  it('un round sans fait affichable ne laisse pas de separateur', () => {
    const lignes = lignesCompactes([e('2', 3, 'text', '=== Début du round 3 ==='), e('1', 2, 'text', 'Domino entre en jeu')])
    expect(lignes.map((l) => l.genre)).toEqual(['round', 'fait'])
  })

  it('ecarte la plomberie des paquets du moteur', () => {
    const lignes = lignesCompactes([
      e('3', 1, 'text', 'EncounterDeck<31> va être mélangé avec EncounterDiscardPile<0>'),
      e('2', 1, 'text', 'AsideDeck<0> créé'),
      e('1', 1, 'text', 'Rhino révélée'),
    ])
    expect(lignes.filter((l) => l.genre === 'fait').map((l) => (l.genre === 'fait' ? l.texte : ''))).toEqual(['Rhino révélée'])
  })
})
