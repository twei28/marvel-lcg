// Le journal pendant une annulation (16/11/2026) : ce que l'action annulée avait écrit est barré, une ligne « Action annulée » est posée,
// et la question re-posée ne s'écrit pas comme un nouvel événement.
import { afterEach, describe, expect, it } from 'vitest'
import { renderHook } from '@testing-library/react'
import { useHistoriquePartie } from './HistoriquePartie'
import { useRestauration } from './annulation'
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

const monde = (renderId: number, prompt: string, restaurations = 0, depuis = 0): World =>
  ({ render_id: renderId, round_id: 1, phase: 'Player 1 Turn', prompt, event_name: 'PlayerOnEvent_Text', restaurations, restaure_depuis_render_id: depuis, ...ZONES }) as unknown as World

afterEach(() => window.sessionStorage.clear())

/** Comme la page : la restauration est calculee UNE fois, puis donnee au journal. */
function useJournal(m: World) {
  const restauration = useRestauration(m)
  return useHistoriquePartie(m, undefined, 'p1', restauration)
}

describe('le journal et l’annulation', () => {
  it('barre ce que l’action annulee avait ecrit et pose « Action annulée »', () => {
    const { result, rerender } = renderHook(({ m }) => useJournal(m), { initialProps: { m: monde(10, 'Tour de Spider-Man') } })
    rerender({ m: monde(20, 'Klaw would deal 2 damage') }) // l'action annulee ensuite
    const ligne = (re: RegExp) => result.current.entrees.find((e) => re.test(e.titre))
    expect(ligne(/Klaw would deal/)?.annule, 'avant l’annulation, rien n’est barre').toBeUndefined()
    rerender({ m: monde(30, 'Tour de Spider-Man', 1, 10) }) // annulation : retour a la question du render 10
    expect(ligne(/Klaw would deal/)?.annule, 'l’action annulee est barree').toBe(true)
    expect(ligne(/Tour de Spider-Man/)?.annule, 'ce qui precede l’action reste intact').toBeFalsy()
    const marque = result.current.entrees.find((e) => e.annulation)
    expect(marque?.titre).toBe('Action annulée')
    expect(result.current.entrees.filter((e) => e.annulation)).toHaveLength(1)
  })

  it('la question re-posee apres l’annulation ne reecrit pas de ligne', () => {
    const { result, rerender } = renderHook(({ m }) => useJournal(m), { initialProps: { m: monde(10, 'Tour de Spider-Man') } })
    rerender({ m: monde(20, 'Klaw would deal 2 damage') })
    rerender({ m: monde(30, 'Tour de Spider-Man', 1, 10) })
    const avant = result.current.entrees.length
    rerender({ m: monde(31, 'Tour de Spider-Man', 1, 10) }) // la meme question, re-posee
    expect(result.current.entrees.filter((e) => e.annulation)).toHaveLength(1)
    expect(result.current.entrees.length).toBeLessThanOrEqual(avant + 1)
  })

  it('sans annulation, rien n’est barre', () => {
    const { result, rerender } = renderHook(({ m }) => useJournal(m), { initialProps: { m: monde(10, 'Tour de Spider-Man') } })
    rerender({ m: monde(20, 'Klaw would deal 2 damage') })
    expect(result.current.entrees.some((e) => e.annule || e.annulation)).toBe(false)
  })
})
