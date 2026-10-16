// Venus (TMNT, `tv`) : ce que le plateau DESSINE une fois la carte résolue.
//
// `tools/cas/tmnt_venus.py` prouve ce que le moteur FAIT ; ce fichier prouve ce que le
// joueur REGARDE (PROCESSUS-CARTE.md, étape 8 bis). On pose à la main l'état d'arrivée
// que le moteur publie (le compteur de dragage est `info.c_dredge` de l'IDENTITE, quelle
// que soit sa face : Venus et Bonnie sont une seule carte), et on affirme sur
// `dessinee(...)`.
//
// Cartes SANS cas propre ici, parce qu'elles ne font que chiffrer ou piocher : tv005
// Eldritch Lance (dégâts + pioche), tv007 Resistance (prévention + pioche : le retrait de
// compteurs est couvert par les cas du compteur), tv008 Evanescence (ressource), tv018
// Groundchuck-Dirtbag (statistiques et Ténacité natives : couvertes par le statut Tough de
// tv019).
//
// Pas de panorama des paires jumelles (Dragon Scale / Turtle Shell, scans 12 et 15) :
// l'utilisateur ne les a pas confirmées, rien n'est déclaré.
import { describe, expect, it } from 'vitest'
import { carteSurTable as carte, cartesDessinees, dessinee, siege, tableAvec } from './plateau-de-test'

const IDENTITE = 1

const heros = (dredge = 0, extra: Record<string, unknown> = {}) =>
  carte(IDENTITE, 'tv001a', 'Hero', 'Venus', { info: dredge > 0 ? { c_dredge: dredge } : {}, ...extra })
const civil = (dredge = 0, extra: Record<string, unknown> = {}) =>
  carte(IDENTITE, 'tv001b', 'AlterEgo', 'Bonnie', { info: dredge > 0 ? { c_dredge: dredge } : {}, ...extra })
const element = (id: number, code: string, nom: string, ready = true) =>
  carte(id, code, 'Upgrade', nom, { bind_object_id: IDENTITE, is_ready: ready })
const dos = (id: number, code: string, type: string, nom: string) =>
  carte(id, code, type, nom, { is_face_up: false, visible_for_players: [] })

describe('le compteur de dragage est dessiné sur l identité (tv001a, tv003, tv004, tv006, tv007, tv010-tv013)', () => {
  it('forme héros : 3 compteurs de dragage posés par tv001a sont visibles sur Venus', () => {
    const monde = tableAvec(siege({ area_hero: [heros(3)] }))
    expect(dessinee(monde, IDENTITE)?.compteurs.dredge).toBe(3)
  })

  it('le plafond de 6 est dessiné tel quel (tv001a, question Q1)', () => {
    const monde = tableAvec(siege({ area_hero: [heros(6)] }))
    expect(dessinee(monde, IDENTITE)?.compteurs.dredge).toBe(6)
  })

  // tv001b Bonnie, tv011 Dragon Scale : le stock suit l'identité en forme civile.
  it('forme alter-ego : le même stock est visible sur Bonnie', () => {
    const monde = tableAvec(siege({ area_hero: [civil(2)] }))
    const bonnie = dessinee(monde, IDENTITE)
    expect(bonnie?.codeCarte).toBe('tv001b')
    expect(bonnie?.compteurs.dredge).toBe(2)
  })

  // tv003 Arc Nova (X), tv010, tv012, tv013 : 2 compteurs retirés.
  it('compteurs retirés : plus aucun compteur dessiné sur l identité', () => {
    const monde = tableAvec(siege({ area_hero: [heros(0)] }))
    expect(dessinee(monde, IDENTITE)?.compteurs.dredge).toBeUndefined()
  })

  it('le compteur n apparaît que sur l identité, pas sur l amélioration attachée', () => {
    const monde = tableAvec(
      siege({ area_hero: [heros(1), element(10, 'tv011', 'Dragon Scale', false)] })
    )
    expect(dessinee(monde, 10)?.compteurs.dredge).toBeUndefined()
    expect(dessinee(monde, 10)?.exhausted).toBe(true)
    expect(dessinee(monde, IDENTITE)?.compteurs.dredge).toBe(1)
  })
})

describe('tv001b Bonnie Setup : l amélioration ELEMENT trouvée est mise en jeu, attachée à l identité', () => {
  const monde = () =>
    tableAvec(
      siege({
        area_hero: [civil(), element(20, 'tv014', 'Turtle Shell')],
        player_deck: [dos(30, 'tv009', 'Upgrade', 'Diode')],
        player_discard_pile: [carte(31, 'tv004', 'Event', 'Brain Burn')],
      })
    )

  it('l amélioration est dessinée sous l identité', () => {
    const vue = dessinee(monde(), 20)
    expect(vue).toBeDefined()
    expect(vue?.portePar).toBe(IDENTITE)
    expect(vue?.kind).toBe('upgrade')
  })

  it('la carte traversée reste visible sur la pile de défausse, la trouvée n y est plus', () => {
    expect(dessinee(monde(), 31)?.zone).toBe('piles-joueur')
    expect(cartesDessinees(monde()).filter((c) => c.codeCarte === 'tv014' && c.zone === 'piles-joueur')).toHaveLength(0)
  })
})

