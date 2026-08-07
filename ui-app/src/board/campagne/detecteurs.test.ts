// Les formes testées ici ne sont pas inventées : elles reprennent des
// descripteurs CAPTURÉS sur des parties réelles de Rise of Red Skull, montées à
// blanc en mode campagne (sonde `ToDescriptor.World` après `GameSetup`).
//
// Les trois relevés qui fondent ces cas :
//
//   Zola + Puzzle.PutIntoPlay('04122') + Puzzle.Counter('04112b','delay',3)
//     area_schemes_side : id=74 bind=0  04122 EncounterSideScheme {k_threat:4}
//                         id=8  bind=74 03002 Ally
//     area_schemes_main : id=48 bind=0  04112b MainScheme {c_delay:3, ...}
//
//   Taskmaster (mise en place seule)
//     area_set_aside    : 04097..04100, tous Ally, bind=0
//     joueur.area_hero  : 03001b AlterEgo {max_health:11, health:11}
//
//   Crossbones + Puzzle.PutIntoPlay('04072')
//     area_villain      : id=51 bind=0  04058 EncounterVillain
//                         id=66 bind=51 04072 Attachment (Laser Rifle)
import { describe, expect, it } from 'vitest'
import type { World } from '../world'
import {
  cartesDansZone,
  cartesDuJoueurParmi,
  cartesEnJeu,
  cartesEnPileVictoire,
  compterTrait,
  cartesSousComplot,
  cleCarnet,
  complotEnJeu,
  compteurManigance,
  conditionRemplie,
  detecter,
  joueurElimine,
  joueursEngages,
  pvRestants,
  type ChampVictoire,
} from './detecteurs'

function carte(id: number, cardId: string, extra: Record<string, unknown> = {}) {
  return {
    id,
    card_id: cardId,
    card_type: 'Ally',
    name: cardId,
    bind_object_id: 0,
    is_ready: true,
    is_face_up: true,
    visible_for_players: [0],
    info: {},
    traits: {},
    buffs: {},
    pic_id: cardId,
    down_card_ids: [],
    cost: 0,
    resources: [],
    ...extra,
  }
}

function joueur(extra: Record<string, unknown> = {}) {
  return {
    area_hero: [],
    allies: [],
    supports: [],
    player_deck: [],
    player_discard_pile: [],
    dealt_encounter_cards: [],
    hand_cards: [],
    engaged_enemies: [],
    set_aside_nemesis_sets: [],
    set_aside_deck: [],
    additional_deck: [],
    additional_discard_pile: [],
    obligations_area: [],
    environment_area: [],
    resources: '',
    is_eliminated: false,
    ...extra,
  }
}

function monde(extra: Record<string, unknown> = {}): World {
  return {
    render_id: 1,
    round_id: 1,
    phase: '',
    prompt: '',
    event_name: '',
    area_schemes_main: [],
    main_schemes_deck: [],
    area_schemes_side: [],
    additional_decks: [],
    additional_discard_piles: [],
    area_villain: [],
    villain_deck: [],
    encounter_deck: [],
    encounter_discard_pile: [],
    area_boost: [],
    area_environment: [],
    area_evidence: [],
    area_rule: [],
    area_processing: [],
    area_revealing: [],
    area_resources: [],
    area_removed: [],
    area_insert: [],
    area_set_aside: [],
    victory_display: [],
    area_status_cards: [],
    players: [joueur()],
    active_card_ids: [],
    ...extra,
  } as unknown as World
}

const EXPERIMENTALES = ['04072', '04073', '04074', '04075']
const CAPTIFS = ['04097', '04098', '04099', '04100']

