// historique-triche-manuel.test.ts — I4 (revue finale, 20/09/2026).
//
// `ajouterTriche` inscrit une intervention du joueur (menu, clavier, glisser)
// dans le journal, en bac à sable COMME en mode manuel — les deux partagent
// le même menu (`CoucheTriche.tsx`). Avant ce correctif, chaque entrée
// portait toujours `type: 'triche'`, affichée « Triche » : juste en bac à
// sable (une partie truquée sciemment), faux en mode manuel (rien n'est
// truqué, c'est le SEUL moyen de jouer) — un rapport de bug qui porte déjà
// la mention « mode manuel » racontait alors deux histoires contradictoires.
//
// PIÈGE (voir historique-brut.test.ts) : le monde doit être construit HORS
// du callback de renderHook, sous peine de boucle.
import { act, fireEvent, render, renderHook } from '@testing-library/react'
import { afterEach, describe, expect, it, vi } from 'vitest'
import { HistoriquePartie, useHistoriquePartie, type EntreeHistorique } from './HistoriquePartie'
import type { World } from './world'

const ZONES = {
  area_schemes_main: [], main_schemes_deck: [], area_schemes_side: [],
  additional_decks: [], additional_discard_piles: [], area_villain: [],
  villain_deck: [], encounter_deck: [], encounter_discard_pile: [],
  area_boost: [], area_environment: [], area_evidence: [], area_rule: [],
  area_processing: [], area_revealing: [], area_resources: [],
  area_removed: [], area_insert: [], area_set_aside: [],
  victory_display: [], area_status_cards: [], players: [],
  active_card_ids: [],
}

function monde(modeManuel: boolean): World {
  return {
    render_id: 1, round_id: 1, phase: 'Player 1 Turn',
    prompt: '', event_name: '', mode_manuel: modeManuel, ...ZONES,
  } as World
}

const BAC_A_SABLE = monde(false)
const MANUEL = monde(true)

afterEach(() => window.sessionStorage.clear())

describe('le type du journal dépend du mode (I4)', () => {
  it('marque « triche » en bac à sable (mode_manuel faux)', () => {
    const { result } = renderHook(() => useHistoriquePartie(BAC_A_SABLE, undefined, 'a1:1'))
    act(() => result.current.ajouterTriche('Retourner — Rhino'))
    expect(result.current.entrees.at(-1)?.type).toBe('triche')
  })

  it('marque « manuel », jamais « triche », en mode manuel (mode_manuel vrai)', () => {
    const { result } = renderHook(() => useHistoriquePartie(MANUEL, undefined, 'a1:2'))
    act(() => result.current.ajouterTriche('Retourner — Rhino'))
    expect(result.current.entrees.at(-1)?.type).toBe('manuel')
  })
})

const ENTREE_TRICHE: EntreeHistorique = {
  cle: 't:1', type: 'triche', renderId: 1, round: 1, phase: '', titre: 'Retourner — Rhino',
}
const ENTREE_MANUEL: EntreeHistorique = {
  cle: 'm:1', type: 'manuel', renderId: 1, round: 1, phase: '', titre: 'Retourner — Rhino',
}

describe('l’étiquette affichée dépend du type (I4)', () => {
  it('affiche « Triche » pour une entrée de type triche', () => {
    const { getByText, getByRole, queryByText } = render(
      <HistoriquePartie entrees={[ENTREE_TRICHE]} effacer={vi.fn()} />
    )
    fireEvent.click(getByRole('button', { name: /Historique/ }))
    expect(getByText('Triche')).not.toBeNull()
    expect(queryByText('Geste manuel')).toBeNull()
  })

  it('affiche « Geste manuel », jamais « Triche », pour une entrée de type manuel', () => {
    const { getByText, getByRole, queryByText } = render(
      <HistoriquePartie entrees={[ENTREE_MANUEL]} effacer={vi.fn()} />
    )
    fireEvent.click(getByRole('button', { name: /Historique/ }))
    expect(getByText('Geste manuel')).not.toBeNull()
    expect(queryByText('Triche')).toBeNull()
  })
})
