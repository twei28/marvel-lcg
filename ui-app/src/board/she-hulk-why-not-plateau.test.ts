// She-Hulk « Why Not » (Merlin, `wn001a`-`wn011`) : ce que le plateau DESSINE une fois les cartes résolues.
//
// `Fusion/marvel-lcg-src/tools/cas/she_hulk_why_not.py` prouve ce que le moteur FAIT ; ce fichier prouve ce que le
// joueur REGARDE (PROCESSUS-CARTE.md, étape 8 bis). Les cartes du pack qui changent ce qu'on VOIT :
//   - wn008 Superhuman Strength : amélioration posée sur She-Hulk, qui RESTE quand l'ennemi attaqué est vaincu,
//     et une carte d'état Sonné sur l'ennemi attaqué sinon ;
//   - wn009 Hey you! : Sonné ET Désorienté sur le même ennemi ;
//   - wn010 Gamma Power : une carte Sonné sur chacun de deux ennemis (méchant et sbire).
// Les trois Team-Up sont retirés de la partie : la zone retirée n'est pas dessinée, rien à montrer.
// Aucun correctif de plateau : le rendu générique suffisait, ces cas sont verts d'emblée.
import { describe, expect, it } from 'vitest'
import { carteSurTable as carte, dessinee, siege, tableAvec } from './plateau-de-test'

const IDENTITE = 1
const FORCE = 2
const RHINO = 80
const SBIRE = 81

const heros = () => carte(IDENTITE, 'wn001a', 'Hero', 'She-Hulk')

describe('wn008 Superhuman Strength : posée sur She-Hulk', () => {
  it('est dessinée derrière She-Hulk (et y reste après avoir vaincu un sbire)', () => {
    const monde = tableAvec(
      siege({ area_hero: [heros(), carte(FORCE, 'wn008', 'Upgrade', 'Superhuman Strength', { bind_object_id: IDENTITE })] })
    )
    expect(dessinee(monde, FORCE)).toBeDefined()
    expect(dessinee(monde, FORCE)?.portePar).toBe(IDENTITE)
  })
})

describe('cartes d état posées par wn008, wn009 et wn010', () => {
  const avecStatuts = (statuts: [number, string, number][]) =>
    tableAvec(siege({ area_hero: [heros()] }), {
      area_villain: [
        carte(RHINO, '01094', 'EncounterVillain', 'Rhino'),
        carte(SBIRE, '01101', 'Minion', 'Hydra Mercenary'),
        ...statuts.map(([id, statut, porteur]) => carte(id, statut, 'StatusCard', statut, { bind_object_id: porteur })),
      ],
    })

  it('wn009 Hey you! : Sonné et Désorienté sur le même ennemi', () => {
    const monde = avecStatuts([
      [90, 'stunned', RHINO],
      [91, 'confused', RHINO],
    ])
    expect(dessinee(monde, 90)?.portePar).toBe(RHINO)
    expect(dessinee(monde, 91)?.portePar).toBe(RHINO)
    expect(dessinee(monde, 91)?.codeCarte).toBe('confused')
  })

  it('wn010 Gamma Power : un Sonné sur chacun des deux ennemis', () => {
    const monde = avecStatuts([
      [90, 'stunned', RHINO],
      [92, 'stunned', SBIRE],
    ])
    expect(dessinee(monde, 90)?.portePar).toBe(RHINO)
    expect(dessinee(monde, 92)?.portePar).toBe(SBIRE)
  })
})
