// La table calee sur le recit : ce qui n'est pas raconte n'apparait pas.
import { describe, expect, it } from 'vitest'
import type { EtapeDeroule } from './deroule-phase'
import { avecFacesRencontreDuRecit, questionDuRecit, cartesAVenir, estEnJeu, majInstantanes, mondeAvantEtape, mondeDeLaTable, sansCartesAVenir, type Instantanes } from './table-calee'
import type { World } from './world'

const monde = (nom: string) => ({ phase: 'Villain Activation', nom }) as unknown as World
const etape = (cle: string, etat: string) => ({ cle, etat }) as unknown as EtapeDeroule
const vide: Instantanes = new Map()

describe('la table suit l etape affichee, pas le monde le plus recent', () => {
  it('le retournement du boost (trame sans changement d etape) ne bouge pas la table', () => {
    // Trame 1 : l'attaque est annoncee, le boost est face cachee.
    let inst = majInstantanes(vide, [etape('a1', 'intention')], monde('boost cache'), true)
    // Trame 2 : le boost est retourne, l'etape « attaque » n'a pas encore change.
    inst = majInstantanes(inst, [etape('a1', 'intention')], monde('boost retourne'), true)
    expect((mondeDeLaTable(inst, 'a1', false) as unknown as { nom: string }).nom).toBe('boost cache')
  })

  it('la resolution change l etape : la table montre alors son monde', () => {
    let inst = majInstantanes(vide, [etape('a1', 'intention')], monde('avant'), true)
    inst = majInstantanes(inst, [etape('a1', 'resolution')], monde('apres'), true)
    expect((mondeDeLaTable(inst, 'a1', false) as unknown as { nom: string }).nom).toBe('apres')
  })

  it('une etape deja vue garde son monde quand une suivante arrive', () => {
    let inst = majInstantanes(vide, [etape('m1', 'resolution')], monde('menace'), true)
    inst = majInstantanes(inst, [etape('m1', 'resolution'), etape('r1', 'resolution')], monde('revelation'), true)
    expect((mondeDeLaTable(inst, 'm1', false) as unknown as { nom: string }).nom).toBe('menace')
    expect((mondeDeLaTable(inst, 'r1', false) as unknown as { nom: string }).nom).toBe('revelation')
  })

  it('une question au joueur : monde reel, les clics doivent viser les vraies cartes', () => {
    const inst = majInstantanes(vide, [etape('a1', 'intention')], monde('x'), true)
    expect(mondeDeLaTable(inst, 'a1', true)).toBeUndefined()
  })

  it('etape sans instantane (le bilan) ou hors phase : monde reel', () => {
    const inst = majInstantanes(vide, [etape('a1', 'intention')], monde('x'), true)
    expect(mondeDeLaTable(inst, 'bilan', false)).toBeUndefined()
    expect(majInstantanes(inst, [], monde('y'), false).size).toBe(0)
  })
})

// REFONTE, LOT 4 (essai, 12/10/2026, decisions 49 et 51).

describe('lot 4 : rien sur la table avant que l ecran ne le raconte', () => {
  const etapeT = (cle: string, titre: string, carteId?: number) => ({ cle, titre, carteId, boosts: [] }) as unknown as EtapeDeroule
  const liste = [etapeT('a1', 'attaque', 10), etapeT('e1', 'entree', 77), etapeT('r1', 'revelation', 88), etapeT('m1', 'manigance', 10)]

  it('les cartes que les etapes SUIVANTES feront entrer en jeu', () => {
    expect([...cartesAVenir(liste, 'a1')].sort()).toEqual([77, 88])
    expect([...cartesAVenir(liste, 'e1')]).toEqual([88])
    expect([...cartesAVenir(liste, 'r1')]).toEqual([])
    expect(cartesAVenir(liste, undefined).size).toBe(0)
  })

  it('le monde perd les cartes a venir face visible et ce qui leur est attache, pas les cartes face cachee', () => {
    const carte = (id: number, faceVisible = true, bind = 0) => ({ id, is_face_up: faceVisible, bind_object_id: bind, name: `c${id}` })
    const m = {
      phase: 'Villain Activation',
      players: [{ area_ally: [carte(5), carte(77), carte(91, true, 77)], dealt: [carte(88, false)] }],
    } as unknown as World
    const resultat = sansCartesAVenir(m, new Set([77, 88])) as unknown as { players: Array<{ area_ally: Array<{ id: number }>; dealt: Array<{ id: number }> }> }
    expect(resultat.players[0].area_ally.map((c) => c.id)).toEqual([5])
    expect(resultat.players[0].dealt.map((c) => c.id)).toEqual([88])
    // Rien a retirer : le meme objet, sans copie.
    expect(sansCartesAVenir(m, new Set())).toBe(m)
  })

  it('avant le resultat, la table montre le monde de l etape precedente', () => {
    let inst = majInstantanes(vide, [etape('m0', 'resolution')], monde('avant attaque'), true)
    inst = majInstantanes(inst, [etape('m0', 'resolution'), etape('a1', 'resolution')], monde('apres attaque'), true)
    const etapes = [etape('m0', 'resolution'), etape('a1', 'resolution')]
    expect((mondeAvantEtape(inst, etapes, 'a1') as unknown as { nom: string }).nom).toBe('avant attaque')
    expect(mondeAvantEtape(inst, etapes, 'm0')).toBeUndefined()
  })
})

