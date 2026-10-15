// Skrull Pantheon (scénario 4 de Skrull Menace, Kajislav) et Dard'van Sect : ce que le plateau DESSINE.
// PROCESSUS-CARTE étape 8 bis, pour les cartes qui changent ce qu'on voit : jetons de foi sur le méchant,
// carte d'état Tenace, méchant à DEUX FACES retourné (Kly'bn / Sl'gur't), attachement Blessed by posé sur un
// sbire, environnement Skrull Pantheon mis en jeu face Stronghold ou Destroyed.
//
// Les états sont CAPTURÉS sur le moteur le 15/10/2026 (`tools/sonde_campagne.py`, scénario sk_skrull_pantheon,
// deck spider_man) après ces commandes Puzzle :
//
//  (1) EmptyEncounterDeck, ChangeForm 01001b, Counter sk170a faith 2, Tough sk170a, PutIntoPlay sk107,
//      PutIntoPlay sk178, Reveal sk176, PutIntoPlay sk179 :
//        area_villain      : id=50 sk170a EncounterVillain {c_faith:3, scheme:2, attack:1, max_health:15}
//                            id=92 tough StatusCard bind=50
//        area_schemes_main : id=48 sk173b MainScheme (face B, down sk173a)
//        area_schemes_side : id=96 sk179 EncounterSideScheme
//        engaged_enemies   : id=93 sk107 Minion {scheme:6 = 3 + 3 de Blessed} ; id=95 sk176 Attachment bind=93 ;
//                            id=94 sk178 Nogor {scheme:4, attack:4, max_health:7 = 1+3, 1+3, 4+3}
//        area_set_aside    : id=91 sk175a Environment (down sk175b)
//  (4) EmptyEncounterDeck, CreateEncounterDeck sk107 x2, Reveal sk186 (Dard'van Sect : 1 carte de boost face cachee au mechant) :
//        area_villain      : id=50 sk170a ; id=93 sk107 Minion bind=50 (la carte de boost, portee par le mechant)
//  (2) EmptyEncounterDeck, EmptyHand, ChangeForm 01001b, PlaceThreat sk173b +3 (stade 1 accompli) :
//        area_villain      : id=50 sk170b EncounterVillain « Sl'gur't » {c_faith:2} (down sk170a)
//        area_schemes_main : id=49 sk174b ; area_environment : id=91 sk175a (Stronghold, down sk175b)
//  (3) idem avec PlaceThreat sk173b -6 (dernière menace retirée) :
//        area_environment  : id=91 sk175b (Destroyed, down sk175a) ; villain id=50 sk170b {c_faith:2}
import { describe, expect, it } from 'vitest'
import { catalogueVide } from './catalogue'
import { toScanCard } from './card-model'
import { carteSurTable, cartesDessinees, dessinee, siege, tableAvec } from './plateau-de-test'
import type { World, WorldCard } from './world'

const KLYBN = 50
const TENACE = 92
const COMPLOT_1B = 48
const COMPLOT_2B = 49
const WASTES = 96
const SCIENTIST = 93
const BLESSED = 95
const NOGOR = 94
const ENV = 91

const klybn = (foi = 3): WorldCard =>
  carteSurTable(KLYBN, 'sk170a', 'EncounterVillain', "Kly'bn", {
    info: { max_health: 15, health: 15, scheme: 2, attack: 1, c_faith: foi },
    down_card_ids: ['sk170b'],
  })

// Après un « Flip the villain » : la MÊME carte (id 50), face Sl'gur't visible, jetons conservés.
const slgurt = (foi = 2): WorldCard =>
  carteSurTable(KLYBN, 'sk170b', 'EncounterVillain', "Sl'gur't", {
    info: { max_health: 15, health: 15, scheme: 1, attack: 2, c_faith: foi },
    down_card_ids: ['sk170a'],
  })

const environnement = (face: 'sk175a' | 'sk175b'): WorldCard =>
  carteSurTable(ENV, face, 'Environment', 'Skrull Pantheon', {
    down_card_ids: [face === 'sk175a' ? 'sk175b' : 'sk175a'],
  })

const monde1 = (): World =>
  tableAvec(
    siege({
      engaged_enemies: [
        carteSurTable(SCIENTIST, 'sk107', 'Minion', 'Skrull Scientist', { info: { max_health: 3, health: 3, scheme: 6, attack: 0 } }),
        carteSurTable(BLESSED, 'sk176', 'Attachment', "Blessed by Kly'bn", { bind_object_id: SCIENTIST }),
        carteSurTable(NOGOR, 'sk178', 'Minion', 'Nogor', { info: { max_health: 7, health: 7, scheme: 4, attack: 4 } }),
      ],
    }),
    {
      area_villain: [klybn(), carteSurTable(TENACE, 'tough', 'StatusCard', 'Tough', { bind_object_id: KLYBN })],
      area_schemes_main: [carteSurTable(COMPLOT_1B, 'sk173b', 'MainScheme', 'Protect the Pantheon')],
      area_schemes_side: [carteSurTable(WASTES, 'sk179', 'EncounterSideScheme', 'Shapeless Wastes')],
    } as Partial<World>
  )

