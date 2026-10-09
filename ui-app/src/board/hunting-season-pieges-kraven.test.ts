// Hunting Season, Kraven : les pièges forment des decks supplémentaires (paquet
// Trap et pièges distribués face cachée), et Bear Trap s'attache à l'identité.
import { describe, expect, it } from 'vitest'
import { construirePlateau } from './zones'
import { catalogueVide } from './catalogue'
import { carteSurTable, cartesDessinees, dessinee, siege, tableAvec } from './plateau-de-test'

const HEROS = 1
const PIEGE_ATTACHE = 2
const PAQUET = [20, 21, 22]
const DISTRIBUE = 30

const cachee = (id: number, cardId: string, type: string, nom: string) =>
  carteSurTable(id, cardId, type, nom, { is_face_up: false, visible_for_players: [] })

const monde = () =>
  tableAvec(
    siege({
      area_hero: [
        carteSurTable(HEROS, '01001a', 'Hero', 'Spider-Man'),
        carteSurTable(PIEGE_ATTACHE, 'hs129', 'Attachment', 'Bear Trap', { bind_object_id: HEROS }),
      ],
    }),
    {
      area_villain: [carteSurTable(10, 'hs104', 'Villain', 'Kraven The Hunter')],
      additional_decks: [
        [cachee(20, 'hs125', 'Minion', 'Ferocious Lion'), cachee(21, 'hs133', 'Attachment', 'Quicksand'), cachee(22, 'hs135', 'Treachery', 'Tranquilizer Darts')],
        [cachee(DISTRIBUE, 'hs138', 'Treachery', 'Swinging Boulder')],
      ],
      additional_discard_piles: [[], []],
    }
  )


describe('Kraven : pièges sur le plateau', () => {
  it('dessine Bear Trap attaché au héros', () => {
    expect(dessinee(monde(), PIEGE_ATTACHE)?.portePar).toBe(HEROS)
  })

  it('n écarte aucune carte des paquets de pièges', () => {
    const plateau = construirePlateau(monde(), { playerId: 0, catalogue: catalogueVide })
    expect(plateau.nombreIgnore).toBe(0)
  })

  it('montre les pièges distribués et le paquet face cachée, sans dévoiler leur face', () => {
    const vues = cartesDessinees(monde())
    const piles = vues.filter((c) => [...PAQUET, DISTRIBUE].includes(c.id))
    expect(piles.length).toBeGreaterThan(0)
    for (const c of piles) expect(c.codeCarte).toBeUndefined()
  })
})
