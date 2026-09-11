// Traduire le « par quel effet » sans jamais toucher a un nom de carte.
//
// Le moteur finit ses narrations par la capacite responsable :
//   « Klaw va comploter (+0) (Advance (When Revealed)) »
// Ces deux morceaux sont du vocabulaire moteur, mais un remplacement par
// SOUS-CHAINE les traduirait partout : mesure du 11/09/2026 sur cards.json,
// 28 cartes contiennent le mot « Attack » (« Massive Attack »), 20 le mot
// « Defense », et trois cartes s'appellent exactement Advance, Surge et
// Teamwork. On ne traduit donc qu'un SEGMENT ENTIER d'une parenthese, jamais
// un mot au milieu d'un nom.

import { describe, expect, it, vi } from 'vitest'
import { traduireEffets } from './vocabulaire-moteur'

vi.mock('./langue', async () => {
  const vrai = await vi.importActual<typeof import('./langue')>('./langue')
  return { ...vrai, langueActuelle: () => 'fr' }
})

describe('traduireEffets', () => {
  it('traduit la capacite et sa fenetre de declenchement', () => {
    expect(traduireEffets('Klaw will scheme (+0) (Advance (When Revealed))')).toBe(
      'Klaw will scheme (+0) (Avancer (Quand révélée))'
    )
  })

  it('traduit une parenthese qui ne porte que la fenetre', () => {
    expect(traduireEffets('Zola agit (When Revealed)')).toBe('Zola agit (Quand révélée)')
  })

  it('LAISSE INTACT un nom de carte entre parentheses', () => {
    // Aucun de ces libelles n'est une entree du dictionnaire.
    expect(traduireEffets('Spider-Man joue (Massive Attack)')).toBe('Spider-Man joue (Massive Attack)')
    expect(traduireEffets('Riposte (Rapid Response)')).toBe('Riposte (Rapid Response)')
    expect(traduireEffets('Effet (Improved Defense Upgrade)')).toBe('Effet (Improved Defense Upgrade)')
  })

  it('ne touche pas aux parentheses qui ne sont pas du vocabulaire', () => {
    expect(traduireEffets('Klaw va comploter (+0)')).toBe('Klaw va comploter (+0)')
    expect(traduireEffets('Deux cartes (2)')).toBe('Deux cartes (2)')
  })

  it('traduit le nom de carte imbrique seulement si la fenetre est connue', () => {
    // « Massive Attack (When Revealed) » : la carte garde son nom, la fenetre
    // se traduit. C'est exactement ce qu'on veut sur une carte fan-made.
    expect(traduireEffets('X (Massive Attack (When Revealed))')).toBe(
      'X (Massive Attack (Quand révélée))'
    )
  })
})
