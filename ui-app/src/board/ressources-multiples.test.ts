// Payer avec PLUSIEURS jetons d'une même carte (30/10/2026).
//
// Cas réel : Raphael peut dépenser chacun de ses jetons Rage comme une ressource physique. Le moteur propose alors le
// MÊME effet autant de fois qu'il a de jetons (3 jetons = 3 moyens de paiement identiques). Headbutt coûte 2 : le premier
// toucher payait un jeton, le second le RENDAIT au lieu d'en payer un deuxième.
import { describe, expect, it } from 'vitest'
import { ressourcesApresToucher } from './ask'
import type { Paiement } from './ask'

const RAGE = 7
const MAIN = 9

/** Raphael a `jetons` jetons Rage : l'effet 7 est proposé `jetons` fois. */
function paiement(cout: string, jetons: number, avecMain = false): Paiement {
  const moyens = Array.from({ length: jetons }, () => ({ effect_id: RAGE, res_text: 'R' }))
  if (avecMain) moyens.push({ effect_id: MAIN, res_text: 'R' })
  return { cost: cout, payment: moyens, rule: [] }
}

describe('une carte qui peut payer plusieurs fois (jetons Rage)', () => {
  it('chaque toucher en ajoute un, jusqu’à ce que le coût soit couvert', () => {
    const p = paiement('RR', 3)
    const un = ressourcesApresToucher([RAGE], [], p, 2, false)
    expect(un).toEqual([RAGE])
    const deux = ressourcesApresToucher([RAGE], un, p, 2, false)
    expect(deux).toEqual([RAGE, RAGE])
  })

  it('le toucher suivant, coût couvert, rend tous les jetons (retour à zéro)', () => {
    const p = paiement('RR', 3)
    expect(ressourcesApresToucher([RAGE], [RAGE, RAGE], p, 2, false)).toEqual([])
  })

  it('on ne prend jamais plus que ce qu’il reste de jetons', () => {
    const p = paiement('RRRR', 2)
    const deux = [RAGE, RAGE]
    // Il manque encore de quoi payer, mais plus de jeton : on rend ceux déjà posés.
    expect(ressourcesApresToucher([RAGE], deux, p, 4, false)).toEqual([])
  })

  it('un coût déjà couvert par une autre carte : aucun jeton de plus', () => {
    const p = paiement('R', 3, true)
    // La carte de la main (effet 9) paie déjà le R : toucher Raphael n'ajoute rien.
    expect(ressourcesApresToucher([RAGE], [MAIN], p, 1, false)).toEqual([MAIN])
  })

  it('coût surpayable (Ant-Man) : on peut aller jusqu’au dernier jeton', () => {
    const p = paiement('R', 3)
    const un = ressourcesApresToucher([RAGE], [RAGE], p, 1, true)
    expect(un).toEqual([RAGE, RAGE])
  })

  it('ne touche pas aux ressources des AUTRES cartes quand elle se vide', () => {
    const p = paiement('RR', 3, true)
    expect(ressourcesApresToucher([RAGE], [MAIN, RAGE], p, 2, false)).toEqual([MAIN])
  })
})

describe('une carte qui ne paie qu’une fois (le cas ordinaire)', () => {
  const p: Paiement = { cost: '1', payment: [{ effect_id: MAIN, res_text: 'R' }], rule: [] }

  it('un toucher paie', () => {
    expect(ressourcesApresToucher([MAIN], [], p, 1, false)).toEqual([MAIN])
  })

  it('un second toucher retire (comportement d’avant, inchangé)', () => {
    expect(ressourcesApresToucher([MAIN], [MAIN], p, 1, false)).toEqual([])
  })

  it('une carte qui ne peut pas payer ne change rien', () => {
    expect(ressourcesApresToucher([42], [MAIN], p, 1, false)).toEqual([MAIN])
  })
})
