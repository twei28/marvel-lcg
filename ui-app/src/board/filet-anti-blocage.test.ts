// LE FILET ANTI-BLOCAGE : 90 s D'INACTIVITE PENDANT UNE TRAME RETENUE.
//
// Le moteur attend l'accuse de CHAQUE client (`WaitSync`) : un onglet fantome
// (en arriere-plan, deconnecte, laisse a l'abandon) gelerait la phase du
// mechant pour toute la table. Le filet la relache au bout d'un temps borne.
//
// Deux defauts successifs, et la regle tenue aujourd'hui vient du second.
//
//  1. Arme A CHAQUE TRAME RETENUE : chaque micro-evenement repoussait
//     l'echeance de 90 s, donc une table bloquee ne l'atteignait jamais tant
//     que le moteur produisait quelque chose (constat F2 de l'audit du
//     06/09/2026).
//  2. Puis arme UNE SEULE FOIS PAR PHASE, sans jamais tenir compte des clics :
//     un joueur ACTIF qui mettait plus de 90 s a lire sa phase se faisait
//     doubler par son propre secours, avec un compte a rebours anxiogene et un
//     accuse qu'il n'avait pas demande (relecture A6).
//
// La regle est donc : armee au premier retenu, DESARMEE par tout accuse du
// joueur (`continuer`, appele par le cartouche), re-armee au retenu suivant.
// Un onglet inactif avance d'une trame toutes les 90 s, et c'est voulu ; un
// onglet FERME ne bloque rien du tout (`CheckSync` cesse de l'attendre).
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

  // LE PREMIER DEFAUT : chaque trame repoussait l'echeance. Le moteur repousse
  // la MEME trame chaque fois qu'il pose sa question (`IsInputReady`), donc le
  // filet n'arrivait jamais a terme sans que personne ait rien fait.
  it('ne repousse pas l echeance tant que le joueur n a rien accuse', async () => {
    await ouvrir()
    const echeance = etat?.echeanceFilet
    for (let fois = 0; fois < 3; fois += 1) {
      vi.advanceTimersByTime(5_000)
      pousser()
      await laisserTourner()
    }
    expect(etat?.trameRetenue).toBe(101)
    expect(etat?.echeanceFilet).toBe(echeance)
  })

  // LE SECOND DEFAUT, celui de la relecture A6 : l'echeance ne bougeait plus du
  // tout, donc un joueur qui LISAIT se faisait doubler par son propre secours.
  it('remet l echeance a zero des que le joueur accuse une trame', async () => {
    await ouvrir()
    const premiere = etat?.echeanceFilet
    vi.advanceTimersByTime(30_000)
    moteur.avancerMaintenant()
    await laisserTourner()
    // Rien n'est retenu entre l'accuse et la trame suivante : plus d'echeance.
    expect(etat?.echeanceFilet).toBeUndefined()
    courant = monde('Enemy Activation', 102)
    pousser()
    await laisserTourner()
    expect(etat?.trameRetenue).toBe(102)
    expect(etat?.echeanceFilet).toBe(Date.now() + DELAI_FILET_ANTI_BLOCAGE_CLIC_MS)
    expect(etat?.echeanceFilet).toBe((premiere ?? 0) + 30_000)
  })

  // LE CAS DE LA RELECTURE, en entier : cinq minutes de lecture, un clic par
  // minute. Le filet ne doit JAMAIS jouer, donc aucun accuse en trop.
  it('ne double jamais un joueur qui lit cinq minutes en cliquant chaque minute', async () => {
    await ouvrir()
    for (let clic = 0; clic < 5; clic += 1) {
      await vi.advanceTimersByTimeAsync(60_000)
      moteur.avancerMaintenant()
      await laisserTourner()
      courant = monde('Enemy Activation', 102 + clic)
      pousser()
      await laisserTourner()
    }
    // Un accuse par clic, et pas un de plus : les cinq trames validees.
    expect(accuses).toEqual([101, 102, 103, 104, 105])
    expect(etat?.trameRetenue).toBe(106)
    expect(etat?.echeanceFilet).toBe(Date.now() + DELAI_FILET_ANTI_BLOCAGE_CLIC_MS)
  })

  // MESURE EN JEU (07/09/2026, Spider-Man contre Rhino) : une SEULE trame
  // retenue peut porter deux etapes (la distribution puis la revelation). Le
  // « Suivant » qui passe de l'une a l'autre n'acquitte rien, le cartouche
  // n'etant pas encore a jour. Le filet ne voyait donc rien de ce clic-la :
  // clics a 60 s et 120 s, compte a rebours a 136 s, filet joue a 151 s.
  it('repousse l echeance sur un geste du joueur qui n acquitte rien', async () => {
    await ouvrir()
    const premiere = etat?.echeanceFilet
    vi.advanceTimersByTime(40_000)
    moteur.signalerActiviteDuJoueur()
    expect(etat?.trameRetenue).toBe(101)
    expect(accuses).toEqual([])
    expect(etat?.echeanceFilet).toBe((premiere ?? 0) + 40_000)
    // Et le filet ne joue donc pas a l'echeance d'origine.
    await vi.advanceTimersByTimeAsync(51_000)
    expect(accuses).toEqual([])
    await vi.advanceTimersByTimeAsync(40_000)
    expect(accuses).toEqual([101])
  })

  it('ne s arme pas sur un geste du joueur quand rien n est retenu', async () => {
    await ouvrir()
    // La premiere trame qui suit la phase (« End Phase », le Bilan) se retient
    // aussi (07/10/2026) : on la relache, puis le tour du joueur ne retient rien.
    courant = monde('End Phase', 102)
    pousser()
    await laisserTourner()
    await moteur.continuer()
    courant = monde('Player 1 Turn', 103)
    pousser()
    await laisserTourner()
    expect(etat?.echeanceFilet).toBeUndefined()
    moteur.signalerActiviteDuJoueur()
    expect(etat?.echeanceFilet).toBeUndefined()
  })

  it('relache la trame quand l echeance tombe, sans aucun clic', async () => {
    await ouvrir()
    expect(accuses).toEqual([])
    await vi.advanceTimersByTimeAsync(DELAI_FILET_ANTI_BLOCAGE_CLIC_MS)
    await laisserTourner()
    expect(accuses).toEqual([101])
  })

  // Le filet qui a joue ne laisse pas la suite de la phase sans protection.
  it('rearme un filet neuf sur la trame qui suit un declenchement', async () => {
    await ouvrir()
    await vi.advanceTimersByTimeAsync(DELAI_FILET_ANTI_BLOCAGE_CLIC_MS)
    await laisserTourner()
    expect(etat?.echeanceFilet).toBeUndefined()
    courant = monde('Enemy Activation', 102)
    pousser()
    await laisserTourner()
    expect(etat?.trameRetenue).toBe(102)
    expect(etat?.echeanceFilet).toBe(Date.now() + DELAI_FILET_ANTI_BLOCAGE_CLIC_MS)
    // Et il joue a son tour, 90 s plus tard.
    await vi.advanceTimersByTimeAsync(DELAI_FILET_ANTI_BLOCAGE_CLIC_MS)
    await laisserTourner()
    expect(accuses).toEqual([101, 102])
  })

  it('desarme le filet a la sortie de la phase du mechant', async () => {
    await ouvrir()
    expect(etat?.echeanceFilet).toBeDefined()
    // La trame du Bilan (« End Phase ») reste sous la protection du filet : un
    // onglet fantome ne doit pas la bloquer plus que les autres.
    courant = monde('End Phase', 102)
    pousser()
    await laisserTourner()
    expect(etat?.trameRetenue).toBe(102)
    expect(etat?.echeanceFilet).toBeDefined()
    await moteur.continuer()
    courant = monde('Player 1 Turn', 103)
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
