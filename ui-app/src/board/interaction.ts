// Le choix du joueur, entre la demande du moteur et la reponse postee.
//
// Deroulement, en une seule etape visible plutot que les trois du runtime
// historique (option, cibles, cout) : on choisit une option, puis on designe ses
// cibles et on paie, dans l'ordre qu'on veut, et « Valider » s'allume quand la
// reponse est complete.
//
// Le moteur reste l'arbitre : il valide la reponse et renvoie une nouvelle
// demande avec un failure_reason si elle ne lui convient pas. Cette couche
// n'essaie donc pas de reimplementer les regles, seulement de rendre le choix
// lisible et de ne pas proposer l'impossible.

import { useCallback, useEffect, useMemo, useRef, useState } from 'react'
import {
  coupSansEffet,
  coutParType,
  foisDisponible,
  paiementCourant,
  paiementFacultatif,
  paiementNulDUneAutreCarte,
  nombreDeRessources,
  typesManquants,
  valeurMoyen,
  valeurPayee,
  reponsePrete,
  type Avertissement,
  type Demande,
  type Paiement,
  type Option,
  type Reponse,
} from './ask'
import { toScanCard } from './card-model'
import { useConfirmation } from './ConfirmationJeu'
import type { Catalogue } from './catalogue'
import { optionsDeLaSource } from './glisser/cibles'
import { cibleRefuseeParLaRegle } from './regles-selection'
import { libellesCible } from './libelles-cible'
import { demandeHorsPanneauManigance } from './manigance-face-a'
import { t } from './langue'
import type { ScanCardProps } from '../components/ScanCard'
import type { World, WorldCard } from './world'

/** Ce qu'une carte peut faire dans l'interaction en cours. */
/** Auto-ciblage : quand une action n'a qu'UNE cible legale possible et en
    exige au moins une, elle est preselectionnee (desactivable, panneau ⚙). */
export const CLE_AUTO_CIBLE = 'marvel-board-auto-cible'

export function lireAutoCible(): boolean {
  try {
    return window.localStorage.getItem(CLE_AUTO_CIBLE) !== 'off'
  } catch {
    return true
  }
}

/** Validation courte : l'etape « valider » saute quand plus rien n'est a decider. */
export const CLE_VALIDATION_COURTE = 'marvel-board-validation-courte'

export function lireValidationCourte(): boolean {
  try {
    return window.localStorage.getItem(CLE_VALIDATION_COURTE) !== 'off'
  } catch {
    return true
  }
}

/**
 * Paiement automatique : quand une seule carte peut encore payer le reste du
 * cout (un seul payeur pulse), elle est payee toute seule au lieu d'attendre
 * le clic. Demande de l'utilisateur, 24/09/2026.
 *
 * TROIS etats, comme `ChoixFinTourAuto` (board/moteur.ts) : la premiere fois
 * que la situation se presente, une modale demande explicitement au joueur
 * s'il veut ce comportement. `'pas-demande'` = jamais repondu (la modale
 * doit encore s'afficher) ; `'on'`/`'off'` = deja repondu, plus jamais
 * redemande, modifiable a tout moment dans Reglages.
 */
export type ChoixPaiementAuto = 'pas-demande' | 'on' | 'off'
export const CLE_PAIEMENT_AUTO = 'marvel-board-paiement-auto'

function lirePaiementAuto(): ChoixPaiementAuto {
  try {
    const brut = window.localStorage.getItem(CLE_PAIEMENT_AUTO)
    return brut === 'on' || brut === 'off' ? brut : 'pas-demande'
  } catch {
    return 'pas-demande'
  }
}

function ecrirePaiementAuto(choix: 'on' | 'off'): void {
  try {
    window.localStorage.setItem(CLE_PAIEMENT_AUTO, choix)
  } catch {
    /* stockage refuse : le choix vaudra pour la session, c'est tout */
  }
}

export type RoleCarte =
  | 'porteur'
  | 'cible'
  | 'cible-preview'
  | 'ressource'
  | 'source'
  | 'indisponible'

export type EtatInteractif = {
  role: RoleCarte
  /** Deja choisie : cible retenue, ou ressource depensee. */
  choisie: boolean
  /** Combien de fois cette carte a ete choisie ou depensee. */
  fois?: number
  /**
   * Position (1-based) dans une selection dont l'ORDRE de clic compte, voir
   * `optionEstOrdonnee`. Absent hors de ce cas, ou si la carte n'est pas
   * encore choisie.
   */
  ordre?: number
  /**
   * Echange cette carte avec sa voisine de rang immediatement INFERIEUR dans
   * `cibles` (demande de l'utilisateur, 28/09/2026, sur le modele du bouton
   * « ← » de Felt Table/Flesh and Blood pour reordonner une selection : pas
   * de glisser-depose, deux boutons qui permutent avec le voisin). Absent
   * hors selection ordonnee, ou quand cette carte est deja en tete (rien a sa
   * gauche).
   */
  ordreReculer?: () => void
  /** Symetrique de `ordreReculer`, vers le voisin de rang superieur. */
  ordreAvancer?: () => void
  /**
   * Assigne d'un coup tout ce que cette carte peut encore recevoir dans une
   * selection repetable (`cibleRepetable`), plutot qu'un clic par point.
   * Demande de l'utilisateur relayee par Yarro (28/09/2026, nice-to-have) :
   * repartir des degats sur plusieurs sbires/allies se faisait clic par clic.
   * Absent hors selection repetable, ou quand cette carte est deja a son
   * maximum, ou qu'il ne reste rien a distribuer (voir `assignerResteQuantite`).
   */
  assignerReste?: () => void
  /** Combien de points `assignerReste` ajouterait en un seul clic. */
  assignerResteQuantite?: number
  /** Halo pulse temporaire depuis le menu d'action. */
  pulse?: boolean
  agir?: () => void
}

export type EtapeInteraction = 'action' | 'target' | 'payment' | 'confirm'

export type CoutSlot = {
  index: number
  rempli: boolean
  label?: string
  type?: string
}

export type AssistantInteraction = {
  etape: EtapeInteraction
  titre: string
  detail?: string
  /** Aide affichée quand une même carte accepte plusieurs attributions. */
  indice?: string
  cibleMinimum: number
  cibleMaximum: number
  cibleNombre: number
  ciblePossibles: number
  /** Vrai dès qu'une carte peut être désignée plus d'une fois. */
  cibleRepetable: boolean
  coutRequis?: number
  coutPaye: number
  coutSlots: CoutSlot[]
  coutRegles: string[]
  /** Ce qui manque type par type quand le coût est par types (design essai). */
  typesManquants?: Record<string, number>
}

/** Une cible que la table ne montre pas : elle passe par le selecteur. */
export type CibleHorsTable = {
  props: ScanCardProps
  choisie: boolean
  fois?: number
  /** Voir `EtatInteractif.ordre`. */
  ordre?: number
  /** Voir `EtatInteractif.ordreReculer`. */
  ordreReculer?: () => void
  /** Voir `EtatInteractif.ordreAvancer`. */
  ordreAvancer?: () => void
  /** Voir `EtatInteractif.assignerReste`. */
  assignerReste?: () => void
  /** Voir `EtatInteractif.assignerResteQuantite`. */
  assignerResteQuantite?: number
  agir: () => void
}

/**
 * La sélection en cours, telle que le joueur la publie au spectateur et à la
 * relecture (genre « sel ») : l'empreinte de la question, l'option, les cibles,
 * les ressources cochées, la carte et la cible focalisées, la carte lâchée.
 */
export type SelectionPartagee = {
  e: string
  o?: number
  c: number[]
  r: number[]
  cf?: number
  cb?: number
  sd?: number
}

const AUCUN: number[] = []

