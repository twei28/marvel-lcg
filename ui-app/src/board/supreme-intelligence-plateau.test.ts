// Supreme Intelligence (scénario 5 de Galactic Storm, Kajislav, lot GS-8) et modulaires du bloc : ce que le
// plateau DESSINE. PROCESSUS-CARTE étape 8 bis, pour les cartes qui changent ce qu'on voit :
//  - gs200 Holding Tank s'attache au méchant (Setup de 1A) et porte des pions « integrity » ;
//  - gs201 Genetic Augmentation s'attache à un sbire KREE ;
//  - gs218 Manipulated Memories s'attache à l'identité du joueur ;
//  - gs222a Nega-Bomb est un complot annexe en jeu dès la mise en place, avec des pions « time ».
//
// Les formes reprennent l'état mesuré par les cas `[gs8]` de `tools/cas/gs8_supreme_intelligence.py`
// (journal du harnais, 20/10/2026) : « Supreme Intelligence s'équipe de Holding Tank », 7 pions
// integrity (1 joueur) ; Genetic Augmentation accrochée à Kree Infantry ; Manipulated Memories accrochée à
// Spider-Man ; Nega-Bomb 8 menaces et 4 pions time.
import { describe, expect, it } from 'vitest'
import { catalogueVide } from './catalogue'
import { toScanCard } from './card-model'
import { carteSurTable, cartesDessinees, dessinee, siege, tableAvec } from './plateau-de-test'
import type { World } from './world'

const MECHANT = 50
const TANK = 90
const INFANTRY = 55
const AUGMENTATION = 53
const HEROS = 1
const MEMOIRES = 102
const NEGA = 82

const monde = (): World =>
  tableAvec(
    siege({
      area_hero: [
        carteSurTable(HEROS, '01001a', 'Hero', 'Spider-Man'),
        carteSurTable(MEMOIRES, 'gs218', 'Attachment', 'Manipulated Memories', { bind_object_id: HEROS }),
      ],
    }),
    {
      area_villain: [
        carteSurTable(MECHANT, 'gs195', 'EncounterVillain', 'Supreme Intelligence', {
          info: { attack: 1, scheme: 2, health: 13, max_health: 13, is_infinite_health: 0 },
        }),
        carteSurTable(TANK, 'gs200', 'Attachment', 'Holding Tank', {
          bind_object_id: MECHANT,
          info: { c_integrity: 7, c_integrity_printed: 7 },
        }),
      ],
      area_schemes_side: [
        carteSurTable(NEGA, 'gs222a', 'EncounterSideScheme', 'Nega-Bomb', { info: { k_threat: 8, c_time: 4 } }),
      ],
    } as Partial<World>
  )

// Le sbire et son attachement vivent dans la zone des ennemis engagés du joueur.
const mondeAvecSbire = (): World => {
  const w = monde()
  const joueur = w.players[0] as unknown as { engaged_enemies: unknown[] }
  joueur.engaged_enemies = [
    carteSurTable(INFANTRY, 'gs202', 'Minion', 'Kree Infantry', { info: { health: 7, max_health: 7 } }),
    carteSurTable(AUGMENTATION, 'gs201', 'Attachment', 'Genetic Augmentation', { bind_object_id: INFANTRY }),
  ]
  return w
}

const contexte = () => ({ playerId: 0, actives: new Set<number>(), catalogue: catalogueVide })
const scan = (world: World, id: number) => {
  const brute = [...(world.area_villain ?? []), ...(world.area_schemes_side ?? [])].find((c) => c.id === id)
  if (!brute) throw new Error(`carte ${id} absente`)
  return toScanCard(brute, contexte())
}

describe('Supreme Intelligence : ce que ses cartes dessinent', () => {
  it('Holding Tank est dessiné, porté par le méchant', () => {
    expect(dessinee(monde(), TANK)).toBeDefined()
    expect(dessinee(monde(), TANK)?.portePar).toBe(MECHANT)
  })

  it('Holding Tank affiche ses pions « intégrité » en français', () => {
    const compteurs = scan(monde(), TANK).counters ?? []
    expect(compteurs.map((c) => [c.label, c.value])).toContainEqual(['intégrité', 7])
  })

  it('Manipulated Memories est dessinée, portée par l’identité', () => {
    expect(dessinee(monde(), MEMOIRES)).toBeDefined()
    expect(dessinee(monde(), MEMOIRES)?.portePar).toBe(HEROS)
  })

  it('Genetic Augmentation est dessinée, portée par le sbire KREE', () => {
    expect(dessinee(mondeAvecSbire(), INFANTRY)).toBeDefined()
    expect(dessinee(mondeAvecSbire(), AUGMENTATION)).toBeDefined()
    expect(dessinee(mondeAvecSbire(), AUGMENTATION)?.portePar).toBe(INFANTRY)
  })

  it('la Nega-Bomb est un complot annexe dessiné, avec ses pions « temps »', () => {
    expect(dessinee(monde(), NEGA)).toBeDefined()
    const compteurs = scan(monde(), NEGA).counters ?? []
    expect(compteurs.map((c) => [c.label, c.value])).toContainEqual(['temps', 4])
  })

  it('TEMOIN : les attachements ne sont pas des racines séparées, la Nega-Bomb l’est', () => {
    const racines = cartesDessinees(mondeAvecSbire()).filter((c) => c.portePar === 0).map((c) => c.id)
    expect(racines).not.toContain(TANK)
    expect(racines).not.toContain(MEMOIRES)
    expect(racines).not.toContain(AUGMENTATION)
    expect(racines).toContain(NEGA)
  })
})
