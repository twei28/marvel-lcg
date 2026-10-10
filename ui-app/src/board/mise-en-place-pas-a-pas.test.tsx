import { afterEach, describe, expect, it } from 'vitest'
import { cleanup, fireEvent, render, renderHook } from '@testing-library/react'
import { etapesNouvelles, mechantAttendLaQuestion, ordonnerRetournements, panneauAvantLaFile, type MemoireMiseEnPlace } from './mise-en-place-pas-a-pas'
import { CoucheMiseEnPlace, useMiseEnPlacePasAPas } from './CoucheMiseEnPlace'
import type { World, WorldCard } from './world'

function carte(id: number, card_type: string, extra: Partial<WorldCard> = {}): WorldCard {
  return {
    id,
    card_type,
    pic_id: `p${id}`,
    card_id: `c${id}`,
    name: `Carte ${id}`,
    is_face_up: true,
    is_ready: true,
    visible_for_players: [],
    bind_object_id: 0,
    info: {},
    traits: {},
    buffs: {},
    down_card_ids: [],
    cost: 0,
    ...extra,
  } as WorldCard
}

function monde(render_id: number, parties: Partial<World> & { heros?: WorldCard[]; engages?: WorldCard[] } = {}): World {
  const { heros = [carte(1, 'Hero', { info: { health: 10 } })], engages = [], ...reste } = parties
  return {
    render_id,
    area_villain: [],
    area_schemes_main: [],
    area_schemes_side: [],
    area_environment: [],
    players: [
      {
        area_hero: heros,
        allies: [],
        supports: [],
        engaged_enemies: engages,
        environment_area: [],
      },
    ],
    ...reste,
  } as unknown as World
}

const SANS_PANNEAU = { panneauPrincipale: false, panneauAnnexe: false }
const AVEC_PANNEAUX = { panneauPrincipale: true, panneauAnnexe: true }

describe('etapesNouvelles', () => {
  it('présente chaque carte qui arrive, dans l’ordre de création, sauf l’identité', () => {
    const m = monde(1, {
      area_villain: [carte(20, 'EncounterVillain')],
      area_schemes_main: [carte(10, 'MainScheme')],
    })
    const { etapes } = etapesNouvelles(new Map(), m, SANS_PANNEAU)
    expect(etapes.map((e) => [e.carteId, e.legende])).toEqual([
      [10, 'Manigance principale'],
      [20, 'Méchant'],
    ])
    expect(etapes[0].paysage).toBe(true)
  })

  it('laisse aux panneaux les manigances qu’ils présentent déjà', () => {
    const m = monde(1, {
      area_villain: [carte(20, 'EncounterVillain')],
      area_schemes_main: [carte(10, 'MainScheme')],
      area_schemes_side: [carte(30, 'EncounterSideScheme')],
    })
    const { etapes } = etapesNouvelles(new Map(), m, AVEC_PANNEAUX)
    expect(etapes.map((e) => e.carteId)).toEqual([20])
  })

  it('ne représente pas une carte déjà vue, mais montre le sbire engagé et les dégâts subis', () => {
    const premier = monde(1, { area_villain: [carte(20, 'EncounterVillain')] })
    const { memoire } = etapesNouvelles(new Map(), premier, AVEC_PANNEAUX)
    const second = monde(2, {
      area_villain: [carte(20, 'EncounterVillain')],
      engages: [carte(40, 'Minion')],
      heros: [carte(1, 'Hero', { name: 'Spider-Man', info: { health: 8 } })],
    })
    const avant: MemoireMiseEnPlace = new Map(memoire)
    avant.set(1, { pic: 'p1', pv: 10 })
    const { etapes } = etapesNouvelles(avant, second, AVEC_PANNEAUX)
    expect(etapes.map((e) => [e.carteId, e.legende, e.detail])).toEqual([
      [40, 'Sbire', { cle: 'héros', valeur: 'Spider-Man' }],
      [1, 'Dégâts', { cle: 'dégâts', valeur: 2 }],
    ])
  })

  it('montre le retournement de la manigance principale avec sa menace de départ', () => {
    const avant: MemoireMiseEnPlace = new Map([[10, { pic: 'p10a' }]])
    const m = monde(3, {
      area_schemes_main: [carte(10, 'MainScheme', { pic_id: 'p10b', info: { k_threat: 2 } })],
    })
    const { etapes } = etapesNouvelles(avant, m, AVEC_PANNEAUX)
    expect(etapes.map((e) => [e.legende, e.detail])).toEqual([
      ['Manigance principale retournée', { cle: 'menace de départ', valeur: 2 }],
    ])
  })

  it('ignore une carte face cachée', () => {
    const m = monde(1, { area_villain: [carte(20, 'Villain', { is_face_up: false })] })
    expect(etapesNouvelles(new Map(), m, SANS_PANNEAU).etapes).toEqual([])
  })
})

