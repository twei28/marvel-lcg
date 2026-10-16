// L'Épuré réservé au compte de l'administrateur, et « Étape par étape bis » (16/10/2026).
import { afterEach, describe, expect, it, vi } from 'vitest'
import { appliquerAffichage, CLE_AFFICHAGE, CLE_EPURE_PERMIS, epurePermis, lireAffichage, retenirEpurePermis } from './affichage'
import { ecrirePhaseBis, lirePhaseBis, suivrePhaseBis } from './phase-bis'

afterEach(() => {
  vi.unstubAllGlobals()
  localStorage.clear()
  sessionStorage.clear()
  delete document.documentElement.dataset.epure
})

describe("l'épuré, réservé à l'administrateur", () => {
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

describe('« Étape par étape bis »', () => {
  it('bis par défaut, et le choix se suit', () => {
    expect(lirePhaseBis()).toBe(true)
    const vus: boolean[] = []
    const fin = suivrePhaseBis((oui) => vus.push(oui))
    ecrirePhaseBis(false)
    expect(lirePhaseBis()).toBe(false)
    ecrirePhaseBis(true)
    fin()
    ecrirePhaseBis(false)
    expect(vus).toEqual([false, true])
  })
})
