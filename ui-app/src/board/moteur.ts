// Le lien avec le moteur, pour une partie en cours.
//
// Trois choses, dans cet ordre, releve sur le runtime historique :
//
//  1. UN SOCKET, pas du sondage. /ws?p=<joueur> pousse un descripteur de trame
//     a chaque rendu : { render_id, game_id, ask_players, ... }. C'est la seule
//     source de `game_id`, et /get_world ne le contient pas.
//
//  2. UN ACCUSE DE RECEPTION OBLIGATOIRE. Apres chaque trame, il faut appeler
//     /client_updated?p=&r=<render_id>&g=<game_id>. Sans lui, le moteur reste
//     bloque : il attend dans DoWaitSync avec un delai de `max_timeout`, mesure
//     a 0 sur ce serveur, ce qui veut dire « sans limite ». Un client qui ouvre
//     le socket sans accuser reception gele la partie.
//
//  3. LA REPONSE. POST /post?p=<joueur> avec le corps JSON de la reponse, ou
//     « {} » pour annuler.

import { lireDemande, type Demande, type Reponse } from './ask'
import { chargerPartieEnCours } from './sources'
import type { World } from './world'

/** Phase du mechant acceleree : plus de « Continue » a chaque activation. */
export const CLE_PHASE_RAPIDE = 'marvel-board-phase-rapide'

export function lirePhaseRapide(): boolean {
  try {
    return window.localStorage.getItem(CLE_PHASE_RAPIDE) !== 'off'
  } catch {
    return true
  }
}

/**
 * Une notification poussee par le moteur (Notify.Show, cote Python). Elle arrive
 * dans `notify_texts`, chaque entree etant un objet DEJA serialise en JSON.
 */
export type Notification = { categorie: string; niveau: string; texte: string }

function lireNotifications(brut: unknown): Notification[] {
  if (!Array.isArray(brut)) return []
  const sorties: Notification[] = []
  for (const entree of brut) {
    if (typeof entree !== 'string') continue
    try {
      const o = JSON.parse(entree) as Record<string, unknown>
      if (typeof o.text !== 'string') continue
      sorties.push({
        categorie: typeof o.category === 'string' ? o.category : '',
        niveau: typeof o.level === 'string' ? o.level : '',
        texte: o.text,
      })
    } catch {
      /* notification illisible : elle ne vaut pas d'interrompre la trame */
    }
  }
  return sorties
}

/** Ce que le socket pousse a chaque rendu du moteur. */
export type Trame = {
  render_id: number
  game_id: number
  ask_players: number[]
  total_players: number
  notifications: Notification[]
  /** Sièges dont plus aucun client ne tient la place. */
  siegesAbsents: number[]
}

function lireTrame(brut: unknown): Trame | undefined {
  if (typeof brut !== 'object' || brut === null) return undefined
  const o = brut as Record<string, unknown>
  // Les messages de position de souris passent par le meme socket.
  if (typeof o.render_id !== 'number' || typeof o.game_id !== 'number') return undefined
  return {
    render_id: o.render_id,
    game_id: o.game_id,
    ask_players: Array.isArray(o.ask_players)
      ? o.ask_players.filter((x): x is number => typeof x === 'number')
      : [],
    total_players: typeof o.total_players === 'number' ? o.total_players : 1,
    notifications: lireNotifications(o.notify_texts),
    siegesAbsents: Array.isArray(o.sieges_absents)
      ? o.sieges_absents.filter((x): x is number => typeof x === 'number')
      : [],
  }
}

/**
 * Adresse du socket, sur la meme origine que la page.
 *
 * HOT-SEAT : on s'annonce pour TOUS les joueurs de la partie, pas seulement
 * celui de la vue. Sans cela, une partie a 2+ heros ne demarre jamais : le
 * moteur attend la connexion de chaque joueur (WaitConnect), et un client
 * « p=0 » seul laisse le joueur 1 aux abonnes absents.
 */
