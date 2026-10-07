import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { analyserRelecture, appliquer, FichierInvalide, lireRelecture } from './fichier'
import { Lecteur, reperesDe } from './lecteur'
import type { EtatMoteur } from '../moteur'

const ligne = (o: unknown) => JSON.stringify(o)

const carte = (id: number, name: string) => ({ id, name })
const monde = (render_id: number, extra: Record<string, unknown> = {}) => ({
  render_id,
  round_id: 1,
  phase: 'Player 1 Turn',
  prompt: '',
  players: [{ area_hero: [carte(1, 'Spider-Man')], allies: [carte(10, 'Black Cat')], player_discard_pile: [] }],
  ...extra,
})

const OPTIONS = JSON.stringify([{ id: 1, name: 'Defense', bind_id: 1, bind_player_id: 0, all_legal_targets: [49], target_num_range: [0, 1] }])

function fichierTexte() {
  return [
    ligne({ k: 'entete', format: 1, scenario: 'Rhino', joueurs: [{ heros: 'Spider-Man' }], resultat: 'victoire', rounds: 2 }),
    ligne({ k: 'cle', r: 1, t: 1000, m: monde(1) }),
    ligne({ k: 'd', r: 2, t: 2000, d: { o: { render_id: { v: 2 }, prompt: { v: 'Spider-Man joue Black Cat' } } } }),
    ligne({ k: 'q', r: 2, t: 2100, p: 0, q: { options_json: OPTIONS } }),
    ligne({ k: 'c', r: 2, t: 2200, p: 0, x: 0.5, y: 0.4, clic: 7 }),
    ligne({ k: 'e', r: 2, t: 2300, p: 0, cle: 'menace:1' }),
    // L'allie part a la defausse, puis nouveau round.
    ligne({
      k: 'd',
      r: 3,
      t: 60000,
      d: {
        o: {
          render_id: { v: 3 },
          players: { i: { '0': { o: { allies: { v: [] }, player_discard_pile: { v: [carte(10, 'Black Cat')] } } } } },
        },
      },
    }),
    ligne({ k: 'd', r: 4, t: 61000, d: { o: { render_id: { v: 4 }, round_id: { v: 2 }, phase: { v: 'Enemy Activation' } } } }),
  ].join('\n')
}

describe('fichier .marvelreplay', () => {
  it('reconstruit chaque monde, la demande, les curseurs et les etapes', () => {
    const r = analyserRelecture(fichierTexte())
    expect(r.entete.scenario).toBe('Rhino')
    expect(r.trames.map((t) => t.monde.render_id)).toEqual([1, 2, 3, 4])
    expect(r.trames[1].monde.prompt).toBe('Spider-Man joue Black Cat')
    expect(r.trames[1].demandes[0]?.options).toHaveLength(1)
    expect(r.trames[0].demandes).toEqual({})
    expect(r.curseurs).toEqual([{ t: 2200, p: 0, x: 0.5, y: 0.4, clic: 7 }])
    expect(r.etapes).toEqual([{ t: 2300, p: 0, cle: 'menace:1' }])
  })

  it('une difference ne copie que le chemin qui change', () => {
    const a = { x: { y: 1 }, z: { w: 2 } }
    const b = appliquer(a, { o: { x: { o: { y: { v: 3 } } } } }) as typeof a
    expect(b).toEqual({ x: { y: 3 }, z: { w: 2 } })
    expect(b.z).toBe(a.z)
    expect(a.x.y).toBe(1)
  })

  it('se lit depuis le gzip', async () => {
    const flux = new Response(fichierTexte()).body!.pipeThrough(new CompressionStream('gzip'))
    const r = await lireRelecture(await new Response(flux).arrayBuffer())
    expect(r.trames).toHaveLength(4)
  })

  it('refuse clairement un fichier qui n est pas une partie', async () => {
    await expect(lireRelecture(new TextEncoder().encode('bonjour').buffer)).rejects.toThrow(FichierInvalide)
    expect(() => analyserRelecture(ligne({ k: 'cle' }))).toThrow(/pas une partie enregistrée/)
    expect(() => analyserRelecture(ligne({ k: 'entete', format: 99 }))).toThrow(/plus récente/)
    expect(() => analyserRelecture(fichierTexte().replace('"m":{', '"m":{{'))).toThrow(/abîmé ou a été modifié/)
    expect(() => analyserRelecture(ligne({ k: 'entete', format: 1 }))).toThrow(/aucune action/)
  })
})

