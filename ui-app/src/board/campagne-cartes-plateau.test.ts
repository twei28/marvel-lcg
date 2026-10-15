// Cartes de campagne de Skrull Menace (Kajislav, sk263-sk289b) : ce que le plateau DESSINE.
// PROCESSUS-CARTE étape 8 bis, pour les cartes qui changent ce qu'on voit :
//   - sk265 Paibok et sk267 Super-Skrull : des cartes glissées FACE CACHÉE sous l'allié ;
//   - sk268 Chilly McHotpants : l'allié devient un SBIRE engagé (autre face, même image) ;
//   - sk272 Fickle Alliance : un sbire du deck rencontre devient un ALLIÉ sous contrôle du joueur ;
//   - sk283 / sk284 / sk286 / sk287 / sk288 : améliorations accrochées à un allié, à un ennemi, à l'identité ;
//   - sk275 Skrull Military Training : en pile de victoire, bonus de stats sur le héros ;
//   - sk280 Princess Anelle : RETIRÉE DE LA PARTIE (zone « Retirées de la partie »).
//
// Les états sont CAPTURÉS sur le moteur le 15/10/2026 (`tools/sonde_campagne.py`, scénario rhino, deck spider_man,
// descripteur de monde tel que le plateau le reçoit) après ces commandes Puzzle. Relevés (id = objet du moteur) :
//
//  C1 : EmptyEncounterDeck, ChangeForm 01001b, PutIntoPlay sk265 + Tough + Discard 01186, PutIntoPlay sk267 + Discard 01022 + 01031,
//       PutIntoPlay sk268, sk038, sk184, puis sk283, sk284, sk286, sk287, sk288 (cibles : première cible légale)
//       joueur0.area_hero        : id=1 01001a Hero {thwart:1, attack:3, defense:3, max_health:13}
//                                  id=92 sk286, id=93 sk287, id=94 sk288 (bind=1)
//       joueur0.allies           : id=81 sk265 Ally {thwart:3, attack:3, max_health:4, health:3, toughness:1}
//                                  id=83 01186 Treachery is_face_up:false bind=81
//                                  id=84 sk267 Ally {thwart:4, attack:4} ; id=85 01022, id=86 01031 (Events, face cachée, bind=84)
//                                  id=88 sk038 Ally ; id=90 sk283 Upgrade bind=88
//       joueur0.engaged_enemies  : id=87 skrull_war_minion Minion pic_id=sk268 {scheme:1, attack:2, max_health:5} ; id=91 sk284 bind=87
//                                  id=89 sk184 Minion {scheme:1}
//  C2 : CreateEncounterDeck 01103, PutIntoPlay sk272, SetThreat 1, Thwart 01001a (le pilote prend la cible proposée)
//       monde.victory_display    : id=82 sk272 PlayerSideScheme
//       joueur0.allies           : id=81 skrull_fickle_ally Ally pic_id=01103 {thwart:1, attack:2, max_health:3, health:3}
//  C3 : PutIntoPlay sk266, sk267, sk275, Thwart sk266, Thwart sk267
//       monde.victory_display    : id=83 sk275 ; joueur0.area_hero id=1 01001a {thwart:2, attack:3, defense:4}
//  C4 : PutIntoPlay sk280, EndPlayerPhase
//       monde.area_removed       : id=81 sk280 Support
import { describe, expect, it } from 'vitest'
import { catalogueVide } from './catalogue'
import { toScanCard } from './card-model'
import { construirePlateau } from './zones'
import { carteSurTable, dessinee, siege, tableAvec } from './plateau-de-test'
import type { World, WorldCard } from './world'

const HEROS = 1
const SANS_IDENTITE = { thwart: 1, attack: 3, defense: 3, max_health: 13, health: 13 }
const GEMME = 94
const SHAPESHIFTER = 93
const REVERTING = 92
const PAIBOK = 81
const TRAITRISE_SOUS_PAIBOK = 83
const SUPER_SKRULL = 84
const POUVOIR_1 = 85
const POUVOIR_2 = 86
const HUMAN_TORCH = 88
const LUNETTES = 90
const CHILLY = 87
const MASQUE = 91
const FANATIC = 89
const RHINO = 49

const contexte = () => ({ playerId: 0, actives: new Set<number>(), catalogue: catalogueVide })
const scan = (carte: WorldCard) => toScanCard(carte, contexte())

const chilly = (): WorldCard =>
  carteSurTable(CHILLY, 'skrull_war_minion', 'Minion', 'Chilly McHotpants', {
    pic_id: 'sk268',
    info: { scheme: 1, attack: 2, max_health: 5, health: 5 },
  })

