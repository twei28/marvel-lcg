// Ce qu'une etape demande a l'ecran : quelle carte mettre en avant, faut-il
// tracer un trait vers une cible, faut-il assombrir le reste.
//
// Module PUR, sans DOM : la decision se teste ici, la pose se fait ailleurs
// (useDerouleScene.ts). C'est le meme partage que pas-a-pas.ts, ou le rythme
// vit dans moteur.ts et la decoration dans le hook.
import { describe, expect, it } from 'vitest'
import { sceneDe } from './deroule-scene'
import type { EtapeDeroule } from './deroule-phase'

const etape = (extra: Partial<EtapeDeroule> = {}): EtapeDeroule => ({
  cle: 'k',
  temps: 'sbires',
  titre: 'attaque',
  regle: 'regle:activations',
  boosts: [],
  consequences: [],
  ...extra,
})

describe('mise en scene d une etape', () => {
  it('met en avant la carte qui agit', () => {
    expect(sceneDe(etape({ carteId: 50 })).carteEnAvant).toBe(50)
  })

  it('trace un trait quand l etape a un auteur ET une cible', () => {
    const scene = sceneDe(etape({ carteId: 50, cibleId: 12 }))
    expect(scene.trait).toBe(true)
    expect(scene.cible).toBe(12)
  })

  it('ne trace aucun trait sans cible', () => {
    expect(sceneDe(etape({ carteId: 50 })).trait).toBe(false)
  })

  it('ne trace aucun trait quand l auteur est sa propre cible', () => {
    // Un trait qui part d'une carte pour y revenir ne montre rien.
    expect(sceneDe(etape({ carteId: 50, cibleId: 50 })).trait).toBe(false)
  })

  it('assombrit le plateau des qu une carte est mise en avant', () => {
    expect(sceneDe(etape({ carteId: 50 })).voile).toBe(true)
  })

  it('n assombrit rien sur une etape sans carte', () => {
    // « Aucun sbire en jeu », le passage du premier joueur : le cartouche parle
    // seul, l'ecran ne bouge pas pour rien.
    const scene = sceneDe(etape({ carteId: undefined }))
    expect(scene.voile).toBe(false)
    expect(scene.carteEnAvant).toBeUndefined()
  })
})
