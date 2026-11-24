// Ch'od (Starjammers, co001a) : ce que la table DESSINE (étape 8 bis de PROCESSUS-CARTE, leçon Contingency Plan).
//
// Cr'reee Captured (co011) glisse Cr'reee SOUS l'obligation, qui reste en jeu dans la zone des obligations du joueur ;
// Duel of Wits (co013) glisse une carte de la main SOUS la manigance annexe. Le joueur doit voir ce qui est retenu.
// Modèles : `corsair-plateau.test.ts` (manigance annexe) et `echo-photographic-reflexes` (zone du joueur).
import { describe, expect, it } from 'vitest'
import { carteSurTable, cartesDessinees, dessinee, siege, tableAvec } from './plateau-de-test'

const OBLIGATION = 10
const CRREEE = 11
const DUEL = 40
const GLISSEE = 41

const monde = () =>
  tableAvec(
    siege({
      area_hero: [carteSurTable(1, 'co001b', 'AlterEgo', "Ch'od")],
      obligations_area: [
        carteSurTable(OBLIGATION, 'co011', 'Obligation', "Cr'reee Captured"),
        carteSurTable(CRREEE, 'co002', 'Ally', "Cr'reee", {
          bind_object_id: OBLIGATION,
          is_face_up: false,
          visible_for_players: [],
        }),
      ],
    }),
    {
      area_schemes_side: [
        carteSurTable(DUEL, 'co013', 'SideScheme', 'Duel of Wits'),
        carteSurTable(GLISSEE, '01090', 'Resource', 'Strength', {
          bind_object_id: DUEL,
          is_face_up: false,
          visible_for_players: [],
        }),
      ],
    }
  )

describe("Cr'reee Captured, Cr'reee glissée sous l'obligation", () => {
  it("dessine l'obligation et la carte retenue, portée par elle", () => {
    expect(dessinee(monde(), OBLIGATION)).toBeDefined()
    expect(dessinee(monde(), CRREEE)).toBeDefined()
    expect(dessinee(monde(), CRREEE)?.portePar).toBe(OBLIGATION)
  })

  it("la montre face cachée, juste derrière l'obligation", () => {
    const vues = cartesDessinees(monde())
    const rang = (id: number) => vues.findIndex((c) => c.id === id)
    expect(rang(CRREEE)).toBe(rang(OBLIGATION) + 1)
    expect(dessinee(monde(), CRREEE)?.facedown).toBe(true)
  })
})

describe('Duel of Wits, carte glissée dessous', () => {
  it('dessine la manigance et la carte retenue, portée par elle', () => {
    expect(dessinee(monde(), DUEL)).toBeDefined()
    expect(dessinee(monde(), GLISSEE)).toBeDefined()
    expect(dessinee(monde(), GLISSEE)?.portePar).toBe(DUEL)
  })

  it('la montre face cachée, juste derrière la manigance', () => {
    const vues = cartesDessinees(monde())
    const rang = (id: number) => vues.findIndex((c) => c.id === id)
    expect(rang(GLISSEE)).toBe(rang(DUEL) + 1)
    expect(dessinee(monde(), GLISSEE)?.facedown).toBe(true)
  })
})
