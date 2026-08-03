// Les cartes SANS scan doivent voler comme les autres.
//
// ScanCard ne pose plus d'<img> quand la carte n'a pas d'image (un src vide
// fait recharger la page). Les fantomes de cette couche lisaient cette <img>
// pour savoir s'il fallait animer : sans elle, pioche et defausse ne
// bougeaient plus du tout, et la mise en jeu repassait un src vide a un <img>.
// Ces tests fixent le comportement attendu : le mouvement s'anime toujours,
// c'est le fantome qui se passe d'image.

import { render } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { CoucheAnimations } from './CoucheAnimations'

/**
 * La couche ne diffe qu'UNE fois par render_id et garde sa memoire au niveau
 * du module : chaque rendu de test doit donc porter un identifiant neuf.
 */
let prochain = 100
const rendu = () => (prochain += 1)

function carte(id: string, image?: string): HTMLElement {
  const el = document.createElement('div')
  el.className = 'scan-card'
  el.dataset.cardId = id
  if (image !== undefined) {
    const img = document.createElement('img')
    img.src = image
    el.append(img)
  }
  return el
}

function poserScene(): { main: HTMLElement; table: HTMLElement } {
  const scene = document.createElement('div')
  scene.className = 'plateau-scene'
  const piles = document.createElement('div')
  piles.className = 'zone-piles-joueur'
  // Ancres de pile : [deck, defausse]. Elles ont un scan, comme en vrai.
  piles.append(carte('deck', 'https://exemple.test/dos.png'), carte('defausse', 'https://exemple.test/dos.png'))
  const main = document.createElement('div')
  main.className = 'zone-main'
  const table = document.createElement('div')
  table.className = 'zone-heros'
  scene.append(piles, main, table)
  document.body.append(scene)
  return { main, table }
}

describe('CoucheAnimations : une carte sans scan vole quand meme', () => {
  beforeEach(() => {
    // Les fantomes se retirent par setTimeout : on ne veut pas de minuterie
    // reelle qui traine apres le test.
    vi.useFakeTimers()
    // Vider la memoire de module : sans .plateau-scene, l'effet la remet a zero.
    render(<CoucheAnimations renderId={rendu()} actif />).unmount()
  })

  afterEach(() => {
    vi.useRealTimers()
    document.body.innerHTML = ''
  })

  it('anime la pioche d\'une carte sans image, avec un fantome sans <img>', () => {
    const { main } = poserScene()
    const { container, rerender } = render(<CoucheAnimations renderId={rendu()} actif />)
    expect(container.querySelector('.vol-carte')).toBeNull()

    main.append(carte('7'))
    rerender(<CoucheAnimations renderId={rendu()} actif />)

    const fantome = container.querySelector('.vol-carte')
    expect(fantome).not.toBeNull()
    expect(fantome?.tagName).toBe('DIV')
    expect(document.querySelector('img[src=""]')).toBeNull()
  })

  it('anime la pioche d\'une carte avec image, avec un fantome <img>', () => {
    const { main } = poserScene()
    const { container, rerender } = render(<CoucheAnimations renderId={rendu()} actif />)

    main.append(carte('8', 'https://exemple.test/scan.png'))
    rerender(<CoucheAnimations renderId={rendu()} actif />)

    const fantome = container.querySelector('.vol-carte')
    expect(fantome?.tagName).toBe('IMG')
    expect(fantome?.getAttribute('src')).toBe('https://exemple.test/scan.png')
  })

  it('anime la defausse d\'une carte sans image', () => {
    const { main } = poserScene()
    const jouee = carte('9')
    main.append(jouee)
    const { container, rerender } = render(<CoucheAnimations renderId={rendu()} actif />)

    jouee.remove()
    rerender(<CoucheAnimations renderId={rendu()} actif />)

    expect(container.querySelector('.vol-carte')).not.toBeNull()
    expect(document.querySelector('img[src=""]')).toBeNull()
  })

  it('anime la mise en jeu d\'une carte sans image sans jamais poser de src vide', () => {
    const { main, table } = poserScene()
    const jouee = carte('10')
    main.append(jouee)
    const { container, rerender } = render(<CoucheAnimations renderId={rendu()} actif />)

    table.append(jouee)
    rerender(<CoucheAnimations renderId={rendu()} actif />)

    const fantome = container.querySelector('.vol-carte')
    expect(fantome).not.toBeNull()
    expect(fantome?.tagName).toBe('DIV')
    expect(document.querySelector('img[src=""]')).toBeNull()
  })
})
