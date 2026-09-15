// La carte qu'on JOUE ne se pose plus chez le mechant.
//
// Defaut signale en jeu le 15/09/2026 : « pourquoi les cartes que je joue, on
// dirait qu'elles se placent derriere le mechant, avant d'aller a la defausse ».
//
// La cause tenait aux DEUX bouts de la chaine :
//
//  - le moteur sait a qui appartient la carte en cours de resolution
//    (`Faces.MoveAllToProcessingArea` la range dans `player.area_processing`),
//    mais il FUSIONNAIT tout dans une seule liste au moment de publier la trame
//    (`to_descriptor.py`, `world_descriptor.area_processing`) ;
//  - le plateau dessinait cette liste unique dans l'emplacement « Mechant »
//    (`zones.ts`), faute de savoir a qui elle etait.
//
// Le moteur publie desormais la zone de resolution DE CHAQUE JOUEUR a cote de
// ses autres zones, et le plateau la dessine aupres de son heros. Ce qui reste
// dans la liste du monde (ce que le scenario resout) ne bouge pas d'un pixel.

import { describe, expect, it } from 'vitest'
import { carteSurTable, cartesDessinees, dessinee, siege, tableAvec } from './plateau-de-test'

/** Un evenement joue par le heros, le temps de sa resolution. */
const EVENEMENT = 50
/** Une traitrise que le scenario resout, elle, cote mechant. */
const TRAITRISE = 60

describe('la carte en cours de resolution', () => {
  it("se dessine aupres de son heros, pas chez le mechant", () => {
    const evenement = carteSurTable(EVENEMENT, '01064', 'Event', 'Swinging Web Kick')
    const table = tableAvec(siege({ area_processing: [evenement] }))

    const vue = dessinee(table, EVENEMENT)

    expect(vue, 'la carte jouee doit etre dessinee quelque part').toBeDefined()
    expect(vue?.zone).toBe('terrain-soutien')
  })

  it('laisse chez le mechant ce que le scenario resout', () => {
    const traitrise = carteSurTable(TRAITRISE, '01084', 'Treachery', 'Shocker')
    const table = tableAvec(siege(), { area_processing: [traitrise] })

    expect(dessinee(table, TRAITRISE)?.zone).toBe('rencontre')
  })

  it('ne la dessine pas DEUX fois quand le moteur la publie aux deux endroits', () => {
    // ⚠ Le moteur garde sa liste fusionnee au niveau du monde, pour ne pas
    // casser l'ancien client qui la lit. La meme carte arrive donc par les deux
    // canaux, et le plateau ne doit la poser qu'une fois.
    const evenement = carteSurTable(EVENEMENT, '01064', 'Event', 'Swinging Web Kick')
    const table = tableAvec(siege({ area_processing: [evenement] }), {
      area_processing: [evenement],
    })

    const vues = cartesDessinees(table).filter((c) => c.id === EVENEMENT)

    expect(vues).toHaveLength(1)
    expect(vues[0]?.zone).toBe('terrain-soutien')
  })
})
