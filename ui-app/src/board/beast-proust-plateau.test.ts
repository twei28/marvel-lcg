// Beast (Proust) (bs001a/b) : ce que la table DESSINE (étape 8 bis de PROCESSUS-CARTE).
//  - bs002 Beast's Lab est un SOUTIEN permanent ; Tech Support, Tech Genius et Réexploitation géniale y GLISSENT jusqu'à 3 améliorations,
//    que le joueur doit VOIR (il les rejoue comme en main) : portées par le Lab, juste derrière lui, lisibles par leur propriétaire ;
//  - bs015 Black Beast (sbire némésis engagé) porte la carte intercalée sous lui (son ATQ en dépend) et bs017 High-Tech Glasses est attachée à lui ;
//  - bs014 Technical Difficulties (complot annexe) est à l'écran.
// Le dessin des cartes glissées sous un soutien ET sous un ennemi est générique (`zones.ts`, voir attachement-en-chaine.test.ts) : ce cas le vaut pour Beast.
import { describe, expect, it } from 'vitest'
import { carteSurTable, cartesDessinees, dessinee, siege, tableAvec } from './plateau-de-test'

const BEAST = 1
const LAB = 2
const SOUS_LAB_A = 3
const SOUS_LAB_B = 4
const BLACK_BEAST = 5
const SOUS_BLACK_BEAST = 6
const LUNETTES = 7
const DIFFICULTES = 8

const monde = () =>
  tableAvec(
    siege({
      area_hero: [carteSurTable(BEAST, 'bs001a', 'Hero', 'Beast (Proust)')],
      supports: [
        carteSurTable(LAB, 'bs002', 'Support', "Beast's Lab"),
        carteSurTable(SOUS_LAB_A, 'bs006', 'Upgrade', "Bobby's Belt", { bind_object_id: LAB, is_face_up: false, visible_for_players: [0] }),
        carteSurTable(SOUS_LAB_B, 'bs008', 'Upgrade', "Xavier's Cerebro", { bind_object_id: LAB, is_face_up: false, visible_for_players: [0] }),
      ],
      engaged_enemies: [
        carteSurTable(BLACK_BEAST, 'bs015', 'Minion', 'Black Beast'),
        carteSurTable(SOUS_BLACK_BEAST, 'bs004', 'Upgrade', 'Hacked Power Gloves', { bind_object_id: BLACK_BEAST, is_face_up: false, visible_for_players: [0] }),
        carteSurTable(LUNETTES, 'bs017', 'Attachment', 'High-Tech Glasses', { bind_object_id: BLACK_BEAST }),
      ],
    }),
    { area_schemes_side: [carteSurTable(DIFFICULTES, 'bs014', 'SideScheme', 'Technical Difficulties')] },
  )

describe('Beast (Proust) : ce que la table dessine', () => {
  it('dessine Beast et son Laboratoire (soutien)', () => {
    expect(dessinee(monde(), BEAST)).toBeDefined()
    expect(dessinee(monde(), LAB)).toBeDefined()
  })
  it('dessine les améliorations glissées sous le Laboratoire, portées par lui, lisibles par leur propriétaire, juste derrière lui', () => {
    const vues = cartesDessinees(monde())
    const rang = (id: number) => vues.findIndex((c) => c.id === id)
    expect(dessinee(monde(), SOUS_LAB_A)).toBeDefined()
    expect(dessinee(monde(), SOUS_LAB_B)).toBeDefined()
    expect(dessinee(monde(), SOUS_LAB_A)?.portePar).toBe(LAB)
    expect(dessinee(monde(), SOUS_LAB_A)?.peeking).toBe(true)
    expect(rang(SOUS_LAB_A)).toBe(rang(LAB) + 1)
    expect(rang(SOUS_LAB_B)).toBe(rang(LAB) + 2)
  })
  it('dessine Black Beast, la carte intercalée sous lui et les lunettes attachées', () => {
    expect(dessinee(monde(), BLACK_BEAST)).toBeDefined()
    expect(dessinee(monde(), SOUS_BLACK_BEAST)).toBeDefined()
    expect(dessinee(monde(), SOUS_BLACK_BEAST)?.portePar).toBe(BLACK_BEAST)
    expect(dessinee(monde(), LUNETTES)).toBeDefined()
    expect(dessinee(monde(), LUNETTES)?.portePar).toBe(BLACK_BEAST)
  })
  it("dessine Technical Difficulties (complot annexe)", () => {
    expect(dessinee(monde(), DIFFICULTES)).toBeDefined()
  })
})