function adresseSocket(playerId: number): string {
  const protocole = window.location.protocol === 'https:' ? 'wss' : 'ws'
  return `${protocole}://${window.location.host}/ws?hot_seat&p=${playerId}`
}

/** Ce que le moteur demande, ou undefined s'il ne demande rien. */
export async function chargerDemande(playerId: number): Promise<Demande | undefined> {
  const reponse = await fetch(`/get_ask?p=${playerId}`, { cache: 'no-store' })
  if (!reponse.ok) return undefined
  const texte = await reponse.text()
  if (!texte.trim()) return undefined
  try {
    return lireDemande(JSON.parse(texte))
  } catch {
    return undefined
  }
}

/** Accuse reception d'une trame, pour TOUS les joueurs locaux (hot-seat). */
export async function accuserReception(playerId: number, trame: Trame): Promise<void> {
  await fetch(`/client_updated?hot_seat&p=${playerId}&r=${trame.render_id}&g=${trame.game_id}`, {
    cache: 'no-store',
  }).catch(() => undefined)
}

/**
 * Envoie la reponse au moteur.
 *
 * Le corps est le JSON brut, exactement comme le runtime historique
 * (public/js/marvel/buttons.js). Le serveur le passe par Unquote : les caracteres
 * du JSON n'ont rien a y perdre, mais le type de contenu doit rester
 * x-www-form-urlencoded, comme lui.
 */
export async function envoyerReponse(playerId: number, reponse: Reponse | null): Promise<void> {
  const corps = reponse === null ? '{}' : JSON.stringify(reponse)
  await fetch(`/post?p=${playerId}`, {
    method: 'POST',
    headers: { 'Content-type': 'application/x-www-form-urlencoded' },
    body: corps,
  })
}

/**
 * Pendant la phase ennemie, on ne s'arrete (Continue) que sur les evenements
 * IMPORTANTS choisis par le joueur : activation/attaque (A), boost (B), degats
 * (C), menace (D). Tout le reste (deplacements de cartes, exhaust/ready,
 * melanges, effets, marqueurs de phase) est saute automatiquement. On classe sur
 * le TEXTE de narration du moteur (anglais), le plus direct et ajustable.
 */
export function evenementNarreImportant(monde: World | undefined): boolean {
  if (!monde) return false
  // On classe sur event_name ET le texte : la menace s'affiche « gained 2⚠ »
  // (icone, sans le mot « threat »), mais l'event_name est « SchemePlaceThreat ».
  const s = `${monde.event_name ?? ''} ${monde.prompt ?? ''} ${monde.prompt_last_text ?? ''}`.toLowerCase()
  // LISTE BLANCHE de moments precis, pas de mots-cles larges : « boost » ou
  // « scheme » seuls attrapaient les etapes techniques (would count boost
  // icons, moved to boost pile, cards moved...), d'ou le « trop d'infos ».
  // BILINGUE : le moteur narre en anglais par defaut, en francais quand
  // translate_fr.json est actif (les motifs FR reprennent MOT POUR MOT les
  // gabarits de data/translate_fr.json — les garder synchronises).
  return (
    /would activate|will attack|will scheme|resolve this attack/.test(s) ||
    /s(?:'|’)appr[eê]te [aà] s(?:'|’)activer|va attaquer|va manigancer|r[eé]soudre cette attaque/.test(s) ||
    /gains? \d+ boost icon|gagne \d+ ic[oô]ne/.test(s) ||
    /is being revealed|en cours de r[eé]v[eé]lation/.test(s) ||
    /damage|threat|d[eé]g[aâ]t|menace/.test(s)
  )
}

