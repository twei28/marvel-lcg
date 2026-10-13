import { describe, expect, it } from 'vitest'
import { COULEUR_COMMUNE, type CadreJoueur } from './couleur-joueur'
import type { EtapeDeroule } from './deroule-phase'
import { bordVers, flechesDeLEtape, traceEntre } from './fleches-phase'

const JAUNE = '#e6be3c'
const VERT = '#34ae61'
const cadres: CadreJoueur[] = [
  { couleurs: [JAUNE], raye: false, siege: 1 },
  { couleurs: [VERT], raye: false, siege: 2 },
]
// Spider-Man (1) et Black Cat (2) a J1, Hulk (3) a J2 ; Klaw (50), manigance (60).
const proprietaire: Record<number, number> = { 1: 0, 2: 0, 3: 1, 77: 0 }
const ctx = { cadres, joueurDeCarte: (id: number | undefined) => (id === undefined ? undefined : proprietaire[id]) }

const base = (e: Partial<EtapeDeroule>): EtapeDeroule => ({ cle: 'e', temps: 'mechant', titre: 'attaque', regle: '', boosts: [], ...e })

describe('flechesDeLEtape (lot 3, decisions 21 a 25, 39, 40)', () => {
  it('attaque : de l attaquant au personnage touche, dans la couleur de son joueur', () => {
    const f = flechesDeLEtape(base({ carteId: 50, cibleId: 1 }), ctx)
    expect(f).toEqual([{ cle: 'table-50>1', de: { lieu: 'table', id: 50 }, vers: { lieu: 'table', id: 1 }, couleur: JAUNE }])
  })

  it('attaque annoncee : vise la cible annoncee', () => {
    const f = flechesDeLEtape(base({ carteId: 50, cibleAnnonceeId: 3, etat: 'annonce' }), ctx)
    expect(f.map((x) => [x.vers.id, x.couleur])).toEqual([[3, VERT]])
  })

  it('Overkill (40) : deux fleches, attaquant -> defenseur puis defenseur -> identite', () => {
    const f = flechesDeLEtape(base({ carteId: 50, defenseurId: 2, cibleId: 1 }), ctx)
    expect(f.map((x) => x.cle)).toEqual(['table-50>2', 'table-2>1'])
  })

  it('un allie qui defend et encaisse : une seule fleche', () => {
    const f = flechesDeLEtape(base({ carteId: 50, defenseurId: 2, cibleId: 2 }), ctx)
    expect(f.map((x) => x.cle)).toEqual(['table-50>2'])
  })

  it('Riposte (39) : un coup du heros sur le sbire, la fleche part du heros', () => {
    const f = flechesDeLEtape(base({ temps: 'sbires', carteId: 1, cibleId: 77 }), ctx)
    expect(f[0].de).toEqual({ lieu: 'table', id: 1 })
    expect(f[0].vers.id).toBe(77)
  })

  it('manigance du mechant : de la boite vers la manigance, en gris acier', () => {
    const f = flechesDeLEtape(base({ temps: 'mechant', titre: 'manigance', carteId: 50, cibleId: 60 }), ctx)
    expect(f).toEqual([{ cle: 'corps>60', de: { lieu: 'boite-corps' }, vers: { lieu: 'table', id: 60 }, couleur: COULEUR_COMMUNE }])
  })

  it('manigance d un sbire : de sa carte vers la manigance', () => {
    const f = flechesDeLEtape(base({ temps: 'sbires', titre: 'manigance', carteId: 70, cibleId: 60 }), ctx)
    expect(f).toEqual([{ cle: 'table-70>60', de: { lieu: 'table', id: 70 }, vers: { lieu: 'table', id: 60 }, couleur: COULEUR_COMMUNE }])
  })

  it('etape 1 : de la boite vers la manigance, en gris acier', () => {
    const f = flechesDeLEtape(base({ temps: 'menace', titre: 'menace', cibleId: 60 }), ctx)
    expect(f).toEqual([{ cle: 'corps>60', de: { lieu: 'boite-corps' }, vers: { lieu: 'table', id: 60 }, couleur: COULEUR_COMMUNE }])
  })

  it('boosts : seulement les boosts etoile deja retournes, de la boite a leur place', () => {
    const e = base({
      carteId: 50,
      cibleId: 1,
      boosts: [
        { cle: 'b1', nom: 'Weapons Runner', cibleId: 90, apport: 0, etoile: true },
        { cle: 'b2', nom: 'Sonic Boom', cibleId: 91, apport: 2, etoile: true },
      ],
    })
    expect(flechesDeLEtape(e, { ...ctx, boostsMontres: 1 }).map((x) => x.cle)).toEqual(['table-50>1', 'boite-90>90'])
    expect(flechesDeLEtape(e, { ...ctx, boostsMontres: 0 }).map((x) => x.cle)).toEqual(['table-50>1'])
  })

  it('carte revelee : de la boite vers sa place, et ses effets vers leur cible', () => {
    const e = base({
      temps: 'revelation',
      titre: 'revelation',
      carteId: 80,
      effets: [
        { genre: 'menace', cible: 'Underground Distribution', cible_id: 60, montant: 2 },
        { genre: 'entree', carte: 'Hydra Soldier', carte_id: 81, type: 'sbire', engage_avec_id: 1 },
      ],
    })
    const f = flechesDeLEtape(e, ctx)
    expect(f.map((x) => [x.cle, x.couleur])).toEqual([
      ['boite-80>80', COULEUR_COMMUNE],
      ['boite-80>60', COULEUR_COMMUNE],
      ['boite-81>81', JAUNE],
    ])
  })

  it('sbire entre en jeu en pleine phase (boost etoile) : de la boite a sa place', () => {
    const f = flechesDeLEtape(base({ titre: 'entree', carteId: 77 }), ctx)
    expect(f.map((x) => [x.cle, x.couleur])).toEqual([['boite-77>77', JAUNE]])
  })

  it('rien sur une etape annulee ni sur le bilan', () => {
    expect(flechesDeLEtape(base({ carteId: 50, cibleId: 1, etat: 'annule' }), ctx)).toEqual([])
    expect(flechesDeLEtape(base({ temps: 'bilan', titre: 'bilan' }), ctx)).toEqual([])
    expect(flechesDeLEtape(undefined, ctx)).toEqual([])
  })
})

describe('traceEntre', () => {
  it('part du bord de la source et arrive au bord de la cible', () => {
    const de = { x: 0, y: 0, w: 100, h: 140 }
    const vers = { x: 400, y: 300, w: 100, h: 140 }
    const t = traceEntre(de, vers)
    expect(t.depart.x).toBeCloseTo(100, 0)
    expect(t.arrivee.x).toBeCloseTo(400, 0)
    expect(t.d.startsWith('M')).toBe(true)
    // La courbe est plus longue que le segment droit d'un bord a l'autre.
    expect(t.longueur).toBeGreaterThan(Math.hypot(t.arrivee.x - t.depart.x, t.arrivee.y - t.depart.y))
  })

  it('bordVers reste dans le rectangle', () => {
    const p = bordVers({ x: 10, y: 10, w: 50, h: 50 }, { x: 500, y: 35 })
    expect(p).toEqual({ x: 60, y: 35 })
  })
})
