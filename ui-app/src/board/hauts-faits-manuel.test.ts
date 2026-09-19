// LE MODE MANUEL N'ENREGISTRE AUCUN HAUT FAIT, COMME LE BAC A SABLE.
//
// Garantie explicite du plan (tache 2, ronde de correction 1) : une victoire
// obtenue en deplacant les cartes a la main ne vaut pas une vraie victoire.
// `enregistrerHautsFaits` est une methode PRIVEE de `Moteur` — on ne l'atteint
// donc qu'en rejouant une vraie trame de socket, comme
// `filet-anti-blocage.test.ts` le fait deja pour le meme genre de logique
// interne. Meme faux transport ici, repris tel quel.
//
// Deux cas, et les deux comptent : le refus en manuel ne prouve rien seul —
// un filtre qui refuserait TOUJOURS passerait ce cas au vert sans avoir rien
// filtre de particulier. Le pendant (partie ordinaire, meme notification)
// prouve que le filtre laisse encore passer le cas normal.
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { Moteur, type EtatMoteur } from './moteur'
import type { World } from './world'

function monde(render_id: number, mode_manuel: boolean): World {
  return {
    render_id,
    round_id: 1,
    phase: 'Player 0 Turn',
    prompt: '',
    players: [],
    cards: [],
    faits_mechant: [],
    mode_manuel,
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

function fauxFetch(url: string): Promise<Response> {
  if (url.startsWith('/get_world')) {
    return Promise.resolve(new Response(JSON.stringify(courant), { status: 200 }))
  }
  if (url.startsWith('/get_ask')) return Promise.resolve(new Response('', { status: 200 }))
  if (url.startsWith('/client_updated')) return Promise.resolve(new Response('', { status: 200 }))
  return Promise.resolve(new Response('', { status: 404 }))
}

/** Laisse les lectures asynchrones du moteur (fetch) se terminer. */
async function laisserTourner() {
  for (let tour = 0; tour < 32; tour += 1) await Promise.resolve()
}

describe('les hauts faits, en mode manuel', () => {
  let moteur: Moteur
  let etat: EtatMoteur | undefined

  beforeEach(() => {
    window.localStorage.clear()
    vi.stubGlobal('WebSocket', FauxSocket as unknown as typeof WebSocket)
    vi.stubGlobal('fetch', vi.fn((url: string) => fauxFetch(url)))
    moteur = new Moteur(0)
    moteur.ecouter((nouveau) => {
      etat = nouveau
    })
  })

  afterEach(() => {
    moteur.arreter()
    vi.unstubAllGlobals()
  })

  /** Pousse une trame portant UNE notification de haut fait, comme le moteur. */
  function pousserHautFait(titre: string) {
    FauxSocket.dernier?.onmessage?.({
      data: JSON.stringify({
        render_id: courant.render_id,
        game_id: 1,
        game_uid: 'test',
        ask_players: [],
        total_players: 1,
        notify_texts: [JSON.stringify({ text: `Haut fait : ${titre}`, category: '', level: '' })],
      }),
    })
  }

  async function ouvrir() {
    moteur.demarrer()
    FauxSocket.dernier?.onopen?.()
    await laisserTourner()
  }

  it('refuse un haut fait quand le monde porte mode_manuel', async () => {
    courant = monde(101, true)
    await ouvrir()
    // `etat.monde` porte deja `mode_manuel` (lu par le `lire()` d'ouverture,
    // avant cette trame) : c'est bien ce monde-la que le filtre consulte.
    expect(etat?.monde?.mode_manuel).toBe(true)
    pousserHautFait('Une victoire truquee')
    await laisserTourner()
    expect(etat?.hautsFaits).toEqual([])
  })

  // LE TEMOIN : sans lui, un filtre qui refuserait TOUJOURS (bogue oppose a
  // celui qu'on redoute) passerait le cas ci-dessus sans avoir rien prouve.
  it('enregistre encore un haut fait en partie ordinaire', async () => {
    courant = monde(101, false)
    await ouvrir()
    expect(etat?.monde?.mode_manuel).toBeFalsy()
    pousserHautFait('Une vraie victoire')
    await laisserTourner()
    expect(etat?.hautsFaits).toEqual(['Une vraie victoire'])
  })
})