const mondeApresStade1 = (face: 'sk175a' | 'sk175b'): World =>
  tableAvec(siege(), {
    area_villain: [slgurt()],
    area_schemes_main: [carteSurTable(COMPLOT_2B, 'sk174b', 'MainScheme', 'Slaying the False Gods')],
    area_environment: [environnement(face)],
  } as Partial<World>)

const contexte = () => ({ playerId: 0, actives: new Set<number>(), catalogue: catalogueVide })
const scan = (carte: WorldCard) => toScanCard(carte, contexte())

describe('Skrull Pantheon : ce que ses cartes dessinent', () => {
  // sk170a : le compteur de foi est publié sous `c_faith` et affiché.
  it("Kly'bn montre ses 3 jetons de foi", () => {
    const jetons = scan(klybn()).counters?.find((c) => c.cle === 'faith')
    expect(jetons?.value).toBe(3)
  })

  // sk170b : après le retournement, la même carte montre la face Sl'gur't ET garde ses jetons.
  it("le méchant retourné est dessiné face Sl'gur't, avec ses 2 jetons de foi", () => {
    const monde = mondeApresStade1('sk175a')
    expect(dessinee(monde, KLYBN)).toBeDefined()
    expect(dessinee(monde, KLYBN)?.codeCarte).toBe('sk170b')
    expect(scan(slgurt()).counters?.find((c) => c.cle === 'faith')?.value).toBe(2)
  })

  // sk170a : la face Kly'bn d'avant le retournement est bien celle de la carte (même id, autre face).
  it("avant le retournement, la même carte est dessinée face Kly'bn", () => {
    expect(dessinee(monde1(), KLYBN)?.codeCarte).toBe('sk170a')
  })

  // sk172a / sk172b : la carte d'état Tenace est dessinée portée par le méchant.
  it('la carte Tenace est dessinée avec le méchant', () => {
    expect(dessinee(monde1(), TENACE)).toBeDefined()
  })

  // sk176 : Blessed by Kly'bn est dessinée attachée au sbire qui la porte.
  it("Blessed by Kly'bn est dessinée attachée au sbire", () => {
    expect(dessinee(monde1(), BLESSED)).toBeDefined()
    expect(dessinee(monde1(), BLESSED)?.portePar).toBe(SCIENTIST)
  })

  // sk186 : la carte de boost donnee face cachee au mechant est dessinee portee par lui (etat (4)).
  it("la carte de boost donnée par Dard'van Sect est dessinée avec le méchant", () => {
    const monde = tableAvec(siege(), {
      area_villain: [klybn(1), carteSurTable(93, 'sk107', 'Minion', 'Skrull Scientist', { bind_object_id: KLYBN, is_face_up: false })],
      area_schemes_main: [carteSurTable(COMPLOT_1B, 'sk173b', 'MainScheme', 'Protect the Pantheon')],
    } as Partial<World>)
    expect(dessinee(monde, 93)).toBeDefined()
  })

  // sk178 / sk179 : le sbire Nogor et le complot annexe sont dessinés.
  it('Nogor et Shapeless Wastes sont dessinés', () => {
    expect(dessinee(monde1(), NOGOR)).toBeDefined()
    expect(dessinee(monde1(), WASTES)).toBeDefined()
  })

  // sk175a / sk175b : l'environnement mis en jeu par la fin du stade 1 est dessiné, face Stronghold ou Destroyed.
  it("l'environnement est dessiné face Stronghold quand le stade 1 est accompli", () => {
    const monde = mondeApresStade1('sk175a')
    expect(dessinee(monde, ENV)).toBeDefined()
    expect(dessinee(monde, ENV)?.codeCarte).toBe('sk175a')
  })

  it("l'environnement est dessiné face Destroyed quand la dernière menace est retirée", () => {
    const monde = mondeApresStade1('sk175b')
    expect(dessinee(monde, ENV)).toBeDefined()
    expect(dessinee(monde, ENV)?.codeCarte).toBe('sk175b')
  })

  // Témoin : tant que le stade 1 dure, l'environnement est mis de côté, donc nulle part à l'écran.
  it("TEMOIN : au stade 1, l'environnement mis de côté n'est pas dessiné", () => {
    expect(dessinee(monde1(), ENV)).toBeUndefined()
  })

  // Témoin : le méchant, le complot principal, le complot annexe et les sbires sont des racines ; Blessed et Tenace non.
  it('TEMOIN : seuls le méchant, les complots et les sbires sont des racines', () => {
    const racines = cartesDessinees(monde1())
      .filter((c) => c.portePar === 0)
      .map((c) => c.id)
    for (const id of [KLYBN, COMPLOT_1B, WASTES, SCIENTIST, NOGOR]) expect(racines).toContain(id)
    expect(racines).not.toContain(BLESSED)
  })

  // Témoin : sans jeton publié, aucun compteur « foi » n'est affiché.
  it('TEMOIN : sans jeton publié, aucun compteur de foi', () => {
    const sans = carteSurTable(KLYBN, 'sk170a', 'EncounterVillain', "Kly'bn", { info: { max_health: 15, health: 15 } })
    expect(scan(sans).counters?.find((c) => c.cle === 'faith')).toBeUndefined()
  })
})
