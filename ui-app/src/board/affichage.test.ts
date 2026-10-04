// Le reglage « Affichage : Normal / Sobre » du plateau (affichage.ts).
import { readFileSync } from 'node:fs'
import { dirname, join } from 'node:path'
import { fileURLToPath } from 'node:url'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import {
  affichageDuCompte,
  CLE_AFFICHAGE,
  ecrireAffichage,
  lireAffichage,
  mouvementReduit,
  normaliserAffichage,
} from './affichage'

beforeEach(() => {
  window.localStorage.clear()
  delete document.documentElement.dataset.affichage
})

afterEach(() => {
  vi.unstubAllGlobals()
})

describe('affichage', () => {
  it('lit la meme cle que la preparation, normal par defaut', () => {
    expect(CLE_AFFICHAGE).toBe('mc_affichage_v1')
    expect(lireAffichage()).toBe('normal')
    window.localStorage.setItem(CLE_AFFICHAGE, 'sobre')
    expect(lireAffichage()).toBe('sobre')
  })

  it('une valeur inconnue vaut normal', () => {
    for (const v of [undefined, null, '', 'fluo', 'SOBRE']) expect(normaliserAffichage(v)).toBe('normal')
  })

  it('ecrire range le choix, pose l attribut et previent le compte', () => {
    const appel = vi.fn(() => Promise.resolve(new Response('{}')))
    vi.stubGlobal('fetch', appel)
    ecrireAffichage('sobre')
    expect(window.localStorage.getItem(CLE_AFFICHAGE)).toBe('sobre')
    expect(document.documentElement.dataset.affichage).toBe('sobre')
    expect(appel).toHaveBeenCalledWith('/save_preferences', expect.objectContaining({ method: 'POST' }))
  })

  it('le compte ne fait foi que s il a deja un fichier', () => {
    expect(affichageDuCompte({ compte: false, existe: false, preferences: {} })).toBeUndefined()
    expect(affichageDuCompte({ compte: true, existe: false, preferences: {} })).toBeUndefined()
    expect(affichageDuCompte(null)).toBeUndefined()
    expect(affichageDuCompte({ compte: true, existe: true, preferences: { affichage: 'sobre' } })).toBe('sobre')
    expect(affichageDuCompte({ compte: true, existe: true, preferences: {} })).toBe('normal')
  })

  it('le mode sobre vaut mouvement reduit, le mode normal suit le systeme', () => {
    // test-setup.ts : matchMedia repond toujours « non ».
    document.documentElement.dataset.affichage = 'normal'
    expect(mouvementReduit()).toBe(false)
    document.documentElement.dataset.affichage = 'sobre'
    expect(mouvementReduit()).toBe(true)
  })
})

// ⚠ LE MODE NORMAL NE DOIT RIEN VOIR DE LA FEUILLE SOBRE. Une seule regle sans
// le prefixe changerait le plateau de tout le monde.
describe('styles/affichage-sobre.css', () => {
  const feuille = readFileSync(join(dirname(fileURLToPath(import.meta.url)), '../../styles/affichage-sobre.css'), 'utf8')
    .replace(/\/\*[\s\S]*?\*\//g, '')

  it('chaque selecteur commence par html[data-affichage=sobre]', () => {
    const selecteurs = [...feuille.matchAll(/([^{}]+)\{[^{}]*\}/g)]
      .flatMap((m) => m[1].split(','))
      .map((s) => s.trim())
      .filter(Boolean)
    expect(selecteurs.length).toBeGreaterThan(20)
    for (const s of selecteurs) expect(s.startsWith("html[data-affichage='sobre']"), s).toBe(true)
  })

  it('ne declare aucune couche (elle doit passer devant toutes)', () => {
    expect(feuille).not.toMatch(/@layer/)
  })
})
