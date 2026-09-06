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
import { doitRattraperLesSieges, DELAI_PREMIERE_TRAME_MS } from './sieges-hot-seat'

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
 * Le rythme de la phase du mechant, en DEUX positions.
 *
 *  - « detaille »   : une etape a la fois, validee avant la suivante (clic
 *                     sur « Suivant » du cartouche). Le defaut.
 *  - « instantane » : rien ne retient le moteur ; le bilan de fin de phase
 *                     raconte apres coup.
 *
 * « Avance auto » (voir `lireAvanceAuto` / `ecrireAvanceAuto` plus bas) est
 * un REGLAGE, pas un troisieme mode : coche a l'interieur de « detaille », il
 * fait defiler chaque etape toute seule apres un delai au lieu d'attendre un
 * clic — c'est l'ancien mode « pas-a-pas ». L'ancien mode « manuel » (un
 * « Continue » a chaque evenement important, sans jamais rien montrer) a
 * simplement disparu : « detaille » fait la meme chose, en mieux, puisqu'il
 * montre l'evenement en plus d'attendre le clic.
 *
 * Le rythme est un confort de LECTURE, pas une regle du jeu : il est donc
 * personnel (localStorage), et en multijoueur chacun le sien.
 */
export type ModePhaseMechant = 'detaille' | 'instantane'

export const CLE_MODE_PHASE = 'marvel-board-mode-phase-mechant'
export const CLE_DELAI_PAS_A_PAS = 'marvel-board-delai-pas-a-pas'
/** Avance auto : reglage independant, qui ne veut rien dire hors de « detaille ». */
export const CLE_AVANCE_AUTO = 'marvel-board-avance-auto'

export const DELAI_PAS_A_PAS_DEFAUT = 1200
export const DELAI_PAS_A_PAS_MIN = 300
export const DELAI_PAS_A_PAS_MAX = 3000

// « detaille » d'abord : c'est le mode par defaut, celui qu'on a en arrivant.
export const MODES: ModePhaseMechant[] = ['detaille', 'instantane']

/**
 * MIGRATION de tout ce qui a existe avant les deux modes actuels. Deux cles
 * plus anciennes, dans l'ordre ou on les consulte :
 *
 *  1. `CLE_MODE_PHASE` pouvait deja contenir un des QUATRE anciens modes.
 *     « detaille » et « instantane » sont gardes tels quels. « manuel »
 *     devient « detaille » avec l'avance auto FAUSSE (ce joueur cliquait pour
 *     avancer, il continuera de cliquer). « pas-a-pas » devient « detaille »
 *     avec l'avance auto VRAIE (ce joueur regardait defiler, il continuera
 *     de regarder defiler).
 *  2. A defaut (cle absente ou valeur non reconnue), `CLE_PHASE_RAPIDE` -
 *     l'ancienne case a cocher d'avant les quatre modes : « off » menait a
 *     « manuel », donc desormais « detaille » sans avance auto ; toute autre
 *     valeur non nulle menait a « pas-a-pas », donc « detaille » AVEC avance
 *     auto ; son absence ne dit rien du tout, et retombe sur le vrai defaut.
 *
 * PURE (aucune ecriture) : `lireModePhaseMechant` et `lireAvanceAuto` y
 * puisent chacun leur part, sans qu'aucun des deux ne decide - ni n'ecrive -
 * a la place de l'autre.
 */
function migrerAncienReglage(): { mode: ModePhaseMechant; avanceAuto: boolean } {
  try {
    const brut = window.localStorage.getItem(CLE_MODE_PHASE)
    if (brut === 'manuel') return { mode: 'detaille', avanceAuto: false }
    if (brut === 'pas-a-pas') return { mode: 'detaille', avanceAuto: true }
    if (brut && (MODES as string[]).includes(brut)) {
      return { mode: brut as ModePhaseMechant, avanceAuto: false }
    }
    const ancienne = window.localStorage.getItem(CLE_PHASE_RAPIDE)
    if (ancienne === 'off') return { mode: 'detaille', avanceAuto: false }
    if (ancienne !== null) return { mode: 'detaille', avanceAuto: true }
    return { mode: 'detaille', avanceAuto: false }
  } catch {
    return { mode: 'detaille', avanceAuto: false }
  }
}

