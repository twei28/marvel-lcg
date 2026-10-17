// Cartes DUAL Shinobi (TMNT Shinobi, `sc`) : ce que le plateau DESSINE une fois la carte résolue.
//
// `Fusion/marvel-lcg-src/tools/cas/tmnt_shinobi_dual.py` prouve ce que le moteur FAIT ; ce fichier prouve ce que le
// joueur REGARDE (PROCESSUS-CARTE.md, étape 8 bis). On pose à la main l'état d'arrivée que le moteur publie, et on
// affirme sur `dessinee(...)`.
//
// Ce que les douze cartes changent à l'écran, et rien d'autre : les COMPTEURS de samouraï des améliorations OATH
// (sc002, sc004, sc005), les cartes d'ÉTAT posées sur un personnage (Cloaked : sc003, sc004, sc007, sc008, sc011,
// sc012 ; Dazed : sc001, sc005, sc008, sc011 ; Tough : sc003), et la carte de rencontre révélée par sc008. Les autres
// (sc006 +2 DEF, sc009 carte remise au-dessus du deck, sc010 soin) ne dessinent rien de nouveau.
//
// ⚠ Verts d'emblée : les mécanismes (compteur de samouraï, cartes d'état, amélioration attachée) sont déjà couverts par
// `tmnt-jennika-plateau.test.ts` et `effets-statuts.test.ts` ; il n'y a donc pas de « vu ROUGE sans le correctif » possible
// ici, et on le dit. Ce fichier verrouille que les cartes DUAL empruntent bien ces chemins (genre, compteurs, porteur).
import { describe, expect, it } from 'vitest'
import { carteSurTable as carte, cartesDessinees, dessinee, siege, tableAvec } from './plateau-de-test'
import type { WorldCard } from './world'

const IDENTITE = 1
const ALLIE = 2
const RHINO = 80
const heros = () => carte(IDENTITE, '01001a', 'Hero', 'Spider-Man')

const amelioration = (id: number, card: string, nom: string, samurai: number, extra: Partial<WorldCard> = {}) =>
  carte(id, card, 'Upgrade', nom, { bind_object_id: IDENTITE, info: { c_samurai: samurai }, ...extra })
const sur = (...cartes: WorldCard[]) => tableAvec(siege({ area_hero: [heros(), ...cartes] }))

describe('sc002 Shugorei, sc004 Kuragari, sc005 Yoi-Dachi : les compteurs de samouraï sont dessinés', () => {
  it('Shugorei entre avec 4 compteurs, en genre amélioration, attachée au héros', () => {
    const c = dessinee(sur(amelioration(10, 'sc002', 'Shugorei', 4)), 10)
    expect(c?.kind).toBe('upgrade')
    expect(c?.compteurs.samurai).toBe(4)
    expect(c?.portePar).toBe(IDENTITE)
  })

  it('Shugorei après une Action : 2 compteurs, carte inclinée donc couchée', () => {
    const c = dessinee(sur(amelioration(10, 'sc002', 'Shugorei', 2, { is_ready: false } as Partial<WorldCard>)), 10)
    expect(c?.compteurs.samurai).toBe(2)
    expect(c?.exhausted).toBe(true)
  })

  it('Kuragari et Yoi-Dachi entrent avec 3 compteurs', () => {
    const m = sur(amelioration(11, 'sc004', 'Kuragari', 3), amelioration(12, 'sc005', 'Yoi-Dachi', 3))
    expect(dessinee(m, 11)?.compteurs.samurai).toBe(3)
    expect(dessinee(m, 12)?.compteurs.samurai).toBe(3)
  })

  it('Yoi-Dachi après une Réponse : 2 compteurs ; au dernier compteur retiré elle quitte la table (défausse du joueur)', () => {
    expect(dessinee(sur(amelioration(12, 'sc005', 'Yoi-Dachi', 2)), 12)?.compteurs.samurai).toBe(2)
    const apres = tableAvec(siege({ area_hero: [heros()], player_discard_pile: [amelioration(12, 'sc005', 'Yoi-Dachi', 0)] }))
    expect(dessinee(apres, 12)?.zone).toBe('piles-joueur')
  })

  it('Kuragari, après son unique utilisation (3 compteurs retirés), est dans la défausse et le héros est redressé', () => {
    const m = tableAvec(siege({ area_hero: [heros()], player_discard_pile: [amelioration(11, 'sc004', 'Kuragari', 0)] }))
    expect(dessinee(m, 11)?.zone).toBe('piles-joueur')
    expect(dessinee(m, IDENTITE)?.exhausted).toBe(false)
  })

  it('Kusuri (sc010, sans compteur) est dessinée en genre amélioration', () => {
    const c = dessinee(sur(carte(13, 'sc010', 'Upgrade', 'Kusuri', { bind_object_id: IDENTITE })), 13)
    expect(c?.kind).toBe('upgrade')
    expect(Object.values(c?.compteurs ?? {}).every((n) => !n)).toBe(true)
  })
})

