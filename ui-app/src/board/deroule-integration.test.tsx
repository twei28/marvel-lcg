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
import { AttenteTable } from './AttenteTable'
import { DELAI_SILENCE_TABLE_MS, useTableSilencieuse } from './attente-table'
import { DeroulePhase } from './DeroulePhase'
import { etapesDeroule } from './deroule-phase'
import { Moteur, PHASES_DU_MECHANT, type EtatMoteur } from './moteur'
import { moteurAttendUneReponse } from './DemandeCentrale'
import type { Demande } from './ask'
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
  /** Tous les sockets ouverts, dans l'ordre : le cas multi en veut deux. */
  static tous: FauxSocket[] = []
  constructor(public readonly url: string) {
    FauxSocket.dernier = this
    FauxSocket.tous.push(this)
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
  /**
   * La QUESTION que le moteur pose au joueur, ou rien.
   *
   * Cote Python, elle n'arrive pas avec une nouvelle trame : `IsInputReady`
   * repousse la MEME (`WebSendRender(..., "GetInput")`) avec `ask_players`
   * rempli, pendant que le fil du jeu attend la reponse. C'est ce protocole-la
   * qui est rejoue ici.
   */
  question: Demande | undefined
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
        ask_players: this.question ? [0] : [],
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
    // Le moteur rend le corps de la question, ou rien du tout.
    const brut = serveur.question
      ? JSON.stringify({
          options_json: JSON.stringify(serveur.question.options),
          prompt_text: serveur.question.prompt_text,
          event_name: serveur.question.event_name,
          show_cancel: serveur.question.show_cancel,
          ability_type: serveur.question.ability_type,
        })
      : ''
    return Promise.resolve(new Response(brut, { status: 200 }))
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
    // Deux clients enchainent deux fois plus de lectures : le compte est
    // large a dessein, il ne coute rien et evite un rendu hors `act`.
    for (let tour = 0; tour < 32; tour += 1) await Promise.resolve()
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

  // LE DEFAUT LE PLUS COUTEUX DE LA JOURNEE, et le seul qu'aucun test du
  // cartouche ne pouvait voir : ce n'est pas le cartouche qui relachait le
  // moteur, c'est le plateau qui redisait son MODE.
  //
  // board.tsx redit le mode au moteur dans un effet. Cet effet dependait d'une
  // fonction recreee a chaque rendu, donc il rejouait a chaque trame — et
  // `setModePhaseMechant` relachait la trame retenue « pour ne pas la laisser
  // en attente d'un geste qui n'arrivera plus ». Mesure en partie reelle
  // (07/09/2026, pile d'appels relevee dans le navigateur) : la phase du
  // mechant entiere defilait sans un clic, quoi que le cartouche decide.
  it('ne relache rien quand on redit au moteur le mode qu il a deja', async () => {
    await ouvrir()
    expect(serveur.accuses).toEqual([])
    // Le plateau redit son mode, dix fois, comme le faisait son effet.
    for (let n = 0; n < 10; n += 1) {
      await act(async () => {
        moteur.setModePhaseMechant('detaille')
      })
      await laisserTourner()
    }
    // Le moteur n'a pas bouge d'une trame, et le joueur lit toujours la meme
    // etape.
    expect(serveur.accuses).toEqual([])
    expect(serveur.rang).toBe(0)
    expect(screen.getByText(/Assault on NORAD gagne 1 menace/)).toBeInTheDocument()
  })

  // LE PIEGE NOMME PAR LA REVUE D'A3-FIX, ET SA SORTIE.
  //
  // Le jour ou `!validationRequise` quitte le signal « le moteur attend le
  // joueur », deux choses arrivent en meme temps pendant la fenetre d'annonce :
  // le cartouche se REPLIE devant la question (il n'a donc plus de bouton
  // « Suivant ») et, si `!questionAuJoueur` restait dans `cartoucheAJour`,
  // l'accuse de reception ne partirait plus. Plus personne ne relacherait la
  // trame : blocage jusqu'au filet de 90 s.
  //
  // La sortie : une question posee au joueur est une RAISON D'ACQUITTER, pas
  // une raison de retenir. Elle ne coute rien au rythme, parce que le moteur ne
  // peut de toute facon rien produire de plus tant qu'on ne lui a pas repondu
  // (Python : `Render` -> `WaitSync` -> `GetInput`, les trois a la suite sur le
  // meme fil). Elle ferme le blocage par construction : cartouche replie
  // implique cartouche a jour, donc trame relachee.
  it('ne bloque pas quand le moteur pose sa question pendant la fenetre d annonce', async () => {
    await ouvrir()
    serveur.automatique = false
    // Le joueur valide la menace ; l'intention arrive.
    await act(async () => {
      fireEvent.click(suivant())
    })
    await laisserTourner()
    await act(async () => {
      serveur.libererLaSuite()
    })
    await laisserTourner()
    expect(screen.getByText('Drone va comploter contre Assault on NORAD')).toBeInTheDocument()
    expect(serveur.accuses).toEqual([101, 102])

    // LE MOTEUR POSE SA QUESTION, sur la MEME trame : il repousse la trame 102
    // avec `ask_players` rempli, exactement comme `IsInputReady`.
    serveur.question = {
      options: [
        {
          id: 1,
          name: 'Defend',
          bind_id: 0,
          bind_player_id: 0,
          all_legal_targets: [],
          target_num_range: [0, 0],
          target_payment: {},
          select_rule: '',
          target_must_include_traits: [],
          failure_reason: '',
          is_search: false,
        },
      ],
      prompt_text: 'Bishop is being attacked by Drone',
      event_name: 'WhenUnitBeingAttack',
      show_cancel: true,
      ability_type: 'Normal',
    }
    await act(async () => {
      serveur.pousser()
    })
    await laisserTourner()
    // Le cartouche se replie : plus de bouton « Suivant », et la fenetre de
    // reponse est dite.
    expect(screen.queryByRole('button', { name: /Suivant/i })).toBeNull()
    expect(screen.getByText('tu peux défendre ou répondre')).toBeInTheDocument()

    // ET LA TRAME SUIVANTE PART QUAND MEME. C'est le point : sans bouton, c'est
    // le seul chemin qui reste, et il doit rester ouvert.
    await act(async () => {
      serveur.libererLaSuite()
    })
    await laisserTourner()
    expect(serveur.accuses).toEqual([101, 102, 103])

    // La question repondue, le cartouche se redeploie sur la resolution et
    // redemande un clic : le rythme n'a rien perdu.
    serveur.question = undefined
    await act(async () => {
      serveur.pousser()
    })
    await laisserTourner()
    expect(screen.getByText('Drone complote contre Assault on NORAD')).toBeInTheDocument()
    expect(serveur.accuses).toEqual([101, 102, 103])
  })

  // Le contre-cas, qui garde la raison d'etre du relachement : passer en
  // Instantane, c'est dire qu'on n'attendra plus rien, et une trame retenue ne
  // doit pas rester suspendue a un geste qui n'arrivera jamais.
  it('relache la trame retenue quand le mode CHANGE vraiment', async () => {
    await ouvrir()
    expect(serveur.accuses).toEqual([])
    await act(async () => {
      moteur.setModePhaseMechant('instantane')
    })
    await laisserTourner()
    expect(serveur.accuses[0]).toBe(101)
  })
})

