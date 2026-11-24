// Starjammers Aspects (Phenexian et Mysteltainn, préfixe sy) : ce que la table DESSINE (étape 8 bis de PROCESSUS-CARTE).
//
// Cartes qui changent ce qu'on VOIT : Havok (sy025) glisse 3 cartes Rencontre sous LUI (un allié, pas l'identité), Corsair allié (sy002) glisse
// les cartes payées sous lui, Blade of the Phoenix (sy018) et Longarm Blaster (sy024) s'attachent à un allié, Kalyx (sy042) met la carte du
// dessus de son deck en jeu comme allié face cachée (gabarit `sy_thorn_ally`).
// Modèle : `corsair-plateau.test.ts`. Le plateau dessine déjà ces cas : aucun correctif n'a été nécessaire, le cas est vert dès son écriture.
import { describe, expect, it } from 'vitest'
import { carteSurTable, dessinee, siege, tableAvec } from './plateau-de-test'

const HAVOK = 1
const GLISSEE_A = 2
const GLISSEE_B = 3
const CORSAIR = 10
const PAYEE = 11
const KORVUS = 20
const LAME = 21
const THORN = 30

const monde = () =>
  tableAvec(
    siege({
      allies: [
        carteSurTable(HAVOK, 'sy025', 'Ally', 'Havok'),
        carteSurTable(GLISSEE_A, '01146', 'Treachery', 'Repair Sequence', { bind_object_id: HAVOK, is_face_up: false, visible_for_players: [] }),
        carteSurTable(GLISSEE_B, '01123', 'Treachery', 'Sonic Boom', { bind_object_id: HAVOK, is_face_up: false, visible_for_players: [] }),
        carteSurTable(CORSAIR, 'sy002', 'Ally', 'Corsair'),
        carteSurTable(PAYEE, '01090', 'Resource', 'Strength', { bind_object_id: CORSAIR, is_face_up: false, visible_for_players: [0] }),
        carteSurTable(KORVUS, 'sy017', 'Ally', "Korvus Rook'shir"),
        carteSurTable(LAME, 'sy018', 'Upgrade', 'Blade of the Phoenix', { bind_object_id: KORVUS }),
        // le gabarit d'allié « face cachée » est une VRAIE face d'allié (face visible) dont l'image est le dos de carte (`pic_id: 'player'`)
        carteSurTable(THORN, 'sy_thorn_ally', 'Ally', 'Thorn Ally', { pic_id: 'player' }),
      ],
    })
  )

describe('Starjammers Aspects : ce que la table dessine', () => {
  it('dessine Havok et les cartes glissées sous lui, portées par lui', () => {
    expect(dessinee(monde(), HAVOK)).toBeDefined()
    expect(dessinee(monde(), GLISSEE_A)).toBeDefined()
    expect(dessinee(monde(), GLISSEE_B)).toBeDefined()
    expect(dessinee(monde(), GLISSEE_A)?.portePar).toBe(HAVOK)
    expect(dessinee(monde(), GLISSEE_B)?.portePar).toBe(HAVOK)
  })

  it('dessine la carte payée glissée sous Corsair (allié), lisible par son propriétaire', () => {
    expect(dessinee(monde(), PAYEE)).toBeDefined()
    expect(dessinee(monde(), PAYEE)?.portePar).toBe(CORSAIR)
    expect(dessinee(monde(), PAYEE)?.peeking).toBe(true)
  })

  it("dessine Blade of the Phoenix attachée à Korvus", () => {
    expect(dessinee(monde(), LAME)).toBeDefined()
    expect(dessinee(monde(), LAME)?.portePar).toBe(KORVUS)
  })

  it("dessine l'allié THORN (dos de carte) comme n'importe quel allié", () => {
    expect(dessinee(monde(), THORN)).toBeDefined()
    expect(dessinee(monde(), THORN)?.portePar).toBe(0)
  })
})
