// L'ECRAN DE JEU, monte pour de vrai.
//
// Voir `moteur-faux.ts` pour le pourquoi : ce fichier est le premier a rendre
// `board.tsx`. Il ne rejoue pas de regles — il pose une table, emet la trame,
// et affirme sur ce que le joueur voit.
import { act, render, screen } from '@testing-library/react'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { MoteurFaux, etatInitial } from './moteur-faux'
import type { EtatMoteur } from './moteur'
import { NOM_OPTION_MANIGANCE } from './manigance-face-a'
import type { Demande, Option } from './ask'
import { DUREE_RETOURNEMENT } from './PanneauManigance'
import { catalogueVide } from './catalogue'
import { carteSurTable, siege, tableAvec } from './plateau-de-test'

vi.mock('./moteur', async (original) => ({
  ...(await original<typeof import('./moteur')>()),
  Moteur: MoteurFaux,
}))

const { PagePartie } = await import('../board')

/** La manigance principale de la table : le panneau la montre par `bind_id`. */
const MANIGANCE_PRINCIPALE = carteSurTable(9, '01097a', 'main_scheme', "The Breakin' and Takin'")

/**
 * Une demande du moteur, TYPEE et complete.
 *
 * ⚠ Pas de raccourci `as never` ici : l'ecran lit `prompt_text`, `event_name`,
 * `ability_type`... et un objet a moitie rempli le fait tomber sur des champs
 * absents, ce qui ferait passer un defaut de decor pour un defaut de cablage.
 */
function option(surcharge: Partial<Option> = {}): Option {
  return {
    id: 7,
    name: 'Play_Card',
    bind_id: 0,
    bind_player_id: 0,
    all_legal_targets: [],
    target_num_range: [0, 0],
    target_payment: {},
    select_rule: '',
    target_must_include_traits: [],
    failure_reason: '',
    is_search: false,
    ...surcharge,
  }
}

function demande(options: Option[]): Demande {
  return {
    options,
    refus: [],
    prompt_text: '',
    event_name: '',
    show_cancel: false,
    ability_type: '',
  }
}

function heros(nom: string, id: number) {
  return siege({ area_hero: [carteSurTable(id, `0100${id}a`, 'hero', nom)] })
}

/**
 * Une table complete du point de vue de l'ECRAN. `tableAvec` suffit aux cas de
 * zones ; l'ecran, lui, lit aussi la phase et le tour (bandeau, splash), et un
 * monde a moitie rempli le fait tomber — ce qui est la bonne nouvelle : le
 * rendu refuse un faux approximatif.
 */
function table(...joueurs: ReturnType<typeof siege>[]) {
  const monde = tableAvec(joueurs[0], {
    phase: 'Player 0 Turn',
    round_id: 1,
    villains: [],
    main_scheme: [],
    encounter_deck_size: 0,
    encounter_discard_pile: [],
    area_schemes_main: [MANIGANCE_PRINCIPALE],
    area_schemes_side: [],
  } as never)
  ;(monde as { players: unknown[] }).players = joueurs
  return monde
}

/**
 * Emet une trame vers l'ecran monte, sur l'etat d'ouverture par defaut.
 *
 * `await` : la trame relance des effets qui posent leur etat en microtache
 * (survols, effets de cartes). Sans ce tour de boucle, React le signale en
 * « update not wrapped in act » et l'ecran est lu a moitie stabilise.
 */
async function emettre(trame: Partial<EtatMoteur>) {
  await act(async () => {
    MoteurFaux.derniere?.emettre({ ...etatInitial(), connecte: true, ...trame })
  })
}

function monter() {
  return render(
    <PagePartie
      playerId={0}
      catalogue={catalogueVide}
      modeActions="simple"
      changerModeActions={() => {}}
    />
  )
}

// jsdom n'implemente pas ResizeObserver : le plateau observe son cadre pour
// calculer l'echelle. Meme bouchon que Board.test.tsx et AssistantAction.test.tsx.
class ResizeObserverBouchon {
  observe() {}
  unobserve() {}
  disconnect() {}
}

beforeEach(() => {
  MoteurFaux.derniere = undefined
  ;(globalThis as { ResizeObserver?: unknown }).ResizeObserver = ResizeObserverBouchon
})

