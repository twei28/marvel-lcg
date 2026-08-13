// Ce que ces cas protègent : le bilan doit ranger chaque fait sous l'étape de
// la phase du méchant qui l'a produit, et TOTALISER juste.
//
// Les deux se sont déjà trompés autrement. Le panneau d'origine groupait par
// nature (dégâts / menace / révélé), ce qui mélangeait dans un même bloc la
// menace posée à l'étape 1 et celle d'une manigance jouée à l'étape 4 : rien ne
// disait plus d'où venait quoi. Et un total qui additionnerait des valeurs
// absolues compterait une menace RETIRÉE comme une menace posée, ce qui donne
// un bilan faux dans le sens le plus trompeur possible — celui qui exagère le
// danger.
import { describe, expect, it } from 'vitest'
import { bilanDeLaPhase } from './RecapPhaseMechant'
import type { EntreeHistorique } from './HistoriquePartie'

let compteur = 0
const entree = (partiel: Partial<EntreeHistorique>): EntreeHistorique => ({
  cle: `e${(compteur += 1)}`,
  type: 'card',
  renderId: compteur,
  round: 2,
  phase: 'Reveal Encounter Cards',
  titre: 'Carte',
  ...partiel,
})

/** L'historique empile les plus récentes EN TÊTE : les cas suivent cet ordre. */
const commeDansLHistorique = (...anciennesDAbord: EntreeHistorique[]) =>
  [...anciennesDAbord].reverse()

describe('bilanDeLaPhase', () => {
  it('range chaque fait sous son étape, dans l’ordre de la carte de référence', () => {
    const bilan = bilanDeLaPhase(
      commeDansLHistorique(
        entree({ phase: 'Main Scheme Place Threat', type: 'threat', titre: 'Manigance +1', valeur: 1, restant: 1 }),
        entree({ phase: 'Enemy Activation', type: 'damage', titre: 'Klaw frappe', valeur: -3 }),
        entree({ phase: 'Reveal Encounter Cards', titre: 'Gang-Up révélée' })
      ),
      2
    )

    expect(bilan?.etapes.map((e) => e.numero)).toEqual([1, 2, 4])
    expect(bilan?.etapes[0].entrees.map((e) => e.titre)).toEqual(['Manigance +1'])
    expect(bilan?.etapes[1].entrees.map((e) => e.titre)).toEqual(['Klaw frappe'])
  })

  it('n’invente pas d’étape vide', () => {
    const bilan = bilanDeLaPhase(
      commeDansLHistorique(entree({ phase: 'Enemy Activation', type: 'damage', valeur: -2 })),
      2
    )
    expect(bilan?.etapes).toHaveLength(1)
    expect(bilan?.etapes[0].numero).toBe(2)
  })

  it('garde l’ordre de jeu à l’intérieur d’une étape', () => {
    const bilan = bilanDeLaPhase(
      commeDansLHistorique(
        entree({ titre: 'Première' }),
        entree({ titre: 'Deuxième' }),
        entree({ titre: 'Troisième' })
      ),
      2
    )
    expect(bilan?.etapes[0].entrees.map((e) => e.titre)).toEqual([
      'Première',
      'Deuxième',
      'Troisième',
    ])
  })

  it('déduit la menace retirée du total au lieu de l’ajouter', () => {
    const bilan = bilanDeLaPhase(
      commeDansLHistorique(
        entree({ phase: 'Main Scheme Place Threat', type: 'threat', valeur: 3, restant: 3 }),
        entree({ phase: 'Main Scheme Place Threat', type: 'threat', valeur: -1, restant: 2 })
      ),
      2
    )
    expect(bilan?.etapes[0].menace).toBe(2)
  })

  it('compte les dégâts en positif, quel que soit le signe de la variation de PV', () => {
    const bilan = bilanDeLaPhase(
      commeDansLHistorique(
        entree({ phase: 'Enemy Activation', type: 'damage', valeur: -3 }),
        entree({ phase: 'Enemy Activation', type: 'damage', valeur: -2 })
      ),
      2
    )
    expect(bilan?.etapes[0].degats).toBe(5)
  })

  it('ignore les autres rounds et les autres phases', () => {
    const bilan = bilanDeLaPhase(
      commeDansLHistorique(
        entree({ round: 1, phase: 'Enemy Activation', type: 'damage', valeur: -9 }),
        entree({ phase: 'Player Turn', titre: 'Carte jouée' }),
        entree({ phase: 'Enemy Activation', type: 'damage', valeur: -1 })
      ),
      2
    )
    expect(bilan?.etapes).toHaveLength(1)
    expect(bilan?.etapes[0].degats).toBe(1)
  })

  it('ne rend rien quand la phase n’a produit aucun fait', () => {
    expect(bilanDeLaPhase([], 2)).toBeUndefined()
    expect(bilanDeLaPhase(commeDansLHistorique(entree({ phase: 'Player Turn' })), 2)).toBeUndefined()
  })
})
