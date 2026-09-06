// LE CARTOUCHE BRANCHE SUR UN VRAI MOTEUR, avec un faux transport en memoire.
//
// Pourquoi ce test existe : les trois regressions du rythme de la phase du
// mechant sont toutes nees ENTRE deux fichiers testes separement. `moteur.ts`
// savait retenir ses trames, `DeroulePhase.tsx` savait compter ses etapes, et
// personne ne mesurait ce que les deux faisaient ensemble. Le defaut du
// 06/09/2026 (deux activations de sbires, la distribution et la revelation
// resolues sur UN seul clic) passait au travers des deux batteries.
//
// Le faux transport rejoue une phase trame par trame, exactement comme le
// moteur Python : une trame est poussee, et la SUIVANTE n'est poussee qu'une
// fois l'accuse de reception recu. Ce qu'on mesure : combien de trames le
// moteur a franchies, et combien de clics le joueur a donnes.
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { useEffect, useState } from 'react'
import { act, fireEvent, render, screen } from '@testing-library/react'
import { DeroulePhase } from './DeroulePhase'
import { etapesDeroule } from './deroule-phase'
import { Moteur, PHASES_DU_MECHANT, type EtatMoteur } from './moteur'
import { moteurAttendUneReponse } from './DemandeCentrale'
import type { FaitMechant, World } from './world'

const SBIRE_ID = 70
const MANIGANCE_ID = 9
const MECHANT_ID = 50

/** Un monde minimal : le cartouche ne lit que la phase, le round et les faits. */
function monde(phase: string, faits: FaitMechant[], render_id: number): World {
  return {
    render_id,
    round_id: 2,
    phase,
    prompt: '',
    players: [],
    cards: [],
    faits_mechant: faits,
  } as unknown as World
}

const menace: FaitMechant = {
  genre: 'menace',
  round_id: 2,
  phase: 'Main Scheme Place Threat',
  cible: 'Assault on NORAD',
  cible_id: MANIGANCE_ID,
  montant: 1,
  restant: 5,
  plafond: 10,
}

function annonce(id: number): FaitMechant {
  return {
    genre: 'manigance',
    etat: 'annonce',
    activation_id: id,
    round_id: 2,
    phase: 'Enemy Activation',
    auteur: 'Drone',
    auteur_id: SBIRE_ID + id,
    cible: 'Assault on NORAD',
    cible_id: MANIGANCE_ID,
    base: 1,
  }
}

function resolue(id: number, restant: number): FaitMechant {
  return {
    ...annonce(id),
    etat: 'resolu',
    boost: 0,
    defense: 0,
    inflige: 1,
    subi: 1,
    restant,
    boosts: [],
  } as FaitMechant
}

/**
 * LA PHASE REJOUEE, une trame par ligne, dans l'ordre ou le moteur les rend.
 *
 * Les deux temps de chaque activation sont dans DEUX trames distinctes (le
 * moteur redessine entre l'annonce et la resolution), et le fait resolu
 * REMPLACE le fait d'intention : la liste des faits ne s'allonge pas. C'est
 * exactement la forme qui trompait le cartouche.
 */
const PHASE: World[] = [
  monde('Main Scheme Place Threat', [menace], 101),
  monde('Enemy Activation', [menace, annonce(1)], 102),
  monde('Enemy Activation', [menace, resolue(1, 4)], 103),
  monde('Enemy Activation', [menace, resolue(1, 4), annonce(2)], 104),
  monde('Enemy Activation', [menace, resolue(1, 4), resolue(2, 3)], 105),
  monde('Deal Encounter Cards', [
    menace,
    resolue(1, 4),
    resolue(2, 3),
    {
      genre: 'distribution',
      round_id: 2,
      phase: 'Deal Encounter Cards',
      joueur: 0,
      joueur_nom: 'Bishop',
    },
  ], 106),
  monde('Reveal Encounter Cards', [
    menace,
    resolue(1, 4),
    resolue(2, 3),
    {
      genre: 'distribution',
      round_id: 2,
      phase: 'Deal Encounter Cards',
      joueur: 0,
      joueur_nom: 'Bishop',
    },
    {
      genre: 'revelation',
      round_id: 2,
      phase: 'Reveal Encounter Cards',
      joueur: 0,
      joueur_nom: 'Bishop',
      carte: 'Drone Swarm',
      carte_id: 88,
    },
  ], 107),
]

/** Le socket du moteur, remplace par un canal en memoire. */
class FauxSocket {
  static dernier: FauxSocket | undefined
  onopen: (() => void) | null = null
  onmessage: ((evenement: { data: unknown }) => void) | null = null
  onclose: (() => void) | null = null
  onerror: (() => void) | null = null
  constructor(public readonly url: string) {
    FauxSocket.dernier = this
  }
  send() {
    /* le faux serveur n'ecoute rien : il pousse quand on l'accuse */
  }
  close() {
    this.onclose?.()
  }
}

