// Fear No Evil, Daredevil (11/10/2026) : `60012` Focus the Senses, une fois
// vaincue, DEPLACE des ameliorations Sens d'un porteur a un autre. Radar Sense
// (60005, ennemi seulement) passe de Rhino a un sbire engage ; Superior Taste
// (60006, manigance seulement) passe d'une manigance annexe a une autre. On
// prouve que chaque amelioration est dessinee sous son NOUVEAU porteur.
//
// Etape 8 bis de PROCESSUS-CARTE : le correctif est cote moteur (60012.py),
// le rattachement par `bind_object_id` est generique ; ces cas sont des GARDES
// de l'etat d'arrivee, verts a la premiere execution.
import { describe, expect, it } from 'vitest'
import { carteSurTable, dessinee, siege, tableAvec } from './plateau-de-test'

const IDENTITE = 1
const RHINO = 40
const SBIRE = 41
const ANNEXE_1 = 50
const ANNEXE_2 = 51
const RADAR = 60
const GOUT = 61

const apresDeplacement = () =>
  tableAvec(
    siege({
      area_hero: [carteSurTable(IDENTITE, '60001a', 'Hero', 'Daredevil')],
      engaged_enemies: [
        carteSurTable(SBIRE, '01110', 'Minion', 'Hydra Soldier'),
        carteSurTable(RADAR, '60005', 'Upgrade', 'Radar Sense', { bind_object_id: SBIRE }),
      ],
    }),
    {
      area_villain: [carteSurTable(RHINO, '01094', 'Villain', 'Rhino')],
      area_schemes_side: [
        carteSurTable(ANNEXE_1, '01107', 'EncounterSideScheme', "Breakin' & Takin'"),
        carteSurTable(ANNEXE_2, '27133', 'EncounterSideScheme', 'Volunteer Work'),
        carteSurTable(GOUT, '60006', 'Upgrade', 'Superior Taste', { bind_object_id: ANNEXE_2 }),
      ],
    }
  )

describe('60012 Focus the Senses : ameliorations Sens deplacees', () => {
  it('dessine Radar Sense sous le sbire qui la porte desormais', () => {
    const carte = dessinee(apresDeplacement(), RADAR)
    expect(carte).toBeDefined()
    expect(carte?.portePar).toBe(SBIRE)
  })

  it('dessine Superior Taste sous la seconde manigance annexe', () => {
    const carte = dessinee(apresDeplacement(), GOUT)
    expect(carte).toBeDefined()
    expect(carte?.portePar).toBe(ANNEXE_2)
  })

  it('laisse Rhino et la premiere manigance sans amelioration', () => {
    const monde = apresDeplacement()
    expect(dessinee(monde, RHINO)?.portePar).toBe(0)
    expect(dessinee(monde, ANNEXE_1)?.portePar).toBe(0)
  })
})
