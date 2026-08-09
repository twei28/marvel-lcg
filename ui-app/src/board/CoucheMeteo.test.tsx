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
import { existsSync, readFileSync } from 'node:fs'
import { dirname, join } from 'node:path'
import { fileURLToPath } from 'node:url'
import {
  CoucheMeteo,
  EFFETS_METEO,
  LIBELLE_EFFET,
  METEO_PAR_CARTE,
  libelleApercu,
  meteoDuMonde,
  meteosDuMonde,
} from './CoucheMeteo'

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
      createElement(CoucheMeteo, { world: undefined, active: false, apercu: ['rain'] })
    )
    expect(src(container)).toBe('/effects/weather/rain.html')
  })

  it('l apercu prime sur la meteo dictee par les cartes', () => {
    const m = monde({ supports: [carte('36005')] })
    const { container } = render(createElement(CoucheMeteo, { world: m, active: true, apercu: ['storm'] }))
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

// Les familles de lieux ajoutees le 8/8/2026. Une carte oubliee ou rangee dans
// la mauvaise famille ne casse rien : elle n'affiche simplement rien, ou la
// mauvaise ambiance. Personne ne le verrait sans ces cas.
describe('les familles de lieux', () => {
  const attendus: Array<[string, string, string]> = [
    ['04080', 'fog', 'Dense Forest'],
    ['16085a', 'fog', 'Library Labyrinth'],
    ['24060', 'fog', 'Back-Alley Enclave'],
    ['24061', 'fog', 'Secret Lair'],
    ['24062', 'fog', 'Sewer Tunnels'],
    ['27077a', 'fog', 'Bell Tower silencieux'],
    ['27077b', 'fog', 'Bell Tower qui sonne'],
    ['16063', 'stars', 'Badoon Ship'],
    ['16085b', 'stars', 'Museum Ship'],
    ['16093', 'stars', "Nebula's Ship"],
    ['16108', 'stars', 'Kree Command Ship'],
    ['16143', 'stars', 'Rogue Vessel'],
    ['45139', 'stars', 'Blue Area of the Moon'],
    ['21076', 'embers', 'Fireball'],
    ['90128', 'embers', 'Burning Building'],
    ['04082', 'dust', 'Rocky Outcrop'],
    ['04083', 'dust', 'Abandoned Facility'],
    ['21079', 'dust', 'Rubblestorm'],
    ['21100b', 'dust', 'Avengers Tower endommagee'],
    ['24063', 'neon', 'Warehouse District'],
    ['27065', 'sandstorm', 'City Streets, la rue de Sandman'],
    ['31037', 'neon', 'Surge in Crime'],
    ['45127', 'jungle', 'The Savage Land'],
    ['45133', 'jungle', 'Genosha'],
    // Mojoverse : le genre se lit aux figurants du paquet, pas au titre
    ['39035', 'noir', 'Dial M for Mojo'],
    ['39041', 'embers', "A Game of Mojo's"],
    ['39047', 'horror', 'The Mojo Files'],
    ['39053', 'cyber', 'Mojo Runner'],
    ['39060', 'sitcom', 'Mojo in the Middle'],
    ['39066', 'sepia', 'Wild Wild Mojo'],
  ]

  it.each(attendus)('%s (%s) : %s', (id, effet) => {
    expect(meteoDuMonde(monde({}, { area_environment: [carte(id)] }))).toBe(effet)
  })

  it('Rubblestorm est de la poussiere, pas du feu', () => {
    expect(meteoDuMonde(monde({}, { area_environment: [carte('21079')] }))).toBe('dust')
  })

  it('la tour des Avengers INTACTE reste sans poussiere', () => {
    // Seule la face endommagee en a une : une tour debout ne s'effrite pas.
    expect(meteoDuMonde(monde({}, { area_environment: [carte('21100a')] }))).toBe('')
  })

  it('les lieux dont l ambiance a ete retiree ne declenchent plus rien', () => {
    // Les trois Manhattan infestes et Skies Over New York : leurs effets ont
    // ete ecrits, juges mauvais, puis retires. Ce cas garde la trace du choix
    // et evite qu'un fichier ressuscite sans qu'on le decide.
    for (const id of ['27117b', '27118b', '27119b', '27116b']) {
      expect(meteoDuMonde(monde({}, { area_environment: [carte(id)] }))).toBe('')
    }
  })

  it('la Roue des genres et la foule restent muettes', () => {
    // Elles sont en jeu EN MEME TEMPS que le decor : leur donner un effet
    // reviendrait a le disputer au genre, puisque la couche n'en montre qu'un.
    for (const id of ['39026a', '39026b', '39003a', '39003b', '39004a', '39004b']) {
      expect(meteoDuMonde(monde({}, { area_environment: [carte(id)] }))).toBe('')
    }
  })

  it('une carte sans ambiance prevue ne declenche rien', () => {
    // 21077 Manipulation et 21078 Pacification sont les deux autres sorts du
    // meme cycle que Rubblestorm : rien ne les rattache a un lieu.
    expect(meteoDuMonde(monde({}, { area_environment: [carte('21077')] }))).toBe('')
    expect(meteoDuMonde(monde({}, { area_environment: [carte('21078')] }))).toBe('')
  })
})

// Le piege du 8/8/2026 : un effet peut etre parfaitement cable cote React et
// n'avoir aucun fichier derriere. L'iframe se cree, la page reste vide, et
// aucun test ne bronche. Le compilateur, lui, ne sait rien des fichiers.
describe('chaque effet a bien son fichier', () => {
  it.each(EFFETS_METEO)('%s.html existe', (effet) => {
    // Chemin construit a la main : `new URL(..., import.meta.url)` serait
    // intercepte par Vite, qui tenterait d'importer le HTML comme un asset.
    const ici = dirname(fileURLToPath(import.meta.url))
    const chemin = join(ici, '../../../Fusion/marvel-lcg-src/public/effects/weather', `${effet}.html`)
    expect(existsSync(chemin)).toBe(true)
  })

  it('chaque effet a un nom affichable', () => {
    for (const effet of EFFETS_METEO) expect(LIBELLE_EFFET[effet]).toBeTruthy()
  })
})

// Auto et Aucun ne disent pas la meme chose, et c'est precisement la confusion
// que ces cas empechent de revenir : avant le 8/8/2026 le selecteur affichait
// « Aucun » pour ce qui etait en fait « Auto », et rien ne permettait de
// couper l'ambiance sans toucher au reglage lui-meme.
describe('les etats de l apercu', () => {
  const src = (c: HTMLElement | null) =>
    [...(c?.querySelectorAll('iframe') ?? [])].map((f) => f.getAttribute('src'))
  const avecCarte = () => monde({ supports: [carte('36005')] })

  it('Auto laisse les cartes en jeu decider', () => {
    const { container } = render(
      createElement(CoucheMeteo, { world: avecCarte(), active: true, apercu: undefined })
    )
    expect(src(container)).toEqual(['/effects/weather/snow.html'])
  })

  it('une liste vide n affiche rien, meme si une carte declencherait un effet', () => {
    const { container } = render(
      createElement(CoucheMeteo, { world: avecCarte(), active: true, apercu: [] })
    )
    expect(container.querySelector('iframe')).toBeNull()
  })

  it('l apercu peut empiler plusieurs effets, c est tout son interet', () => {
    const { container } = render(
      createElement(CoucheMeteo, { world: undefined, active: false, apercu: ['rain', 'fog'] })
    )
    expect(src(container)).toEqual(['/effects/weather/rain.html', '/effects/weather/fog.html'])
  })

  it('le libelle resume l etat sans enumerer', () => {
    expect(libelleApercu(undefined)).toBe('Auto')
    expect(libelleApercu([])).toBe('Aucun')
    expect(libelleApercu(['rain'])).toBe('Pluie')
    expect(libelleApercu(['rain', 'fog', 'snow'])).toBe('3 effets')
  })

  it('chaque effet a un nom affichable', () => {
    for (const effet of EFFETS_METEO) expect(LIBELLE_EFFET[effet]).toBeTruthy()
  })
})

// La superposition, decidee le 8/8/2026 : deux cartes d'ambiance en jeu ne se
// disputent plus l'affichage, elles s'empilent. Avant, la premiere trouvee
// gagnait, et l'ordre venait du moteur : l'ambiance pouvait donc basculer sans
// raison visible quand une carte quittait le jeu.
describe('plusieurs ambiances a la fois', () => {
  it('empile le decor du scenario ET la carte du joueur', () => {
    const m = monde({ supports: [carte('36003')] }, { area_environment: [carte('04081')] })
    // Le scenario d'abord : il est peint EN DESSOUS.
    expect(meteosDuMonde(m)).toEqual(['snow', 'rain'])
  })

  it('ne repete pas deux fois le meme effet', () => {
    // Deux lieux du Hood, tous deux en brume.
    const m = monde({}, { area_environment: [carte('24060'), carte('24062')] })
    expect(meteosDuMonde(m)).toEqual(['fog'])
  })

  it('respecte l ordre des sieges entre joueurs', () => {
    const m = {
      players: [{ supports: [carte('36003')] }, { supports: [carte('36005')] }],
    } as unknown as World
    expect(meteosDuMonde(m)).toEqual(['rain', 'snow'])
  })

  it('l ambiance dominante reste la premiere peinte', () => {
    const m = monde({ supports: [carte('36003')] }, { area_environment: [carte('04081')] })
    expect(meteoDuMonde(m)).toBe('snow')
  })

  it('affiche autant d iframes que d ambiances', () => {
    const m = monde({ supports: [carte('36003')] }, { area_environment: [carte('04081')] })
    const { container } = render(createElement(CoucheMeteo, { world: m, active: true }))
    const sources = [...container.querySelectorAll('iframe')].map((f) => f.getAttribute('src'))
    expect(sources).toEqual(['/effects/weather/snow.html', '/effects/weather/rain.html'])
  })
})
