// Signale en jeu (Alison Blaire, Dazzler) : « quand je cherche une chanson, il
// me montre juste les noms, pas les cartes, je ne sais pas ce qu'elles font ».
//
// Le moteur n'y peut rien — `AskChooseOneText` ne transporte que du texte. Mais
// le descripteur, lui, contient le deck en entier : la carte est LA, il ne
// manquait que le rapprochement par le nom.

import { describe, expect, it } from 'vitest'
import { catalogueVide } from './catalogue'
import { carteDeCampagneParOption, carteDuSchemaCampagneParOption, carteNommeeParOption, cartesDuLotParOption, cleNomCarte, indexerCartesMondeParNom } from './option-carte'
import type { Option } from './ask'
import type { WorldCard } from './world'

function carte(id: number, name: string, cardId: string): WorldCard {
  return {
    id,
    is_ready: true,
    // Une carte du DECK : le moteur ne la montre a personne.
    is_face_up: false,
    visible_for_players: [],
    bind_object_id: 0,
    name,
    info: {},
    traits: {},
    buffs: {},
    card_id: cardId,
    pic_id: cardId,
    down_card_ids: ['player'],
    card_type: 'Event',
    cost: 2,
    resources: [],
  }
}

function option(name: string, bindId = 0): Option {
  return {
    id: 7,
    name,
    bind_id: bindId,
    bind_player_id: 0,
    all_legal_targets: [],
    target_num_range: [0, 0],
    target_payment: {},
    select_rule: '',
    target_must_include_traits: [],
    failure_reason: '',
    is_search: false,
  }
}

const CHANSONS = new Map<number, WorldCard>([
  [61, carte(61, '"Beautiful Dreamer"', 'dz004')],
  [62, carte(62, '"Beauty and the Beast"', 'dz003')],
  [9, carte(9, 'Alison Blaire', 'dz001b')],
])

describe('cleNomCarte', () => {
  it('ignore les guillemets, la casse et les espaces en trop', () => {
    expect(cleNomCarte('  "Beautiful   Dreamer" ')).toBe(cleNomCarte('beautiful dreamer'))
  })
})

describe('carteNommeeParOption', () => {
  const parNom = indexerCartesMondeParNom(CHANSONS)

  it('retrouve la carte du deck que l’option nomme', () => {
    const trouvee = carteNommeeParOption(option('"Beautiful Dreamer"'), parNom, 0, catalogueVide)
    expect(trouvee?.codeCarte).toBe('dz004')
    expect(trouvee?.name).toBe('"Beautiful Dreamer"')
  })

  it('la montre de FACE : la question la revele deja, en texte', () => {
    // Sans ce forcage, toScanCard rendrait le DOS du deck (visible_for_players
    // est vide) et le joueur verrait deux dos identiques.
    const trouvee = carteNommeeParOption(option('"Beauty and the Beast"'), parNom, 0, catalogueVide)
    expect(trouvee?.facedown).toBeFalsy()
    expect(trouvee?.imageUrl).toContain('dz003')
  })

  it('ne montre rien pour une option qui ne nomme aucune carte', () => {
    expect(carteNommeeParOption(option('Cancel'), parNom, 0, catalogueVide)).toBeUndefined()
  })

  it('ne redouble pas la carte PORTEUSE de l’option', () => {
    // Elle est deja sur la table, et son nom est deja sous le bouton.
    expect(carteNommeeParOption(option('Alison Blaire', 9), parNom, 0, catalogueVide)).toBeUndefined()
  })

  it('ignore les noms trop courts pour designer une carte', () => {
    // « R », « B », « 2 »... : types de ressource et nombres passent par le
    // meme AskChooseOneText que les cartes.
    const parNomCourt = indexerCartesMondeParNom(new Map([[1, carte(1, 'R', 'x')]]))
    expect(carteNommeeParOption(option('R'), parNomCourt, 0, catalogueVide)).toBeUndefined()
  })
})

