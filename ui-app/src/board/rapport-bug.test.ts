// Ce que le rapport doit contenir, et ce qu'il ne doit JAMAIS taire.
//
// Le piege principal : le journal est stocke du PLUS RECENT AU PLUS ANCIEN
// (ajouterNouvellesEntrees fait un unshift). Une portee « les 20 dernieres »
// ecrite avec slice(-20) rendrait le DEBUT de la partie, silencieusement.
import { describe, expect, it } from 'vitest'
import {
  construireRapport,
  entreesDeLaPortee,
  nomFichierRapport,
  rapportEnTexte,
} from './rapport-bug'
import { MAX_ENTREES, type EntreeHistorique } from './HistoriquePartie'
import type { Demande } from './ask'
import type { World, WorldCard, WorldPlayer } from './world'

const ZONES = {
  area_schemes_main: [], main_schemes_deck: [], area_schemes_side: [],
  additional_decks: [], additional_discard_piles: [], area_villain: [],
  villain_deck: [], encounter_deck: [], encounter_discard_pile: [],
  area_boost: [], area_environment: [], area_evidence: [], area_rule: [],
  area_processing: [], area_revealing: [], area_resources: [],
  area_removed: [], area_insert: [], area_set_aside: [],
  victory_display: [], area_status_cards: [], players: [],
  active_card_ids: [],
}

function carte(
  id: number,
  nom: string,
  cardId: string,
  type: string,
  info: Record<string, number> = {}
): WorldCard {
  return {
    id, is_ready: true, is_face_up: true, visible_for_players: [0],
    bind_object_id: 0, name: nom, info, traits: {}, buffs: {},
    card_id: cardId, pic_id: cardId, down_card_ids: [], card_type: type,
    cost: 0, resources: [],
  }
}

function siege(surcharge: Partial<WorldPlayer> = {}): WorldPlayer {
  return {
    area_hero: [], allies: [], supports: [], player_deck: [],
    player_discard_pile: [], dealt_encounter_cards: [], hand_cards: [],
    engaged_enemies: [], set_aside_nemesis_sets: [], set_aside_deck: [],
    additional_deck: [], additional_discard_pile: [], obligations_area: [],
    environment_area: [], resources: '', is_eliminated: false, ...surcharge,
  }
}

const CONTEXTE = { horodatage: '2026-08-12T21:00:00.000Z', siege: 0 }

function monde(surcharge: Partial<World> = {}): World {
  return {
    render_id: 43, round_id: 3, phase: 'Player 1 Turn', prompt: '',
    event_name: 'PlayerOnEvent_Text', ...ZONES,
    area_schemes_main: [carte(48, 'None Shall Pass', '04079b', 'MainScheme', { k_threat: 2, target_threat: 12 })],
    area_villain: [carte(50, 'Absorbing Man', '04077a', 'EncounterVillain', { health: 14 })],
    ...surcharge,
  }
}

const entree = (round: number, titre: string, reste: Partial<EntreeHistorique> = {}): EntreeHistorique => ({
  cle: `${round}:${titre}`, type: 'text', renderId: round, round, phase: '', titre, ...reste,
})

describe('la portee', () => {
  // Le plus recent est en TETE : « les 20 dernieres » se prend au debut.
  const journal = [entree(3, 'c'), entree(3, 'b'), entree(2, 'a')]

  it('« recent » prend les 20 premieres, qui sont les plus recentes', () => {
    const long = Array.from({ length: 30 }, (_, i) => entree(3, `e${i}`))
    const pris = entreesDeLaPortee(long, 'recent', 3)
    expect(pris).toHaveLength(20)
    expect(pris[0]?.titre).toBe('e0')
  })

  it('« tour » ne garde que le round courant', () => {
    expect(entreesDeLaPortee(journal, 'tour', 3).map((e) => e.titre)).toEqual(['c', 'b'])
  })

  it('« partie » garde tout', () => {
    expect(entreesDeLaPortee(journal, 'partie', 3)).toHaveLength(3)
  })
})

