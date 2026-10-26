// Rachel Summers / Marvel Girl (Dipsome, `rm001a`) : ce que la table DESSINE (étape 8 bis de PROCESSUS-CARTE, leçon
// Contingency Plan).
//
// Temporal Retrieval (`rm010`) attache jusqu'à 3 cartes de la main FACE CACHÉE sous une amélioration posée sur l'identité :
// attachement à DEUX étages, comme Contingency Plan (`su012`). Hound Clothes (`rm016`) s'attache à l'identité et Hound
// Program (`rm014`) est une manigance annexe qui accumule de la menace : l'un comme l'autre doivent se voir.
// Fixture écrite à la main (modèle `attachement-en-chaine.test.ts` et `corsair-plateau.test.ts`).
import { describe, expect, it } from 'vitest'
import { carteSurTable, cartesDessinees, dessinee, siege, tableAvec } from './plateau-de-test'

const MARVEL_GIRL = 1
const RETRIEVAL = 2
const GLISSEE_A = 3
const GLISSEE_B = 4
const VETEMENTS = 5
const PROGRAMME = 40

const monde = () =>
  tableAvec(
    siege({
      area_hero: [
        carteSurTable(MARVEL_GIRL, 'rm001a', 'Hero', 'Marvel Girl'),
        carteSurTable(RETRIEVAL, 'rm010', 'Upgrade', 'Temporal Retrieval', { bind_object_id: MARVEL_GIRL }),
        carteSurTable(GLISSEE_A, '01088', 'Resource', 'Energy', {
          bind_object_id: RETRIEVAL,
          is_face_up: false,
          visible_for_players: [0],
        }),
        carteSurTable(GLISSEE_B, '01089', 'Resource', 'Genius', {
          bind_object_id: RETRIEVAL,
          is_face_up: false,
          visible_for_players: [0],
        }),
        carteSurTable(VETEMENTS, 'rm016', 'Attachment', 'Hound Clothes', { bind_object_id: MARVEL_GIRL }),
      ],
    }),
    {
      area_schemes_side: [carteSurTable(PROGRAMME, 'rm014', 'SideScheme', 'Hound Program')],
    }
  )

describe('Marvel Girl, cartes attachées face cachée sous Temporal Retrieval', () => {
  it('dessine Marvel Girl', () => {
    expect(dessinee(monde(), MARVEL_GIRL)).toBeDefined()
  })

  // L'assertion qui aurait attrapé Contingency Plan : une carte attachée à une amélioration elle-même attachée.
  it('dessine chaque carte attachée à Temporal Retrieval', () => {
    expect(dessinee(monde(), GLISSEE_A)).toBeDefined()
    expect(dessinee(monde(), GLISSEE_B)).toBeDefined()
  })

  it('les remonte à l identité, juste derrière Temporal Retrieval, posées face cachée mais lisibles par leur propriétaire', () => {
    const vues = cartesDessinees(monde())
    const rang = (id: number) => vues.findIndex((c) => c.id === id)
    expect(dessinee(monde(), GLISSEE_A)?.portePar).toBe(MARVEL_GIRL)
    expect(rang(GLISSEE_A)).toBe(rang(RETRIEVAL) + 1)
    expect(dessinee(monde(), GLISSEE_A)?.peeking).toBe(true)
    expect(dessinee(monde(), GLISSEE_A)?.facedown).toBe(false)
  })

  // Cas témoin : l'amélioration porteuse reste attachée à l'identité, face visible.
  it('garde Temporal Retrieval attachée à Marvel Girl, face visible', () => {
    const carte = dessinee(monde(), RETRIEVAL)
    expect(carte?.portePar).toBe(MARVEL_GIRL)
    expect(carte?.peeking).toBe(false)
  })
})

describe('Hound Clothes et Hound Program', () => {
  it('dessine Hound Clothes attachée à l identité', () => {
    expect(dessinee(monde(), VETEMENTS)?.portePar).toBe(MARVEL_GIRL)
  })

  it('dessine la manigance annexe Hound Program', () => {
    expect(dessinee(monde(), PROGRAMME)).toBeDefined()
  })
})
