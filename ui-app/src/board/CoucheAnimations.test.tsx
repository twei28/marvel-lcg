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
import { CoucheAnimations, dureeDe, inclinaisonDe } from './CoucheAnimations'

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

  it('anime la pioche d\'une carte avec image, l\'image dans la couche du geste', () => {
    // ⚠ DEPUIS LE 14/09/2026 le fantome a DEUX couches : `.vol-carte` porte la
    // translation, `.vol-carte-geste` l'inclinaison et l'ombre, et l'image vit
    // dedans. La racine est donc toujours un DIV, meme avec un scan.
    const { main } = poserScene()
    const { container, rerender } = render(<CoucheAnimations renderId={rendu()} actif />)

    main.append(carte('8', 'https://exemple.test/scan.png'))
    rerender(<CoucheAnimations renderId={rendu()} actif />)

    const fantome = container.querySelector('.vol-carte')
    expect(fantome?.tagName).toBe('DIV')
    const image = container.querySelector('.vol-carte-image')
    expect(image?.tagName).toBe('IMG')
    expect(image?.getAttribute('src')).toBe('https://exemple.test/scan.png')
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

/**
 * La regle du POIDS, testee sur les fonctions elles-memes.
 *
 * ⚠ PAS EN JSDOM SUR LE DOM : jsdom ne calcule aucune position, tous les
 * rectangles y valent zero. Un test qui simulerait des geometries couterait
 * cher et ne prouverait rien de la regle. Ici on teste la regle.
 */
describe('la duree suit la distance, et l inclinaison le sens du trajet', () => {
  const boite = (x: number, y: number) => ({ x, y, w: 100, h: 140 })

  it('un trajet long dure plus longtemps qu un court', () => {
    // ⚠ LA CAUSE PRINCIPALE DU « MOU » relevee le 14/09/2026 : c'etait 250 ms
    // fixes, qu'une carte traverse l'ecran ou bouge de trois centimetres.
    const court = dureeDe(boite(0, 0), boite(30, 0))
    const long = dureeDe(boite(0, 0), boite(1200, 600))
    expect(long).toBeGreaterThan(court)
  })

  it('une carte qui ne bouge pas prend la duree la plus courte', () => {
    expect(dureeDe(boite(10, 10), boite(10, 10))).toBe(130)
  })

  it('au-dela de la traversee, on ne ralentit plus', () => {
    // Sans plafond, un deplacement absurde donnerait une duree absurde.
    expect(dureeDe(boite(0, 0), boite(4000, 4000))).toBe(dureeDe(boite(0, 0), boite(900, 0)))
  })

  it('le sens du trajet donne le sens de l inclinaison', () => {
    expect(inclinaisonDe(boite(0, 0), boite(400, 0))).toBeGreaterThan(0)
    expect(inclinaisonDe(boite(400, 0), boite(0, 0))).toBeLessThan(0)
  })

  it('l inclinaison est BORNEE : jamais une carte qui tourne', () => {
    // L'utilisateur a demande « sans que ce soit trop charge » : au-dela de
    // trois degres on ne lit plus une carte lancee.
    expect(Math.abs(inclinaisonDe(boite(0, 0), boite(5000, 0)))).toBeLessThanOrEqual(3)
    expect(Math.abs(inclinaisonDe(boite(5000, 0), boite(0, 0)))).toBeLessThanOrEqual(3)
  })

  it('un deplacement purement vertical n incline pas', () => {
    expect(inclinaisonDe(boite(0, 0), boite(0, 600))).toBe(0)
  })
})