describe("l'ecran de jeu", () => {
  it('ouvre le moteur au montage et le ferme au demontage', async () => {
    const vue = monter()
    const moteur = MoteurFaux.derniere
    expect(moteur?.demarrages).toBe(1)
    vue.unmount()
    expect(moteur?.arrets).toBe(1)
  })

  it('dessine la table quand la premiere trame arrive', async () => {
    monter()
    await emettre({ monde: table(heros('Spider-Man', 1)) })
    expect(screen.getByText(/Spider-Man/)).toBeTruthy()
  })
})

// DEFAUT N°1 DU 15/09/2026. La refonte des onglets du 14/09 avait range la Vue
// DANS le bouton « Partie », contre une decision ecrite, et aucun cas n'a rougi
// parce que rien ne montait cette barre. Ces deux cas la montent.
describe('la barre du haut', () => {
  it('offre la Vue a plusieurs, un bouton par heros plus Auto', async () => {
    monter()
    await emettre({ monde: table(heros('Spider-Man', 1), heros('Captain Marvel', 2)) })
    expect(screen.getByText('Vue')).toBeTruthy()
    expect(screen.getByRole('button', { name: 'Auto' })).toBeTruthy()
    expect(screen.getByRole('button', { name: 'Spider-Man' })).toBeTruthy()
    expect(screen.getByRole('button', { name: 'Captain' })).toBeTruthy()
  })

  it('ne l\'offre pas en solo : il n\'y a qu\'une vue possible', async () => {
    monter()
    await emettre({ monde: table(heros('Spider-Man', 1)) })
    expect(screen.queryByText('Vue')).toBeNull()
    expect(screen.queryByRole('button', { name: 'Auto' })).toBeNull()
  })

  it('ne propose pas la vue d\'un joueur elimine', async () => {
    monter()
    const elimine = heros('Captain Marvel', 2)
    ;(elimine as { is_eliminated: boolean }).is_eliminated = true
    await emettre({ monde: table(heros('Spider-Man', 1), elimine) })
    expect(screen.queryByRole('button', { name: 'Captain' })).toBeNull()
  })
})

// DEFAUT N°3 DU 15/09/2026. `plateau-de-test.ts` court-circuite `board.tsx` :
// il ne sait meme pas qu'un panneau de manigance existe. Seul le montage de
// l'ecran prouve que la condition est bien cablee — et que le bouton REPOND.
describe('le panneau de la manigance', () => {
  it('parait quand le moteur attend la confirmation du retournement', async () => {
    monter()
    await emettre({
      monde: table(heros('Spider-Man', 1)),
      demande: demande([option({ name: NOM_OPTION_MANIGANCE, bind_id: 9 })]),
      aNous: true,
    })
    expect(screen.getByRole('button', { name: 'Retourner la manigance' })).toBeTruthy()
  })

  it('ne parait pas sur une demande ordinaire', async () => {
    monter()
    await emettre({
      monde: table(heros('Spider-Man', 1)),
      demande: demande([option({ bind_id: 9 })]),
      aNous: true,
    })
    expect(screen.queryByRole('button', { name: 'Retourner la manigance' })).toBeNull()
  })

  // Le bouton laisse d'abord la carte se retourner (DUREE_RETOURNEMENT), PUIS
  // repond : sans horloge factice, ce cas verrait une liste vide et passerait
  // pour un defaut de cablage.
  it('renvoie la reponse au moteur quand on valide, le retournement fini', async () => {
    vi.useFakeTimers()
    try {
      monter()
      await emettre({
        monde: table(heros('Spider-Man', 1)),
        demande: demande([option({ name: NOM_OPTION_MANIGANCE, bind_id: 9 })]),
        aNous: true,
      })
      act(() => {
        screen.getByRole('button', { name: 'Retourner la manigance' }).click()
      })
      act(() => {
        vi.advanceTimersByTime(DUREE_RETOURNEMENT)
      })
      expect(MoteurFaux.derniere?.reponses).toEqual([
        { reponse: { id: 7, targets: [], resources: [] }, bindPlayerId: 0 },
      ])
    } finally {
      vi.useRealTimers()
    }
  })
})
