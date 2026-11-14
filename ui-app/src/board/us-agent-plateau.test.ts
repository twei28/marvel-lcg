// U.S. Agent (DesignHacker, `us001a`-`us016`) : ce que le plateau DESSINE une fois les cartes résolues
// (PROCESSUS-CARTE.md, étape 8 bis). `Fusion/marvel-lcg-src/tools/cas/us_agent.py` prouve ce que le moteur FAIT ; ce
// fichier prouve ce que le joueur REGARDE. Les cartes du pack qui changent ce qu'on VOIT :
//   - us003 Deflection (Sonné sur deux sbires), us005 Roundhouse (Désorienté sur l'ennemi touché) et us007 Convincer
//     (Sonné sur le sbire touché) : des cartes d'état posées sur des ennemis ;
//   - us002 Bouncing Bulwark : le bouclier (us011) part en défausse puis REVIENT en jeu, porté par le héros ;
//   - us007 / us010 : Convincer et la Machine Gun portent leurs compteurs « charge » / « ammo » ;
//   - us006 Walker's Chopper : un soutien posé sur la table ;
//   - us014 Battle of the Patriots : une manigance annexe, menace de départ 4 ;
//   - us016 Spear of Odin : un attachement de rencontre posé sur un ENNEMI (Rhino).
// Aucun correctif de plateau : le rendu générique suffisait, ces cas sont verts d'emblée.
import { describe, expect, it } from 'vitest'
import { carteSurTable as carte, dessinee, siege, tableAvec } from './plateau-de-test'

const IDENTITE = 1
const BOUCLIER = 2
const FUSIL = 3
const CONVAINCRE = 4
const HELICO = 5
const RHINO = 80
const LANCE = 81
const BATAILLE = 82

const heros = () => carte(IDENTITE, 'us001a', 'Hero', 'U.S. Agent')

const monde = () =>
  tableAvec(
    siege({
      area_hero: [
        heros(),
        carte(BOUCLIER, 'us011', 'Upgrade', "U.S. Agent's Shield", { bind_object_id: IDENTITE, is_ready: false }),
        carte(FUSIL, 'us010', 'Upgrade', "U.S. Agent's Machine Gun", { bind_object_id: IDENTITE, info: { c_ammo: 3 } }),
        carte(CONVAINCRE, 'us007', 'Upgrade', 'Convincer', { bind_object_id: IDENTITE, info: { c_charge: 2 } }),
      ],
      supports: [carte(HELICO, 'us006', 'Support', "Walker's Chopper")],
    }),
    {
      area_villain: [
        carte(RHINO, '01094', 'EncounterVillain', 'Rhino'),
        carte(LANCE, 'us016', 'Attachment', 'Spear of Odin', { bind_object_id: RHINO }),
      ],
      area_schemes_side: [carte(BATAILLE, 'us014', 'SideScheme', 'Battle of the Patriots', { info: { k_threat: 4 } })],
    }
  )

describe('us002 Bouncing Bulwark : le bouclier revenu en jeu', () => {
  it('est dessiné derrière U.S. Agent, incliné quand il a servi', () => {
    expect(dessinee(monde(), BOUCLIER)).toBeDefined()
    expect(dessinee(monde(), BOUCLIER)?.portePar).toBe(IDENTITE)
    expect(dessinee(monde(), BOUCLIER)?.exhausted).toBe(true)
  })
})

describe('us007 Convincer et us010 Machine Gun : leurs compteurs', () => {
  it('la Machine Gun montre ses 3 compteurs munition (ammo)', () => {
    expect(dessinee(monde(), FUSIL)?.portePar).toBe(IDENTITE)
    expect(dessinee(monde(), FUSIL)?.compteurs.ammo).toBe(3)
  })

  it('Convincer montre ses compteurs charge restants', () => {
    expect(dessinee(monde(), CONVAINCRE)?.compteurs.charge).toBe(2)
  })
})

describe('us006 Walker\'s Chopper', () => {
  it('est dessiné parmi les soutiens', () => {
    expect(dessinee(monde(), HELICO)).toBeDefined()
  })
})

describe('us014 Battle of the Patriots', () => {
  it('est dessinée avec sa menace de départ', () => {
    expect(dessinee(monde(), BATAILLE)?.menace).toBe(4)
  })
})

describe('us016 Spear of Odin', () => {
  it('est dessinée, portée par Rhino', () => {
    expect(dessinee(monde(), LANCE)).toBeDefined()
    expect(dessinee(monde(), LANCE)?.portePar).toBe(RHINO)
  })
})

describe('cartes d état posées par us003, us005 et us007', () => {
  const SBIRE_1 = 83
  const SBIRE_2 = 84
  const avecStatuts = (statuts: [number, string, number][]) =>
    tableAvec(siege({ area_hero: [heros()] }), {
      area_villain: [
        carte(RHINO, '01094', 'EncounterVillain', 'Rhino'),
        carte(SBIRE_1, '01121', 'Minion', 'Weapons Runner'),
        carte(SBIRE_2, '01103', 'Minion', 'Shocker'),
        ...statuts.map(([id, statut, porteur]) => carte(id, statut, 'StatusCard', statut, { bind_object_id: porteur })),
      ],
    })

  it('us003 Deflection : un Sonné sur chacun de deux sbires', () => {
    const monde = avecStatuts([
      [90, 'stunned', SBIRE_1],
      [91, 'stunned', SBIRE_2],
    ])
    expect(dessinee(monde, 90)?.portePar).toBe(SBIRE_1)
    expect(dessinee(monde, 91)?.portePar).toBe(SBIRE_2)
  })

  it('us005 Roundhouse : Désorienté sur Rhino', () => {
    const monde = avecStatuts([[92, 'confused', RHINO]])
    expect(dessinee(monde, 92)?.portePar).toBe(RHINO)
    expect(dessinee(monde, 92)?.codeCarte).toBe('confused')
  })
})
