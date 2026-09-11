// Filet pose le 11/09/2026 avant de traduire les noms de cartes a l'affichage.
//
// `airesVilains()` range le deck vilain par NOM : les phases a venir se posent
// derriere le vilain actif qui porte le meme nom, et les vilains d'un AUTRE nom
// partent dans la pile « en attente ». Ces deux tris comparaient un nom
// d'affichage (`UniteAffichee.carte.name`, issu de toScanCard) avec un nom du
// moteur (`WorldCard.name`). Tant que rien n'etait traduit, les deux chaines
// etaient identiques et le tri marchait par coincidence.
//
// Traduire le nom d'affichage rompt cette coincidence en silence : les phases
// ne se rattachent plus a personne et tous les vilains tombent « en attente ».
// Aucun test ne l'aurait vu. Celui-ci le voit.
//
// On l'ecrit avec un vilain dont la VF DIFFERE de la VO, sinon le test reste
// vert quoi qu'on casse : Green Goblin devient « Le Bouffon Vert ».

import { beforeEach, afterEach, describe, expect, it } from 'vitest'
import { carteSurTable, siege, tableAvec } from './plateau-de-test'
import { CLE_SCANS_FR } from './scans-fr'
import { NOMS_FR } from './noms-fr'
import { construirePlateau } from './zones'
import { catalogueVide } from './catalogue'

// Rhino porte le meme nom dans les deux langues, donc inutilisable ici : il
// faut un vilain dont la traduction DIFFERE, sinon le test reste vert meme
// casse. 02014 = Green Goblin -> « Le Bouffon Vert ».
const CODE_VILAIN = '02014'
const NOM_MOTEUR = '* Green Goblin'

beforeEach(() => window.localStorage.removeItem(CLE_SCANS_FR))
afterEach(() => window.localStorage.removeItem(CLE_SCANS_FR))

/** Un vilain actif, et une phase suivante du meme vilain dans le deck. */
function tableVilainADeuxPhases() {
  const actif = carteSurTable(1, CODE_VILAIN, 'EncounterVillain', NOM_MOTEUR)
  const phaseII = carteSurTable(2, CODE_VILAIN, 'EncounterVillain', NOM_MOTEUR)
  return tableAvec(siege(), { area_villain: [actif], villain_deck: [phaseII] })
}

describe('airesVilains, quand le nom affiche est traduit', () => {
  it('verifie d\'abord que le vilain choisi a bien une VF differente', () => {
    // Si cette assertion tombe, les deux suivantes ne prouvent plus rien.
    expect(NOMS_FR[CODE_VILAIN]).toBeDefined()
    expect(NOMS_FR[CODE_VILAIN]).not.toBe(NOM_MOTEUR)
  })

  it('pose la phase suivante DERRIERE le vilain actif, pas dans « en attente »', () => {
    const plateau = construirePlateau(tableVilainADeuxPhases(), {
      playerId: 0,
      catalogue: catalogueVide,
    })
    const vilains = plateau.emplacements.find((e) => e.cle === 'rencontre')
    const unites = vilains?.groupes.flat() ?? []
    const actif = unites.find((u) => u.carte.id === '1')
    expect(actif, 'le vilain actif doit etre dessine').toBeDefined()
    expect(actif?.stagesArriere).toHaveLength(1)
    expect(actif?.stagesArriere?.[0]?.id).toBe('2')
  })

  it('ne range pas le meme vilain dans la pile « en attente »', () => {
    const plateau = construirePlateau(tableVilainADeuxPhases(), {
      playerId: 0,
      catalogue: catalogueVide,
    })
    const unites = plateau.emplacements.find((e) => e.cle === 'rencontre')?.groupes.flat() ?? []
    // Une seule unite : le vilain actif. Pas de seconde unite « en attente ».
    expect(unites).toHaveLength(1)
  })
})
