// Rapport nicodede62 #147 (18/11/2026) : Mantis joue Bug (allié dont la cible est SON identité). L'identité peut payer par
// « Avantage empathique », mais garde son rôle de CIBLE : son « pulse » devenait l'éclair doré d'une cible, jamais le halo bleu
// de paiement. Rien ne disait au joueur qu'il pouvait cliquer Mantis pour payer.
import { describe, expect, it } from 'vitest'
import type { ScanCardProps } from '../components/ScanCard'
import { avecInteraction } from './Board'
import type { EtatInteractif } from './interaction'

const carte = { id: '1', name: 'Mantis' } as unknown as ScanCardProps

describe('halo bleu de paiement sur une carte qui est aussi la cible', () => {
  it('cible ET payeuse : halo de paiement, pas l’éclair de cible', () => {
    const etat: EtatInteractif = { role: 'cible', payeur: true, choisie: true, pulse: true }
    const rendu = avecInteraction(carte, new Map([[1, etat]]), new Map())
    expect(rendu.paymentPulse).toBe(true)
    expect(rendu.targetPulse).toBe(false)
  })

  it('cible seule : l’éclair de cible, inchangé', () => {
    const etat: EtatInteractif = { role: 'cible', choisie: false, pulse: true }
    const rendu = avecInteraction(carte, new Map([[1, etat]]), new Map())
    expect(rendu.paymentPulse).toBe(false)
    expect(rendu.targetPulse).toBe(true)
  })
})