/**
 * Le faux moteur : il pousse une trame, puis attend son accuse de reception
 * pour pousser la suivante. Exactement le protocole du moteur Python en mode
 * Detaille (`max_timeout = 0`).
 */
class FauxServeur {
  rang = 0
  accuses: number[] = []
  /**
   * Faux : les trames ne partent plus toutes seules, le test les libere une
   * par une. Cela sert a tenir le cartouche SUR une intention le temps d'un
   * clic — le geste meme qui a fait defiler toute la phase en partie reelle.
   */
  automatique = true
  private socket: FauxSocket | undefined

  brancher(socket: FauxSocket) {
    this.socket = socket
  }

  mondeCourant(): World {
    return PHASE[this.rang]!
  }

  pousser() {
    const monde = this.mondeCourant()
    this.socket?.onmessage?.({
      data: JSON.stringify({
        render_id: monde.render_id,
        game_id: 1,
        game_uid: 'test',
        ask_players: [],
        total_players: 1,
        notify_texts: [],
      }),
    })
  }

  accuser(renderId: number) {
    this.accuses.push(renderId)
    // Un accuse en retard (trame deja depassee) ne fait pas avancer le moteur.
    if (renderId !== this.mondeCourant().render_id) return
    if (!this.automatique) return
    this.libererLaSuite()
  }

  /** Le moteur passe a la trame suivante et la pousse. */
  libererLaSuite() {
    if (this.rang + 1 >= PHASE.length) return
    this.rang += 1
    this.pousser()
  }
}

let serveur: FauxServeur

function fauxFetch(url: string): Promise<Response> {
  if (url.startsWith('/get_world')) {
    return Promise.resolve(
      new Response(JSON.stringify(serveur.mondeCourant()), { status: 200 })
    )
  }
  if (url.startsWith('/get_ask')) {
    return Promise.resolve(new Response('', { status: 200 }))
  }
  if (url.startsWith('/client_updated')) {
    const renderId = Number(new URLSearchParams(url.split('?')[1] ?? '').get('r'))
    serveur.accuser(renderId)
    return Promise.resolve(new Response('', { status: 200 }))
  }
  return Promise.resolve(new Response('', { status: 404 }))
}

/** Le plateau, reduit a ce que la phase du mechant met en jeu. */
function Table({ moteur }: { moteur: Moteur }) {
  const [etat, setEtat] = useState<EtatMoteur>()
  useEffect(() => moteur.ecouter(setEtat), [moteur])
  const monde = etat?.monde
  if (!etat || !monde) return null
  // Le meme cablage que board.tsx, aux seuls arguments que la phase demande.
  const etapes = etapesDeroule(
    monde.faits_mechant ?? [],
    [],
    monde.round_id,
    new Set([MECHANT_ID])
  )
  return (
    <DeroulePhase
      etapes={etapes}
      identitePhase={monde.round_id}
      phaseMechantEnCours={PHASES_DU_MECHANT.has(monde.phase)}
      partieFinie={false}
      questionAuJoueur={moteurAttendUneReponse(etat)}
      trameRetenue={etat.trameRetenue}
      onSuivant={() => moteur.avancerMaintenant()}
      onTerminer={() => moteur.avancerMaintenant()}
    />
  )
}

/** Laisse les lectures asynchrones du moteur (fetch) se terminer. */
async function laisserTourner() {
  await act(async () => {
    for (let tour = 0; tour < 12; tour += 1) await Promise.resolve()
  })
}

