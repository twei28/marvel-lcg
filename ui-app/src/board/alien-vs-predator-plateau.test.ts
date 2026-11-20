// Alien vs. Predator (RyCoRan, `ap001a`-`ap306`) : ce que le plateau DESSINE (PROCESSUS-CARTE étape 8 bis).
// `tools/cas/alien_vs_predator*.py` prouvent ce que le moteur FAIT. Ici, ce que le joueur REGARDE :
//   - deux vilains en jeu en même temps (Alien Queen, Predator Warlord), compteur actif sur l'un ;
//   - ap005a : le deck Xenomorph (Alien Scout) glissé SOUS Alien Queen, face cachée ;
//   - ap010 Skulls for the Taking : allié vaincu glissé dessous ;
//   - ap011 Plasmacaster : attachement du Warlord avec ses compteurs « plasma » ;
//   - ap013 Thermal Target : attachement de rencontre sur l'identité ;
//   - ap009 / ap010 : les deux manigances annexes permanentes et leur menace.
import { describe, expect, it } from 'vitest'
import { carteSurTable as carte, cartesDessinees, dessinee, siege, tableAvec } from './plateau-de-test'

const IDENTITE = 1
const CIBLE = 2
const REINE = 10
const WARLORD = 11
const PLASMA = 12
const SCOUT_1 = 13
const SCOUT_2 = 14
const HIVE = 20
const SKULLS = 21
const CHAT = 22

const monde = () =>
  tableAvec(
    siege({
      area_hero: [
        carte(IDENTITE, '01001b', 'AlterEgo', 'Peter Parker'),
        carte(CIBLE, 'ap013', 'Attachment', 'Thermal Target', { bind_object_id: IDENTITE }),
      ],
    }),
    {
      area_villain: [
        carte(REINE, 'ap001a', 'EncounterVillain', 'Alien Queen', { info: { c_active: 1 } }),
        carte(SCOUT_1, 'ap101', 'Minion', 'Alien Scout', { bind_object_id: REINE, is_face_up: false }),
        carte(SCOUT_2, 'ap104', 'Minion', 'Alien Scout', { bind_object_id: REINE, is_face_up: false }),
        carte(WARLORD, 'ap002a', 'EncounterVillain', 'Predator Warlord'),
        carte(PLASMA, 'ap011', 'Attachment', 'Plasmacaster', { bind_object_id: WARLORD, info: { c_plasma: 3 } }),
      ],
      area_schemes_side: [
        carte(HIVE, 'ap009', 'SideScheme', 'Expanding Hive', { info: { k_threat: 2 } }),
        carte(SKULLS, 'ap010', 'SideScheme', 'Skulls for the Taking', { info: { k_threat: 4 } }),
        carte(CHAT, '01002', 'Ally', 'Black Cat', { bind_object_id: SKULLS, is_face_up: false }),
      ],
    }
  )

describe('deux vilains en jeu', () => {
  it('Alien Queen et Predator Warlord sont dessinés tous les deux', () => {
    expect(dessinee(monde(), REINE)).toBeDefined()
    expect(dessinee(monde(), WARLORD)).toBeDefined()
  })
})

describe('ap005a : le deck Xenomorph sous Alien Queen', () => {
  it('les Alien Scout glissés sous la Reine sont dessinés, juste derrière elle', () => {
    const vues = cartesDessinees(monde())
    const rang = (id: number) => vues.findIndex((c) => c.id === id)
    expect(dessinee(monde(), SCOUT_1)).toBeDefined()
    expect(dessinee(monde(), SCOUT_2)).toBeDefined()
    expect(rang(SCOUT_1)).toBeGreaterThan(rang(REINE))
    expect(rang(SCOUT_2)).toBeGreaterThan(rang(REINE))
  })
})

describe('ap011 Plasmacaster', () => {
  it('est dessiné, porté par le Warlord, avec ses 3 compteurs plasma', () => {
    expect(dessinee(monde(), PLASMA)).toBeDefined()
    expect(dessinee(monde(), PLASMA)?.portePar).toBe(WARLORD)
    expect(dessinee(monde(), PLASMA)?.compteurs.plasma).toBe(3)
  })
})

describe('ap013 Thermal Target', () => {
  it('est dessinée sur l identité', () => {
    expect(dessinee(monde(), CIBLE)).toBeDefined()
    expect(dessinee(monde(), CIBLE)?.portePar).toBe(IDENTITE)
  })
})

describe('ap009 / ap010 : manigances permanentes', () => {
  it('les deux sont dessinées avec leur menace', () => {
    expect(dessinee(monde(), HIVE)?.menace).toBe(2)
    expect(dessinee(monde(), SKULLS)?.menace).toBe(4)
  })

  it('ap010 : l allié glissé sous Skulls for the Taking est dessiné, derrière elle', () => {
    const vues = cartesDessinees(monde())
    const rang = (id: number) => vues.findIndex((c) => c.id === id)
    expect(dessinee(monde(), CHAT)).toBeDefined()
    expect(rang(CHAT)).toBeGreaterThan(rang(SKULLS))
  })
})
