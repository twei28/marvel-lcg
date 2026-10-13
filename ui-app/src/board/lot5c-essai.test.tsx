// Refonte de la phase du méchant, lot 5c (essai, 12/10/2026) : distribution en
// tableau (42), effet ★ différé (38), élimination (45), suite d'un changement
// de stade (11). L'ordre des activations (41, 47) vit dans SousCadre.test.tsx.
import { afterEach, describe, expect, it, vi } from 'vitest'
import { cleanup, render } from '@testing-library/react'
import { CartouchePhase, type CartouchePhaseProps } from './CartouchePhase'
import type { EtapeDeroule } from './deroule-phase'
import { etapesDeroule } from './deroule-phase'
import {
  avecEcranElimination,
  avecEtapesEtoileDifferee,
  avecEtapesRiposte,
  avecTableauDistribution,
  effetEtoileDiffere,
} from './etapes-essai'
import { titreCourt, vueDeLEtape, type ContexteVue, type VueDistribution, type VueRangee, type VueStade } from './vue-cartouche'
import type { FaitMechant } from './world'

const base = (e: Partial<EtapeDeroule>): EtapeDeroule => ({
  cle: 'activation:1',
  temps: 'mechant',
  titre: 'attaque',
  regle: 'regle:activations',
  boosts: [],
  ...e,
})

const ctx = (etapes: EtapeDeroule[], extra: Partial<ContexteVue> = {}): ContexteVue =>
  ({ etapes, indexCourant: 0, boostsMontres: 9, pvMaxParNom: new Map(), ...extra }) as unknown as ContexteVue

const distribution = (joueur: number, extra: Record<string, unknown> = {}) =>
  ({ genre: 'distribution', phase: 'Deal Encounter Cards', round_id: 3, joueur, joueur_nom: `Héros ${joueur + 1}`, ...extra }) as unknown as FaitMechant

describe('la distribution en tableau (decision 42)', () => {
  it('etapesDeroule recopie la raison de chaque carte, les cartes recues plus tot d abord', () => {
    const faits = [
      distribution(0, { raison: 'base', deja: [{ raison: 'carte', source: 'Hydra Soldier' }] }),
      distribution(1, { raison: 'base' }),
      distribution(0, { raison: 'danger', source: 'Illegal Arms Factory' }),
    ]
    const etapes = etapesDeroule(faits, [], 3, new Set(), new Set(), 0, ['Héros 1', 'Héros 2'])
    const j1 = etapes.find((e) => e.titre === 'distribution' && e.joueur === 0)
    expect(j1?.montant).toBe(2)
    expect(j1?.raisonsCartes).toEqual([
      { raison: 'carte', source: 'Hydra Soldier' },
      { raison: 'base' },
      { raison: 'danger', source: 'Illegal Arms Factory' },
    ])
  })

  it('un moteur ancien (sans raison) ne publie aucune raison', () => {
    const etapes = etapesDeroule([distribution(0)], [], 3, new Set(), new Set(), 0, ['Héros 1'])
    expect(etapes.find((e) => e.titre === 'distribution')?.raisonsCartes).toBeUndefined()
  })

  it('les etapes « X recoit N cartes » deviennent UN tableau, a la place de la premiere', () => {
    const avant = base({ cle: 'a' })
    const d1 = base({ cle: 'd1', temps: 'distribution', titre: 'distribution', joueur: 0, auteurNom: 'Spider-Man', montant: 2, raisonsCartes: [{ raison: 'base' }, { raison: 'danger', source: 'Illegal Arms Factory' }] })
    const d2 = base({ cle: 'd2', temps: 'distribution', titre: 'distribution', joueur: 1, auteurNom: 'Hulk', montant: 1 })
    const apres = base({ cle: 'r', temps: 'revelation', titre: 'revelation' })
    const suite = avecTableauDistribution([avant, d1, d2, apres])
    expect(suite.map((e) => e.cle)).toEqual(['a', 'd1:tableau', 'r'])
    expect(suite[1]).toMatchObject({ titre: 'distribution-tableau', temps: 'distribution', montant: 3 })
    const vue = vueDeLEtape(suite[1], ctx(suite)) as VueDistribution
    expect(vue.genre).toBe('distribution')
    expect(vue.lignes.map((l) => [l.nom, l.cartes, l.raisons])).toEqual([
      ['Spider-Man', 2, ['la règle (1 par joueur)', 'Danger : Illegal Arms Factory']],
      ['Hulk', 1, []],
    ])
    // 13/10/2026 (encadré ⑪) : le titre dit combien.
    expect(titreCourt(suite[1], ctx(suite))).toBe('Distribution : 3 cartes rencontre')
  })

  it('13/10/2026 : en solo, une seule carte sans raison particulière n a pas d ecran', () => {
    const d1 = base({ cle: 'd1', temps: 'distribution', titre: 'distribution', joueur: 0, auteurNom: 'Spider-Man', montant: 1, raisonsCartes: [{ raison: 'base' }] })
    const apres = base({ cle: 'r', temps: 'revelation', titre: 'revelation' })
    expect(avecTableauDistribution([d1, apres]).map((e) => e.cle)).toEqual(['r'])
    const danger = base({ ...d1, raisonsCartes: [{ raison: 'danger', source: 'Illegal Arms Factory' }] })
    expect(avecTableauDistribution([danger, apres]).map((e) => e.cle)).toEqual(['d1:tableau', 'r'])
  })

  it('sans distribution, la meme liste', () => {
    const etapes = [base({})]
    expect(avecTableauDistribution(etapes)).toBe(etapes)
  })
})

