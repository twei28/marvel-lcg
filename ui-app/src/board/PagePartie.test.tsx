// L'ECRAN DE JEU, monte pour de vrai.
//
// Voir `moteur-faux.ts` pour le pourquoi : ce fichier est le premier a rendre
// `board.tsx`. Il ne rejoue pas de regles — il pose une table, emet la trame,
// et affirme sur ce que le joueur voit.
import { act, fireEvent, render, screen, within } from '@testing-library/react'
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

// ⚠ ON NE REMPLACE QUE L'ATTERRISSAGE. `laTableVaSeFermer` et `fermerLaTable`
// restent les vraies : c'est le cablage du bouton qu'on mesure, pas un decor.
// jsdom, lui, ne sait pas naviguer — et on veut de toute facon AFFIRMER sur la
// destination, pas la subir.
const atterrissages: string[] = []
vi.mock('./quitter-la-table', async (original) => ({
  ...(await original<typeof import('./quitter-la-table')>()),
  atterrir: (url: string) => {
    atterrissages.push(url)
  },
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

/** Laisse la chaîne fetch/basculerPause se résoudre (même idiome que CoucheTriche.test.tsx). */
const attendreLeReseau = () => act(() => new Promise((resolve) => setTimeout(resolve, 0)))

function monter(playerId = 0) {
  return render(
    <PagePartie
      playerId={playerId}
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

  // 24/09/2026 : griser l'onglet d'un heros qui a deja boucle son tour ce
  // round (inspire d'Arkham Horror LCG). Purement visuel -- toujours
  // cliquable, jamais desactive.
  it('grise l\'onglet d\'un heros qui a fini son tour, sans le desactiver', async () => {
    monter()
    const fini = heros('Captain Marvel', 2)
    ;(fini as { has_finished_turn_this_round: boolean }).has_finished_turn_this_round = true
    await emettre({ monde: table(heros('Spider-Man', 1), fini) })
    const boutonFini = screen.getByRole('button', { name: 'Captain' })
    expect(boutonFini.className).toMatch(/est-tour-fini/)
    expect(boutonFini).not.toBeDisabled()
    const boutonPasFini = screen.getByRole('button', { name: 'Spider-Man' })
    expect(boutonPasFini.className).not.toMatch(/est-tour-fini/)
  })

  // TACHE 7 BIS (19/09/2026). Ce bandeau a ete reconditionne sur `!manuel`
  // (board.tsx) pour laisser la place a `SelecteurHeros` en mode manuel, qui
  // n'a pas de bouton Auto (le moteur n'y demande plus rien). Rien ne
  // surveillait cette condition avant ce cas : un `!manuel` mal pose (ou
  // inverse) aurait pu faire disparaitre Auto en partie ORDINAIRE sans
  // qu'aucun test ne rougisse.
  it('mode ordinaire : Auto reste la a plusieurs, meme avec le mode manuel dans le paysage', async () => {
    monter()
    const monde = table(heros('Spider-Man', 1), heros('Captain Marvel', 2))
    ;(monde as { mode_manuel?: boolean }).mode_manuel = false
    await emettre({ monde })
    expect(screen.getByRole('button', { name: 'Auto' })).toBeTruthy()
  })
})

// TACHE 3 (correctif, arbitrage du plan du 20/09/2026). `SelecteurHeros` se
// reglait sur `leMoteurSeTait` seul (`manuel`, la variable interne de
// board.tsx) : ce champ vaut aussi vrai pendant une simple PAUSE d'une partie
// ORDINAIRE (route `/manuel_pause`), pas seulement en mode manuel DECLARE.
// Une table EN LIGNE mise en pause aurait alors propose de regarder la main
// de N'IMPORTE QUEL joueur -- exactement la fuite d'information ("chaque
// joueur a son propre ecran") que l'arbitrage interdit. Il doit se regler sur
// `estModeManuel` (la REGLE), pas `leMoteurSeTait` (l'ETAT).
describe('le selecteur de heros manuel (tache 3, correctif de gating)', () => {
  function monde2Heros() {
    return table(heros('Spider-Man', 1), heros('Captain Marvel', 2))
  }

  it('ne s\'active PAS pendant une pause d\'une partie ORDINAIRE, meme a plusieurs heros', async () => {
    monter()
    const monde = monde2Heros() as { mode_manuel?: boolean; manuel_actif?: boolean }
    monde.mode_manuel = false
    monde.manuel_actif = true
    await emettre({ monde: monde as never })
    expect(screen.queryByRole('tablist', { name: /Quel héros/ })).toBeNull()
  })

  it('s\'active bien en mode manuel DECLARE (boucle manuelle entree)', async () => {
    monter()
    const monde = monde2Heros() as { mode_manuel?: boolean; manuel_actif?: boolean }
    monde.mode_manuel = true
    monde.manuel_actif = true
    await emettre({ monde: monde as never })
    expect(screen.queryByRole('tablist', { name: /Quel héros/ })).not.toBeNull()
  })
})

// TACHE 3 (ronde de correction 1). La contrainte la plus lourde de ce plan
// est que le mode ORDINAIRE ne perde RIEN -- et une pause reste un moment de
// mode ordinaire. Le selecteur de vue « Auto » (juste au-dessus, gate
// `!manuel && ... > 1`) se reglait sur l'ETAT (`leMoteurSeTait`) au lieu de
// la REGLE (`estModeManuel`) : une table a plusieurs heros mise en pause
// perdait donc TOUT selecteur de vue, puisque `SelecteurHeros` ne prend pas
// le relais en pause (arbitrage n°2, delibere). Corrige sur
// `!modeManuelDeclare`.
describe('le selecteur de vue Auto (tache 3, correctif de gating)', () => {
  it('survit a une pause d\'une partie ORDINAIRE, a plusieurs heros', async () => {
    monter()
    const monde = table(heros('Spider-Man', 1), heros('Captain Marvel', 2)) as {
      mode_manuel?: boolean
      manuel_actif?: boolean
    }
    monde.mode_manuel = false
    monde.manuel_actif = true
    await emettre({ monde: monde as never })
    expect(screen.getByText('Vue')).toBeTruthy()
    expect(screen.getByRole('button', { name: 'Auto' })).toBeTruthy()
  })

  it('reste absent en mode manuel DECLARE (SelecteurHeros prend le relais)', async () => {
    monter()
    const monde = table(heros('Spider-Man', 1), heros('Captain Marvel', 2)) as {
      mode_manuel?: boolean
      manuel_actif?: boolean
    }
    monde.mode_manuel = true
    monde.manuel_actif = true
    await emettre({ monde: monde as never })
    expect(screen.queryByText('Vue')).toBeNull()
    expect(screen.queryByRole('button', { name: 'Auto' })).toBeNull()
  })
})

/** Depuis le 04/10/2026, plus de fenetre « Plus d'options » : la pause est un
 * bouton de la barre (choix de l'utilisateur). Rien a ouvrir. */
function ouvrirPlusOptions() {}

describe('la barre du haut sans « Plus d options » (04/10/2026)', () => {
  it('le bouton ⚙ ouvre directement les Reglages', async () => {
    monter()
    await emettre({ monde: table(heros('Spider-Man', 1)) })
    expect(screen.queryByRole('button', { name: /Plus d.?options/ })).toBeNull()
    fireEvent.click(screen.getByRole('button', { name: 'Réglages' }))
    expect(screen.getByRole('dialog', { name: 'Réglages' })).toBeTruthy()
  })

  it('la langue a son bouton dans la barre', async () => {
    monter()
    await emettre({ monde: table(heros('Spider-Man', 1)) })
    expect(screen.getByRole('button', { name: /^(FR|EN)$/ })).toBeTruthy()
  })
})

// L'interrupteur « Auto / Manuel » (05/10/2026) : remplace l'ancien bouton
// « Mettre en pause ». Toujours dans la barre, il pose ou leve la pause d'une
// partie commencee en auto, et rend la table au moteur (fenetre « On en est
// ou ? ») pour une partie commencee en manuel.
describe('l\'interrupteur Auto / Manuel', () => {
  it('est toujours dans la barre, sur Auto en partie ordinaire', async () => {
    monter()
    await emettre({ monde: table(heros('Spider-Man', 1)) })
    expect(screen.getByRole('button', { name: 'Mode automatique', pressed: true })).toBeTruthy()
    expect(screen.getByRole('button', { name: 'Mode manuel', pressed: false })).toBeTruthy()
  })

  it('Manuel pose la pause au clic (POST /manuel_pause, actif: true, aucun champ qui)', async () => {
    vi.stubGlobal('fetch', vi.fn(async () => ({ ok: true }) as Response))
    monter()
    await emettre({ monde: table(heros('Spider-Man', 1)) })
    fireEvent.click(screen.getByRole('button', { name: 'Mode manuel' }))
    await attendreLeReseau()
    expect(fetch).toHaveBeenCalledWith('/manuel_pause', expect.objectContaining({
      method: 'POST',
      body: JSON.stringify({ actif: true }),
    }))
    vi.unstubAllGlobals()
  })

  it('en pause : Manuel est allume, et Auto leve la pause (le moteur reprend a sa question)', async () => {
    vi.stubGlobal('fetch', vi.fn(async () => ({ ok: true }) as Response))
    monter()
    const monde = table(heros('Spider-Man', 1)) as { mode_manuel?: boolean; manuel_actif?: boolean }
    monde.mode_manuel = false
    monde.manuel_actif = true
    await emettre({ monde: monde as never })
    expect(screen.getByRole('button', { name: 'Mode manuel', pressed: true })).toBeTruthy()
    fireEvent.click(screen.getByRole('button', { name: 'Mode automatique' }))
    await attendreLeReseau()
    expect(fetch).toHaveBeenCalledWith('/manuel_pause', expect.objectContaining({
      body: JSON.stringify({ actif: false }),
    }))
    vi.unstubAllGlobals()
  })

  it('partie commencee en manuel : Auto ouvre « On en est ou ? » et reprend a la phase choisie', async () => {
    vi.stubGlobal('fetch', vi.fn(async () => ({ ok: true }) as Response))
    monter()
    const monde = table(heros('Spider-Man', 1)) as { mode_manuel?: boolean; manuel_actif?: boolean }
    monde.mode_manuel = true
    monde.manuel_actif = true
    await emettre({ monde: monde as never })
    fireEvent.click(screen.getByRole('button', { name: 'Mode automatique' }))
    expect(screen.getByRole('dialog', { name: 'On en est où ?' })).toBeTruthy()
    expect(fetch).not.toHaveBeenCalledWith('/manuel_reprise', expect.anything())
    fireEvent.click(screen.getByText('Au début de la phase méchant'))
    await attendreLeReseau()
    expect(fetch).toHaveBeenCalledWith('/manuel_reprise', expect.objectContaining({
      method: 'POST',
      body: JSON.stringify({ phase: 'mechant' }),
    }))
    vi.unstubAllGlobals()
  })

  it('en manuel : l\'aide s\'ouvre toute seule, se ferme a la main, et la languette la rouvre', async () => {
    monter()
    const monde = table(heros('Spider-Man', 1)) as { mode_manuel?: boolean; manuel_actif?: boolean }
    monde.mode_manuel = false
    monde.manuel_actif = true
    await emettre({ monde: monde as never })
    expect(screen.getByRole('dialog', { name: 'Aide du mode manuel' })).toBeTruthy()
    fireEvent.click(within(screen.getByRole('dialog', { name: 'Aide du mode manuel' })).getByTitle('Fermer'))
    expect(screen.queryByRole('dialog', { name: 'Aide du mode manuel' })).toBeNull()
    fireEvent.click(screen.getByRole('button', { name: 'Aide' }))
    expect(screen.getByRole('dialog', { name: 'Aide du mode manuel' })).toBeTruthy()
  })

  it('en automatique : pas l aide du manuel, mais sa propre aide, fermee par defaut', async () => {
    monter()
    await emettre({ monde: table(heros('Spider-Man', 1)) })
    expect(screen.queryByRole('dialog', { name: 'Aide du mode manuel' })).toBeNull()
    expect(screen.queryByRole('dialog', { name: 'Aide' })).toBeNull()
    fireEvent.click(screen.getByRole('button', { name: 'Aide' }))
    expect(screen.getByRole('dialog', { name: 'Aide' })).toBeInTheDocument()
    expect(screen.getByText('Alt + glisser')).toBeInTheDocument()
  })
})

// ⚠ LA TABLE FERMEE, VUE DU PLATEAU (17/09/2026). Le bandeau repetait
// « nouvel essai dans Xs » indefiniment : un joueur dont la table avait ete
// fermee voyait un decompte qui ne menait nulle part. Constate en direct sur
// le plateau d'un joueur, 19 tentatives de socket en dix minutes, toutes en
// 502. Les delais etant 2, 4, 8, 15 puis 30 s, cinq essais valent une minute :
// passe ce cap, une coupure passagere serait revenue.
describe('le bandeau de connexion', () => {
  const coupe = (tentatives: number) => ({
    monde: table(heros('Spider-Man', 1)),
    connecte: false,
    tentatives,
    prochaineTentative: Date.now() + 8000,
  })

  it('parle de reconnexion tant que la coupure peut etre passagere', async () => {
    monter()
    await emettre(coupe(2))
    expect(screen.getByText(/Connexion perdue/)).toBeTruthy()
    expect(screen.queryByText(/Cette table a été fermée/)).toBeNull()
  })

  // ⚠ VINGT-NEUF SECONDES DE SILENCE, ET C'ETAIT TROP (21/09/2026). Les
  // delais sont 2, 4, 8, 15 puis 30 s : l'invite dont l'hote vient de fermer
  // la table lisait « Connexion perdue » pendant une demi-minute avant
  // d'apprendre qu'il n'y avait plus rien a rejoindre. C'etait supportable
  // quand seul un deploiement fermait une table ; fermer est devenu un clic.

  /** Monte un INVITE (siege 1) sur une table qui vient du site. */
  async function invitePrivéDeSocket(tentatives: number) {
    vi.stubGlobal('fetch', vi.fn(async () => ({
      ok: true,
      status: 200,
      json: async () => ({ url: 'https://exemple.test' }),
    })) as unknown as typeof fetch)
    monter(1)
    await attendreLeReseau()
    await emettre(coupe(tentatives))
  }

  it('nomme la cause probable des le 3e essai, sans rien declarer', async () => {
    await invitePrivéDeSocket(3)
    expect(screen.getByText(/l’hôte a peut-être fermé la table/)).toBeTruthy()
    // ⚠ UNE POSSIBILITE, PAS UNE DECLARATION : une vraie coupure met le meme
    // temps a revenir, et l'affirmation reste au 5e essai.
    expect(screen.queryByText(/Cette table a été fermée/)).toBeNull()
    // ⚠ ET LA SORTIE NE BOUGE PAS AVEC ELLE. A six secondes, la partie est
    // presque surement recuperable : offrir « Revenir a l'accueil » ferait
    // quitter sa partie a un invite impatient pendant un hoquet de wifi — et
    // il est arrive par un lien de siege dont la cle est dans l'adresse,
    // donc l'accueil ne l'y ramene pas. Dire, oui ; pousser dehors, non.
    expect(screen.queryByRole('button', { name: /Revenir à l’accueil/ })).toBeNull()
    vi.unstubAllGlobals()
  })

  it('mais se tait au 2e : un hoquet de reseau n’est pas une table fermee', async () => {
    await invitePrivéDeSocket(2)
    expect(screen.queryByText(/peut-être fermé la table/)).toBeNull()
    expect(screen.queryByRole('button', { name: /Revenir à l’accueil/ })).toBeNull()
    vi.unstubAllGlobals()
  })

  it('⚠ et se tait pour l’HOTE, qui saurait tres bien s’il avait ferme', async () => {
    // Le bandeau ne recoit qu'un etat de socket : sans qu'on le lui dise, il
    // suggerait a l'hote lui-meme que « l'hote a peut-etre ferme la table »,
    // pendant une simple coupure.
    vi.stubGlobal('fetch', vi.fn(async () => ({
      ok: true,
      status: 200,
      json: async () => ({ url: 'https://exemple.test' }),
    })) as unknown as typeof fetch)
    monter(0)
    await attendreLeReseau()
    await emettre(coupe(4))
    expect(screen.queryByText(/peut-être fermé la table/)).toBeNull()
    expect(screen.getByText(/Connexion perdue/)).toBeTruthy()
    vi.unstubAllGlobals()
  })

  it('⚠ et se tait en partie LOCALE : il n’y a ni hote ni table', async () => {
    // JOUER-SOLO.bat, sur 127.0.0.1 : le moteur repond « aucun site ».
    vi.stubGlobal('fetch', vi.fn(async () => ({
      ok: true,
      status: 200,
      json: async () => ({ url: '' }),
    })) as unknown as typeof fetch)
    monter(1)
    await attendreLeReseau()
    await emettre(coupe(4))
    expect(screen.queryByText(/peut-être fermé la table/)).toBeNull()
    vi.unstubAllGlobals()
  })

  it('finit par dire que la table est fermee, et offre ALORS la sortie', async () => {
    monter()
    await emettre(coupe(5))
    expect(screen.getByText(/Cette table a été fermée/)).toBeTruthy()
    expect(screen.getByRole('button', { name: /Revenir à l’accueil/ })).toBeTruthy()
    // ⚠ ON NE RENONCE PAS POUR AUTANT : le bouton de reconnexion reste, une
    // table peut rouvrir.
    expect(screen.getByRole('button', { name: /Reconnecter maintenant/ })).toBeTruthy()
    expect(screen.queryByText(/Connexion perdue/)).toBeNull()
  })

  it('ne dit rien du tout tant que le socket tient', async () => {
    monter()
    await emettre({ monde: table(heros('Spider-Man', 1)), connecte: true, tentatives: 0 })
    expect(screen.queryByText(/Connexion perdue/)).toBeNull()
    expect(screen.queryByText(/Cette table a été fermée/)).toBeNull()
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


// ==========================================================================
// Le menu simple et la fermeture complète sont deux choix distincts.
// ==========================================================================
// ⚠ C'EST LE CABLAGE QUI CASSE, PAS LE MODULE. `quitter-la-table.test.ts`
// prouve que les décisions sont justes ; il ne dit rien du bouton. Or c'est
// précisément le bouton qui, pendant des mois, n'a fait que naviguer vers
// `/prepare.html` en laissant la table debout — et les invités bloqués sur
// l'ancienne partie.
//
// Le même bouton sert sur MOBILE : `BandeauPortrait` rend le `.board-actions`
// du plateau tel quel (`menu={props.actionsPartie}`), donc le même
// `onClick`. Un seul câblage, un seul cas.
describe('le bouton « Menu » du plateau', () => {
  /**
   * Répond aux deux routes du départ.
   *
   * `site` : `{url}` que rend `/get_site_url`, ou `'panne'` pour un échec —
   * et la nuance est tout le sujet : « pas de site » et « je n'ai pas pu
   * savoir » ne doivent pas mener au même écran.
   */
  function reseau(site: string | 'panne', fermeture: unknown) {
    return vi.fn(async (cible: string) => {
      if (cible === '/get_site_url') {
        if (site === 'panne') throw new Error('coupé')
        return { ok: true, json: async () => ({ url: site }) }
      }
      if (cible === '/quitter_la_table') return { ok: true, json: async () => fermeture }
      return { ok: true, json: async () => ({}) }
    }) as unknown as typeof fetch
  }

  const questions: string[] = []

  /**
   * Monte, laisse l'adresse du site se lire, pose la table, ouvre la modale
   * « Menu » (refonte du header du 24/09/2026 : « Menu » et « Déconnexion
   * complète » sont FUSIONNÉS derrière un seul bouton qui ouvre un choix),
   * puis clique le choix demandé DANS cette modale.
   */
  async function cliquerSortie(nom: string | RegExp, playerId = 0) {
    monter(playerId)
    // ⚠ L'ADRESSE EST LUE AU MONTAGE, plus au clic : sans ce tour de boucle,
    // le plateau croirait encore ne rien savoir du site.
    await attendreLeReseau()
    await emettre({ monde: table(heros('Spider-Man', 1)) })
    fireEvent.click(screen.getByRole('button', { name: 'Menu' }))
    fireEvent.click(screen.getByRole('button', { name: nom }))
    await attendreLeReseau()
    await attendreLeReseau()
  }

  const cliquerMenu = (playerId = 0) => cliquerSortie(/Retour au menu/, playerId)
  const cliquerDeconnexion = (playerId = 0) =>
    cliquerSortie(/Déconnexion complète/, playerId)

  beforeEach(() => {
    atterrissages.length = 0
    questions.length = 0
    // Hors `FournisseurConfirmation`, `useConfirmation` retombe sur
    // `window.confirm` : c'est par là qu'on lit ce que le joueur a sous les
    // yeux avant de décider.
    vi.stubGlobal('confirm', vi.fn((texte: string) => {
      questions.push(texte)
      return true
    }))
  })

  it('le menu revient au choix du héros sans fermer la table', async () => {
    vi.stubGlobal('fetch', reseau('https://exemple.test',
      { issue: 'fermee', url: 'https://exemple.test/arret' }))
    await cliquerMenu()
    expect(fetch).not.toHaveBeenCalledWith('/quitter_la_table', expect.anything())
    expect(atterrissages).toEqual(['/prepare.html'])
    vi.unstubAllGlobals()
  })

  it('⚠ la déconnexion complète ferme vraiment la table de l’hôte, et le dépose sur le site', async () => {
    vi.stubGlobal('fetch', reseau('https://exemple.test',
      { issue: 'fermee', url: 'https://exemple.test/arret' }))
    await cliquerDeconnexion()
    expect(fetch).toHaveBeenCalledWith('/quitter_la_table', expect.objectContaining({
      method: 'POST',
    }))
    // ⚠ JAMAIS UNE PAGE DU MOTEUR. Il est mort une seconde après la réponse :
    // `/prepare.html` le serait avec lui.
    expect(atterrissages).toEqual(['https://exemple.test/arret'])
    vi.unstubAllGlobals()
  })

  it('⚠ annonce la fermeture, pas seulement la partie perdue', async () => {
    vi.stubGlobal('fetch', reseau('https://exemple.test',
      { issue: 'fermee', url: 'https://exemple.test/arret' }))
    await cliquerDeconnexion()
    // « La partie en cours sera perdue » ne suffit plus : ce qui disparaît,
    // c'est la TABLE, et les autres joueurs sont mis dehors avec elle.
    const question = questions.join('\n')
    expect(question).toMatch(/table/i)
    expect(question).toMatch(/déconnect|dehors/i)
    expect(question).toMatch(/site/i)
    // ⚠ ET ON N'EFFRAIE PAS POUR RIEN : le site sauve la partie avant de
    // tuer le moteur et la range dans « Reprendre ». Dire « perdue » serait
    // faux sur un geste déjà lourd.
    expect(question).toMatch(/Reprendre/)
    expect(question).not.toMatch(/perdue/i)
    vi.unstubAllGlobals()
  })

  it('renoncer ne ferme rien du tout', async () => {
    vi.stubGlobal('confirm', vi.fn(() => false))
    vi.stubGlobal('fetch', reseau('https://exemple.test',
      { issue: 'fermee', url: 'https://exemple.test/arret' }))
    await cliquerDeconnexion()
    expect(fetch).not.toHaveBeenCalledWith('/quitter_la_table', expect.anything())
    expect(atterrissages).toEqual([])
    vi.unstubAllGlobals()
  })

  it('⚠ un INVITÉ part sans rien fermer, et on ne lui promet rien', async () => {
    vi.stubGlobal('fetch', reseau('https://exemple.test', { issue: 'sans-site', url: '' }))
    await cliquerDeconnexion(1)
    expect(fetch).not.toHaveBeenCalledWith('/quitter_la_table', expect.anything())
    expect(questions.join('\n')).not.toMatch(/déconnect/i)
    expect(atterrissages).toEqual(['/prepare.html'])
    vi.unstubAllGlobals()
  })

  it('sans site derrière, on retourne simplement à l’écran des héros', async () => {
    // Partie locale : rien à rendre, et `/prepare.html` reste vivant puisque
    // le moteur ne s'éteint pas.
    vi.stubGlobal('fetch', reseau('', { issue: 'sans-site', url: '' }))
    await cliquerDeconnexion()
    expect(fetch).not.toHaveBeenCalledWith('/quitter_la_table', expect.anything())
    expect(atterrissages).toEqual(['/prepare.html'])
    vi.unstubAllGlobals()
  })

  it('⚠ adresse du site INCONNUE : on demande quand même, et on le dit', async () => {
    // LE DÉFAUT RÉTABLI EN SILENCE. Un hoquet sur `/get_site_url` faisait
    // passer l'hôte pour un joueur local : ancienne fenêtre, départ, table
    // laissée debout avec l'ancienne partie dedans. Exactement le défaut
    // qu'on corrige, remis en place par une panne de réseau.
    vi.stubGlobal('fetch', reseau('panne',
      { issue: 'fermee', url: 'https://exemple.test/arret' }))
    await cliquerDeconnexion()
    expect(fetch).toHaveBeenCalledWith('/quitter_la_table', expect.anything())
    expect(questions.join('\n')).toMatch(/n’a pas pu le vérifier/)
    expect(atterrissages).toEqual(['https://exemple.test/arret'])
    vi.unstubAllGlobals()
  })

  it('⚠ issue INCONNUE : on n’affirme rien, on ouvre le site', async () => {
    // LE SEUL ENDROIT OÙ CE TRAVAIL POUVAIT AFFIRMER LE FAUX. `/api/eteindre`
    // révoque et lance l'extinction AVANT de répondre : au-delà du plafond de
    // dix secondes du moteur, la table disparaît quand même. Dire « rien n'a
    // été détruit » et proposer de rester sur la partie, c'était promettre un
    // moteur condamné.
    vi.stubGlobal('fetch', reseau('https://exemple.test',
      { issue: 'inconnue', url: 'https://exemple.test' }))
    await cliquerDeconnexion()
    const question = questions.join('\n')
    expect(question).toMatch(/peut-être en train de se fermer/)
    expect(question).not.toMatch(/Rien n’a été détruit/)
    expect(atterrissages).toEqual(['https://exemple.test'])
    vi.unstubAllGlobals()
  })

  /** Le départ, avec un statut HTTP choisi sur `/quitter_la_table`. */
  function reseauAvecStatut(statut: number) {
    return vi.fn(async (cible: string) => {
      if (cible === '/get_site_url') {
        return { ok: true, status: 200, json: async () => ({ url: 'https://exemple.test' }) }
      }
      if (cible === '/quitter_la_table') {
        return { ok: false, status: statut, json: async () => ({}) }
      }
      return { ok: true, status: 200, json: async () => ({}) }
    }) as unknown as typeof fetch
  }

  it('un 403 du moteur, lui, peut affirmer que rien n’a bougé', async () => {
    vi.stubGlobal('fetch', reseauAvecStatut(403))
    await cliquerDeconnexion()
    expect(questions.join('\n')).toMatch(/Rien n’a été touché/)
    expect(atterrissages).toEqual(['/prepare.html'])
    vi.unstubAllGlobals()
  })

  it('⚠ un 502 ne peut rien affirmer : c’est un moteur qui n’est plus là', async () => {
    // LE CHEMIN QUE LA FENÊTRE « inconnue » FABRIQUAIT ELLE-MÊME : issue
    // inconnue, l'hôte choisit « Rester ici », la table finit de s'éteindre,
    // il reclique Menu, Caddy rend 502 — et il lisait « Rien n'a été touché »
    // avec « Rester sur la partie », sur une table déjà disparue.
    vi.stubGlobal('fetch', reseauAvecStatut(502))
    await cliquerDeconnexion()
    const question = questions.join('\n')
    expect(question).toMatch(/peut-être en train de se fermer/)
    expect(question).not.toMatch(/Rien n’a été touché/)
    // Et on l'envoie là où la réponse existe, pas sur une page du moteur.
    // ⚠ Un 502 ne porte aucun corps : l'adresse vient de la lecture du
    // montage, pas de la réponse — d'où l'intérêt de l'avoir déjà.
    expect(atterrissages).toEqual(['https://exemple.test'])
    vi.unstubAllGlobals()
  })
})

// L'ECRAN DE FIN EN ONOMATOPEE BD (decision du 04/10/2026, questions une a
// une) : un eclat de BD derriere « DÉFAITE ! » (rouge) ou « VICTOIRE ! »
// (jaune et bleu), puis le cartouche en dessous.
describe('l ecran de fin de partie en onomatopee BD', () => {
  it('defaite : un eclat « DÉFAITE ! »', async () => {
    monter()
    await emettre({ monde: { ...table(heros('Spider-Man', 1)), game_over: true, players_won: false } as never })
    const eclat = document.querySelector('.fin-partie .fin-partie-eclat')
    expect(eclat?.textContent).toBe('DÉFAITE !')
    expect(document.querySelector('.fin-partie.est-defaite')).not.toBeNull()
  })

  it('victoire : un eclat « VICTOIRE ! »', async () => {
    monter()
    await emettre({ monde: { ...table(heros('Spider-Man', 1)), game_over: true, players_won: true } as never })
    expect(document.querySelector('.fin-partie .fin-partie-eclat')?.textContent).toBe('VICTOIRE !')
  })
})
