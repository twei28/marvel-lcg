// Relecture fidele (08/10/2026) : ce que le joueur voit, publie puis rejoue.
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { estUnReglage, recouvrir, reglagesDuJoueur, StockageMemoire } from './cadre-joueur'
import { placerCadre } from './CadreJoueur'
import { appliquerDefilements, cheminDe } from './defilement-partage'
import { estLibre, poserVitre } from './vitre-spectateur'
import { oublierVusPublies, publierVu, publierVuLimite } from './vu-partage'
import { actionDuClavier } from './relecture/PageRelecture'

function adresse(recherche: string) {
  window.history.replaceState(null, '', `/app/board.html${recherche}`)
}

describe('publication de ce que le joueur voit', () => {
  const envois: { p: number; g: string; v: unknown }[] = []
  beforeEach(() => {
    envois.length = 0
    oublierVusPublies()
    vi.stubGlobal(
      'fetch',
      vi.fn((_url: string, init?: RequestInit) => {
        envois.push(JSON.parse(String(init?.body)))
        return Promise.resolve(new Response('{}'))
      })
    )
  })
  afterEach(() => {
    vi.unstubAllGlobals()
    adresse('')
  })

  it('publie une valeur, une seule fois tant qu elle ne change pas', () => {
    adresse('')
    publierVu(0, 'sel', { e: 'x', c: [1], r: [] })
    publierVu(0, 'sel', { e: 'x', c: [1], r: [] })
    publierVu(0, 'sel', { e: 'x', c: [1, 2], r: [] })
    expect(envois.map((e) => e.v)).toEqual([
      { e: 'x', c: [1], r: [] },
      { e: 'x', c: [1, 2], r: [] },
    ])
  })

  it('un spectateur ou une relecture ne publie rien', () => {
    adresse('?spectateur')
    publierVu(0, 'loupe', { a: '3', f: null })
    adresse('?relecture&cadre')
    publierVu(0, 'loupe', { a: '4', f: null })
    expect(envois).toEqual([])
  })

  it('le glisser se publie au plus toutes les 60 ms, la derniere position toujours', () => {
    vi.useFakeTimers()
    adresse('')
    publierVuLimite(0, 'glis', { x: 1 }, 60)
    publierVuLimite(0, 'glis', { x: 2 }, 60)
    publierVuLimite(0, 'glis', { x: 3 }, 60)
    expect(envois.map((e) => e.v)).toEqual([{ x: 1 }])
    vi.advanceTimersByTime(60)
    expect(envois.map((e) => e.v)).toEqual([{ x: 1 }, { x: 3 }])
    vi.useRealTimers()
  })
})

describe('les reglages du joueur dans le cadre', () => {
  it('voyagent tous, sauf la langue et ce qui n est pas un reglage', () => {
    expect(estUnReglage('marvel-board-volume-sons')).toBe(true)
    expect(estUnReglage('mc_affichage_v1')).toBe(true)
    expect(estUnReglage('mode-plateau')).toBe(true)
    expect(estUnReglage('marvel-langue')).toBe(false)
    expect(estUnReglage('marvel-board-scans-fr')).toBe(false)
    expect(estUnReglage('marvel-historique-partie')).toBe(false)
    expect(estUnReglage('jeton-de-session')).toBe(false)
  })

  it('recouvrent ceux de celui qui regarde, sans toucher a sa langue', () => {
    const regarde = new StockageMemoire({
      'marvel-langue': 'en',
      'marvel-board-sons': 'off',
      'mc_affichage_v1': 'sobre',
      autre: 'x',
    })
    recouvrir(regarde, { 'marvel-board-volume-sons': '60', 'mc_affichage_v1': 'riche', 'marvel-langue': 'fr' })
    expect(regarde.getItem('marvel-langue')).toBe('en')
    expect(regarde.getItem('mc_affichage_v1')).toBe('riche')
    expect(regarde.getItem('marvel-board-volume-sons')).toBe('60')
    // Un reglage que le joueur n'avait pas reprend sa valeur par defaut.
    expect(regarde.getItem('marvel-board-sons')).toBeNull()
    expect(regarde.getItem('autre')).toBe('x')
  })

  it('se lisent sur le stockage du joueur', () => {
    const joueur = new StockageMemoire({ 'marvel-board-sons': 'on', 'marvel-langue': 'fr', 'mc_x': 'y'.repeat(3000) })
    expect(reglagesDuJoueur(joueur)).toEqual({ 'marvel-board-sons': 'on' })
  })
})

