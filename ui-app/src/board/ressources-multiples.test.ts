// Payer avec PLUSIEURS jetons d'une même carte (30/10/2026).
//
// Cas réel : Raphael peut dépenser chacun de ses jetons Rage comme une ressource physique. Le moteur propose alors le
// MÊME effet autant de fois qu'il a de jetons (3 jetons = 3 moyens de paiement identiques). Headbutt coûte 2 : le premier
// toucher payait un jeton, le second le RENDAIT au lieu d'en payer un deuxième.
import { describe, expect, it } from 'vitest'
import { ressourcesApresToucher } from './ask'
import { moyensChoisisDesAlternatives } from './interaction'
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

// Mantis (01/11/2026) : Empathetic Advantage offre DEUX moyens ALTERNATIFS sur la meme carte : un ennemi desoriente donne
// [wild][mental] (effet 1), un personnage de Mantis [mental] (effet 2). Chaque moyen est propose UNE fois.
describe('des moyens alternatifs d’une même carte (Empathetic Advantage)', () => {
  const ENNEMI = 1
  const PERSO = 2
  const p = (cout: string): Paiement => ({
    cost: cout,
    payment: [{ effect_id: ENNEMI, res_text: 'BG' }, { effect_id: PERSO, res_text: 'B' }],
    rule: [],
  })

  it('cout 1 : le premier toucher pose la source ennemie, le second passe a la source personnage, le troisieme rend tout', () => {
    const un = ressourcesApresToucher([ENNEMI, PERSO], [], p('B'), 1, false)
    expect(un).toEqual([ENNEMI])
    const deux = ressourcesApresToucher([ENNEMI, PERSO], un, p('B'), 1, false)
    expect(deux).toEqual([PERSO])
    expect(ressourcesApresToucher([ENNEMI, PERSO], deux, p('B'), 1, false)).toEqual([])
  })

  it('cout 2 : la source personnage ne couvre pas, le second toucher rend la ressource (comportement d’avant)', () => {
    const un = ressourcesApresToucher([ENNEMI, PERSO], [], p('BB'), 2, false)
    expect(un).toEqual([ENNEMI])
    expect(ressourcesApresToucher([ENNEMI, PERSO], un, p('BB'), 2, false)).toEqual([])
  })

  it('ne touche pas aux ressources des autres cartes en passant d’un moyen a l’autre', () => {
    const autre = 9
    const avec: Paiement = { cost: 'B', payment: [...p('B').payment, { effect_id: autre, res_text: 'B' }], rule: [] }
    expect(ressourcesApresToucher([ENNEMI, PERSO], [autre, ENNEMI], avec, 1, false)).toEqual([autre, PERSO])
  })

  it('un seul moyen offert (un seul statut a defausser) : toucher paie, retoucher rend', () => {
    const seul: Paiement = { cost: 'B', payment: [{ effect_id: PERSO, res_text: 'B' }], rule: [] }
    const un = ressourcesApresToucher([PERSO], [], seul, 1, false)
    expect(un).toEqual([PERSO])
    expect(ressourcesApresToucher([PERSO], un, seul, 1, false)).toEqual([])
  })
})

describe('moyensChoisisDesAlternatives : dire quel moyen est posé', () => {
  const mantis = { name: 'Mantis', resources: [1, 2] } as unknown as import('./world').WorldCard
  const autre = { name: 'Genius', resources: [9] } as unknown as import('./world').WorldCard
  const p: Paiement = {
    cost: 'B',
    payment: [{ effect_id: 1, res_text: 'BG' }, { effect_id: 2, res_text: 'B' }, { effect_id: 9, res_text: 'B' }],
    rule: [],
  }
  it('nomme le moyen posé quand la carte en offre plusieurs', () => {
    expect(moyensChoisisDesAlternatives(p, [1], [mantis, autre])).toBe('Mantis : mental + joker')
    expect(moyensChoisisDesAlternatives(p, [2], [mantis, autre])).toBe('Mantis : mental')
  })
  it('ne dit rien pour une carte ordinaire ni sans ressource posée', () => {
    expect(moyensChoisisDesAlternatives(p, [9], [mantis, autre])).toBeUndefined()
    expect(moyensChoisisDesAlternatives(p, [], [mantis, autre])).toBeUndefined()
  })
})