export function lireModePhaseMechant(): ModePhaseMechant {
  return migrerAncienReglage().mode
}

export function ecrireModePhaseMechant(mode: ModePhaseMechant): void {
  try {
    window.localStorage.setItem(CLE_MODE_PHASE, mode)
  } catch {
    /* stockage refuse : le mode vaudra pour la session, c'est tout */
  }
}

/**
 * Avance toute seule : meme regle de migration que `lireModePhaseMechant`,
 * lue de l'autre cote - si `CLE_AVANCE_AUTO` est absente, on retombe sur ce
 * que l'ancien reglage impliquait deja, plutot que sur le defaut FAUX qui
 * priverait un joueur d'un choix qu'il avait deja fait.
 */
export function lireAvanceAuto(): boolean {
  try {
    const brut = window.localStorage.getItem(CLE_AVANCE_AUTO)
    if (brut === 'on') return true
    if (brut === 'off') return false
  } catch {
    return false
  }
  return migrerAncienReglage().avanceAuto
}

export function ecrireAvanceAuto(actif: boolean): void {
  try {
    window.localStorage.setItem(CLE_AVANCE_AUTO, actif ? 'on' : 'off')
  } catch {
    /* idem */
  }
}

/**
 * Le libelle affiche dans le panneau Options pour CE mode precis.
 *
 * Une seule source pour l'affichage et pour le test : l'ancien ternaire a
 * trois branches (`manuel` / `pas-a-pas` / sinon « Instantane ») retombait
 * sur « Instantane » des que le mode valait « detaille », qui est pourtant
 * le defaut. Toute nouvelle partie affichait donc un mode faux.
 */
export function libelleModePhase(mode: ModePhaseMechant): string {
  switch (mode) {
    case 'detaille':
      return 'Détaillé'
    case 'instantane':
      return 'Instantané'
  }
}

/** Borne le delai : une valeur hors plage rendrait la phase injouable. */
export function bornerDelai(valeur: number): number {
  if (!Number.isFinite(valeur)) return DELAI_PAS_A_PAS_DEFAUT
  return Math.min(DELAI_PAS_A_PAS_MAX, Math.max(DELAI_PAS_A_PAS_MIN, Math.round(valeur)))
}

export function lireDelaiPasAPas(): number {
  try {
    const brut = window.localStorage.getItem(CLE_DELAI_PAS_A_PAS)
    return brut === null ? DELAI_PAS_A_PAS_DEFAUT : bornerDelai(Number(brut))
  } catch {
    return DELAI_PAS_A_PAS_DEFAUT
  }
}

export function ecrireDelaiPasAPas(valeur: number): void {
  try {
    window.localStorage.setItem(CLE_DELAI_PAS_A_PAS, String(bornerDelai(valeur)))
  } catch {
    /* idem */
  }
}

/**
 * Les quatre etapes de la phase du mechant, telles que le moteur les nomme
 * (game/world/phase.py). Memes cles que RecapPhaseMechant : c'est la carte de
 * reference, et le pas a pas doit raconter la meme histoire que le bilan.
 * Le point 5 (jeton de premier joueur) ne produit rien a montrer.
 */
export const PHASES_DU_MECHANT = new Set([
  'Main Scheme Place Threat',
  'Enemy Activation',
  'Deal Encounter Cards',
  'Reveal Encounter Cards',
])

/**
 * Ce qu'on montre en detaille, avance auto ou pas. Plus LARGE que
 * `evenementNarreImportant`, qui ne sert plus qu'a decider le bandeau central
 * de phase ennemie (board.tsx, `afficherEvenementCentrale`) : celui-ci ignore
 * les cartes de boost/rencontre et les statuts, qu'on veut pourtant voir
 * passer ici.
 *
 * Les statuts (etourdi/confus/tenace) s'ajoutent donc a la liste, et ils ne se
 * lisent PAS dans le texte : ils ont leurs propres evenements.
 */
/**
 * QUI retient l'accuse de reception, et pourquoi. Extrait de `lire()` pour etre
 * testable : c'est la seule regle qui decide du rythme, et une erreur ici rend
 * soit la phase illisible (on n'attend jamais), soit la partie bloquee (on
 * attend toujours).
 */