// ------------------------------------------------------------------ MULTI
//
// LE CAS F5 DE L'AUDIT, monte pour de vrai : deux clients sur le meme faux
// serveur, l'un en Instantane, l'autre en Detaille. Le moteur Python n'avance
// qu'une fois que TOUS les clients ont accuse reception (`WaitSync`) : le
// premier acquitte donc tout de suite et attend le second, sans rien pour le
// lui dire. « Le joueur en Instantane voit son plateau se figer sans aucun
// cartouche, aucun bouton, aucun message. »

/** Le meme faux moteur, mais qui compte les accuses de CHAQUE siege. */
class FauxServeurMulti {
  rang = 0
  accuses: { siege: number; trame: number }[] = []
  private sockets: FauxSocket[] = []
  private synchronises = new Map<number, number>()

  constructor(private readonly sieges: number[]) {}

  brancher(sockets: FauxSocket[]) {
    this.sockets = sockets
  }

  mondeCourant(): World {
    return PHASE[this.rang]!
  }

  pousser() {
    const monde = this.mondeCourant()
    const message = {
      data: JSON.stringify({
        render_id: monde.render_id,
        game_id: 1,
        game_uid: 'test',
        ask_players: [],
        total_players: this.sieges.length,
        notify_texts: [],
      }),
    }
    for (const socket of this.sockets) socket.onmessage?.(message)
  }

  accuser(siege: number, trame: number) {
    this.accuses.push({ siege, trame })
    this.synchronises.set(siege, Math.max(this.synchronises.get(siege) ?? 0, trame))
    const courante = this.mondeCourant().render_id
    // `WaitSync` : la trame n'est franchie que lorsque TOUS les sieges l'ont
    // acquittee. Un seul retardataire tient la table entiere.
    if (!this.sieges.every((s) => (this.synchronises.get(s) ?? 0) >= courante)) return
    if (this.rang + 1 >= PHASE.length) return
    this.rang += 1
    this.pousser()
  }
}

let serveurMulti: FauxServeurMulti

function fauxFetchMulti(url: string): Promise<Response> {
  if (url.startsWith('/get_world')) {
    return Promise.resolve(new Response(JSON.stringify(serveurMulti.mondeCourant()), { status: 200 }))
  }
  if (url.startsWith('/get_ask')) return Promise.resolve(new Response('', { status: 200 }))
  if (url.startsWith('/client_updated')) {
    const parametres = new URLSearchParams(url.split('?')[1] ?? '')
    serveurMulti.accuser(Number(parametres.get('p')), Number(parametres.get('r')))
    return Promise.resolve(new Response('', { status: 200 }))
  }
  return Promise.resolve(new Response('', { status: 404 }))
}

