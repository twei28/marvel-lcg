// Bloc plateau (PROCESSUS-CARTE.md étape 8 bis) : dm011 Arrival of the
// Triple-Evil! (Obligation) met dm009 The Triune Understanding (Support) en
// jeu ATTACHÉ À L'OBLIGATION ELLE-MÊME — pas à l'identité directement — avec
// un compteur acceleration. Même géométrie que le bug Superior Spider-Man
// (su001b/su012/su005, voir attachement-en-chaine.test.ts) : une carte
// attachée à une carte qui n'est pas la racine (`bind_object_id !== 0`). Le
// correctif est déjà générique (`zones.ts`, sous-arbre aplati), ce test
// prouve qu'il couvre bien ce pack-ci.
import { describe, expect, it } from 'vitest'
import { carteSurTable, cartesDessinees, dessinee, siege, tableAvec } from './plateau-de-test'

const IDENTITE = 1
const OBLIGATION = 11
const SUPPORT = 9

const monde = () =>
  tableAvec(
    siege({
      area_hero: [carteSurTable(IDENTITE, 'dm001b', 'AlterEgo', 'Delroy Garrett Jr.')],
      obligations_area: [
        carteSurTable(OBLIGATION, 'dm011', 'Obligation', 'Arrival of the Triple-Evil!', {
          bind_object_id: IDENTITE,
        }),
        carteSurTable(SUPPORT, 'dm009', 'Support', 'The Triune Understanding', {
          bind_object_id: OBLIGATION,
        }),
      ],
    })
  )

describe('dm011 Arrival of the Triple-Evil! — The Triune Understanding attachee a l obligation', () => {
  it('dessine le support attache a l obligation (et non invisible)', () => {
    expect(dessinee(monde(), SUPPORT)).toBeDefined()
  })

  it('le place juste derriere l obligation dans la cascade', () => {
    const vues = cartesDessinees(monde())
    const rang = (id: number) => vues.findIndex((c) => c.id === id)
    expect(rang(SUPPORT)).toBe(rang(OBLIGATION) + 1)
  })

  it('garde l obligation elle-meme visible, comme racine de sa propre unite dans la zone', () => {
    const carte = dessinee(monde(), OBLIGATION)
    expect(carte).toBeDefined()
    expect(carte?.portePar).toBe(0)
  })
})
