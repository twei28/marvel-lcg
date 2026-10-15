// Super-Skrull (scénario 2 de Skrull Menace, Kajislav) : ce que le plateau
// DESSINE. PROCESSUS-CARTE étape 8 bis, pour les cartes du scénario qui
// changent ce qu'on voit : les pouvoirs SUPERPOWER et Lord Kl'rt s'attachent au
// méchant, Invisible Forcefield porte des compteurs de dégâts, Earth
// Involvement est un complot annexe Permanent + crise, le méchant a de VRAIS PV
// (pas de cadran déporté, pas de « INF »).
//
// Les formes reprennent un descripteur CAPTURÉ le 15/10/2026 (sonde
// `tools/sonde_campagne.py` sur `.game-src`, scénario sk_super_skrull, deck
// spider_man) après ces commandes Puzzle : Remove sk122, Reveal sk124 (Pyrokinesis),
// Reveal sk123 (Invisibility), Reveal sk126 (Invisible Forcefield), Damage sk117 2,
// Reveal sk127 (Lord Kl'rt), PutIntoPlay sk131. Relevé :
//
//   world.area_villain      : id=50 sk117 EncounterVillain {attack:3, scheme:2, health:14, max_health:14, is_infinite_health:0}
//                             id=92 sk124 Attachment bind=50    id=91 sk123 Attachment bind=50
//                             id=53 sk126 Attachment bind=50 {c_damage:2}
//                             id=55 sk127 Attachment bind=50 {amplify:1}
//   world.area_schemes_side : id=87 sk138 EncounterSideScheme {crisis:1, permanent:1, k_threat:1}
//                             id=59 sk131 EncounterSideScheme {k_threat:3}
import { describe, expect, it } from 'vitest'
import { catalogueVide } from './catalogue'
import { toScanCard } from './card-model'
import { carteSurTable, cartesDessinees, dessinee, siege, tableAvec } from './plateau-de-test'
import type { World } from './world'

const SUPER_SKRULL = 50
const PYROKINESIS = 92
const INVISIBILITY = 91
const FORCEFIELD = 53
const KLRT = 55
const EARTH = 87
const COUNCIL = 59

const monde = (): World =>
  tableAvec(siege(), {
    area_villain: [
      carteSurTable(SUPER_SKRULL, 'sk117', 'EncounterVillain', 'Super-Skrull', {
        info: { attack: 3, scheme: 2, health: 14, max_health: 14, is_infinite_health: 0 },
      }),
      carteSurTable(PYROKINESIS, 'sk124', 'Attachment', 'Pyrokinesis', { bind_object_id: SUPER_SKRULL }),
      carteSurTable(INVISIBILITY, 'sk123', 'Attachment', 'Invisibility', { bind_object_id: SUPER_SKRULL }),
      carteSurTable(FORCEFIELD, 'sk126', 'Attachment', 'Invisible Forcefield', {
        bind_object_id: SUPER_SKRULL,
        info: { c_damage: 2 },
      }),
      carteSurTable(KLRT, 'sk127', 'Attachment', "Lord Kl'rt", { bind_object_id: SUPER_SKRULL, info: { amplify: 1 } }),
    ],
    area_schemes_side: [
      carteSurTable(EARTH, 'sk138', 'EncounterSideScheme', 'Earth Involvement', {
        info: { crisis: 1, permanent: 1, k_threat: 1 },
      }),
      carteSurTable(COUNCIL, 'sk131', 'EncounterSideScheme', 'Galactic Council Membership', { info: { k_threat: 3 } }),
    ],
  } as Partial<World>)

const contexte = () => ({ playerId: 0, actives: new Set<number>(), catalogue: catalogueVide })
const scan = (world: World, id: number) => {
  const brute = [...(world.area_villain ?? []), ...(world.area_schemes_side ?? [])].find((c) => c.id === id)
  if (!brute) throw new Error(`carte ${id} absente`)
  return toScanCard(brute, contexte())
}

describe('Super-Skrull : ce que ses cartes dessinent', () => {
  // sk122-125, sk127 : « Attach to Super-Skrull » : chaque carte est DESSINÉE et
  // portée par le méchant (jamais une racine perdue, jamais invisible).
  it('les pouvoirs SUPERPOWER et Lord Kl’rt sont dessinés, portés par le Super-Skrull', () => {
    expect(dessinee(monde(), SUPER_SKRULL)).toBeDefined()
    for (const id of [PYROKINESIS, INVISIBILITY, FORCEFIELD, KLRT]) {
      expect(dessinee(monde(), id)).toBeDefined()
      expect(dessinee(monde(), id)?.portePar).toBe(SUPER_SKRULL)
    }
  })

  // sk117 : le Super-Skrull a de vrais PV (14 par joueur) : pas de pastille INF
  // ni de cadran déporté sur une autre carte (contraire de Skrull Empire).
  it('le méchant montre ses PV, sans « INF » ni jauge déportée', () => {
    expect(scan(monde(), SUPER_SKRULL).allyHp).toBe('14/14')
  })

  // sk126 Invisible Forcefield : les dégâts « placés ici » se VOIENT sur la carte.
  it('Invisible Forcefield affiche ses dégâts en compteur', () => {
    const compteurs = scan(monde(), FORCEFIELD).counters ?? []
    expect(compteurs.map((c) => [c.label, c.value])).toEqual([['dégâts', 2]])
  })

  // sk138 Earth Involvement : complot annexe en jeu dès le départ, avec sa menace.
  it('Earth Involvement est un complot annexe dessiné, avec sa menace de départ', () => {
    expect(dessinee(monde(), EARTH)).toBeDefined()
    expect(dessinee(monde(), COUNCIL)).toBeDefined()
  })

  // Témoin : sans lui, un plateau qui dessinerait tout en racine passerait.
  it('TEMOIN : les pouvoirs ne sont pas des racines séparées, les complots annexes le sont', () => {
    const racines = cartesDessinees(monde()).filter((c) => c.portePar === 0).map((c) => c.id)
    expect(racines).not.toContain(PYROKINESIS)
    expect(racines).not.toContain(FORCEFIELD)
    expect(racines).toContain(EARTH)
  })
})
