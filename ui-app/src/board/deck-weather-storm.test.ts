// La météo de Storm : la carte Weather EN JEU vit dans la case Weather, avec
// son deck, et la case montre toutes les cartes au survol (01/10/2026).
import { describe, expect, it } from 'vitest'
import { carteSurTable, cartesDessinees, siege, tableAvec } from './plateau-de-test'
import { catalogueVide } from './catalogue'
import { construirePlateau } from './zones'

const meteo = (id: number, nom: string) =>
  carteSurTable(id, `3600${id}`, 'Support', nom, { traits: { t_WEATHER: 1 } })

const monde = () =>
  tableAvec(
    siege({
      area_hero: [carteSurTable(1, '36001b', 'AlterEgo', 'Ororo Munroe')],
      supports: [meteo(2, 'Blizzard'), carteSurTable(9, '01020', 'Support', 'Helicarrier')],
      additional_deck: [meteo(3, 'Orage'), meteo(4, 'Brume')],
    })
  )

describe('la case Weather de Storm', () => {
  const plateau = () => construirePlateau(monde(), { playerId: 0, catalogue: catalogueVide })
  const ids = (cle: string) =>
    plateau()
      .emplacements.find((e) => e.cle === cle)!
      .groupes.flat()
      .map((u) => Number(u.carte.id))

  it('range la météo en jeu dans la case Weather, pas dans les soutiens', () => {
    expect(ids('deck-special')).toContain(2)
    expect(ids('terrain-soutien')).not.toContain(2)
  })

  // Témoin : un soutien ordinaire reste chez les soutiens.
  it('laisse les autres soutiens où ils sont', () => {
    expect(ids('terrain-soutien')).toContain(9)
    expect(ids('deck-special')).not.toContain(9)
  })

  it('glisse les cartes Weather non utilisees SOUS celle en jeu', () => {
    const unites = plateau().emplacements.find((e) => e.cle === 'deck-special')!.groupes.flat()
    const enJeu = unites.find((u) => Number(u.carte.id) === 2)
    expect(enJeu?.attachees.map((c) => Number(c.id))).toEqual([3, 4])
  })

  // Pas deux fois a l'ecran : le deck n'a plus de pile propre tant qu'une
  // meteo est en jeu.
  it('ne redessine pas ces cartes en pile a cote', () => {
    expect(ids('deck-special')).not.toContain(3)
    expect(ids('deck-special')).not.toContain(4)
  })

  // Sans meteo en jeu, le deck reste une pile ordinaire.
  it('garde le deck en pile quand aucune meteo n est en jeu', () => {
    const sans = tableAvec(
      siege({
        area_hero: [carteSurTable(1, '36001b', 'AlterEgo', 'Ororo Munroe')],
        additional_deck: [meteo(3, 'Orage'), meteo(4, 'Brume')],
      })
    )
    const zone = construirePlateau(sans, { playerId: 0, catalogue: catalogueVide }).emplacements.find(
      (e) => e.cle === 'deck-special'
    )
    expect(zone?.groupes.flat().length).toBeGreaterThan(0)
  })

  it('titre la case « Weather »', () => {
    expect(plateau().emplacements.find((e) => e.cle === 'deck-special')?.titre).toBe('Weather')
    expect(cartesDessinees(monde()).length).toBeGreaterThan(0)
  })
})
