// L'Épuré réservé au compte de l'administrateur, et « Étape par étape bis » (16/10/2026).
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { appliquerAffichage, CLE_AFFICHAGE, CLE_EPURE_PERMIS, epurePermis, lireAffichage, reglerEpurePourTous, retenirEpurePermis } from './affichage'
import { ecrirePresentationPhase, lirePresentationPhase, suivrePresentationPhase } from './phase-presentation'

afterEach(() => {
  vi.unstubAllGlobals()
  localStorage.clear()
  sessionStorage.clear()
  delete document.documentElement.dataset.epure
  reglerEpurePourTous(true)
})

describe("l'épuré pour tout le monde, seul affichage (18/10/2026)", () => {
  it("tout le monde y a droit, même en ligne, sans réponse du serveur, même en vue « compte classique »", () => {
    vi.stubGlobal('location', { hostname: 'narwhalchampions.com' })
    localStorage.setItem('mc_vue_joueur', 'oui')
    localStorage.setItem(CLE_AFFICHAGE, 'sobre')
    expect(epurePermis()).toBe(true)
    expect(lireAffichage()).toBe('epure')
    appliquerAffichage('normal')
    expect(document.documentElement.dataset.epure).toBe('oui')
    // Le choix rangé n'est pas effacé : les anciens modes sont désactivés, pas supprimés.
    expect(localStorage.getItem(CLE_AFFICHAGE)).toBe('sobre')
  })
})

describe("l'épuré, réservé à l'administrateur (ancienne règle, conservée)", () => {
  beforeEach(() => reglerEpurePourTous(false))
  it('en ligne, sans réponse du serveur : un épuré rangé se montre en sobre', () => {
    vi.stubGlobal('location', { hostname: 'narwhalchampions.com' })
    localStorage.setItem(CLE_AFFICHAGE, 'epure')
    expect(epurePermis()).toBe(false)
    expect(lireAffichage()).toBe('sobre')
    appliquerAffichage('epure')
    expect(document.documentElement.dataset.affichage).toBe('sobre')
    expect(document.documentElement.dataset.epure).toBeUndefined()
    // Le choix rangé n'est pas effacé.
    expect(localStorage.getItem(CLE_AFFICHAGE)).toBe('epure')
  })

  it("l'administrateur (réponse retenue) le garde", () => {
    vi.stubGlobal('location', { hostname: 'narwhalchampions.com' })
    localStorage.setItem(CLE_AFFICHAGE, 'epure')
    retenirEpurePermis(true)
    expect(sessionStorage.getItem(CLE_EPURE_PERMIS)).toBe('oui')
    expect(lireAffichage()).toBe('epure')
    appliquerAffichage('epure')
    expect(document.documentElement.dataset.epure).toBe('oui')
  })

  it("la vue « compte classique » de l'administrateur ne l'a pas", () => {
    vi.stubGlobal('location', { hostname: 'narwhalchampions.com' })
    retenirEpurePermis(true)
    localStorage.setItem('mc_vue_joueur', 'oui')
    expect(epurePermis()).toBe(false)
  })

  it('un moteur lancé sur la machine y a droit', () => {
    vi.stubGlobal('location', { hostname: 'localhost' })
    expect(epurePermis()).toBe(true)
  })
})

describe('les présentations de la phase du méchant', () => {
  it('bis par défaut, le choix se suit et se relit', () => {
    expect(lirePresentationPhase()).toBe('bis')
    const vus: string[] = []
    const fin = suivrePresentationPhase((p) => vus.push(p))
    ecrirePresentationPhase('dynamique')
    expect(lirePresentationPhase()).toBe('dynamique')
    ecrirePresentationPhase('etape')
    fin()
    ecrirePresentationPhase('bis')
    expect(vus).toEqual(['dynamique', 'etape'])
  })

  it("l'ancien réglage « mc_phase_bis » est repris tant qu'aucun choix n'est fait", () => {
    localStorage.setItem('mc_phase_bis', 'non')
    expect(lirePresentationPhase()).toBe('etape')
    localStorage.setItem('mc_phase_bis', 'oui')
    expect(lirePresentationPhase()).toBe('bis')
    // Un choix explicite prime, une valeur inconnue est ignorée.
    localStorage.setItem('mc_phase_presentation', 'dynamique')
    expect(lirePresentationPhase()).toBe('dynamique')
    localStorage.setItem('mc_phase_presentation', 'n-importe-quoi')
    expect(lirePresentationPhase()).toBe('bis')
  })
})
