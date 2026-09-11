// Le jargon du moteur ne doit jamais atteindre l'ecran.
//
// Capture de l'utilisateur (11/09/2026), dans le panneau de decision :
//   « Klaw va comploter (+0) ((^!142) Advance (When Revealed) [01186]
//     WhenCardRevealed) »
// Le champ `by_effect` du moteur deverse ses identifiants internes : la
// reference d'une capacite (^!142), le code de la carte [01186], et le nom
// d'evenement CamelCase qui repete deja ce que dit « (When Revealed) ».
//
// `sansIdentifiants` ne connaissait que la forme « [(50,01113) Klaw] ».

import { describe, expect, it } from 'vitest'
import { nettoyerNarration, sansIdentifiants } from './BarreAction'

const propre = (texte: string) => nettoyerNarration(sansIdentifiants(texte))

describe('nettoyerNarration, le jargon de by_effect', () => {
  it('retire la reference de capacite, le code de carte et le nom d’evenement', () => {
    expect(
      propre('Klaw will scheme (+0) ((^!142) Advance (When Revealed) [01186] WhenCardRevealed)')
    ).toBe('Klaw will scheme (+0) (Advance (When Revealed))')
  })

  it('retire aussi ces formes isolees', () => {
    expect(propre('Rhino attacks (^!7)')).toBe('Rhino attacks')
    expect(propre('Zola revealed [01186]')).toBe('Zola revealed')
    expect(propre('Une riposte AfterAttackResolved')).toBe('Une riposte')
  })

  it('ne touche pas au nom d’une carte, ni aux jetons de ressource', () => {
    expect(propre('[(50,01113) Klaw] attaque')).toBe('Klaw attaque')
    expect(propre('Defense Network est en jeu')).toBe('Defense Network est en jeu')
    // Un mot CamelCase qui n'est pas un evenement moteur reste intact.
    expect(propre('Spider-Man joue Backflip')).toBe('Spider-Man joue Backflip')
  })

  it('ne laisse pas de parenthese vide quand il ne reste rien dedans', () => {
    expect(propre('Klaw va comploter (+0) ((^!142) [01186] WhenCardRevealed)')).toBe(
      'Klaw va comploter (+0)'
    )
  })
})
