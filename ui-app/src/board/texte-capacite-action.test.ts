import { describe, expect, it } from 'vitest'
import { nomActionParlant } from './texte-capacite'

const DEUX = '<b>Hero Action</b>: Spend [[energy]] → draw 1 card.\n<b>Hero Action</b>: Exhaust this card → heal 2 damage.'

describe('nomActionParlant', () => {
  it('nomme chaque action par son paragraphe quand la carte en offre deux du meme type', () => {
    expect(nomActionParlant('Hero_Action', DEUX)).toBe('Spend [energy] → draw 1 card.')
    expect(nomActionParlant('Hero_Action_1', DEUX)).toBe('Exhaust this card → heal 2 damage.')
  })
  it("ne dit rien quand il n'y a qu'une action de ce type", () => {
    expect(nomActionParlant('Hero_Action', '<b>Hero Action</b>: Spend [[energy]] → draw 1 card.')).toBeUndefined()
  })
  it('ne confond pas Action et Hero Action', () => {
    const texte = '<b>Action</b>: Draw 1 card.\n<b>Hero Action</b>: Heal 1.\n<b>Hero Action</b>: Heal 2.'
    expect(nomActionParlant('Action', texte)).toBeUndefined()
    expect(nomActionParlant('Hero_Action_1', texte)).toBe('Heal 2.')
  })
  it('lit le francais officiel', () => {
    const fr = '<b>Action de héros</b> : Dépensez [[energy]] → piochez 1 carte.\n<b>Action de héros</b> : Soignez 2 dégâts.'
    expect(nomActionParlant('Hero_Action_1', fr)).toBe('Soignez 2 dégâts.')
  })
  it("laisse les noms qui ne sont pas des actions et les textes absents", () => {
    expect(nomActionParlant('Interrupt', DEUX)).toBeUndefined()
    expect(nomActionParlant('Action', undefined)).toBeUndefined()
  })
})
