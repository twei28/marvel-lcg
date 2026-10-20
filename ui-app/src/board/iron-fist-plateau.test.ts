// Iron Fist (pack officiel MC64EN, `64001a`-`64012`) : ce que le plateau DESSINE une fois la carte résolue.
//
// `Fusion/marvel-lcg-src/tools/cas/iron_fist.py` prouve ce que le moteur FAIT ; ce fichier prouve ce que le
// joueur REGARDE (PROCESSUS-CARTE.md, étape 8 bis). On pose à la main l'état d'arrivée que le moteur publie :
// le compteur de chi est `info.c_chi` de la CARTE d'identité (Iron Fist et Danny Rand sont une seule carte,
// le stock reste au retournement), et `info.c_chi` d'Embody the Dragon pour les chi déplacés sur elle.
//
// Aucun correctif de plateau n'a été nécessaire : le rendu générique des compteurs (`compteurs` de
// `dessinee`, nom français « chi » dans compteurs-fr.ts) suffisait. Sensibilité vérifiée le 20/10/2026 :
// sans `c_chi` dans l'état publié, les assertions `toBe(n)` tombent (valeur `undefined`).
//
// Cartes SANS cas propre ici, parce qu'elles ne font que chiffrer : 64003 Dragon Punch, 64004 Fists of Fury
// (dégâts ; le Sonné de Dragon Punch est le même rendu que tv004), 64005 The Way of Things, 64010 Feel the
// Flow (menace), 64006 Lei Kung (pioche ; seule son inclinaison est dessinée, cas ci-dessous), 64012
// Redirect Chi (ressource).
import { describe, expect, it } from 'vitest'
import { carteSurTable as carte, cartesDessinees, dessinee, siege, tableAvec } from './plateau-de-test'

const IDENTITE = 1

const heros = (chi = 0, extra: Record<string, unknown> = {}) =>
  carte(IDENTITE, '64001a', 'Hero', 'Iron Fist', { info: chi > 0 ? { c_chi: chi } : {}, ...extra })
const civil = (chi = 0, extra: Record<string, unknown> = {}) =>
  carte(IDENTITE, '64001b', 'AlterEgo', 'Danny Rand', { info: chi > 0 ? { c_chi: chi } : {}, ...extra })
const technique = (id: number, code: string, nom: string, extra: Record<string, unknown> = {}) =>
  carte(id, code, 'Upgrade', nom, { bind_object_id: IDENTITE, ...extra })

describe('64001a Iron Fist : le chi posé « ici » est dessiné sur l identité', () => {
  it('forme héros : 3 chi visibles sur Iron Fist', () => {
    const monde = tableAvec(siege({ area_hero: [heros(3)] }))
    expect(dessinee(monde, IDENTITE)?.compteurs.chi).toBe(3)
  })

  it('forme alter ego : le même stock reste visible sur Danny Rand (décision n°5)', () => {
    const monde = tableAvec(siege({ area_hero: [civil(5)] }))
    const danny = dessinee(monde, IDENTITE)
    expect(danny?.codeCarte).toBe('64001b')
    expect(danny?.compteurs.chi).toBe(5)
  })

  it('tous les chi dépensés : plus aucun compteur dessiné', () => {
    const monde = tableAvec(siege({ area_hero: [heros(0)] }))
    expect(dessinee(monde, IDENTITE)?.compteurs.chi).toBeUndefined()
  })
})

describe('64001b Meditation / 64007 Book of the Iron Fist : la Technique mise en jeu est attachée à l identité', () => {
  const monde = () =>
    tableAvec(
      siege({
        area_hero: [
          civil(0),
          technique(10, '64011', "Keep 'Em Coming"),
          carte(11, '64007', 'Upgrade', 'Book of the Iron Fist', { bind_object_id: IDENTITE, is_ready: false }),
        ],
      })
    )

  it('la Technique est dessinée sous l identité', () => {
    const vue = dessinee(monde(), 10)
    expect(vue).toBeDefined()
    expect(vue?.portePar).toBe(IDENTITE)
    expect(vue?.kind).toBe('upgrade')
  })

  it('le Livre est couché après usage', () => {
    expect(dessinee(monde(), 11)?.exhausted).toBe(true)
  })
})

describe('64009 Embody the Dragon : les chi déplacés sont dessinés sur la carte, pas sur l identité', () => {
  it('1 chi sur la carte, 1 sur Iron Fist', () => {
    const monde = tableAvec(
      siege({ area_hero: [heros(1), technique(20, '64009', 'Embody the Dragon', { info: { c_chi: 1 } })] })
    )
    expect(dessinee(monde, 20)?.compteurs.chi).toBe(1)
    expect(dessinee(monde, IDENTITE)?.compteurs.chi).toBe(1)
  })
})

describe('64006 Lei Kung : soutien couché après son Action', () => {
  it('Lei Kung est dessiné chez les soutiens, incliné', () => {
    const monde = tableAvec(
      siege({ area_hero: [heros(0)], supports: [carte(30, '64006', 'Support', 'Lei Kung', { is_ready: false })] })
    )
    const vue = dessinee(monde, 30)
    expect(vue).toBeDefined()
    expect(vue?.exhausted).toBe(true)
  })
})

describe('64002 Deep Breathing : la carte Iron Fist trouvée arrive en main, les autres en défausse', () => {
  const monde = () =>
    tableAvec(
      siege({
        area_hero: [heros(1)],
        hand_cards: [carte(40, '64010', 'Upgrade', 'Feel the Flow')],
        player_discard_pile: [carte(41, '01089', 'Resource', 'Genius'), carte(42, '64002', 'Event', 'Deep Breathing')],
      })
    )

  it('la carte trouvée est dans la main', () => {
    expect(dessinee(monde(), 40)?.zone).toBe('main')
  })

  it('la défausse montre la carte du dessus, 2 cartes', () => {
    const piles = cartesDessinees(monde()).filter((c) => c.zone === 'piles-joueur' && !c.facedown)
    expect(piles.length).toBeGreaterThan(0)
  })
})

describe('64008-64012 : les Techniques en jeu sont dessinées attachées à Iron Fist', () => {
  it('les cinq Techniques sont sous l identité', () => {
    const monde = tableAvec(
      siege({
        area_hero: [
          heros(2),
          technique(50, '64008', 'Channel the Iron Fist'),
          technique(51, '64009', 'Embody the Dragon'),
          technique(52, '64010', 'Feel the Flow'),
          technique(53, '64011', "Keep 'Em Coming"),
          technique(54, '64012', 'Redirect Chi'),
        ],
      })
    )
    for (const id of [50, 51, 52, 53, 54]) {
      expect(dessinee(monde, id)?.portePar).toBe(IDENTITE)
    }
  })
})
