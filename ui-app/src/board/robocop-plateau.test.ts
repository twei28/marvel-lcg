// RoboCop (rc001a/b) : ce que la table DESSINE (étape 8 bis de PROCESSUS-CARTE).
//  - rc005 Auto-9 et rc009 Gunarm (armes) sont posées sur RoboCop (héros) ;
//  - rc015 Stairs est attachée à ED-209 (rc013), sbire engagé : la carte attachée doit être dessinée, portée par son hôte ;
//  - rc014 Corporate Demonstration (manigance annexe) est à l'écran.
import { describe, expect, it } from 'vitest'
import { carteSurTable, dessinee, siege, tableAvec } from './plateau-de-test'

const ROBOCOP = 1
const AUTO9 = 2
const GUNARM = 3
const ED209 = 4
const STAIRS = 5
const DEMO = 6

const monde = () =>
  tableAvec(
    siege({
      area_hero: [
        carteSurTable(ROBOCOP, 'rc001a', 'Hero', 'RoboCop'),
        carteSurTable(AUTO9, 'rc005', 'Upgrade', 'Auto-9', { bind_object_id: ROBOCOP }),
        carteSurTable(GUNARM, 'rc009', 'Upgrade', 'Gunarm', { bind_object_id: ROBOCOP }),
      ],
      engaged_enemies: [
        carteSurTable(ED209, 'rc013', 'Minion', 'ED-209'),
        carteSurTable(STAIRS, 'rc015', 'Attachment', 'Stairs', { bind_object_id: ED209 }),
      ],
    }),
    { area_schemes_side: [carteSurTable(DEMO, 'rc014', 'SideScheme', 'Corporate Demonstration')] },
  )

describe('RoboCop : ce que la table dessine', () => {
  it('dessine Auto-9 et Gunarm sur RoboCop', () => {
    expect(dessinee(monde(), AUTO9)).toBeDefined()
    expect(dessinee(monde(), AUTO9)?.portePar).toBe(ROBOCOP)
    expect(dessinee(monde(), GUNARM)).toBeDefined()
    expect(dessinee(monde(), GUNARM)?.portePar).toBe(ROBOCOP)
  })
  it("dessine ED-209 (engagé) et Stairs qui lui est attachée", () => {
    expect(dessinee(monde(), ED209)).toBeDefined()
    expect(dessinee(monde(), STAIRS)).toBeDefined()
    expect(dessinee(monde(), STAIRS)?.portePar).toBe(ED209)
  })
  it('dessine Corporate Demonstration (complot annexe)', () => {
    expect(dessinee(monde(), DEMO)).toBeDefined()
  })
})
