// LA MAIN PENDANT LA PHASE DU MECHANT (revirement du 05/10/2026) : le carre de
// la phase ne cache plus la main. Quand le moteur attend une reponse du
// joueur, la main est VISIBLE et cliquable, ses cartes jouables en
// surbrillance, pour qu'une carte mal parametree se voie et se signale.
import { describe, expect, it } from 'vitest'
import { mainVisibleForcee } from './main-visible'

const repos = {
  modeManuelDeclare: false,
  ciblageEnCours: false,
  etapeAssistant: undefined,
  carreDeLaPhase: false,
  questionAuJoueur: false,
} as const

describe('mainVisibleForcee', () => {
  it('au repos, la main garde son comportement normal (rognee)', () => {
    expect(mainVisibleForcee(repos)).toBe(false)
  })

  it('pendant le carre de la phase, une question pour le joueur montre la main', () => {
    expect(mainVisibleForcee({ ...repos, carreDeLaPhase: true, questionAuJoueur: true })).toBe(true)
  })

  it('pendant le carre de la phase, sans question, la main reste au repos', () => {
    expect(mainVisibleForcee({ ...repos, carreDeLaPhase: true })).toBe(false)
  })

  it('une question hors du carre ne force rien', () => {
    expect(mainVisibleForcee({ ...repos, questionAuJoueur: true })).toBe(false)
  })

  it('un ciblage en etape cible ou paiement montre la main, meme pendant la phase', () => {
    expect(mainVisibleForcee({ ...repos, ciblageEnCours: true, etapeAssistant: 'target' })).toBe(true)
    expect(mainVisibleForcee({ ...repos, ciblageEnCours: true, etapeAssistant: 'payment', carreDeLaPhase: true })).toBe(true)
    expect(mainVisibleForcee({ ...repos, ciblageEnCours: true, etapeAssistant: 'choose' })).toBe(false)
  })

  it('le mode manuel declare la montre toujours', () => {
    expect(mainVisibleForcee({ ...repos, modeManuelDeclare: true })).toBe(true)
  })
})
