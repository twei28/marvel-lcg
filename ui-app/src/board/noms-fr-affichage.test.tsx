// Suite du defaut du 11/09/2026 : apres le plateau lui-meme (card-model), les
// endroits qui ecrivent un nom de carte SANS passer par toScanCard. Ils lisent
// une `WorldCard`, dont le `name` reste anglais par construction (le moteur et
// le plateau comparent dessus), et affichaient donc l'anglais a cote d'une
// carte francaise.
//
// La carte de reference est 01097a, « The Break-In! » -> « L'Effraction ! » :
// prendre une carte dont la VF egale la VO laisserait l'assertion verte meme
// non branchee.
//
// NOTE sur ce qui n'est PAS teste ici : le titre du menu et ses aria-labels
// lisent `carte: ScanCardProps`, deja traduit en amont par toScanCard
// (card-model-nom-fr.test.ts). Y rappeler la traduction ne ferait rien.

import { afterEach, beforeEach, describe, expect, it } from 'vitest'
import { CLE_SCANS_FR } from './scans-fr'
import { carteSurTable } from './plateau-de-test'
import { nomAffiche } from './noms-cartes-fr'
import type { WorldCard } from './world'

const CODE = '01097a'
const NOM_VO = 'The Break-In!'
const NOM_VF = "L'Effraction !"

beforeEach(() => window.localStorage.removeItem(CLE_SCANS_FR))
afterEach(() => window.localStorage.removeItem(CLE_SCANS_FR))

const manigance = (id = 1): WorldCard => carteSurTable(id, CODE, 'MainScheme', NOM_VO)

describe('le nom qu\'un ecran tire d\'une WorldCard', () => {
  it('part bien de l\'anglais dans le monde du moteur', () => {
    // Le garde-fou du test : si le moteur se mettait a livrer du francais,
    // les assertions suivantes ne prouveraient plus rien.
    expect(manigance().name).toBe(NOM_VO)
  })

  it('devient francais une fois passe par nomAffiche', () => {
    expect(nomAffiche(manigance())).toBe(NOM_VF)
  })
})

// Les ecrans reellement branches, verifies par lecture du module : chacun
// appelle nomAffiche sur ses WorldCard. Le test lit la source plutot que de
// monter sept composants React, chacun avec son propre echafaudage (le menu
// d'actions demande a lui seul un bouchon de ResizeObserver). Ce qu'on
// verrouille ici, c'est qu'aucun de ces points ne RETOMBE en anglais lors
// d'une modification ulterieure.
import { readFileSync } from 'node:fs'

// board.tsx vit a la racine de src/, d'ou son chemin d'import different.
const SOURCES: Array<[string, string, string[]]> = [
  ['src/board/MenuActionsCarte.tsx', './noms-cartes-fr', ['nomAffiche(carte)', 'nomAffiche(source)']],
  ['src/board/DemandeCentrale.tsx', './noms-cartes-fr', ['nomAffiche(']],
  ['src/board/AssistantAction.tsx', './noms-cartes-fr', ['nomAffiche(']],
  ['src/board/HistoriquePartie.tsx', './noms-cartes-fr', ['nomAffiche(']],
  ['src/board/CoucheRevelation.tsx', './noms-cartes-fr', ['nomAffiche(']],
  ['src/board/RecapPhaseMechant.tsx', './noms-cartes-fr', ['nomAffiche(']],
  ['src/board/card-model.ts', './noms-cartes-fr', ['nomAffiche(card)']],
  ['src/board.tsx', './board/noms-cartes-fr', ['nomAffiche(']],
]

describe('les ecrans qui nomment une carte appellent bien le traducteur', () => {
  for (const [fichier, chemin, attendus] of SOURCES) {
    it(`${fichier} passe ses WorldCard par nomAffiche`, () => {
      const source = readFileSync(fichier, 'utf-8')
      expect(source).toContain(`from '${chemin}'`)
      for (const attendu of attendus) expect(source).toContain(attendu)
    })
  }
})