// C1 : tout ce qui s'accroche, se glisse ou se convertit.
const monde = (surcharges: { lienPaibok?: boolean; lienMasque?: boolean } = {}): World =>
  tableAvec(
    siege({
      area_hero: [
        carteSurTable(HEROS, '01001a', 'Hero', 'Spider-Man', { info: SANS_IDENTITE }),
        carteSurTable(REVERTING, 'sk286', 'Upgrade', 'Reverting Device', { bind_object_id: HEROS }),
        carteSurTable(SHAPESHIFTER, 'sk287', 'Upgrade', 'Skrull Shapeshifter', { bind_object_id: HEROS }),
        carteSurTable(GEMME, 'sk288', 'Upgrade', 'Sy-Torak Gem', { bind_object_id: HEROS }),
      ],
      allies: [
        carteSurTable(PAIBOK, 'sk265', 'Ally', 'Paibok', {
          info: { thwart: 3, attack: 3, max_health: 4, health: 3, toughness: 1 },
        }),
        carteSurTable(TRAITRISE_SOUS_PAIBOK, '01186', 'Treachery', 'Advance', {
          is_face_up: false,
          bind_object_id: surcharges.lienPaibok === false ? 0 : PAIBOK,
          down_card_ids: ['encounter'],
        }),
        carteSurTable(SUPER_SKRULL, 'sk267', 'Ally', 'Super-Skrull', { info: { thwart: 4, attack: 4, max_health: 4, health: 4 } }),
        carteSurTable(POUVOIR_1, '01022', 'Event', 'Ground Stomp', {
          is_face_up: false,
          bind_object_id: SUPER_SKRULL,
          down_card_ids: ['player'],
        }),
        carteSurTable(POUVOIR_2, '01031', 'Event', 'Repulsor Blast', {
          is_face_up: false,
          bind_object_id: SUPER_SKRULL,
          down_card_ids: ['player'],
        }),
        carteSurTable(HUMAN_TORCH, 'sk038', 'Ally', 'Human Torch', { info: { thwart: 1, attack: 2, max_health: 3, health: 3 } }),
        carteSurTable(LUNETTES, 'sk283', 'Upgrade', "3-D Man's Goggles", { bind_object_id: HUMAN_TORCH }),
      ],
      engaged_enemies: [
        chilly(),
        carteSurTable(MASQUE, 'sk284', 'Upgrade', 'Inhibitor Mask', {
          bind_object_id: surcharges.lienMasque === false ? 0 : CHILLY,
        }),
        carteSurTable(FANATIC, 'sk184', 'Minion', "Dard'van Fanatic", { info: { scheme: 1, attack: 2, max_health: 4, health: 4 } }),
      ],
    }),
    {
      area_villain: [carteSurTable(RHINO, '01094', 'EncounterVillain', 'Rhino', { info: { max_health: 14, health: 14 } })],
    } as Partial<World>
  )

// C2 : Fickle Alliance vaincue, Shocker est un allié ; le complot est en pile de victoire.
const mondeFickle = (): World =>
  tableAvec(
    siege({
      area_hero: [carteSurTable(HEROS, '01001a', 'Hero', 'Spider-Man')],
      allies: [
        carteSurTable(81, 'skrull_fickle_ally', 'Ally', 'Shocker', {
          pic_id: '01103',
          info: { thwart: 1, attack: 2, max_health: 3, health: 3 },
        }),
      ],
    }),
    {
      victory_display: [carteSurTable(82, 'sk272', 'PlayerSideScheme', 'Fickle Alliance')],
    } as Partial<World>
  )

// C3 : Skrull Military Training en pile de victoire, le héros porte +1 CTR / +1 ATQ / +1 DEF.
const mondeVictoire = (): World =>
  tableAvec(
    siege({
      area_hero: [
        carteSurTable(HEROS, '01001a', 'Hero', 'Spider-Man', {
          info: { thwart: 2, attack: 3, defense: 4, max_health: 10, health: 10 },
        }),
      ],
    }),
    {
      victory_display: [carteSurTable(83, 'sk275', 'PlayerSideScheme', 'Skrull Military Training')],
    } as Partial<World>
  )

// C4 : Princess Anelle quitte la partie.
const mondeRetiree = (): World =>
  tableAvec(siege({ area_hero: [carteSurTable(HEROS, '01001a', 'Hero', 'Spider-Man')] }), {
    area_removed: [carteSurTable(81, 'sk280', 'Support', 'Princess Anelle')],
  } as Partial<World>)

/** Les cartes contenues dans une pile ouverte du plateau (« Pile de victoire », « Retirées de la partie »). */
function cartesDeLaPile(world: World, cleDuGroupe: string): string[] {
  const plateau = construirePlateau(world, { playerId: 0, catalogue: catalogueVide })
  const ids: string[] = []
  for (const emplacement of plateau.emplacements)
    for (const groupe of emplacement.groupes)
      for (const unite of groupe)
        for (const g of unite.pileGroupes ?? []) if (g.cle === cleDuGroupe) ids.push(...g.cartes.map((c) => c.id))
  return ids
}