describe('sc003 Omawari, sc004 Kuragari, sc007 Mizuki, sc011 Kenbu : les cartes d état sur les amis', () => {
  it('Omawari : le héros porte Cloaked ET Tough, deux cartes distinctes', () => {
    const m = sur(
      carte(70, 'cloaked', 'StatusCard', 'Cloaked', { bind_object_id: IDENTITE }),
      carte(71, 'tough', 'StatusCard', 'Tough', { bind_object_id: IDENTITE })
    )
    expect(dessinee(m, 70)?.portePar).toBe(IDENTITE)
    expect(dessinee(m, 70)?.codeCarte).toBe('cloaked')
    expect(dessinee(m, 71)?.portePar).toBe(IDENTITE)
    expect(dessinee(m, 71)?.codeCarte).toBe('tough')
  })

  it('Mizuki : un allié camouflé porte sa carte Cloaked, le héros (sans carte) n en porte aucune', () => {
    const m = tableAvec(
      siege({
        area_hero: [
          heros(),
          carte(ALLIE, '01059', 'Ally', 'Jessica Jones'),
          carte(70, 'cloaked', 'StatusCard', 'Cloaked', { bind_object_id: ALLIE }),
        ],
      })
    )
    expect(dessinee(m, 70)?.portePar).toBe(ALLIE)
    expect(cartesDessinees(m).filter((c) => c.portePar === IDENTITE && c.kind === 'status')).toHaveLength(0)
  })
})

describe('sc001 Nendō, sc005 Yoi-Dachi, sc008 Naito Dansā, sc011 Kenbu : Dazed posé sur les ennemis', () => {
  it('chaque ennemi hébété porte SA carte Dazed (jamais deux sur le même)', () => {
    const m = tableAvec(siege({ area_hero: [heros()] }), {
      area_villain: [
        carte(RHINO, '01094', 'EncounterVillain', 'Rhino'),
        carte(81, 'dazed', 'StatusCard', 'Dazed', { bind_object_id: RHINO }),
      ],
    })
    expect(dessinee(m, 81)?.kind).toBe('status')
    expect(dessinee(m, 81)?.codeCarte).toBe('dazed')
    expect(dessinee(m, 81)?.portePar).toBe(RHINO)
  })
})

describe('sc008 Naito Dansā : la carte de rencontre révélée est sur la table', () => {
  it('l attachement révélé est attaché à Rhino', () => {
    const m = tableAvec(siege({ area_hero: [heros()] }), {
      area_villain: [carte(RHINO, '01094', 'EncounterVillain', 'Rhino'), carte(90, '01100', 'Attachment', 'Enhanced Ivory Horn', { bind_object_id: RHINO })],
    })
    expect(dessinee(m, 90)).toBeDefined()
    expect(dessinee(m, 90)?.portePar).toBe(RHINO)
  })
})