export type DecisionAccuse = 'immediat' | 'attendre-clic' | 'attendre-delai'

export function decisionAccuse(
  mode: ModePhaseMechant,
  monde: World | undefined,
  phaseSautee: boolean,
  avanceAuto: boolean
): DecisionAccuse {
  if (mode === 'instantane') return 'immediat'
  // « detaille » retient l'accuse de reception sur les quatre phases du
  // mechant, et seulement sur un evenement a montrer (sans ce filtre, chaque
  // deplacement de carte deviendrait une etape et la phase durerait des
  // minutes). « Tout passer » (phaseSautee) court-circuite tout ca.
  const phase = monde?.phase ?? ''
  if (phaseSautee || !PHASES_DU_MECHANT.has(phase) || !evenementAMontrer(monde)) return 'immediat'
  // Avance auto : l'etape se lit puis rend la main toute seule, sans manipuler
  // (l'ancien mode « pas-a-pas »). Sans elle, « detaille » VALIDE chaque etape
  // au clic (bouton « Suivant » du cartouche).
  return avanceAuto ? 'attendre-delai' : 'attendre-clic'
}

export function evenementAMontrer(monde: World | undefined): boolean {
  if (!monde) return false
  const nom = monde.event_name ?? ''
  if (nom === 'AfterUnitGainStatus' || nom === 'AfterUnitLostStatus') return true
  return evenementNarreImportant(monde)
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
  /**
   * Identifiant UNIQUE de la partie, tire au demarrage par le moteur.
   *
   * `game_id` ne suffit pas : il repart a 1 dans chaque processus moteur
   * (`game_session.py`), et le serveur en allume un par partie. Deux parties
   * successives portaient donc le meme numero, et le journal de la premiere
   * restait affiche sur la seconde. Vide sur un moteur qui ne l'envoie pas
   * encore : on retombe alors sur `game_id` seul.
   */
  game_uid: string
  ask_players: number[]
  total_players: number
  notifications: Notification[]
  /** Sièges dont plus aucun client ne tient la place. */
  siegesAbsents: number[]
}

/**
 * L'etiquette qui dit « c'est encore la meme partie ».
 *
 * Les deux morceaux comptent : `game_uid` distingue deux moteurs successifs,
 * `game_id` distingue deux parties dans un MEME moteur (« Rejouer » sans
 * quitter). Un moteur qui n'envoie pas encore l'uid retombe sur le numero seul.
 */
export function clePartie(trame: Pick<Trame, 'game_id' | 'game_uid'>): string {
  return `${trame.game_uid}:${trame.game_id}`
}

