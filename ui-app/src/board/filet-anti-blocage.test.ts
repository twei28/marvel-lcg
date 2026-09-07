// LE FILET ANTI-BLOCAGE, UNE SEULE ECHEANCE PAR PHASE.
//
// Le moteur attend l'accuse de CHAQUE client (`WaitSync`) : un onglet fantome
// (ferme sans prevenir, en arriere-plan, deconnecte) gelerait la phase du
// mechant pour toute la table. Le filet la relache au bout d'un temps borne.
//
// Il etait arme A CHAQUE TRAME RETENUE : chaque micro-evenement repoussait
// l'echeance de 90 s, donc une table bloquee ne l'atteignait jamais tant que le
// moteur produisait quelque chose, et une table qui l'atteignait subissait 90 s
// par trame (constat F2 de l'audit du 06/09/2026). Il est desormais arme UNE
// FOIS, au premier accuse retenu, et desarme a la sortie de la phase.
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import {
  DELAI_FILET_ANTI_BLOCAGE_CLIC_MS,
  Moteur,
  type EtatMoteur,
} from './moteur'
import type { World } from './world'

function monde(phase: string, render_id: number): World {
  return {
    render_id,
    round_id: 2,
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

/** Laisse les lectures asynchrones du moteur (fetch) se terminer. */
async function laisserTourner() {
  for (let tour = 0; tour < 32; tour += 1) await Promise.resolve()
}

describe('le filet anti-blocage de la phase du mechant', () => {
  let moteur: Moteur
  let etat: EtatMoteur | undefined

  beforeEach(() => {
    vi.useFakeTimers()
    window.localStorage.clear()
    accuses = []
    courant = monde('Enemy Activation', 101)
    vi.stubGlobal('WebSocket', FauxSocket as unknown as typeof WebSocket)
    vi.stubGlobal('fetch', vi.fn((url: string) => fauxFetch(url)))
    moteur = new Moteur(0)
    moteur.setModePhaseMechant('detaille')
    moteur.ecouter((nouveau) => {
      etat = nouveau
    })
  })

  afterEach(() => {
    moteur.arreter()
    vi.unstubAllGlobals()
    vi.useRealTimers()
  })

  /** Pousse la trame du monde courant, comme le socket du moteur. */
  function pousser() {
    FauxSocket.dernier?.onmessage?.({
      data: JSON.stringify({
        render_id: courant.render_id,
        game_id: 1,
        game_uid: 'test',
        ask_players: [],
        total_players: 1,
        notify_texts: [],
      }),
    })
  }

  async function ouvrir() {
    moteur.demarrer()
    FauxSocket.dernier?.onopen?.()
    await laisserTourner()
    pousser()
    await laisserTourner()
  }

  it('arme une echeance des la premiere trame retenue', async () => {
    await ouvrir()
    expect(etat?.trameRetenue).toBe(101)
    expect(etat?.echeanceFilet).toBe(Date.now() + DELAI_FILET_ANTI_BLOCAGE_CLIC_MS)
  })

  // LE DEFAUT : chaque trame repoussait l'echeance. Une phase du mechant en
  // produit une par micro-evenement, donc le filet n'arrivait jamais a terme.
  it('ne repousse pas l echeance a chaque trame de la meme phase', async () => {
    await ouvrir()
    const echeance = etat?.echeanceFilet
    for (let trame = 0; trame < 3; trame += 1) {
      vi.advanceTimersByTime(5_000)
      moteur.avancerMaintenant()
      await laisserTourner()
      courant = monde('Enemy Activation', 102 + trame)
      pousser()
      await laisserTourner()
    }
    expect(etat?.trameRetenue).toBe(104)
    expect(etat?.echeanceFilet).toBe(echeance)
  })

  it('relache la trame quand l echeance tombe', async () => {
    await ouvrir()
    expect(accuses).toEqual([])
    await vi.advanceTimersByTimeAsync(DELAI_FILET_ANTI_BLOCAGE_CLIC_MS)
    await laisserTourner()
    expect(accuses).toEqual([101])
  })

  it('desarme le filet a la sortie de la phase du mechant', async () => {
    await ouvrir()
    expect(etat?.echeanceFilet).toBeDefined()
    courant = monde('Player 1 Turn', 102)
    pousser()
    await laisserTourner()
    expect(etat?.trameRetenue).toBeUndefined()
    expect(etat?.echeanceFilet).toBeUndefined()
    // Et plus rien ne se declenche tout seul ensuite.
    const avant = accuses.length
    await vi.advanceTimersByTimeAsync(DELAI_FILET_ANTI_BLOCAGE_CLIC_MS * 2)
    expect(accuses.length).toBe(avant)
  })
})
