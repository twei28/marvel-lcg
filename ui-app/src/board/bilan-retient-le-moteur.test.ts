// LE BILAN RETIENT LE MOTEUR (07/10/2026).
//
// Defaut releve en rejouant une phase du mechant sur un moteur d'essai
// (Rhino, Klaw ; mode « Etape par etape ») : le moteur ne retenait que les
// trames des QUATRE phases du mechant. Des que la derniere etape etait
// validee, il filait sans rien attendre par « End Phase », « End Round »,
// « Start Round » jusqu'a « Player 1 Turn » du round suivant, 44 ms apres que
// le Bilan s'etait affiche. Le joueur lisait donc son Bilan au-dessus d'une
// table deja au round 2 (main repiochee, cartes redressees), avec « A toi de
// jouer » et le bandeau « Round 2 » par-dessus : le resultat sur la table avant
// la modale, et le tour suivant lance sans qu'il ait valide le Bilan.
//
// La regle : la PREMIERE trame qui suit la phase du mechant est retenue
// comme les autres, jusqu'a ce que le cartouche rende la main (Bilan valide).
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { decisionAccuse, DELAI_FILET_RESYNC_MS, Moteur, type EtatMoteur } from './moteur'
import type { World } from './world'

function monde(phase: string, render_id: number): World {
  return {
    render_id,
    round_id: 1,
    phase,
    prompt: '',
    players: [],
    cards: [],
    faits_mechant: [],
  } as unknown as World
}

class FauxSocket {
  static dernier: FauxSocket | undefined
  onopen: (() => void) | null = null
  onmessage: ((evenement: { data: unknown }) => void) | null = null
  onclose: (() => void) | null = null
  onerror: (() => void) | null = null
  constructor(public readonly url: string) {
    FauxSocket.dernier = this
  }
  send() {}
  close() {
    this.onclose?.()
  }
}

let courant: World
let accuses: number[]
let partie: number

function fauxFetch(url: string): Promise<Response> {
  if (url.startsWith('/get_world')) {
    return Promise.resolve(new Response(JSON.stringify(courant), { status: 200 }))
  }
  if (url.startsWith('/get_ask')) return Promise.resolve(new Response('', { status: 200 }))
  if (url.startsWith('/client_updated')) {
    accuses.push(Number(new URLSearchParams(url.split('?')[1] ?? '').get('r')))
    return Promise.resolve(new Response('', { status: 200 }))
  }
  return Promise.resolve(new Response('', { status: 404 }))
}

async function laisserTourner() {
  for (let tour = 0; tour < 32; tour += 1) await Promise.resolve()
}

describe('decisionAccuse : la trame qui suit la phase du mechant', () => {
  it('est retenue quand on vient de la phase du mechant', () => {
    expect(decisionAccuse('detaille', monde('End Phase', 98), true)).toBe('attendre-clic')
    expect(decisionAccuse('sur-table', monde('End Phase', 98), true)).toBe('attendre-clic')
  })

  it('ne l est jamais en mode « d un coup »', () => {
    expect(decisionAccuse('instantane', monde('End Phase', 98), true)).toBe('immediat')
  })

  it('ne retient jamais un monde absent', () => {
    expect(decisionAccuse('detaille', undefined, true)).toBe('immediat')
  })

  it('ne l est pas sans la phase du mechant avant elle (fin de la phase du joueur)', () => {
    expect(decisionAccuse('detaille', monde('End Phase', 52))).toBe('immediat')
    expect(decisionAccuse('detaille', monde('End Phase', 52), false)).toBe('immediat')
  })
})

