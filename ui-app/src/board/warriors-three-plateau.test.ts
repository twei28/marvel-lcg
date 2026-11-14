// The Warriors Three (`wt001a`-`wt025`) : ce que le plateau DESSINE une fois le pack en jeu.
//
// `Fusion/marvel-lcg-src/tools/cas/warriors_three.py` prouve ce que le moteur FAIT ; ce fichier prouve ce que le joueur REGARDE
// (PROCESSUS-CARTE.md, étape 8 bis). Ce que le pack change à l'écran :
//   - wt002 « The Warriors Three » : amélioration-titre Permanent/Setup posée sur l'identité (le héros actif) ;
//   - wt003-wt005 : les trois héros inactifs, soutiens PERSONA mis en jeu au Setup (celui du héros actif reste en jeu, sans effet) ;
//   - wt007-wt009 : les armes Restricted posées sur l'identité ;
//   - wt018 Countdown to Ragnarok : manigance annexe, menace posée par Fenris.
// Aucun correctif de plateau : le rendu générique suffisait (modèle `hepzibah-plateau.test.ts`).
import { describe, expect, it } from 'vitest'
import { carteSurTable as carte, dessinee, siege, tableAvec } from './plateau-de-test'

const IDENTITE = 1
const TITRE = 2
const SOUTIEN_FANDRAL = 3
const SOUTIEN_HOGUN = 4
const SOUTIEN_VOLSTAGG = 5
const ARME = 6

const table = (face: string, nom: string) =>
  tableAvec(
    siege({
      area_hero: [
        carte(IDENTITE, face, 'Hero', nom),
        carte(TITRE, 'wt002', 'Upgrade', 'The Warriors Three', { bind_object_id: IDENTITE }),
        carte(SOUTIEN_FANDRAL, 'wt003', 'Support', 'Fandral'),
        carte(SOUTIEN_HOGUN, 'wt004', 'Support', 'Hogun'),
        carte(SOUTIEN_VOLSTAGG, 'wt005', 'Support', 'Volstagg'),
        carte(ARME, 'wt007', 'Upgrade', 'Brandrheid Undrsigr', { bind_object_id: IDENTITE }),
      ],
    })
  )

describe('The Warriors Three : le héros actif et ses cartes', () => {
  it('le héros actif est dessiné, la carte-titre est portée par lui', () => {
    const m = table('wt001a', 'Fandral')
    expect(dessinee(m, IDENTITE)).toBeDefined()
    expect(dessinee(m, TITRE)).toBeDefined()
    expect(dessinee(m, TITRE)?.portePar).toBe(IDENTITE)
  })

  it('les trois soutiens PERSONA (héros inactifs) sont dessinés', () => {
    const m = table('wt001c', 'Hogun')
    expect(dessinee(m, SOUTIEN_FANDRAL)).toBeDefined()
    expect(dessinee(m, SOUTIEN_HOGUN)).toBeDefined()
    expect(dessinee(m, SOUTIEN_VOLSTAGG)).toBeDefined()
  })

  it("l'arme Restricted est dessinée derrière l'identité, quel que soit le héros actif", () => {
    for (const [face, nom] of [['wt001a', 'Fandral'], ['wt001c', 'Hogun'], ['wt001d', 'Volstagg']] as const) {
      const m = table(face, nom)
      expect(dessinee(m, ARME)?.portePar).toBe(IDENTITE)
    }
  })
})

describe("arbitrages du 26/10/2026 : ce que le joueur voit de plus", () => {
  // Notice de l'auteur : « Status cards on your inactive heroes will remain on them ». Le moteur range la carte d'état d'un héros
  // inactif dans la zone d'état de SON SOUTIEN (wt003-wt005) ; le plateau doit l'y dessiner.
  const SONNE = 90
  const TENACE = 91
  it("la carte d'état d'un héros inactif est dessinée sur son soutien PERSONA", () => {
    const m = tableAvec(
      siege({
        area_hero: [
          carte(IDENTITE, 'wt001c', 'Hero', 'Hogun'),
          carte(SOUTIEN_FANDRAL, 'wt003', 'Support', 'Fandral'),
          carte(SOUTIEN_VOLSTAGG, 'wt005', 'Support', 'Volstagg'),
          carte(SONNE, 'stunned', 'StatusCard', 'Stunned', { bind_object_id: SOUTIEN_FANDRAL }),
          carte(TENACE, 'tough', 'StatusCard', 'Tough', { bind_object_id: SOUTIEN_VOLSTAGG }),
        ],
      })
    )
    expect(dessinee(m, SONNE)).toBeDefined()
    expect(dessinee(m, SONNE)?.portePar).toBe(SOUTIEN_FANDRAL)
    expect(dessinee(m, TENACE)).toBeDefined()
    expect(dessinee(m, TENACE)?.portePar).toBe(SOUTIEN_VOLSTAGG)
  })

  // wt016 A Questing We Shall Go! : « Reveal it, then attach this card to it » : l'obligation est dessinée SOUS le sbire.
  it("A Questing We Shall Go! est dessinée attachée au sbire, pas à l'identité", () => {
    const SBIRE = 95
    const OBLIGATION = 96
    const m = tableAvec(
      siege({
        area_hero: [carte(IDENTITE, 'wt001a', 'Hero', 'Fandral')],
      }),
      {
        area_villain: [
          carte(SBIRE, '01101', 'Minion', 'Hydra Mercenary'),
          carte(OBLIGATION, 'wt016', 'Obligation', 'A Questing We Shall Go!', { bind_object_id: SBIRE }),
        ],
      }
    )
    expect(dessinee(m, OBLIGATION)).toBeDefined()
    expect(dessinee(m, OBLIGATION)?.portePar).toBe(SBIRE)
  })
})

describe('wt017 Fenris et wt018 Countdown to Ragnarok : la menace posée par Fenris se lit sur la manigance', () => {
  const FENRIS = 80
  const COMPTE_A_REBOURS = 81
  const monde = () =>
    tableAvec(siege({ area_hero: [carte(IDENTITE, 'wt001a', 'Hero', 'Fandral')] }), {
      area_villain: [carte(FENRIS, 'wt017', 'Minion', 'Fenris')],
      area_schemes_side: [carte(COMPTE_A_REBOURS, 'wt018', 'SideScheme', 'Countdown to Ragnarok', { info: { threat: 3 } })],
    })

  it('Fenris est dessiné parmi les ennemis', () => {
    expect(dessinee(monde(), FENRIS)).toBeDefined()
  })

  it('Countdown to Ragnarok est dessinée dans la zone des manigances annexes', () => {
    expect(dessinee(monde(), COMPTE_A_REBOURS)).toBeDefined()
  })
})
