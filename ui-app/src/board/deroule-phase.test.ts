// Le decoupage de la phase du mechant en ETAPES a valider une par une.
//
// La source n'est pas une relecture du monde : le moteur envoie deja ses
// activations resolues (`FaitMechant`), avec la composition du coup — base,
// boost, defense — qu'aucune deduction ne saurait reconstituer. Le journal
// complete pour ce que les faits ne couvrent pas.
import { describe, expect, it } from 'vitest'
import { etapesDeroule } from './deroule-phase'
import type { FaitMechant } from './world'
import type { EntreeHistorique } from './HistoriquePartie'

const attaque = (extra: Partial<FaitMechant> = {}): FaitMechant => ({
  genre: 'attaque',
  phase: 'Enemy Activation',
  auteur: 'Ultron',
  auteur_id: 50,
  cible: 'Shuri',
  cible_id: 12,
  base: 3,
  boost: 2,
  defense: 0,
  inflige: 5,
  subi: 5,
  restant: 7,
  boosts: [],
  ...extra,
})

const entree = (extra: Partial<EntreeHistorique> = {}): EntreeHistorique =>
  ({
    cle: 'k1',
    type: 'threat',
    renderId: 1,
    round: 1,
    phase: 'Main Scheme Place Threat',
    titre: 'Menace posee',
    valeur: 1,
    ...extra,
  }) as EntreeHistorique

describe('etapesDeroule', () => {
  it('fait une etape par activation du moteur', () => {
    const etapes = etapesDeroule([attaque(), attaque({ auteur: 'Drone', auteur_id: 60 })], [])
    const activations = etapes.filter((e) => e.temps === 'activations')
    expect(activations).toHaveLength(2)
  })

  it('met la carte qui agit en avant et retient sa cible', () => {
    const [etape] = etapesDeroule([attaque()], []).filter((e) => e.temps === 'activations')
    expect(etape.carteId).toBe(50)
    expect(etape.cibleId).toBe(12)
  })

  it('porte les boosts de l activation, dans l ordre', () => {
    const etapes = etapesDeroule(
      [attaque({ boosts: [{ nom: 'Boost A', id: 91, apport: 1 }, { nom: 'Boost B', id: 92, apport: 1 }] })],
      []
    )
    const [etape] = etapes.filter((e) => e.temps === 'activations')
    expect(etape.boosts.map((b) => b.nom)).toEqual(['Boost A', 'Boost B'])
    expect(etape.boosts.map((b) => b.cle)).toEqual(['boost:0:91', 'boost:1:92'])
  })

  it('range une activation declenchee par une carte revelee sous la revelation', () => {
    // Un vilain peut frapper une seconde fois hors de l'etape des activations :
    // le fait porte sa propre phase, on la suit plutot que de tout ranger sous
    // « activations ».
    const etapes = etapesDeroule([attaque({ phase: 'Reveal Encounter Cards' })], [])
    expect(etapes.filter((e) => e.temps === 'revelation')).toHaveLength(1)
    expect(etapes.filter((e) => e.temps === 'activations')).toHaveLength(0)
  })

  it('fait une etape de menace a partir du journal', () => {
    const etapes = etapesDeroule([], [entree()])
    expect(etapes.filter((e) => e.temps === 'menace')).toHaveLength(1)
  })

  it('donne une cle stable et unique a chaque etape', () => {
    const etapes = etapesDeroule([attaque(), attaque({ auteur_id: 60 })], [entree()])
    const cles = etapes.map((e) => e.cle)
    expect(new Set(cles).size).toBe(cles.length)
  })

  it('rend les etapes dans l ordre des quatre temps', () => {
    const etapes = etapesDeroule(
      [attaque(), attaque({ phase: 'Reveal Encounter Cards', auteur_id: 60 })],
      [entree()]
    )
    expect(etapes.map((e) => e.temps)).toEqual(['menace', 'activations', 'revelation'])
  })

  it('ne rend aucune etape quand la phase n a rien produit', () => {
    expect(etapesDeroule([], [])).toEqual([])
  })
})