describe('l effet ★ differe (decision 38)', () => {
  it('reconnait les effets qui s appliquent apres le retournement, FR et EN', () => {
    expect(effetEtoileDiffere('If this activation deals damage to you, exhaust your hero.')).toBe(true)
    expect(effetEtoileDiffere('si cette activation vous inflige des dégâts, inclinez votre héros.')).toBe(true)
    expect(effetEtoileDiffere('After this activation ends, reveal this card.')).toBe(true)
    expect(effetEtoileDiffere('Deal 1 damage to each hero.')).toBe(false)
    expect(effetEtoileDiffere(undefined)).toBe(false)
  })

  const texteEtoile = (id: number) => (id === 70 ? 'If this activation deals damage to you, exhaust your hero.' : 'Deal 1 damage.')
  const attaque = base({
    carteId: 50,
    cibleId: 1,
    auteurNom: 'Klaw',
    cibleNom: 'Spider-Man',
    etat: 'resolu',
    montant: 2,
    boosts: [
      { cle: 'b70', nom: 'Sonic Boom', cibleId: 70, apport: 2, etoile: true },
      { cle: 'b71', nom: 'Other', cibleId: 71, apport: 0, etoile: true },
    ],
  })

  it('un ecran a part, apres l attaque ET sa Riposte, seulement pour le boost differe', () => {
    const avecRiposte = avecEtapesRiposte([{ ...attaque, riposte: { degats: 1 } }, base({ cle: 'activation:2' })])
    const suite = avecEtapesEtoileDifferee(avecRiposte, texteEtoile)
    expect(suite.map((e) => e.cle)).toEqual(['activation:1', 'activation:1:riposte', 'activation:1:etoile:b70', 'activation:2'])
    expect(suite[2]).toMatchObject({ titre: 'etoile-differe', carteId: 70, auteurNom: 'Sonic Boom', montant: 2 })
  })

  it('l issue dit si la condition est remplie', () => {
    const [, ecran] = avecEtapesEtoileDifferee([attaque], texteEtoile)
    const vue = vueDeLEtape(ecran, ctx([ecran], { texteEtoile })) as VueRangee
    expect(vue.etoileDifferee?.issue).toBe('Condition remplie : 2 dégâts subis, l’effet s’applique.')
    const sansDegats = { ...ecran, montant: 0 }
    expect((vueDeLEtape(sansDegats, ctx([sansDegats], { texteEtoile })) as VueRangee).etoileDifferee?.issue).toBe('Sans effet : aucun dégât subi.')
    expect(titreCourt(ecran, ctx([ecran]))).toBe('Effet ★ de Sonic Boom')
  })

  it('sans texte ★ ou sur une annonce : rien n est insere', () => {
    expect(avecEtapesEtoileDifferee([attaque], undefined)).toEqual([attaque])
    expect(avecEtapesEtoileDifferee([{ ...attaque, etat: 'annonce' }], texteEtoile)).toHaveLength(1)
  })
})

describe('l elimination (decision 45)', () => {
  it('un ecran dedie juste apres le coup qui met un heros a terre', () => {
    const coup = base({ carteId: 50, cibleId: 1, cibleNom: 'Spider-Man', etat: 'resolu', defaite: true })
    const suite = avecEcranElimination([coup, base({ cle: 'activation:2' })])
    expect(suite.map((e) => e.cle)).toEqual(['activation:1', 'activation:1:elimination', 'activation:2'])
    const vue = vueDeLEtape(suite[1], ctx(suite)) as VueRangee
    expect(vue.elimine).toBe(true)
    expect(vue.acteur?.carteId).toBe(1)
    expect(titreCourt(suite[1], ctx(suite))).toBe('Spider-Man est éliminé')
  })

  it('sans defaite, la meme liste', () => {
    const etapes = [base({})]
    expect(avecEcranElimination(etapes)).toBe(etapes)
  })
})

describe('le rendu (essai seulement)', () => {
  afterEach(() => cleanup())
  const monter = (etapes: EtapeDeroule[], essai: boolean) => {
    const props: CartouchePhaseProps = {
      refCartouche: () => {},
      gestes: { onPointerDown: () => {}, onPointerMove: () => {}, onPointerUp: () => {}, onPointerCancel: () => {} },
      etape: etapes[0],
      etapes,
      index: 0,
      efface: false,
      questionAuJoueur: false,
      avancer: vi.fn(),
      enAttente: false,
      attendUnAutreJoueur: false,
      defaiteLocale: false,
      boostsMontres: 99,
      tempsParDecision: 0,
      cartesDistribuees: 0,
      essai,
    } as unknown as CartouchePhaseProps
    return render(<CartouchePhase {...props} />)
  }

  it('le tableau de distribution', () => {
    const [tableau] = avecTableauDistribution([
      base({ cle: 'd1', temps: 'distribution', titre: 'distribution', joueur: 0, auteurNom: 'Spider-Man', montant: 2 }),
    ])
    monter([tableau], true)
    expect(document.querySelector('.essai-distribution table')?.textContent).toContain('Spider-Man')
  })

  it('la suite d un changement de stade, dans l essai seulement', () => {
    const stade = base({ cle: 's', titre: 'stade', stade: 'manigance', carteId: 5, cibleNom: 'Underground Distribution' })
    expect((vueDeLEtape(stade, ctx([stade])) as VueStade).suite).toContain('La phase continue')
    monter([stade], true)
    expect(document.querySelector('.essai-stade-suite')?.textContent).toContain('La phase continue')
    cleanup()
    monter([stade], false)
    expect(document.querySelector('.essai-stade-suite')).toBeNull()
  })
})
