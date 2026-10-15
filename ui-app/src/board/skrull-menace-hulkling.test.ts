// Hulkling (Kajislav, pack skrull_menace) : ce que le plateau DESSINE.
// PROCESSUS-CARTE étape 8 bis, pour les 17 cartes du pack qui changent ce
// qu'on voit (retournement, attachement, statut, compteur, zone).
//
// Les formes ne sont pas inventées : elles reprennent un descripteur CAPTURÉ
// le 15/10/2026 (`tools/sonde_campagne.py` pointée sur `.game-src`, scénario
// rhino, deck hulkling_kajislav), après ces commandes Puzzle :
//   ChangeToFace sk001b->sk001a, Flip sk002a, Reveal sk034, PutIntoPlay sk031,
//   PutIntoPlay sk010 (+ Counter individual -1), Tough/Confuse sur l'identité,
//   Confuse + Stun Rhino, Reveal sk032, PutIntoPlay sk033, PutIntoPlay sk015 +
//   Tough. Relevé :
//
//   joueur.area_hero        : id=1  sk001a Hero
//                             id=86 confused StatusCard     bind=1
//                             id=2  sk002b Upgrade (Kree Origin, face B) bind=1
//                             id=6  sk034 Attachment (Inhibited)         bind=1
//   joueur.allies           : id=24 sk015 Ally (Lauri-Ell)
//                             id=85 tough StatusCard        bind=24
//   joueur.supports         : id=19 sk010 Support {c_individual:1, c_individual_printed:2}
//   joueur.obligations_area : id=3  sk031 Obligation
//   joueur.engaged_enemies  : id=4  sk032 Minion (Empress R'Klll)
//   world.area_schemes_side : id=5  sk033 EncounterSideScheme (DNA Masking)
//   world.area_villain      : id=50 01094 EncounterVillain
//                             id=83 confused StatusCard bind=50, id=84 stunned bind=50
import { describe, expect, it } from 'vitest'
import { construirePlateau } from './zones'
import { catalogueVide } from './catalogue'
import { carteSurTable, cartesDessinees, dessinee, siege, tableAvec } from './plateau-de-test'
import type { World } from './world'

const HULKLING = 1
const ORIGINE = 2
const INHIBITED = 6
const DESORIENTE = 86
const LAURI = 24
const TENACE = 85
const ANCESTORS = 19
const HATRED = 3
const RKLLL = 4
const DNA = 5
const RHINO = 50
const RHINO_DESORIENTE = 83
const RHINO_SONNE = 84

const monde = (): World =>
  tableAvec(
    siege({
      area_hero: [
        carteSurTable(HULKLING, 'sk001a', 'Hero', 'Hulkling'),
        carteSurTable(DESORIENTE, 'confused', 'StatusCard', 'Confused', { bind_object_id: HULKLING }),
        carteSurTable(ORIGINE, 'sk002b', 'Upgrade', 'Kree Origin', { bind_object_id: HULKLING }),
        carteSurTable(INHIBITED, 'sk034', 'Attachment', 'Inhibited', { bind_object_id: HULKLING }),
      ],
      allies: [
        carteSurTable(LAURI, 'sk015', 'Ally', 'Lauri-Ell'),
        carteSurTable(TENACE, 'tough', 'StatusCard', 'Tough', { bind_object_id: LAURI }),
      ],
      supports: [
        carteSurTable(ANCESTORS, 'sk010', 'Support', 'Ancestors', {
          info: { c_individual: 1, c_individual_printed: 2, k_threat: 0 },
        }),
      ],
      obligations_area: [carteSurTable(HATRED, 'sk031', 'Obligation', 'Interracial Hatred')],
      engaged_enemies: [carteSurTable(RKLLL, 'sk032', 'Minion', "Empress R'Klll")],
      player_discard_pile: [carteSurTable(70, 'sk014', 'Upgrade', 'Nega Rings')],
      hand_cards: [carteSurTable(71, 'sk004', 'Event', 'Kree Durability')],
    }),
    {
      area_schemes_side: [carteSurTable(DNA, 'sk033', 'EncounterSideScheme', 'DNA Masking')],
      area_villain: [
        carteSurTable(RHINO, '01094', 'EncounterVillain', 'Rhino'),
        carteSurTable(RHINO_DESORIENTE, 'confused', 'StatusCard', 'Confused', { bind_object_id: RHINO }),
        carteSurTable(RHINO_SONNE, 'stunned', 'StatusCard', 'Stunned', { bind_object_id: RHINO }),
      ],
    } as Partial<World>
  )

