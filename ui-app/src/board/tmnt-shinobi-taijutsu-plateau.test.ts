// TMNT Shinobi Taijutsu (`sh`) : ce que le plateau DESSINE une fois la carte résolue.
//
// `Fusion/marvel-lcg-src/tools/cas/tmnt_shinobi_taijutsu.py` prouve ce que le moteur FAIT ; ce fichier prouve
// ce que le joueur REGARDE (PROCESSUS-CARTE.md, étape 8 bis). On pose à la main l'état d'arrivée que le moteur
// publie, et on affirme sur `dessinee(...)`.
//
// Cartes concernées (elles changent ce qu'on VOIT) :
//   sh012 Mutant Fight Club : événements ATTACHÉS face cachée sous un SOUTIEN ;
//   sh010 Martial Skill (compteurs chi), sh016 Jō (compteurs cudgel, nom français « bâton ») ;
//   sh014 Minarai : amélioration attachée à un ALLIÉ ; sh017 Odyn : carte Tough sur un allié ;
//   sh003 / sh009 / sh011 / sh016 : carte Dazed posée sur un ennemi ; sh004 : Stunned ; sh007 : Stunned / Confused.
// Cartes SANS cas : sh001, sh002, sh005, sh006, sh008, sh013, sh015, sh018, sh019 (prévention, pioche, retour en main :
// aucune trace de plus sur la table), sh020 (carte Tough sur le héros : même dessin que sh017).
import { afterEach, describe, expect, it, vi } from 'vitest'
import * as langue from './langue'
import { nomDeCompteur } from './compteurs-fr'
import { carteSurTable as carte, cartesDessinees, dessinee, siege, tableAvec } from './plateau-de-test'
import type { WorldCard } from './world'

afterEach(() => vi.restoreAllMocks())

const IDENTITE = 1
const CLUB = 10
const GLISSEE_1 = 11
const GLISSEE_2 = 12
const MARTIAL = 13
const JO = 14
const ALLIE = 20
const MINARAI = 21
const ODYN = 22
const TOUGH = 23
const RHINO = 60

const alterEgo = () => carte(IDENTITE, '01001b', 'AlterEgo', 'Peter Parker')
const heros = () => carte(IDENTITE, '01001a', 'Hero', 'Spider-Man')
const club = (extra: Partial<WorldCard> = {}) => carte(CLUB, 'sh012', 'Support', '* Mutant Fight Club', extra)
const glissee = (id: number, cardId: string, nom: string, extra: Partial<WorldCard> = {}) =>
  carte(id, cardId, 'Event', nom, { bind_object_id: CLUB, is_face_up: false, ...extra })

describe('sh012 Mutant Fight Club : les événements attachés face cachée sont dessinés', () => {
  const monde = () =>
    tableAvec(
      siege({
        area_hero: [alterEgo()],
        supports: [club({ is_ready: false })],
        hand_cards: [carte(40, 'sh003', 'Event', 'Stiff Jab')],
      })
    )

  it('le Club est dessiné en genre soutien, couché après l Action', () => {
    expect(dessinee(monde(), CLUB)?.kind).toBe('support')
    expect(dessinee(monde(), CLUB)?.exhausted).toBe(true)
  })

  it('un événement attaché est à l écran (assertion qui aurait attrapé Contingency Plan)', () => {
    const m = tableAvec(siege({ area_hero: [alterEgo()], supports: [club(), glissee(GLISSEE_1, '01087', 'Haymaker')] }))
    expect(dessinee(m, GLISSEE_1)).toBeDefined()
  })

  it('il est posé face cachée (visible de son propriétaire), pas réduit à un dos', () => {
    const m = tableAvec(siege({ area_hero: [alterEgo()], supports: [club(), glissee(GLISSEE_1, '01087', 'Haymaker')] }))
    expect(dessinee(m, GLISSEE_1)?.peeking).toBe(true)
    expect(dessinee(m, GLISSEE_1)?.facedown).toBe(false)
  })

  it('deux événements attachés (aucun plafond imprimé) : les DEUX sont dessinés, à la suite du Club', () => {
    const m = tableAvec(
      siege({
        area_hero: [alterEgo()],
        supports: [club(), glissee(GLISSEE_1, '01087', 'Haymaker'), glissee(GLISSEE_2, '01003', 'Backflip')],
      })
    )
    const vues = cartesDessinees(m)
    const rang = (id: number) => vues.findIndex((c) => c.id === id)
    expect(dessinee(m, GLISSEE_1)).toBeDefined()
    expect(dessinee(m, GLISSEE_2)).toBeDefined()
    expect(rang(GLISSEE_1)).toBe(rang(CLUB) + 1)
    expect(rang(GLISSEE_2)).toBe(rang(CLUB) + 2)
  })

  it('vue d un autre siège : l événement attaché n est qu un dos', () => {
    const m = tableAvec(
      siege({
        area_hero: [alterEgo()],
        supports: [club(), glissee(GLISSEE_1, '01087', 'Haymaker', { visible_for_players: [] })],
      })
    )
    expect(dessinee(m, GLISSEE_1)?.facedown).toBe(true)
    expect(dessinee(m, GLISSEE_1)?.codeCarte).toBeUndefined()
  })

  it('une fois jouée depuis le Club, la carte quitte le Club et rejoint la défausse', () => {
    const m = tableAvec(
      siege({
        area_hero: [heros()],
        supports: [club()],
        player_discard_pile: [carte(GLISSEE_1, '01087', 'Event', 'Haymaker')],
      })
    )
    expect(dessinee(m, GLISSEE_1)?.zone).toBe('piles-joueur')
    expect(cartesDessinees(m).filter((c) => c.peeking)).toHaveLength(0)
  })
})