function lireTrame(brut: unknown): Trame | undefined {
  if (typeof brut !== 'object' || brut === null) return undefined
  const o = brut as Record<string, unknown>
  // Les messages de position de souris passent par le meme socket.
  if (typeof o.render_id !== 'number' || typeof o.game_id !== 'number') return undefined
  return {
    render_id: o.render_id,
    game_id: o.game_id,
    game_uid: typeof o.game_uid === 'string' ? o.game_uid : '',
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
 * Cette partie est-elle REPARTIE sur plusieurs machines ?
 *
 * Le salon pose `multi=1` sur le lien de chaque siege (salon/app.js). Le
 * lancement solo, lui, ouvre `/app/board.html` sans ce drapeau — y compris a
 * la reprise, qui passe `?p=0` : la seule presence de `p` ne suffit donc PAS
 * a distinguer les deux cas, d'ou un drapeau explicite.
 */
function estMultijoueur(): boolean {
  return new URLSearchParams(window.location.search).has('multi')
}

/**
 * Adresse du socket, sur la meme origine que la page.
 *
 * HOT-SEAT : hors multijoueur, on s'annonce pour TOUS les joueurs de la partie
 * et pas seulement celui de la vue. Sans cela, une partie a 2+ heros sur UN
 * ecran ne demarre jamais : le moteur attend la connexion de chaque joueur
 * (WaitConnect), et un client « p=0 » seul laisse le joueur 1 aux abonnes
 * absents.
 *
 * ⚠ MAIS JAMAIS EN MULTIJOUEUR. `hot_seat` fait rendre au serveur TOUS les
 * sieges (`get_player_ids`, server_base.py:90) des lors qu'aucun mot de passe
 * de siege n'est defini — `allowed_seats` rend alors `None`, donc aucun
 * filtrage. L'hote reservait ainsi les sieges de tout le monde et se voyait
 * interroge pour eux, cartes en main comprises. Signale en jeu : « en tant
 * qu'hote je vois toutes les cartes, alors que ceux qui rejoignent ne voient
 * bien que les leurs ». Les invites n'etaient pas touches parce qu'ils
 * arrivent sur un siege deja pris par l'hote.
 */
function adresseSocket(playerId: number): string {
  const protocole = window.location.protocol === 'https:' ? 'wss' : 'ws'
  const siege = estMultijoueur() ? `p=${playerId}` : `hot_seat&p=${playerId}`
  return `${protocole}://${window.location.host}/ws?${siege}`
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

/** Accuse reception d'une trame : pour TOUS les joueurs locaux en hot-seat,
 *  pour SON SEUL siege en multijoueur (meme raison que `adresseSocket`). */
export async function accuserReception(playerId: number, trame: Trame): Promise<void> {
  const siege = estMultijoueur() ? `p=${playerId}` : `hot_seat&p=${playerId}`
  await fetch(`/client_updated?${siege}&r=${trame.render_id}&g=${trame.game_id}`, {
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
  /**
   * Pas a pas : une etape est affichee et son echeance court. `enPause` fige
   * l'echeance jusqu'a nouvel ordre. Sert au plateau pour le clic « suite »,
   * l'indicateur de pause et le bouton « Tout passer ».
   */
  pasAPas: { actif: boolean; enPause: boolean }
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
  partieId?: string
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
    pasAPas: { actif: false, enPause: false },
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
  private mode: ModePhaseMechant = 'detaille'
  /** Avance auto : reglage independant, ne vaut que sous « detaille ». */
  private avanceAuto = false
  private delaiPasAPas = DELAI_PAS_A_PAS_DEFAUT
  private minuteurPasAPas: number | undefined
  private enPause = false
  /** « Tout passer » : vrai jusqu'a la SORTIE de la phase du mechant. */
  private phaseSautee = false

  setModePhaseMechant(mode: ModePhaseMechant) {
    this.mode = mode
    // Un accuse deja retenu ne doit pas rester en attente d'un geste qui
    // n'arrivera plus : changer de mode le libere immediatement. (L'ancien
    // mode « manuel », seul a devoir survivre a un changement de mode, a
    // disparu : plus rien n'exempte donc ce cas.)
    if (this.trameEnAttente) void this.continuer()
  }

  setDelaiPasAPas(ms: number) {
    this.delaiPasAPas = bornerDelai(ms)
  }

  setAvanceAuto(actif: boolean) {
    this.avanceAuto = actif
  }

  /** Clic du joueur : l'etape affichee a ete lue, on passe a la suivante. */
  avancerMaintenant(): void {
    if (this.trameEnAttente) void this.continuer()
  }

  /**
   * Espace : fige (ou relance) l'echeance. En pause on ne programme rien ; le
   * moteur attend, exactement comme en mode manuel.
   */
  basculerPause(): boolean {
    this.enPause = !this.enPause
    this.publier({ pasAPas: { actif: this.trameEnAttente !== undefined, enPause: this.enPause } })
    if (this.enPause) {
      if (this.minuteurPasAPas !== undefined) window.clearTimeout(this.minuteurPasAPas)
      this.minuteurPasAPas = undefined
    } else {
      this.programmerAvance()
    }
    return this.enPause
  }

  /** « Tout passer » : le reste de la phase defile sans s'arreter. */
  passerToutLaPhase(): void {
    this.phaseSautee = true
    this.enPause = false
    this.avancerMaintenant()
  }

  private programmerAvance(): void {
    if (this.minuteurPasAPas !== undefined) window.clearTimeout(this.minuteurPasAPas)
    this.minuteurPasAPas = undefined
    if (this.enPause || !this.trameEnAttente) return
    this.minuteurPasAPas = window.setTimeout(() => void this.continuer(), this.delaiPasAPas)
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
  private partieDesHautsFaits: string | undefined
  /** Les sieges ont deja ete reclames une fois : on ne recommence pas. */
  private siegesRattrapes = false
  /** Minuteur qui guette le silence apres l'ouverture du socket. */
  private guetteurSieges: number | undefined

  /**
   * Le recapitulatif de fin doit porter sur LA partie qui vient de finir. Sans
   * cette remise a zero, enchainer deux parties sans recharger la page ferait
   * reapparaitre les hauts faits de la premiere sur l'ecran de fin de la
   * seconde.
   */
  private oublierSiNouvellePartie(trame: Trame) {
    const cle = clePartie(trame)
    if (this.partieDesHautsFaits === cle) return
    this.partieDesHautsFaits = cle
    this.hautsFaits = []
    this.publier({ hautsFaits: this.hautsFaits, partieId: cle })
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

      // GUETTEUR DE SILENCE. Connecte avant que la partie soit montee, le
      // client ne tient AUCUN siege — et le moteur n'envoie ses trames qu'aux
      // clients d'un siege : le socket reste ouvert et parfaitement muet. On
      // rouvre alors une fois pour les reclamer. Voir sieges-hot-seat.ts.
      if (this.guetteurSieges !== undefined) window.clearTimeout(this.guetteurSieges)
      this.guetteurSieges = window.setTimeout(() => {
        this.guetteurSieges = undefined
        if (
          !doitRattraperLesSieges({
            multijoueur: estMultijoueur(),
            trameRecue: this.trame !== undefined,
            dejaRattrape: this.siegesRattrapes,
          })
        ) {
          return
        }
        if (!this.vivant) return
        this.siegesRattrapes = true
        socket.close()
        this.ouvrirSocket()
      }, DELAI_PREMIERE_TRAME_MS)
      // (le minuteur est annule des la premiere trame, a la fermeture du socket
      //  et a l'arret du moteur)
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
      this.oublierSiNouvellePartie(trame)

      // Une trame est arrivee : les sieges sont bien tenus (voir le guetteur
      // de silence pose a l'ouverture).
      if (this.guetteurSieges !== undefined) {
        window.clearTimeout(this.guetteurSieges)
        this.guetteurSieges = undefined
      }

      this.enregistrerHautsFaits(trame.notifications)
      this.publier({ siegesAbsents: trame.siegesAbsents })
      void this.lire()
    }

    socket.onclose = () => {
      this.trameEnAttente = undefined
      if (this.guetteurSieges !== undefined) {
        window.clearTimeout(this.guetteurSieges)
        this.guetteurSieges = undefined
      }
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
      // « Tout passer » ne vaut que pour LA phase en cours : des qu'on en sort,
      // le pas a pas reprend au round suivant sans rien demander.
      const dansLaPhase = PHASES_DU_MECHANT.has(monde?.phase ?? '')
      if (!dansLaPhase && this.phaseSautee) this.phaseSautee = false

      const decision = decisionAccuse(this.mode, monde, this.phaseSautee, this.avanceAuto)
      if (this.trame && decision === 'attendre-clic') {
        this.trameEnAttente = this.trame
        this.publier({ validationRequise: true })
        // Filet anti-blocage : auto-continue si personne ne clique (evite qu'un
        // client fantome bloque la phase ennemie pour tout le monde).
        if (this.minuteurAutoContinue !== undefined) window.clearTimeout(this.minuteurAutoContinue)
        this.minuteurAutoContinue = window.setTimeout(() => void this.continuer(), 6000)
      } else if (this.trame && decision === 'attendre-delai') {
        // On retient l'accuse le temps que l'etape se lise. Le moteur attend
        // sans limite (max_timeout = 0), c'est donc NOUS qui donnons le rythme :
        // aucun monde n'est bufferise, aucune desynchronisation possible.
        this.trameEnAttente = this.trame
        this.publier({ pasAPas: { actif: true, enPause: this.enPause } })
        this.programmerAvance()
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
    if (this.minuteurPasAPas !== undefined) {
      window.clearTimeout(this.minuteurPasAPas)
      this.minuteurPasAPas = undefined
    }
    const trame = this.trameEnAttente
    if (!trame) return
    this.trameEnAttente = undefined
    this.publier({ validationRequise: false, pasAPas: { actif: false, enPause: this.enPause } })
    await accuserReception(this.playerId, trame)
  }
}
