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
import { texteSignificatif, useHistoriquePartie } from './HistoriquePartie'
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

describe('les noms de cartes du journal, dans la langue du joueur', () => {
  const STAMPEDE = monde('[(61,01106) Stampede] discarded')

  it('affiche le nom francais quand on joue en francais', () => {
    const { result } = renderHook(() => useHistoriquePartie(STAMPEDE, undefined, 'a1:2'))
    const narration = result.current.entrees.find((e) => e.type === 'text')
    expect(narration?.titre).toBe('Ruée discarded')
    expect(narration?.brut).toBe('[(61,01106) Stampede] discarded')
  })

  it('garde le nom anglais quand le francais est coupe', () => {
    window.localStorage.setItem('marvel-board-scans-fr', 'off')
    try {
      const { result } = renderHook(() => useHistoriquePartie(STAMPEDE, undefined, 'a1:3'))
      expect(result.current.entrees.find((e) => e.type === 'text')?.titre).toBe('Stampede discarded')
    } finally {
      window.localStorage.removeItem('marvel-board-scans-fr')
    }
  })
})

// Rapport n°134 (16/11/2026) : le journal francais disait « reçoit 1 compteur(s) « sound » » et « "Too Good to be True" ».
describe('texteSignificatif — noms francais dans le journal (cartes fan-made et compteurs)', () => {
  it('traduit le nom du compteur dans une ligne francaise', () => {
    expect(texteSignificatif('[(19,dz012) "Too Good to be True"] reçoit 1 compteur(s) « sound » ([(1,dz001a) Dazzler])')).toBe(
      '"Trop Beau pour Être Vrai" reçoit 1 compteur(s) « son » (Dazzler)'
    )
    expect(texteSignificatif('[(9,dz002) Longshot] perd 1 compteur(s) « knife »')).toMatch(/« couteau »|« knife »/)
  })

  it('laisse une ligne anglaise intacte', () => {
    expect(texteSignificatif('Longshot loses 1 counter(s) « sound »')).toBe('Longshot loses 1 counter(s) « sound »')
  })
})

// Demande du 16/11/2026 : les restes anglais de la narration (etapes de mise en place, piles, statuts) en francais, pour tous les heros.
describe('texteSignificatif — la mise en place et les piles en francais', () => {
  it('traduit les etapes et les noms de piles', () => {
    expect(texteSignificatif('\n--- Resolve Mulligans ---')).toBe('Résolution des mulligans')
    expect(texteSignificatif("Dazzler's PlayerDeck<39> va être mélangé avec Dazzler's DiscardPile<0>")).toBe(
      'deck de Dazzler va être mélangé avec défausse de Dazzler'
    )
    expect(texteSignificatif('[(9,01001b) Peter Parker] reçoit 1 pion(s) « first_player_token »')).toBe('Peter Parker reçoit 1 pion(s) « premier joueur »')
  })
})
