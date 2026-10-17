// TMNT Shinobi Ninjutsu (`sa`) : ce que le plateau DESSINE une fois la carte résolue.
//
// `Fusion/marvel-lcg-src/tools/cas/tmnt_shinobi_ninjutsu.py` prouve ce que le moteur FAIT ; ce fichier prouve ce que le joueur
// REGARDE (PROCESSUS-CARTE.md, étape 8 bis). On pose à la main l'état d'arrivée que le moteur publie (`bind_object_id` = la carte
// porteuse, `info.c_<compteur>` = les compteurs) et on affirme sur `dessinee(...)`.
//
// Ce que les Ninjutsu font VOIR : la carte d'état Cloaked sur un personnage (identité ou allié : toutes les cartes), les compteurs
// `shadow` de Hamato Clan (sa007) et `smoke` de Smoke Bombs (sa008), l'amélioration Twilight Sentry attachée à un ALLIÉ (sa009),
// Shadow Summon qui met un allié en jeu (sa016, un allié posé : couvert par les zones de base). Les cartes qui ne font que
// chiffrer, piocher, regarder un deck (sa003, rien d'affiché) ou incliner n'ont pas de cas.
import { afterEach, describe, expect, it, vi } from 'vitest'
import { nomDeCompteur } from './compteurs-fr'
import * as langue from './langue'
import { carteSurTable as carte, dessinee, siege, tableAvec } from './plateau-de-test'

afterEach(() => vi.restoreAllMocks())

const IDENTITE = 1
const ALLIE = 20
const CLOAKED_HEROS = 30
const CLOAKED_ALLIE = 31
const CLAN = 40
const BOMBES = 41
const SENTRY = 42

const heros = () => carte(IDENTITE, '01001a', 'Hero', 'Spider-Man')
const allie = () => carte(ALLIE, 'tl002', 'Ally', 'Splinter')

describe('Cloaked : la carte d état est dessinée sur le personnage camouflé', () => {
  it('sur le héros', () => {
    const m = tableAvec(
      siege({ area_hero: [heros(), carte(CLOAKED_HEROS, 'cloaked', 'StatusCard', 'Cloaked', { bind_object_id: IDENTITE })] })
    )
    expect(dessinee(m, CLOAKED_HEROS)).toBeDefined()
    expect(dessinee(m, CLOAKED_HEROS)?.portePar).toBe(IDENTITE)
    expect(dessinee(m, CLOAKED_HEROS)?.codeCarte).toBe('cloaked')
  })

  it('sur un allié (Hamato Clan, Smoke Bombs, Twilight Sentry, Moja)', () => {
    const m = tableAvec(
      siege({
        area_hero: [heros()],
        allies: [allie(), carte(CLOAKED_ALLIE, 'cloaked', 'StatusCard', 'Cloaked', { bind_object_id: ALLIE })],
      })
    )
    expect(dessinee(m, CLOAKED_ALLIE)?.portePar).toBe(ALLIE)
  })

  it('témoin : sans carte d état, rien n est dessiné sur l allié', () => {
    expect(dessinee(tableAvec(siege({ area_hero: [heros()], allies: [allie()] })), CLOAKED_ALLIE)).toBeUndefined()
  })
})

describe('sa007 Hamato Clan : les compteurs shadow sont dessinés sur le soutien', () => {
  const clan = (ombres: number, extra = {}) =>
    carte(CLAN, 'sa007', 'Support', 'Hamato Clan', { info: { c_shadow: ombres }, ...extra })
  const monde = (...cartes: ReturnType<typeof clan>[]) => tableAvec(siege({ area_hero: [heros()], supports: cartes }))

  it('un compteur après le départ d un allié', () => {
    expect(dessinee(monde(clan(1)), CLAN)?.compteurs.shadow).toBe(1)
  })

  it('en genre soutien, dans la zone des soutiens', () => {
    expect(dessinee(monde(clan(1)), CLAN)?.kind).toBe('support')
  })

  it('l action incline la carte : couchée, avec le compteur restant', () => {
    const c = dessinee(monde(clan(1, { is_ready: false })), CLAN)
    expect(c?.exhausted).toBe(true)
    expect(c?.compteurs.shadow).toBe(1)
  })

  it('libellé français du compteur', () => {
    vi.spyOn(langue, 'langueActuelle').mockReturnValue('fr')
    expect(nomDeCompteur('shadow')).toBe('ombre')
  })
})

describe('sa008 Smoke Bombs : les compteurs smoke sont dessinés sur l amélioration', () => {
  const bombes = (fumees: number, extra = {}) =>
    carte(BOMBES, 'sa008', 'Upgrade', 'Smoke Bombs', { bind_object_id: IDENTITE, info: { c_smoke: fumees }, ...extra })
  const monde = (b: ReturnType<typeof bombes>) => tableAvec(siege({ area_hero: [heros(), b] }))

  it('elle entre avec 2 compteurs', () => {
    expect(dessinee(monde(bombes(2)), BOMBES)?.compteurs.smoke).toBe(2)
  })

  it('en genre amélioration, portée par le héros', () => {
    const c = dessinee(monde(bombes(2)), BOMBES)
    expect(c?.kind).toBe('upgrade')
    expect(c?.portePar).toBe(IDENTITE)
  })

  it('après la dernière utilisation : plus sur la table, dans la défausse du joueur', () => {
    const m = tableAvec(siege({ area_hero: [heros()], player_discard_pile: [bombes(0)] }))
    expect(dessinee(m, BOMBES)?.zone).toBe('piles-joueur')
  })

  it('libellé français du compteur', () => {
    vi.spyOn(langue, 'langueActuelle').mockReturnValue('fr')
    expect(nomDeCompteur('smoke')).toBe('fumée')
  })
})

describe('sa009 Twilight Sentry : l amélioration est dessinée sur l ALLIÉ, avec sa carte Cloaked', () => {
  const monde = () =>
    tableAvec(
      siege({
        area_hero: [heros()],
        allies: [
          allie(),
          carte(SENTRY, 'sa009', 'Upgrade', 'Twilight Sentry', { bind_object_id: ALLIE }),
          carte(CLOAKED_ALLIE, 'cloaked', 'StatusCard', 'Cloaked', { bind_object_id: ALLIE }),
        ],
      })
    )

  it('l amélioration est à l écran, portée par l allié (pas par le héros)', () => {
    expect(dessinee(monde(), SENTRY)).toBeDefined()
    expect(dessinee(monde(), SENTRY)?.portePar).toBe(ALLIE)
    expect(dessinee(monde(), SENTRY)?.kind).toBe('upgrade')
  })

  it('la carte Cloaked posée à l attache est dessinée aussi sur l allié', () => {
    expect(dessinee(monde(), CLOAKED_ALLIE)?.portePar).toBe(ALLIE)
  })
})
