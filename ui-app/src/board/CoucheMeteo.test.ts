// Ce que ces cas protègent : la couche météo doit lire ce qui est EN JEU, et
// rien d'autre. Storm joue avec un deck météo de quatre cartes rangé dans
// `additional_deck` ; si la couche le parcourait, elle afficherait la météo
// d'une carte qui n'est pas sur la table. Le code d'origine parcourait tout
// l'objet joueur, main et decks compris, et ne s'en sortait que parce que
// `supports` précède `additional_deck` dans l'ordre des clés du descripteur.
import { describe, expect, it } from 'vitest'
import type { World } from './world'
import { meteoDuMonde } from './CoucheMeteo'

const carte = (cardId: string) => ({
  id: 1,
  card_id: cardId,
  card_type: 'Support',
  name: cardId,
  bind_object_id: 0,
})

/** Un monde minimal : on ne remplit que les zones qui comptent pour le cas. */
const monde = (joueur: Record<string, unknown>, mondeZones: Record<string, unknown> = {}): World =>
  ({ players: [joueur], ...mondeZones }) as unknown as World

describe('meteoDuMonde', () => {
  it('rend l effet d un soutien météo EN JEU', () => {
    expect(meteoDuMonde(monde({ supports: [carte('36005')] }))).toBe('snow')
  })

  it('ignore une carte météo restée en MAIN', () => {
    expect(meteoDuMonde(monde({ hand_cards: [carte('36004')] }))).toBe('')
  })

  it('ignore le DECK MÉTÉO de Storm, qui contient les trois autres cartes', () => {
    expect(meteoDuMonde(monde({ additional_deck: [carte('36003'), carte('36004')] }))).toBe('')
  })

  it('la carte en jeu l emporte sur celles du deck météo', () => {
    const m = monde({
      supports: [carte('36005')],
      additional_deck: [carte('36003'), carte('36004')],
    })
    expect(meteoDuMonde(m)).toBe('snow')
  })

  it('lit un environnement posé au niveau du MONDE', () => {
    expect(meteoDuMonde(monde({}, { area_environment: [carte('04081')] }))).toBe('snow')
  })

  it('lit un environnement posé dans la zone d un joueur', () => {
    expect(meteoDuMonde(monde({ environment_area: [carte('29039')] }))).toBe('storm')
  })

  it('rend une chaîne vide quand rien ne s applique', () => {
    expect(meteoDuMonde(monde({ supports: [carte('01034')] }))).toBe('')
    expect(meteoDuMonde(undefined)).toBe('')
  })

  it('Clear Skies ne déclenche aucun effet, il n a pas de visuel', () => {
    expect(meteoDuMonde(monde({ supports: [carte('36002')] }))).toBe('')
  })
})
