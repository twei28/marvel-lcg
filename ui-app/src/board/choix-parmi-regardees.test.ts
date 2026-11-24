// Rapport nicodede62 (18/11/2026), « Futuriste » de Tony Stark : trois fenêtres pour un seul choix parmi 3 cartes regardées.
import { afterEach, describe, expect, it } from 'vitest'
import type { Option } from './ask'
import { ciblesDejaRegardees, optionACiblesSeule, optionParmiRegardees } from './choix-parmi-regardees'
import { pileAOuvrirSeule } from './pile-auto'
import { nomDeCapacite } from './DemandeCentrale'

afterEach(() => localStorage.removeItem('marvel-langue'))

const option = (id: number, name: string, cibles: number[], echec = ''): Option =>
  ({ id, name, bind_id: 1, bind_player_id: 0, all_legal_targets: cibles, target_num_range: [cibles.length ? 1 : 0, cibles.length ? 1 : 0],
     target_payment: {}, select_rule: '', select_rule_param: [0, 0], target_must_include_traits: [], failure_reason: echec,
     is_search: false, is_text_choice: true }) as unknown as Option
const REGARDEES = new Set([38, 45, 15])

describe('choisir parmi des cartes déjà regardées', () => {
  it('« Futuriste » : la seule option, dont les 3 cibles sont les cartes regardées, se lance d’office', () => {
    const futuriste = option(1, 'Futurist', [38, 45, 15])
    expect(optionParmiRegardees([futuriste], REGARDEES)).toBe(futuriste)
  })

  it('pas d’office : plusieurs options jouables, une cible pas regardée, ou rien de regardé', () => {
    expect(optionParmiRegardees([option(1, 'Futurist', [38, 45]), option(7, 'Change_Form', [])], REGARDEES)).toBeUndefined()
    expect(optionParmiRegardees([option(1, 'Futurist', [38, 99])], REGARDEES)).toBeUndefined()
    expect(optionParmiRegardees([option(1, 'Futurist', [38])], new Set())).toBeUndefined()
    expect(optionParmiRegardees([option(1, 'Interrupt', [])], REGARDEES)).toBeUndefined()
  })

  it('jamais une décision de jeu, même si ses cibles ont été regardées', () => {
    for (const name of ['Defense', 'Attack', 'Thwart', 'Hero_Interrupt', 'Play']) {
      const o = { ...option(1, name, [38, 45, 15]), is_text_choice: false, is_search: false } as Option
      expect(optionParmiRegardees([o], REGARDEES)).toBeUndefined()
    }
  })

  it('une option refusée par le moteur ne compte pas', () => {
    const futuriste = option(1, 'Futurist', [38, 45, 15])
    expect(optionParmiRegardees([futuriste, option(2, 'Play', [38], 'check_cost')], REGARDEES)).toBe(futuriste)
  })

  it('la pile s’ouvre d’office SUR PC quand les cartes cherchées ont déjà été regardées', () => {
    const piles = new Map([[34, 'Deck']])
    const base = { telephone: false, rechercheEnCours: true, piles, pileOuverte: undefined }
    expect(pileAOuvrirSeule(base)).toBeUndefined()
    expect(pileAOuvrirSeule({ ...base, dejaRegardees: ciblesDejaRegardees([38, 45, 15], REGARDEES) })).toBe(34)
    expect(ciblesDejaRegardees([38, 99], REGARDEES)).toBe(false)
  })

  it('le titre prend le nom imprimé français (« Futuriste »), pas le nom moteur', () => {
    localStorage.setItem('marvel-langue', 'fr')
    const texte = 'Futuriste — Action : regardez les 3 cartes du dessus de votre deck. Ajoutez-en 1 à votre main et défaussez les autres.'
    expect(nomDeCapacite(option(1, 'Futurist', [38, 45, 15]), texte)).toBe('Futuriste')
  })
})

describe('une seule option qui ne sert qu’à désigner des cartes : le sélecteur s’ouvre directement', () => {
  const avec = (o: Partial<Option>): Option => ({ ...option(1, 'Pay_cost_Discard', [42, 26, 35]), ...o }) as Option
  it('#158 Captain America : « Pay cost Discard » (la main) s’ouvre directement', () => {
    const o = avec({ target_num_range: [1, 1] })
    expect(optionACiblesSeule([o])).toBe(o)
  })
  it('#153 Magneto : la recherche de la M-Type Sentinel s’ouvre directement', () => {
    const o = avec({ name: 'When_Revealed', is_search: true, all_legal_targets: [70, 71, 72] })
    expect(optionACiblesSeule([o])).toBe(o)
  })
  it('jamais : plusieurs options, minimum 0, aucune cible, une carte à jouer', () => {
    expect(optionACiblesSeule([avec({}), avec({ id: 2 })])).toBeUndefined()
    expect(optionACiblesSeule([avec({ target_num_range: [0, 3] })])).toBeUndefined()
    expect(optionACiblesSeule([avec({ all_legal_targets: [], target_num_range: [0, 0] })])).toBeUndefined()
    expect(optionACiblesSeule([avec({ name: 'Play' })])).toBeUndefined()
    // #160 : « In the Wings » (interruption héros, seule cible : elle-même) ne se lance pas seule non plus.
    expect(optionACiblesSeule([avec({ name: 'Hero_Interrupt', is_search: false, all_legal_targets: [42] })])).toBeUndefined()
    // #161 : une décision (défendre, attaquer) n'est jamais lancée d'office, même seule : le joueur doit pouvoir refuser.
    expect(optionACiblesSeule([avec({ name: 'Defense', is_search: false, all_legal_targets: [49] })])).toBeUndefined()
    expect(optionACiblesSeule([avec({ name: 'Attack', is_search: false, all_legal_targets: [49] })])).toBeUndefined()
    expect(optionACiblesSeule([avec({ target_payment: { 0: { cost: '1' } } as unknown as Option['target_payment'] })])).toBeUndefined()
  })
})