export type EtatMoteur = {
  monde?: World
  demande?: Demande
  /** Vrai quand le moteur attend une reponse d'un joueur LOCAL (hot-seat). */
  aNous: boolean
  /** Joueur que le moteur interroge en ce moment (hot-seat : la vue le suit). */
  joueurDemande?: number
  erreur?: string
  /** Le socket est-il etabli ? Sans lui, la partie ne peut pas avancer. */
  connecte: boolean
  /** Le moteur attend une validation visuelle avant de poursuivre. */
  validationRequise: boolean
  /** Reconnexion : horodatage (ms) de la prochaine tentative, si programmee. */
  prochaineTentative?: number
  /** Nombre de tentatives de reconnexion depuis la coupure. */
  tentatives: number
  /** Titres des hauts faits débloqués depuis l'ouverture de la page. */
  hautsFaits: string[]
  /**
   * Sièges sans client connecté. Quand le moteur interroge l'un d'eux, la
   * partie s'arrête sans un mot : c'est ce champ qui permet de le dire.
   */
  siegesAbsents: number[]
  /**
   * Partie en cours, telle que le moteur la numérote. Change à chaque NOUVELLE
   * partie, mais PAS sur un retour en arrière — c'est ce qui permet à
   * l'historique de survivre à un « Annuler ».
   */
  partieId?: number
}

type Ecouteur = (etat: EtatMoteur) => void

/**
 * Suit une partie en cours : socket, lecture du monde et de la demande, accuse
 * de reception. Une seule instance par page.
 */
/**
 * Delais de reconnexion (s), comme le ConnectionManager du client original :
 * rapide d'abord, puis espace, plafonne. Remis a zero des que ca marche.
 */
const DELAIS_RECONNEXION = [2, 4, 8, 15, 30]

export class Moteur {
  private socket: WebSocket | null = null
  private trame: Trame | undefined
  private etat: EtatMoteur = {
    aNous: false,
    connecte: false,
    validationRequise: false,
    tentatives: 0,
    hautsFaits: [],
    siegesAbsents: [],
  }
  private ecouteurs = new Set<Ecouteur>()
  private relance: number | undefined
  private vivant = true
  /** Evite deux lectures simultanees quand les trames arrivent en rafale. */
  private lectureEnCours = false
  private lectureADemander = false
  private trameEnAttente: Trame | undefined
  /**
   * Filet anti-blocage de la phase ennemie. On retient l'accuse de reception
   * jusqu'au bouton Continue, mais le moteur attend l'ack de CHAQUE client
   * connecte : un onglet en trop ou une connexion fantome qui ne clique jamais
   * Continue bloquerait tout le monde. Ce minuteur auto-continue apres un delai,
   * ce qui casse le deadlock (et sert d'auto-avance si le joueur ne clique pas).
   */
  private minuteurAutoContinue: number | undefined

  /**
   * Phase du mechant acceleree : on n'attend plus le bouton « Continue ».
   *
   * C'est aussi ce qui SUPPRIME le risque de blocage a plusieurs clients : le
   * moteur attend l'accuse de CHAQUE client connecte, donc un seul onglet qui
   * ne clique jamais gelait la phase pour tout le monde. En accusant tout de
   * suite, plus personne ne retient personne.
   */
  private phaseRapide = false

  setPhaseRapide(actif: boolean) {
    this.phaseRapide = actif
    // Un accuse deja retenu ne doit pas rester en attente d'un clic qui
    // n'arrivera plus : on le libere immediatement.
    if (actif && this.trameEnAttente) void this.continuer()
  }

  constructor(private readonly playerId: number) {}

  ecouter(ecouteur: Ecouteur): () => void {
    this.ecouteurs.add(ecouteur)
    ecouteur(this.etat)
    return () => this.ecouteurs.delete(ecouteur)
  }

  private publier(modif: Partial<EtatMoteur>) {
    this.etat = { ...this.etat, ...modif }
    for (const ecouteur of this.ecouteurs) ecouteur(this.etat)
  }

