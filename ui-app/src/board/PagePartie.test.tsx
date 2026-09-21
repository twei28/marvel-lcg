// L'ECRAN DE JEU, monte pour de vrai.
//
// Voir `moteur-faux.ts` pour le pourquoi : ce fichier est le premier a rendre
// `board.tsx`. Il ne rejoue pas de regles — il pose une table, emet la trame,
// et affirme sur ce que le joueur voit.
import { act, fireEvent, render, screen } from '@testing-library/react'
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
    expect(screen.queryByRole('tablist')).toBeNull()
  })

  it('s\'active bien en mode manuel DECLARE (boucle manuelle entree)', async () => {
    monter()
    const monde = monde2Heros() as { mode_manuel?: boolean; manuel_actif?: boolean }
    monde.mode_manuel = true
    monde.manuel_actif = true
    await emettre({ monde: monde as never })
    expect(screen.queryByRole('tablist')).not.toBeNull()
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

// TACHE 3. Le bouton qui met une partie ORDINAIRE en pause : dans la barre du
// haut, a cote d'Annuler -- ni un reglage cache (FenetreReglages), ni un
// bouton qu'on presse par accident (voir board.tsx pour la justification
// complete). Masque des que la pause est posee : `BandeauPause` devient alors
// le seul moyen de reprendre.
describe('le bouton de pause (tache 3)', () => {
  it('existe en partie ORDINAIRE, hors pause', async () => {
    monter()
    await emettre({ monde: table(heros('Spider-Man', 1)) })
    expect(screen.getByRole('button', { name: /Mettre en pause/ })).toBeTruthy()
  })

  it('pose la pause au clic (POST /manuel_pause, actif: true, aucun champ qui)', async () => {
    vi.stubGlobal('fetch', vi.fn(async () => ({ ok: true }) as Response))
    monter()
    await emettre({ monde: table(heros('Spider-Man', 1)) })
    fireEvent.click(screen.getByRole('button', { name: /Mettre en pause/ }))
    await attendreLeReseau()
    expect(fetch).toHaveBeenCalledWith('/manuel_pause', expect.objectContaining({
      method: 'POST',
      body: JSON.stringify({ actif: true }),
    }))
    vi.unstubAllGlobals()
  })

  it('disparait pendant la pause : le bandeau devient le seul moyen de reprendre', async () => {
    monter()
    const monde = table(heros('Spider-Man', 1)) as { mode_manuel?: boolean; manuel_actif?: boolean }
    monde.mode_manuel = false
    monde.manuel_actif = true
    await emettre({ monde: monde as never })
    expect(screen.queryByRole('button', { name: /Mettre en pause/ })).toBeNull()
    expect(screen.getByText('Reprendre')).toBeTruthy()
  })

  it('n\'existe pas en mode manuel DECLARE : rien a « pauser », ManualLoop tient deja la table muette', async () => {
    monter()
    const monde = table(heros('Spider-Man', 1)) as { mode_manuel?: boolean; manuel_actif?: boolean }
    monde.mode_manuel = true
    monde.manuel_actif = true
    await emettre({ monde: monde as never })
    expect(screen.queryByRole('button', { name: /Mettre en pause/ })).toBeNull()
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

  it('finit par dire que la table est fermee, et offre la sortie', async () => {
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
// « Quitter la partie » ferme la table (21/09/2026)
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
  /** Répond à chaque route du départ. `siteUrl` vide = aucun site derrière. */
  function reseau(siteUrl: string, fermeture: unknown) {
    return vi.fn(async (cible: string) => {
      if (cible === '/get_site_url') return { ok: true, json: async () => ({ url: siteUrl }) }
      if (cible === '/quitter_la_table') return { ok: true, json: async () => fermeture }
      return { ok: true, json: async () => ({}) }
    } ) as unknown as typeof fetch
  }

  const questions: string[] = []

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

  it('⚠ ferme vraiment la table de l’hôte, et le dépose sur le site', async () => {
    vi.stubGlobal('fetch', reseau('https://exemple.test',
      { eteinte: true, url: 'https://exemple.test/arret' }))
    monter()
    await emettre({ monde: table(heros('Spider-Man', 1)) })
    fireEvent.click(screen.getByRole('button', { name: 'Menu' }))
    await attendreLeReseau()
    await attendreLeReseau()
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
      { eteinte: true, url: 'https://exemple.test/arret' }))
    monter()
    await emettre({ monde: table(heros('Spider-Man', 1)) })
    fireEvent.click(screen.getByRole('button', { name: 'Menu' }))
    await attendreLeReseau()
    // « La partie en cours sera perdue » ne suffit plus : ce qui disparaît,
    // c'est la TABLE, et les autres joueurs sont mis dehors avec elle.
    const question = questions.join('\n')
    expect(question).toMatch(/table/i)
    expect(question).toMatch(/déconnect|dehors/i)
    expect(question).toMatch(/site/i)
    vi.unstubAllGlobals()
  })

  it('renoncer ne ferme rien du tout', async () => {
    vi.stubGlobal('confirm', vi.fn(() => false))
    vi.stubGlobal('fetch', reseau('https://exemple.test',
      { eteinte: true, url: 'https://exemple.test/arret' }))
    monter()
    await emettre({ monde: table(heros('Spider-Man', 1)) })
    fireEvent.click(screen.getByRole('button', { name: 'Menu' }))
    await attendreLeReseau()
    expect(fetch).not.toHaveBeenCalledWith('/quitter_la_table', expect.anything())
    expect(atterrissages).toEqual([])
    vi.unstubAllGlobals()
  })

  it('⚠ un INVITÉ part sans rien fermer, et on ne lui promet rien', async () => {
    vi.stubGlobal('fetch', reseau('https://exemple.test', { eteinte: false, url: '' }))
    monter(1)
    await emettre({ monde: table(heros('Spider-Man', 1)) })
    fireEvent.click(screen.getByRole('button', { name: 'Menu' }))
    await attendreLeReseau()
    await attendreLeReseau()
    expect(fetch).not.toHaveBeenCalledWith('/quitter_la_table', expect.anything())
    expect(questions.join('\n')).not.toMatch(/déconnect/i)
    expect(atterrissages).toEqual(['/prepare.html'])
    vi.unstubAllGlobals()
  })

  it('sans site derrière, on retourne simplement à l’écran des héros', async () => {
    // Partie locale : rien à rendre, et `/prepare.html` reste vivant puisque
    // le moteur ne s'éteint pas.
    vi.stubGlobal('fetch', reseau('', { eteinte: false, url: '' }))
    monter()
    await emettre({ monde: table(heros('Spider-Man', 1)) })
    fireEvent.click(screen.getByRole('button', { name: 'Menu' }))
    await attendreLeReseau()
    await attendreLeReseau()
    expect(fetch).not.toHaveBeenCalledWith('/quitter_la_table', expect.anything())
    expect(atterrissages).toEqual(['/prepare.html'])
    vi.unstubAllGlobals()
  })
})
