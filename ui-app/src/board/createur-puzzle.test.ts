// La logique du createur de puzzle : details -> puzzle v2, refus avant envoi, publication.
import { describe, expect, it, vi } from 'vitest'
import {
  DETAILS_VIDES,
  assemblerPuzzle,
  capturerLePlateau,
  erreursDesDetails,
  memoriserMonPuzzle,
  publierSurLeSite,
  urlSitePuzzles,
} from './createur-puzzle'

const bon = { ...DETAILS_VIDES, titre: 'Sauve Peter' }

describe('erreursDesDetails', () => {
  it('accepte un titre et un objectif', () => {
    expect(erreursDesDetails(bon, 1)).toEqual([])
  })
  it('exige un titre', () => {
    expect(erreursDesDetails({ ...bon, titre: '  ' }, 1).join()).toContain('titre')
  })
  it('refuse un objectif « terminer une manigance » sans cible, et un objectif libre sans texte', () => {
    const e = erreursDesDetails(
      { ...bon, objectifs: [{ kind: 'complete_scheme', target: '', text: '' }, { kind: 'free_text', target: '', text: '' }] },
      1
    )
    expect(e).toHaveLength(2)
  })
  it('refuse plus de 6 objectifs, plus de 10 indices et un premier joueur inexistant', () => {
    const objectifs = Array.from({ length: 7 }, () => ({ kind: 'survive' as const, target: '', text: '' }))
    expect(erreursDesDetails({ ...bon, objectifs }, 1).join()).toContain('6 objectifs')
    expect(erreursDesDetails({ ...bon, indices: Array(11).fill('x') }, 1).join()).toContain('10 indices')
    expect(erreursDesDetails({ ...bon, premierJoueur: 2 }, 2).join()).toContain('n’existe pas')
  })
})

describe('assemblerPuzzle', () => {
  const capture = { format: 1, players: [{ identities: ['01001a'] }], villain: ['01094'], puzzle_command: ['Puzzle.Damage(1)'] }
  it('garde la capture et ajoute les details du format 2', () => {
    const p = assemblerPuzzle(capture, {
      ...bon,
      histoire: ' Rhino arrive. ',
      difficulte: 3,
      indices: ['Pense au Stun', '  '],
      objectifs: [{ kind: 'complete_scheme', target: '01097a', text: 'ignoré' }, { kind: 'free_text', target: 'ignoré', text: 'Sans perdre de PV' }],
      modeObjectifs: 'any',
      phaseDeDepart: 'villain',
      solution: ' Frappe deux fois ',
      pseudo: ' Moi ',
    })
    expect(p.villain).toEqual(['01094'])
    expect(p.puzzle_command).toEqual(['Puzzle.Damage(1)'])
    expect(p).toMatchObject({
      format: 2, title: 'Sauve Peter', description: 'Rhino arrive.', difficulty: 3, hints: ['Pense au Stun'], author: 'Moi',
      objectives_mode: 'any', start_phase: 'villain', solution_text: 'Frappe deux fois', has_solution: true,
    })
    expect(p.objectives).toEqual([
      { kind: 'complete_scheme', target: '01097a', text: '' },
      { kind: 'free_text', target: '', text: 'Sans perdre de PV' },
    ])
  })
  it('ne modifie pas la capture et dit « pas de solution » quand elle est vide', () => {
    const p = assemblerPuzzle(capture, bon)
    expect(capture.format).toBe(1)
    expect(p.has_solution).toBe(false)
  })
})

describe('urlSitePuzzles', () => {
  const loc = (hostname: string, port = '') => ({ hostname, protocol: 'https:', port, host: hostname + (port ? ':' + port : '') })
  it('retire le prefixe de la table', () => {
    expect(urlSitePuzzles(loc('p14.narwhalchampions.com'))).toBe('https://narwhalchampions.com')
  })
  it('n\'a pas de site en local', () => {
    expect(urlSitePuzzles(loc('127.0.0.1', '8080'))).toBeNull()
  })
})

describe('capturerLePlateau / publierSurLeSite', () => {
  const reponse = (corps: unknown, ok = true, status = 200) => ({ ok, status, json: async () => corps }) as unknown as Response
  it('rend le puzzle et les avertissements', async () => {
    const f = vi.fn().mockResolvedValue(reponse({ puzzle: { format: 2 }, avertissements: ['x'] }))
    expect(await capturerLePlateau(f as unknown as typeof fetch)).toEqual({ puzzle: { format: 2 }, avertissements: ['x'] })
    expect(f).toHaveBeenCalledWith('/puzzle_capture', { cache: 'no-store' })
  })
  it('explique le refus 409', async () => {
    const f = vi.fn().mockResolvedValue(reponse({}, false, 409))
    await expect(capturerLePlateau(f as unknown as typeof fetch)).rejects.toThrow('table de création')
  })
  it('publie sur le site avec le pseudo, sans cookie', async () => {
    const f = vi.fn().mockResolvedValue(reponse({ code: 'PZ-ABCD', cle: 'k', expire_le: 5 }, true, 201))
    const pub = await publierSurLeSite({ format: 2 }, 'Moi', { site: 'https://s.test', f: f as unknown as typeof fetch })
    expect(pub).toEqual({ code: 'PZ-ABCD', cle: 'k', expire_le: 5 })
    const [url, options] = f.mock.calls[0]
    expect(url).toBe('https://s.test/api/puzzle/publier')
    expect(options.credentials).toBe('omit')
    expect(JSON.parse(options.body)).toEqual({ puzzle: { format: 2 }, pseudo: 'Moi' })
  })
  it('rend les raisons de refus du site, ou dit qu\'on est hors ligne', async () => {
    const f = vi.fn().mockResolvedValue(reponse({ erreur: ['titre vide', 'trop long'] }, false, 400))
    await expect(publierSurLeSite({}, '', { site: 'https://s.test', f: f as unknown as typeof fetch })).rejects.toThrow('titre vide ; trop long')
    await expect(publierSurLeSite({}, '', { site: null })).rejects.toThrow('hors ligne')
  })
})

describe('memoriserMonPuzzle', () => {
  it('ajoute le puzzle en tete de « Mes puzzles » sans doublon', () => {
    const memoire: Record<string, string> = {}
    const stockage = { getItem: (k: string) => memoire[k] ?? null, setItem: (k: string, v: string) => { memoire[k] = v } }
    memoriserMonPuzzle({ code: 'PZ-1', cle: 'a', titre: 'Un' }, stockage)
    memoriserMonPuzzle({ code: 'PZ-2', cle: 'b', titre: 'Deux' }, stockage)
    memoriserMonPuzzle({ code: 'PZ-1', cle: 'a2', titre: 'Un bis' }, stockage)
    const liste = JSON.parse(memoire['mc-puzzles-crees'])
    expect(liste.map((x: { code: string }) => x.code)).toEqual(['PZ-1', 'PZ-2'])
    expect(liste[0].cle).toBe('a2')
  })
})
