// Shadowland, scénario 3 « Heart of Shadow » (sl057-sl071) : ce que le plateau DESSINE.
//
// `Fusion/marvel-lcg-src/tools/cas/shadowland_c.py` prouve ce que le moteur FAIT ; ce fichier prouve ce que le joueur REGARDE
// (PROCESSUS-CARTE.md, étape 8 bis). On pose à la main l'état d'arrivée que le moteur publie, et on affirme sur `dessinee(...)`.
//
// Cartes concernées (elles changent ce qu'on VOIT) :
//   sl062 Dark Shroud, sl063 Fear Projection : attachements portés par le VILAIN Krahllak ;
//   sl064 Mark of the Wicked, sl065 Pull of Power : attachements portés par l'IDENTITÉ du joueur ;
//   sl072a/b Creeping Corruption (posée par sl060a, jetons posés par sl057-sl071) : amélioration à jetons `corruption` ;
//   sl069 Snakeroot Elders : jetons `corruption` posés sur le SBIRE.
// Cartes SANS cas : sl057-sl059 (ses attaques, déjà couvertes par la jauge), sl060b-sl061b (menace), sl066-sl068, sl070, sl071.
import { describe, expect, it } from 'vitest'
import { nomDeCompteur } from './compteurs-fr'
import { carteSurTable as carte, dessinee, siege, tableAvec } from './plateau-de-test'

const IDENTITE = 1
const CORRUPTION = 2
const KRAHLLAK = 10
const SHROUD = 11
const PROJECTION = 12
const MARK = 13
const PULL = 14
const ELDERS = 20

const heros = () => carte(IDENTITE, '01001a', 'Hero', 'Spider-Man')
const cc = (n: number) => carte(CORRUPTION, 'sl072a', 'Upgrade', 'Creeping Corruption', { bind_object_id: IDENTITE, info: { c_corruption: n } })
const krahllak = () => carte(KRAHLLAK, 'sl057', 'Villain', '* Krahllak')

describe('sl062 / sl063 : les attachements de Krahllak sont dessinés, portés par le vilain', () => {
  const monde = () =>
    tableAvec(siege({ area_hero: [heros(), cc(0)] }), {
      area_villain: [
        krahllak(),
        carte(SHROUD, 'sl062', 'Attachment', 'Dark Shroud', { bind_object_id: KRAHLLAK }),
        carte(PROJECTION, 'sl063', 'Attachment', 'Fear Projection', { bind_object_id: KRAHLLAK }),
      ],
    })

  it('Dark Shroud est à l écran, portée par Krahllak (assertion qui aurait attrapé Contingency Plan)', () => {
    expect(dessinee(monde(), SHROUD)).toBeDefined()
    expect(dessinee(monde(), SHROUD)?.portePar).toBe(KRAHLLAK)
  })

  it('Fear Projection aussi : les DEUX attachements sont dessinés', () => {
    expect(dessinee(monde(), PROJECTION)?.portePar).toBe(KRAHLLAK)
  })
})

describe('sl064 / sl065 : les attachements de l identité sont dessinés, portés par le héros', () => {
  it('Mark of the Wicked et Pull of Power sont à l écran, portées par l identité', () => {
    const m = tableAvec(
      siege({
        area_hero: [
          heros(),
          cc(1),
          carte(MARK, 'sl064', 'Attachment', 'Mark of the Wicked', { bind_object_id: IDENTITE }),
          carte(PULL, 'sl065', 'Attachment', 'Pull of Power', { bind_object_id: IDENTITE }),
        ],
      })
    )
    expect(dessinee(m, MARK)).toBeDefined()
    expect(dessinee(m, MARK)?.portePar).toBe(IDENTITE)
    expect(dessinee(m, PULL)?.portePar).toBe(IDENTITE)
  })
})

describe('Creeping Corruption, sl069 : les jetons corruption sont dessinés', () => {
  it('la Creeping Corruption est une amélioration attachée à l identité, POSÉE À CÔTÉ d elle (jamais à moitié cachée), avec ses jetons', () => {
    for (const n of [0, 1, 4]) {
      const m = tableAvec(siege({ area_hero: [heros(), cc(n)] }))
      expect(dessinee(m, CORRUPTION)?.kind).toBe('upgrade')
      // 23/10/2026 : elle sort de la cascade (CARTES_A_COTE) ; `portePar: 0` = posee seule, comme une carte de la rangee
      expect(dessinee(m, CORRUPTION)?.portePar).toBe(0)
      expect(dessinee(m, CORRUPTION)?.compteurs.corruption ?? 0).toBe(n)
    }
  })

  it('Snakeroot Elders porte son jeton corruption (« here »), sur le sbire engagé', () => {
    const m = tableAvec(
      siege({
        area_hero: [heros(), cc(0)],
        engaged_enemies: [carte(ELDERS, 'sl069', 'Minion', '* Snakeroot Elders', { info: { c_corruption: 1 } })],
      })
    )
    expect(dessinee(m, ELDERS)).toBeDefined()
    expect(dessinee(m, ELDERS)?.compteurs.corruption).toBe(1)
  })

  it('le nom du compteur reste lisible (corruption : meme mot en français, repli anglais sinon)', () => {
    expect(nomDeCompteur('corruption')).toBe('corruption')
  })
})
