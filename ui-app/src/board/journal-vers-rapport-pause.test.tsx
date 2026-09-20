// journal-vers-rapport-pause.test.tsx — I1 (revue finale, 20/09/2026).
//
// ⚠ CE FICHIER EXISTE POUR RELIER LE PRODUCTEUR AU CONSOMMATEUR, et c'est
// tout son objet. Le journal PRODUIT les entrées (`useHistoriquePartie`,
// `ajouterTriche`) ; le rapport de bug les CONSOMME (`construireRapport`,
// qui ne retient dans « GESTES MANUELS » que le type `'manuel'`). Les deux
// étaient testés séparément, et tous les deux verts :
//
//   — `historique-triche-manuel.test.tsx` produit, mais n'interroge que le
//     type de l'entrée, jamais le rapport ;
//   — `rapport-bug.test.ts` consomme, mais INJECTE `type: 'manuel'` à la
//     main, donc sans jamais passer par le producteur.
//
// Entre les deux, personne ne regardait la SEULE configuration que le
// chantier de la pause livre : une partie ORDINAIRE (`mode_manuel` faux) mise
// en PAUSE (`manuel_actif` vrai). Le producteur y écrivait `'triche'`, le
// consommateur cherche `'manuel'` : la section « GESTES MANUELS » n'était
// jamais imprimée, et le journal affichait `[triche]` sous un en-tête qui
// venait de crier « PARTIE CORRIGÉE À LA MAIN ».
//
// Un test qui n'exercerait que la ligne corrigée refermerait le défaut sans
// refermer le TROU : c'est le chaînage des deux modules, en une seule
// mesure, qui le garde.
//
// PIÈGE (voir historique-brut.test.ts) : le monde doit être construit HORS
// du callback de renderHook, sous peine de boucle.
import { act, renderHook } from '@testing-library/react'
import { afterEach, describe, expect, it } from 'vitest'
import { useHistoriquePartie } from './HistoriquePartie'
import { construireRapport, rapportEnTexte } from './rapport-bug'
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

/**
 * Une partie ORDINAIRE mise en PAUSE : la règle `mode_manuel` est FAUSSE
 * (cette partie n'a jamais été déclarée manuelle), l'état `manuel_actif` est
 * VRAI (le moteur s'est tu, le temps qu'on corrige la table). C'est ce que
 * `POST /manuel_pause` produit, et la seule configuration que ce chantier
 * livre.
 */
const EN_PAUSE = {
  render_id: 7, round_id: 3, phase: 'Player 1 Turn',
  prompt: '', event_name: '',
  mode_manuel: false,
  manuel_actif: true,
  corrigee_a_la_main: true,
  ...ZONES,
} as World

const CONTEXTE = { horodatage: '2026-09-20T17:12:00.000Z' }

afterEach(() => window.sessionStorage.clear())

describe('un geste posé en pause de partie ordinaire arrive au rapport (I1)', () => {
  it('imprime la section « GESTES MANUELS », et jamais « [triche] »', () => {
    // LE PRODUCTEUR : le vrai chemin, celui du menu au clic droit et du
    // clavier (`CoucheTriche` appelle `historique.ajouterTriche`).
    const { result } = renderHook(() => useHistoriquePartie(EN_PAUSE, undefined, 'pause:1'))
    act(() => result.current.ajouterTriche('Infliger des dégâts — Rhino'))

    // LE CONSOMMATEUR : sans retoucher une seule entrée entre les deux.
    const rapport = construireRapport(EN_PAUSE, undefined, result.current.entrees, 'partie', CONTEXTE)
    const texte = rapportEnTexte(rapport)

    expect(rapport.gestesManuels.map((g) => g.texte)).toContain('Infliger des dégâts — Rhino')
    expect(texte).toContain('GESTES MANUELS')
    // Les deux histoires contradictoires dans le même document : l'en-tête
    // crie la correction à la main, le journal parlait de triche.
    expect(texte).toContain('PARTIE CORRIGÉE À LA MAIN')
    expect(texte).not.toContain('[triche]')
    expect(texte).toContain('[manuel]')
  })

  it('garde « triche » au bac à sable : le moteur s’y tait pas, rien n’est corrigé', () => {
    const bacASable = { ...EN_PAUSE, manuel_actif: false, corrigee_a_la_main: false, mode_sandbox: true } as World
    const { result } = renderHook(() => useHistoriquePartie(bacASable, undefined, 'sable:1'))
    act(() => result.current.ajouterTriche('Infliger des dégâts — Rhino'))

    const rapport = construireRapport(bacASable, undefined, result.current.entrees, 'partie', CONTEXTE)
    const texte = rapportEnTexte(rapport)

    expect(rapport.gestesManuels).toEqual([])
    expect(texte).not.toContain('GESTES MANUELS')
    expect(texte).toContain('[triche]')
  })
})