function compteursDe(world: World, id: number) {
  const plateau = construirePlateau(world, { playerId: 0, catalogue: catalogueVide })
  for (const e of plateau.emplacements)
    for (const g of e.groupes) for (const u of g) if (Number(u.carte.id) === id) return u.carte.counters ?? []
  throw new Error(`carte ${id} absente du plateau`)
}

describe('Hulkling (Kajislav) : ce que ses cartes dessinent', () => {
  // sk001b (Setup) puis sk002a/b (Action « flip this card ») : l'origine est
  // une amélioration permanente posée sur l'identité, et c'est la FACE qui
  // dit quelle forme Hulkling a. Après le retournement, la face B doit être
  // celle qu'on voit, accrochée à Hulkling.
  it("l'origine retournée est dessinée sur Hulkling, face Kree Origin visible", () => {
    const carte = dessinee(monde(), ORIGINE)
    expect(carte).toBeDefined()
    expect(carte?.portePar).toBe(HULKLING)
    expect(carte?.codeCarte).toBe('sk002b')
    expect(carte?.facedown).toBe(false)
  })

  // sk034 Inhibited : « Attach to your identity ».
  it('Inhibited est dessinée attachée à Hulkling', () => {
    expect(dessinee(monde(), INHIBITED)?.portePar).toBe(HULKLING)
  })

  // sk024 Drunk in Love (Confused sur l'identité), sk004/sk015/sk016 (Tenace),
  // sk006 Shift and Strike (Sonné/Désorienté sur l'ennemi).
  it("les statuts posés par le pack sont dessinés sur leur porteur", () => {
    expect(dessinee(monde(), DESORIENTE)?.portePar).toBe(HULKLING)
    expect(dessinee(monde(), TENACE)?.portePar).toBe(LAURI)
    expect(dessinee(monde(), RHINO_DESORIENTE)?.portePar).toBe(RHINO)
    expect(dessinee(monde(), RHINO_SONNE)?.portePar).toBe(RHINO)
  })

  // sk010 Ancestors : « Uses (2 individual counters) », un déjà retiré.
  it('Ancestors montre son compteur individual restant', () => {
    expect(compteursDe(monde(), ANCESTORS)).toContainEqual(expect.objectContaining({ value: 1 }))
  })

  // sk031 obligation, sk032 sbire némésis, sk033 complot annexe : trois zones.
  it("l'obligation, le sbire némésis et le complot annexe sont sur la table", () => {
    expect(dessinee(monde(), HATRED)).toBeDefined()
    expect(dessinee(monde(), RKLLL)).toBeDefined()
    expect(dessinee(monde(), DNA)).toBeDefined()
  })

  // sk014 Nega Rings, sk030 Pride, sk021 Deflect the Blow, sk029 Glorious
  // Flight : des cartes changent de zone entre main et défausse. La carte du
  // dessus de la défausse et la carte de la main restent dessinées.
  it('la carte arrivée en défausse et celle arrivée en main sont dessinées', () => {
    const zones = Object.fromEntries(cartesDessinees(monde()).map((c) => [c.id, c.zone]))
    expect(zones[70]).toBe('piles-joueur')
    expect(zones[71]).toBe('main')
  })

  // Témoin : sans lui, un plateau qui dessinerait TOUT en racine passerait le
  // premier cas. L'origine ne doit pas apparaître comme une carte séparée.
  it("TEMOIN : l'origine n'est pas dessinée comme une racine séparée", () => {
    const racines = cartesDessinees(monde()).filter((c) => c.portePar === 0).map((c) => c.id)
    expect(racines).not.toContain(ORIGINE)
    expect(racines).toContain(HULKLING)
  })
})