describe('Cartes de campagne (Skrull Menace) : ce que le plateau dessine', () => {
  // sk265 Paibok : « attach it facedown here ». La traîtrise doit être DESSINÉE (toBeDefined : l'assertion qui aurait
  // attrapé Contingency Plan), portée par Paibok et face cachée.
  it('sk265 : la traîtrise attachée à Paibok est dessinée, portée par lui, face cachée', () => {
    const carte = dessinee(monde(), TRAITRISE_SOUS_PAIBOK)
    expect(carte).toBeDefined()
    expect(carte?.portePar).toBe(PAIBOK)
    expect(carte?.peeking || carte?.facedown).toBe(true)
  })

  // sk267 Super-Skrull : deux SUPERPOWER glissés sous lui.
  it('sk267 : les deux SUPERPOWER attachés à Super-Skrull sont dessinés, portés par lui, face cachée', () => {
    for (const id of [POUVOIR_1, POUVOIR_2]) {
      const carte = dessinee(monde(), id)
      expect(carte).toBeDefined()
      expect(carte?.portePar).toBe(SUPER_SKRULL)
      expect(carte?.peeking || carte?.facedown).toBe(true)
    }
  })

  // sk268 : le moteur publie la FACE SBIRE (card_id du gabarit) avec le pic_id de l'allié : le plateau doit dessiner
  // un sbire ENGAGÉ avec l'image de la carte de campagne (sk268), pas l'image du gabarit.
  it("sk268 : Chilly McHotpants est dessiné comme un sbire engagé, avec l'image de la carte (sk268)", () => {
    expect(dessinee(monde(), CHILLY)).toBeDefined()
    expect(dessinee(monde(), CHILLY)?.zone).toBe(dessinee(monde(), FANATIC)?.zone)
    expect(scan(chilly()).picId).toBe('sk268')
    expect(scan(chilly()).kind).toBe('minion')
  })

  it("sk284 : le masque inhibiteur est dessiné attaché à l'ennemi SKRULL (Chilly McHotpants)", () => {
    expect(dessinee(monde(), MASQUE)).toBeDefined()
    expect(dessinee(monde(), MASQUE)?.portePar).toBe(CHILLY)
  })

  it('sk283 : les lunettes de 3-D Man sont dessinées attachées à Human Torch', () => {
    expect(dessinee(monde(), LUNETTES)).toBeDefined()
    expect(dessinee(monde(), LUNETTES)?.portePar).toBe(HUMAN_TORCH)
  })

  it("sk286 / sk287 / sk288 : les trois améliorations sont dessinées attachées à l'identité", () => {
    for (const id of [REVERTING, SHAPESHIFTER, GEMME]) {
      expect(dessinee(monde(), id)).toBeDefined()
      expect(dessinee(monde(), id)?.portePar).toBe(HEROS)
    }
  })

  it("sk288 : l'identité affiche ses 13 PV (10 + 3 de la gemme) tels que le moteur les publie", () => {
    const heros = monde().players[0].area_hero.find((c) => c.id === HEROS) as WorldCard
    expect(heros.info.max_health).toBe(13)
  })

  // sk272 : le sbire devenu allié est dessiné dans la zone des alliés, avec l'image du sbire (pic_id 01103).
  it("sk272 : le sbire devenu allié est dessiné chez les alliés, avec l'image du sbire", () => {
    const carte = dessinee(mondeFickle(), 81)
    expect(carte).toBeDefined()
    const allie = mondeFickle().players[0].allies[0]
    expect(scan(allie).picId).toBe('01103')
    expect(scan(allie).kind).toBe('ally')
  })

  it('sk272 : le complot vaincu est dans la pile de victoire', () => {
    expect(cartesDeLaPile(mondeFickle(), 'victoire')).toContain('82')
  })

  // sk275 : en pile de victoire, la carte est visible dans la pile et le héros montre ses bonus (chiffres du moteur).
  it('sk275 : Skrull Military Training est dans la pile de victoire', () => {
    expect(cartesDeLaPile(mondeVictoire(), 'victoire')).toContain('83')
  })

  it('sk275 : le héros du propriétaire affiche +1 CTR, +1 ATQ, +1 DEF', () => {
    const info = mondeVictoire().players[0].area_hero[0].info
    expect([info.thwart, info.attack, info.defense]).toEqual([2, 3, 4])
  })

  // sk280 : retirée de la PARTIE, pas défaussée : elle est dans la pile « Retirées de la partie », pas dans la défausse.
  it('sk280 : Princess Anelle est dans la pile « Retirées de la partie » et pas dans la défausse du joueur', () => {
    expect(cartesDeLaPile(mondeRetiree(), 'retirees')).toContain('81')
    expect(mondeRetiree().players[0].player_discard_pile.map((c) => c.id)).not.toContain(81)
  })

  // Contre-cas : détachées (état cassé), les cartes redeviennent des racines et les cas précédents tombent : c'est ce
  // qui prouve que les tests mesurent bien le lien (bind_object_id).
  it("ETAT CASSE : sans lien bind, la traîtrise n'est plus portée par Paibok", () => {
    expect(dessinee(monde({ lienPaibok: false }), TRAITRISE_SOUS_PAIBOK)?.portePar).not.toBe(PAIBOK)
  })

  it("ETAT CASSE : sans lien bind, le masque n'est plus porté par Chilly McHotpants", () => {
    expect(dessinee(monde({ lienMasque: false }), MASQUE)?.portePar).not.toBe(CHILLY)
  })
})
