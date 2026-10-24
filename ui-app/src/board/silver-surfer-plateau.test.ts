// Silver Surfer (DesignHacker, MC4 SEALED, `sv001a`-`sv015`) : ce que le plateau DESSINE une fois les cartes résolues.
//
// `Fusion/marvel-lcg-src/tools/cas/silver_surfer.py` prouve ce que le moteur FAIT ; ce fichier prouve ce que le
// joueur REGARDE (PROCESSUS-CARTE.md, étape 8 bis). Les cartes du pack qui changent ce qu'on VOIT :
//   - sv003 The Silver Surfboard : amélioration posée sur l'identité ;
//   - sv004 Energy Manipulation : compteurs d'énergie (`info.c_energy`, le même nom que 01018 Energy Channel) ;
//   - sv012 Galactus / sv013 The World Eater : deux sbires élites engagés avec le joueur ;
//   - sv015 Cosmic Power : attachement de rencontre posé sur Galactus (ou le méchant).
// Aucun correctif de plateau n'a été nécessaire : le rendu générique suffisait.
import { describe, expect, it } from 'vitest'
import { carteSurTable as carte, cartesDessinees, dessinee, siege, tableAvec } from './plateau-de-test'

const IDENTITE = 1
const PLANCHE = 2
const MANIPULATION = 3
const GALACTUS = 10
const MANGEUR = 11
const PUISSANCE = 12

const heros = () => carte(IDENTITE, 'sv001a', 'Hero', 'Silver Surfer')

describe('sv003 The Silver Surfboard : posée sur l identité', () => {
  const monde = () =>
    tableAvec(
      siege({
        area_hero: [heros(), carte(PLANCHE, 'sv003', 'Upgrade', 'The Silver Surfboard', { bind_object_id: IDENTITE })],
      })
    )

  it('est dessinée, juste derrière Silver Surfer', () => {
    expect(dessinee(monde(), PLANCHE)).toBeDefined()
    expect(dessinee(monde(), PLANCHE)?.portePar).toBe(IDENTITE)
  })

  it('se couche une fois inclinée (Hero Action : exhaust -> ready Silver Surfer)', () => {
    const incline = tableAvec(
      siege({
        area_hero: [
          heros(),
          carte(PLANCHE, 'sv003', 'Upgrade', 'The Silver Surfboard', { bind_object_id: IDENTITE, is_ready: false }),
        ],
      })
    )
    expect(dessinee(incline, PLANCHE)?.exhausted).toBe(true)
    expect(dessinee(monde(), PLANCHE)?.exhausted).toBe(false)
  })
})

describe('sv004 Energy Manipulation : les compteurs d énergie sont dessinés', () => {
  const avec = (n: number) =>
    tableAvec(
      siege({
        area_hero: [
          heros(),
          carte(MANIPULATION, 'sv004', 'Upgrade', 'Energy Manipulation', {
            bind_object_id: IDENTITE,
            info: n > 0 ? { c_energy: n } : {},
          }),
        ],
      })
    )

  it('3 compteurs visibles sur la carte', () => {
    expect(dessinee(avec(3), MANIPULATION)?.compteurs.energy).toBe(3)
  })

  it('aucun compteur : rien de dessiné', () => {
    expect(dessinee(avec(0), MANIPULATION)?.compteurs.energy).toBeUndefined()
  })
})

describe('sv012 Galactus / sv013 The World Eater / sv015 Cosmic Power', () => {
  const monde = () =>
    tableAvec(
      siege({
        area_hero: [heros()],
        engaged_enemies: [
          carte(GALACTUS, 'sv012', 'Minion', 'Galactus'),
          carte(MANGEUR, 'sv013', 'Minion', 'The World Eater'),
          carte(PUISSANCE, 'sv015', 'Attachment', 'Cosmic Power', { bind_object_id: GALACTUS }),
        ],
      })
    )

  it('les deux sbires engagés sont dessinés', () => {
    expect(dessinee(monde(), GALACTUS)).toBeDefined()
    expect(dessinee(monde(), MANGEUR)).toBeDefined()
  })

  it('Cosmic Power est dessinée sur Galactus (et non sur l identité)', () => {
    const vue = dessinee(monde(), PUISSANCE)
    expect(vue).toBeDefined()
    expect(vue?.portePar).toBe(GALACTUS)
    expect(cartesDessinees(monde()).filter((c) => c.portePar === IDENTITE)).toHaveLength(0)
  })
})
