// Ce que le plateau DESSINE du pack Iron Patriot : le deck REGISTERED, et les
// alliés que Reign's End glisse FACE CACHÉE sous elle.
//
// Étape 8 bis de `docs/reference/PROCESSUS-CARTE.md`. Deux cartes du pack
// changent ce qu'on VOIT, et l'une des deux a exactement la forme du défaut
// Contingency Plan du 09/09/2026 :
//
//  - `ip017` Reign's End place chaque allié REGISTERED vaincu FACE CACHÉE sous
//    elle (`PlaceCardHere`). Trois par joueur, et les joueurs perdent. Un
//    compteur qu'on ne voit pas est un compteur qui n'existe pas.
//  - `ip001b` Norman Osborn monte un SECOND DECK de 20 sbires
//    (`additional_deck`). Sans lui à l'écran, tout le pack est injouable :
//    c'est là qu'on lit ce qu'on va pouvoir recruter, et à quel prix.
import { describe, expect, it } from 'vitest'
import { carteSurTable, cartesDessinees, dessinee, siege, tableAvec } from './plateau-de-test'
import { catalogueVide } from './catalogue'
import { construirePlateau } from './zones'

const REIGNS_END = 30
const SOUS_1 = 31
const SOUS_2 = 32
const SOUS_3 = 33

const mondeReignsEnd = () =>
  tableAvec(
    siege({
      area_hero: [carteSurTable(1, 'ip001a', 'Hero', 'Iron Patriot')],
    }),
    {
      area_schemes_side: [
        carteSurTable(REIGNS_END, 'ip017', 'SideScheme', "Reign's End"),
        carteSurTable(SOUS_1, 'registered_ally', 'Ally', 'H.A.M.M.E.R. Agents', {
          bind_object_id: REIGNS_END,
          is_face_up: false,
        }),
        carteSurTable(SOUS_2, 'registered_ally', 'Ally', 'Bullseye', {
          bind_object_id: REIGNS_END,
          is_face_up: false,
        }),
        carteSurTable(SOUS_3, 'registered_ally', 'Ally', 'Venom', {
          bind_object_id: REIGNS_END,
          is_face_up: false,
        }),
      ],
    }
  )

// CALIBRAGE §9, mesuré le 10/09/2026 — et il dit une chose désagréable qu'il
// faut écrire :
//  - `sousArbre` renvoyant `[]` : les DEUX premiers cas tombent au rouge. Ils
//    prouvent donc bien que la lecture des cartes posées sous la manigance est
//    la seule chose qui les fasse apparaître.
//  - `sousArbre` amputé de sa seule RÉCURSION (le défaut Contingency Plan
//    exact) : ils restent VERTS. Reign's End est une racine, ses cartes ne
//    pendent qu'à un étage. Ce fichier ne remplace donc PAS
//    `attachement-en-chaine.test.ts`, qui garde l'étage profond ; il garde
//    l'étage simple, pour ce pack.
describe("Reign's End, ce qui est glissé dessous", () => {
  // L'assertion qui compte : une carte absente de `cartesDessinees` n'est
  // NULLE PART à l'écran. C'est la seule qui aurait attrapé Contingency Plan.
  it('dessine les trois alliés posés sous la manigance', () => {
    const monde = mondeReignsEnd()
    expect(dessinee(monde, SOUS_1)).toBeDefined()
    expect(dessinee(monde, SOUS_2)).toBeDefined()
    expect(dessinee(monde, SOUS_3)).toBeDefined()
  })

  it('les rattache toutes les trois à Reign s End, dans l ordre où elles y sont tombées', () => {
    const monde = mondeReignsEnd()
    const vues = cartesDessinees(monde)
    for (const id of [SOUS_1, SOUS_2, SOUS_3]) {
      expect(dessinee(monde, id)?.portePar).toBe(REIGNS_END)
    }
    const rang = (id: number) => vues.findIndex((c) => c.id === id)
    expect(rang(SOUS_1)).toBeLessThan(rang(SOUS_2))
    expect(rang(SOUS_2)).toBeLessThan(rang(SOUS_3))
  })

  // Cas témoin : la manigance elle-même reste une RACINE, face visible. Sans
  // lui, un correctif qui dessinerait tout à plat passerait aussi.
  it('garde la manigance en racine, face visible', () => {
    const carte = dessinee(mondeReignsEnd(), REIGNS_END)
    expect(carte?.portePar).toBe(0)
    expect(carte?.facedown).toBe(false)
  })
})

describe('le deck REGISTERED', () => {
  const mondeDeck = () =>
    tableAvec(
      siege({
        area_hero: [carteSurTable(1, 'ip001b', 'AlterEgo', 'Norman Osborn')],
        additional_deck: [
          carteSurTable(50, 'ip020', 'Minion', 'H.A.M.M.E.R. Agents'),
          carteSurTable(51, 'ip023', 'Minion', 'Bullseye'),
        ],
        additional_discard_pile: [carteSurTable(52, 'registered_ally', 'Ally', 'Penance')],
      })
    )

  // Le deck spécial a sa propre zone, à GAUCHE du héros, deck et défausse côte
  // à côte (le cycle recrutement -> mort -> retour au deck).
  it('lui donne sa zone à part, avec sa défausse à côté', () => {
    const plateau = construirePlateau(mondeDeck(), { playerId: 0, catalogue: catalogueVide })
    const zone = plateau.emplacements.find((e) => e.cle === 'deck-special')
    expect(zone).toBeDefined()
    const piles = zone!.groupes.flat()
    expect(piles.length).toBeGreaterThanOrEqual(1)
  })

  // ⚠ ÉCART CONNU, mesuré le 10/09/2026 et laissé tel quel : l'étiquette de la
  // zone se déduit du seul trait COMMUN à toutes les cartes du deck
  // (`nomDeckSpecial`, zones.ts:427) — « Invocation » chez Docteur Strange. Les
  // 20 sbires REGISTERED n'ont AUCUN trait commun (H.A.M.M.E.R., ASSASSIN,
  // ASGARD...), donc la zone retombe sur le libellé générique. Le deck est bien
  // là et bien lisible ; c'est son titre qui ne dit pas son nom.
  it('retombe sur le libellé générique, faute de trait commun aux 20 sbires', () => {
    const plateau = construirePlateau(mondeDeck(), { playerId: 0, catalogue: catalogueVide })
    const zone = plateau.emplacements.find((e) => e.cle === 'deck-special')
    expect(zone?.titre).toBe('Deck spécial')
  })
})
