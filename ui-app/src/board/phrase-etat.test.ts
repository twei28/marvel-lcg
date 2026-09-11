// La consigne et la phrase d'état de l'assistant (design essai).
//
// Le panneau dit trois choses, dans cet ordre : QUOI (la carte), CE QU'ON TE
// DEMANDE (« Payer 1 pour jouer »), OÙ ON EN EST (« Il manque 1 ressource »).
// Aucun nom de carte dans la phrase : les cartes payables brillent déjà dans
// la main, et en désigner une pousserait vers un choix qui n'est pas
// forcément le bon (retour de l'utilisateur, 11/09/2026).

import { describe, expect, it } from 'vitest'
import type { AssistantInteraction } from './interaction'
import { consigne, phraseEtat } from './phrase-etat'

function assistant(partiel: Partial<AssistantInteraction>): AssistantInteraction {
  return {
    etape: 'payment',
    titre: 'Payer le coût',
    cibleMinimum: 0,
    cibleMaximum: 0,
    cibleNombre: 0,
    ciblePossibles: 0,
    cibleRepetable: false,
    coutPaye: 0,
    coutSlots: [],
    coutRegles: [],
    ...partiel,
  }
}

describe('phraseEtat', () => {
  it('compte ce qui manque, au singulier comme au pluriel', () => {
    expect(phraseEtat(assistant({ coutPaye: 0, coutRequis: 1 }), false)).toBe('Il manque 1 ressource')
    expect(phraseEtat(assistant({ coutPaye: 1, coutRequis: 3 }), false)).toBe('Il manque 2 ressources')
  })

  it('nomme le type quand le coût est par types', () => {
    expect(phraseEtat(assistant({ typesManquants: { Y: 1 } }), false)).toBe('Il manque 1 énergie')
    expect(phraseEtat(assistant({ typesManquants: { B: 1, Y: 1 } }), false)).toBe(
      'Il manque 1 mentale et 1 énergie'
    )
  })

  it('dit que le coût est couvert plutôt que de répéter le compte', () => {
    expect(phraseEtat(assistant({ coutPaye: 2, coutRequis: 2 }), true)).toBe('Coût couvert')
  })

  it('annonce que tout est prêt à la confirmation', () => {
    expect(phraseEtat(assistant({ etape: 'confirm' }), true)).toBe('Tout est prêt')
  })

  it('garde le détail du ciblage tel quel', () => {
    expect(phraseEtat(assistant({ etape: 'target', detail: '1/3 requise(s)' }), false)).toBe(
      '1/3 requise(s)'
    )
  })
})

describe('consigne', () => {
  it('dit combien payer et pour quoi', () => {
    expect(consigne(assistant({ coutRequis: 1 }), 'Jouer')).toBe('Payer 1 pour jouer')
    expect(consigne(assistant({ coutRequis: 2 }), 'Attaquer')).toBe('Payer 2 pour attaquer')
  })

  it('retombe sur « Payer le coût » quand le nombre n’est pas connu (coût X, types)', () => {
    expect(consigne(assistant({ coutRequis: undefined }), 'Jouer')).toBe('Payer le coût')
  })

  it('reprend le titre du ciblage hors paiement', () => {
    expect(consigne(assistant({ etape: 'target', titre: 'Choisir la cible' }), 'Jouer')).toBe(
      'Choisir la cible'
    )
  })
})