// L'ORDRE DU LIVRET (Learn to Play, étapes 10 à 12) : le méchant et la
// manigance principale entrent ensemble, 1A puis 2A se montrent d'abord
// (décision de l'utilisateur, 10/10/2026), PUIS les méchants ; la manigance ne
// se retourne qu'après (étape 12), 1B avant 2B. Mesuré sur Tower Defense :
// Proxima et Corvus passaient avant les panneaux, 2B avant 1B.
describe('ordre de la mise en place à plusieurs manigances', () => {
  it('retourne les manigances principales dans l’ordre de la table, pas des numéros de carte', () => {
    const un = carte(50, 'MainScheme', { pic_id: '21098a' })
    const deux = carte(40, 'MainScheme', { pic_id: '21099a' })
    const avant = monde(1, { area_schemes_main: [un, deux] })
    const { memoire } = etapesNouvelles(new Map(), avant, AVEC_PANNEAUX)
    const apres = monde(2, {
      area_schemes_main: [{ ...un, pic_id: '21098b' }, { ...deux, pic_id: '21099b' }],
    })
    const { etapes } = etapesNouvelles(memoire, apres, AVEC_PANNEAUX)
    expect(etapes.map((e) => e.picId)).toEqual(['21098b', '21099b'])
  })

  it('remet dans l’ordre de la table des retournements arrivés dans DEUX trames (2B puis 1B)', () => {
    // Tower Defense : la mise en place de 1A révèle 2A, qui se retourne en 2B
    // AVANT que 1A ne se retourne. Deux trames, 2B d'abord.
    const un = carte(48, 'MainScheme', { pic_id: '21098a' })
    const deux = carte(49, 'MainScheme', { pic_id: '21099a' })
    const tour = carte(84, 'Environment')
    let mem: MemoireMiseEnPlace = etapesNouvelles(new Map(), monde(1, { area_schemes_main: [un, deux] }), AVEC_PANNEAUX).memoire
    const t2 = monde(2, { area_schemes_main: [un, { ...deux, pic_id: '21099b' }], area_environment: [tour] })
    const r2 = etapesNouvelles(mem, t2, AVEC_PANNEAUX)
    mem = r2.memoire
    const t3 = monde(3, { area_schemes_main: [{ ...un, pic_id: '21098b' }, { ...deux, pic_id: '21099b' }], area_environment: [tour] })
    const r3 = etapesNouvelles(mem, t3, AVEC_PANNEAUX)
    const file = ordonnerRetournements([...r2.etapes, ...r3.etapes], t3, 0)
    expect(file.map((e) => e.picId)).toEqual(['p84', '21098b', '21099b'])
  })

  it('un méchant en tête attend la première question du moteur (la trame arrive parfois avant)', () => {
    const mechant = etapesNouvelles(new Map(), monde(1, { area_villain: [carte(20, 'EncounterVillain')] }), AVEC_PANNEAUX)
      .etapes[0]
    const sbire = etapesNouvelles(new Map(), monde(1, { engages: [carte(30, 'Minion')] }), AVEC_PANNEAUX).etapes[0]
    const base = { enMiseEnPlace: true, confirmPrincipale: true, demandePresente: false }
    expect(mechantAttendLaQuestion(mechant, base)).toBe(true)
    expect(mechantAttendLaQuestion(mechant, { ...base, demandePresente: true })).toBe(false)
    expect(mechantAttendLaQuestion(mechant, { ...base, confirmPrincipale: false })).toBe(false)
    expect(mechantAttendLaQuestion(mechant, { ...base, enMiseEnPlace: false })).toBe(false)
    expect(mechantAttendLaQuestion(sbire, base)).toBe(false)
  })

  it('les `figees` premières étapes ne bougent pas', () => {
    const un = carte(48, 'MainScheme', { pic_id: '21098b' })
    const deux = carte(49, 'MainScheme', { pic_id: '21099b' })
    const m = monde(3, { area_schemes_main: [un, deux] })
    const a = { cle: 'a', carteId: 49, picId: '21099b', codeCarte: '', type: 'MainScheme', traits: [], legende: 'x', paysage: true }
    const b = { ...a, cle: 'b', carteId: 48, picId: '21098b' }
    expect(ordonnerRetournements([a, b], m, 1).map((e) => e.cle)).toEqual(['a', 'b'])
  })

  it('le panneau de la manigance PRINCIPALE passe avant un méchant en tête de file', () => {
    const mechant = etapesNouvelles(new Map(), monde(1, { area_villain: [carte(20, 'EncounterVillain')] }), AVEC_PANNEAUX)
      .etapes[0]
    expect(panneauAvantLaFile(mechant, carte(10, 'MainScheme'))).toBe(true)
  })

  it('mais pas avant un sbire, ni pour une manigance annexe (étape 12, après le méchant)', () => {
    const sbire = etapesNouvelles(new Map(), monde(1, { engages: [carte(30, 'Minion')] }), AVEC_PANNEAUX).etapes[0]
    const mechant = etapesNouvelles(new Map(), monde(1, { area_villain: [carte(20, 'EncounterVillain')] }), AVEC_PANNEAUX)
      .etapes[0]
    expect(panneauAvantLaFile(sbire, carte(10, 'MainScheme'))).toBe(false)
    expect(panneauAvantLaFile(mechant, carte(11, 'EncounterSideScheme'))).toBe(false)
    expect(panneauAvantLaFile(undefined, carte(10, 'MainScheme'))).toBe(false)
  })
})

