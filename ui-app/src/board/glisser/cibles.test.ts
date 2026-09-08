import { describe, expect, it } from 'vitest'
import type { Option } from '../ask'
import {
  ciblesDeLaSource,
  estSourceGlissable,
  optionsDuDepot,
  optionsSansCible,
  raisonDuRefus,
  zonesDeLaSource,
} from './cibles'

function option(partiel: Partial<Option>): Option {
  return {
    id: 1,
    name: 'Action',
    bind_id: 0,
    bind_player_id: 0,
    all_legal_targets: [],
    target_num_range: [0, 0],
    target_payment: {},
    select_rule: '',
    target_must_include_traits: [],
    failure_reason: '',
    is_search: false,
    ...partiel,
  }
}

const HEROS = 10
const RHINO = 20
const SBIRE = 21
const MANIGANCE = 30

describe('ce qu on peut soulever', () => {
  it('une carte qui porte une action offerte se souleve', () => {
    const options = [option({ bind_id: HEROS, all_legal_targets: [RHINO], target_num_range: [1, 1] })]
    expect(estSourceGlissable(options, HEROS)).toBe(true)
  })

  it('une carte dont la seule action est refusee ne se souleve pas', () => {
    const options = [
      option({ bind_id: HEROS, all_legal_targets: [RHINO], target_num_range: [1, 1], failure_reason: 'epuise' }),
    ]
    expect(estSourceGlissable(options, HEROS)).toBe(false)
  })

  it('une carte sans action ne se souleve pas', () => {
    const options = [option({ bind_id: SBIRE, target_num_range: [1, 1], all_legal_targets: [RHINO] })]
    expect(estSourceGlissable(options, HEROS)).toBe(false)
  })

  // ⚠ LE CAS QUI COMPTE POUR LE HEROS. Les actions generales du moteur portent
  // `bind_id === 0` : sans ce rattachement a l'identite, soulever son heros ne
  // proposerait que ses capacites imprimees, jamais l'attaque de base.
  it('les actions generales sont rattachees a l identite', () => {
    const options = [option({ bind_id: 0, all_legal_targets: [RHINO], target_num_range: [1, 1] })]
    expect(estSourceGlissable(options, HEROS, HEROS)).toBe(true)
    expect(estSourceGlissable(options, SBIRE, HEROS)).toBe(false)
  })
})

describe('ou l on peut lacher', () => {
  const options = [
    option({ id: 1, bind_id: HEROS, all_legal_targets: [RHINO, SBIRE], target_num_range: [1, 1] }),
    option({ id: 2, bind_id: HEROS, all_legal_targets: [MANIGANCE], target_num_range: [1, 1] }),
  ]
  const affiches = new Set([HEROS, RHINO, SBIRE, MANIGANCE])

  it('reunit les cibles de toutes les actions de la source', () => {
    expect([...ciblesDeLaSource(options, HEROS, affiches)].sort()).toEqual([RHINO, SBIRE, MANIGANCE].sort())
  })

  // ⚠ TEMOIN. Une cible legale enfouie dans une pile n'est pas dessinee : on ne
  // peut pas glisser vers ce qu'on ne voit pas, et l'allumer mentirait.
  it('ecarte une cible qui n est pas dessinee', () => {
    const partiel = new Set([HEROS, RHINO])
    expect([...ciblesDeLaSource(options, HEROS, partiel)]).toEqual([RHINO])
  })

  it('ne se propose jamais elle-meme', () => {
    const surSoi = [option({ bind_id: HEROS, all_legal_targets: [HEROS, RHINO], target_num_range: [1, 1] })]
    expect([...ciblesDeLaSource(surSoi, HEROS, affiches)]).toEqual([RHINO])
  })

  it('une action refusee n allume aucune cible', () => {
    const refusee = [
      option({ bind_id: HEROS, all_legal_targets: [RHINO], target_num_range: [1, 1], failure_reason: 'epuise' }),
    ]
    expect(ciblesDeLaSource(refusee, HEROS, affiches).size).toBe(0)
  })

  it('une action sans cible n allume aucune carte', () => {
    const allie = [option({ bind_id: 99, target_num_range: [0, 0] })]
    expect(ciblesDeLaSource(allie, 99, affiches).size).toBe(0)
  })
})