describe('lot 4 : la carte revelee arrive sur la table a SON ecran', () => {
  const sbire = (faceVisible: boolean) => ({ id: 57, is_face_up: faceVisible, bind_object_id: 0 })
  const mondeAvec = (nom: string, enJeu: boolean) =>
    ({ phase: 'Reveal Encounter Cards', nom, area_villain: [], players: [{ engaged_enemies: enJeu ? [sbire(true)] : [] }] }) as unknown as World
  const revelation = { cle: 'r57', titre: 'revelation', carteId: 57, boosts: [] } as unknown as EtapeDeroule

  it('estEnJeu : sur la table face visible, pas ailleurs', () => {
    expect(estEnJeu(mondeAvec('a', true), 57)).toBe(true)
    expect(estEnJeu(mondeAvec('b', false), 57)).toBe(false)
  })

  it('dans l essai, le monde de la revelation suit jusqu a ce que la carte soit en jeu', () => {
    let inst = majInstantanes(vide, [revelation], mondeAvec('revelee', false), true, true)
    inst = majInstantanes(inst, [revelation], mondeAvec('engagee', true), true, true)
    expect((mondeDeLaTable(inst, 'r57', false) as unknown as { nom: string }).nom).toBe('engagee')
    // Une fois en jeu, le monde ne bouge plus.
    inst = majInstantanes(inst, [revelation], mondeAvec('plus tard', true), true, true)
    expect((mondeDeLaTable(inst, 'r57', false) as unknown as { nom: string }).nom).toBe('engagee')
  })

  it('sans l essai, comportement d avant : le monde de la revelation ne suit pas', () => {
    let inst = majInstantanes(vide, [revelation], mondeAvec('revelee', false), true)
    inst = majInstantanes(inst, [revelation], mondeAvec('engagee', true), true)
    expect((mondeDeLaTable(inst, 'r57', false) as unknown as { nom: string }).nom).toBe('revelee')
  })
})


describe('décisions et faces des rencontres suivent le récit', () => {
  it('retient une question future tant que le résultat sur table n’est pas validé', () => {
    const resolue = etape('a', 'resolu')
    expect(questionDuRecit(true, resolue, false, true)).toBe(false)
    expect(questionDuRecit(true, resolue, true, true)).toBe(true)
    expect(questionDuRecit(true, etape('a', 'annonce'), false, true)).toBe(true)
    expect(questionDuRecit(true, etape('a', 'annonce'), false, true, true)).toBe(false)
    expect(questionDuRecit(true, resolue, false, false)).toBe(true)
  })

  it('une question actualise la main sans révéler puis recacher un boost', () => {
    const boost = { id: 72, is_face_up: false, visible_for_players: [] }
    const recit = { area_boost: [boost], encounter_deck: [], players: [] } as unknown as World
    const actuel = { area_boost: [{ ...boost, is_face_up: true, visible_for_players: [0] }], players: [{ hand_cards: [{ id: 99, is_face_up: true }] }] } as unknown as World
    const stable = avecFacesRencontreDuRecit(actuel, recit)
    expect(stable.area_boost[0].is_face_up).toBe(false)
    expect(stable.area_boost[0].visible_for_players).toEqual([])
    expect(stable.players).toBe(actuel.players)
    expect(actuel.area_boost[0].is_face_up).toBe(true)
  })

  it('figer les compteurs sur un monde précédent ne recache pas un boost déjà lu', () => {
    const boost = { id: 72, is_face_up: false, visible_for_players: [] }
    const avant = { area_boost: [boost], players: [] } as unknown as World
    const lu = { area_boost: [{ ...boost, is_face_up: true, visible_for_players: [0] }], players: [] } as unknown as World
    expect(avecFacesRencontreDuRecit(avant, lu).area_boost[0].is_face_up).toBe(true)
    expect(avecFacesRencontreDuRecit(lu, lu, true).area_boost[0].is_face_up).toBe(false)
  })
})
