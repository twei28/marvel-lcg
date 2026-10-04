// Les cartes glissées face cachée sous une OBLIGATION doivent être dessinées
// (étape 8 bis de PROCESSUS-CARTE, leçon Contingency Plan).
//
// Triumph Probation (`65015`, pack custom Wave, 22/09/2026) cherche Wave's
// Swords et Wave's Crown dans la main/le deck/la défausse/la zone de jeu du
// joueur et les place face cachée dessous : le moteur les émet dans
// `obligations_area` à la suite de l'obligation, liées par `bind_object_id`
// — même mécanisme que The Mother of Night / Highway Robbery sous une
// manigance annexe (`mere-de-la-nuit-cartes-dessous.test.ts`), mais sous une
// OBLIGATION. Réserve laissée ouverte lors du premier passage (le cas moteur
// `wave_triumph_probation_cycle_complet` prouve le glissement côté règles,
// jamais vu à l'écran avant ce cas).
import { describe, expect, it } from 'vitest'
import { carteSurTable, cartesDessinees, dessinee, siege, tableAvec } from './plateau-de-test'

const OBLIGATION = 40
const SWORDS = 41
const CROWN = 42

const monde = () =>
  tableAvec(
    siege({
      area_hero: [carteSurTable(1, '65001b', 'AlterEgo', 'Pearl Pangan')],
      obligations_area: [
        carteSurTable(OBLIGATION, '65015', 'Obligation', 'Triumph Probation'),
        carteSurTable(SWORDS, '65009', 'Upgrade', "Wave's Swords", {
          bind_object_id: OBLIGATION,
          is_face_up: false,
          visible_for_players: [],
        }),
        carteSurTable(CROWN, '65010', 'Upgrade', "Wave's Crown", {
          bind_object_id: OBLIGATION,
          is_face_up: false,
          visible_for_players: [],
        }),
      ],
    })
  )

describe('Triumph Probation, cartes glissées dessous', () => {
  it('dessine l’obligation', () => {
    expect(dessinee(monde(), OBLIGATION)).toBeDefined()
  })

  it('dessine les deux cartes glissées, portées par l’obligation', () => {
    expect(dessinee(monde(), SWORDS)).toBeDefined()
    expect(dessinee(monde(), CROWN)).toBeDefined()
    expect(dessinee(monde(), SWORDS)?.portePar).toBe(OBLIGATION)
    expect(dessinee(monde(), CROWN)?.portePar).toBe(OBLIGATION)
  })

  it('les montre face cachée, juste derrière l’obligation, même pour leur propriétaire', () => {
    // Différence de fond avec Wave's Crown en jeu normal (`TuckCardUnderHere`
    // avec `peek=True`, la carte y reste visible à son propriétaire) : ICI
    // c'est Triumph Probation qui glisse « facedown » sans exception de
    // visibilité — `65010.py` documente ce contraste en tête de fichier.
    const vues = cartesDessinees(monde())
    const rang = (id: number) => vues.findIndex((c) => c.id === id)
    expect(rang(SWORDS)).toBe(rang(OBLIGATION) + 1)
    expect(rang(CROWN)).toBe(rang(OBLIGATION) + 2)
    expect(dessinee(monde(), SWORDS)?.facedown).toBe(true)
    expect(dessinee(monde(), SWORDS)?.peeking).toBe(false)
    expect(dessinee(monde(), CROWN)?.facedown).toBe(true)
    expect(dessinee(monde(), CROWN)?.peeking).toBe(false)
  })

  it('les trois cartes sont dessinées ensemble, sans en perdre une', () => {
    // `obligations_area` rejoint `area_hero`/`supports` dans UN SEUL
    // emplacement affiché (« terrain-soutien », voir zones.ts), aux côtés de
    // l'identité elle-même (id 1) — ce n'est pas une zone à part sur le
    // plateau.
    const vues = cartesDessinees(monde()).filter((c) => c.zone === 'terrain-soutien')
    expect(vues.map((c) => c.id).sort((a, b) => a - b)).toEqual([1, OBLIGATION, SWORDS, CROWN].sort((a, b) => a - b))
  })
})
