// Aspects TMNT « Dual-Aspect » (pack tmnt_aspect_dual, prefixe ud, Inkwire) : ce que le plateau
// DESSINE. PROCESSUS-CARTE etape 8 bis, pour les cartes qui changent ce qu'on VOIT :
//  - ud003 Heavy Metal entre en jeu avec 2 compteurs « amp » (affiches « ampli »), en perd un
//    a chaque Reponse ;
//  - le cadre d'une carte double aspect (« Aggression;Justice ») : sous un effet delavant, le
//    lisere prend le PREMIER aspect imprime (aspectDeClasse), faute de lisere bicolore.
// Les etats Cloaked / Tough poses par ud001, ud004, ud005, ud006 sont des cartes d'etat deja
// dessinees par le plateau (cas cloaked / toughness des packs TMNT) : rien de neuf ici.
import { describe, expect, it } from 'vitest'
import { aspectDeClasse, catalogueVide } from './catalogue'
import { toScanCard } from './card-model'
import { carteSurTable, dessinee, siege, tableAvec } from './plateau-de-test'
import type { WorldCard } from './world'

const HEROS = 1
const HEAVY_METAL = 40

const heavyMetal = (amp: number): WorldCard =>
  carteSurTable(HEAVY_METAL, 'ud003', 'Ally', 'Heavy Metal', {
    info: { max_health: 2, health: 2, ...(amp ? { c_amp: amp } : {}) },
  })

const monde = (amp: number) =>
  tableAvec(siege({
    area_hero: [carteSurTable(HEROS, '01001a', 'Hero', 'Spider-Man')],
    allies: [heavyMetal(amp)],
  }))

const scan = (carte: WorldCard) => toScanCard(carte, { playerId: 0, actives: new Set<number>(), catalogue: catalogueVide })

describe('ud003 Heavy Metal : compteurs amp', () => {
  it('est dessinee avec ses 2 compteurs amp', () => {
    const vue = dessinee(monde(2), HEAVY_METAL)
    expect(vue).toBeDefined()
    expect(vue?.compteurs['amp']).toBe(2)
  })

  it('le compteur porte un nom francais (« ampli »)', () => {
    const etiquette = scan(heavyMetal(1)).counters?.find((c) => c.cle === 'amp')?.label
    expect(etiquette?.toLowerCase()).toContain('ampli')
  })

  it('sans compteur, aucun compteur amp dessine (temoin)', () => {
    expect(scan(heavyMetal(0)).counters?.find((c) => c.cle === 'amp')).toBeUndefined()
  })
})

describe('cadre d une carte double aspect', () => {
  it('lisere du premier aspect imprime, jamais « inconnu »', () => {
    expect(aspectDeClasse('Aggression;Justice')).toBe('aggression')
    expect(aspectDeClasse('Justice;Leadership')).toBe('justice')
    expect(aspectDeClasse('Leadership;Protection')).toBe('leadership')
  })
})
