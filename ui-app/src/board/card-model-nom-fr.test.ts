// Defaut signale par l'utilisateur le 11/09/2026 : sur le plateau, la carte
// montrait son illustration francaise (« L'Effraction ! ») et son titre en
// anglais (« THE BREAK-IN! ») juste a cote.
//
// `toScanCard()` est le seul passage de WorldCard vers ce que le plateau
// dessine : c'est donc le seul endroit ou le nom doit etre traduit, et pas les
// quarante lieux d'affichage en aval.

import { afterEach, beforeEach, describe, expect, it } from 'vitest'
import { catalogueVide } from './catalogue'
import { toScanCard } from './card-model'
import { carteSurTable } from './plateau-de-test'
import { CLE_SCANS_FR } from './scans-fr'

const contexte = () => ({
  playerId: 0,
  actives: new Set<number>(),
  catalogue: catalogueVide,
})

beforeEach(() => window.localStorage.removeItem(CLE_SCANS_FR))
afterEach(() => window.localStorage.removeItem(CLE_SCANS_FR))

describe('toScanCard, le nom dessine', () => {
  it('rend le nom francais officiel quand les scans francais sont actifs', () => {
    const carte = carteSurTable(1, '01097a', 'MainScheme', 'The Break-In!')
    expect(toScanCard(carte, contexte()).name).toBe("L'Effraction !")
  })

  it('rend le nom anglais quand le joueur a coupe les scans francais', () => {
    window.localStorage.setItem(CLE_SCANS_FR, 'off')
    const carte = carteSurTable(1, '01097a', 'MainScheme', 'The Break-In!')
    expect(toScanCard(carte, contexte()).name).toBe('The Break-In!')
  })

  it('laisse le nom du moteur aux cartes fan-made, que marvelcdb ne connait pas', () => {
    const carte = carteSurTable(1, 'wd002a', 'SideScheme', 'Shock Party')
    expect(toScanCard(carte, contexte()).name).toBe('Shock Party')
  })
})