describe('le rapport', () => {
  it('dit que le journal est tronque quand le tampon est plein', () => {
    const plein = Array.from({ length: MAX_ENTREES }, (_, i) => entree(3, `e${i}`))
    expect(construireRapport(monde(), undefined, plein, 'partie', CONTEXTE).tronque).toBe(true)
    expect(construireRapport(monde(), undefined, plein.slice(1), 'partie', CONTEXTE).tronque).toBe(false)
  })

  it('ne pretend jamais etre tronque sur une portee courte', () => {
    const plein = Array.from({ length: MAX_ENTREES }, (_, i) => entree(3, `e${i}`))
    expect(construireRapport(monde(), undefined, plein, 'recent', CONTEXTE).tronque).toBe(false)
  })

  it('donne a chaque carte son object id sous la forme visable en console', () => {
    const rapport = construireRapport(monde(), undefined, [], 'recent', CONTEXTE)
    const complot = rapport.table.cartes.find((c) => c.objet === 'c48')
    expect(complot).toMatchObject({
      objet: 'c48', card_id: '04079b', nom: 'None Shall Pass',
      zone: 'complot principal', menace: 2,
    })
  })

  it('recopie les points de vie du vilain', () => {
    const rapport = construireRapport(monde(), undefined, [], 'recent', CONTEXTE)
    expect(rapport.table.cartes.find((c) => c.objet === 'c50')).toMatchObject({ vie: 14, zone: 'vilain' })
  })

  it('garde le texte brut du journal, identifiants compris', () => {
    const journal = [entree(3, 'Klaw would deal 2 damage', { brut: '[(50,01113) Klaw] would deal 2 damage' })]
    const rapport = construireRapport(monde(), undefined, journal, 'recent', CONTEXTE)
    expect(rapport.journal[0]?.texte).toBe('[(50,01113) Klaw] would deal 2 damage')
  })

  it("retombe sur le texte affiche quand l'entree n'a pas de brut", () => {
    const rapport = construireRapport(monde(), undefined, [entree(3, 'Ball and Chain joue')], 'recent', CONTEXTE)
    expect(rapport.journal[0]?.texte).toBe('Ball and Chain joue')
  })

  it('rend la cible du journal sous forme d object id', () => {
    const journal = [entree(3, 'Klaw subit 2 degats', { type: 'damage', cibleId: 50 })]
    const rapport = construireRapport(monde(), undefined, journal, 'recent', CONTEXTE)
    expect(rapport.journal[0]?.cible).toBe('c50')
  })

  it('recopie la demande avec ses cibles legales et son cout', () => {
    const demande: Demande = {
      refus: [],
      prompt_text: 'Choisissez une action', event_name: 'WhenPlayerInTurn',
      show_cancel: true, ability_type: 'Hero_Response',
      options: [{
        id: 12, name: 'p_Play', bind_id: 57, bind_player_id: 0,
        all_legal_targets: [48, 50], target_num_range: [1, 1],
        target_payment: { 0: { cost: '2', payment: [{ effect_id: 91, res_text: 'physical' }], rule: [] } },
        select_rule: '', target_must_include_traits: [], failure_reason: '', is_search: false,
      }],
    }
    const rapport = construireRapport(monde(), demande, [], 'recent', CONTEXTE)
    expect(rapport.demande).toMatchObject({
      type: 'Hero_Response', evenement: 'WhenPlayerInTurn', annulable: true,
    })
    expect(rapport.demande?.options[0]).toMatchObject({
      id: 12, nom: 'Play', porteePar: 'c57', cibles: ['c48', 'c50'],
      nombreDeCibles: [1, 1], cout: '2', injouable: null,
    })
  })

  it('nomme la raison quand une option est injouable', () => {
    const demande: Demande = {
      refus: [],
      prompt_text: '', event_name: '', show_cancel: false, ability_type: '',
      options: [{
        id: 13, name: 'p_Attack', bind_id: 0, bind_player_id: 0,
        all_legal_targets: [], target_num_range: [0, 0], target_payment: {},
        select_rule: '', target_must_include_traits: [],
        failure_reason: 'not enough resources', is_search: false,
      }],
    }
    const rapport = construireRapport(monde(), demande, [], 'recent', CONTEXTE)
    expect(rapport.demande?.options[0]?.injouable).toBe('not enough resources')
  })

  it("rend une demande nulle quand le moteur n'attend rien", () => {
    expect(construireRapport(monde(), undefined, [], 'recent', CONTEXTE).demande).toBeNull()
  })

  it('nomme le mode campagne, le bac a sable et le nombre de sieges', () => {
    const table = monde({
      mode_sandbox: true,
      players: [siege({ area_hero: [carte(1, 'She-Hulk', '04001a', 'Hero', { health: 20 })] })],
    })
    const rapport = construireRapport(table, undefined, [], 'recent', {
      ...CONTEXTE, campagne: { id: 'trors-1', scenario: 'crossbones' },
    })
    expect(rapport.contexte).toMatchObject({
      sandbox: true, sieges: 1, round: 3, phase: 'Player 1 Turn', render_id: 43,
      campagne: { id: 'trors-1', scenario: 'crossbones' },
      scenario: 'None Shall Pass', vilain: 'Absorbing Man',
      heros: ['She-Hulk'],
    })
  })

  it('decrit la main de CHAQUE siege, pas seulement celui qui rapporte', () => {
    const table = monde({
      players: [
        siege({ hand_cards: [carte(60, 'Swinging Stone', '04083', 'Event')] }),
        siege({ hand_cards: [carte(61, 'Steel Kick', '04084', 'Event')] }),
      ],
    })
    const mains = construireRapport(table, undefined, [], 'recent', CONTEXTE).table.cartes.filter(
      (c) => c.zone === 'main'
    )
    expect(mains.map((c) => [c.objet, c.joueur])).toEqual([['c60', 0], ['c61', 1]])
  })

  it("nomme la fin de partie quand il y en a une", () => {
    const fini = monde({ game_over: true, game_over_reason: 'The Final Stage of the Villain was Defeated' })
    const rapport = construireRapport(fini, undefined, [], 'recent', CONTEXTE)
    expect(rapport.contexte.fin).toBe('The Final Stage of the Villain was Defeated')
  })
})

