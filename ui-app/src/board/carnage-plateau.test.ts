// Carnage / Eddie Brock (ca001a/b) : ce que la table DESSINE (étape 8 bis de PROCESSUS-CARTE).
//  - ca004 Lethal Restraint, ca006 Frenzied Violence, ca008 Amorphous Arsenal : améliorations attachées au héros ; ca003 Symbiote Hive-Mind : soutien ; ca002 Spider-Man : allié ;
//  - ca015 Torment : sbire némésis engagé, porteur de ca017 Death Spiral (attachement à un ENNEMI, pas à l'identité : le trou de Contingency Plan, à deux étages) ;
//  - ca016 Meticulous Targeting et ca021 Recognizing Evil : manigances annexes (paysage) ; ca019 Muse, ca020 Bushwacker : sbires engagés, ca022 Murderous Nature attachée à l'un d'eux.
// Le dessin d'un attachement à un ennemi est générique (`zones.ts`) : ce cas le vaut pour Carnage.
import { describe, expect, it } from 'vitest'
import { carteSurTable, dessinee, siege, tableAvec } from './plateau-de-test'

const CARNAGE = 1
const SPIDER_MAN = 2
const HIVE_MIND = 3
const RESTRAINT = 4
const FRENZIED = 5
const ARSENAL = 6
const TORMENT = 7
const SPIRAL = 8
const MUSE = 9
const BUSHWACKER = 10
const NATURE = 11
const TARGETING = 12
const RECOGNIZING = 13

const monde = () =>
  tableAvec(
    siege({
      area_hero: [
        carteSurTable(CARNAGE, 'ca001a', 'Hero', 'Carnage'),
        carteSurTable(RESTRAINT, 'ca004', 'Upgrade', 'Lethal Restraint', { bind_object_id: CARNAGE }),
        carteSurTable(FRENZIED, 'ca006', 'Upgrade', 'Frenzied Violence', { bind_object_id: CARNAGE }),
        carteSurTable(ARSENAL, 'ca008', 'Upgrade', 'Amorphous Arsenal', { bind_object_id: CARNAGE }),
      ],
      allies: [carteSurTable(SPIDER_MAN, 'ca002', 'Ally', 'Spider-Man')],
      supports: [carteSurTable(HIVE_MIND, 'ca003', 'Support', 'Symbiote Hive-Mind')],
      engaged_enemies: [
        carteSurTable(TORMENT, 'ca015', 'Minion', 'Torment'),
        carteSurTable(SPIRAL, 'ca017', 'Attachment', 'Death Spiral', { bind_object_id: TORMENT }),
        carteSurTable(MUSE, 'ca019', 'Minion', 'Muse'),
        carteSurTable(BUSHWACKER, 'ca020', 'Minion', 'Bushwacker'),
        carteSurTable(NATURE, 'ca022', 'Attachment', 'Murderous Nature', { bind_object_id: BUSHWACKER }),
      ],
    }),
    { area_schemes_side: [carteSurTable(TARGETING, 'ca016', 'SideScheme', 'Meticulous Targeting'), carteSurTable(RECOGNIZING, 'ca021', 'SideScheme', 'Recognizing Evil')] },
  )

describe('Carnage : ce que la table dessine', () => {
  it("dessine Carnage, ses trois améliorations (portées par l'identité), Spider-Man et Symbiote Hive-Mind", () => {
    for (const id of [CARNAGE, RESTRAINT, FRENZIED, ARSENAL, SPIDER_MAN, HIVE_MIND]) expect(dessinee(monde(), id)).toBeDefined()
    for (const id of [RESTRAINT, FRENZIED, ARSENAL]) expect(dessinee(monde(), id)?.portePar).toBe(CARNAGE)
  })
  it('dessine Torment avec Death Spiral attaché à lui, Muse, Bushwacker avec Murderous Nature, et les deux manigances annexes', () => {
    for (const id of [TORMENT, SPIRAL, MUSE, BUSHWACKER, NATURE, TARGETING, RECOGNIZING]) expect(dessinee(monde(), id)).toBeDefined()
    expect(dessinee(monde(), SPIRAL)?.portePar).toBe(TORMENT)
    expect(dessinee(monde(), NATURE)?.portePar).toBe(BUSHWACKER)
    expect(dessinee(monde(), SPIRAL)?.codeCarte).toBe('ca017')
  })
})
