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
  agir: () => void
}

export type Interaction = {
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

function reglesCout(paiement: Paiement | undefined): string[] {
  return (paiement?.rule ?? [])
    .filter((regle) => regle !== 'UpTo')
    .map((regle) => regle.replace(/([a-z])([A-Z])/g, '$1 $2'))
}

function optionDemarreAuto(option: Option): boolean {
  return option.failure_reason === '' && option.name.toLowerCase().includes('mulligan')
}

function estIdentiteJoueur(carte: WorldCard | undefined): boolean {
  return carte?.card_type === 'Hero' || carte?.card_type === 'AlterEgo'
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
  modeActions: 'simple' | 'detailed' = 'simple'
): Interaction {
  const [idOption, setIdOption] = useState<number | undefined>(undefined)
  const [cibles, setCibles] = useState<number[]>([])
  const [ressources, setRessources] = useState<number[]>([])
  const [carteFocus, setCarteFocus] = useState<number | undefined>(undefined)
  const [cibleFocus, setCibleFocus] = useState<number | undefined>(undefined)
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
  const [sourceDepot, setSourceDepot] = useState<number | undefined>(undefined)

  /**
   * ⚠ LA QUESTION DE LA MANIGANCE N'EXISTE PAS POUR LA TABLE. Son panneau la
   * tient (voir `demandeHorsPanneauManigance`) : sans cette porte, la table
   * posait son halo sur la manigance principale, son menu offrait l'option
   * sous son libellé technique, et en mode Détaillé le clic sur la carte
   * RÉPONDAIT — y compris pendant les 400 ms où l'overlay du panneau laisse
   * passer les clics, donc à la question suivante.
   *
   * La référence est inchangée pour toute autre demande : aucune dépendance de
   * hook n'est invalidée par ce passage.
   */
  const demande = demandeHorsPanneauManigance(demandeBrute)

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

  const option = options.find((o) => o.id === idOption)
  const paiement = option ? paiementCourant(option, cibles) : undefined
  const requis = nombreDeRessources(paiement)
  const index = useMemo(() => indexerCartes(world), [world])
  // La carte que porte l'option recompense-t-elle un surpaiement ? (Ant-Man,
  // Wasp, Wonder Man : voir catalogue.surpayable.)
  const surpaiementRecompense =
    option !== undefined && catalogue.surpayable(index.get(option.bind_id)?.card_id ?? '')
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
      const peutViser = cibles.length < max
      if (!peutViser && fois === 0) continue
      etats.set(cible, {
        role: 'cible',
        choisie: fois > 0,
        fois: maxParCible > 1 ? fois : undefined,
        pulse: etape === 'target' && fois === 0,
        agir:
          peutViser || fois > 0 ? () => basculerCible(cible, max, maxParCible) : undefined,
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
    basculerRessource,
  ])

  const ciblesHorsTable = useMemo<CibleHorsTable[]>(() => {
    if (!option || etape !== 'target') return []
    const [, max] = option.target_num_range
    const liste: CibleHorsTable[] = []

    for (const [cible, maxParCible] of ciblesParOccurrence(option)) {
      if (idsAffiches.has(cible)) continue
      const carte = index.get(cible)
      if (!carte) continue
      const fois = nombreDeFois(cibles, cible)
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
        agir: () => basculerCible(cible, max, maxParCible),
      })
    }

    return liste
  }, [option, etape, index, idsAffiches, cibles, playerId, catalogue, basculerCible])

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
  const valider = useCallback(() => {
    if (!option) return
    const envoyer = () =>
      repondre({ id: option.id, targets: cibles, resources: ressources }, option.bind_player_id)
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
  }, [option, cibles, ressources, paiement, repondre, confirmer])

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
  const validationEvidente =
    option !== undefined &&
    etape === 'confirm' &&
    (ciblePossibles <= 1 || designeeParGeste) &&
    !cibleRepetable &&
    !cibleSupplementairePossible &&
    !surpaiementRecompense &&
    !paiementFacultatif(paiement) &&
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
    repondre(null, demande?.options[0]?.bind_player_id ?? 0)
  }, [option, abandonnerOption, repondre, demande])

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
    assistant,
    choisirOption,
    abandonnerOption,
    valider,
    annuler,
  }
}
