// Paibok (scénario 3 de Skrull Menace, Kajislav) et New Revengers : ce que le plateau DESSINE.
// PROCESSUS-CARTE étape 8 bis, pour les cartes qui changent ce qu'on voit : jetons de maîtrise
// sur Paibok, attachements POWER SKRULL et Captain Paibok accrochés à Paibok, condition accrochée
// à l'identité du joueur, jetons d'absorption sur Asti.
//
// L'état est CAPTURÉ sur le moteur le 15/10/2026 (`tools/sonde_campagne.py` sur `.game-src`,
// scénario sk_paibok, deck spider_man) après ces commandes Puzzle : Remove des 4 POWER SKRULL,
// PutIntoPlay sk148 (Electricity Projection) et sk151 (Metallic Skin), ChangeForm 01001b (héros),
// PutIntoPlay sk147 (Distracted) et sk146 (Captain Paibok), PutIntoPlay sk163 (Asti),
// Counter sk163 absorption 2, Counter sk141 mastery 1 (1 jeton posé par la mise en place + 1).
// Relevé (id = identifiant d'objet du moteur) :
//
//   area_villain      : id=50 sk141 EncounterVillain {c_mastery:2, toughness:1, retaliate:1, attack:4}
//                       id=52 tough StatusCard bind=50 ; id=93 sk148, id=94 sk151, id=53 sk146 (bind=50)
//   area_schemes_main : id=48 sk144b MainScheme
//   player.area_hero  : id=1 01001a Hero ; id=55 sk147 Attachment bind=1 (Distracted)
//   engaged_enemies   : id=85 sk163 Minion {c_absorption:2}
import { describe, expect, it } from 'vitest'
import { catalogueVide } from './catalogue'
import { toScanCard } from './card-model'
import { carteSurTable, cartesDessinees, dessinee, siege, tableAvec } from './plateau-de-test'
import type { World, WorldCard } from './world'

const PAIBOK = 50
const TENACE = 52
const ELECTRICITY = 93
const METALLIC = 94
const CAPTAIN = 53
const COMPLOT = 48
const HEROS = 1
const DISTRACTED = 55
const ASTI = 85

const paibok = (): WorldCard =>
  carteSurTable(PAIBOK, 'sk141', 'EncounterVillain', 'Paibok', {
    info: { max_health: 13, health: 13, toughness: 1, retaliate: 1, attack: 4, c_mastery: 2 },
  })

const monde = (): World =>
  tableAvec(
    siege({
      area_hero: [
        carteSurTable(HEROS, '01001a', 'Hero', 'Spider-Man'),
        carteSurTable(DISTRACTED, 'sk147', 'Attachment', 'Distracted', { bind_object_id: HEROS }),
      ],
      engaged_enemies: [
        carteSurTable(ASTI, 'sk163', 'Minion', 'Asti the All-Seeing', {
          info: { max_health: 4, health: 4, c_absorption: 2 },
        }),
      ],
    }),
    {
      area_villain: [
        paibok(),
        carteSurTable(TENACE, 'tough', 'StatusCard', 'Tough', { bind_object_id: PAIBOK }),
        carteSurTable(ELECTRICITY, 'sk148', 'Attachment', 'Electricity Projection', { bind_object_id: PAIBOK }),
        carteSurTable(METALLIC, 'sk151', 'Attachment', 'Metallic Skin', { bind_object_id: PAIBOK }),
        carteSurTable(CAPTAIN, 'sk146', 'Attachment', 'Captain Paibok', { bind_object_id: PAIBOK }),
      ],
      area_schemes_main: [carteSurTable(COMPLOT, 'sk144b', 'MainScheme', 'Power Skrull Engineering')],
    } as Partial<World>
  )

const contexte = () => ({ playerId: 0, actives: new Set<number>(), catalogue: catalogueVide })
const scan = (carte: WorldCard) => toScanCard(carte, contexte())

describe('Paibok : ce que ses cartes dessinent', () => {
  // sk141 / sk144a / sk145 : les jetons de maîtrise sont publiés sous `c_mastery` et affichés.
  it('Paibok montre ses 2 jetons de maîtrise', () => {
    const jetons = scan(paibok()).counters?.find((c) => c.cle === 'mastery')
    expect(jetons?.value).toBe(2)
  })

  // sk148 / sk151 / sk146 : attachés à Paibok, ils sont dessinés portés par lui.
  it('Electricity Projection, Metallic Skin et Captain Paibok sont dessinés attachés à Paibok', () => {
    for (const id of [ELECTRICITY, METALLIC, CAPTAIN]) {
      expect(dessinee(monde(), id)).toBeDefined()
      expect(dessinee(monde(), id)?.portePar).toBe(PAIBOK)
    }
  })

  // sk147 : la condition est attachée à l'IDENTITÉ du joueur, pas posée seule sur la table.
  it("Distracted est dessinée attachée à l'identité du joueur", () => {
    expect(dessinee(monde(), DISTRACTED)).toBeDefined()
    expect(dessinee(monde(), DISTRACTED)?.portePar).toBe(HEROS)
  })

  // sk163 : jetons d'absorption.
  it('Asti montre ses 2 jetons d’absorption', () => {
    const jetons = scan(
      carteSurTable(ASTI, 'sk163', 'Minion', 'Asti the All-Seeing', { info: { max_health: 4, health: 4, c_absorption: 2 } })
    ).counters?.find((c) => c.cle === 'absorption')
    expect(jetons?.value).toBe(2)
  })

  // Témoin : Paibok, le complot et Asti sont des racines ; les attachements n'en sont pas.
  it('TEMOIN : Paibok, le complot principal et Asti sont des racines, pas les attachements', () => {
    const racines = cartesDessinees(monde())
      .filter((c) => c.portePar === 0)
      .map((c) => c.id)
    expect(racines).toContain(PAIBOK)
    expect(racines).toContain(COMPLOT)
    expect(racines).toContain(ASTI)
    for (const id of [ELECTRICITY, METALLIC, CAPTAIN, DISTRACTED]) expect(racines).not.toContain(id)
  })

  // Témoin : sans jeton, aucun compteur « mastery » n'est affiché.
  it('TEMOIN : sans jeton publié, aucun compteur maîtrise', () => {
    const sans = carteSurTable(PAIBOK, 'sk141', 'EncounterVillain', 'Paibok', { info: { max_health: 13, health: 13 } })
    expect(scan(sans).counters?.find((c) => c.cle === 'mastery')).toBeUndefined()
  })
})
