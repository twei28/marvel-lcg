// Ce que ces cas protègent : le bilan doit RÉSUMER la phase du méchant, pas la
// dérouler, et ranger chaque fait sous l'étape qui l'a produit.
//
// Les trois se sont déjà trompés autrement. Le panneau d'origine groupait par
// nature (dégâts / menace / révélé), ce qui mélangeait la menace posée à
// l'étape 1 et celle d'une manigance jouée à l'étape 4. Sa refonte a laissé
// entrer la narration du moteur : poser une menace affichait six lignes dont
// une seule disait quelque chose. Et un total en valeur absolue compterait une
// menace RETIRÉE comme une menace posée — un bilan faux dans le sens qui
// exagère le danger.
import { describe, expect, it } from 'vitest'
import { bilanDeLaPhase, type Noms } from './RecapPhaseMechant'
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

const noms: Noms = {
  carte: (id) => (id === undefined ? undefined : `Carte#${id}`),
  heros: (joueur) => (joueur === undefined ? undefined : `Héros${joueur}`),
}

describe('bilanDeLaPhase — découpage', () => {
  it('range chaque fait sous son étape, dans l’ordre de la carte de référence', () => {
    const bilan = bilanDeLaPhase(
      commeDansLHistorique(
        entree({ phase: 'Main Scheme Place Threat', type: 'threat', valeur: 1, restant: 1, plafond: 6, cibleId: 7 }),
        entree({ phase: 'Enemy Activation', type: 'damage', valeur: -3, acteur: 'Klaw', cibleId: 9 }),
        entree({ phase: 'Reveal Encounter Cards', nomCarte: 'Gang-Up' })
      ),
      2,
      noms
    )

    expect(bilan?.etapes.map((e) => e.numero)).toEqual([1, 2, 4])
  })

  it('ignore les autres rounds et les autres phases', () => {
    const bilan = bilanDeLaPhase(
      commeDansLHistorique(
        entree({ round: 1, phase: 'Enemy Activation', type: 'damage', valeur: -9 }),
        entree({ phase: 'Player Turn', titre: 'Carte jouée' }),
        entree({ phase: 'Enemy Activation', type: 'damage', valeur: -1 })
      ),
      2,
      noms
    )
    expect(bilan?.etapes).toHaveLength(1)
    expect(bilan?.etapes[0].degats).toBe(1)
  })

  it('ne rend rien quand la phase n’a produit aucun fait', () => {
    expect(bilanDeLaPhase([], 2, noms)).toBeUndefined()
    expect(bilanDeLaPhase(commeDansLHistorique(entree({ phase: 'Player Turn' })), 2, noms)).toBeUndefined()
  })
})