  /**
   * Hauts faits debloques depuis l'ouverture de la page.
   *
   * Le moteur les annonce par Notify.Game (« Haut fait : <titre> », voir
   * game/achievements.py). Le serveur les pousse dans notify_texts, mais UNE
   * SEULE FOIS : Notify.Get() les consomme en les lisant. Il faut donc les
   * accumuler ici — sans quoi l'ecran de fin de partie n'aurait plus rien a
   * recapituler au moment de s'afficher.
   */
  private hautsFaits: string[] = []
  /** Partie a laquelle se rapporte la liste ci-dessus. */
  private partieDesHautsFaits: number | undefined

  /**
   * Le recapitulatif de fin doit porter sur LA partie qui vient de finir. Sans
   * cette remise a zero, enchainer deux parties sans recharger la page ferait
   * reapparaitre les hauts faits de la premiere sur l'ecran de fin de la
   * seconde.
   */
  private oublierSiNouvellePartie(gameId: number) {
    if (this.partieDesHautsFaits === gameId) return
    this.partieDesHautsFaits = gameId
    this.hautsFaits = []
    this.publier({ hautsFaits: this.hautsFaits, partieId: gameId })
  }

  private enregistrerHautsFaits(notifications: Notification[]) {
    // Mode Bac a sable : rien n'est enregistre. Un haut fait obtenu en
    // truquant la partie ne vaut rien, et le decouvrir apres coup devaluerait
    // tous les autres. Le filtre est ici, au plus pres de la source : le
    // moteur continue de les annoncer, on refuse simplement de les retenir.
    if (this.etat.monde?.mode_sandbox === true) return

    const nouveaux: string[] = []
    for (const notification of notifications) {
      const trouve = notification.texte.match(/^Haut fait\s*:\s*(.+)$/)
      if (!trouve) continue
      const titre = trouve[1].trim()
      if (this.hautsFaits.includes(titre) || nouveaux.includes(titre)) continue
      nouveaux.push(titre)
    }
    if (nouveaux.length === 0) return
    this.hautsFaits = [...this.hautsFaits, ...nouveaux]
    this.publier({ hautsFaits: this.hautsFaits })
  }

  demarrer() {
    this.vivant = true
    this.ouvrirSocket()
    // Premiere lecture sans attendre la premiere trame : la page montre la
    // partie tout de suite, meme si le moteur ne rend rien dans l'immediat.
    void this.lire()
  }

  arreter() {
    this.vivant = false
    if (this.relance !== undefined) window.clearTimeout(this.relance)
    if (this.minuteurAutoContinue !== undefined) window.clearTimeout(this.minuteurAutoContinue)
    this.socket?.close()
    this.socket = null
    this.ecouteurs.clear()
  }

  private ouvrirSocket() {
    if (!this.vivant) return

    const socket = new WebSocket(adresseSocket(this.playerId))
    this.socket = socket

    socket.onopen = () => {
      // Le serveur n'envoie la premiere trame qu'apres ce message (voir
      // websocket_handler : il attend un texte commencant par « Connected »).
      socket.send(`Connected ${window.location.href}`)
      this.publier({ connecte: true, erreur: undefined, tentatives: 0, prochaineTentative: undefined })
      // Rattrapage : tout ce qui s'est passe pendant la coupure.
      void this.lire()
    }

    socket.onmessage = (evenement) => {
      if (typeof evenement.data !== 'string') return
      let brut: unknown
      try {
        brut = JSON.parse(evenement.data)
      } catch {
        return
      }
      const trame = lireTrame(brut)
      if (!trame) return
      this.trame = trame
      this.oublierSiNouvellePartie(trame.game_id)
      this.enregistrerHautsFaits(trame.notifications)
      this.publier({ siegesAbsents: trame.siegesAbsents })
      void this.lire()
    }

    socket.onclose = () => {
      this.trameEnAttente = undefined
      if (this.minuteurAutoContinue !== undefined) {
        window.clearTimeout(this.minuteurAutoContinue)
        this.minuteurAutoContinue = undefined
      }
      if (!this.vivant) {
        this.publier({ connecte: false, validationRequise: false })
        return
      }
      // Reconnexion automatique avec repli progressif : le plateau affiche le
      // compte a rebours et propose « Reconnect now » (voir BandeauConnexion).
      const tentatives = this.etat.tentatives + 1
      const delai =
        DELAIS_RECONNEXION[Math.min(tentatives - 1, DELAIS_RECONNEXION.length - 1)] * 1000
      this.publier({
        connecte: false,
        validationRequise: false,
        tentatives,
        prochaineTentative: Date.now() + delai,
      })
      this.relance = window.setTimeout(() => this.ouvrirSocket(), delai)
    }

    socket.onerror = () => {
      this.publier({ connecte: false })
    }
  }

