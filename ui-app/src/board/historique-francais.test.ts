// Releve du 11/09/2026 dans le navigateur, partie en francais : le panneau
// d'historique s'ouvrait sur « GAME HISTORY », et chaque entree de phase
// disait « Player 1 Turn ».
//
// Deux causes distinctes :
//  - le titre du panneau etait ecrit en anglais EN DUR, alors que dico-en.ts
//    porte deja la paire « Historique de la partie » -> « Game history » ;
//  - l'entree de phase recopiait `monde.phase`, la chaine BRUTE du moteur,
//    alors que libellePhase() sait la dire (« Tour de Steve Rogers »).

import { describe, expect, it } from 'vitest'
import { readFileSync } from 'node:fs'
import { libellePhase } from './etat-partie'
import type { World } from './world'

const monde = (phase: string): World =>
  ({ phase, round_id: 1, players: [{ area_hero: [{ name: '* Steve Rogers' }] }] }) as unknown as World

describe('l\'historique, en francais', () => {
  it('dit la phase en clair au lieu de recopier la chaine du moteur', () => {
    // Le garde-fou : si libellePhase cessait de traduire, l'assertion suivante
    // ne prouverait plus rien.
    expect(libellePhase(monde('Player 1 Turn'))).toBe('Tour de Steve Rogers')
  })

  it('n\'ecrit plus « Game history » en dur dans le panneau', () => {
    const source = readFileSync('src/board/HistoriquePartie.tsx', 'utf-8')
    expect(source).not.toContain('"Game history"')
    expect(source).not.toContain('>Game history<')
  })

  it('passe la phase de l\'entree par libellePhase', () => {
    const source = readFileSync('src/board/HistoriquePartie.tsx', 'utf-8')
    expect(source).toContain('libellePhase')
  })
})