describe('bilanDeLaPhase — résumé', () => {
  it('écarte la narration du moteur des lignes, mais la garde sous le repli', () => {
    const bilan = bilanDeLaPhase(
      commeDansLHistorique(
        entree({ phase: 'Main Scheme Place Threat', type: 'text', titre: 'Main scheme phase start' }),
        entree({ phase: 'Main Scheme Place Threat', type: 'text', titre: 'would place 1 threat' }),
        entree({ phase: 'Main Scheme Place Threat', type: 'threat', valeur: 1, restant: 1, plafond: 6, cibleId: 7 }),
        entree({ phase: 'Main Scheme Place Threat', type: 'text', titre: 'placed 1 threat token' }),
        entree({ phase: 'Main Scheme Place Threat', type: 'text', titre: 'Main scheme phase end' })
      ),
      2,
      noms
    )

    const etape = bilan!.etapes[0]
    expect(etape.lignes).toHaveLength(1)
    expect(etape.lignes[0]).toMatchObject({ genre: 'menace', titre: 'Carte#7', chiffre: '+1 → 1/6' })
    expect(etape.brut).toHaveLength(5)
  })

  it('rattache les cartes de boost à l’attaque qui les a retournées', () => {
    const bilan = bilanDeLaPhase(
      commeDansLHistorique(
        entree({ phase: 'Enemy Activation', nomCarte: 'Sonic Boom', boost: true, cibleId: 21 }),
        entree({ phase: 'Enemy Activation', nomCarte: 'T’Challa’s Shadow', boost: true, cibleId: 22 }),
        entree({ phase: 'Enemy Activation', type: 'damage', valeur: -3, restant: 8, acteur: 'Klaw', cibleId: 9 })
      ),
      2,
      noms
    )

    const etape = bilan!.etapes[0]
    expect(etape.lignes).toHaveLength(1)
    expect(etape.lignes[0]).toMatchObject({
      genre: 'attaque',
      titre: 'Klaw attaque Carte#9',
      chiffre: '3 dégâts → 8 PV',
    })
    expect(etape.lignes[0].boosts?.map((b) => b.nom)).toEqual(['Sonic Boom', 'T’Challa’s Shadow'])
    // Un boost n'est pas une carte de plus : il appartient à l'activation.
    expect(etape.cartes).toBe(0)
  })

  it('distingue une manigance d’ennemi d’une attaque', () => {
    const bilan = bilanDeLaPhase(
      commeDansLHistorique(
        entree({ phase: 'Enemy Activation', type: 'threat', valeur: 2, restant: 3, plafond: 6, acteur: 'Klaw', cibleId: 7 })
      ),
      2,
      noms
    )
    expect(bilan!.etapes[0].lignes[0]).toMatchObject({
      genre: 'manigance',
      titre: 'Klaw manigance sur Carte#7',
      chiffre: '+2 → 3/6',
    })
  })

  it('attribue à une carte révélée ce qu’elle a produit ensuite', () => {
    const bilan = bilanDeLaPhase(
      commeDansLHistorique(
        entree({ nomCarte: 'Gang-Up', joueur: 0, cibleId: 31 }),
        entree({ type: 'damage', valeur: -2, restant: 6, cibleId: 9 })
      ),
      2,
      noms
    )
    const ligne = bilan!.etapes[0].lignes[0]
    expect(ligne).toMatchObject({ genre: 'carte', titre: 'Gang-Up', heros: 'Héros0' })
    expect(ligne.effets).toEqual(['Carte#9 : 2 dégâts → 6 PV'])
    // Une seule ligne : la conséquence est DANS la carte, pas à côté.
    expect(bilan!.etapes[0].lignes).toHaveLength(1)
  })

  it('garde la phrase du moteur quand l’auteur de l’attaque est inconnu', () => {
    const bilan = bilanDeLaPhase(
      commeDansLHistorique(
        entree({ phase: 'Enemy Activation', type: 'damage', titre: 'Black Panther subit 3 dégât(s)', valeur: -3, cibleId: 9 })
      ),
      2,
      noms
    )
    expect(bilan!.etapes[0].lignes[0].titre).toBe('Black Panther subit 3 dégât(s)')
  })

  it('déduit la menace retirée du total au lieu de l’ajouter', () => {
    const bilan = bilanDeLaPhase(
      commeDansLHistorique(
        entree({ phase: 'Main Scheme Place Threat', type: 'threat', valeur: 3, restant: 3 }),
        entree({ phase: 'Main Scheme Place Threat', type: 'threat', valeur: -1, restant: 2 })
      ),
      2,
      noms
    )
    expect(bilan!.etapes[0].menace).toBe(2)
  })

  it('compte les dégâts en positif, quel que soit le signe de la variation de PV', () => {
    const bilan = bilanDeLaPhase(
      commeDansLHistorique(
        entree({ phase: 'Enemy Activation', type: 'damage', valeur: -3 }),
        entree({ phase: 'Enemy Activation', type: 'damage', valeur: -2 })
      ),
      2,
      noms
    )
    expect(bilan!.etapes[0].degats).toBe(5)
  })
})