describe('le cartouche branche sur un vrai moteur', () => {
  let moteur: Moteur

  beforeEach(() => {
    window.localStorage.clear()
    serveur = new FauxServeur()
    vi.stubGlobal('WebSocket', FauxSocket as unknown as typeof WebSocket)
    vi.stubGlobal('fetch', vi.fn((url: string) => fauxFetch(url)))
    moteur = new Moteur(0)
    moteur.setModePhaseMechant('detaille')
  })

  afterEach(() => {
    moteur.arreter()
    vi.unstubAllGlobals()
  })

  async function ouvrir() {
    render(<Table moteur={moteur} />)
    await act(async () => {
      moteur.demarrer()
    })
    const socket = FauxSocket.dernier
    expect(socket).toBeDefined()
    serveur.brancher(socket!)
    await act(async () => {
      socket!.onopen?.()
    })
    await laisserTourner()
    serveur.pousser()
    await laisserTourner()
  }

  const suivant = () => screen.getByRole('button', { name: /Suivant/i })

  // LE TEST QUI AURAIT ATTRAPE LE DEFAUT. Le moteur ne doit franchir aucune
  // trame que le joueur n'a pas validee, sauf celles qui n'annoncent qu'une
  // intention (decision 7 : pas de clic sur « va comploter »).
  it('ne franchit pas une trame sans un clic sur une etape resolue', async () => {
    await ouvrir()
    // Trame 1 : la menace. Le moteur est retenu, le cartouche la montre.
    expect(screen.getByText(/Assault on NORAD gagne 1 menace/)).toBeInTheDocument()
    expect(serveur.rang).toBe(0)

    // Le joueur valide la menace. Le moteur avance d'une trame — l'intention
    // du premier sbire — puis d'une seconde toute seule (l'intention ne coute
    // pas de clic), et s'arrete sur la RESOLUTION.
    await act(async () => {
      fireEvent.click(suivant())
    })
    await laisserTourner()
    expect(serveur.rang).toBe(2)
    expect(screen.getByText('Drone complote contre Assault on NORAD')).toBeInTheDocument()

    // Deuxieme clic : meme chose pour le second sbire.
    await act(async () => {
      fireEvent.click(suivant())
    })
    await laisserTourner()
    expect(serveur.rang).toBe(4)
    expect(screen.getByText('Drone complote contre Assault on NORAD')).toBeInTheDocument()

    // Troisieme clic : la distribution. Elle n'a pas de second temps, le
    // moteur s'arrete donc dessus.
    await act(async () => {
      fireEvent.click(suivant())
    })
    await laisserTourner()
    expect(serveur.rang).toBe(5)
    expect(screen.getByText('Bishop reçoit sa carte rencontre')).toBeInTheDocument()

    // Quatrieme clic : la revelation, la derniere trame de la phase.
    await act(async () => {
      fireEvent.click(suivant())
    })
    await laisserTourner()
    expect(serveur.rang).toBe(6)
    expect(screen.getByText('Bishop révèle Drone Swarm')).toBeInTheDocument()
  })

  // Le compte, sechement : CINQ clics pour SEPT trames — la menace, les deux
  // activations resolues, la distribution, la revelation. Les deux trames
  // franchies sans clic sont les deux intentions, et rien d'autre.
  it('acquitte chaque trame une fois, et une seule', async () => {
    await ouvrir()
    for (let clic = 0; clic < 5; clic += 1) {
      await act(async () => {
        fireEvent.click(suivant())
      })
      await laisserTourner()
    }
    expect(serveur.rang).toBe(PHASE.length - 1)
    // Sept trames, sept accuses : aucune trame relachee deux fois, aucune
    // rafale.
    expect(serveur.accuses).toEqual([101, 102, 103, 104, 105, 106, 107])
  })

  // LE GESTE MESURE EN PARTIE REELLE. Le joueur clique pendant que le
  // cartouche affiche l'intention (elle reste a l'ecran tant que le moteur
  // resout, et le bouton « Suivant » y est). Ce clic ne doit pas valider par
  // avance la resolution, qui n'est pas encore arrivee : sinon le moteur
  // repart pour toute la phase, et le joueur ne lit plus rien.
  it("ne s'emballe pas quand le joueur clique pendant la fenetre d'annonce", async () => {
    await ouvrir()
    // On tient le moteur a la main a partir d'ici : on veut voir l'intention.
    serveur.automatique = false
    await act(async () => {
      fireEvent.click(suivant())
    })
    await laisserTourner()
    // Trame de l'intention.
    await act(async () => {
      serveur.libererLaSuite()
    })
    await laisserTourner()
    expect(screen.getByText('Drone va comploter contre Assault on NORAD')).toBeInTheDocument()
    // L'intention a ete acquittee toute seule (decision 7), et c'est bien.
    expect(serveur.accuses).toEqual([101, 102])

    // LE CLIC DE TROP. Il ne doit rien relacher de plus.
    await act(async () => {
      fireEvent.click(suivant())
    })
    await laisserTourner()
    expect(serveur.accuses).toEqual([101, 102])

    // La resolution arrive et prend la place de l'intention, sans allonger la
    // liste des faits. Le cartouche la MONTRE et la retient.
    await act(async () => {
      serveur.libererLaSuite()
    })
    await laisserTourner()
    expect(screen.getByText('Drone complote contre Assault on NORAD')).toBeInTheDocument()
    expect(screen.queryByText('La suite arrive…')).not.toBeInTheDocument()
    expect(serveur.accuses).toEqual([101, 102])

    // Et c'est ce clic-la, sur le coup resolu, qui relache le moteur.
    await act(async () => {
      fireEvent.click(suivant())
    })
    await laisserTourner()
    expect(serveur.accuses).toEqual([101, 102, 103])
  })
})
