import { describe, expect, it } from 'vitest'
import { contexteDePose, estCacheePourLeJoueur, origineDe, poserEnJeu, TYPES_CONNUS } from './poser-en-jeu'
import type { World, WorldCard, WorldPlayer } from '../world'

const carte = (id: number, card_type: string, name = `c${id}`): WorldCard =>
  ({ id, card_type, name, card_id: `x${id}` }) as unknown as WorldCard

const joueur = (zones: Partial<WorldPlayer>): WorldPlayer =>
  ({
    area_hero: [], allies: [], supports: [], player_deck: [], player_discard_pile: [],
    dealt_encounter_cards: [], hand_cards: [], engaged_enemies: [], set_aside_nemesis_sets: [],
    set_aside_deck: [], additional_deck: [], additional_discard_pile: [], obligations_area: [],
    environment_area: [], resources: '', is_eliminated: false, ...zones,
  }) as WorldPlayer

const SEUL = { siege: 0, identite: { id: 1, nom: 'Spider-Man' }, ciblesAmelioration: [{ id: 1, nom: 'Spider-Man' }] }

describe('poser une carte en jeu selon son type (table D.3)', () => {
  it.each([
    ['Ally', 'AlliesArea', 0],
    ['Support', 'SupportsArea', 0],
    ['Path', 'SupportsArea', 0],
    ['Event', 'PlayerProcessingArea', 0],
    ['Minion', 'EngagedEnemiesArea', 0],
    ['PlayerMinion', 'EngagedEnemiesArea', 0],
    ['Obligation', 'ObligationsArea', 0],
  ])('%s va dans %s du siège du joueur', (type, zone, siege) => {
    expect(poserEnJeu({ id: 9, type }, SEUL)).toEqual({ genre: 'deplacer', zone, siege })
  })

  it.each([
    ['Environment', 'EnvironmentArea'],
    ['PlayerSideScheme', 'SideSchemesArea'],
    ['EncounterSideScheme', 'SideSchemesArea'],
    ['Treachery', 'ProcessingArea'],
  ])('%s va dans %s, une zone partagée', (type, zone) => {
    expect(poserEnJeu({ id: 9, type }, SEUL)).toEqual({ genre: 'deplacer', zone })
  })

  it('le siège suit le joueur visé', () => {
    expect(poserEnJeu({ id: 9, type: 'Ally' }, { ...SEUL, siege: 2 })).toEqual({
      genre: 'deplacer',
      zone: 'AlliesArea',
      siege: 2,
    })
  })

  it("une amélioration s'attache directement à l'identité quand c'est la seule cible", () => {
    expect(poserEnJeu({ id: 9, type: 'Upgrade' }, SEUL)).toEqual({ genre: 'attacher', cible: 1 })
  })

  it('une amélioration propose ses cibles quand il y en a plusieurs (question 3)', () => {
    const cibles = [
      { id: 1, nom: 'Spider-Man' },
      { id: 4, nom: 'Black Cat' },
    ]
    expect(poserEnJeu({ id: 9, type: 'Upgrade' }, { ...SEUL, ciblesAmelioration: cibles })).toEqual({
      genre: 'choisir',
      cibles,
    })
  })

  it('cas limite : une amélioration sans aucune cible en jeu est refusée', () => {
    const pose = poserEnJeu({ id: 9, type: 'Upgrade' }, { siege: 0, ciblesAmelioration: [] })
    expect(pose.genre).toBe('refus')
  })

  it('une ressource est refusée : elle se défausse pour payer', () => {
    const pose = poserEnJeu({ id: 9, type: 'Resource' }, SEUL)
    expect(pose).toEqual({ genre: 'refus', raison: 'Une ressource se défausse pour payer : Suppr, ou glisse-la sur ta défausse' })
  })

  it("une pièce jointe lâchée sans hôte attend en zone de résolution, comme après Ctrl+D (06/10/2026)", () => {
    // Le dessus du deck Rencontre glissé sur la table : on la glisse ensuite
    // sur la carte qu'elle accompagne. Avant : refus, la pile semblait figée.
    expect(poserEnJeu({ id: 9, type: 'Attachment' }, SEUL)).toEqual({ genre: 'deplacer', zone: 'ProcessingArea' })
  })

  it('Evidence est refusé : il accompagne une carte', () => {
    expect(poserEnJeu({ id: 9, type: 'Evidence' }, SEUL)).toEqual({
      genre: 'refus',
      raison: 'Lâche-la sur la carte qu’elle accompagne',
    })
  })

  it.each(['Hero', 'AlterEgo', 'EncounterVillain', 'Leader', 'MainScheme', 'StatusCard', 'Insert', 'Challenge'])(
    '%s ne se pose pas sur la table : refus nommé, jamais un repli',
    (type) => {
      expect(poserEnJeu({ id: 9, type }, SEUL)).toEqual({
        genre: 'refus',
        raison: 'Cette carte ne se pose pas sur la table : glisse-la sur une pile ou fais Déplacer vers',
      })
    }
  )

  it("cas d'erreur : un type inconnu est refusé", () => {
    expect(poserEnJeu({ id: 9, type: 'Machin' }, SEUL).genre).toBe('refus')
    expect(poserEnJeu({ id: 9, type: '' }, SEUL).genre).toBe('refus')
  })

  it('nomme TOUS les types finaux du moteur (game/card/face/card_type/)', () => {
    // Liste relevée le 06/10/2026 par `grep "^class .*FinalType"` : un type
    // ajouté au moteur doit être rangé ici, jamais deviné.
    expect([...TYPES_CONNUS].sort()).toEqual(
      [
        'Ally', 'AlterEgo', 'Attachment', 'Challenge', 'EncounterSideScheme', 'EncounterVillain', 'Environment',
        'Event', 'Evidence', 'Hero', 'Insert', 'Leader', 'MainScheme', 'Minion', 'Obligation', 'PlayerMinion',
        'Path', 'PlayerSideScheme', 'Resource', 'StatusCard', 'Support', 'Treachery', 'Upgrade',
      ].sort()
    )
  })
})

