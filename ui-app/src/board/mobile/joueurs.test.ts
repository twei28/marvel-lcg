import { describe, expect, it } from 'vitest'
import { groupesParJoueur, ordreDAffichage } from './joueurs'
import { construirePlateau } from '../zones'
import type { EmplacementAffiche } from '../zones'
import { catalogueVide } from '../catalogue'
import type { World, WorldCard, WorldPlayer } from '../world'

// Fixture minimale pour passer par construirePlateau() : le vrai chemin qui
// aplatit les aires des joueurs dans terrain-soutien, plutot qu'un objet
// EmplacementAffiche construit a la main qui ne passe jamais par la logique
// de pairage-puis-filtrage de zones.ts.
function fabriqueCartes(): (overrides?: Partial<WorldCard>) => WorldCard {
  let compteur = 0
  return (overrides = {}) => {
    compteur += 1
    return {
      id: compteur,
      is_ready: true,
      is_face_up: true,
      visible_for_players: [0, 1],
      bind_object_id: 0,
      name: `Carte ${compteur}`,
      info: {},
      traits: {},
      buffs: {},
      card_id: `carte-${compteur}`,
      pic_id: `pic-${compteur}`,
      down_card_ids: [],
      card_type: 'Ally',
      cost: 0,
      resources: [],
      ...overrides,
    }
  }
}

function joueurVide(): WorldPlayer {
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
  }
}

function mondeMinimal(joueurs: WorldPlayer[]): World {
  return {
    render_id: 0,
    round_id: 0,
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
    players: joueurs,
    active_card_ids: [],
  }
}

const EMPLACEMENT: EmplacementAffiche = {
  cle: 'terrain-soutien',
  titre: 'Héros et soutiens',
  groupes: [[], [], [], [], [], []],
  nombreSurLaLigne: 0,
  proprietaires: [0, 0, 0, 1, 1, 1],
}

describe('groupesParJoueur', () => {
  it('range chaque groupe sous son joueur', () => {
    const par = groupesParJoueur(EMPLACEMENT)
    expect([...par.keys()]).toEqual([0, 1])
    expect(par.get(0)).toHaveLength(3)
    expect(par.get(1)).toHaveLength(3)
  })

  it('met tout sous le joueur 0 quand le champ est absent', () => {
    const par = groupesParJoueur({ ...EMPLACEMENT, proprietaires: undefined })
    expect([...par.keys()]).toEqual([0])
    expect(par.get(0)).toHaveLength(6)
  })

  it(
    'range correctement les groupes de terrain-soutien construits par ' +
      'construirePlateau(), y compris quand un groupe du joueur courant ' +
      'est filtre (obligations_area vide)',
    () => {
      const carte = fabriqueCartes()

      // Joueur 0 (le joueur courant) : obligations_area reste vide, donc son
      // 3e groupe (voir zones.ts) disparait au filtrage de emplacement(). Il
      // ne doit rester que 2 groupes sous lui, pas 3.
      const joueur0: WorldPlayer = {
        ...joueurVide(),
        area_hero: [carte({ name: 'Heros joueur 0', card_type: 'Hero' })],
        supports: [carte({ name: 'Soutien joueur 0' })],
      }

      // Joueur 1 (l'autre) : ses 3 groupes (deck special, heros, soutiens)
      // sont tous peuples, donc aucun n'est filtre.
      const joueur1: WorldPlayer = {
        ...joueurVide(),
        area_hero: [carte({ name: 'Heros joueur 1', card_type: 'Hero' })],
        supports: [carte({ name: 'Soutien joueur 1' })],
        additional_deck: [carte({ name: 'Deck special joueur 1' })],
      }

      const monde = mondeMinimal([joueur0, joueur1])
      const plateau = construirePlateau(monde, { playerId: 0, catalogue: catalogueVide })
      const soutien = plateau.emplacements.find((e) => e.cle === 'terrain-soutien')
      expect(soutien).toBeDefined()

      const par = groupesParJoueur(soutien!)

      // Le simple compte suffirait a reveler une desynchronisation
      // (groupes/proprietaires de longueurs differentes), mais pas a reveler
      // un decalage qui garde les memes longueurs (ex: prendre les N premiers
      // identifiants d'un tableau non filtre). On verifie donc AUSSI le
      // contenu : les bonnes cartes doivent se retrouver sous le bon joueur.
      expect(par.get(0)).toHaveLength(2)
      expect(par.get(1)).toHaveLength(3)

      const nomsJoueur0 = par.get(0)!.flat().map((u) => u.carte.name)
      const nomsJoueur1 = par.get(1)!.flat().map((u) => u.carte.name)

      expect(nomsJoueur0).toEqual(['Heros joueur 0', 'Soutien joueur 0'])
      expect(nomsJoueur1).toContain('Heros joueur 1')
      expect(nomsJoueur1).toContain('Soutien joueur 1')
      expect(nomsJoueur1).not.toContain('Heros joueur 0')
      expect(nomsJoueur1).not.toContain('Soutien joueur 0')
      expect(nomsJoueur0).not.toContain('Heros joueur 1')
      expect(nomsJoueur0).not.toContain('Soutien joueur 1')
    }
  )
})

describe('ordreDAffichage', () => {
  it('met le joueur actif en premier', () => {
    expect(ordreDAffichage([0, 1, 2], 2)).toEqual([2, 0, 1])
  })

  it("ne bouge rien si l'actif est inconnu", () => {
    expect(ordreDAffichage([0, 1, 2], 7)).toEqual([0, 1, 2])
  })
})
