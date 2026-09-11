// Releve en jouant, 11/09/2026 : un tap sur le heros ouvre bien ses actions,
// mais la carte s'agrandissait de 2,5x sur place et sortait de l'ecran par la
// gauche (mesure : bord gauche a -69 px sur 500). Le nom et l'etiquette
// etaient coupes.
//
// Cause : `ScanCard.css` agrandit `.scan-visuel` sur `:hover` et
// `:focus-visible`. Sur le plateau PC c'est la loupe de consultation, a la
// souris. Sur un telephone il n'y a pas de souris, et le tap POSE LE FOCUS :
// l'agrandissement se declenchait a chaque fois qu'on jouait une carte. Le
// portrait a deja son propre geste de lecture (tap pour ouvrir), il n'a rien
// a faire de cette loupe.
//
// jsdom ne fait pas de mise en page : on verrouille la REGLE dans la feuille,
// comme portrait-table-defilement.test.ts.

import { readFileSync } from 'node:fs'
import { describe, expect, it } from 'vitest'

const CSS = readFileSync('src/board/mobile/portrait.css', 'utf-8')

describe('le plateau portrait', () => {
  it('n\'agrandit pas les cartes au survol ni au focus', () => {
    expect(CSS).toContain('.plateau-portrait .scan-card:focus-visible .scan-visuel')
    expect(CSS).toContain('transform: none')
  })
})
