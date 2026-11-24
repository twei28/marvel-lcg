// Les STARJAMMER glissés FACE VISIBLE sous Imprisoned on Chandilar doivent être dessinés (étape 8 bis de
// PROCESSUS-CARTE, leçon Contingency Plan).
//
// Galactic Storm, scénario Majestrix's Verdict (`gs119`, lot GS-5, 20/10/2026). La mise en place (1A, `gs117a`)
// glisse les six alliés STARJAMMER sous la manigance annexe ; le livret 1.2 p.4 veut le glissé FACE VISIBLE
// (`PlaceCardHere(faces, True, ..)`), là où The Mother of Night (`mere-de-la-nuit-cartes-dessous.test.ts`) pose
// face cachée. Le moteur les émet dans `area_schemes_side` à la suite de la manigance, liés par `bind_object_id`
// (mesuré au harnais : « déplacée(s) vers [gs119]'s PlaceCardArea<6> »). Le joueur doit pouvoir LIRE qui est en
// prison : c'est ce qu'il choisit de libérer.
import { describe, expect, it } from 'vitest'
import { carteSurTable, cartesDessinees, dessinee, siege, tableAvec } from './plateau-de-test'

const PRISON = 86
const LILANDRA = 88
const CHOD = 89

const monde = () =>
  tableAvec(siege({ area_hero: [carteSurTable(1, '01001a', 'Hero', 'Spider-Man')] }), {
    area_schemes_side: [
      carteSurTable(PRISON, 'gs119', 'SideScheme', 'Imprisoned on Chandilar'),
      carteSurTable(LILANDRA, 'gs121', 'Ally', 'Lilandra', { bind_object_id: PRISON }),
      carteSurTable(CHOD, 'gs122', 'Ally', "Ch'od", { bind_object_id: PRISON }),
    ],
  })

describe('Imprisoned on Chandilar, STARJAMMER glissés dessous', () => {
  it('dessine la prison', () => {
    expect(dessinee(monde(), PRISON)).toBeDefined()
  })

  it('dessine les alliés glissés, portés par la prison', () => {
    expect(dessinee(monde(), LILANDRA)).toBeDefined()
    expect(dessinee(monde(), CHOD)).toBeDefined()
    expect(dessinee(monde(), LILANDRA)?.portePar).toBe(PRISON)
    expect(dessinee(monde(), CHOD)?.portePar).toBe(PRISON)
  })

  it('les montre FACE VISIBLE (on lit qui est en prison), juste derrière la manigance', () => {
    const vues = cartesDessinees(monde())
    const rang = (id: number) => vues.findIndex((c) => c.id === id)
    expect(rang(LILANDRA)).toBe(rang(PRISON) + 1)
    expect(rang(CHOD)).toBe(rang(PRISON) + 2)
    expect(dessinee(monde(), LILANDRA)?.facedown).toBe(false)
    expect(dessinee(monde(), LILANDRA)?.peeking).toBe(false)
    expect(dessinee(monde(), LILANDRA)?.codeCarte).toBe('gs121')
  })
})