describe('le contexte de pose, lu dans la trame', () => {
  const monde = {
    players: [
      joueur({ area_hero: [carte(1, 'Hero', 'Spider-Man')], allies: [carte(4, 'Ally', 'Black Cat')] }),
      joueur({ area_hero: [carte(2, 'Hero', 'Captain Marvel')] }),
    ],
  } as unknown as World

  it("rend le siège, l'identité et les cartes qui peuvent porter une amélioration", () => {
    expect(contexteDePose(monde, 0)).toEqual({
      siege: 0,
      identite: { id: 1, nom: 'Spider-Man' },
      ciblesAmelioration: [
        { id: 1, nom: 'Spider-Man' },
        { id: 4, nom: 'Black Cat' },
      ],
    })
    expect(contexteDePose(monde, 1).ciblesAmelioration).toEqual([{ id: 2, nom: 'Captain Marvel' }])
  })

  it('propose aussi les ennemis en jeu, après les cartes du joueur (décision du 06/10/2026)', () => {
    const avecEnnemis = {
      area_villain: [carte(30, 'EncounterVillain', 'Rhino')],
      players: [
        joueur({
          area_hero: [carte(1, 'Hero', 'Spider-Man')],
          engaged_enemies: [carte(31, 'Minion', 'Hydra Mercenary')],
        }),
        joueur({ area_hero: [carte(2, 'Hero', 'Captain Marvel')], engaged_enemies: [carte(32, 'Minion', 'Shocker')] }),
      ],
    } as unknown as World
    expect(contexteDePose(avecEnnemis, 0).ciblesAmelioration).toEqual([
      { id: 1, nom: 'Spider-Man' },
      { id: 30, nom: 'Rhino' },
      { id: 31, nom: 'Hydra Mercenary' },
      { id: 32, nom: 'Shocker' },
    ])
  })

  it("n'offre pas une carte du méchant qui n'est pas un ennemi (attachement posé sur lui)", () => {
    const avecAttachement = {
      area_villain: [carte(30, 'EncounterVillain', 'Rhino'), carte(33, 'Attachment', 'Armored Rhino Suit')],
      players: [joueur({ area_hero: [carte(1, 'Hero', 'Spider-Man')] })],
    } as unknown as World
    expect(contexteDePose(avecAttachement, 0).ciblesAmelioration.map((c) => c.id)).toEqual([1, 30])
  })

  it('sans identité en jeu, aucune cible', () => {
    expect(contexteDePose({ players: [joueur({})] } as unknown as World, 0)).toEqual({
      siege: 0,
      identite: undefined,
      ciblesAmelioration: [],
    })
  })
})

describe("l'origine d'une carte", () => {
  const monde = {
    players: [
      joueur({
        hand_cards: [carte(10, 'Ally')],
        area_processing: [carte(11, 'Event')],
        player_deck: [carte(12, 'Ally')],
        player_discard_pile: [carte(13, 'Event')],
        allies: [carte(14, 'Ally')],
      }),
    ],
    area_processing: [carte(15, 'Treachery')],
    encounter_deck: [carte(16, 'Minion')],
  } as unknown as World

  it('distingue la main, la résolution, les piles et le jeu', () => {
    expect(origineDe(monde, 10)).toBe('main')
    expect(origineDe(monde, 11)).toBe('resolution')
    expect(origineDe(monde, 15)).toBe('resolution')
    expect(origineDe(monde, 12)).toBe('pile')
    expect(origineDe(monde, 13)).toBe('pile')
    expect(origineDe(monde, 16)).toBe('pile')
    expect(origineDe(monde, 14)).toBe('jeu')
  })

  it("une carte introuvable n'a pas d'origine", () => {
    expect(origineDe(monde, 999)).toBeUndefined()
    expect(origineDe(undefined, 10)).toBeUndefined()
  })
})

describe('une carte face cachée, pour le joueur qui la manipule', () => {
  const cachee = (id: number) => ({ ...carte(id, 'Ally'), is_face_up: false }) as WorldCard
  const monde = {
    players: [joueur({ hand_cards: [cachee(10)], player_deck: [cachee(12)], allies: [carte(14, 'Ally')] })],
  } as unknown as World

  it('le dessus du deck, face cachée, est caché', () => {
    expect(estCacheePourLeJoueur(monde, 12)).toBe(true)
  })

  it('une carte EN MAIN ne l’est jamais : son propriétaire la voit (constat du 06/10/2026)', () => {
    expect(estCacheePourLeJoueur(monde, 10)).toBe(false)
  })

  it('une carte visible ou inconnue ne l’est pas', () => {
    expect(estCacheePourLeJoueur(monde, 14)).toBe(false)
    expect(estCacheePourLeJoueur(monde, 999)).toBe(false)
  })
})