describe('cartesEnJeu — armes expérimentales de Crossbones', () => {
  it("compte une arme attachée au vilain (forme mesurée sur Crossbones)", () => {
    const m = monde({
      area_villain: [
        carte(51, '04058', { card_type: 'EncounterVillain' }),
        carte(66, '04072', { card_type: 'Attachment', bind_object_id: 51 }),
      ],
    })
    expect(cartesEnJeu(m, EXPERIMENTALES)).toEqual(['04072'])
  })

  it('compte une arme déjà défaussée : elle est bien entrée en jeu', () => {
    const m = monde({
      encounter_discard_pile: [carte(90, '04074', { card_type: 'Attachment' })],
    })
    expect(cartesEnJeu(m, EXPERIMENTALES)).toEqual(['04074'])
  })

  it("ne compte PAS une arme qui dort encore dans la zone mise de côté", () => {
    const m = monde({
      area_set_aside: EXPERIMENTALES.map((id, i) => carte(80 + i, id, { card_type: 'Attachment' })),
    })
    expect(cartesEnJeu(m, EXPERIMENTALES)).toEqual([])
  })

  it("ne compte PAS une arme mélangée au deck de rencontre sans être révélée", () => {
    const m = monde({ encounter_deck: [carte(91, '04075', { card_type: 'Attachment' })] })
    expect(cartesEnJeu(m, EXPERIMENTALES)).toEqual([])
  })

  // RÉGRESSION. Relevé sur une vraie partie de Crossbones jouée jusqu'à la
  // victoire : le deck des Armes Expérimentales est un deck ADDITIONNEL, et
  // seule Energy Shield (04073) était attachée au vilain. La première version
  // du détecteur déclarait les quatre entrées en jeu — la campagne aurait
  // reçu trois armes de trop dans chacun de ses quatre scénarios suivants.
  it("ne compte que l'arme réellement attachée, pas le deck additionnel qui attend", () => {
    const m = monde({
      area_villain: [
        carte(51, '04058', { card_type: 'EncounterVillain' }),
        carte(64, '04073', { card_type: 'Attachment', bind_object_id: 51 }),
      ],
      additional_decks: [
        [
          carte(70, '04075', { card_type: 'Attachment', bind_object_id: 51 }),
          carte(71, '04074', { card_type: 'Attachment', bind_object_id: 51 }),
          carte(72, '04072', { card_type: 'Attachment', bind_object_id: 51 }),
        ],
      ],
    })
    expect(cartesEnJeu(m, EXPERIMENTALES)).toEqual(['04073'])
  })

  it("rend les identifiants dans l'ordre du livret, pas dans celui des zones", () => {
    const m = monde({
      encounter_discard_pile: [carte(1, '04075'), carte(2, '04073')],
      area_villain: [carte(3, '04072')],
    })
    expect(cartesEnJeu(m, EXPERIMENTALES)).toEqual(['04072', '04073', '04075'])
  })
})

describe("compteurManigance — pions retard de l'Homme Absorbant", () => {
  it('lit c_delay sur la manigance principale (mesuré à 3 sur Zola)', () => {
    const m = monde({
      area_schemes_main: [
        carte(48, '04112b', {
          card_type: 'MainScheme',
          info: { c_delay: 3, k_threat: 2, target_threat: 6 },
        }),
      ],
    })
    expect(compteurManigance(m, 'delay')).toBe(3)
  })

  it('ne confond pas le compteur c_ avec le jeton k_ de la menace', () => {
    const m = monde({
      area_schemes_main: [carte(48, '04079b', { card_type: 'MainScheme', info: { k_threat: 7 } })],
    })
    expect(compteurManigance(m, 'delay')).toBe(0)
  })

  it('prend le maximum quand plusieurs manigances principales coexistent', () => {
    const m = monde({
      area_schemes_main: [
        carte(1, '04112b', { card_type: 'MainScheme', info: { c_delay: 2 } }),
        carte(2, '04113b', { card_type: 'MainScheme', info: { c_delay: 5 } }),
      ],
    })
    expect(compteurManigance(m, 'delay')).toBe(5)
  })
})

