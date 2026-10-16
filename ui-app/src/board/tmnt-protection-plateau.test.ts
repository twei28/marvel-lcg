// Aspect TMNT Protection (`up`) : ce que le plateau DESSINE une fois la carte résolue.
//
// `tools/cas/tmnt_aspect_protection.py` prouve ce que le moteur FAIT ; ce fichier prouve ce que le
// joueur REGARDE (PROCESSUS-CARTE.md, étape 8 bis). On pose à la main l'état d'arrivée que le moteur
// publie (cartes d'état et améliorations rattachées par `bind_object_id`) et on affirme sur
// `dessinee(...)`. Les cartes qui ne font que chiffrer n'ont pas de cas ici.
import { describe, expect, it } from 'vitest'
import { carteSurTable as carte, dessinee, siege, tableAvec } from './plateau-de-test'

const IDENTITE = 1
const identite = () => carte(IDENTITE, '01001a', 'Hero', 'Spider-Man')

describe('statuts posés par les cartes Protection', () => {
  it('up007 Cyber Ninja : la carte Camouflé posée sur l allié est dessinée sous lui', () => {
    const m = tableAvec(siege({
      area_hero: [identite()],
      allies: [carte(50, 'up007', 'Ally', 'Cyber Ninja'), carte(60, 'cloaked', 'StatusCard', 'Cloaked', { bind_object_id: 50 })],
    }))
    expect(dessinee(m, 60)).toBeDefined()
    expect(dessinee(m, 60)?.kind).toBe('status')
    expect(dessinee(m, 60)?.portePar).toBe(50)
  })

  it('up023 Lookout : Camouflé sur le héros, Lookout parti en défausse', () => {
    const m = tableAvec(siege({
      area_hero: [identite(), carte(61, 'cloaked', 'StatusCard', 'Cloaked', { bind_object_id: IDENTITE })],
      player_discard_pile: [carte(20, 'up023', 'Upgrade', 'Lookout')],
    }))
    expect(dessinee(m, 61)?.portePar).toBe(IDENTITE)
    expect(dessinee(m, 20)?.zone).toBe('piles-joueur')
  })

  it('up016 Herman : ses trois cartes Tenace sont toutes à l écran, sous lui', () => {
    const m = tableAvec(siege({
      area_hero: [identite()],
      allies: [
        carte(51, 'up016', 'Ally', 'Herman'),
        carte(62, 'tough', 'StatusCard', 'Tough', { bind_object_id: 51 }),
        carte(63, 'tough', 'StatusCard', 'Tough', { bind_object_id: 51 }),
        carte(64, 'tough', 'StatusCard', 'Tough', { bind_object_id: 51 }),
      ],
    }))
    for (const id of [62, 63, 64]) expect(dessinee(m, id)?.portePar).toBe(51)
  })

  it('up024 Nobody : Tenace OU Camouflé posé sur lui', () => {
    const m = tableAvec(siege({
      area_hero: [identite()],
      allies: [carte(52, 'up024', 'Ally', 'Nobody'), carte(65, 'cloaked', 'StatusCard', 'Cloaked', { bind_object_id: 52 })],
    }))
    expect(dessinee(m, 65)?.portePar).toBe(52)
  })
})

describe('améliorations Protection attachées', () => {
  it('up027 Protection Training et up033 Senkon sous un allié', () => {
    const m = tableAvec(siege({
      area_hero: [identite()],
      allies: [
        carte(53, 'up043', 'Ally', 'Wonder Turtle'),
        carte(21, 'up027', 'Upgrade', 'Protection Training', { bind_object_id: 53 }),
        carte(22, 'up033', 'Upgrade', 'Senkon', { bind_object_id: 53, is_ready: false }),
      ],
    }))
    expect(dessinee(m, 21)?.portePar).toBe(53)
    expect(dessinee(m, 22)?.portePar).toBe(53)
    expect(dessinee(m, 22)?.exhausted).toBe(true)
  })

  it('up028 Rabid Infection sous le sbire engagé, pas sur l identité', () => {
    const m = tableAvec(siege({
      area_hero: [identite()],
      engaged_enemies: [
        carte(81, '01101', 'Minion', 'Hydra Mercenary'),
        carte(23, 'up028', 'Upgrade', 'Rabid Infection', { bind_object_id: 81 }),
      ],
    }))
    expect(dessinee(m, 23)).toBeDefined()
    expect(dessinee(m, 23)?.portePar).toBe(81)
  })

  it('témoin : une carte absente de la table n est pas dessinée', () => {
    const m = tableAvec(siege({ area_hero: [identite()] }))
    expect(dessinee(m, 999)).toBeUndefined()
  })
})
