// TMNT Shinobi, Kuji-Kiri (`sj`) : ce que le plateau DESSINE une fois la carte résolue (PROCESSUS-CARTE, étape 8 bis).
//
// `Fusion/marvel-lcg-src/tools/cas/tmnt_shinobi_kuji_kiri.py` prouve ce que le moteur FAIT ; ce fichier prouve ce que le joueur
// REGARDE. Les cartes qui changent ce qu'on voit : une amélioration attachée à un allié (sj002 Imbued Weapons, sj014 Kuji-Kaijū),
// un soutien qui porte des compteurs mystiques (sj012 A Thin Place), un sbire passé allié contrôlé qui porte Enthrall (sj006).
// On pose à la main l'état d'arrivée que le moteur publie (`bind_object_id` = le porteur, `info.c_mystic`) et on affirme sur `dessinee`.
//
// Sans cas ici, parce qu'elles ne font que chiffrer, piocher, défausser, redresser ou poser un statut (badge déjà couvert par
// `effets-statuts.test.ts`) : sj001, sj003, sj004, sj005, sj007, sj008, sj009 (la pile de victoire est déjà dessinée), sj010,
// sj011, sj013 (le Crayon quitte la partie), sj015, sj016, sj017, sj018, sj019, sj020.
import { describe, expect, it } from 'vitest'
import { carteSurTable as carte, cartesDessinees, dessinee, siege, tableAvec } from './plateau-de-test'

const IDENTITE = 1
const ALLIE = 20
const AMELIORATION = 21
const KAIJU = 22
const THIN = 30

describe('sj002 / sj014 : une amélioration attachée à un allié est dessinée avec lui', () => {
  const monde = (...attachees: ReturnType<typeof carte>[]) =>
    tableAvec(
      siege({
        area_hero: [carte(IDENTITE, '01001a', 'Hero', 'Spider-Man')],
        allies: [carte(ALLIE, '01059', 'Ally', 'Jessica Jones'), ...attachees],
      })
    )
  const imbued = carte(AMELIORATION, 'sj002', 'Upgrade', 'Imbued Weapons', { bind_object_id: ALLIE })
  const kaiju = carte(KAIJU, 'sj014', 'Upgrade', 'Kuji-Kaijū', { bind_object_id: ALLIE })

  it('Imbued Weapons est à l écran, portée par l allié', () => {
    const c = dessinee(monde(imbued), AMELIORATION)
    expect(c).toBeDefined()
    expect(c?.portePar).toBe(ALLIE)
    expect(c?.kind).toBe('upgrade')
  })

  it('deux améliorations sur le même allié (Imbued Weapons et Kuji-Kaijū) sont dessinées derrière lui', () => {
    const m = monde(imbued, kaiju)
    const vues = cartesDessinees(m)
    const rang = (id: number) => vues.findIndex((c) => c.id === id)
    expect(dessinee(m, AMELIORATION)).toBeDefined()
    expect(dessinee(m, KAIJU)).toBeDefined()
    expect(rang(AMELIORATION)).toBeGreaterThan(rang(ALLIE))
    expect(rang(KAIJU)).toBeGreaterThan(rang(ALLIE))
  })

  it('témoin : sans amélioration, rien n est dessiné derrière l allié', () => {
    expect(dessinee(monde(), AMELIORATION)).toBeUndefined()
  })
})

describe('sj012 A Thin Place : les compteurs mystiques sont dessinés sur le soutien', () => {
  const monde = (mystiques: number) =>
    tableAvec(
      siege({
        area_hero: [carte(IDENTITE, '01001b', 'AlterEgo', 'Peter Parker')],
        supports: [carte(THIN, 'sj012', 'Support', 'A Thin Place', { info: { c_mystic: mystiques } })],
      })
    )

  it('3 compteurs mystiques posés : le plateau affiche 3 « mystique »', () => {
    expect(dessinee(monde(3), THIN)?.compteurs.mystique ?? dessinee(monde(3), THIN)?.compteurs.mystic).toBe(3)
  })

  it('témoin : aucun compteur, aucune pastille', () => {
    const c = dessinee(monde(0), THIN)
    expect(c).toBeDefined()
    expect(c?.compteurs.mystique ?? c?.compteurs.mystic ?? 0).toBe(0)
  })
})

describe('sj006 Enthrall : le sbire contrôlé (allié) et son Enthrall sont dessinés dans la zone des alliés', () => {
  it('l allié contrôlé et l amélioration qui le contrôle sont à l écran', () => {
    const m = tableAvec(
      siege({
        area_hero: [carte(IDENTITE, '01001a', 'Hero', 'Spider-Man')],
        allies: [
          carte(ALLIE, 'enthrall_controlled_ally', 'Ally', 'Shocker', { pic_id: '01103' }),
          carte(AMELIORATION, 'sj006', 'Upgrade', 'Enthrall', { bind_object_id: ALLIE }),
        ],
      })
    )
    expect(dessinee(m, ALLIE)).toBeDefined()
    expect(dessinee(m, AMELIORATION)?.portePar).toBe(ALLIE)
  })
})
