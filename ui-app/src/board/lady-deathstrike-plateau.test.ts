// Lady Deathstrike (Mysteltainn, `ld001`-`ld018`) : ce que le plateau DESSINE (PROCESSUS-CARTE étape 8 bis).
// `tools/cas/lady_deathstrike*.py` prouvent ce que le moteur FAIT. Ici :
//   - ld005 Bleeding Out : attachement Permanent sur l'identité, compteurs « bleed » ;
//   - ld004b Mutant Hunting Season : complot principal avec jeton d'accélération ;
//   - ld006 / ld008 : attachements de rencontre posés sur Lady Deathstrike ;
//   - ld012 Stalking Prey : manigance annexe, menace dessinée ;
import { describe, expect, it } from 'vitest'
import { carteSurTable as carte, dessinee, siege, tableAvec } from './plateau-de-test'

const IDENTITE = 1
const SAIGNEMENT = 2
const VILAIN = 10
const ARMURE = 11
const GRIFFES = 12
const PREDATION = 20

const monde = () =>
  tableAvec(
    siege({
      area_hero: [
        carte(IDENTITE, '01001b', 'AlterEgo', 'Peter Parker'),
        carte(SAIGNEMENT, 'ld005', 'Attachment', 'Bleeding Out', { bind_object_id: IDENTITE, info: { c_bleed: 4 } }),
      ],
    }),
    {
      area_villain: [
        carte(VILAIN, 'ld001', 'EncounterVillain', 'Lady Deathstrike'),
        carte(ARMURE, 'ld006', 'Attachment', 'Adamantium Nanoskeleton', { bind_object_id: VILAIN }),
        carte(GRIFFES, 'ld008', 'Attachment', 'Reinforced Adamantium Claws', { bind_object_id: VILAIN }),
      ],
      area_schemes_side: [carte(PREDATION, 'ld012', 'SideScheme', 'Stalking Prey', { info: { k_threat: 6 } })],
    }
  )

describe('ld005 Bleeding Out', () => {
  it('est dessinée sur l identité avec ses 4 compteurs de saignement', () => {
    expect(dessinee(monde(), SAIGNEMENT)).toBeDefined()
    expect(dessinee(monde(), SAIGNEMENT)?.portePar).toBe(IDENTITE)
    expect(dessinee(monde(), SAIGNEMENT)?.compteurs.bleed).toBe(4)
  })
})

describe('ld006 / ld008 : attachements sur Lady Deathstrike', () => {
  it('l armure et les griffes sont dessinées, portées par le vilain', () => {
    expect(dessinee(monde(), ARMURE)?.portePar).toBe(VILAIN)
    expect(dessinee(monde(), GRIFFES)?.portePar).toBe(VILAIN)
  })
})

describe('ld012 Stalking Prey', () => {
  it('manigance annexe dessinée avec sa menace', () => {
    expect(dessinee(monde(), PREDATION)).toBeDefined()
    expect(dessinee(monde(), PREDATION)?.menace).toBe(6)
  })
})
