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
  foisDisponible,
  paiementCourant,
  paiementFacultatif,
  nombreDeRessources,
  valeurMoyen,
  valeurPayee,
  reponsePrete,
  type Demande,
  type Paiement,
  type Option,
  type Reponse,
} from './ask'
import { toScanCard } from './card-model'
import type { Catalogue } from './catalogue'
import { libellesCible } from './libelles-cible'
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
  focaliserCible: (id: number) => void
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
  assistant: AssistantInteraction
  choisirOption: (option: Option, ciblesInitiales?: number[]) => void
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
  demande: Demande | undefined,
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
  const coutInconnuRequis =
    option !== undefined &&
    paiement !== undefined &&
    requis === undefined &&
    paiement.payment.length > 0 &&
    ressources.length === 0
  const cibleSupplementairePossible =
    aDesCibles && cibles.length >= cibleMinimum && cibles.length < cibleMaximum
  const etape: EtapeInteraction = !option
    ? 'action'
    : cibleRequise || (ciblesOptionnelles && cibles.length === 0)
      ? 'target'
    : coutRequis || coutInconnuRequis
      ? 'payment'
      : cibleSupplementairePossible && (!paiement || requis === undefined || requis === 0 || paye >= requis)
        ? 'target'
      : 'confirm'

  const choisirOption = useCallback((choisie: Option, ciblesInitiales: number[] = []) => {
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
  }, [])
  const focaliserCarte = useCallback((id: number) => {
    setCarteFocus(id)
    setCibleFocus(undefined)
  }, [])
  const focaliserCible = useCallback((id: number) => {
    setCibleFocus(id)
    setCarteFocus(undefined)
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

    const [, max] = option.target_num_range
    for (const [cible, maxParCible] of ciblesParOccurrence(option)) {
      // Une cible que la table ne dessine pas ne peut pas etre cliquee dessus :
      // elle passe par le selecteur (voir ciblesHorsTable).
      if (!idsAffiches.has(cible)) continue
      const fois = nombreDeFois(cibles, cible)
      if (etape !== 'target' && fois === 0) continue
      etats.set(cible, {
        role: 'cible',
        choisie: fois > 0,
        fois: maxParCible > 1 ? fois : undefined,
        pulse: etape === 'target' && fois === 0,
        agir: etape === 'target' ? () => basculerCible(cible, max, maxParCible) : undefined,
      })
    }

    if (option.bind_id !== 0 && idsAffiches.has(option.bind_id) && !etats.has(option.bind_id)) {
      etats.set(option.bind_id, {
        role: 'source',
        choisie: true,
      })
    }

    // Les cartes qui peuvent payer. Une cible peut aussi etre une ressource :
    // dans ce cas le role de cible passe devant, il vient plus tot.
    if (paiement && paiement.payment.length > 0) {
      for (const [id, carte] of index) {
        if (etats.has(id)) continue
        if (!idsAffiches.has(id)) continue
        const fois = carte.resources.filter((effectId) => ressources.includes(effectId)).length
        const selectionnee = fois > 0
        const peutPayer = carte.resources.some((effectId) => foisDisponible(paiement, effectId) > 0)
        if (!peutPayer && fois === 0) continue
        // On peut depenser des ressources pendant l'etape 'payment' (cout requis)
        // MAIS AUSSI a la confirmation : c'est la que se fait le SURPAIEMENT
        // (overpay). Sans ca, une carte a cout 0 surpayable (ex. l'allie Ant-Man)
        // n'offrait jamais de payer, puisque le cout requis etant 0 on sautait
        // directement a 'confirm'.
        const peutDepenser = etape === 'payment' || etape === 'confirm'
        if (!peutDepenser && fois === 0) continue
        // Le pulse signale le paiement REQUIS. On l'allume aussi a la
        // confirmation, mais seulement pour les cartes qui recompensent le
        // surpaiement : sans ce rappel, l'allie Ant-Man entrait en jeu a 0 PV et
        // mourait aussitot, sans que rien n'ait jamais suggere qu'on POUVAIT
        // payer. Le limiter a ces cartes evite de harceler a chaque
        // confirmation ordinaire.
        etats.set(id, {
          role: 'ressource',
          choisie: selectionnee,
          fois,
          pulse: (etape === 'payment' || surpaiementRecompense) && !selectionnee,
          agir: peutDepenser || selectionnee ? () => basculerRessource(carte) : undefined,
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
    surpaiementRecompense,
    index,
    idsAffiches,
    carteFocus,
    cibleFocus,
    identiteJoueurId,
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
  }

  const valider = useCallback(() => {
    if (!option) return
    repondre(
      { id: option.id, targets: cibles, resources: ressources },
      option.bind_player_id
    )
  }, [option, cibles, ressources, repondre])

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
  const optionsAffichees =
    cibleFocus !== undefined
      ? options.filter(
          (o) =>
            !o.failure_reason &&
            o.target_num_range[1] > 0 &&
            o.all_legal_targets.includes(cibleFocus)
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
    assistant,
    choisirOption,
    abandonnerOption,
    valider,
    annuler,
  }
}