describe('sh010 Martial Skill, sh016 Jō : les compteurs chi et cudgel sont dessinés', () => {
  it('Martial Skill entre avec 2 compteurs chi, en genre amélioration attachée à l identité', () => {
    const m = tableAvec(
      siege({
        area_hero: [heros(), carte(MARTIAL, 'sh010', 'Upgrade', 'Martial Skill', { bind_object_id: IDENTITE, info: { c_chi: 2 } })],
      })
    )
    expect(dessinee(m, MARTIAL)?.compteurs.chi).toBe(2)
    expect(dessinee(m, MARTIAL)?.kind).toBe('upgrade')
  })

  it('après la Réponse : 1 compteur chi, la carte est couchée', () => {
    const m = tableAvec(
      siege({
        area_hero: [
          heros(),
          carte(MARTIAL, 'sh010', 'Upgrade', 'Martial Skill', { bind_object_id: IDENTITE, is_ready: false, info: { c_chi: 1 } }),
        ],
      })
    )
    expect(dessinee(m, MARTIAL)?.compteurs.chi).toBe(1)
    expect(dessinee(m, MARTIAL)?.exhausted).toBe(true)
  })

  it('Jō entre avec 3 compteurs cudgel et peut en porter plus de 3 (aucun plafond imprimé)', () => {
    for (const n of [3, 4]) {
      const m = tableAvec(
        siege({ area_hero: [heros(), carte(JO, 'sh016', 'Upgrade', '* Jō', { bind_object_id: IDENTITE, info: { c_cudgel: n } })] })
      )
      expect(dessinee(m, JO)?.compteurs.cudgel).toBe(n)
    }
  })

  it('le compteur cudgel s écrit « bâton » en français (compteurs-fr.ts), « cudgel » en anglais', () => {
    vi.spyOn(langue, 'langueActuelle').mockReturnValue('fr')
    expect(nomDeCompteur('cudgel')).toBe('bâton')
    vi.spyOn(langue, 'langueActuelle').mockReturnValue('en')
    expect(nomDeCompteur('cudgel')).toBe('cudgel')
  })

  it('le compteur chi garde son nom français « chi »', () => {
    vi.spyOn(langue, 'langueActuelle').mockReturnValue('fr')
    expect(nomDeCompteur('chi')).toBe('chi')
  })

  it('Jō vidée de ses compteurs (Uses) : elle n est plus sur la table, elle est en défausse', () => {
    const m = tableAvec(
      siege({ area_hero: [heros()], player_discard_pile: [carte(JO, 'sh016', 'Upgrade', '* Jō', { info: { c_cudgel: 0 } })] })
    )
    expect(dessinee(m, JO)?.zone).toBe('piles-joueur')
  })
})

describe('sh014 Minarai, sh017 Odyn : amélioration attachée à un allié, carte Tough sur Odyn', () => {
  const allie = () => carte(ALLIE, '01020', 'Ally', '* Hellcat')
  const minarai = (extra: Partial<WorldCard> = {}) =>
    carte(MINARAI, 'sh014', 'Upgrade', '* Minarai', { bind_object_id: ALLIE, ...extra })

  it('Minarai est dessinée, en genre amélioration, portée par l allié (et non par l identité)', () => {
    const m = tableAvec(siege({ area_hero: [heros()], allies: [allie(), minarai()] }))
    expect(dessinee(m, MINARAI)).toBeDefined()
    expect(dessinee(m, MINARAI)?.kind).toBe('upgrade')
    expect(dessinee(m, MINARAI)?.portePar).toBe(ALLIE)
  })

  it('l allié vaincu : l amélioration part avec lui, toutes deux en défausse', () => {
    const m = tableAvec(
      siege({
        area_hero: [heros()],
        player_discard_pile: [carte(ALLIE, '01020', 'Ally', '* Hellcat'), carte(MINARAI, 'sh014', 'Upgrade', '* Minarai')],
      })
    )
    // La défausse n'est dessinée que par sa carte du dessus (Minarai) : la pile en compte deux, et plus rien n'est en jeu.
    expect(dessinee(m, MINARAI)?.zone).toBe('piles-joueur')
    expect(dessinee(m, MINARAI)?.pileCount).toBe(2)
    expect(cartesDessinees(m).filter((c) => c.id === ALLIE || c.portePar === ALLIE)).toHaveLength(0)
  })

  it('Odyn porte sa carte Tough (donnée par la Réponse)', () => {
    const m = tableAvec(
      siege({
        area_hero: [heros()],
        allies: [
          carte(ODYN, 'sh017', 'Ally', '* Odyn'),
          carte(TOUGH, 'tough', 'StatusCard', 'Tough', { bind_object_id: ODYN }),
        ],
      })
    )
    expect(dessinee(m, TOUGH)?.kind).toBe('status')
    expect(dessinee(m, TOUGH)?.codeCarte).toBe('tough')
    expect(dessinee(m, TOUGH)?.portePar).toBe(ODYN)
  })
})

describe('sh003, sh004, sh007, sh009, sh011, sh016 : les cartes d état Hébété, Étourdi, Désorienté sont posées sur Rhino', () => {
  it.each(['dazed', 'stunned', 'confused'])('la carte %s est dessinée sur l ennemi', (statut) => {
    const m = tableAvec(siege({ area_hero: [heros()] }), {
      area_villain: [carte(RHINO, '01094', 'EncounterVillain', 'Rhino'), carte(81, statut, 'StatusCard', statut, { bind_object_id: RHINO })],
    })
    expect(dessinee(m, 81)?.portePar).toBe(RHINO)
    expect(dessinee(m, 81)?.kind).toBe('status')
    expect(dessinee(m, 81)?.codeCarte).toBe(statut)
  })
})