describe('CoucheMiseEnPlace', () => {
  afterEach(cleanup)

  const etape = {
    cle: 'k',
    carteId: 20,
    picId: 'p20',
    codeCarte: '21102',
    type: 'Minion',
    traits: [],
    legende: 'Sbire',
    detail: { cle: 'héros', valeur: 'Spider-Man' },
    paysage: false,
  }

  it('affiche la carte, sa légende, et passe à la suivante avec Continuer ou Espace', () => {
    let appels = 0
    const vue = render(
      <CoucheMiseEnPlace etape={etape} restantes={2} suivant={() => appels++} animations={false} />
    )
    expect(vue.getByText('Sbire')).toBeTruthy()
    expect(vue.getByText(/Spider-Man/)).toBeTruthy()
    fireEvent.click(vue.getByRole('button'))
    expect(appels).toBe(1)
    fireEvent.keyDown(window, { key: ' ' })
    expect(appels).toBe(2)
  })

  it('ne rend rien sans étape', () => {
    const vue = render(<CoucheMiseEnPlace etape={undefined} restantes={0} suivant={() => {}} animations={false} />)
    expect(vue.container.innerHTML).toBe('')
  })
})

describe('useMiseEnPlacePasAPas', () => {
  afterEach(cleanup)
  const m = (r: number) => monde(r, { area_villain: [carte(20, 'EncounterVillain')] })

  it('file les cartes pendant la mise en place quand le mode le permet', () => {
    const { result } = renderHook(() => useMiseEnPlacePasAPas(m(5), { enCours: true, voile: false, muet: false }))
    expect(result.current.etape?.carteId).toBe(20)
  })

  it('ne montre rien hors du mode « Étape par étape » (muet)', () => {
    const { result } = renderHook(() => useMiseEnPlacePasAPas(m(5), { enCours: true, voile: false, muet: true }))
    expect(result.current.etape).toBeUndefined()
  })

  it('ne rejoue pas la table d’une partie déjà commencée', () => {
    const { result } = renderHook(() => useMiseEnPlacePasAPas(m(5), { enCours: false, voile: false, muet: false }))
    expect(result.current.etape).toBeUndefined()
  })
})