describe('ce que le lacher declenche', () => {
  it('une seule action vers la cible : elle est rendue seule', () => {
    const options = [
      option({ id: 1, bind_id: HEROS, all_legal_targets: [RHINO], target_num_range: [1, 1] }),
      option({ id: 2, bind_id: HEROS, all_legal_targets: [MANIGANCE], target_num_range: [1, 1] }),
    ]
    expect(optionsDuDepot(options, HEROS, RHINO).map((o) => o.id)).toEqual([1])
  })

  it('plusieurs actions vers la meme cible : toutes rendues, au plateau de trancher', () => {
    const options = [
      option({ id: 1, name: 'Attaque', bind_id: HEROS, all_legal_targets: [RHINO], target_num_range: [1, 1] }),
      option({ id: 2, name: 'Capacite', bind_id: HEROS, all_legal_targets: [RHINO], target_num_range: [1, 1] }),
    ]
    expect(optionsDuDepot(options, HEROS, RHINO).map((o) => o.id)).toEqual([1, 2])
  })

  it('aucune action vers cette cible : rien', () => {
    const options = [option({ bind_id: HEROS, all_legal_targets: [MANIGANCE], target_num_range: [1, 1] })]
    expect(optionsDuDepot(options, HEROS, RHINO)).toEqual([])
  })

  it('les actions sans cible se rangent a part', () => {
    const options = [
      option({ id: 1, bind_id: 99, target_num_range: [0, 0] }),
      option({ id: 2, bind_id: 99, all_legal_targets: [RHINO], target_num_range: [1, 1] }),
    ]
    expect(optionsSansCible(options, 99).map((o) => o.id)).toEqual([1])
  })
})

describe('pourquoi un lacher est refuse', () => {
  // ⚠ LE CAS QUI COMPTE : le moteur a DEJA formule le refus. L'inventer nous
  // ferait mentir des qu'une regle nous echappe.
  it('rend la raison du moteur quand elle nomme la cible', () => {
    const options = [
      option({
        bind_id: HEROS,
        all_legal_targets: [RHINO],
        target_num_range: [1, 1],
        failure_reason: 'Un Gardien vous en empeche',
      }),
    ]
    expect(raisonDuRefus(options, HEROS, RHINO)).toBe('Un Gardien vous en empeche')
  })

  it('se rabat sur la raison de la source quand la cible n est nommee nulle part', () => {
    const options = [
      option({ bind_id: HEROS, all_legal_targets: [MANIGANCE], target_num_range: [1, 1], failure_reason: 'deja epuise' }),
    ]
    expect(raisonDuRefus(options, HEROS, RHINO)).toBe('deja epuise')
  })

  it('ne dit rien quand le moteur n a rien a dire', () => {
    const options = [option({ bind_id: HEROS, all_legal_targets: [MANIGANCE], target_num_range: [1, 1] })]
    expect(raisonDuRefus(options, HEROS, RHINO)).toBeUndefined()
  })
})

describe('les zones qui acceptent la carte', () => {
  const IDENTITE = 40
  const AUTRE = 41
  // L'aire du heros contient l'identite ; la ligne de combat, deux allies.
  const zoneDe = (id: number) =>
    id === IDENTITE ? 'terrain-soutien' : id === AUTRE || id === RHINO ? 'terrain-combat' : undefined

  // ⚠ LE CAS QUI COMPTE, ET IL VIENT D'UNE PARTIE REELLE : jouer une carte de
  // la main est une option qui VISE l'identite. Une regle ecrite sur le type de
  // carte (« un allie va dans la ligne de combat ») se trompait sur toutes les
  // cartes de la main.
  it('une zone qui contient la cible legale accepte la carte', () => {
    const jouer = [option({ bind_id: 99, all_legal_targets: [IDENTITE], target_num_range: [1, 1] })]
    expect([...zonesDeLaSource(jouer, 99, zoneDe)]).toEqual([['terrain-soutien', IDENTITE]])
  })

  it('une zone qui en contient DEUX reste ambigue, donc refusee', () => {
    const deux = [option({ bind_id: 99, all_legal_targets: [AUTRE, RHINO], target_num_range: [1, 1] })]
    expect(zonesDeLaSource(deux, 99, zoneDe).size).toBe(0)
  })

  it('une action refusee n ouvre aucune zone', () => {
    const refusee = [
      option({ bind_id: 99, all_legal_targets: [IDENTITE], target_num_range: [1, 1], failure_reason: 'trop cher' }),
    ]
    expect(zonesDeLaSource(refusee, 99, zoneDe).size).toBe(0)
  })

  it('une cible hors de toute zone dessinee n ouvre rien', () => {
    const ailleurs = [option({ bind_id: 99, all_legal_targets: [999], target_num_range: [1, 1] })]
    expect(zonesDeLaSource(ailleurs, 99, zoneDe).size).toBe(0)
  })
})