export type Interaction = {
  /** La sélection en cours, à publier pour le spectateur et la relecture. */
  selectionPartagee?: SelectionPartagee
  /** Option en cours de composition, s'il y en a une. */
  option?: Option
  cibles: number[]
  ressources: number[]
  /** Options proposees, dans l'ordre du moteur (filtrees sur la carte focalisee). */
  options: Option[]
  /**
   * Carte cliquee qui porte PLUSIEURS options (ex. le heros : attaque / blocage /
   * pouvoir) : ses options sont alors les seules affichees, comme un menu.
   */
  carteFocus?: number
  /**
   * Cible cliquee directement (ennemi, scheme, parfois personnage) : le panneau
   * central liste alors les actions disponibles qui peuvent viser CETTE carte.
   */
  cibleFocus?: number
  /** Referme le menu d'une carte multi-options. */
  defocaliser: () => void
  /** Ouvre le menu d'actions d'une carte, meme si elle n'a aucune action. */
  focaliserCarte: (id: number) => void
  /** Ouvre le menu des actions qui peuvent viser cette cible. */
  /**
   * Ouvre le menu des actions qui visent cette cible.
   *
   * `source` : la carte LÂCHÉE quand le menu vient d'un glisser-déposer. Le
   * menu se restreint alors à SES actions. Sans elle (un clic sur la cible),
   * il liste tout ce qui peut viser la carte.
   */
  focaliserCible: (id: number, source?: number) => void
  /** Par identifiant d'objet de carte. */
  cartes: Map<number, EtatInteractif>
  /**
   * Cibles legales absentes de la table, a proposer dans un selecteur.
   * Cas typique : une capacite de recherche cible les cartes du deck, dont la
   * table ne montre que le dessus.
   */
  ciblesHorsTable: CibleHorsTable[]
  /** Vide quand la reponse est complete. */
  raison: string
  prete: boolean
  /** Cout affichable, par exemple « 2 » ou « 1/2 ». */
  coutAffiche: string
  /**
   * La carte recompense un SURPAIEMENT : coût X, ou texte qui parle
   * d'« overpay ». L'assistant doit le dire, sans quoi le joueur confirme sans
   * rien dépenser et la carte ne fait rien. Signalé en jeu sur Tendril
   * Explosion (vr006), mais les neuf cartes à coût X du catalogue avaient le
   * même défaut, dont deux officielles.
   */
  surpaiementRecompense: boolean
  ciblesRestantes: number
  assistant: AssistantInteraction
  /**
   * Engage une action. `parGeste` dit que le joueur a DESIGNE sa cible d'un
   * geste (un glisser-deposer) et non d'un clic dans une liste : la validation
   * courte n'a alors plus de raison d'hesiter, voir `validationEvidente`.
   */
  choisirOption: (option: Option, ciblesInitiales?: number[], parGeste?: boolean) => void
  abandonnerOption: () => void
  valider: () => void
  annuler: () => void
  /**
   * Paiement automatique : 'pas-demande' tant que la modale d'accord n'a pas
   * encore ete posee, 'on'/'off' une fois repondu. Expose ici (plutot que lu
   * en localStorage a la volee, comme `autoCible`) pour que le panneau
   * Reglages reflete tout de suite la reponse donnee dans la modale, sans
   * attendre un remontage.
   */
  paiementAutoChoix: ChoixPaiementAuto
  basculerPaiementAuto: () => void
}

/** Toutes les cartes du monde, par identifiant d'objet. */
function indexerCartes(world: World | undefined): Map<number, WorldCard> {
  const index = new Map<number, WorldCard>()
  if (!world) return index

  const parcourir = (valeur: unknown) => {
    if (Array.isArray(valeur)) {
      for (const element of valeur) parcourir(element)
      return
    }
    if (typeof valeur !== 'object' || valeur === null) return
    const objet = valeur as Record<string, unknown>
    if (typeof objet.id === 'number' && typeof objet.card_type === 'string') {
      index.set(objet.id, objet as unknown as WorldCard)
    }
    for (const enfant of Object.values(objet)) parcourir(enfant)
  }

  parcourir(world)
  return index
}

/**
 * Les doublons dans all_legal_targets sont significatifs : le moteur les utilise
 * pour les selections reparties (ex. Falcon retire 1 menace par treachery, donc
 * la meme scheme peut etre choisie plusieurs fois si elle a assez de menace).
 */
function ciblesParOccurrence(option: Option): Map<number, number> {
  const occurrences = new Map<number, number>()
  for (const cible of option.all_legal_targets) {
    occurrences.set(cible, (occurrences.get(cible) ?? 0) + 1)
  }
  return occurrences
}

function nombreDeFois(cibles: number[], id: number): number {
  return cibles.filter((cible) => cible === id).length
}

function libelleRessource(resText: string): string {
  const lettres = (resText.match(/[rbyg]/gi) ?? []).join('').toUpperCase()
  return lettres || '*'
}

function slotsCout(
  paiement: Paiement | undefined,
  ressources: number[],
  requis: number | undefined
): CoutSlot[] {
  if (requis === undefined || requis <= 0) return []
  const texteParEffet = new Map<number, string>()
  for (const moyen of paiement?.payment ?? []) {
    if (!texteParEffet.has(moyen.effect_id)) texteParEffet.set(moyen.effect_id, moyen.res_text)
  }

  const remplis: Array<{ label: string; type: string }> = []
  for (const id of ressources) {
    const texte = texteParEffet.get(id) ?? ''
    const valeur = Math.max(1, valeurMoyen(texte))
    const label = libelleRessource(texte)
    for (let i = 0; i < valeur; i += 1) {
      remplis.push({ label, type: label.charAt(Math.min(i, label.length - 1)) || label })
    }
  }

  return Array.from({ length: requis }, (_, index) => ({
    index,
    rempli: index < remplis.length,
    label: remplis[index]?.type,
    type: remplis[index]?.type,
  }))
}

/** Le nom d'un type de ressource (les memes cles que la phrase d'etat du cout). */
const NOM_COULEUR: Record<string, string> = {
  R: 'physique',
  B: 'mental',
  Y: 'énergie',
  G: 'joker',
  L: 'éclair',
}

/**
 * Les mots de la confirmation « ce coup ne fera rien », dans la langue du
 * plateau. Une phrase par verrou et par mode, la couleur injectee APRES
 * traduction pour que l'ordre des mots reste juste dans les deux langues.
 */
export function textesCoupSansEffet(avertissement: Avertissement): { titre: string; texte: string } {
  const couleur = t(NOM_COULEUR[avertissement.ressource.toUpperCase()] ?? avertissement.ressource)
  const verrou =
    avertissement.mot_cle === 'Crisis'
      ? t('Une icône de Crise est en jeu : cette carte n’ignore la Crise que si elle est payée')
      : avertissement.mot_cle === 'Patrol'
        ? t('Une Patrouille est en jeu : cette carte n’ignore la Patrouille que si elle est payée')
        : t('Cette carte ne produit son effet que si elle est payée')
  const condition = avertissement.seulement
    ? t('uniquement avec des ressources de type {ressource}.')
    : t('avec au moins une ressource de type {ressource}.')
  return {
    titre: t('Ce coup ne retirera aucune menace'),
    texte: `${verrou} ${condition.replace('{ressource}', couleur)} ${t('Payée comme ça, elle sera défaussée sans rien retirer. Continuer quand même ?')}`,
  }
}

/** Les mots de l'avertissement « des points ne sont pas tous places ». */
export function textesPointsNonPlaces(restants: number): { titre: string; texte: string } {
  return {
    titre: t('Tout n’est pas placé'),
    texte: t('Il te reste {n} à placer. Si tu valides maintenant, ils seront perdus. Valider quand même ?').replace(
      '{n}',
      String(restants)
    ),
  }
}

function reglesCout(paiement: Paiement | undefined): string[] {
  return (paiement?.rule ?? [])
    .filter((regle) => regle !== 'UpTo')
    .map((regle) => regle.replace(/([a-z])([A-Z])/g, '$1 $2'))
}

function optionDemarreAuto(option: Option): boolean {
  return option.failure_reason === '' && option.name.toLowerCase().includes('mulligan')
}

