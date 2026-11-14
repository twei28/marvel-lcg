// Major Victory (Vance Astro, mv001a/b) : ce que la table DESSINE (étape 8 bis de PROCESSUS-CARTE, leçon Contingency Plan).
//
// Trois cartes changent ce qu'on VOIT :
//  - mv012 Damaged Containment Suit glisse Containment Suit (mv004) FACE CACHÉE sous l'obligation (`PlaceCardHere`) ;
//  - mv001a Shield Toss et mv013 Michael Korvac (qui révèle Korvac's Future, un complot annexe qui entre en jeu) déplacent des cartes
//    entre zones : le bouclier (mv002) est posé sur Major Victory, Korvac's Future est un complot annexe de la zone des manigances.
// Le moteur émet une carte glissée à la suite de son hôte, liée par `bind_object_id` (modèle `chod-plateau.test.ts` et
// `attachement-en-chaine.test.ts`) : une carte non dessinée serait invisible alors que sa règle s'applique.
import { describe, expect, it } from 'vitest'
import { carteSurTable, cartesDessinees, dessinee, siege, tableAvec } from './plateau-de-test'

const VANCE = 1
const OBLIGATION = 2
const COSTUME = 3
const MAJOR_VICTORY = 4
const BOUCLIER = 5
const FUTURE = 6
const KORVAC = 7

const monde = () =>
  tableAvec(
    siege({
      area_hero: [carteSurTable(VANCE, 'mv001b', 'AlterEgo', 'Vance Astro')],
      // Un sbire ENGAGÉ avec le joueur vit dans `engaged_enemies` de son siège (pas dans une zone du monde).
      engaged_enemies: [carteSurTable(KORVAC, 'mv013', 'Minion', 'Michael Korvac')],
      obligations_area: [
        carteSurTable(OBLIGATION, 'mv012', 'Obligation', 'Damaged Containment Suit'),
        carteSurTable(COSTUME, 'mv004', 'Upgrade', 'Containment Suit', {
          bind_object_id: OBLIGATION,
          is_face_up: false,
          visible_for_players: [],
        }),
      ],
    }),
    {
      area_schemes_side: [carteSurTable(FUTURE, 'mv014', 'SideScheme', "Korvac's Future")],
    },
  )

const mondeHeros = () =>
  tableAvec(
    siege({
      area_hero: [
        carteSurTable(MAJOR_VICTORY, 'mv001a', 'Hero', 'Major Victory'),
        carteSurTable(BOUCLIER, 'mv002', 'Upgrade', "Captain America's Shield", { bind_object_id: MAJOR_VICTORY }),
      ],
    }),
  )

describe('Damaged Containment Suit, Containment Suit glissé sous l\'obligation', () => {
  it('dessine l\'obligation et la carte retenue, portée par elle', () => {
    expect(dessinee(monde(), OBLIGATION)).toBeDefined()
    expect(dessinee(monde(), COSTUME)).toBeDefined()
    expect(dessinee(monde(), COSTUME)?.portePar).toBe(OBLIGATION)
  })

  it('la montre face cachée, juste derrière l\'obligation', () => {
    const vues = cartesDessinees(monde())
    const rang = (id: number) => vues.findIndex((c) => c.id === id)
    expect(rang(COSTUME)).toBe(rang(OBLIGATION) + 1)
    expect(dessinee(monde(), COSTUME)?.facedown).toBe(true)
  })
})

describe('Korvac et Korvac\'s Future', () => {
  it('dessine le sbire Michael Korvac et le complot annexe Korvac\'s Future', () => {
    expect(dessinee(monde(), KORVAC)).toBeDefined()
    expect(dessinee(monde(), FUTURE)).toBeDefined()
  })
})

describe('Major Victory et son bouclier', () => {
  it('dessine le bouclier posé sur Major Victory, juste derrière lui', () => {
    const vues = cartesDessinees(mondeHeros())
    const rang = (id: number) => vues.findIndex((c) => c.id === id)
    expect(dessinee(mondeHeros(), BOUCLIER)?.portePar).toBe(MAJOR_VICTORY)
    expect(rang(BOUCLIER)).toBe(rang(MAJOR_VICTORY) + 1)
  })
})
