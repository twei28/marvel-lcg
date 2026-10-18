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
  reglerEpurePourTous,
} from './affichage'

beforeEach(() => {
  window.localStorage.clear()
  delete document.documentElement.dataset.affichage
})

afterEach(() => {
  vi.unstubAllGlobals()
  reglerEpurePourTous(true)
})

describe('affichage', () => {
  it('lit la meme cle que la preparation ; l affichage de depart est epure, qui se lit « Normal » (18/10/2026)', () => {
    expect(CLE_AFFICHAGE).toBe('mc_affichage_v1')
    expect(lireAffichage()).toBe('epure')
    // Les trois affichages se CHOISISSENT : ce que le navigateur a range est respecte.
    for (const v of ['normal', 'sobre', 'epure'] as const) {
      window.localStorage.setItem(CLE_AFFICHAGE, v)
      expect(lireAffichage()).toBe(v)
    }
  })

  it('sans droit a l epure (ancienne reserve a l administrateur) : un epure range, ou le depart, se montre en sobre', () => {
    reglerEpurePourTous(false)
    window.localStorage.setItem('mc_vue_joueur', 'oui')
    expect(lireAffichage()).toBe('sobre')
    window.localStorage.setItem(CLE_AFFICHAGE, 'epure')
    expect(lireAffichage()).toBe('sobre')
    window.localStorage.setItem(CLE_AFFICHAGE, 'normal')
    expect(lireAffichage()).toBe('normal')
  })

  it('une valeur inconnue vaut l affichage de depart (epure, « Normal »)', () => {
    for (const v of [undefined, null, '', 'fluo', 'SOBRE']) expect(normaliserAffichage(v)).toBe('epure')
    expect(normaliserAffichage('normal')).toBe('normal')
  })

  it('ecrire range le choix, pose l attribut et previent le compte', () => {
    const appel = vi.fn(() => Promise.resolve(new Response('{}')))
    vi.stubGlobal('fetch', appel)
    ecrireAffichage('sobre')
    expect(window.localStorage.getItem(CLE_AFFICHAGE)).toBe('sobre')
    expect(document.documentElement.dataset.affichage).toBe('sobre')
    expect(appel).toHaveBeenCalledWith('/save_preferences', expect.objectContaining({ method: 'POST' }))
  })

  it('l epure est un sobre de plus : data-affichage vaut sobre, data-epure s ajoute', () => {
    expect(normaliserAffichage('epure')).toBe('epure')
    vi.stubGlobal('fetch', vi.fn(() => Promise.resolve(new Response('{}'))))
    ecrireAffichage('epure')
    expect(window.localStorage.getItem(CLE_AFFICHAGE)).toBe('epure')
    expect(document.documentElement.dataset.affichage).toBe('sobre')
    expect(document.documentElement.dataset.epure).toBe('oui')
    // L'épuré garde ses animations (16/10/2026) : seul le sobre les coupe.
    expect(mouvementReduit()).toBe(false)
    ecrireAffichage('sobre')
    expect(document.documentElement.dataset.epure).toBeUndefined()
  })

  it('le compte ne fait foi que s il a deja un fichier', () => {
    expect(affichageDuCompte({ compte: false, existe: false, preferences: {} })).toBeUndefined()
    expect(affichageDuCompte({ compte: true, existe: false, preferences: {} })).toBeUndefined()
    expect(affichageDuCompte(null)).toBeUndefined()
    expect(affichageDuCompte({ compte: true, existe: true, preferences: { affichage: 'sobre' } })).toBe('sobre')
    expect(affichageDuCompte({ compte: true, existe: true, preferences: {} })).toBe('epure')
  })

  it('le mode sobre vaut mouvement reduit, le mode normal suit le systeme', () => {
    // test-setup.ts : matchMedia repond toujours « non ».
    delete document.documentElement.dataset.epure
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

// ⚠ NORMAL ET SOBRE NE DOIVENT RIEN VOIR DE LA FEUILLE EPURE (15/10/2026) : une
// seule regle sans `html[data-epure]` changerait le plateau de tout le monde.
// Meme garde pour la feuille des pages hors plateau.
describe.each([
  ['styles/affichage-epure.css', '../../styles/affichage-epure.css'],
  ['public/css/affichage-epure-pages.css', '../../../Fusion/marvel-lcg-src/public/css/affichage-epure-pages.css'],
])('%s', (_nom, chemin) => {
  const feuille = readFileSync(join(dirname(fileURLToPath(import.meta.url)), chemin), 'utf8')
    .replace(/\/\*[\s\S]*?\*\//g, '')

  it('chaque selecteur commence par html[data-epure]', () => {
    const selecteurs = [...feuille.matchAll(/([^{}]+)\{[^{}]*\}/g)]
      .flatMap((m) => m[1].split(','))
      .map((s) => s.trim())
      .filter(Boolean)
    expect(selecteurs.length).toBeGreaterThan(20)
    // Une `@font-face` ne change rien a l'affichage tant qu'aucune regle ne s'en sert : elle est permise.
    for (const s of selecteurs) expect(s.startsWith('html[data-epure]') || s === '@font-face', s).toBe(true)
  })

  it('ne declare aucune couche (elle doit passer devant toutes)', () => {
    expect(feuille).not.toMatch(/@layer/)
  })
})