describe('cartesDuJoueurParmi — alliés secourus de Taskmaster', () => {
  it("ne compte aucun captif tant qu'ils sont dans la zone mise de côté du scénario", () => {
    const m = monde({
      area_set_aside: CAPTIFS.map((id, i) => carte(84 + i, id)),
      players: [joueur()],
    })
    expect(cartesDuJoueurParmi(m, 0, CAPTIFS)).toEqual([])
  })

  it('compte un allié passé dans le deck du joueur', () => {
    const m = monde({ players: [joueur({ player_deck: [carte(84, '04098')] })] })
    expect(cartesDuJoueurParmi(m, 0, CAPTIFS)).toEqual(['04098'])
  })

  it("compte un allié en jeu comme un allié en main", () => {
    const m = monde({
      players: [joueur({ allies: [carte(84, '04097')], hand_cards: [carte(85, '04100')] })],
    })
    expect(cartesDuJoueurParmi(m, 0, CAPTIFS)).toEqual(['04097', '04100'])
  })

  it("n'attribue pas au joueur 0 ce que le joueur 1 a secouru", () => {
    const m = monde({
      players: [joueur(), joueur({ allies: [carte(84, '04099')] })],
    })
    expect(cartesDuJoueurParmi(m, 0, CAPTIFS)).toEqual([])
    expect(cartesDuJoueurParmi(m, 1, CAPTIFS)).toEqual(['04099'])
  })
})

describe('joueursEngages — fin du scénario de Zola', () => {
  it('rend les indices des joueurs qui ont encore un ennemi en face', () => {
    const m = monde({
      players: [
        joueur({ engaged_enemies: [carte(1, '04101', { card_type: 'Minion' })] }),
        joueur(),
        joueur({ engaged_enemies: [carte(2, '04114', { card_type: 'Minion' })] }),
      ],
    })
    expect(joueursEngages(m)).toEqual(['0', '2'])
  })

  it('rend une liste vide quand la table est nette', () => {
    expect(joueursEngages(monde({ players: [joueur(), joueur()] }))).toEqual([])
  })
})

describe("cartesSousComplot — Prison d'Hydra", () => {
  // Forme mesurée : la prison et l'allié qu'elle retient sont dans LA MÊME
  // zone, l'allié portant le bind_object_id de la prison.
  const AVEC_PRISON = monde({
    area_schemes_side: [
      carte(74, '04122', { card_type: 'EncounterSideScheme', info: { k_threat: 4 } }),
      carte(8, '03002', { card_type: 'Ally', bind_object_id: 74 }),
    ],
  })

  it("rend les alliés que la prison retient encore", () => {
    expect(cartesSousComplot(AVEC_PRISON, '04122', 'Ally')).toEqual(['03002'])
  })

  it('ne rend rien si la prison a été déjouée', () => {
    const m = monde({ area_schemes_side: [] })
    expect(cartesSousComplot(m, '04122', 'Ally')).toEqual([])
    expect(complotEnJeu(m, '04122')).toBe(false)
  })

  it("ne prend pas une carte liée à un AUTRE complot annexe", () => {
    const m = monde({
      area_schemes_side: [
        carte(74, '04122', { card_type: 'EncounterSideScheme' }),
        carte(75, '04123', { card_type: 'EncounterSideScheme' }),
        carte(9, '03014', { card_type: 'Ally', bind_object_id: 75 }),
      ],
    })
    expect(cartesSousComplot(m, '04122', 'Ally')).toEqual([])
  })

  it('filtre sur le type demandé : un attachement sous la prison ne compte pas', () => {
    const m = monde({
      area_schemes_side: [
        carte(74, '04122', { card_type: 'EncounterSideScheme' }),
        carte(10, '04117', { card_type: 'Attachment', bind_object_id: 74 }),
      ],
    })
    expect(cartesSousComplot(m, '04122', 'Ally')).toEqual([])
  })
})

