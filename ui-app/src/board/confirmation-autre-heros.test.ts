// La confirmation « tu regardes un héros, l'action va agir pour un autre »
// (24/09/2026, demande de l'utilisateur, capture à l'appui) : cliquer Fin du
// tour (ou n'importe quelle action) en regardant le plateau de She-Hulk ne
// doit pas terminer le tour de Shuri sans le dire. Couvre `valider` (une
// action composée) et `annuler` (Fin du tour / passer), dans les deux sens :
// le message nomme les deux héros, Annuler bloque l'envoi, Continuer laisse
// passer.
import { act, renderHook } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import type { Demande, Option } from './ask'
import type { Catalogue } from './catalogue'
import { CLE_VALIDATION_COURTE, useInteraction } from './interaction'
import type { World } from './world'

const SHURI = 0
const SHE_HULK = 1

function carte(id: number, nom: string, extra: Record<string, unknown> = {}) {
  return {
    id,
    card_type: 'hero',
    name: nom,
    card_id: `0100${id}`,
    resources: [],
    info: {},
    traits: {},
    buffs: {},
    ...extra,
  }
}

/** Deux héros sur la même table, un par siège. */
const MONDE = {
  render_id: 1,
  players: [
    { area_hero: [carte(100, 'Shuri')], hand: [] },
    { area_hero: [carte(101, 'She-Hulk')], hand: [] },
  ],
} as unknown as World

const CATALOGUE: Catalogue = {
  pvMax: () => undefined,
  statImprimee: () => undefined,
  motsCles: () => [],
  surpayable: () => false,
  type: () => undefined,
} as unknown as Catalogue

/** Une action sans coût ni cible, liée au siège de Shuri (0). */
function actionDeShuri(): Option {
  return {
    id: 1,
    name: 'Play',
    bind_id: 100,
    bind_player_id: 0,
    all_legal_targets: [],
    target_num_range: [0, 0],
    target_payment: {},
    select_rule: '',
    target_must_include_traits: [],
    failure_reason: '',
    is_search: false,
  }
}

function monter(joueurAffiche: number, options: Option[] = []) {
  const repondre = vi.fn()
  const demande: Demande = {
    options: options.length ? options : [actionDeShuri()],
    refus: [],
    prompt_text: '',
    event_name: 'test',
    show_cancel: true,
    ability_type: '',
  }
  const rendu = renderHook(() =>
    useInteraction(MONDE, demande, repondre, new Set([100, 101]), joueurAffiche, CATALOGUE, 'simple')
  )
  return { ...rendu, repondre }
}

afterEach(() => {
  vi.unstubAllGlobals()
})

describe('Fin du tour (annuler) : héros affiché ≠ héros dont c’est le tour', () => {
  it('prévient, nomme les deux héros, et Annuler ne termine rien', async () => {
    vi.stubGlobal('confirm', vi.fn(() => false))
    // Affiche She-Hulk (1), mais la demande active est liée à Shuri (0).
    const { result, repondre } = monter(SHE_HULK)
    await act(async () => {
      result.current.annuler()
      await Promise.resolve()
    })
    expect(window.confirm).toHaveBeenCalledOnce()
    const texte = (window.confirm as ReturnType<typeof vi.fn>).mock.calls[0]![0] as string
    expect(texte).toMatch(/Shuri/)
    expect(texte).toMatch(/She-Hulk/)
    expect(repondre).not.toHaveBeenCalled()
  })

  it('Continuer quand même termine bien le tour de Shuri', async () => {
    vi.stubGlobal('confirm', vi.fn(() => true))
    const { result, repondre } = monter(SHE_HULK)
    await act(async () => {
      result.current.annuler()
      await Promise.resolve()
    })
    expect(repondre).toHaveBeenCalledWith(null, 0)
  })

  it('aucune confirmation quand le héros affiché est bien celui dont c’est le tour', () => {
    vi.stubGlobal('confirm', vi.fn(() => false))
    const { result, repondre } = monter(SHURI)
    act(() => result.current.annuler())
    expect(window.confirm).not.toHaveBeenCalled()
    expect(repondre).toHaveBeenCalledWith(null, 0)
  })
})

describe('Valider une action composée : héros affiché ≠ héros ciblé par l’action', () => {
  // Validation courte OFF ici : une action sans coût ni cible se valide
  // toute seule dès `choisirOption` (voir `validationEvidente` dans
  // interaction.ts), ce qui appellerait `valider()` une première fois avant
  // même l'appel explicite du test — la confirmation serait alors demandée
  // deux fois pour un seul clic.
  beforeEach(() => window.localStorage.setItem(CLE_VALIDATION_COURTE, 'off'))
  afterEach(() => window.localStorage.removeItem(CLE_VALIDATION_COURTE))

  it('prévient avant d’envoyer, et Annuler n’envoie rien', async () => {
    vi.stubGlobal('confirm', vi.fn(() => false))
    const { result, repondre } = monter(SHE_HULK)
    act(() => result.current.choisirOption(actionDeShuri()))
    await act(async () => {
      result.current.valider()
      await Promise.resolve()
    })
    expect(window.confirm).toHaveBeenCalledOnce()
    expect(repondre).not.toHaveBeenCalled()
  })

  it('Continuer quand même envoie la réponse pour Shuri', async () => {
    vi.stubGlobal('confirm', vi.fn(() => true))
    const { result, repondre } = monter(SHE_HULK)
    act(() => result.current.choisirOption(actionDeShuri()))
    await act(async () => {
      result.current.valider()
      await Promise.resolve()
    })
    expect(repondre).toHaveBeenCalledWith({ id: 1, targets: [], resources: [] }, 0)
  })

  it('aucune confirmation quand l’action est bien pour le héros affiché', () => {
    vi.stubGlobal('confirm', vi.fn(() => false))
    const { result, repondre } = monter(SHURI)
    act(() => result.current.choisirOption(actionDeShuri()))
    act(() => result.current.valider())
    expect(window.confirm).not.toHaveBeenCalled()
    expect(repondre).toHaveBeenCalledWith({ id: 1, targets: [], resources: [] }, 0)
  })
})
