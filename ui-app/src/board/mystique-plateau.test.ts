// Mystique (my001a/b) : ce que la table DESSINE (étape 8 bis de PROCESSUS-CARTE).
//  - my003-my005 : les trois Formes Métamorphose sont des améliorations à DEUX faces posées sur l'identité : FACE CACHÉE (`b`, grisée) au Setup, FACE VISIBLE (`a`) quand on les retourne ;
//    chaque forme doit être dessinée, portée par l'identité, quelle que soit sa face (le plateau lit la face courante de la carte) ;
//  - my002 Shapeshifter (permanente) et my008 Shapeshifter Focus sont des améliorations attachées à l'identité ;
//  - my006 Destiny est un allié ; my007 Infiltration est une manigance annexe de JOUEUR (paysage) à l'écran, puis dans la pile de victoire ;
//  - my016 Mister Sinister (sbire némésis engagé), my017 Destiny's Warning (manigance annexe).
// Le dessin d'une amélioration attachée et d'une carte en pile de victoire est générique (`zones.ts`) : ce cas le vaut pour Mystique.
import { describe, expect, it } from 'vitest'
import { carteSurTable, dessinee, siege, tableAvec } from './plateau-de-test'

const MYSTIQUE = 1
const SHAPESHIFTER = 2
const CIVILIAN_CACHEE = 3
const ENEMY_VISIBLE = 4
const FRIEND_CACHEE = 5
const DESTINY = 6
const INFILTRATION = 7
const SINISTER = 8
const WARNING = 9

const monde = () =>
  tableAvec(
    siege({
      area_hero: [
        carteSurTable(MYSTIQUE, 'my001a', 'Hero', 'Mystique'),
        carteSurTable(SHAPESHIFTER, 'my002', 'Upgrade', 'Shapeshifter', { bind_object_id: MYSTIQUE }),
        carteSurTable(CIVILIAN_CACHEE, 'my003b', 'Upgrade', 'Civilian', { bind_object_id: MYSTIQUE }),
        carteSurTable(ENEMY_VISIBLE, 'my004a', 'Upgrade', 'Enemy', { bind_object_id: MYSTIQUE }),
        carteSurTable(FRIEND_CACHEE, 'my005b', 'Upgrade', 'Friend', { bind_object_id: MYSTIQUE }),
      ],
      allies: [carteSurTable(DESTINY, 'my006', 'Ally', 'Destiny')],
      engaged_enemies: [carteSurTable(SINISTER, 'my016', 'Minion', 'Mister Sinister')],
    }),
    { area_schemes_side: [carteSurTable(INFILTRATION, 'my007', 'PlayerSideScheme', 'Infiltration'), carteSurTable(WARNING, 'my017', 'SideScheme', "Destiny's Warning")] },
  )

describe('Mystique : ce que la table dessine', () => {
  it("dessine Mystique, Shapeshifter et les trois formes, chacune sur sa face courante, portées par l'identité", () => {
    for (const id of [MYSTIQUE, SHAPESHIFTER, CIVILIAN_CACHEE, ENEMY_VISIBLE, FRIEND_CACHEE]) expect(dessinee(monde(), id)).toBeDefined()
    expect(dessinee(monde(), CIVILIAN_CACHEE)?.portePar).toBe(MYSTIQUE)
    expect(dessinee(monde(), ENEMY_VISIBLE)?.portePar).toBe(MYSTIQUE)
    expect(dessinee(monde(), CIVILIAN_CACHEE)?.codeCarte).toBe('my003b')
    expect(dessinee(monde(), ENEMY_VISIBLE)?.codeCarte).toBe('my004a')
  })
  it('dessine Destiny (allié), Infiltration (manigance annexe de joueur), Mister Sinister et Destiny\'s Warning', () => {
    for (const id of [DESTINY, INFILTRATION, SINISTER, WARNING]) expect(dessinee(monde(), id)).toBeDefined()
  })
})