describe('pvRestants — campagne experte', () => {
  it('lit health sur la carte identité (mesuré 11/11 sur Steve Rogers)', () => {
    const m = monde({
      players: [
        joueur({
          area_hero: [carte(1, '03001b', { card_type: 'AlterEgo', info: { health: 7, max_health: 11 } })],
        }),
      ],
    })
    expect(pvRestants(m, 0)).toBe(7)
  })

  it('plafonne aux PV imprimés, comme le demande la p17 du livret', () => {
    const m = monde({
      players: [
        joueur({
          area_hero: [carte(1, '03001b', { card_type: 'AlterEgo', info: { health: 15, max_health: 11 } })],
        }),
      ],
    })
    expect(pvRestants(m, 0)).toBe(11)
  })

  it("ne reporte rien pour un héros éliminé : il revient à pleins PV", () => {
    const m = monde({
      players: [
        joueur({
          is_eliminated: true,
          area_hero: [carte(1, '03001b', { card_type: 'AlterEgo', info: { health: 0, max_health: 11 } })],
        }),
      ],
    })
    expect(pvRestants(m, 0)).toBeUndefined()
    expect(joueurElimine(m, 0)).toBe(true)
  })

  it('rend 0 et non undefined quand un héros survit à 0 PV', () => {
    const m = monde({
      players: [
        joueur({
          area_hero: [carte(1, '03001b', { card_type: 'AlterEgo', info: { health: 0, max_health: 11 } })],
        }),
      ],
    })
    expect(pvRestants(m, 0)).toBe(0)
  })
})

describe('detecter — la valeur écrite dans le carnet', () => {
  const champListe: ChampVictoire = {
    cle: 'Experimental Weapons added to encounter deck',
    type: 'auto',
    format: 'liste',
    detection: 'cartes_en_jeu',
    libelle: '',
    options: EXPERIMENTALES,
  }

  it('joint les identifiants par « ; », comme le moteur les relit', () => {
    const m = monde({
      area_villain: [carte(1, '04072'), carte(2, '04074')],
    })
    expect(detecter(champListe, m, 0)).toBe('04072;04074')
  })

  it("n'écrit RIEN plutôt qu'une chaîne vide quand il n'y a rien à noter", () => {
    expect(detecter(champListe, monde(), 0)).toBeUndefined()
  })

  it('rend le compteur en texte', () => {
    const champ: ChampVictoire = {
      cle: 'Number of delay counters on main scheme',
      type: 'auto',
      format: 'int',
      detection: 'compteur_manigance',
      parametres: { compteur: 'delay' },
      libelle: '',
    }
    const m = monde({
      area_schemes_main: [carte(48, '04112b', { card_type: 'MainScheme', info: { c_delay: 4 } })],
    })
    expect(detecter(champ, m, 0)).toBe('4')
  })

  it('rend undefined pour une détection inconnue au lieu de deviner', () => {
    const champ: ChampVictoire = { cle: 'X', type: 'auto', detection: 'inexistant', libelle: '' }
    expect(detecter(champ, monde(), 0)).toBeUndefined()
  })
})

describe('conditionRemplie — la récompense conditionnelle de Zola', () => {
  const champ: ChampVictoire = {
    cle: 'Basic Upgrade',
    type: 'choix',
    condition: 'complot_absent',
    parametres: { complot: '04122' },
    libelle: '',
  }

  it("autorise le passage en version supérieure quand la prison est tombée", () => {
    expect(conditionRemplie(champ, monde())).toBe(true)
  })

  it("le refuse tant que la prison tient", () => {
    const m = monde({
      area_schemes_side: [carte(74, '04122', { card_type: 'EncounterSideScheme' })],
    })
    expect(conditionRemplie(champ, m)).toBe(false)
  })

  it('un champ sans condition passe toujours', () => {
    expect(conditionRemplie({ cle: 'X', type: 'auto', libelle: '' }, monde())).toBe(true)
  })

  it("masque un champ dont la condition n'est pas comprise, plutôt que de l'accorder", () => {
    const inconnu: ChampVictoire = { cle: 'X', type: 'choix', condition: 'jamais_vu', libelle: '' }
    expect(conditionRemplie(inconnu, monde())).toBe(false)
  })
})