describe('la marque « corrigée à la main » (tâche 6)', () => {
  it("n'apparaît pas sur une partie ordinaire, jamais corrigée", () => {
    const rapport = construireRapport(monde(), undefined, [], 'recent', CONTEXTE)
    expect(rapport.contexte.corrigeeALaMain).toBe(false)
    expect(rapportEnTexte(rapport)).not.toContain('CORRIGÉE')
  })

  it("apparaît, avant même le corps du rapport, quand la partie a ete corrigee", () => {
    const rapport = construireRapport(monde({ corrigee_a_la_main: true }), undefined, [], 'recent', CONTEXTE)
    expect(rapport.contexte.corrigeeALaMain).toBe(true)
    const texte = rapportEnTexte(rapport)
    expect(texte).toContain('CORRIGÉE À LA MAIN')
    // « avant meme de lire » : la marque doit preceder le corps du rapport.
    expect(texte.indexOf('CORRIGÉE À LA MAIN')).toBeLessThan(texte.indexOf('--- CONTEXTE ---'))
  })
})

describe('les gestes manuels regroupes en fin de rapport (tâche 6)', () => {
  it("n'ajoute aucune section quand aucun geste manuel n'a eu lieu", () => {
    const journal = [entree(3, 'Klaw joue une carte', { type: 'card' })]
    const rapport = construireRapport(monde(), undefined, journal, 'partie', CONTEXTE)
    expect(rapport.gestesManuels).toHaveLength(0)
    expect(rapportEnTexte(rapport)).not.toContain('GESTES MANUELS')
  })

  it('reprend UNIQUEMENT les gestes manuels, pas tout le journal', () => {
    const journal = [
      entree(2, 'Klaw joue une carte', { type: 'card' }),
      entree(2, 'PV de Klaw fixes a la main', { type: 'manuel' }),
      entree(3, 'Menace ajustee a la main', { type: 'manuel' }),
      entree(3, 'She-Hulk attaque', { type: 'damage' }),
    ]
    const rapport = construireRapport(monde(), undefined, journal, 'partie', CONTEXTE)
    expect(rapport.gestesManuels).toHaveLength(2)
    expect(rapport.gestesManuels.map((g) => g.texte)).toEqual([
      'PV de Klaw fixes a la main',
      'Menace ajustee a la main',
    ])

    const texte = rapportEnTexte(rapport)
    const section = texte.split('--- GESTES MANUELS')[1]
    expect(section).toBeDefined()
    expect(section).toContain('PV de Klaw fixes a la main')
    expect(section).toContain('Menace ajustee a la main')
    expect(section).not.toContain('Klaw joue une carte')
    expect(section).not.toContain('She-Hulk attaque')
  })

  it('couvre TOUTE LA PARTIE, meme quand la portee choisie est plus courte', () => {
    // roundCourant vaut 3 (voir monde()) : la portee « tour » ne retient que
    // le round 3 dans le journal, mais le geste manuel du round 1 doit rester
    // visible dans la section d'audit.
    const journal = [
      entree(1, 'Main redistribuee a la main', { type: 'manuel' }),
      entree(3, 'Klaw joue une carte', { type: 'card' }),
    ]
    const rapport = construireRapport(monde(), undefined, journal, 'tour', CONTEXTE)
    expect(rapport.journal).toHaveLength(1)
    expect(rapport.gestesManuels).toHaveLength(1)
    expect(rapport.gestesManuels[0]?.texte).toBe('Main redistribuee a la main')
  })
})