describe('cartesDuLotParOption : le lot d\'un role (Mutant Genesis, 22/10/2026)', () => {
  it('montre les cinq ameliorations du role choisi, sans les chercher dans le monde', () => {
    // ⚠ Le moteur emet le nom avec un souligne a la place de l'espace
    // (GetDisplayName(remove_space=True)) : c'est « Role:_Brawler » qui arrive,
    // pas « Role: Brawler ». Le test doit refleter l'entree REELLE, sinon il
    // verdit sur un libelle que la production ne produit jamais.
    const lot = cartesDuLotParOption(option('Role:_Brawler', 99), 0, catalogueVide)
    expect(lot?.map((c) => c.codeCarte)).toEqual(['32176', '32177', '32178', '32179', '32180'])
  })

  it('tolere aussi le libelle avec espace (Role: Brawler)', () => {
    const lot = cartesDuLotParOption(option('Role: Brawler', 99), 0, catalogueVide)
    expect(lot?.map((c) => c.codeCarte)).toEqual(['32176', '32177', '32178', '32179', '32180'])
  })

  it('ne dit rien d\'une option qui n\'est pas un role', () => {
    expect(cartesDuLotParOption(option('Role: Inconnu'), 0, catalogueVide)).toBeUndefined()
    expect(cartesDuLotParOption(option('Defense'), 0, catalogueVide)).toBeUndefined()
  })
})

describe('carteDuSchemaCampagneParOption : « Put "X" into play » (NeXt Evolution)', () => {
  it('montre la manigance nommee, meme recue avec des soulignes et des guillemets', () => {
    // Forme REELLE emise par le moteur (GetDisplayName(remove_space=True)).
    const carte = carteDuSchemaCampagneParOption(option('Put_"Assemble_the_Team"_into_play', 99), 0, catalogueVide)
    expect(carte?.codeCarte).toBe('40190a')
  })

  it('tolere aussi la forme avec espaces', () => {
    const carte = carteDuSchemaCampagneParOption(option('Put "Mission Prep" into play'), 0, catalogueVide)
    expect(carte?.codeCarte).toBe('40193a')
  })

  it('ne dit rien d\'une option qui ne nomme pas une manigance de campagne connue', () => {
    expect(carteDuSchemaCampagneParOption(option('Put "Autre chose" into play'), 0, catalogueVide)).toBeUndefined()
    expect(carteDuSchemaCampagneParOption(option('Role: Brawler'), 0, catalogueVide)).toBeUndefined()
  })
})

describe('carteDeCampagneParOption : mise en place de MojoMania (28/10/2026)', () => {
  it('« Reveal Longshot » montre Longshot, meme recu avec des soulignes, sans qu\'il soit dans le monde', () => {
    const carteLongshot = carteDeCampagneParOption(option('Reveal_Longshot', 99), new Map(), 0, catalogueVide)
    expect(carteLongshot?.codeCarte).toBe('39071')
    const melange = carteDeCampagneParOption(option('Shuffle_Longshot_into_the_encounter_deck', 99), new Map(), 0, catalogueVide)
    expect(melange?.codeCarte).toBe('39071')
  })

  it('« Put <carte> into play under your control » retrouve la carte du deck par son nom', () => {
    const parNom = indexerCartesMondeParNom(new Map([[1, carte(1, 'Stark Tower', '01034')]]))
    const montree = carteDeCampagneParOption(option('Put_Stark_Tower_into_play_under_your_control', 99), parNom, 0, catalogueVide)
    expect(montree?.codeCarte).toBe('01034')
  })

  it("ne dit rien d'une option qui n'en est pas une, ni d'une carte absente du monde", () => {
    expect(carteDeCampagneParOption(option('Defense'), new Map(), 0, catalogueVide)).toBeUndefined()
    expect(carteDeCampagneParOption(option('Put_Inconnue_into_play_under_your_control'), new Map(), 0, catalogueVide)).toBeUndefined()
  })
})
