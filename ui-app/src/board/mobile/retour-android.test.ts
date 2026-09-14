// Le Retour ferme la feuille du sommet (retour-android.ts).
import { act, renderHook } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { FERMABLES, fermerLaFeuille, useRetourAndroid } from './retour-android'

/** L'observateur repasse par requestAnimationFrame : on laisse un tour passer. */
async function laisserObserver() {
  await act(async () => {
    await new Promise((r) => setTimeout(r, 30))
  })
}

describe('le Retour Android sur les feuilles du plateau portrait', () => {
  let pousses: unknown[]
  beforeEach(() => {
    document.body.innerHTML = ''
    pousses = []
    vi.spyOn(window.history, 'pushState').mockImplementation((etat) => {
      pousses.push(etat)
    })
    vi.spyOn(window.history, 'back').mockImplementation(() => {
      // Le navigateur repond par un popstate, ici tout de suite.
      window.dispatchEvent(new PopStateEvent('popstate'))
    })
    vi.stubGlobal('requestAnimationFrame', (fn: FrameRequestCallback) => setTimeout(() => fn(0), 0) as unknown as number)
    vi.stubGlobal('cancelAnimationFrame', (id: number) => clearTimeout(id))
  })
  afterEach(() => {
    vi.restoreAllMocks()
    vi.unstubAllGlobals()
  })

  it('une feuille qui s ouvre pousse une entree, le Retour la referme par son bouton', async () => {
    const { unmount } = renderHook(() => useRetourAndroid(true))
    const bouton = document.createElement('button')
    bouton.className = 'reglages-fermer'
    const clics = vi.fn(() => feuille.remove())
    bouton.addEventListener('click', clics)
    document.body.append(bouton)
    const feuille = document.createElement('div')
    // La fenetre des reglages (14/09/2026) : elle a remplace le popover.
    feuille.className = 'reglages-fond'
    document.body.append(feuille)
    await laisserObserver()
    expect(pousses).toEqual([{ feuilleMobile: '.reglages-fond' }])

    await act(async () => {
      window.dispatchEvent(new PopStateEvent('popstate'))
    })
    expect(clics).toHaveBeenCalledTimes(1)
    expect(document.querySelector('.reglages-fond')).toBeNull()
    await laisserObserver()
    // Refermee par le Retour : aucun history.back() de notre part.
    expect(window.history.back).not.toHaveBeenCalled()
    unmount()
  })

  it('une feuille refermee a la main retire son entree sans en refermer une autre', async () => {
    const { unmount } = renderHook(() => useRetourAndroid(true))
    const feuille = document.createElement('section')
    feuille.className = 'historique-panneau'
    const bouton = document.createElement('button')
    bouton.className = 'bh-history'
    const clics = vi.fn()
    bouton.addEventListener('click', clics)
    document.body.append(bouton, feuille)
    await laisserObserver()
    expect(pousses).toHaveLength(1)
    feuille.remove()
    await laisserObserver()
    expect(window.history.back).toHaveBeenCalledTimes(1)
    // Le popstate provoque par ce back() n'a rien referme d'autre.
    expect(clics).not.toHaveBeenCalled()
    unmount()
  })

  it('inactif sur un etat enregistre : rien n est pousse', async () => {
    const { unmount } = renderHook(() => useRetourAndroid(false))
    const feuille = document.createElement('div')
    feuille.className = 'popover-sauvegardes popover-plus'
    document.body.append(feuille)
    await laisserObserver()
    expect(pousses).toEqual([])
    unmount()
  })

  it('sans bouton connu, referme par un « Fermer » de la feuille', () => {
    const feuille = document.createElement('div')
    feuille.className = 'plateau-selecteur'
    const fermer = document.createElement('button')
    fermer.textContent = 'Annuler'
    const clic = vi.fn()
    fermer.addEventListener('click', clic)
    feuille.append(fermer)
    document.body.append(feuille)
    expect(fermerLaFeuille('.plateau-selecteur')).toBe(true)
    expect(clic).toHaveBeenCalledTimes(1)
  })

  it('chaque fermable de la liste a un selecteur valide', () => {
    for (const f of FERMABLES) expect(() => document.querySelector(f.selecteur)).not.toThrow()
  })
})