  /** Relit le monde et la demande, puis accuse reception. */
  async lire(): Promise<void> {
    if (this.lectureEnCours) {
      this.lectureADemander = true
      return
    }
    this.lectureEnCours = true

    try {
      const monde = await chargerPartieEnCours(this.playerId)
      // Hot-seat : tous les joueurs sont locaux. On repond pour CELUI que le
      // moteur interroge, quel qu'il soit ; la vue le suit (voir PagePartie).
      const interroge = this.trame ? this.trame.ask_players[0] : this.playerId
      const aNous = interroge !== undefined
      const demande = aNous ? await chargerDemande(interroge!) : undefined
      this.publier({ monde, demande, aNous, joueurDemande: interroge, erreur: undefined })

      // APRES avoir lu : le moteur peut repartir. Pendant la phase ennemie, on
      // retient volontairement cet accuse de reception jusqu'au bouton Continue,
      // MAIS seulement pour les evenements IMPORTANTS (activation/attaque, boost,
      // degats, menace). Les etapes de detail (deplacements, exhaust, melanges,
      // effets, marqueurs) sont accusees tout de suite -> passees sans Continue.
      if (
        this.trame &&
        !this.phaseRapide &&
        monde?.phase === 'Enemy Activation' &&
        evenementNarreImportant(monde)
      ) {
        this.trameEnAttente = this.trame
        this.publier({ validationRequise: true })
        // Filet anti-blocage : auto-continue si personne ne clique (evite qu'un
        // client fantome bloque la phase ennemie pour tout le monde).
        if (this.minuteurAutoContinue !== undefined) window.clearTimeout(this.minuteurAutoContinue)
        this.minuteurAutoContinue = window.setTimeout(() => void this.continuer(), 6000)
      } else if (this.trame) {
        await accuserReception(this.playerId, this.trame)
      }
    } catch (cause: unknown) {
      this.publier({ erreur: cause instanceof Error ? cause.message : String(cause) })
    } finally {
      this.lectureEnCours = false
      if (this.lectureADemander) {
        this.lectureADemander = false
        void this.lire()
      }
    }
  }

  /** Repond au moteur, puis relit. `null` annule. */
  async repondre(reponse: Reponse | null, bindPlayerId = this.playerId): Promise<void> {
    try {
      await envoyerReponse(bindPlayerId, reponse)
      this.publier({ demande: undefined })
      await this.lire()
    } catch (cause: unknown) {
      this.publier({ erreur: cause instanceof Error ? cause.message : String(cause) })
    }
  }

  /** Retente la connexion tout de suite, sans attendre le compte a rebours. */
  reconnecterMaintenant(): void {
    if (!this.vivant || this.etat.connecte) return
    if (this.relance !== undefined) {
      window.clearTimeout(this.relance)
      this.relance = undefined
    }
    this.publier({ prochaineTentative: undefined })
    this.ouvrirSocket()
  }

  /** Autorise le moteur a poursuivre le rendu ennemi actuellement affiche. */
  async continuer(): Promise<void> {
    if (this.minuteurAutoContinue !== undefined) {
      window.clearTimeout(this.minuteurAutoContinue)
      this.minuteurAutoContinue = undefined
    }
    const trame = this.trameEnAttente
    if (!trame) return
    this.trameEnAttente = undefined
    this.publier({ validationRequise: false })
    await accuserReception(this.playerId, trame)
  }
}
