// Le rapport de bug se vise par OBJECT ID. Or les identifiants du moteur
// (« [(50,01113) Klaw] ») sont effaces des la creation de l'entree, par
// texteSignificatif(). Le journal garde donc le texte BRUT a cote du texte
// propre : l'affichage continue de lire le propre, le rapport lit le brut.
//
// PIEGE : le monde doit etre construit HORS du callback de renderHook. Un
// objet neuf a chaque rendu relance l'effet, qui appelle setEntrees, qui
// redessine, qui reconstruit un objet neuf : la boucle epuise le tas.
import { afterEach, describe, expect, it } from 'vitest'
import { renderHook } from '@testing-library/react'
import { useHistoriquePartie } from './HistoriquePartie'
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

function monde(prompt: string): World {
  return {
    render_id: 1, round_id: 1, phase: 'Player 1 Turn',
    prompt, event_name: 'PlayerOnEvent_Text', ...ZONES,
  }
}

const AVEC_IDENTIFIANTS = monde('[(50,01113) Klaw] would deal 2 damage')
const SANS_NARRATION = monde('')

afterEach(() => window.sessionStorage.clear())

describe('le texte brut du journal', () => {
  it('garde les identifiants du moteur a cote du texte affiche', () => {
    const { result } = renderHook(() => useHistoriquePartie(AVEC_IDENTIFIANTS, undefined, 'a1:1'))
    const narration = result.current.entrees.find((e) => e.type === 'text')
    expect(narration?.titre).toBe('Klaw would deal 2 damage')
    expect(narration?.brut).toBe('[(50,01113) Klaw] would deal 2 damage')
  })

  it("laisse brut absent sur les entrees qui ne viennent pas d'une narration", () => {
    const { result } = renderHook(() => useHistoriquePartie(SANS_NARRATION, undefined, 'a1:1'))
    const phase = result.current.entrees.find((e) => e.type === 'phase')
    expect(phase?.brut).toBeUndefined()
  })
})
