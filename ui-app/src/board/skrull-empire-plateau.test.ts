// Skrull Empire (scénario 1 de Skrull Menace, Kajislav) : ce que le plateau
// DESSINE. PROCESSUS-CARTE étape 8 bis, pour les cartes du scénario qui
// changent ce qu'on voit (environnements, sbire créé par Impostor, allié placé
// sous un complot annexe, méchant sans cadran de PV).
//
// Les formes reprennent un descripteur CAPTURÉ le 15/10/2026 (sonde sur
// `.game-src`, scénario sk_skrull_empire, deck spider_man) après ces commandes
// Puzzle : Remove des 9 planètes, ChangeForm 01001b, PutIntoPlay sk090,
// PutIntoPlay 04014, Reveal sk098 (Impostor), PutIntoPlay sk099, Reveal sk115
// (Hijacked), Counter sk086 damage 5. Relevé :
//
//   world.area_villain      : id=94  sk070 EncounterVillain {is_infinite_health:1, pv_sur_environnement:1}
//   world.area_environment  : id=102 sk086 Environment {cadran_pv:1, health:9, max_health:14}
//                             id=113 sk090 Environment (Hy'lt Minor)
//   world.area_schemes_side : id=91  sk115 EncounterSideScheme {k_threat:4}
//                             id=38  01084 Ally bind=91 (l'allié placé dessous)
//   joueur.engaged_enemies  : id=114 skrull_minion Minion pic_id=04014 « U.S. Agent » {max_health:5}
//                             id=52  sk098 Attachment bind=114 (Impostor)
//                             id=53  sk099 Minion (Intelligentsia)
import { describe, expect, it } from 'vitest'
import { catalogueVide } from './catalogue'
import { toScanCard } from './card-model'
import { carteSurTable, cartesDessinees, dessinee, siege, tableAvec } from './plateau-de-test'
import type { World } from './world'

const DORREK = 94
const EMPIRE = 102
const PLANETE = 113
const HIJACKED = 91
const ALLIE_SOUS = 38
const AGENT = 114
const IMPOSTOR = 52
const INTELLIGENTSIA = 53

const monde = (): World =>
  tableAvec(
    siege({
      engaged_enemies: [
        carteSurTable(AGENT, 'skrull_minion', 'Minion', 'U.S. Agent', {
          pic_id: '04014',
          info: { max_health: 5, health: 5 },
        }),
        carteSurTable(IMPOSTOR, 'sk098', 'Attachment', 'Impostor', { bind_object_id: AGENT }),
        carteSurTable(INTELLIGENTSIA, 'sk099', 'Minion', 'Intelligentsia', {
          info: { max_health: 5, health: 5 },
        }),
      ],
    }),
    {
      area_villain: [
        carteSurTable(DORREK, 'sk070', 'EncounterVillain', 'Emperor Dorrek I', {
          info: { is_infinite_health: 1, health: 1, max_health: 0, pv_sur_environnement: 1 },
        }),
      ],
      area_environment: [
        carteSurTable(EMPIRE, 'sk086', 'Environment', 'Skrull Empire', {
          info: { cadran_pv: 1, health: 9, max_health: 14, k_damage: 5 },
        }),
        carteSurTable(PLANETE, 'sk090', 'Environment', "Hy'lt Minor"),
      ],
      area_schemes_side: [
        carteSurTable(HIJACKED, 'sk115', 'EncounterSideScheme', 'Hijacked', { info: { k_threat: 4 } }),
        carteSurTable(ALLIE_SOUS, '01084', 'Ally', 'Nick Fury', { bind_object_id: HIJACKED }),
      ],
    } as Partial<World>
  )

const contexte = () => ({ playerId: 0, actives: new Set<number>(), catalogue: catalogueVide })
const scan = (world: World, id: number) => {
  const brute = [
    ...(world.area_villain ?? []),
    ...(world.area_environment ?? []),
  ].find((c) => c.id === id)
  if (!brute) throw new Error(`carte ${id} absente`)
  return toScanCard(brute, contexte())
}

describe('Skrull Empire : ce que ses cartes dessinent', () => {
  // sk086 : le cadran de PV est sur l'environnement, pas sur le méchant.
  it("l'environnement montre le cadran, le méchant ne dit pas INF", () => {
    expect(scan(monde(), EMPIRE).allyHp).toBe('9/14')
    expect(scan(monde(), DORREK).allyHp).toBeUndefined()
    expect(scan(monde(), DORREK).jauge).toBeUndefined()
  })

  // sk089-097 : une planète est une carte Environnement posée dans sa zone.
  it('le méchant, l’environnement et la planète sont sur la table', () => {
    for (const id of [DORREK, EMPIRE, PLANETE]) expect(dessinee(monde(), id)).toBeDefined()
  })

  // sk098 Impostor : l'allié devient un sbire engagé qui garde le visuel de
  // l'allié (pic_id 04014), et Impostor est accroché à lui.
  it("Impostor est dessiné attaché au sbire, qui garde l'image de l'allié", () => {
    expect(dessinee(monde(), IMPOSTOR)?.portePar).toBe(AGENT)
    expect(dessinee(monde(), AGENT)?.codeCarte).toBe('skrull_minion')
  })

  // sk115 Hijacked : l'allié placé dessous est dessiné sous le complot annexe.
  it("l'allié placé sous Hijacked est dessiné porté par le complot", () => {
    expect(dessinee(monde(), HIJACKED)).toBeDefined()
    expect(dessinee(monde(), ALLIE_SOUS)?.portePar).toBe(HIJACKED)
  })

  // Témoin : sans lui, un plateau qui dessinerait tout en racine passerait.
  it("TEMOIN : l'allié placé dessous n'est pas une racine séparée, Intelligentsia l'est", () => {
    const racines = cartesDessinees(monde()).filter((c) => c.portePar === 0).map((c) => c.id)
    expect(racines).not.toContain(ALLIE_SOUS)
    expect(racines).toContain(INTELLIGENTSIA)
  })
})
