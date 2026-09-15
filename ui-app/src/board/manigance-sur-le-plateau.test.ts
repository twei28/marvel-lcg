// L'ÉTAPE 8 BIS DE LA QUESTION `Reveal_Main_Scheme` : CE QUE LE PLATEAU DESSINE.
//
// `manigance-face-a.test.ts` prouve la règle PURE (quelle question reconnaître,
// quand lever le voile). Il ne regarde jamais ce que `zones.ts` pose réellement
// sur la table à cet instant précis. Superior Spider-Man a montré ce que ça
// coûte de sauter cette étape (voir l'en-tête de `plateau-de-test.ts`) : un
// moteur vert 32 fois sur 32, et une carte invisible à l'écran.
//
// Le risque ici est symétrique de celui de Contingency Plan. Là-bas, une carte
// bien réelle disparaissait de l'affichage. Ici, c'est la face qui pourrait se
// tromper : le moteur s'arrête AVANT de retourner la manigance principale
// (`World.ConfirmMainSchemeReveal`) et pose la question `Reveal_Main_Scheme`
// pendant que `area_schemes_main` porte encore la face A. Si un jour le
// plateau montrait déjà `01097b` à ce moment-là, ou si le voile d'ouverture
// masquait encore le vilain et le héros derrière le panneau, ce test doit
// rougir.
//
// ⚠ Les assertions portent sur `cartesDessinees`/`dessinee`, ce que le
// harnais dit RÉELLEMENT dessiné (via `construirePlateau` puis `toScanCard`),
// jamais sur les cartes qu'on a soi-même posées dans le monde de test.

import { describe, expect, it } from 'vitest'
import { carteSurTable, cartesDessinees, dessinee, siege, tableAvec } from './plateau-de-test'
import { NOM_OPTION_MANIGANCE, questionDeLaManigance } from './manigance-face-a'
import type { Demande, Option } from './ask'

const ID_VILAIN = 1
const ID_HEROS = 2
const ID_MANIGANCE = 3

const FACE_A = '01097a'
const FACE_B = '01097b'

function optionUnique(nom: string): Option {
  return {
    id: 7,
    name: nom,
    bind_id: ID_MANIGANCE,
    bind_player_id: 0,
    all_legal_targets: [],
    target_num_range: [0, 0],
    target_payment: {},
    select_rule: '',
    target_must_include_traits: [],
    failure_reason: '',
    is_search: false,
  }
}

/** La question du moteur, telle qu'elle voyage pendant l'arrêt sur la face A. */
const QUESTION_FACE_A: Demande = {
  options: [optionUnique(NOM_OPTION_MANIGANCE)],
  refus: [],
  prompt_text: '',
  event_name: '',
  show_cancel: false,
  ability_type: '',
}

/**
 * La table telle qu'elle doit être montée au moment où le moteur pose la
 * question : le vilain et le héros déjà en place, la manigance principale
 * encore sur `faceManigance`.
 */
function tableAuMomentDeLaQuestion(faceManigance: string) {
  const vilain = carteSurTable(ID_VILAIN, '01097', 'EncounterVillain', 'Rhino')
  const heros = carteSurTable(ID_HEROS, '01001', 'Hero', 'Spider-Man')
  const manigance = carteSurTable(ID_MANIGANCE, faceManigance, 'MainScheme', 'Rhino Charges In')
  return tableAvec(siege({ area_hero: [heros] }), {
    area_villain: [vilain],
    area_schemes_main: [manigance],
    round_id: 0,
    confirm_main_scheme: true,
  })
}

describe('la manigance principale, au moment de la question Reveal_Main_Scheme', () => {
  it("vérifie d'abord que la question posée est bien celle-là, et personne d'autre", () => {
    // Si cette assertion tombe, les suivantes ne prouvent plus rien : le
    // scénario ne serait plus celui de l'arrêt sur la face A.
    expect(questionDeLaManigance(QUESTION_FACE_A)?.name).toBe(NOM_OPTION_MANIGANCE)
  })

  it('dessine la face A dans la zone de la manigance principale, pas la face B', () => {
    const table = tableAuMomentDeLaQuestion(FACE_A)

    const vue = dessinee(table, ID_MANIGANCE)

    expect(vue, 'la manigance doit être dessinée quelque part').toBeDefined()
    expect(vue?.zone).toBe('complot-principal')
    expect(vue?.codeCarte).toBe(FACE_A)
    expect(vue?.codeCarte).not.toBe(FACE_B)
  })

  it('monte déjà le vilain et le héros derrière : la table est prête, seul le panneau est par-dessus', () => {
    const table = tableAuMomentDeLaQuestion(FACE_A)

    const vilain = dessinee(table, ID_VILAIN)
    const heros = dessinee(table, ID_HEROS)

    expect(vilain, 'le vilain doit être dessiné').toBeDefined()
    expect(vilain?.zone).toBe('rencontre')
    expect(heros, 'le héros doit être dessiné').toBeDefined()
    expect(heros?.zone).toBe('terrain-soutien')

    // Les trois pièces de la table sont dessinées ensemble : ce n'est pas la
    // manigance qui apparaît seule pendant que le reste attend.
    const ids = cartesDessinees(table).map((c) => c.id)
    expect(ids).toEqual(expect.arrayContaining([ID_VILAIN, ID_HEROS, ID_MANIGANCE]))
  })
})