// --- Sinister Motives -------------------------------------------------------
// Formes mesurées sur une mise en place de Venom en mode campagne :
//   area_villain     : 27073 Venom, traits { t_SYMBIOTE: 1 }
//   J0.player_deck   : 03004 Heroic Strike, traits { t_ATTACK: 1 }
//   victory_display  : vide en début de partie
const SERVICES = ['27176', '27177', '27178', '27179', '27180']
const SIX = ['27094', '27095', '27096', '27097', '27098', '27099']

describe('cartesEnPileVictoire — Community Service', () => {
  it('rend la manigance annexe déjouée', () => {
    const m = monde({
      victory_display: [carte(30, '27178', { card_type: 'EncounterSideScheme' })],
    })
    expect(cartesEnPileVictoire(m, SERVICES)).toEqual(['27178'])
  })

  it("ne rend rien pour une manigance encore en jeu", () => {
    const m = monde({
      area_schemes_side: [carte(30, '27178', { card_type: 'EncounterSideScheme' })],
    })
    expect(cartesEnPileVictoire(m, SERVICES)).toEqual([])
  })
})

describe('cartesDansZone — les Sinistres Six encore debout', () => {
  // Le livret dit « note le nom de chaque vilain EN JEU » : ceux qui tiennent
  // encore reviennent en sbires au scénario 5. C'est une pénalité.
  it('rend les vilains toujours en jeu à la fin', () => {
    const m = monde({
      area_villain: [
        carte(10, '27095', { card_type: 'EncounterVillain' }),
        carte(11, '27099', { card_type: 'EncounterVillain' }),
      ],
    })
    expect(cartesDansZone(m, 'area_villain', SIX)).toEqual(['27095', '27099'])
  })

  it("ne rend rien quand les six sont tombés", () => {
    const m = monde({ area_villain: [], victory_display: SIX.map((id, i) => carte(20 + i, id)) })
    expect(cartesDansZone(m, 'area_villain', SIX)).toEqual([])
  })
})

describe('compterTrait — les cartes ILLUSION de Mysterio', () => {
  it('compte le trait dans le deck, la main et la défausse', () => {
    const m = monde({
      players: [
        joueur({
          player_deck: [carte(1, '27084', { traits: { t_ILLUSION: 1 } })],
          hand_cards: [carte(2, '27085', { traits: { t_ILLUSION: 1 } })],
          player_discard_pile: [carte(3, '27086', { traits: { t_ILLUSION: 1 } })],
        }),
      ],
    })
    expect(compterTrait(m, 'ILLUSION')).toBe(3)
  })

  it('additionne les joueurs, et ignore les autres traits', () => {
    const m = monde({
      players: [
        joueur({ player_deck: [carte(1, '27084', { traits: { t_ILLUSION: 1 } })] }),
        joueur({
          player_deck: [
            carte(2, '27085', { traits: { t_ILLUSION: 1 } }),
            carte(3, '03004', { traits: { t_ATTACK: 1 } }),
          ],
        }),
      ],
    })
    expect(compterTrait(m, 'ILLUSION')).toBe(2)
  })

  it("ne compte pas les cartes en jeu : le livret parle des decks", () => {
    const m = monde({
      players: [joueur({ allies: [carte(1, '27084', { traits: { t_ILLUSION: 1 } })] })],
    })
    expect(compterTrait(m, 'ILLUSION')).toBe(0)
  })
})

describe('cleCarnet', () => {
  it('préfixe les champs par joueur, comme le moteur les cherche', () => {
    expect(cleCarnet({ cle: 'Tech Upgrade', type: 'choix', parJoueur: true, libelle: '' }, 1))
      .toBe('Player 2 Tech Upgrade')
  })

  it('laisse les champs communs tels quels', () => {
    expect(cleCarnet({ cle: 'Reputation Track', type: 'auto', libelle: '' }, 2))
      .toBe('Reputation Track')
  })
})
