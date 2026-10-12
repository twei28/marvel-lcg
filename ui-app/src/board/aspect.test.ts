// Ce que ces cas protegent : sous le noir et blanc, la couleur du cadre d'une
// carte disparait, et c'est elle qui dit si la carte est basique, d'aspect ou
// de heros. Le lisere qui la remplace ne vaut que si l'aspect lu dans le
// catalogue est juste — une carte mal classee tromperait le joueur plus
// surement qu'une carte sans lisere.
import { describe, expect, it } from 'vitest'
import { readFileSync } from 'node:fs'
import { dirname, join } from 'node:path'
import { fileURLToPath } from 'node:url'
import { aspectDeClasse } from './catalogue'
import { EFFETS_DELAVANTS, effetsAffiches } from './CoucheMeteo'
import type { World } from './world'

describe('aspectDeClasse', () => {
  it('reconnait les quatre aspects, le Pool et Determination', () => {
    expect(aspectDeClasse('Aggression')).toBe('aggression')
    expect(aspectDeClasse('Justice')).toBe('justice')
    expect(aspectDeClasse('Leadership')).toBe('leadership')
    expect(aspectDeClasse('Protection')).toBe('protection')
    expect(aspectDeClasse("'Pool")).toBe('pool')
    expect(aspectDeClasse('Determination')).toBe('determination')
  })

  it('reconnait heros et basique', () => {
    expect(aspectDeClasse('Hero')).toBe('hero')
    expect(aspectDeClasse('Basic')).toBe('basic')
  })

  it('un aspect l emporte sur Hero, qui l emporte sur Basic', () => {
    // Quatre cartes du catalogue portent « Hero;<aspect> ». C'est l'aspect qui
    // est l'information rare, donc celle qu'il faut montrer.
    expect(aspectDeClasse('Hero;Aggression')).toBe('aggression')
    expect(aspectDeClasse('Hero;Justice')).toBe('justice')
    expect(aspectDeClasse('Campaign;Basic')).toBe('basic')
    expect(aspectDeClasse('Basic;Campaign')).toBe('basic')
  })

  it('ignore ce qui ne dit rien de la couleur du cadre', () => {
    expect(aspectDeClasse('Campaign')).toBeUndefined()
    expect(aspectDeClasse('Encounter')).toBeUndefined()
    expect(aspectDeClasse(undefined)).toBeUndefined()
    expect(aspectDeClasse('')).toBeUndefined()
  })
})

// Le catalogue reel, pas un echantillon : c'est la seule facon de savoir que
// la lecture de `desc.Class` colle vraiment aux donnees du jeu.
describe('le catalogue reel', () => {
  const cartes = (() => {
    const ici = dirname(fileURLToPath(import.meta.url))
    const base = join(ici, '../../../Fusion/marvel-lcg-src/data')
    const sortie: Array<{ card_id?: string; desc?: Record<string, string> }> = []
    for (const nom of ['cards.json', 'cards_custom.json']) {
      const brut = JSON.parse(readFileSync(join(base, nom), 'utf-8')) as Record<string, unknown[]>
      for (const liste of Object.values(brut)) {
        for (const c of liste) if (c && typeof c === 'object') sortie.push(c as { card_id?: string })
      }
    }
    return sortie
  })()

  it('a bien ete charge', () => {
    expect(cartes.length).toBeGreaterThan(4000)
  })

  it('classe plus de mille cartes de joueur', () => {
    const classees = cartes.filter((c) => aspectDeClasse(c.desc?.Class)).length
    expect(classees).toBeGreaterThan(1000)
  })

  it('ne laisse aucune valeur de Class inconnue sans explication', () => {
    // Toute valeur qui n'est ni un aspect, ni Hero, ni Basic doit etre une
    // combinaison de Campaign et Encounter : si une nouvelle valeur apparait
    // un jour dans les donnees, ce cas la signale au lieu de la perdre.
    const inconnues = new Set<string>()
    for (const c of cartes) {
      const brut = c.desc?.Class
      if (!brut || aspectDeClasse(brut)) continue
      for (const p of brut.split(';')) if (!['Campaign', 'Encounter'].includes(p.trim())) inconnues.add(p)
    }
    expect([...inconnues]).toEqual([])
  })
})

describe('effetsAffiches', () => {
  const monde = (...cardIds: string[]): World =>
    ({
      area_environment: cardIds.map((cardId, i) => ({
        id: i + 1,
        card_id: cardId,
        card_type: 'Support',
        name: cardId,
        bind_object_id: 0,
      })),
    }) as unknown as World

  it('rend l effet des cartes quand la meteo est allumee', () => {
    // 01034 Stark Tower n'a aucune ambiance : c'est un Soutien de heros.
    expect(effetsAffiches(monde('01034'), true)).toEqual([])
    expect(effetsAffiches(monde('04081'), true)).toEqual(['snow'])
  })

  it('l apercu prime, et « aucun » impose le vide', () => {
    expect(effetsAffiches(monde('04081'), true, ['fog'])).toEqual(['fog'])
    expect(effetsAffiches(monde('04081'), true, [])).toEqual([])
  })

  it('l apercu impose exactement sa liste, quelles que soient les cartes', () => {
    expect(effetsAffiches(monde('04081', '21076'), true, ['rain'])).toEqual(['rain'])
    expect(effetsAffiches(monde('04081'), true, ['rain', 'fog'])).toEqual(['rain', 'fog'])
  })

  it('aucun effet ne delave depuis le retrait du noir et blanc (12/10/2026)', () => {
    expect(EFFETS_DELAVANTS).toEqual([])
  })
})
