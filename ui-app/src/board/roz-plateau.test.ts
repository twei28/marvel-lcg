// Roz (jakxin, `rz001a`-`rz020`) : ce que le plateau DESSINE une fois les cartes résolues.
//
// `Fusion/marvel-lcg-src/tools/cas/roz.py` prouve ce que le moteur FAIT ; ce fichier prouve ce que le joueur REGARDE
// (PROCESSUS-CARTE.md, étape 8 bis). Les cartes du pack qui changent ce qu'on VOIT :
//   - rz007 Agent of Wakanda : amélioration posée sur Roz, avec ses compteurs `agent` (jusqu'à 6) ;
//   - rz008 A.T.M.C.P. : soutien (zone des soutiens) ;
//   - rz002 / rz003 : deux alliés Thor (zone des alliés) ;
//   - rz017 Dario Agger : sbire némésis engagé, portant rz019 Minotaur et rz020 Lawyers (attachements sur un SBIRE) ;
//   - rz018 Legal Council : manigance annexe (carte paysage) posée sur la table de rencontre.
// Aucun correctif de plateau : le rendu générique suffit, ces cas sont verts d'emblée. Le compteur `agent` a son
// libellé français dans `compteurs-fr.ts`.
import { describe, expect, it } from 'vitest'
import { carteSurTable as carte, dessinee, siege, tableAvec } from './plateau-de-test'

const IDENTITE = 1
const AGENT = 2
const JUMPSUIT = 3
const SOUTIEN = 4
const JANE = 5
const ODINSON = 6
const DARIO = 80
const MINOTAUR = 81
const AVOCATS = 82
const CONSEIL = 83

const heros = () => carte(IDENTITE, 'rz001a', 'Hero', 'Roz')

describe('rz007 Agent of Wakanda : posé sur Roz avec ses compteurs agent', () => {
  it('est dessiné derrière Roz, avec ses 4 compteurs agent', () => {
    const monde = tableAvec(
      siege({
        area_hero: [
          heros(),
          carte(AGENT, 'rz007', 'Upgrade', 'Agent of Wakanda', { bind_object_id: IDENTITE, info: { c_agent: 4 } }),
          carte(JUMPSUIT, 'rz005', 'Upgrade', 'Wakandan Jumpsuit', { bind_object_id: IDENTITE }),
        ],
      })
    )
    expect(dessinee(monde, AGENT)).toBeDefined()
    expect(dessinee(monde, AGENT)?.portePar).toBe(IDENTITE)
    expect(dessinee(monde, AGENT)?.compteurs.agent).toBe(4)
    expect(dessinee(monde, JUMPSUIT)?.portePar).toBe(IDENTITE)
  })

  it('les 6 compteurs sont tous dessinés, puis plus aucun une fois dépensés', () => {
    const six = tableAvec(
      siege({ area_hero: [heros(), carte(AGENT, 'rz007', 'Upgrade', 'Agent of Wakanda', { bind_object_id: IDENTITE, info: { c_agent: 6 } })] })
    )
    expect(dessinee(six, AGENT)?.compteurs.agent).toBe(6)
    const zero = tableAvec(
      siege({ area_hero: [heros(), carte(AGENT, 'rz007', 'Upgrade', 'Agent of Wakanda', { bind_object_id: IDENTITE })] })
    )
    expect(dessinee(zero, AGENT)?.compteurs.agent).toBeUndefined()
  })
})

describe('rz008 A.T.M.C.P. et les deux Thor', () => {
  it('le soutien et les deux alliés sont dessinés', () => {
    const monde = tableAvec(
      siege({
        area_hero: [heros()],
        supports: [carte(SOUTIEN, 'rz008', 'Support', 'A.T.M.C.P.')],
        allies: [carte(JANE, 'rz002', 'Ally', 'Thor'), carte(ODINSON, 'rz003', 'Ally', 'Thor')],
      })
    )
    expect(dessinee(monde, SOUTIEN)).toBeDefined()
    expect(dessinee(monde, JANE)).toBeDefined()
    expect(dessinee(monde, ODINSON)).toBeDefined()
    expect(dessinee(monde, SOUTIEN)?.kind).not.toBe(dessinee(monde, JANE)?.kind)
  })
})

describe('rz017 Dario Agger porte Minotaur et Lawyers', () => {
  const monde = () =>
    tableAvec(
      siege({
        area_hero: [heros()],
        engaged_enemies: [
          carte(DARIO, 'rz017', 'Minion', 'Dario Agger'),
          carte(MINOTAUR, 'rz019', 'Attachment', 'Minotaur', { bind_object_id: DARIO }),
          carte(AVOCATS, 'rz020', 'Attachment', 'Lawyers', { bind_object_id: DARIO }),
        ],
      })
    )

  it('Dario Agger est dessiné, ses deux attachements derrière lui', () => {
    const vues = [DARIO, MINOTAUR, AVOCATS].map((id) => dessinee(monde(), id))
    expect(vues.every((v) => v !== undefined)).toBe(true)
    expect(dessinee(monde(), MINOTAUR)?.portePar).toBe(DARIO)
    expect(dessinee(monde(), AVOCATS)?.portePar).toBe(DARIO)
  })
})

describe('rz018 Legal Council : manigance annexe paysage', () => {
  it('est dessinée avec sa menace (2 par joueur) sur la table de rencontre', () => {
    const monde = tableAvec(siege({ area_hero: [heros()] }), {
      area_villain: [carte(CONSEIL, 'rz018', 'EncounterSideScheme', 'Legal Council', { info: { threat: 2 } })],
    })
    expect(dessinee(monde, CONSEIL)).toBeDefined()
    expect(dessinee(monde, CONSEIL)?.codeCarte).toBe('rz018')
  })
})
