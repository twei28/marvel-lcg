// Refonte de la phase du méchant, lot 5b (essai, 12/10/2026) : Riposte (39) et
// mots-clés Perçant / Robuste / Déferlement (40), de bout en bout côté plateau.
import { describe, expect, it } from 'vitest'
import type { EtapeDeroule } from './deroule-phase'
import { etapesDeroule } from './deroule-phase'
import { avecEtapesRiposte } from './etapes-essai'
import { flechesDeLEtape } from './fleches-phase'
import { lignesMotsCles, titreCourt, vueDeLEtape, type ContexteVue, type VueRangee } from './vue-cartouche'
import type { FaitMechant } from './world'

const base = (e: Partial<EtapeDeroule>): EtapeDeroule => ({
  cle: 'activation:1',
  temps: 'mechant',
  titre: 'attaque',
  regle: 'regle:activations',
  boosts: [],
  ...e,
})

const ctx = (etapes: EtapeDeroule[]): ContexteVue =>
  ({ etapes, indexCourant: 0, boostsMontres: 9, pvMaxParNom: new Map([['Rhino', 14]]) }) as unknown as ContexteVue

describe('avecEtapesRiposte (decision 39)', () => {
  it('insere un ecran Riposte juste apres l attaque, les roles inverses', () => {
    const attaque = base({ carteId: 50, cibleId: 1, auteurNom: 'Rhino', cibleNom: 'Spider-Man', etat: 'resolu', montant: 2, riposte: { degats: 1, restant: 13, vaincu: false } })
    const suite = avecEtapesRiposte([attaque, base({ cle: 'activation:2' })])
    expect(suite.map((e) => e.cle)).toEqual(['activation:1', 'activation:1:riposte', 'activation:2'])
    expect(suite[1]).toMatchObject({ titre: 'riposte', carteId: 1, cibleId: 50, auteurNom: 'Spider-Man', cibleNom: 'Rhino', montant: 1, restant: 13 })
  })

  it('sans riposte, la meme liste (meme identite)', () => {
    const etapes = [base({ carteId: 50, cibleId: 1 })]
    expect(avecEtapesRiposte(etapes)).toBe(etapes)
  })

  it('une attaque annulee ne riposte pas', () => {
    const etapes = [base({ etat: 'annule', riposte: { degats: 1 } })]
    expect(avecEtapesRiposte(etapes)).toHaveLength(1)
  })
})

describe('vue de la Riposte (decision 39)', () => {
  it('acteur = la carte touchee, cible = l attaquant avec ses PV, VAINCU', () => {
    const riposte = avecEtapesRiposte([
      base({ carteId: 50, cibleId: 1, auteurNom: 'Rhino', cibleNom: 'Spider-Man', etat: 'resolu', montant: 2, riposte: { degats: 1, restant: 0, vaincu: true } }),
    ])[1]
    const vue = vueDeLEtape(riposte, ctx([riposte])) as VueRangee
    expect(vue.genre).toBe('rangee')
    expect(vue.riposte).toEqual({ vaincu: true })
    expect(vue.acteur?.carteId).toBe(1)
    expect(vue.cibles[0]?.carteId).toBe(50)
    expect(vue.resultat?.texte).toContain('VAINCU')
    expect(vue.resultat?.jauge).toEqual({ avant: 1, apres: 0, plafond: 14 })
    expect(titreCourt(riposte, ctx([riposte]))).toBe('Riposte de Spider-Man')
  })

  it('la fleche part de la carte touchee vers l attaquant', () => {
    const riposte = avecEtapesRiposte([base({ carteId: 50, cibleId: 1, etat: 'resolu', riposte: { degats: 1 } })])[1]
    const fleches = flechesDeLEtape(riposte, { cadres: [], joueurDeCarte: () => undefined })
    expect(fleches.map((f) => f.cle)).toEqual(['table-1>50'])
  })
})

describe('mots-cles du coup (decision 40)', () => {
  it('une ligne par mot-cle qui a joue', () => {
    expect(lignesMotsCles(base({ motsCles: { percant: true } }))).toEqual(['Perçant : la carte Robuste est défaussée avant les dégâts'])
    expect(lignesMotsCles(base({ motsCles: { robuste: true } }))).toEqual(['Robuste : la carte Robuste absorbe tout le coup'])
    expect(lignesMotsCles(base({ motsCles: { overkill: { cible: 'Spider-Man', cible_id: 1, degats: 3 } } }))).toEqual([
      'Déferlement : 3 dégâts en trop sur Spider-Man',
    ])
    expect(lignesMotsCles(base({}))).toBeUndefined()
  })

  it('la vue d une attaque resolue porte les lignes, pas une annonce', () => {
    const resolue = base({ carteId: 50, cibleId: 2, etat: 'resolu', montant: 2, motsCles: { robuste: true } })
    expect((vueDeLEtape(resolue, ctx([resolue])) as VueRangee).motsCles).toHaveLength(1)
    const annonce = base({ carteId: 50, cibleId: 2, etat: 'annonce', motsCles: { robuste: true } })
    expect((vueDeLEtape(annonce, ctx([annonce])) as VueRangee).motsCles).toBeUndefined()
  })

  it('Deferlement : seconde fleche de la carte abattue vers celle qui recoit l exces', () => {
    const etape = base({ carteId: 50, cibleId: 2, etat: 'resolu', motsCles: { overkill: { cible: 'Spider-Man', cible_id: 1, degats: 1 } } })
    const fleches = flechesDeLEtape(etape, { cadres: [], joueurDeCarte: () => undefined })
    expect(fleches.map((f) => f.cle)).toEqual(['table-50>2', 'table-2>1'])
  })

  it('etapesDeroule recopie mots_cles et riposte du fait resolu', () => {
    const fait = {
      genre: 'attaque',
      etat: 'resolu',
      activation_id: 1,
      phase: 'Enemy Activation',
      round_id: 3,
      auteur: 'Rhino',
      auteur_id: 50,
      cible: 'Spider-Man',
      cible_id: 1,
      base: 2,
      boost: 0,
      defense: 0,
      inflige: 2,
      subi: 0,
      restant: 10,
      boosts: [],
      mots_cles: { robuste: true },
      riposte: { degats: 1, restant: 13, vaincu: false },
    } as unknown as FaitMechant
    const [etape] = etapesDeroule([fait], [], 3, new Set([50]), new Set())
    expect(etape?.motsCles).toEqual({ robuste: true })
    expect(etape?.riposte).toEqual({ degats: 1, restant: 13, vaincu: false })
  })
})