describe('lecteur', () => {
  beforeEach(() => vi.useFakeTimers())
  afterEach(() => vi.useRealTimers())

  it('reperes : round, phase du mechant, allie vaincu', () => {
    const reperes = reperesDe(analyserRelecture(fichierTexte()))
    expect(reperes).toEqual([
      { index: 2, genre: 'vaincu', libelle: 'Black Cat vaincu' },
      { index: 3, genre: 'round', libelle: 'Round 2' },
      { index: 3, genre: 'phase-mechant', libelle: 'Phase du méchant, round 2' },
    ])
  })

  it('joue a la vitesse reglee, et plafonne les longues pauses', () => {
    const lecteur = new Lecteur(analyserRelecture(fichierTexte()), 'test')
    const vus: number[] = []
    lecteur.ecouter((etat: EtatMoteur) => vus.push(etat.monde!.render_id))
    lecteur.demarrer()
    lecteur.reglerPauseMax(5)
    lecteur.lecture()
    vi.advanceTimersByTime(999)
    expect(vus).toEqual([1])
    vi.advanceTimersByTime(1)
    expect(vus).toEqual([1, 2])
    // 58 s d'ecart reel : plafonnees a 5 s.
    vi.advanceTimersByTime(5000)
    expect(vus).toEqual([1, 2, 3])
    lecteur.reglerVitesse(2)
    vi.advanceTimersByTime(500)
    expect(vus).toEqual([1, 2, 3, 4])
    expect(lecteur.lireControle().enLecture).toBe(false)
  })

  it('un saut se signale, un pas a pas non, et la demande suit', () => {
    const lecteur = new Lecteur(analyserRelecture(fichierTexte()), 'test')
    const etats: EtatMoteur[] = []
    lecteur.ecouter((etat) => etats.push(etat))
    lecteur.aller(3)
    expect(etats.at(-1)?.saut).toBe(true)
    lecteur.precedent()
    expect(etats.at(-1)?.saut).toBe(false)
    lecteur.aller(1)
    expect(etats.at(-1)?.demande?.options).toHaveLength(1)
    expect(etats.at(-1)?.aNous).toBe(false)
  })

  it('curseurs et etape au temps de la lecture, curseur perime apres 5 s', () => {
    const lecteur = new Lecteur(analyserRelecture(fichierTexte()), 'test')
    expect(lecteur.curseursA(2100)).toEqual({})
    expect(lecteur.curseursA(2500)).toEqual({ 0: { x: 0.5, y: 0.4, clic: 7 } })
    expect(lecteur.curseursA(8000)).toEqual({})
    expect(lecteur.etapeA(2299)).toBeUndefined()
    expect(lecteur.etapeA(2300)).toBe('menace:1')
  })
})

describe('fichier produit par le serveur (engine/enregistrement.py)', () => {
  it('se relit a l identique : 60 mondes reels, differences comprises', async () => {
    const { readFileSync } = await import('node:fs')
    const { dirname, join } = await import('node:path')
    const { fileURLToPath } = await import('node:url')
    const brut = readFileSync(join(dirname(fileURLToPath(import.meta.url)), '__fixtures__/exemple.marvelreplay'))
    const r = await lireRelecture(brut.buffer.slice(brut.byteOffset, brut.byteOffset + brut.byteLength))
    expect(r.entete.scenario).toBe('Rhino')
    expect(r.entete.resultat).toBe('inachevee')
    expect(r.trames.map((t) => t.monde.render_id)).toEqual(Array.from({ length: 60 }, (_, i) => i + 1))
    expect(r.trames[59].monde.prompt).toBe('etape 59')
    expect(r.trames[59].monde.players[0].hand_cards.length).toBe(r.trames[0].monde.players[0].hand_cards.length - 1)
  })
})
