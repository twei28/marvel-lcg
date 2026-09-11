// La confirmation « ce coup ne fera rien » (decision utilisateur du 11/09/2026).
//
// Le cas : 15012 Crisis Averted sous une Crise. Le moteur laisse viser le
// complot principal (la carte declare ignorer la Crise... si elle est payee
// avec une mentale), mais le paiement vient APRES le ciblage. Payee sans
// mentale, la carte part en defausse sans rien retirer, et le joueur croyait
// a un bug. Le moteur envoie donc, dans `target_payment`, un `warning`
// {"keyword": "Crisis", "paid_with": "B"} ; le plateau compare les lettres du
// paiement choisi et demande confirmation si aucune ne convient.
import { act, renderHook } from '@testing-library/react'
import { afterEach, describe, expect, it, vi } from 'vitest'
import { coupSansEffet, lireDemande, type Demande, type Option, type Paiement } from './ask'
import type { Catalogue } from './catalogue'
import { textesCoupSansEffet, useInteraction } from './interaction'
import type { World } from './world'

const MENTALE = 65
const PHYSIQUE = 62
const JOKER = 70

function paiement(extra: Partial<Paiement> = {}): Paiement {
  return {
    cost: '3',
    payment: [
      { effect_id: PHYSIQUE, res_text: 'R' },
      { effect_id: MENTALE, res_text: 'B' },
      { effect_id: JOKER, res_text: 'G' },
    ],
    rule: [],
    avertissement: { mot_cle: 'Crisis', ressource: 'B', seulement: false },
    ...extra,
  }
}

describe('coupSansEffet : quand prevenir', () => {
  it('ne dit rien sans avertissement du moteur, quel que soit le paiement', () => {
    expect(coupSansEffet(paiement({ avertissement: undefined }), [PHYSIQUE])).toBeUndefined()
    expect(coupSansEffet(undefined, [PHYSIQUE])).toBeUndefined()
  })

  it('previent quand aucune ressource choisie ne porte la couleur exigee', () => {
    expect(coupSansEffet(paiement(), [PHYSIQUE, PHYSIQUE])).toEqual({ mot_cle: 'Crisis', ressource: 'B', seulement: false })
    // Rien de choisi : on previent aussi, le moteur ne paiera pas mieux a notre place.
    expect(coupSansEffet(paiement(), [])).toBeDefined()
  })

  it('se tait des qu’une mentale, ou un joker, est dans le paiement', () => {
    expect(coupSansEffet(paiement(), [PHYSIQUE, MENTALE])).toBeUndefined()
    expect(coupSansEffet(paiement(), [PHYSIQUE, JOKER])).toBeUndefined()
  })

  it('mode « seulement » (On the Prowl) : une autre couleur dans le paiement suffit a prevenir', () => {
    const seulement = paiement({ avertissement: { mot_cle: 'Crisis', ressource: 'B', seulement: true } })
    expect(coupSansEffet(seulement, [MENTALE, MENTALE])).toBeUndefined()
    expect(coupSansEffet(seulement, [MENTALE, JOKER])).toBeUndefined()
    expect(coupSansEffet(seulement, [MENTALE, PHYSIQUE])).toBeDefined()
    expect(coupSansEffet(seulement, [])).toBeDefined()
  })

  it('lit la couleur du moteur sans se soucier de la casse', () => {
    expect(coupSansEffet(paiement({ avertissement: { mot_cle: 'Crisis', ressource: 'b', seulement: false } }), [MENTALE])).toBeUndefined()
  })
})

describe('lireDemande : le champ warning du moteur', () => {
  const brut = {
    options_json: JSON.stringify([
      {
        id: 3,
        name: 'Play',
        bind_id: 40,
        bind_player_id: 0,
        all_legal_targets: [48],
        target_num_range: [1, 1],
        target_payment: {
          '0': { cost: '3', payment: [{ '62': 'R' }], rule: [], warning: { keyword: 'Crisis', paid_with: 'B', mode: 'only' } },
        },
        select_rule: '',
        target_must_include_traits: [],
        failure_reason: '',
        is_search: false,
      },
      {
        id: 4,
        name: 'Attack',
        bind_id: 40,
        bind_player_id: 0,
        all_legal_targets: [],
        target_num_range: [0, 0],
        target_payment: { '0': { cost: '', payment: [], rule: [], warning: {} } },
        select_rule: '',
        target_must_include_traits: [],
        failure_reason: '',
        is_search: false,
      },
    ]),
    prompt_text: '',
    event_name: 'e',
    show_cancel: true,
    ability_type: '',
  }

  it('devient un avertissement type, et un warning vide n’en cree pas', () => {
    const demande = lireDemande(brut)!
    expect(demande.options[0]!.target_payment[0]!.avertissement).toEqual({ mot_cle: 'Crisis', ressource: 'B', seulement: true })
    expect(demande.options[1]!.target_payment[0]!.avertissement).toBeUndefined()
  })
})