/**
 * Une selection ou l'ORDRE de clic compte, pas seulement le fait d'etre
 * choisi : « Place on top »/« Place on bottom » (`PlaceOnTopInAnyOrder`,
 * `PlaceOnBottomInAnyOrder`, `PlaceOnTopAndOrBottomInAnyOrder`, cote moteur
 * `player_cards.py` -- Madame Web et une dizaine d'autres cartes) posent les
 * cartes sur le deck dans l'ordre INVERSE du clic (le dernier clic finit
 * dessus). Signalement Yarro n28 (27/09/2026) : rien a l'ecran ne montre cet
 * ordre, le joueur clique a l'aveugle. Meme famille pour l'ordre d'activation
 * des sbires (`ChooseOrder`, `enemies.py`).
 *
 * Reconnue par le NOM de l'option (`AbilityFactory.ForChoiceAbility(prompt)`
 * cote moteur pose ce texte comme nom de l'option) -- meme convention que
 * `optionDemarreAuto` juste au-dessus pour « mulligan ». Aucun champ dedie
 * n'existe cote moteur pour distinguer une selection ordonnee d'une simple
 * selection multiple ; ce nom est le seul signal disponible sans y toucher.
 */
function optionEstOrdonnee(option: Option | undefined): boolean {
  if (!option) return false
  // Le moteur remplace les espaces par des underscores dans `name`
  // (src/game/effect/effect.py, `remove_space`) : le format reel sur le
  // fil est "Place_on_top", pas "Place on top".
  return (
    option.name === 'Place_on_top' ||
    option.name === 'Place_on_bottom' ||
    option.name === 'Minion_Activates_Order'
  )
}

function estIdentiteJoueur(carte: WorldCard | undefined): boolean {
  return carte?.card_type === 'Hero' || carte?.card_type === 'AlterEgo'
}

/** Le nom du héros affiché à l'index `i` (celui de `world.players`), ou
    `undefined` si cet index n'a pas de héros nommé — un cas qu'on ne bloque
    jamais dessus, voir `texteAutreHeros` plus bas. */
function nomHeros(world: World | undefined, i: number): string | undefined {
  return world?.players?.[i]?.area_hero?.[0]?.name
}

/**
 * La confirmation « tu regardes un héros, mais l'action va agir pour un
 * autre » (24/09/2026, demande de l'utilisateur, capture à l'appui : « je
 * peux faire fin de tour en cliquant sur She-Hulk alors que c'est la phase
 * de Shuri »). Nomme les DEUX héros : dire seulement « ce n'est pas ton tour »
 * ne dirait pas pour qui le clic va compter.
 */
function texteAutreHeros(nomAffiche: string, nomCible: string): { titre: string; texte: string } {
  return {
    titre: t('Agir pour {heros} ?').replace('{heros}', nomCible),
    texte: t('Le plateau affiché est celui de {affiche}, pas de {heros}.')
      .replace('{affiche}', nomAffiche)
      .replace('{heros}', nomCible),
  }
}

