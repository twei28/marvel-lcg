// Aspect TMNT Justice (`uj`) : ce que le plateau DESSINE (PROCESSUS-CARTE étape 8 bis).
// Cartes qui changent ce qu'on VOIT :
//  - uj020 Mona Lisa : SOUTIEN qui glisse un événement face cachée sous lui (tuck) ;
//  - uj005 Delirium : amélioration attachée à un SBIRE engagé ;
//  - uj002 Chance Encounter : amélioration attachée à une manigance (principale ou annexe) ;
//  - uj034 Turtle Line : amélioration attachée à un allié, jetons « rope » (corde) ;
//  - uj026 Ram-Shell : jetons « momentum » (élan) ; uj039 Zebulon : jetons « scorch » (brûlure) ;
//  - uj021 Mondo Gecko : carte d'état Cloaked attachée à un allié ;
//  - uj019 Mission Training : amélioration attachée à un allié.
// L'état d'arrivée est posé à la main, dans la forme publiée par le moteur (identifiants
// d'objet, `bind_object_id`, clés `c_<compteur>` de `info`) relevée par les cas
// `[uj]` de `tools/cas/tmnt_aspect_justice.py` (journal : « déplacée(s) vers ...
// PlaceCardArea », « s'équipe de », « gagne Cloaked »).
import { describe, expect, it } from 'vitest'
import { catalogueVide } from './catalogue'
import { toScanCard } from './card-model'
import { carteSurTable, cartesDessinees, dessinee, siege, tableAvec } from './plateau-de-test'
import type { World, WorldCard } from './world'

const HEROS = 1
const MONA = 82
const GLISSEE = 26
const SBIRE = 56
const DELIRIUM = 81
const PRINCIPALE = 48
const ANNEXE = 60
const CHANCE = 83
const GECKO = 84
const LIGNE = 85
const CAMOUFLE = 86
const RAM = 87
const ZEB = 88
const TRAINING = 89

const monde = (): World =>
  tableAvec(
    siege({
      area_hero: [carteSurTable(HEROS, '01001a', 'Hero', 'Spider-Man')],
      supports: [
        carteSurTable(MONA, 'uj020', 'Support', 'Mona Lisa'),
        carteSurTable(GLISSEE, '04049', 'Event', 'Clear the Area', { bind_object_id: MONA, is_face_up: false }),
      ],
      allies: [
        carteSurTable(GECKO, 'uj021', 'Ally', 'Mondo Gecko'),
        carteSurTable(CAMOUFLE, 'cloaked', 'Status', 'Cloaked', { bind_object_id: GECKO }),
        carteSurTable(LIGNE, 'uj034', 'Upgrade', 'Turtle Line', { bind_object_id: GECKO, info: { c_rope: 2 } }),
        carteSurTable(TRAINING, 'uj019', 'Upgrade', 'Mission Training', { bind_object_id: GECKO }),
        carteSurTable(RAM, 'uj026', 'Ally', 'Ram-Shell', { info: { c_momentum: 3 } }),
        carteSurTable(ZEB, 'uj039', 'Ally', 'Zebulon', { info: { c_scorch: 4 } }),
      ],
      engaged_enemies: [
        carteSurTable(SBIRE, '01101', 'Minion', 'Hydra Mercenary'),
        carteSurTable(DELIRIUM, 'uj005', 'Upgrade', 'Delirium', { bind_object_id: SBIRE }),
      ],
    }),
    {
      area_schemes_main: [
        carteSurTable(PRINCIPALE, '01097b', 'MainScheme', 'The Break-In!'),
        carteSurTable(CHANCE, 'uj002', 'Upgrade', 'Chance Encounter', { bind_object_id: PRINCIPALE }),
      ],
      area_schemes_side: [carteSurTable(ANNEXE, '01107', 'SideScheme', "Breakin' & Takin'")],
    } as Partial<World>
  )

const contexte = () => ({ playerId: 0, actives: new Set<number>(), catalogue: catalogueVide })
const scan = (carte: WorldCard) => toScanCard(carte, contexte())

describe('uj020 Mona Lisa : événement glissé sous un SOUTIEN', () => {
  it('dessine la carte glissée', () => {
    expect(dessinee(monde(), GLISSEE)).toBeDefined()
  })
  it('la dessine dans l unité de Mona Lisa, juste derrière elle, posée face cachée', () => {
    const vues = cartesDessinees(monde())
    const rang = (id: number) => vues.findIndex((c) => c.id === id)
    expect(dessinee(monde(), GLISSEE)?.portePar).toBe(MONA)
    expect(rang(GLISSEE)).toBe(rang(MONA) + 1)
    expect(dessinee(monde(), GLISSEE)?.peeking).toBe(true)
  })
})

describe('uj005 Delirium / uj002 Chance Encounter / uj019 Mission Training : améliorations attachées', () => {
  it('Delirium est dessinée sur le sbire engagé', () => {
    expect(dessinee(monde(), DELIRIUM)?.portePar).toBe(SBIRE)
  })
  it('Chance Encounter est dessinée sur la manigance principale', () => {
    expect(dessinee(monde(), CHANCE)?.portePar).toBe(PRINCIPALE)
  })
  it('Mission Training et Turtle Line sont dessinées sur Mondo Gecko', () => {
    expect(dessinee(monde(), TRAINING)?.portePar).toBe(GECKO)
    expect(dessinee(monde(), LIGNE)?.portePar).toBe(GECKO)
  })
})

describe('uj021 Mondo Gecko : carte d état Cloaked', () => {
  it('la carte Cloaked est dessinée sur Mondo Gecko', () => {
    expect(dessinee(monde(), CAMOUFLE)?.portePar).toBe(GECKO)
  })
})

describe('compteurs uj : momentum (Ram-Shell), scorch (Zebulon), rope (Turtle Line)', () => {
  it('les trois compteurs sont dessinés avec leur valeur', () => {
    expect(dessinee(monde(), RAM)?.compteurs['momentum']).toBe(3)
    expect(dessinee(monde(), ZEB)?.compteurs['scorch']).toBe(4)
    expect(dessinee(monde(), LIGNE)?.compteurs['rope']).toBe(2)
  })
  it('leurs noms français : élan, brûlure, corde', () => {
    const etiquette = (carte: WorldCard, cle: string) =>
      scan(carte).counters?.find((c) => c.cle === cle)?.label?.toLowerCase()
    expect(etiquette(carteSurTable(RAM, 'uj026', 'Ally', 'Ram-Shell', { info: { c_momentum: 1 } }), 'momentum')).toContain('élan')
    expect(etiquette(carteSurTable(ZEB, 'uj039', 'Ally', 'Zebulon', { info: { c_scorch: 1 } }), 'scorch')).toContain('brûlure')
    expect(etiquette(carteSurTable(LIGNE, 'uj034', 'Upgrade', 'Turtle Line', { info: { c_rope: 1 } }), 'rope')).toContain('corde')
  })
})
