import { describe, expect, it } from 'vitest'
import { CADRES_PENCHES, ZONES_MANUELLES, corrigerZone } from './zones-corrections'
import type { ZoneTexte } from './traduction-posee'

const detectee: ZoneTexte = { x0: 0.1, y0: 0.6, x1: 0.9, y1: 0.8, fond: [250, 250, 250], bords: [[0.1, 0.9]] }

describe('corrigerZone : zones relevées à la main', () => {
  it('une zone manuelle remplace la détection, et existe même quand la détection ne trouve rien', () => {
    const m = ZONES_MANUELLES.sk196
    const sansDetection = corrigerZone('sk196', null)!
    expect(sansDetection).not.toBeNull()
    expect([sansDetection.x0, sansDetection.y0, sansDetection.x1, sansDetection.y1]).toEqual([m.x0, m.y0, m.x1, m.y1])
    expect(corrigerZone('sk196', detectee)!.y0).toBe(m.y0)
  })

  it('le coin d\'un badge raccourcit le haut de la zone seulement', () => {
    const zone = corrigerZone('pu013', null)!
    expect(zone.bords[0][1]).toBeLessThan(zone.bords[zone.bords.length - 1][1])
  })

  it('un palier change le bord gauche ou droit sur une partie de la hauteur (illustration qui mord sur le cadre)', () => {
    const tk010 = corrigerZone('tk010', null)!
    expect(tk010.bords[0][0]).toBeGreaterThan(tk010.bords[tk010.bords.length - 1][0])
    const tk001a = corrigerZone('tk001a', null)!
    expect(tk001a.bords[0][1]).toBeLessThan(tk001a.bords[tk001a.bords.length - 1][1])
  })

  it('une carte sans correction garde sa détection, ou son absence', () => {
    expect(corrigerZone('zz999', detectee)).toBe(detectee)
    expect(corrigerZone('zz999', null)).toBeNull()
  })

  it('bg014 (manigance annexe couchée) : la zone remonte jusqu\'à la première ligne du flavor, qui était coupée en haut', () => {
    const detectee: ZoneTexte = { x0: 0.447, y0: 0.27, x1: 0.98, y1: 0.684, fond: [250, 250, 250], bords: [[0.447, 0.98]] }
    expect(corrigerZone('bg014', detectee)!.y0).toBeLessThan(0.25)
  })

  it('sq015 : cadre qui penche à gauche, le français suit le départ des lignes anglaises ; les cartes ordinaires non', () => {
    expect(CADRES_PENCHES.has('sq015')).toBe(true)
    expect(CADRES_PENCHES.has('co001a')).toBe(false) // la citation en retrait n'est pas une pente
  })
})
