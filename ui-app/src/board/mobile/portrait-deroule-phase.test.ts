// La scene de la phase du mechant (DeroulePhase), ancree en bas en portrait.
//
// jsdom ne fait pas de mise en page (pas de position:fixed calculee, pas de
// dvh) : ce genre de regle ne peut pas se verifier au rendu. On verrouille
// donc la REGLE dans la feuille, comme le fait deja
// ui-app/src/board/deroule-survol.test.ts.
//
// PIEGE evite ici : DeroulePhase et PlateauPortrait sont rendus COTE A COTE
// dans le meme fragment racine (board.tsx), jamais l'un dans l'autre. Un
// selecteur descendant `.plateau-portrait .deroule-phase` ne matcherait donc
// JAMAIS : on verifie ici que la regle utilise bien `:has()` avec un
// combinateur de fratrie, la seule facon de conditionner ce style a
// « on est en portrait telephone » depuis la feuille seule.

import { readFileSync } from 'node:fs'
import { describe, expect, it } from 'vitest'

// Chemin depuis la racine d'ui-app, comme deroule-survol.test.ts.
const CSS = readFileSync('src/board/mobile/portrait.css', 'utf-8')

/** Les declarations d'un selecteur, sans les regles voisines. */
function bloc(selecteur: string): string {
  const debut = CSS.indexOf(`\n  ${selecteur} {`)
  expect(debut, `selecteur absent de portrait.css : ${selecteur}`).toBeGreaterThan(-1)
  return CSS.slice(debut, CSS.indexOf('}', debut))
}

describe('la scene de la phase du mechant en portrait', () => {
  it('cible .deroule-phase par fratrie, pas par descendance (DeroulePhase et PlateauPortrait sont cote a cote)', () => {
    // La regle existe bel et bien : bloc() leve si ce selecteur (littéral,
    // sur sa propre ligne d'ouverture) est absent de la feuille.
    expect(bloc('.deroule-phase:has(~ .plateau-portrait)')).not.toBe('')
  })

  it('sort la scene de son ancrage flottant : pleine largeur, collee en bas', () => {
    const regle = bloc('.deroule-phase:has(~ .plateau-portrait)')
    expect(regle).toContain('bottom: 0')
    expect(regle).toContain('width: 100%')
    expect(regle).toContain('transform: none')
  })

  it('plafonne sa hauteur a l ecran moins l entete (24/10/2026, avant : la moitie) et defile au-dela', () => {
    const regle = bloc('.deroule-phase:has(~ .plateau-portrait)')
    expect(regle).toContain('max-height: calc(100dvh - 56px)')
    expect(regle).toContain('overflow-y: auto')
  })

  it('reste ancree en bas meme quand le moteur pose une question (.est-question redefinit bottom sur PC)', () => {
    expect(bloc('.deroule-phase.est-question:has(~ .plateau-portrait)')).toContain('bottom: 0')
  })

  it('vit dans la couche utilitaires, seule a primer sur la regle generale (elle-meme en utilitaires, board.css)', () => {
    // La regle generale de .deroule-phase vit dans @layer utilitaires
    // (board.css) : un override loge dans @layer composants serait ignore,
    // quelle que soit sa specificite (utilitaires prime toujours dans ce
    // projet, voir le commentaire de board.css:1839). On verifie donc que la
    // regle vit APRES l'ouverture d'un `@layer utilitaires` dans ce fichier.
    const ouverture = CSS.lastIndexOf('@layer utilitaires')
    const position = CSS.indexOf('.deroule-phase:has(~ .plateau-portrait)')
    expect(ouverture).toBeGreaterThan(-1)
    expect(position).toBeGreaterThan(ouverture)
  })

  it('assombrit le plateau derriere la scene, comme sur PC (.deroule-voile .plateau-scene::after, board.css)', () => {
    expect(CSS).toContain('.deroule-voile .plateau-portrait::after')
  })
})