describe('tv002 Bludgeon : une carte de la défausse remonte sur le dessus du deck', () => {
  const monde = () =>
    tableAvec(
      siege({
        area_hero: [civil()],
        allies: [carte(40, 'tv002', 'Ally', 'Bludgeon')],
        player_deck: [
          dos(41, '01090', 'Event', 'Fond'),
          dos(42, '01089', 'Event', 'Remontée'),
        ],
        player_discard_pile: [carte(43, '01088', 'Event', 'Energy')],
      })
    )

  it('l allié est dessiné chez les alliés', () => {
    expect(dessinee(monde(), 40)?.kind).toBe('ally')
  })

  it('la pile du deck est représentée par la carte du dessus, dos visible, 2 cartes', () => {
    const deck = dessinee(monde(), 42)
    expect(deck?.zone).toBe('piles-joueur')
    expect(deck?.facedown).toBe(true)
    expect(deck?.pileCount).toBe(2)
  })

  it('la défausse ne montre plus la carte remontée', () => {
    expect(dessinee(monde(), 43)?.pileCount).toBe(1)
    expect(cartesDessinees(monde()).filter((c) => c.codeCarte === '01089' && c.zone === 'piles-joueur' && !c.facedown)).toHaveLength(0)
  })
})

describe('tv006 Quantanucleic Acid : Venus porte une carte d état Tenace', () => {
  it('la carte de statut est dessinée sous l identité', () => {
    const monde = tableAvec(
      siege({ area_hero: [heros(0), carte(50, 'tough', 'StatusCard', 'Tough', { bind_object_id: IDENTITE })] })
    )
    const statut = dessinee(monde, 50)
    expect(statut?.kind).toBe('status')
    expect(statut?.codeCarte).toBe('tough')
    expect(statut?.portePar).toBe(IDENTITE)
  })
})

describe('tv004 Brain Burn : l ennemi est Sonné ET Désorienté', () => {
  const monde = () =>
    tableAvec(siege({ area_hero: [heros(0)] }), {
      area_villain: [
        carte(60, '01094', 'EncounterVillain', 'Rhino'),
        carte(61, 'stunned', 'StatusCard', 'Stunned', { bind_object_id: 60 }),
        carte(62, 'confused', 'StatusCard', 'Confused', { bind_object_id: 60 }),
      ],
    })

  it('les deux cartes de statut sont dessinées sur le vilain', () => {
    for (const [id, code] of [[61, 'stunned'], [62, 'confused']] as const) {
      const vue = dessinee(monde(), id)
      expect(vue).toBeDefined()
      expect(vue?.portePar).toBe(60)
      expect(vue?.codeCarte).toBe(code)
    }
  })
})

describe('tv009-tv014 : les améliorations ELEMENT utilisées sont dessinées inclinées', () => {
  const monde = () =>
    tableAvec(
      siege({
        area_hero: [
          heros(0),
          element(70, 'tv009', 'Arcane Emitting Diode', false),
          element(71, 'tv010', 'Cosmic Requiem', false),
          element(72, 'tv012', 'Dream Weaver', false),
          element(73, 'tv013', 'Reanimator Engine', false),
          element(74, 'tv014', 'Turtle Shell', false),
        ],
      })
    )

  it('chacune est couchée, attachée à l identité', () => {
    for (const id of [70, 71, 72, 73, 74]) {
      const vue = dessinee(monde(), id)
      expect(vue?.exhausted).toBe(true)
      expect(vue?.portePar).toBe(IDENTITE)
    }
  })

  it('tv014 Turtle Shell : Venus est REDRESSÉE pendant que la carapace est couchée', () => {
    expect(dessinee(monde(), IDENTITE)?.exhausted).toBe(false)
    expect(dessinee(monde(), 74)?.exhausted).toBe(true)
  })
})

describe('tv010 Cosmic Requiem et tv012 Dream Weaver : la carte trouvée arrive en main, les autres sont défaussées', () => {
  const monde = () =>
    tableAvec(
      siege({
        area_hero: [heros(0)],
        hand_cards: [carte(80, '01053', 'Event', 'Relentless Assault')],
        player_discard_pile: [carte(81, '01073', 'Event', 'Traversée')],
        player_deck: [dos(82, '01083', 'Ally', 'Fond')],
      })
    )

  it('la carte en main est dessinée dans la main', () => {
    expect(dessinee(monde(), 80)?.zone).toBe('main')
  })

  it('la carte traversée est sur la pile de défausse', () => {
    expect(dessinee(monde(), 81)?.zone).toBe('piles-joueur')
  })
})