describe('la version texte', () => {
  const base = () => construireRapport(monde(), undefined, [], 'recent', CONTEXTE)

  it('donne les object id, pas seulement les noms', () => {
    const texte = rapportEnTexte(base())
    expect(texte).toContain('c48')
    expect(texte).toContain('None Shall Pass')
    expect(texte).toContain('04079b')
  })

  it("rappelle qu'une commande se vise par object id", () => {
    expect(rapportEnTexte(base())).toContain('object id')
  })

  it('AVERTIT quand le journal est tronque', () => {
    const plein = Array.from({ length: MAX_ENTREES }, (_, i) => entree(3, `e${i}`))
    const texte = rapportEnTexte(construireRapport(monde(), undefined, plein, 'partie', CONTEXTE))
    expect(texte).toContain('TRONQU')
  })

  it("ne parle pas de troncature quand il n'y en a pas", () => {
    expect(rapportEnTexte(base()).toLowerCase()).not.toContain('tronqu')
  })

  it('avertit que le rapport contient les mains de tous les sieges', () => {
    expect(rapportEnTexte(base())).toContain('mains de tous les sièges')
  })

  it("dit quand le moteur n'attend rien", () => {
    expect(rapportEnTexte(base())).toContain('Aucune demande en cours')
  })

  it("montre le cout et la raison d'injouabilite d'une option", () => {
    const demande: Demande = {
      refus: [],
      prompt_text: 'Choisissez', event_name: 'WhenPlayerInTurn',
      show_cancel: true, ability_type: 'Hero_Response',
      options: [
        {
          id: 12, name: 'p_Play', bind_id: 57, bind_player_id: 0,
          all_legal_targets: [48], target_num_range: [1, 1],
          target_payment: { 0: { cost: '2', payment: [], rule: [] } },
          select_rule: '', target_must_include_traits: [], failure_reason: '', is_search: false,
        },
        {
          id: 13, name: 'p_Attack', bind_id: 0, bind_player_id: 0,
          all_legal_targets: [], target_num_range: [0, 0], target_payment: {},
          select_rule: '', target_must_include_traits: [],
          failure_reason: 'not enough resources', is_search: false,
        },
      ],
    }
    const texte = rapportEnTexte(construireRapport(monde(), demande, [], 'recent', CONTEXTE))
    expect(texte).toContain('[12] Play')
    expect(texte).toContain('portée par c57')
    expect(texte).toContain('coût 2')
    expect(texte).toContain('INJOUABLE : not enough resources')
  })

  // Regression du 02/09/2026 : le rapport ne rendait que `health` et
  // `k_threat`, et jetait le reste de `info`. Un compteur de pouvoir sur le
  // heros (dd001a « Power Syphon », maximum 3) etait donc invisible, ce qui
  // rendait le bug correspondant indiagnosticable depuis un rapport.
  it('rend les compteurs que la ligne ne montre pas deja', () => {
    const doom = carte(70, '* Doctor Doom', 'dd001a', 'Hero', { health: 11, power: 2 })
    const texte = rapportEnTexte(
      construireRapport(monde({ area_villain: [doom] }), undefined, [], 'recent', CONTEXTE)
    )
    expect(texte).toContain('11 PV')
    expect(texte).toContain('power=2')
  })

  it('ne repete pas en compteur ce que la ligne rend en clair', () => {
    const doom = carte(70, '* Doctor Doom', 'dd001a', 'Hero', { health: 11 })
    const texte = rapportEnTexte(
      construireRapport(monde({ area_villain: [doom] }), undefined, [], 'recent', CONTEXTE)
    )
    expect(texte).toContain('11 PV')
    expect(texte).not.toContain('health=11')
  })

  it('rend les mots-cles temporaires poses par un effet', () => {
    const doom = carte(70, '* Doctor Doom', 'dd001a', 'Hero', { health: 11 })
    doom.buffs = { villainous: '1' }
    const texte = rapportEnTexte(
      construireRapport(monde({ area_villain: [doom] }), undefined, [], 'recent', CONTEXTE)
    )
    expect(texte).toContain('buff:villainous=1')
  })

  // Regression du 02/09/2026 : `zone` etait collectee mais jamais rendue.
  // Savoir si un sbire est engage ou au rebut decide si sa capacite continue
  // s'applique encore.
  it('ecrit la zone de chaque carte', () => {
    const sbire = carte(5, '* Mister Fantastic', 'dd015', 'Minion', { health: 4 })
    const texte = rapportEnTexte(
      construireRapport(monde({ encounter_discard_pile: [sbire] }), undefined, [], 'recent', CONTEXTE)
    )
    expect(texte).toContain('(dd015, Minion, défausse rencontre)')
  })

  it('nomme le fichier avec le scenario et le round', () => {
    expect(nomFichierRapport(base())).toBe('rapport-none-shall-pass-r3.json')
  })

  it('nomme le fichier sans scenario quand la table est vide', () => {
    const vide = construireRapport(monde({ area_schemes_main: [] }), undefined, [], 'recent', CONTEXTE)
    expect(nomFichierRapport(vide)).toBe('rapport-partie-r3.json')
  })

  it('retire les accents du nom de fichier', () => {
    const accents = monde({
      area_schemes_main: [carte(48, "L'Épée de Damoclès", '99999b', 'MainScheme')],
    })
    const rapport = construireRapport(accents, undefined, [], 'recent', CONTEXTE)
    expect(nomFichierRapport(rapport)).toBe('rapport-l-epee-de-damocles-r3.json')
  })
})
