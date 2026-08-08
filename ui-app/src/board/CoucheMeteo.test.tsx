// Ce que ces cas protègent : la couche météo doit lire ce qui est EN JEU, et
// rien d'autre. Storm joue avec un deck météo de quatre cartes rangé dans
// `additional_deck` ; si la couche le parcourait, elle afficherait la météo
// d'une carte qui n'est pas sur la table. Le code d'origine parcourait tout
// l'objet joueur, main et decks compris, et ne s'en sortait que parce que
// `supports` précède `additional_deck` dans l'ordre des clés du descripteur.
import { describe, expect, it } from 'vitest'
import { render } from '@testing-library/react'
import { createElement } from 'react'
import type { World } from './world'
import { CoucheMeteo, meteoDuMonde } from './CoucheMeteo'

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

// L'apercu est un OUTIL : il doit montrer l'effet meme quand le joueur a coupe
// la meteo dans ses reglages. Sans ces cas, la dependance a l'interrupteur
// reviendrait en silence et l'outil paraitrait casse, ce qui est exactement ce
// qui s'est produit le 8/8/2026.
describe('CoucheMeteo, apercu et interrupteur', () => {
  const src = (c: HTMLElement | null) => c?.querySelector('iframe')?.getAttribute('src') ?? null

  it('affiche l apercu meme quand la meteo est coupee', () => {
    const { container } = render(
      createElement(CoucheMeteo, { world: undefined, active: false, apercu: 'rain' })
    )
    expect(src(container)).toBe('/effects/weather/rain.html')
  })

  it('l apercu prime sur la meteo dictee par les cartes', () => {
    const m = monde({ supports: [carte('36005')] })
    const { container } = render(createElement(CoucheMeteo, { world: m, active: true, apercu: 'storm' }))
    expect(src(container)).toBe('/effects/weather/storm.html')
  })

  it('sans apercu, l interrupteur coupe bien la meteo du jeu', () => {
    const m = monde({ supports: [carte('36005')] })
    const { container } = render(createElement(CoucheMeteo, { world: m, active: false }))
    expect(container.querySelector('iframe')).toBeNull()
  })

  it('sans apercu et interrupteur allume, la carte en jeu decide', () => {
    const m = monde({ supports: [carte('36005')] })
    const { container } = render(createElement(CoucheMeteo, { world: m, active: true }))
    expect(src(container)).toBe('/effects/weather/snow.html')
  })
})
