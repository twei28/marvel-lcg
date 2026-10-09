import { readFileSync } from 'node:fs'
import { resolve } from 'node:path'
import { describe, expect, it } from 'vitest'
import { codeImage } from './TraductionPosee'
import { typeDeBoite } from './traduction-carte'
import { ZONES_ARTS_ALTERNATIFS } from './zones-arts-alternatifs'
import { artsDisponiblesPourHeros } from './variantes'

describe('zones des arts alternatifs de héros', () => {
  it('chaque art proposé au choix a sa zone de texte relevée', () => {
    const source = readFileSync(resolve(__dirname, 'variantes.ts'), 'utf8')
    const faces = [...source.matchAll(/^ {2}'([0-9a-z]+)': \[/gm)].map((m) => m[1]!)
    expect(faces.length).toBeGreaterThan(100)
    const manquantes = faces.flatMap((face) =>
      artsDisponiblesPourHeros(face)
        .map((serie) => `${face}_${serie}`)
        .filter((cle) => !ZONES_ARTS_ALTERNATIFS[cle])
    )
    expect(manquantes).toEqual([])
  })

  it('les zones restent dans la carte, en bas, et ont une forme', () => {
    for (const [cle, zone] of Object.entries(ZONES_ARTS_ALTERNATIFS)) {
      expect(zone, cle).not.toBeNull()
      expect(zone!.x0, cle).toBeGreaterThanOrEqual(0)
      expect(zone!.x1, cle).toBeLessThanOrEqual(1)
      expect(zone!.y0, cle).toBeGreaterThan(0.5)
      expect(zone!.y1, cle).toBeLessThanOrEqual(1)
      expect(zone!.x1 - zone!.x0, cle).toBeGreaterThan(0.2)
      expect(zone!.bords.length, cle).toBeGreaterThan(0)
    }
  })
})

describe('codeImage', () => {
  it('retrouve le code d’un scan, langue et extension retirées', () => {
    expect(codeImage('/scan/fr_01001a_cb')).toBe('01001a_cb')
    expect(codeImage('/scan/01019b_rog.jpg?v=2')).toBe('01019b_rog')
    expect(codeImage('/scan/hs004a')).toBe('hs004a')
  })
})

describe('typeDeBoite', () => {
  it('ramène les manigances annexes du moteur au côté de leur boîte', () => {
    expect(typeDeBoite('MainScheme')).toBe('MainScheme')
    expect(typeDeBoite('EncounterSideScheme')).toBe('SideScheme')
    expect(typeDeBoite('PlayerSideScheme')).toBe('SideScheme')
    expect(typeDeBoite('Treachery')).toBe('Treachery')
  })
})

describe('elargirPaysage', () => {
  it('élargit côté illustration et en bas, sans sortir de la carte', async () => {
    const { elargirPaysage } = await import('./traduction-posee')
    const zone = { x0: 0.05, y0: 0.3, x1: 0.5, y1: 0.99, fond: [240, 230, 210] as [number, number, number], bords: [[0.05, 0.5]] as Array<[number, number]> }
    const large = elargirPaysage(zone, 'gauche')
    expect(large.x1).toBeCloseTo(0.512, 5)
    expect(large.x0).toBeCloseTo(0.044, 5)
    expect(large.y1).toBe(1)
    expect(elargirPaysage(zone, 'droite').x0).toBeCloseTo(0.038, 5)
  })
})

describe('elargirPaysage et encoches', () => {
  it('ne pousse pas un bord creusé autour d’un badge', async () => {
    const { elargirPaysage } = await import('./traduction-posee')
    const zone = {
      x0: 0.05, y0: 0.3, x1: 0.5, y1: 0.9, fond: [240, 230, 210] as [number, number, number],
      bords: [[0.05, 0.5], [0.05, 0.42]] as Array<[number, number]>,
    }
    const large = elargirPaysage(zone, 'gauche')
    expect(large.bords[0]![1]).toBeCloseTo(0.512, 5)
    expect(large.bords[1]![1]).toBeCloseTo(0.42, 5)
  })
})

describe('elargirPaysage et badge blanc', () => {
  it('ne s’élargit pas sur une ligne dont la bande ajoutée est blanche', async () => {
    const { elargirPaysage } = await import('./traduction-posee')
    const largeur = 100
    const hauteur = 100
    const pixels = new Uint8ClampedArray(largeur * hauteur * 4).fill(90)
    // Badge blanc à droite de la boîte, sur la moitié basse.
    for (let y = 60; y < 100; y += 1) for (let x = 50; x < 54; x += 1) pixels.set([255, 255, 255, 255], (y * largeur + x) * 4)
    const zone = {
      x0: 0.05, y0: 0.2, x1: 0.5, y1: 0.9, fond: [240, 230, 210] as [number, number, number],
      bords: [[0.05, 0.5], [0.05, 0.5]] as Array<[number, number]>,
    }
    const large = elargirPaysage(zone, 'gauche', { pixels, largeur, hauteur })
    expect(large.bords[0]![1]).toBeCloseTo(0.512, 5)
    expect(large.bords[1]![1]).toBeCloseTo(0.5, 5)
  })
})
