// Les packs custom du dépôt (Angel, Beast, Gambit, Human Torch, Jubilee,
// Magneto, The Thing, Wave) doivent pouvoir être choisis comme collection
// d'art des ressources doubles, au même titre que les promos FFG ou les
// re-skins déjà câblés (Gwenpool, Howard the Duck, Ms. America) — ajoutés le
// 22/09/2026, ils n'étaient nulle part dans `COLLECTIONS` avant ce cas.
import { describe, expect, it } from 'vitest'
import { collectionPourJoueur, picIdAffiche } from './variantes'

const PACKS_CUSTOM: Array<[string, [string, string, string]]> = [
  ['angel', ['42033', '42034', '42035']],
  ['beast', ['bt024', 'bt025', 'bt026']],
  ['gambit', ['37036', '37037', '37038']],
  ['human_torch', ['ht015', 'ht016', 'ht017']],
  ['jubilee', ['47035', '47036', '47037']],
  ['magneto', ['49043', '49044', '49045']],
  ['the_thing', ['th016', 'th017', 'th018']],
  ['wave', ['65017', '65018', '65019']],
]

describe('collections de ressources des packs custom', () => {
  it.each(PACKS_CUSTOM)('%s : choisie pour un héros, elle est bien appliquée', (code) => {
    const arts = { '65001': code }
    expect(collectionPourJoueur('65001a,65001b', 1, arts)).toBe(code)
  })

  it.each(PACKS_CUSTOM)('%s : substitue les trois ressources dans le bon ordre (Energy, Genius, Strength)', (code, [energie, genie, force]) => {
    expect(picIdAffiche('01088', code)).toBe(energie)
    expect(picIdAffiche('01089', code)).toBe(genie)
    expect(picIdAffiche('01090', code)).toBe(force)
  })

  it.each(PACKS_CUSTOM)('%s : ne touche à aucune autre carte', (code) => {
    expect(picIdAffiche('01094', code)).toBe('01094')
  })

  it('« standard » (chaîne vide) ne substitue rien, quel que soit le héros', () => {
    expect(picIdAffiche('01088', '')).toBe('01088')
    expect(picIdAffiche('01089', undefined)).toBe('01089')
  })
})
