// Les cartes ACCROCHEES a Hellcat doivent etre dessinees (etape 8 bis de
// PROCESSUS-CARTE, lecon Contingency Plan).
//
// Hellcat (`hc001a`, pack custom jakxin, 11/09/2026) glisse sous son identite
// les evenements a ressource mentale qu'elle joue (Response), Hedy Wolfe
// (`hc011`) en remonte de la defausse. Le moteur les emet dans `area_hero`
// a la suite de l'identite, FACE VISIBLE, lies par `bind_object_id` : meme
// mecanisme que les cartes glissees sous une manigance (Highway Robbery,
// The Mother of Night), mais sous un HEROS, et face visible.
//
// Le joueur compte ces cartes en jeu (Illusion, Empowered) : une carte
// accrochee invisible rendrait le pack injouable a l'oeil, cas vert ou pas.
import { describe, expect, it } from 'vitest'
import { carteSurTable, cartesDessinees, dessinee, siege, tableAvec } from './plateau-de-test'

const HELLCAT = 1
const HELLUVA = 12
const GENIUS = 81

const monde = () =>
  tableAvec(
    siege({
      area_hero: [
        carteSurTable(HELLCAT, 'hc001a', 'Hero', 'Hellcat'),
        carteSurTable(HELLUVA, 'hc005', 'Event', 'Helluva Punch', {
          bind_object_id: HELLCAT,
          is_face_up: true,
        }),
        carteSurTable(GENIUS, '01089', 'Resource', 'Genius', {
          bind_object_id: HELLCAT,
          is_face_up: true,
        }),
      ],
    })
  )

describe('Hellcat, cartes accrochees a l’identite', () => {
  it('dessine Hellcat', () => {
    expect(dessinee(monde(), HELLCAT)).toBeDefined()
  })

  it('dessine les deux cartes accrochees, portees par Hellcat', () => {
    expect(dessinee(monde(), HELLUVA)).toBeDefined()
    expect(dessinee(monde(), GENIUS)).toBeDefined()
    expect(dessinee(monde(), HELLUVA)?.portePar).toBe(HELLCAT)
    expect(dessinee(monde(), GENIUS)?.portePar).toBe(HELLCAT)
  })

  it('les montre face visible, juste derriere Hellcat', () => {
    const vues = cartesDessinees(monde())
    const rang = (id: number) => vues.findIndex((c) => c.id === id)
    expect(rang(HELLUVA)).toBe(rang(HELLCAT) + 1)
    expect(rang(GENIUS)).toBe(rang(HELLCAT) + 2)
    expect(dessinee(monde(), HELLUVA)?.facedown).toBe(false)
    expect(dessinee(monde(), HELLUVA)?.peeking).toBe(false)
  })
})
