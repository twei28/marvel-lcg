// Sets modulaires de Skrull Menace (Kajislav) : Shaper of Worlds, ensembles d'Elites (Crusader, Jazinda,
// Skymax, War Skrull, Xavin), Standard / Expert Skrull. Ce que le plateau DESSINE.
// PROCESSUS-CARTE étape 8 bis, pour les cartes qui changent ce qu'on voit : attachements portés par un
// sbire ou par le méchant (Enemy Adaptation, Invisible Forcefield avec ses dégâts « placés ici »), sbire
// aux PV INFINIS (Shaper of Worlds, badge ∞), cartes mises de côté (Shaper et ses 4 fragments : absents de la table).
//
// L'état est CAPTURÉ sur le moteur le 15/10/2026 (`tools/sonde_campagne.py` sur `.game-src`, scénario
// d'essai sk_essai_modulaires, deck spider_man, descripteur sans erreur) après ces commandes Puzzle :
// ChangeForm 01001b (héros), EmptyEncounterDeck, PutIntoPlay sk113, Reveal sk232, PutIntoPlay sk251,
// Counter sk251 damage 3, Reveal sk229, PutIntoPlay 01002 (allié), PutIntoPlay sk243. Relevé (id = objet moteur) :
//
//   p0.engaged_enemies  : id=111 sk113 Minion {attack:3, scheme:3}   id=112 sk232 Attachment bind=111
//                         id=75  sk228 Minion {is_infinite_health:1, max_health:0, health:1, attack:3, scheme:2}
//   world.area_villain  : id=49 01094 EncounterVillain {max_health:14, health:14}
//                         id=113 sk251 Attachment bind=49 {c_damage:3}
//   world.area_schemes_side : id=114 sk229 {k_threat:2}   id=115 sk243 {k_threat:2}
//   world.area_set_aside    : sk230a..d Resource (4 fragments) ; sk228 y était avant la révélation de sk229
import { describe, expect, it } from 'vitest'
import { catalogueVide } from './catalogue'
import { toScanCard } from './card-model'
import { carteSurTable, cartesDessinees, dessinee, siege, tableAvec } from './plateau-de-test'
import type { World } from './world'

const RHINO = 49
const COMMANDER = 111
const ADAPTATION = 112
const SHAPER = 75
const FORCEFIELD = 113
const CREATION = 114
const ALLIANCE = 115
const FRAGMENT = 77

const monde = (): World =>
  tableAvec(
    siege({
      engaged_enemies: [
        carteSurTable(COMMANDER, 'sk113', 'Minion', 'Skrull Commander', {
          info: { max_health: 5, health: 5, attack: 3, scheme: 3 },
        }),
        carteSurTable(ADAPTATION, 'sk232', 'Attachment', 'Enemy Adaptation', { bind_object_id: COMMANDER }),
        carteSurTable(SHAPER, 'sk228', 'Minion', 'Shaper of Worlds', {
          info: { is_infinite_health: 1, max_health: 0, health: 1, attack: 3, scheme: 2 },
        }),
      ],
    }),
    {
      area_villain: [
        carteSurTable(RHINO, '01094', 'EncounterVillain', 'Rhino', { info: { max_health: 14, health: 14 } }),
        carteSurTable(FORCEFIELD, 'sk251', 'Attachment', 'Invisible Forcefield', {
          bind_object_id: RHINO,
          info: { c_damage: 3 },
        }),
      ],
      area_schemes_side: [
        carteSurTable(CREATION, 'sk229', 'EncounterSideScheme', 'Cosmic Cube Creation', { info: { k_threat: 2 } }),
        carteSurTable(ALLIANCE, 'sk243', 'EncounterSideScheme', 'Surprising Alliance', { info: { k_threat: 2 } }),
      ],
      area_set_aside: [carteSurTable(FRAGMENT, 'sk230a', 'Resource', 'Cosmic Cube Fragment', { is_face_up: false })],
    } as Partial<World>
  )

const contexte = () => ({ playerId: 0, actives: new Set<number>(), catalogue: catalogueVide })
const scan = (world: World, id: number) => {
  const brute = [
    ...(world.area_villain ?? []),
    ...(world.players?.[0]?.engaged_enemies ?? []),
  ].find((c) => c.id === id)
  if (!brute) throw new Error(`carte ${id} absente`)
  return toScanCard(brute, contexte())
}

describe('Sets modulaires Skrull Menace : ce que leurs cartes dessinent', () => {
  // sk232 : « Attach to a SKRULL minion » : l'attachement est dessiné, porté par le sbire.
  it('Enemy Adaptation est dessinée attachée au sbire SKRULL', () => {
    expect(dessinee(monde(), ADAPTATION)).toBeDefined()
    expect(dessinee(monde(), ADAPTATION)?.portePar).toBe(COMMANDER)
  })

  // sk251 : attaché à l'ennemi aux PV imprimés les plus hauts (le méchant), il porte les dégâts détournés.
  it('Invisible Forcefield est dessiné attaché au méchant et montre ses dégâts en compteur', () => {
    expect(dessinee(monde(), FORCEFIELD)?.portePar).toBe(RHINO)
    const compteurs = scan(monde(), FORCEFIELD).counters ?? []
    expect(compteurs.map((c) => [c.label, c.value])).toEqual([['dégâts', 3]])
  })

  // sk228 : PV infinis (badge ∞ du scan) : la pastille dit « INF », sans jauge.
  it('Shaper of Worlds montre « INF » et aucune jauge', () => {
    expect(scan(monde(), SHAPER).allyHp).toBe('∞')
    expect(scan(monde(), SHAPER).jauge).toBeUndefined()
  })

  // sk229 / sk243 : compléments annexes dessinés dans la zone des complots annexes.
  it('Cosmic Cube Creation et Surprising Alliance sont des complots annexes dessinés', () => {
    for (const id of [CREATION, ALLIANCE]) expect(dessinee(monde(), id)).toBeDefined()
  })

  // sk228 / sk230a-d : mis de côté à la mise en place, le fragment attend FACE CACHÉE dans la pile annexe
  // (zone « annexes », capturé sur le moteur) : il n'est pas posé sur la table comme une carte jouée.
  it('un Cosmic Cube Fragment mis de côté est dessiné face cachée dans la pile annexe, hors des cartes en jeu', () => {
    const fragment = dessinee(monde(), FRAGMENT)
    expect(fragment?.facedown).toBe(true)
    expect(fragment?.zone).toBe('annexes')
    expect(dessinee(monde(), COMMANDER)?.facedown).toBeFalsy()
  })

  // Témoin : les attachements ne sont pas des racines.
  it('TEMOIN : l’attachement et la carte jouée ne sont pas confondus avec la pile annexe', () => {
    const racines = cartesDessinees(monde()).filter((c) => c.portePar === 0).map((c) => c.id)
    expect(racines).toContain(COMMANDER)
    expect(racines).toContain(SHAPER)
    expect(racines).not.toContain(ADAPTATION)
    expect(racines).not.toContain(FORCEFIELD)
  })
})