describe('textesCoupSansEffet : les mots, en francais', () => {
  it('nomme la Crise et la couleur exigee', () => {
    const { titre, texte } = textesCoupSansEffet({ mot_cle: 'Crisis', ressource: 'B', seulement: false })
    expect(titre).toBe('Ce coup ne retirera aucune menace')
    expect(texte).toContain('icône de Crise')
    expect(texte).toContain('au moins une ressource de type mental.')
    expect(texte).not.toContain('{ressource}')
    expect(texte).toContain('Continuer quand même ?')
  })

  it('dit « uniquement » en mode seulement, et nomme la Patrouille', () => {
    const { texte } = textesCoupSansEffet({ mot_cle: 'Patrol', ressource: 'B', seulement: true })
    expect(texte).toContain('Patrouille')
    expect(texte).toContain('uniquement avec des ressources de type mental.')
  })
})

// ---- Le hook : la reponse ne part qu'apres confirmation ------------------

const HEROS = 100
const COMPLOT = 48
const CARTE_R = 300
const CARTE_B = 301

function carte(id: number, extra: Record<string, unknown> = {}) {
  return { id, card_type: 'ally', name: `Carte ${id}`, card_id: `0100${id}`, resources: [], info: {}, traits: {}, buffs: {}, ...extra }
}

const MONDE = {
  render_id: 1,
  players: [
    {
      area_hero: [carte(HEROS, { card_type: 'hero' })],
      hand: [
        carte(CARTE_R, { card_type: 'event', resources: [PHYSIQUE] }),
        carte(CARTE_B, { card_type: 'event', resources: [MENTALE] }),
      ],
    },
  ],
} as unknown as World

function optionCrisisAverted(): Option {
  return {
    id: 1,
    name: 'Play',
    bind_id: HEROS,
    bind_player_id: 0,
    all_legal_targets: [COMPLOT],
    target_num_range: [1, 1],
    target_payment: {
      0: {
        cost: '1',
        payment: [
          { effect_id: PHYSIQUE, res_text: 'R' },
          { effect_id: MENTALE, res_text: 'B' },
        ],
        rule: [],
        avertissement: { mot_cle: 'Crisis', ressource: 'B', seulement: false },
      },
    },
    select_rule: '',
    target_must_include_traits: [],
    failure_reason: '',
    is_search: false,
  }
}

const CATALOGUE: Catalogue = {
  pvMax: () => undefined,
  statImprimee: () => undefined,
  motsCles: () => [],
  surpayable: () => false,
} as unknown as Catalogue

function monterLeHook(repondre: ReturnType<typeof vi.fn>) {
  const option = optionCrisisAverted()
  const demande: Demande = { options: [option], refus: [], prompt_text: '', event_name: 'test', show_cancel: true, ability_type: '' }
  const affiches = new Set([HEROS, COMPLOT, CARTE_R, CARTE_B])
  const { result } = renderHook(() => useInteraction(MONDE, demande, repondre, affiches, 0, CATALOGUE, 'simple'))
  act(() => result.current.choisirOption(option, [COMPLOT]))
  return result
}

describe('useInteraction : valider un coup sans effet demande confirmation', () => {
  afterEach(() => {
    vi.restoreAllMocks()
  })

  it('paye en physique : la modale sort, et « Annuler » retient la reponse', async () => {
    const confirm = vi.spyOn(window, 'confirm').mockReturnValue(false)
    const repondre = vi.fn()
    const result = monterLeHook(repondre)
    act(() => result.current.cartes.get(CARTE_R)?.agir?.())
    await act(async () => {
      result.current.valider()
    })
    expect(confirm).toHaveBeenCalledTimes(1)
    expect(confirm.mock.calls[0]![0]).toContain('Crise')
    expect(repondre).not.toHaveBeenCalled()
  })

  it('paye en physique : « Continuer » envoie la reponse telle quelle', async () => {
    vi.spyOn(window, 'confirm').mockReturnValue(true)
    const repondre = vi.fn()
    const result = monterLeHook(repondre)
    act(() => result.current.cartes.get(CARTE_R)?.agir?.())
    await act(async () => {
      result.current.valider()
    })
    expect(repondre).toHaveBeenCalledWith({ id: 1, targets: [COMPLOT], resources: [PHYSIQUE] }, 0)
  })

  it('paye en mental : aucune modale, la reponse part directement', async () => {
    const confirm = vi.spyOn(window, 'confirm')
    const repondre = vi.fn()
    const result = monterLeHook(repondre)
    act(() => result.current.cartes.get(CARTE_B)?.agir?.())
    await act(async () => {
      result.current.valider()
    })
    expect(confirm).not.toHaveBeenCalled()
    expect(repondre).toHaveBeenCalledWith({ id: 1, targets: [COMPLOT], resources: [MENTALE] }, 0)
  })
})