describe('tv013 Reanimator Engine : des cartes de la défausse sont remélangées dans le deck', () => {
  it('la défausse ne les montre plus, la pile du deck grossit', () => {
    const monde = tableAvec(
      siege({
        area_hero: [heros(0)],
        player_deck: [dos(90, '01074', 'Event', 'Mélangée'), dos(91, '01075', 'Event', 'Mélangée'), dos(92, '01083', 'Ally', 'Fond')],
        player_discard_pile: [carte(93, '01073', 'Event', 'Restée')],
      })
    )
    expect(dessinee(monde, 93)?.pileCount).toBe(1)
    const piles = cartesDessinees(monde).filter((c) => c.zone === 'piles-joueur' && c.facedown)
    expect(piles.length).toBeGreaterThan(0)
    expect(piles[0].pileCount).toBe(3)
  })
})

describe('tv011 Dragon Scale : amélioration couchée, compteur retiré sur l identité', () => {
  it('incliné et le compteur a bien disparu de l identité', () => {
    const monde = tableAvec(siege({ area_hero: [civil(0), element(100, 'tv011', 'Dragon Scale', false)] }))
    expect(dessinee(monde, 100)?.exhausted).toBe(true)
    expect(dessinee(monde, IDENTITE)?.compteurs.dredge).toBeUndefined()
  })
})

describe('tv015 Faulty Creation : l obligation est dessinée, Bonnie peut être en civil', () => {
  it('l obligation est dans la zone des obligations et l identité apparaît en civil', () => {
    const monde = tableAvec(
      siege({ area_hero: [civil()], obligations_area: [carte(110, 'tv015', 'Obligation', 'Faulty Creation')] })
    )
    expect(dessinee(monde, 110)).toBeDefined()
    expect(dessinee(monde, IDENTITE)?.codeCarte).toBe('tv001b')
  })

  it('une fois retirée de la partie, elle n est plus dessinée', () => {
    const monde = tableAvec(siege({ area_hero: [civil()], obligations_area: [] }))
    expect(dessinee(monde, 110)).toBeUndefined()
  })
})

describe('tv016 Jasper Barlow s Lab : la manigance annexe et ses jetons de menace', () => {
  it('la manigance porte 2 jetons de menace (Entrave 2) et la principale 5 (Incitation 2)', () => {
    const monde = tableAvec(siege({ area_hero: [civil()] }), {
      area_schemes_side: [carte(120, 'tv016', 'EncounterSideScheme', "Jasper Barlow's Lab", { info: { k_threat: 2 } })],
    })
    expect(dessinee(monde, 120)).toBeDefined()
    expect(dessinee(monde, 120)?.menace).toBe(2)
  })
})

describe('tv017 Jasper Barlow et tv019 Salvaged Scales : Tenace sur les sbires et le vilain', () => {
  const monde = () =>
    tableAvec(
      siege({
        area_hero: [civil()],
        engaged_enemies: [
          carte(130, '01101', 'Minion', 'Hydra Mercenary'),
          carte(131, 'tough', 'StatusCard', 'Tough', { bind_object_id: 130 }),
          carte(132, 'tv017', 'Minion', 'Jasper Barlow'),
          carte(133, 'tough', 'StatusCard', 'Tough', { bind_object_id: 132 }),
        ],
      }),
      {
        area_villain: [
          carte(140, '01094', 'EncounterVillain', 'Rhino'),
          carte(141, 'tough', 'StatusCard', 'Tough', { bind_object_id: 140 }),
        ],
      }
    )

  it('chaque sbire engagé porte sa carte Tenace', () => {
    expect(dessinee(monde(), 131)?.portePar).toBe(130)
    expect(dessinee(monde(), 133)?.portePar).toBe(132)
  })

  it('le vilain porte la sienne (tv019)', () => {
    const vue = dessinee(monde(), 141)
    expect(vue?.portePar).toBe(140)
    expect(vue?.kind).toBe('status')
  })
})

describe('tv017 / tv018 : [star] Boost, la carte est donnée au premier joueur face cachée', () => {
  it('la carte distribuée est dessinée dos seul', () => {
    const monde = tableAvec(
      siege({
        area_hero: [civil()],
        dealt_encounter_cards: [dos(150, 'tv018', 'Minion', 'Groundchuck-Dirtbag')],
      })
    )
    const vue = dessinee(monde, 150)
    expect(vue).toBeDefined()
    expect(vue?.facedown).toBe(true)
  })
})