/**
 * Un client, dans SON mode. Le meme cablage que board.tsx pour ce que la phase
 * du mechant met en jeu, y compris la mention d'attente du joueur qui n'a pas
 * de cartouche.
 */
function TableMulti({ moteur, mode }: { moteur: Moteur; mode: 'detaille' | 'instantane' }) {
  const [etat, setEtat] = useState<EtatMoteur>()
  useEffect(() => moteur.ecouter(setEtat), [moteur])
  const monde = etat?.monde
  // Les hooks AVANT toute sortie : ce composant en a un `return null`.
  const silencieuse = useTableSilencieuse(
    monde?.render_id,
    Boolean(etat?.connecte) &&
      PHASES_DU_MECHANT.has(monde?.phase ?? '') &&
      etat?.trameRetenue === undefined
  )
  if (!etat || !monde) return null
  if (mode === 'instantane') return silencieuse ? <AttenteTable /> : null
  const etapes = etapesDeroule(monde.faits_mechant ?? [], [], monde.round_id, new Set([MECHANT_ID]))
  return (
    <DeroulePhase
      etapes={etapes}
      identitePhase={monde.round_id}
      phaseMechantEnCours={PHASES_DU_MECHANT.has(monde.phase)}
      questionAuJoueur={moteurAttendUneReponse(etat)}
      trameRetenue={etat.trameRetenue}
      onSuivant={() => moteur.avancerMaintenant()}
      onTerminer={() => moteur.avancerMaintenant()}
    />
  )
}

describe('deux clients, un en Instantane et un en Detaille', () => {
  let rapide: Moteur
  let lent: Moteur

  beforeEach(() => {
    window.localStorage.clear()
    FauxSocket.tous = []
    serveurMulti = new FauxServeurMulti([0, 1])
    vi.stubGlobal('WebSocket', FauxSocket as unknown as typeof WebSocket)
    vi.stubGlobal('fetch', vi.fn((url: string) => fauxFetchMulti(url)))
    rapide = new Moteur(0)
    rapide.setModePhaseMechant('instantane')
    lent = new Moteur(1)
    lent.setModePhaseMechant('detaille')
  })

  afterEach(() => {
    rapide.arreter()
    lent.arreter()
    vi.unstubAllGlobals()
    vi.useRealTimers()
  })

  async function ouvrir() {
    render(
      <>
        <TableMulti moteur={rapide} mode="instantane" />
        <TableMulti moteur={lent} mode="detaille" />
      </>
    )
    await act(async () => {
      rapide.demarrer()
      lent.demarrer()
    })
    expect(FauxSocket.tous).toHaveLength(2)
    serveurMulti.brancher(FauxSocket.tous)
    await act(async () => {
      for (const socket of FauxSocket.tous) socket.onopen?.()
    })
    serveurMulti.pousser()
    await laisserTourner()
  }

  const suivant = () => screen.getByRole('button', { name: /Suivant/i })

  it('le joueur en Instantane ne bloque rien et voit qu on attend quelqu un', async () => {
    vi.useFakeTimers()
    await ouvrir()
    // Le rapide a acquitte tout de suite ; le lent retient. La table n'a donc
    // pas franchi sa premiere trame.
    expect(serveurMulti.accuses).toEqual([{ siege: 0, trame: 101 }])
    expect(serveurMulti.rang).toBe(0)
    // Son plateau ne dit encore rien : l'attente ordinaire dure une fraction
    // de seconde, et une mention qui clignote serait pire que rien.
    expect(screen.queryByText("En attente d'un autre joueur")).not.toBeInTheDocument()

    await act(async () => {
      vi.advanceTimersByTime(DELAI_SILENCE_TABLE_MS)
    })
    expect(screen.getByText("En attente d'un autre joueur")).toBeInTheDocument()

    // Et le cartouche du joueur en Detaille, lui, montre bien son etape.
    expect(screen.getByText(/Assault on NORAD gagne 1 menace/)).toBeInTheDocument()
  })

  it('la phase avance au rythme du joueur en Detaille', async () => {
    await ouvrir()
    expect(serveurMulti.rang).toBe(0)

    // Le lent valide la menace : la table franchit sa trame, et le rapide
    // acquitte la suivante sans qu'on lui demande rien.
    await act(async () => {
      fireEvent.click(suivant())
    })
    await laisserTourner()
    expect(serveurMulti.rang).toBe(2)
    expect(screen.getByText('Drone complote contre Assault on NORAD')).toBeInTheDocument()

    for (let clic = 0; clic < 4; clic += 1) {
      await act(async () => {
        fireEvent.click(suivant())
      })
      await laisserTourner()
    }
    expect(serveurMulti.rang).toBe(PHASE.length - 1)
    // Le siege rapide a acquitte CHAQUE trame, et n'en a jamais retenu une :
    // le rythme est celui du lent, pas une course entre les deux.
    const parLeRapide = serveurMulti.accuses
      .filter((a) => a.siege === 0)
      .map((a) => a.trame)
    expect(parLeRapide).toEqual([101, 102, 103, 104, 105, 106, 107])
  })
})