describe('le cadre a la taille de l ecran du joueur', () => {
  it('mis a l echelle et centre dans la place disponible', () => {
    expect(placerCadre({ w: 1920, h: 1080 }, { w: 1280, h: 720 })).toEqual({ w: 1280, h: 720, echelle: 1.5, gauche: 0, haut: 0 })
    const etroit = placerCadre({ w: 1000, h: 1000 }, { w: 2000, h: 1000 })
    expect(etroit.echelle).toBe(0.5)
    expect(etroit.haut).toBe(250)
    // Sous la barre du spectateur (32 px).
    expect(placerCadre({ w: 800, h: 632 }, { w: 800, h: 600 }, 32)).toEqual({ w: 800, h: 600, echelle: 1, gauche: 0, haut: 32 })
    // Ecran inconnu (partie d'avant le 08/10/2026) : celui de celui qui regarde.
    expect(placerCadre({ w: 800, h: 600 }, undefined)).toEqual({ w: 800, h: 600, echelle: 1, gauche: 0, haut: 0 })
  })
})

describe('les defilements', () => {
  it('une boite se retrouve par son chemin de classes, et reprend sa position', () => {
    document.body.innerHTML = `
      <div class="plateau"><div class="main est-active"><div class="liste" style="overflow:auto"></div></div>
      <div class="main"><div class="liste"></div></div></div>`
    const listes = document.querySelectorAll<HTMLElement>('.liste')
    const chemin = cheminDe(listes[1])
    expect(chemin).toEqual({ k: 'div.plateau > div.main > div.liste', i: 1 })
    // jsdom ne calcule pas de mise en page : on lui donne des dimensions.
    Object.defineProperty(listes[1], 'scrollHeight', { value: 1000 })
    Object.defineProperty(listes[1], 'clientHeight', { value: 200 })
    appliquerDefilements([{ ...chemin, x: 0, y: 0.5 }])
    expect(listes[1].scrollTop).toBe(400)
    expect(listes[0].scrollTop).toBe(0)
  })
})

describe('la vitre du spectateur', () => {
  it('arrete les clics sur le plateau, laisse passer la barre de lecture', () => {
    document.body.innerHTML = `<button class="carte">carte</button><div class="relecture-barre"><button class="lire">lire</button></div>`
    const clics: string[] = []
    document.body.addEventListener('click', (e) => clics.push((e.target as HTMLElement).className))
    const retirer = poserVitre()
    document.querySelector<HTMLElement>('.carte')!.click()
    document.querySelector<HTMLElement>('.lire')!.click()
    retirer()
    document.querySelector<HTMLElement>('.carte')!.click()
    expect(clics).toEqual(['lire', 'carte'])
    expect(estLibre(document.querySelector('.lire'))).toBe(true)
  })
})

describe('le clavier de la relecture', () => {
  const touche = (key: string, shiftKey = false) => ({ key, shiftKey, ctrlKey: false, altKey: false, metaKey: false })
  it('comme une video', () => {
    expect(actionDuClavier(touche(' '))).toBe('basculerLecture')
    expect(actionDuClavier(touche('ArrowRight'))).toBe('suivant')
    expect(actionDuClavier(touche('ArrowLeft'))).toBe('precedent')
    expect(actionDuClavier(touche('ArrowRight', true))).toBe('roundSuivant')
    expect(actionDuClavier(touche('ArrowLeft', true))).toBe('roundPrecedent')
    expect(actionDuClavier(touche('+'))).toBe('vitessePlus')
    expect(actionDuClavier(touche('-'))).toBe('vitesseMoins')
    expect(actionDuClavier(touche('a'))).toBeUndefined()
    expect(actionDuClavier({ ...touche('ArrowRight'), ctrlKey: true })).toBeUndefined()
  })
})