export function useInteraction(
  world: World | undefined,
  /**
   * La demande BRUTE du moteur. Voir `demandeOrdinaire` juste en dessous : la
   * question de la face A de la manigance ne franchit pas cette porte.
   */
  demandeBrute: Demande | undefined,
  repondre: (reponse: Reponse | null, bindPlayerId: number) => void,
  /** Cartes que la table dessine vraiment. Voir Plateau.idsAffiches. */
  idsAffiches: Set<number>,
  playerId: number,
  catalogue: Catalogue,
  modeActions: 'simple' | 'detailed' = 'simple',
  /**
   * Pour chaque carte d'une pile, la carte que la pile montre (`Plateau.representantsDePile`).
   * Sert à garder dans la liste « hors table » la carte du DESSUS d'une pile, que la table
   * dessine donc déjà : voir `ciblesHorsTable`.
   */
  representantsDePile?: ReadonlyMap<number, number>,
  /**
   * SPECTATEUR ET RELECTURE (08/10/2026) : la sélection que le JOUEUR compose,
   * telle qu'il la publie (`selectionPartagee`, genre « sel » de vu-partage.ts).
   * `undefined` : ce plateau joue, il se sert de son propre état. `null` : il
   * regarde, et le joueur n'a rien en cours.
   */
  selectionImposee?: SelectionPartagee | null
): Interaction {
  const [idOptionLocal, setIdOption] = useState<number | undefined>(undefined)
  const [ciblesLocales, setCibles] = useState<number[]>([])
  const [ressourcesLocales, setRessources] = useState<number[]>([])
  const [carteFocusLocale, setCarteFocus] = useState<number | undefined>(undefined)
  const [cibleFocusLocale, setCibleFocus] = useState<number | undefined>(undefined)
  /**
   * La carte LÂCHÉE qui a ouvert ce menu de cible, quand il vient d'un dépôt.
   *
   * ⚠ SANS ELLE, LE GESTE PERD SA SOURCE. Défaut signalé en jeu le 15/09/2026 :
   * « quand je drag n drop mon perso sur le méchant, il me propose deux attack,
   * l'une d'elle c'est l'attaque avec un allié ». Le dépôt calculait bien les
   * actions de la carte lâchée, puis ouvrait ce menu-ci, qui les recalculait
   * sans elle : toutes les actions visant la cible revenaient, celles des
   * alliés comprises. `undefined` = la cible a été cliquée, pas reçue d'un
   * dépôt, et le menu liste alors tout ce qui peut la viser, ce qui est bien
   * son rôle.
   */
  const [sourceDepotLocale, setSourceDepot] = useState<number | undefined>(undefined)

  /**
   * ⚠ LA QUESTION DE LA MANIGANCE N'EXISTE PAS POUR LA TABLE. Son panneau la
   * tient (voir `demandeHorsPanneauManigance`) : sans cette porte, la table
   * posait son halo sur la manigance principale, son menu offrait l'option
   * sous son libellé technique, et en mode Détaillé le clic sur la carte
   * RÉPONDAIT, y compris pendant les 400 ms où l'overlay du panneau laisse
   * passer les clics, donc à la question suivante.
   *
   * La référence est inchangée pour toute autre demande : aucune dépendance de
   * hook n'est invalidée par ce passage.
   */
  const demande = demandeHorsPanneauManigance(demandeBrute, world)

  const options = demande?.options ?? []
  const optionsGenerales = useMemo(() => options.filter((o) => o.bind_id === 0), [options])

  // Une nouvelle demande annule toute composition en cours : les identifiants
  // d'options ne veulent plus rien dire d'une demande a l'autre.
  const empreinte = useMemo(
    () => `${demande?.event_name ?? ''}|${options.map((o) => o.id).join(',')}`,
    [demande?.event_name, options]
  )
  useEffect(() => {
    setIdOption(undefined)
    setCibles([])
    setRessources([])
    setCarteFocus(undefined)
    setCibleFocus(undefined)
    setSourceDepot(undefined)
  }, [empreinte])

  // Ce plateau regarde : la sélection est celle du joueur, si elle vise bien
  // la question affichée (une sélection d'une autre question ne veut rien dire).
  const regarde = selectionImposee !== undefined
  const imposee = regarde && selectionImposee && selectionImposee.e === empreinte ? selectionImposee : undefined
  const idOption = regarde ? imposee?.o : idOptionLocal
  const cibles = regarde ? (imposee?.c ?? AUCUN) : ciblesLocales
  const ressources = regarde ? (imposee?.r ?? AUCUN) : ressourcesLocales
  const carteFocus = regarde ? imposee?.cf : carteFocusLocale
  const cibleFocus = regarde ? imposee?.cb : cibleFocusLocale
  const sourceDepot = regarde ? imposee?.sd : sourceDepotLocale
  const selectionPartagee = useMemo<SelectionPartagee>(
    () => ({ e: empreinte, o: idOption, c: cibles, r: ressources, cf: carteFocus, cb: cibleFocus, sd: sourceDepot }),
    [empreinte, idOption, cibles, ressources, carteFocus, cibleFocus, sourceDepot]
  )

  const option = options.find((o) => o.id === idOption)
  const paiement = option ? paiementCourant(option, cibles) : undefined
  const requis = nombreDeRessources(paiement)
  const index = useMemo(() => indexerCartes(world), [world])
  // La carte que porte l'option recompense-t-elle un surpaiement ? (Ant-Man,
  // Wasp, Wonder Man : voir catalogue.surpayable.)
  const surpaiementRecompense =
    option !== undefined &&
    (catalogue.surpayable(index.get(option.bind_id)?.card_id ?? '') || paiementNulDUneAutreCarte(option))
  const identiteJoueurId = world?.players?.[playerId]?.area_hero?.[0]?.id

  /**
   * Cloisonnement main / réserve du pack Brawn.
   *
   * L'insert : « a player cannot generate resources by discarding cards from
   * both their reserve and their hand; they must choose one or the other. »
   *
   * Le moteur applique déjà la moitié déterministe de la règle (une carte jouée
   * depuis la main ne se finance que par la main, voir le # CORRECTIF de
   * game/ability/factory/resources.py). Mais il dresse la liste des payeurs
   * AVANT que le joueur ait choisi quoi que ce soit : pour un coût qui n'est ni
   * l'un ni l'autre — capacité d'une carte en jeu, coût d'une carte de
   * rencontre — les deux zones sont légitimement proposées, et c'est ICI, au
   * moment du choix, que le mélange doit être fermé.
   */
  const zonesDePaiement = useMemo(() => {
    const notre = world?.players?.[playerId]
    const idsDe = (liste: readonly { id: number }[] | undefined) =>
      new Set((liste ?? []).map((carte) => carte.id))
    return { main: idsDe(notre?.hand_cards), reserve: idsDe(notre?.reserve) }
  }, [world, playerId])

  /**
   * La zone déjà engagée dans le paiement en cours, s'il y en a une. On la
   * déduit des cartes dont une ressource est posée, et non d'un état séparé :
   * annuler un paiement rouvre donc l'autre zone tout seul.
   */
  const zoneEngagee = useMemo((): 'main' | 'reserve' | undefined => {
    if (ressources.length === 0) return undefined
    for (const [id, carte] of index) {
      if (!carte.resources.some((effectId) => ressources.includes(effectId))) continue
      if (zonesDePaiement.main.has(id)) return 'main'
      if (zonesDePaiement.reserve.has(id)) return 'reserve'
    }
    return undefined
  }, [ressources, index, zonesDePaiement])
  const paye = valeurPayee(paiement, ressources)
  const cibleMinimum = option?.target_num_range[0] ?? 0
  const cibleMaximum = option?.target_num_range[1] ?? 0
  const occurrences = useMemo(
    () => (option ? ciblesParOccurrence(option) : new Map<number, number>()),
    [option]
  )
  const ciblePossibles = occurrences.size
  // Une action « répartie » (43006 Regenerative Longevity : 4 soins entre
  // l'identité et Honey Badger) se reconnaît a ceci : le moteur repete la meme
  // carte dans all_legal_targets. Sans le dire, le joueur clique une fois,
  // valide, et n'obtient qu'un point.
  const cibleRepetable = [...occurrences.values()].some((nombre) => nombre > 1)
  const aDesCibles = option !== undefined && cibleMaximum > 0 && ciblePossibles > 0
  const ciblesOptionnelles = aDesCibles && cibleMinimum === 0
  const cibleManquantes = Math.max(0, cibleMinimum - cibles.length)
  const cibleRequise = option !== undefined && cibleMaximum > 0 && cibleManquantes > 0
  const coutRequis =
    option !== undefined &&
    paiement !== undefined &&
    requis !== undefined &&
    !paiementFacultatif(paiement) &&
    paye < requis
  // Cout ecrit en TYPES (« BY » pour Energy Shield, sur Crossbones) : le nombre
  // de ressources ne veut rien dire, il faut une ressource de chaque type
  // demande. Tant qu'il en manque, on reste au paiement.
  const typesRequis =
    option !== undefined &&
    paiement !== undefined &&
    !paiementFacultatif(paiement) &&
    Object.keys(typesManquants(paiement, ressources)).length > 0
  const coutInconnuRequis =
    option !== undefined &&
    paiement !== undefined &&
    requis === undefined &&
    coutParType(paiement.cost) === undefined &&
    paiement.payment.length > 0 &&
    ressources.length === 0
  // Combien de designations la table peut encore offrir : une carte repetable
  // en vaut plusieurs. Sans ce plafond reel, une action « jusqu'a 3 cibles » ne
  // disposant que d'UNE carte legale resterait indefiniment a l'etape des
  // cibles, a reclamer un choix impossible.
  const capaciteCibles = [...occurrences.values()].reduce((somme, n) => somme + n, 0)
  const cibleSupplementairePossible =
    aDesCibles &&
    cibles.length >= cibleMinimum &&
    cibles.length < cibleMaximum &&
    cibles.length < capaciteCibles
  // Combien de points d'une selection REPARTIE (degats, soins) restent a placer.
  // Reserve aux selections repetables : « jusqu'a 3 cartes » distinctes n'est
  // pas une repartition, et personne n'y a de « reste » a perdre.
  const ciblesRestantes =
    option !== undefined && cibleRepetable
      ? Math.max(0, Math.min(cibleMaximum, capaciteCibles) - cibles.length)
      : 0
  // L'annonce suit ce que le joueur a ete invite a faire. Le paiement passait
  // devant les cibles restantes : une action « jusqu'a 3 cibles » basculait sur
  // « Paie 0/1 » des la premiere designee, et les deux autres paraissaient
  // perdues. Les cibles encore prenables sont donc annoncees d'abord ; le
  // paiement reste possible pendant ce temps (voir `peutDepenser`), si bien
  // qu'aucun ordre n'est impose au joueur.
  const etape: EtapeInteraction = !option
    ? 'action'
    : cibleRequise || (ciblesOptionnelles && cibles.length === 0)
      ? 'target'
      : cibleSupplementairePossible
        ? 'target'
        : coutRequis || coutInconnuRequis || typesRequis
          ? 'payment'
          : 'confirm'

  /** Identifiant de l'option engagee par un GESTE, tant qu'elle dure. */
  const optionParGeste = useRef<number | undefined>(undefined)

  const choisirOption = useCallback((choisie: Option, ciblesInitiales: number[] = [], parGeste = false) => {
    optionParGeste.current = parGeste ? choisie.id : undefined
    const max = choisie.target_num_range[1]
    let prochainesCibles =
      max > 0
        ? ciblesInitiales
            .filter((cible) => choisie.all_legal_targets.includes(cible))
            .slice(0, max)
        : []
    if (prochainesCibles.length === 0 && max > 0 && choisie.target_num_range[0] >= 1 && lireAutoCible()) {
      const distinctes = [...new Set(choisie.all_legal_targets)]
      if (distinctes.length === 1) prochainesCibles = [distinctes[0]]
    }
    setIdOption(choisie.id)
    setCibles(prochainesCibles)
    setRessources([])
    setCarteFocus(undefined)
    setCibleFocus(undefined)
    setSourceDepot(undefined)
  }, [])

  useEffect(() => {
    const seule = options[0]
    if (idOption !== undefined || options.length !== 1 || !seule || !optionDemarreAuto(seule)) {
      return
    }
    setIdOption(seule.id)
    setCibles([])
    setRessources([])
    setCarteFocus(undefined)
    setCibleFocus(undefined)
    setSourceDepot(undefined)
  }, [idOption, options])

  // Cible unique et obligatoire (ex. une capacite qui ne peut viser que ton
  // propre heros) : on la choisit automatiquement, c'est penible d'avoir a
  // designer la seule cible legale. Condition stricte : il FAUT une cible
  // (min >= 1), une SEULE (max === 1) et une seule candidate. On memorise
  // l'option traitee pour ne pas re-cocher si le joueur decoche volontairement.
  const autoCibleFaite = useRef<number | undefined>(undefined)
  useEffect(() => {
    if (!option) {
      autoCibleFaite.current = undefined
      return
    }
    if (autoCibleFaite.current === option.id) return
    if (cibleMinimum >= 1 && cibleMaximum === 1 && ciblePossibles === 1 && cibles.length === 0) {
      const seule = [...ciblesParOccurrence(option).keys()][0]
      if (seule !== undefined) {
        autoCibleFaite.current = option.id
        setCibles([seule])
      }
    }
  }, [option, cibleMinimum, cibleMaximum, ciblePossibles, cibles.length])

  const abandonnerOption = useCallback(() => {
    setIdOption(undefined)
    setCibles([])
    setRessources([])
  }, [])

  const defocaliser = useCallback(() => {
    setCarteFocus(undefined)
    setCibleFocus(undefined)
    setSourceDepot(undefined)
  }, [])
  const focaliserCarte = useCallback((id: number) => {
    setCarteFocus(id)
    setCibleFocus(undefined)
    setSourceDepot(undefined)
  }, [])
  const focaliserCible = useCallback((id: number, source?: number) => {
    setCibleFocus(id)
    setCarteFocus(undefined)
    setSourceDepot(source)
  }, [])

  const basculerCible = useCallback(
    (id: number, max: number, maxParCible = 1) => {
      setCibles((actuelles) => {
        const deja = nombreDeFois(actuelles, id)
        if (deja > 0) {
          const peutAjouter = deja < maxParCible && (max <= 0 || actuelles.length < max)
          return peutAjouter ? [...actuelles, id] : actuelles.filter((x) => x !== id)
        }
        if (max > 0 && actuelles.length >= max) return actuelles
        return [...actuelles, id]
      })
      // Changer de premiere cible change le cout : les ressources deja posees
      // ne veulent plus rien dire.
      setRessources([])
    },
    []
  )

  /**
   * Echange la position de deux cibles DEJA CHOISIES dans `cibles` -- les
   * deux boutons « ← »/« → » d'une selection ordonnee (voir `ordreReculer`/
   * `ordreAvancer`, `EtatInteractif`). N'ajoute ni ne retire rien : si l'un
   * des deux id est absent, ne fait rien plutot que de deviner.
   */
  const permuterCibles = useCallback((idA: number, idB: number) => {
    setCibles((actuelles) => {
      const posA = actuelles.indexOf(idA)
      const posB = actuelles.indexOf(idB)
      if (posA === -1 || posB === -1) return actuelles
      const permutee = [...actuelles]
      ;[permutee[posA], permutee[posB]] = [permutee[posB], permutee[posA]]
      return permutee
    })
  }, [])

  /**
   * Assigne `quantite` occurrences de `id` d'un coup, plutot qu'un clic par
   * occurrence (voir `EtatInteractif.assignerReste`). L'appelant calcule
   * deja `quantite` a partir de `maxParCible` et du total encore a
   * distribuer : cette fonction ne revalide rien, elle pousse tel quel.
   */
  const assignerReste = useCallback((id: number, quantite: number) => {
    if (quantite <= 0) return
    setCibles((actuelles) => [...actuelles, ...Array(quantite).fill(id)])
    setRessources([])
  }, [])

  const basculerRessource = useCallback(
    (carte: WorldCard) => {
      setRessources((actuelles) => {
        const disponibles = carte.resources.filter(
          (effectId) => foisDisponible(paiement, effectId) > 0
        )
        // On retire d'abord si cette carte a deja paye : un second clic rend la
        // ressource au lieu d'en depenser une de plus.
        const dejaPosee = disponibles.find((effectId) => actuelles.includes(effectId))
        if (dejaPosee !== undefined) {
          const position = actuelles.indexOf(dejaPosee)
          return [...actuelles.slice(0, position), ...actuelles.slice(position + 1)]
        }
        for (const effectId of disponibles) {
          const posees = actuelles.filter((x) => x === effectId).length
          if (posees < foisDisponible(paiement, effectId)) return [...actuelles, effectId]
        }
        return actuelles
      })
    },
    [paiement]
  )

  /**
   * La regle de selection de l'option (`select_rule`) appliquee A LA
   * DESIGNATION : une cible qui la casserait n'est pas cliquable. Voir
   * `regles-selection.ts` : refuser au moment de valider ferait perdre la
   * carte, c'est le defaut corrige le 18/09/2026.
   */
  const refuseeParLaRegle = useCallback(
    (cible: number) => {
      if (!option || !option.select_rule) return false
      const candidate = index.get(cible)
      if (!candidate) return false
      const choisies = cibles
        .filter((id) => id !== cible)
        .map((id) => index.get(id))
        .filter((carte): carte is WorldCard => carte !== undefined)
      return cibleRefuseeParLaRegle(option.select_rule, choisies, candidate)
    },
    [option, cibles, index]
  )

  const cartes = useMemo(() => {
    const etats = new Map<number, EtatInteractif>()
    if (!demande) return etats

    if (!option) {
      // Pas encore d'option choisie : une carte avec une seule action disponible
      // demarre directement la sequence. Le heros/alter-ego garde le role de hub
      // si des actions generales existent.
      const parPorteur = new Map<number, Option[]>()
      for (const candidate of demande.options) {
        if (candidate.bind_id === 0) continue
        const liste = parPorteur.get(candidate.bind_id) ?? []
        liste.push(candidate)
        parPorteur.set(candidate.bind_id, liste)
      }
      if (
        identiteJoueurId !== undefined &&
        (optionsGenerales.length > 0 || demande.show_cancel) &&
        !parPorteur.has(identiteJoueurId)
      ) {
        parPorteur.set(identiteJoueurId, [])
      }
      for (const [bindId, liste] of parPorteur) {
        const estHubIdentite = bindId === identiteJoueurId && estIdentiteJoueur(index.get(bindId))
        const disponiblesSource = liste.filter((candidate) => !candidate.failure_reason)
        const disponiblesGenerales = estHubIdentite
          ? optionsGenerales.filter((candidate) => !candidate.failure_reason)
          : []
        const disponibles = [...disponiblesGenerales, ...disponiblesSource]
        const ouvreHub = estHubIdentite && (optionsGenerales.length > 0 || demande.show_cancel)
        const actionUnique =
          modeActions === 'detailed' && !ouvreHub && disponibles.length === 1
            ? disponibles[0]
            : undefined
        const focalisee = carteFocus === bindId
        etats.set(bindId, {
          role: focalisee || ouvreHub ? 'source' : disponibles.length > 0 ? 'porteur' : 'indisponible',
          choisie: focalisee,
          agir: actionUnique ? () => choisirOption(actionUnique) : () => focaliserCarte(bindId),
        })
      }
      if (cibleFocus !== undefined && idsAffiches.has(cibleFocus) && !etats.has(cibleFocus)) {
        etats.set(cibleFocus, {
          role: 'cible-preview',
          choisie: true,
          agir: () => focaliserCible(cibleFocus),
        })
      }
      if (carteFocus !== undefined && idsAffiches.has(carteFocus) && !etats.has(carteFocus)) {
        etats.set(carteFocus, {
          role: 'source',
          choisie: true,
          agir: () => focaliserCarte(carteFocus),
        })
      }
      return etats
    }

    const [minCibles, max] = option.target_num_range
    // Le ciblage est-il satisfait ? Sert au cas ou une meme carte est A LA FOIS
    // la cible et le payeur : tant qu'il manque des cibles son clic vise, une
    // fois le compte atteint il paie (voir le bloc des payeurs plus bas).
    const ciblageSatisfait = cibles.length >= minCibles
    const ordonnee = optionEstOrdonnee(option)
    for (const [cible, maxParCible] of ciblesParOccurrence(option)) {
      // Une cible que la table ne dessine pas ne peut pas etre cliquee dessus :
      // elle passe par le selecteur (voir ciblesHorsTable).
      if (!idsAffiches.has(cible)) continue
      const fois = nombreDeFois(cibles, cible)
      // Le droit de viser depend du MAXIMUM restant, jamais de l'etape en
      // cours. Les deux etaient lies, et une action « jusqu'a 3 cibles » dont
      // le cout devenait du apres la premiere designation rendait les deux
      // suivantes non cliquables : le joueur voyait « 1/3 » sans plus pouvoir
      // completer. Une cible deja prise reste toujours cliquable, pour la
      // retirer.
      const peutViser = cibles.length < max && !refuseeParLaRegle(cible)
      if (!peutViser && fois === 0) continue
      // Une cible deja choisie reste cliquable pour la retirer -- SAUF si
      // elle est la SEULE candidate possible et que le compte exige est FIXE
      // (min === max) : la retirer ne mene nulle part (rien a lui substituer,
      // le minimum l'exige de toute facon), et ne fait plus que declencher
      // l'effet de bord de `basculerCible` (vider tout paiement deja pose)
      // sans aucune action utile. Signalement Yarro n24 (27/09/2026) : la
      // carte qui porte Sync Ratio est AUSSI la cible unique et obligatoire
      // de l'amelioration jouee (elle s'attache au heros) ; une fois ses
      // interfaces toutes inclinees elle n'est plus payeuse, et le joueur qui
      // la recliquait par reflexe perdait toute sa main deja payee, sans un
      // mot.
      const detargetInutile = minCibles >= max && ciblesParOccurrence(option).size <= max
      // Position dans `cibles` : -1 si pas encore choisie (ordre alors absent
      // plus bas, `indexOf` seul ne suffit pas a le dire sans ce garde-fou
      // sur `fois`).
      const position = ordonnee && fois > 0 ? cibles.indexOf(cible) : -1
      // Combien `assignerReste` ajouterait en un clic : plafonne par ce que
      // CETTE carte peut encore recevoir ET par ce qu'il reste a distribuer
      // au total. En dessous de 2, ca ne ferait rien de plus qu'un clic
      // ordinaire : pas la peine de proposer le raccourci.
      const resteQuantite = Math.min(maxParCible - fois, max - cibles.length)
      etats.set(cible, {
        role: 'cible',
        choisie: fois > 0,
        fois: maxParCible > 1 ? fois : undefined,
        ordre: position >= 0 ? position + 1 : undefined,
        ordreReculer: position > 0 ? () => permuterCibles(cible, cibles[position - 1]) : undefined,
        ordreAvancer:
          position >= 0 && position < cibles.length - 1
            ? () => permuterCibles(cible, cibles[position + 1])
            : undefined,
        assignerReste:
          maxParCible > 1 && peutViser && resteQuantite > 1
            ? () => assignerReste(cible, resteQuantite)
            : undefined,
        assignerResteQuantite:
          maxParCible > 1 && peutViser && resteQuantite > 1 ? resteQuantite : undefined,
        pulse: etape === 'target' && fois === 0,
        agir:
          peutViser || (fois > 0 && !detargetInutile)
            ? () => basculerCible(cible, max, maxParCible)
            : undefined,
      })
    }

    if (option.bind_id !== 0 && idsAffiches.has(option.bind_id) && !etats.has(option.bind_id)) {
      etats.set(option.bind_id, {
        role: 'source',
        choisie: true,
      })
    }

    // Les cartes qui peuvent payer.
    //
    // Une meme carte peut etre A LA FOIS la cible et le payeur : c'est le cas
    // de toute AMELIORATION posee sur une identite qui genere elle-meme des
    // ressources — Venom recoit le Sonic Rifle et le finance avec « Symbiotic
    // Bond ». Le role de cible passait devant et confisquait le clic : une
    // fois Venom designe, le cliquer ne faisait plus que le DE-cibler, et sa
    // ressource restait inatteignable.
    // Depuis, tant qu'il manque des cibles le clic vise ; des que le compte
    // est atteint, il paie. La carte garde son apparence de cible choisie.
    if (paiement && paiement.payment.length > 0) {
      for (const [id, carte] of index) {
        const dejaPose = etats.get(id)
        // Une carte deja marquee peut tres bien etre AUSSI un payeur. On ne la
        // saute que si son premier role a encore besoin du clic, c'est-a-dire
        // tant qu'il reste des cibles a designer. Deux familles la concernent :
        //   - la CIBLE qui recoit l'amelioration (Venom et son Sonic Rifle) ;
        //   - la carte SOURCE, qui porte l'action et la finance elle-meme.
        // Une carte jouee depuis la main n'est jamais proposee comme payeuse
        // d'elle-meme par le moteur : elle ressort donc plus bas sur
        // `peutPayer`, sans traitement particulier ici.
        const roleLibere =
          dejaPose === undefined ||
          dejaPose.role === 'source' ||
          (dejaPose.role === 'cible' && ciblageSatisfait)
        if (!roleLibere) continue
        if (!idsAffiches.has(id)) continue
        const fois = carte.resources.filter((effectId) => ressources.includes(effectId)).length
        const selectionnee = fois > 0
        const peutPayer = carte.resources.some((effectId) => foisDisponible(paiement, effectId) > 0)
        if (!peutPayer && fois === 0) continue
        // Cloisonnement main / réserve (pack Brawn) : une fois qu'une zone
        // finance le paiement en cours, l'autre se ferme. On ne coupe QUE les
        // cartes non encore posées, sinon on ne pourrait plus rendre une
        // ressource déjà dépensée et le joueur resterait coincé.
        if (zoneEngagee !== undefined && !selectionnee) {
          const autreZone =
            zoneEngagee === 'main' ? zonesDePaiement.reserve : zonesDePaiement.main
          if (autreZone.has(id)) continue
        }
        // On peut depenser des ressources pendant l'etape 'payment' (cout requis)
        // MAIS AUSSI a la confirmation : c'est la que se fait le SURPAIEMENT
        // (overpay). Sans ca, une carte a cout 0 surpayable (ex. l'allie Ant-Man)
        // n'offrait jamais de payer, puisque le cout requis etant 0 on sautait
        // directement a 'confirm'.
        // Symetrique du bloc des cibles : depenser depend du COUT, pas de
        // l'etape. Puisque les cibles restantes sont desormais annoncees en
        // premier, s'en tenir a l'etape aurait juste deplace le blocage sur le
        // paiement. Aucun ordre n'est impose : viser puis payer, ou l'inverse.
        const peutDepenser =
          etape === 'payment' ||
          etape === 'confirm' ||
          coutRequis ||
          coutInconnuRequis ||
          typesRequis
        if (!peutDepenser && fois === 0) continue
        // Le pulse signale le paiement REQUIS. On l'allume aussi a la
        // confirmation, mais seulement pour les cartes qui recompensent le
        // surpaiement : sans ce rappel, l'allie Ant-Man entrait en jeu a 0 PV et
        // mourait aussitot, sans que rien n'ait jamais suggere qu'on POUVAIT
        // payer. Le limiter a ces cartes evite de harceler a chaque
        // confirmation ordinaire.
        etats.set(id, {
          // Une carte qui est aussi la cible garde son role : le joueur doit
          // continuer a voir OU part son amelioration.
          role: dejaPose?.role ?? 'ressource',
          choisie: (dejaPose?.choisie ?? false) || selectionnee,
          fois,
          pulse: (etape === 'payment' || surpaiementRecompense) && !selectionnee,
          agir:
            peutDepenser || selectionnee
              ? () => basculerRessource(carte)
              : dejaPose?.agir,
        })
      }
    }

    return etats
  }, [
    demande,
    option,
    cibles,
    ressources,
    paiement,
    etape,
    coutRequis,
    coutInconnuRequis,
    surpaiementRecompense,
    index,
    idsAffiches,
    carteFocus,
    cibleFocus,
    identiteJoueurId,
    zonesDePaiement,
    zoneEngagee,
    optionsGenerales,
    modeActions,
    choisirOption,
    focaliserCarte,
    focaliserCible,
    basculerCible,
    permuterCibles,
    assignerReste,
    basculerRessource,
    refuseeParLaRegle,
  ])

  const ciblesHorsTable = useMemo<CibleHorsTable[]>(() => {
    // Rapport n76 (10/10/2026) : quand TOUTES les cibles sont hors table, la
    // liste reste montee a l'etape « confirm » : la carte choisie y reste en
    // surbrillance et la fenetre de choix porte son propre « Valider ». Sinon
    // le choix d'une carte refermait la fenetre et renvoyait au panneau central.
    const toutesHorsTable =
      option !== undefined && option.all_legal_targets.length > 0 && option.all_legal_targets.every((c) => !idsAffiches.has(c) || representantsDePile?.get(c) === c)
    if (!option || (etape !== 'target' && !(etape === 'confirm' && toutesHorsTable))) return []
    const [, max] = option.target_num_range
    const ordonnee = optionEstOrdonnee(option)
    const liste: CibleHorsTable[] = []

    for (const [cible, maxParCible] of ciblesParOccurrence(option)) {
      // La carte du DESSUS d'une pile (la défausse, le deck) est dessinée sur la table
      // et cliquable là, mais la fenêtre de liste doit l'offrir AUSSI : sinon une
      // recherche (Study the Tape) montre 4 cartes alors que 5 sont éligibles, et la
      // 5e, qui clignote ailleurs, passe inaperçue (rapport n°57, 04/10/2026).
      const dessusDePile = representantsDePile?.get(cible) === cible
      if (idsAffiches.has(cible) && !dessusDePile) continue
      const carte = index.get(cible)
      if (!carte) continue
      const fois = nombreDeFois(cibles, cible)
      // Une cible que la regle de selection refuse n'est pas proposee (sauf
      // si elle est deja choisie, pour pouvoir la retirer).
      if (fois === 0 && refuseeParLaRegle(cible)) continue
      const position = ordonnee && fois > 0 ? cibles.indexOf(cible) : -1
      // Voir le commentaire jumeau dans la boucle des cibles sur table.
      const resteQuantite = Math.min(maxParCible - fois, max - cibles.length)
      liste.push({
        // Une carte proposee au choix est forcement visible pour nous : le
        // moteur ne demanderait pas de choisir a l'aveugle. On la montre donc
        // face visible, meme si elle dort dans un deck.
        props: toScanCard(
          { ...carte, visible_for_players: [playerId], is_face_up: true },
          { playerId, actives: new Set(), catalogue }
        ),
        choisie: fois > 0,
        fois: maxParCible > 1 ? fois : undefined,
        ordre: position >= 0 ? position + 1 : undefined,
        ordreReculer: position > 0 ? () => permuterCibles(cible, cibles[position - 1]) : undefined,
        ordreAvancer:
          position >= 0 && position < cibles.length - 1
            ? () => permuterCibles(cible, cibles[position + 1])
            : undefined,
        assignerReste:
          maxParCible > 1 && resteQuantite > 1 ? () => assignerReste(cible, resteQuantite) : undefined,
        assignerResteQuantite: maxParCible > 1 && resteQuantite > 1 ? resteQuantite : undefined,
        agir: () => basculerCible(cible, max, maxParCible),
      })
    }

    return liste
  }, [
    option,
    etape,
    index,
    idsAffiches,
    representantsDePile,
    cibles,
    playerId,
    catalogue,
    basculerCible,
    permuterCibles,
    assignerReste,
    refuseeParLaRegle,
  ])

  const controle = option
    ? reponsePrete(option, cibles, ressources)
    : { prete: false, raison: t('Choisir une action') }

  const coutAffiche =
    requis === 0
      ? ''
      : requis === undefined
      ? paiement?.cost && paiement.cost !== '0'
        ? paiement.cost
        : ''
      : `${paye}/${requis}${paiementFacultatif(paiement) ? ' max' : ''}`

  const libelles = libellesCible({
    choisies: cibles.length,
    minimum: cibleMinimum,
    maximum: cibleMaximum,
    cartesCiblables: ciblePossibles,
    repetable: cibleRepetable,
    mulligan: option?.name.toLowerCase().includes('mulligan'),
  })

  const assistant: AssistantInteraction = {
    etape,
    titre: !option
      ? t('Choisir une action')
      : etape === 'target'
        ? libelles.titre
        : etape === 'payment'
          ? t('Payer le coût')
          : t('Prêt à valider'),
    detail: !option
      ? undefined
      : etape === 'target'
        ? libelles.detail
        : etape === 'payment'
          ? requis !== undefined
            ? `${paye}/${requis} ${t('payé')}`
            : paiement?.cost
          : controle.prete
            ? t('Appuyer sur Valider quand tout est correct')
            : controle.raison,
    indice: option && etape === 'target' ? libelles.indice : undefined,
    cibleMinimum,
    cibleMaximum,
    cibleNombre: cibles.length,
    ciblePossibles,
    cibleRepetable,
    coutRequis: requis,
    coutPaye: paye,
    coutSlots: slotsCout(paiement, ressources, requis),
    coutRegles: reglesCout(paiement),
    typesManquants: typesManquants(paiement, ressources),
  }

  // La confirmation « ce coup ne fera rien » (11/09/2026). Le moteur accepte
  // le coup ; c'est le plateau qui, AVANT d'envoyer, demande au joueur s'il
  // tient vraiment a payer Crisis Averted sans mentale sous une Crise. Hors
  // fournisseur (tests), `useConfirmation` retombe sur window.confirm.
  const confirmer = useConfirmation()

  // Paiement automatique (24/09/2026, demande de l'utilisateur). Expose ici,
  // pas lu en localStorage a la volee comme `lireAutoCible` : la modale de
  // premiere fois peut ecrire ce choix, et le panneau Reglages (board.tsx)
  // doit le refleter tout de suite, sans attendre un remontage.
  const [paiementAutoChoix, setPaiementAutoChoix] = useState(lirePaiementAuto)
  const basculerPaiementAuto = useCallback(() => {
    setPaiementAutoChoix((c) => {
      const nouveau = c === 'on' ? 'off' : 'on'
      ecrirePaiementAuto(nouveau)
      return nouveau
    })
  }, [])
  // Un seul payeur restant (une seule carte au role 'ressource' qui pulse
  // encore, cf. `cartes` ci-dessus) : ce n'est plus un choix, c'est la seule
  // carte cliquable. On la paie a sa place. Cle de garde = option + nombre de
  // ressources deja posees, pour avancer a chaque paiement automatique sans
  // jamais re-agir deux fois sur le meme etat (une carte a payer plusieurs
  // fois reste donc payee coup par coup, un evenement par clic economise).
  const paiementAutoFait = useRef<string | undefined>(undefined)
  useEffect(() => {
    if (etape !== 'payment' || !option) {
      paiementAutoFait.current = undefined
      return
    }
    const payeurs = [...cartes.entries()].filter(([, e]) => e.role === 'ressource' && e.pulse)
    if (payeurs.length !== 1) return
    const cle = `${option.id}:${ressources.length}`
    if (paiementAutoFait.current === cle) return
    paiementAutoFait.current = cle
    // ⚠ CHEMIN SYNCHRONE QUAND LE CHOIX EST DEJA TRANCHE, comme
    // `detecterAutreHeros`/`valider` plus bas : y faire systematiquement
    // passer une Promise (meme sans modale a attendre) decale `agir()` d'un
    // tick de micro-tache et casse la meme classe de test (glisser-depose
    // synchrone) que le piege deja corrige le jour meme pour l'ecart de
    // heros. Seul le premier "jamais demande" a vraiment besoin d'attendre.
    if (paiementAutoChoix === 'on') {
      payeurs[0][1].agir?.()
      return
    }
    if (paiementAutoChoix === 'off') return
    void confirmer({
      titre: t('Payer automatiquement ?'),
      texte: t(
        'Quand une seule carte peut encore payer le reste du coût, le jeu peut la dépenser tout seul sans attendre un clic. Ce choix se change à tout moment dans Réglages.'
      ),
      confirmer: t('Oui, automatiquement'),
      annuler: t('Non, je clique moi-même'),
    }).then((accepte) => {
      ecrirePaiementAuto(accepte ? 'on' : 'off')
      setPaiementAutoChoix(accepte ? 'on' : 'off')
      if (accepte) payeurs[0][1].agir?.()
    })
  }, [etape, option, cartes, ressources.length, paiementAutoChoix, confirmer])

  // La confirmation « tu regardes un héros, l'action va agir pour un autre »
  // (24/09/2026). PAS fusionnée avec « coup sans effet » ci-dessous : deux
  // motifs différents méritent deux messages différents, et annuler celle-ci
  // ne doit pas laisser passer l'autre par accident.
  //
  // ⚠ VERIFICATION SYNCHRONE, PAS UNE PROMESSE SYSTEMATIQUE. Faire passer
  // TOUTE validation par un `.then()`, meme sans ecart, decale `repondre` d'un
  // tick de micro-tache -- deux gestes de glisser-deposer (validation-geste)
  // attendaient un `repondre` synchrone juste apres l'appel et cassaient.
  const detecterAutreHeros = useCallback(
    (bindPlayerId: number): { nomAffiche: string; nomCible: string } | undefined => {
      if (bindPlayerId === playerId) return undefined
      const nomCible = nomHeros(world, bindPlayerId)
      const nomAffiche = nomHeros(world, playerId)
      if (nomCible === undefined || nomAffiche === undefined) return undefined
      return { nomAffiche, nomCible }
    },
    [world, playerId]
  )

  const valider = useCallback(() => {
    if (!option) return
    const envoyer = () =>
      repondre({ id: option.id, targets: cibles, resources: ressources }, option.bind_player_id)
    const envoyerAvecAvertissementCout = () => {
      const avertissement = coupSansEffet(paiement, ressources)
      if (!avertissement) {
        envoyer()
        return
      }
      void confirmer({
        ...textesCoupSansEffet(avertissement),
        confirmer: t('Continuer'),
        annuler: t('Annuler'),
        ton: 'danger',
      }).then((accepte) => {
        if (accepte) envoyer()
      })
    }
    const verifierAutreHeros = () => {
      const ecart = detecterAutreHeros(option.bind_player_id)
      if (!ecart) {
        envoyerAvecAvertissementCout()
        return
      }
      void confirmer({
        ...texteAutreHeros(ecart.nomAffiche, ecart.nomCible),
        confirmer: t('Continuer'),
        ton: 'normal',
      }).then((accepte) => {
        if (accepte) envoyerAvecAvertissementCout()
      })
    }
    // Des degats (ou soins) repartis dont il reste des points : le joueur les
    // perd en validant, autant qu'il le sache (30/09/2026).
    if (ciblesRestantes === 0) {
      verifierAutreHeros()
      return
    }
    void confirmer({
      ...textesPointsNonPlaces(ciblesRestantes),
      confirmer: t('Valider quand même'),
      annuler: t('Continuer à placer'),
      ton: 'danger',
    }).then((accepte) => {
      if (accepte) verifierAutreHeros()
    })
  }, [option, cibles, ressources, paiement, repondre, confirmer, detecterAutreHeros, ciblesRestantes])

  // --- Validation courte -----------------------------------------------------
  // L'etape « valider » ne sert a rien quand il ne reste RIEN a decider. Quatre
  // garde-fous, sans lesquels on volerait un choix au joueur :
  //   - cible unique : s'il y avait plusieurs cibles legales, il vient de
  //     choisir, et un dernier regard avant de lancer a de la valeur ;
  //   - aucune cible facultative a ajouter, et pas d'action « repartie » ;
  //   - paiement non facultatif (« UpTo » : c'est LUI qui decide combien) ;
  //   - carte non surpayable : Ant-Man et consorts se jouent justement en
  //     ajoutant des ressources APRES que le cout est couvert.
  // ⚠ UN GESTE VAUT LE CHOIX. Le garde-fou « cible unique » existe parce qu'un
  // joueur qui vient de choisir parmi plusieurs cibles gagne a jeter un dernier
  // regard avant de lancer. Celui qui a TRAINE sa carte sur un ennemi, lui, a
  // deja designe : lui redemander confirmation, c'est lui faire faire deux fois
  // le meme choix. Signale des le premier essai du glisser (08/09/2026).
  // Les autres garde-fous restent tous en place : rien ne part tout seul quand
  // il reste un paiement facultatif, un surpaiement recompense, une cible
  // repetable ou une cible de plus a prendre.
  const designeeParGeste = option !== undefined && optionParGeste.current === option.id
  // Signalement Yarro n23 (26/09/2026) : Sync Ratio (SP//dr) annonce, pour
  // UN SEUL clic, la somme des ressources de TOUTES ses interfaces pretes
  // (2 si 2 sont pretes), meme si le joueur ne veut en incliner qu'une pour
  // completer avec une carte de main. Ce clic seul suffisait donc a couvrir
  // le cout ANNONCE, la validation courte partait aussitot -- avant que la
  // carte de main ait pu s'ajouter -- et le paiement REEL (souvent inferieur
  // a l'annonce) tombait court : le correctif atomique du 20/09/2026 rendait
  // tout, sans perte, mais l'action se terminait quand meme sans effet.
  // Meme forme sur toute capacite qui GENERE plus d'une ressource par clic
  // (`valeurMoyen` > 1) : tant qu'un AUTRE moyen de payer existe et n'a pas
  // ete choisi, un dernier "Valider" explicite laisse le temps de l'ajouter.
  const moyenSurvaloriseNonExclusif = useMemo(() => {
    if (!paiement) return false
    const distincts = new Set(paiement.payment.map((moyen) => moyen.effect_id))
    if (distincts.size <= 1) return false
    const texteParEffet = new Map<number, string>()
    for (const moyen of paiement.payment) {
      if (!texteParEffet.has(moyen.effect_id)) texteParEffet.set(moyen.effect_id, moyen.res_text)
    }
    return ressources.some((id) => valeurMoyen(texteParEffet.get(id) ?? '') > 1)
  }, [paiement, ressources])
  const validationEvidente =
    option !== undefined &&
    etape === 'confirm' &&
    (ciblePossibles <= 1 || designeeParGeste) &&
    !cibleRepetable &&
    !cibleSupplementairePossible &&
    !surpaiementRecompense &&
    !paiementFacultatif(paiement) &&
    !moyenSurvaloriseNonExclusif &&
    // Un coup sans effet merite le dernier regard : pas de validation courte.
    coupSansEffet(paiement, ressources) === undefined

  const dejaValidee = useRef<number | undefined>(undefined)
  useEffect(() => {
    if (!lireValidationCourte()) return
    if (!validationEvidente || !option) {
      if (!option) dejaValidee.current = undefined
      return
    }
    // Une option ne se valide qu'une fois : sans ce verrou, le temps que le
    // moteur reponde, un nouveau rendu relancerait la meme validation.
    if (dejaValidee.current === option.id) return
    dejaValidee.current = option.id
    valider()
  }, [validationEvidente, option, valider])

  const annuler = useCallback(() => {
    // Une option en cours de composition s'abandonne cote client ; sans option,
    // annuler veut dire « passer », et c'est au moteur qu'il faut le dire.
    if (option) {
      abandonnerOption()
      return
    }
    const bindPlayerId = demande?.options[0]?.bind_player_id ?? 0
    const ecart = detecterAutreHeros(bindPlayerId)
    if (!ecart) {
      repondre(null, bindPlayerId)
      return
    }
    void confirmer({
      ...texteAutreHeros(ecart.nomAffiche, ecart.nomCible),
      confirmer: t('Continuer'),
      ton: 'normal',
    }).then((accepte) => {
      if (accepte) repondre(null, bindPlayerId)
    })
  }, [option, abandonnerOption, repondre, demande, confirmer, detecterAutreHeros])

  // Une carte focalisee reduit le panneau a SES options. L'identite du joueur
  // sert aussi de hub pour les actions generales (bind_id 0). Une cible focalisee
  // montre seulement les actions disponibles qui peuvent la viser maintenant.
  const idsDeLaSource =
    sourceDepot !== undefined
      ? new Set(optionsDeLaSource(options, sourceDepot, identiteJoueurId).map((o) => o.id))
      : undefined
  const optionsAffichees =
    cibleFocus !== undefined
      ? options.filter(
          (o) =>
            !o.failure_reason &&
            o.target_num_range[1] > 0 &&
            o.all_legal_targets.includes(cibleFocus) &&
            // Menu ouvert par un DÉPÔT : seules les actions de la carte lâchée.
            // Une même définition de « les actions de cette source » que le
            // glisser-déposer lui-même (`glisser/cibles.ts`), sinon les deux
            // divergeraient et le menu rouvrirait la porte qu'on ferme ici.
            (idsDeLaSource === undefined || idsDeLaSource.has(o.id))
        )
      : carteFocus !== undefined
        ? options.filter(
            (o) =>
              o.bind_id === carteFocus ||
              (carteFocus === identiteJoueurId && optionsGenerales.includes(o))
          )
        : options

  return {
    option,
    cibles,
    ressources,
    selectionPartagee,
    options: optionsAffichees,
    carteFocus,
    cibleFocus,
    defocaliser,
    focaliserCarte,
    focaliserCible,
    cartes,
    ciblesHorsTable,
    raison: controle.raison,
    prete: controle.prete,
    coutAffiche,
    surpaiementRecompense,
    ciblesRestantes,
    assistant,
    choisirOption,
    abandonnerOption,
    valider,
    annuler,
    paiementAutoChoix,
    basculerPaiementAuto,
  }
}