describe('le moteur retient la premiere trame apres la phase du mechant', () => {
  let moteur: Moteur
  let etat: EtatMoteur | undefined

  beforeEach(() => {
    vi.useFakeTimers()
    window.localStorage.clear()
    accuses = []
    partie = 1
    courant = monde('Player 1 Turn', 40)
    vi.stubGlobal('WebSocket', FauxSocket as unknown as typeof WebSocket)
    vi.stubGlobal('fetch', vi.fn((url: string) => fauxFetch(url)))
    moteur = new Moteur(0)
    moteur.setModePhaseMechant('detaille')
    moteur.ecouter((nouveau) => {
      etat = nouveau
    })
    moteur.demarrer()
    FauxSocket.dernier?.onopen?.()
  })

  afterEach(() => {
    moteur.arreter()
    vi.unstubAllGlobals()
    vi.useRealTimers()
  })

  async function trame(phase: string, render_id: number) {
    courant = monde(phase, render_id)
    FauxSocket.dernier?.onmessage?.({
      data: JSON.stringify({
        render_id,
        game_id: partie,
        game_uid: `test-${partie}`,
        ask_players: [],
        total_players: 1,
        notify_texts: [],
        sieges_non_acquittes: [0],
      }),
    })
    await laisserTourner()
  }

  /** Joue la phase jusqu'a sa derniere trame, en relachant chaque trame retenue. */
  async function jouerLaPhase() {
    await trame('Player 1 Turn', 40)
    await trame('Main Scheme Place Threat', 54)
    await moteur.continuer()
    await trame('Enemy Activation', 60)
    await moteur.continuer()
    await trame('Reveal Encounter Cards', 77)
    await moteur.continuer()
  }

  it('retient « End Phase » tant que le cartouche n a pas rendu la main', async () => {
    await jouerLaPhase()
    await trame('End Phase', 98)
    expect(etat?.trameRetenue).toBe(98)
    expect(accuses).not.toContain(98)

    // Le moteur ne produit rien de plus tant qu'il n'est pas acquitte : on
    // verifie qu'une relecture de la MEME trame (question reposee) ne la
    // relache pas non plus.
    await trame('End Phase', 98)
    expect(etat?.trameRetenue).toBe(98)
    expect(accuses).not.toContain(98)

    await moteur.continuer()
    expect(accuses).toContain(98)
  })

  it('apres la reprise, plus rien n est retenu : les trames suivantes filent', async () => {
    await jouerLaPhase()
    await trame('End Phase', 98)
    await moteur.continuer()
    await trame('End Round', 99)
    await trame('Player 1 Turn', 102)
    expect(accuses).toContain(99)
    expect(accuses).toContain(102)
    expect(etat?.trameRetenue).toBeUndefined()
  })

  it('une fin de phase DU JOUEUR (sans phase du mechant avant) n est pas retenue', async () => {
    await trame('Player 1 Turn', 40)
    await trame('End Phase', 52)
    expect(accuses).toContain(52)
    expect(etat?.trameRetenue).toBeUndefined()
  })

  it('une partie neuve ne herite pas de la phase du mechant de la precedente', async () => {
    await jouerLaPhase()
    partie = 2
    await trame('Player 1 Turn', 1)
    expect(accuses).toContain(1)
    expect(etat?.trameRetenue).toBeUndefined()
  })

  // LE DEFAUT DU 07/10/2026, MESURE SUR UN MOTEUR D'ESSAI : le battement de
  // resynchronisation (toutes les 4 s) voyait la trame retenue « en retard » (le
  // serveur y liste notre siege tant qu'il n'a pas acquitte) et l'acquittait
  // sans clic. Une etape lue 8 s laissait le moteur avancer de 18 rendus : c'est
  // « l'etape suivante part sans mon Suivant », pour TOUTES les etapes.
  it('une trame retenue n est PAS relachee par le battement de resynchronisation', async () => {
    await jouerLaPhase()
    await trame('End Phase', 98)
    expect(etat?.trameRetenue).toBe(98)
    await vi.advanceTimersByTimeAsync(DELAI_FILET_RESYNC_MS * 3)
    await laisserTourner()
    expect(accuses).not.toContain(98)
    expect(etat?.trameRetenue).toBe(98)
    await moteur.continuer()
    expect(accuses).toContain(98)
  })

  it('le battement rattrape toujours un accuse PERDU (trame non retenue)', async () => {
    await trame('Player 1 Turn', 40)
    accuses.length = 0
    await vi.advanceTimersByTimeAsync(DELAI_FILET_RESYNC_MS + 100)
    await laisserTourner()
    expect(accuses).toContain(40)
  })

  it('une trame retenue d une etape ordinaire n est pas relachee non plus', async () => {
    await trame('Player 1 Turn', 40)
    await trame('Enemy Activation', 60)
    expect(etat?.trameRetenue).toBe(60)
    await vi.advanceTimersByTimeAsync(DELAI_FILET_RESYNC_MS * 3)
    await laisserTourner()
    expect(accuses).not.toContain(60)
    expect(etat?.trameRetenue).toBe(60)
  })

  it('apres un Annuler, le premier tour du joueur n est pas pris pour le Bilan', async () => {
    await trame('Enemy Activation', 60)
    await trame('Player 1 Turn', 12)
    expect(accuses).toContain(12)
    expect(etat?.trameRetenue).toBeUndefined()
  })

  // MESURE EN LECTURE LENTE (07/10/2026) : une lecture declenchee par une
  // reponse precede parfois la trame de 98 : le monde est deja a « End Phase »
  // alors que la trame tenue est encore celle de 97. Retenir cette trame-la, et
  // consommer le marqueur, laissait la VRAIE trame 98 filer sans retenue.
  it('une lecture du monde AVANT sa trame ne fait pas filer le Bilan', async () => {
    await jouerLaPhase()
    // Le monde lu est deja « End Phase » (98), la trame tenue est encore 97.
    courant = monde('End Phase', 98)
    FauxSocket.dernier?.onmessage?.({
      data: JSON.stringify({
        render_id: 97, game_id: partie, game_uid: `test-${partie}`, ask_players: [],
        total_players: 1, notify_texts: [], sieges_non_acquittes: [0],
      }),
    })
    await laisserTourner()
    // Le cartouche relache ce qu'il tient (la trame perimee) : le Bilan ne doit pas en pâtir.
    await moteur.continuer()
    await trame('End Phase', 98)
    expect(etat?.trameRetenue).toBe(98)
    expect(accuses).not.toContain(98)
    await moteur.continuer()
    expect(accuses).toContain(98)
  })

  it('en mode « d un coup », rien n est retenu apres la phase', async () => {
    moteur.setModePhaseMechant('instantane')
    await trame('Enemy Activation', 60)
    await trame('End Phase', 98)
    expect(accuses).toContain(98)
    expect(etat?.trameRetenue).toBeUndefined()
  })
})
