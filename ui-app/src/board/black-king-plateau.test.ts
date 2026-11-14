// Black King (Hellfire Hunt, Dipsome, `hf`, scénario 2) : ce que la table DESSINE (étape 8 bis de PROCESSUS-CARTE).
//
// Trois choses visibles changent dans ce scénario :
//   - hf206 Captured by Hellfire! cache FACE CACHÉE sous elle un captif par joueur (`PlaceCardHere`) : le joueur doit voir
//     que des mutants sont retenus et combien (modèle `corsair-plateau`, Slave Pits, `area_schemes_side`) ;
//   - hf207a / hf207b Black King : attachement Permanent posé sur Sebastian Shaw ;
//   - les compteurs « énergie » (Absorb) posés sur Shaw, lisibles sur la carte du vilain.
// Le moteur émet les cartes glissées à la suite de leur hôte, liées par `bind_object_id`.
import { describe, expect, it } from 'vitest'
import { carteSurTable, cartesDessinees, dessinee, siege, tableAvec } from './plateau-de-test'

const IDENTITE = 1
const SHAW = 10
const ROI_NOIR = 11
const CAPTURE = 40
const CAPTIF_1 = 41
const CAPTIF_2 = 42
const COMPLOT = 50

const monde = () =>
  tableAvec(
    siege({ area_hero: [carteSurTable(IDENTITE, '01001b', 'AlterEgo', 'Peter Parker')] }),
    {
      area_villain: [
        carteSurTable(SHAW, 'hf201', 'EncounterVillain', 'Sebastian Shaw', { info: { c_energy: 5 } }),
        carteSurTable(ROI_NOIR, 'hf207a', 'Attachment', 'Black King', { bind_object_id: SHAW }),
      ],
      area_schemes_main: [carteSurTable(COMPLOT, 'hf204b', 'MainScheme', 'Jailbreak at the Hellfire Club', { info: { k_threat: 3 } })],
      area_schemes_side: [
        carteSurTable(CAPTURE, 'hf206', 'SideScheme', 'Captured by Hellfire!', { info: { k_threat: 5 } }),
        carteSurTable(CAPTIF_1, 'hf208', 'Ally', 'Dust', { bind_object_id: CAPTURE, is_face_up: false, visible_for_players: [] }),
        carteSurTable(CAPTIF_2, 'hf210', 'Ally', 'Surge', { bind_object_id: CAPTURE, is_face_up: false, visible_for_players: [] }),
      ],
    }
  )

describe('hf206 Captured by Hellfire! : les captifs cachés dessous', () => {
  it('dessine la manigance annexe avec ses 5 menaces', () => {
    expect(dessinee(monde(), CAPTURE)).toBeDefined()
    expect(dessinee(monde(), CAPTURE)?.menace).toBe(5)
  })

  it('dessine chaque captif glissé dessous, juste derrière elle, face cachée (dos de carte pour le joueur)', () => {
    const vues = cartesDessinees(monde())
    const rang = (id: number) => vues.findIndex((c) => c.id === id)
    expect(dessinee(monde(), CAPTIF_1)).toBeDefined()
    expect(dessinee(monde(), CAPTIF_2)).toBeDefined()
    expect(rang(CAPTIF_1)).toBeGreaterThan(rang(CAPTURE))
    expect(rang(CAPTIF_2)).toBeGreaterThan(rang(CAPTURE))
    expect(dessinee(monde(), CAPTIF_1)?.facedown).toBe(true)
  })
})

describe('hf207a Black King et les compteurs d énergie de Shaw', () => {
  it('dessine Black King, attaché à Sebastian Shaw', () => {
    expect(dessinee(monde(), ROI_NOIR)).toBeDefined()
    expect(dessinee(monde(), ROI_NOIR)?.portePar).toBe(SHAW)
  })

  it('dessine les 5 compteurs d énergie sur Shaw', () => {
    expect(dessinee(monde(), SHAW)?.compteurs.energy).toBe(5)
  })

  it('dessine le complot principal avec la menace convertie', () => {
    expect(dessinee(monde(), COMPLOT)?.menace).toBe(3)
  })
})
