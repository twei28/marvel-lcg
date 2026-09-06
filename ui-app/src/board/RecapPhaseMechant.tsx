// Le bilan de la phase du méchant, en une fois.
//
// En mode rapide, la phase s'enchaîne sans s'arrêter : plus de présentation
// plein écran, plus de « Continue » à chaque activation. On ne voit donc plus
// passer ce qu'on a encaissé. Ce panneau le rejoue à la fin, groupé.
//
// Il ne réinvente rien : il relit les entrées que l'historique a déjà produites
// pendant la phase. Chaque entrée porte le round et la phase où elle est née,
// c'est tout ce qu'il faut pour les retrouver.
//
// DEUX RÈGLES DE LECTURE, apprises en le voyant tourner :
//
// 1. Il suit LA CARTE DE RÉFÉRENCE du jeu, une étape par point de la carte. Le
//    moteur découpe déjà sa phase de la même façon et chaque entrée sait de quel
//    découpage elle vient : on affiche son découpage, on ne re-catégorise rien.
//
// 2. Il RÉSUME au lieu de dérouler. Poser une menace coûte six lignes au moteur
//    (début de phase, intention, pose du jeton, gain, fin de phase) dont une
//    seule dit quelque chose à un joueur. Le déroulé complet reste accessible
//    sous le repli de chaque étape — mais il ne s'impose plus.

import { useCallback, useEffect, useMemo, useRef, useState } from 'react'
import { CarteApercu } from './Board'
import { toScanCard, type ContexteCarte } from './card-model'
import type { Catalogue } from './catalogue'
import type { EntreeHistorique } from './HistoriquePartie'
import { t } from './langue'
import type { ScanCardProps } from '../components/ScanCard'
import type { FaitMechant, World, WorldCard } from './world'

/**
 * Les étapes de la phase du méchant, dans l'ordre de la carte de référence.
 *
 * Les clés sont les états que le moteur nomme lui-même (voir game/world/phase.py,
 * Phase.State) : il n'a pas d'état unique pour « phase du méchant », il la
 * découpe exactement comme la carte.
 *
 * Le point 5 de la carte (« passer le jeton de premier joueur ») ne produit
 * aucun fait à raconter : il n'a pas d'étape ici.
 */
const ETAPES = [
  { phase: 'Main Scheme Place Threat', numero: 1, titre: 'Menace sur la manigance' },
  { phase: 'Enemy Activation', numero: 2, titre: 'Activations' },
  { phase: 'Deal Encounter Cards', numero: 3, titre: 'Cartes distribuées' },
  { phase: 'Reveal Encounter Cards', numero: 4, titre: 'Cartes révélées' },
] as const

const PHASES_MECHANT = new Set<string>(ETAPES.map((e) => e.phase))

/**
 * Les seuls types qui racontent un FAIT de jeu.
 *
 * Tout le reste (`text`) est la narration interne du moteur — « Main scheme
 * phase start », « Underground Distribution would place 1 », « moved to
 * BoostCardsDeck<1> ». Elle a sa place dans le journal, où l'on vient chercher
 * le détail ; elle n'en a pas dans un bilan qu'on lit en trois secondes.
 */
const TYPES_FAITS = new Set(['damage', 'heal', 'threat', 'card'])

type Boost = { cle: string; nom: string; cibleId?: number; apport?: number }

/** Une ligne du bilan : un fait, déjà mis en phrase. */
type Ligne = {
  cle: string
  /** Colore et choisit le verbe. */
  genre: 'menace' | 'attaque' | 'manigance' | 'carte'
  titre: string
  /** Cartes de boost retournées pour cette activation. */
  boosts?: Boost[]
  /** Héros qui a reçu la carte. */
  heros?: string
  /** Ce que la carte a produit ensuite, dans ses propres mots. */
  effets?: string[]
  cibleId?: number
  /** Ce qui se fusionne quand deux faits frappent la même cible. */
  valeur?: number
  restant?: number
  plafond?: number
  /** Auteur, pour ne fusionner que ce qui vient du même ennemi. */
  acteur?: string
  /**
   * La composition du coup, quand le moteur l'a publiée : « 3 de base + 2 de
   * boost - 1 de défense ». Absente des lignes déduites, qui ne connaissent
   * que le résultat.
   */
  calcul?: { base: number; boost: number; defense: number }
  /** Carte qui a déclenché cette activation, quand ce n'est pas l'ennemi. */
  cause?: string
}

/**
 * Range chaque activation sous L'ÉTAPE OÙ ELLE A EU LIEU, et sous la carte qui
 * l'a déclenchée quand il y en a une.
 *
 * Un vilain frappe une fois par joueur à l'étape des activations — mais une
 * carte de rencontre révélée à l'étape 4 peut le faire frapper encore. Tout
 * verser dans l'étape 2 donnait « Klaw attaque » deux fois de suite, sans que
 * rien n'explique la seconde.
 *
 * Un moteur qui ne date pas ses activations (version antérieure, sauvegarde)
 * les envoie sans phase : elles retournent alors à l'étape des activations,
 * qui reste le cas de très loin le plus fréquent.
 */
function faitsDeLEtape(faits: FaitMechant[], phase: string): FaitMechant[] {
  return faits.filter((fait) => (fait.phase ?? 'Enemy Activation') === phase)
}

/** Insère chaque activation déclenchée juste sous la carte qui l'a causée. */
function rattacherAuxCauses(cartes: Ligne[], activations: Ligne[]): Ligne[] {
  const sorties: Ligne[] = []
  const orphelines = [...activations]

  for (const carte of cartes) {
    sorties.push(carte)
    for (let i = orphelines.length - 1; i >= 0; i -= 1) {
      if (orphelines[i].cause === carte.titre) sorties.push(...orphelines.splice(i, 1))
    }
  }
  // Ce qu'aucune carte de l'étape ne réclame passe à la suite, sans se perdre.
  return [...sorties, ...orphelines]
}

/**
 * Deux faits qui laissent la MÊME cible dans le MÊME état sont le même fait.
 *
 * Le moteur rend la table plusieurs fois autour d'une seule résolution — il
 * annonce l'intention, pose le jeton, puis constate le gain — et la comparaison
 * de photos y voit passer la même transition à chaque rendu. En jeu, ça donnait
 * trois lignes « Underground Distribution +1 → 1/6 » et un total de « +3 » sur
 * une manigance qui n'en portait qu'une.
 *
 * L'état d'arrivée est ce qui tranche : deux poses RÉELLES sur la même
 * manigance la laissent à 1/6 puis à 2/6, donc elles survivent toutes les deux.
 * Seule une cible qui revient à un état déjà vu dans la même étape serait
 * confondue — au sein d'une seule étape, ça ne s'est jamais produit.
 */
function signature(fait: EntreeHistorique): string {
  return [fait.type, fait.cibleId, fait.valeur, fait.restant, fait.titre].join('|')
}

function sansDoublons(faits: EntreeHistorique[]): EntreeHistorique[] {
  const vues = new Set<string>()
  return faits.filter((fait) => {
    const cle = signature(fait)
    if (vues.has(cle)) return false
    vues.add(cle)
    return true
  })
}

type Etape = {
  numero: number
  titre: string
  lignes: Ligne[]
  /** Le déroulé complet du moteur, pour le repli. */
  brut: EntreeHistorique[]
  /** Menace posée sur l'étape, retraits déduits. */
  menace: number
  /** Dégâts encaissés sur l'étape, en positif. */
  degats: number
  /** Cartes entrées en jeu sur l'étape, boosts non compris. */
  cartes: number
}

type Bilan = { cle: string; round: number; etapes: Etape[] }

/** De quoi nommer une carte et un héros sans que le bilan lise le monde. */
export type Noms = {
  carte: (id: number | undefined) => string | undefined
  heros: (joueur: number | undefined) => string | undefined
  /** Seuil de menace d'une manigance, lu sur la carte elle-même. */
  plafond: (id: number | undefined) => number | undefined
}

/** « 3 dégâts → 8 PV ». */
function chiffreDegats(valeur: number, restant?: number): string {
  const texte = `${Math.abs(valeur)} ${t('dégâts')}`
  return restant === undefined ? texte : `${texte} → ${restant} ${t('PV')}`
}

/** « +1 → 1/6 », ou « +1 → 4 » quand la manigance n'affiche pas de seuil. */
function chiffreMenace(valeur: number, restant?: number, plafond?: number): string {
  const signe = valeur > 0 ? `+${valeur}` : `${valeur}`
  if (restant === undefined) return signe
  return plafond ? `${signe} → ${restant}/${plafond}` : `${signe} → ${restant}`
}

/**
 * « 3 de base + 2 de boost − 1 de défense ».
 *
 * On n'écrit que ce qui a joué : sans boost ni défense, la composition se
 * résume au chiffre déjà affiché à droite, et la répéter serait du bruit.
 */
export function detailDuCalcul(calcul: {
  base: number
  boost: number
  defense: number
}): string | undefined {
  if (calcul.boost === 0 && calcul.defense === 0) return undefined
  const morceaux = [`${calcul.base} ${t('de base')}`]
  if (calcul.boost !== 0) morceaux.push(`+ ${calcul.boost} ${t('de boost')}`)
  if (calcul.defense !== 0) morceaux.push(`− ${calcul.defense} ${t('de défense')}`)
  return morceaux.join(' ')
}

/** Le chiffre affiché à droite d'une ligne, selon son genre. */
function chiffreDe(ligne: Ligne): string | undefined {
  if (ligne.valeur === undefined) return undefined
  return ligne.genre === 'attaque'
    ? chiffreDegats(ligne.valeur, ligne.restant)
    : chiffreMenace(ligne.valeur, ligne.restant, ligne.plafond)
}

/**
 * Les lignes d'une étape, résumées.
 *
 * Le rattachement des boosts suit L'ORDRE DU MOTEUR, qui retourne les cartes de
 * boost AVANT de résoudre l'attaque qu'elles gonflent : on accumule les boosts
 * rencontrés et on les verse sur le premier fait qui suit. C'est ce que montre
 * le déroulé réel (« Sonic Boom revealed », « T'Challa's Shadow revealed »,
 * « Black Panther is being attacked by Klaw »), et ça n'invente aucun lien que
 * la chronologie ne porte pas déjà.
 *
 * Même principe pour les cartes de rencontre, dans l'autre sens : ce qu'une
 * carte révélée a produit la SUIT, jusqu'à la révélation suivante.
 */
function lignesDeLEtape(faits: EntreeHistorique[], noms: Noms): Ligne[] {
  const lignes: Ligne[] = []
  let boostsEnAttente: Boost[] = []
  /** Dernière carte révélée, à qui rattacher ce qui arrive ensuite. */
  let derniereCarte: Ligne | undefined

  const verser = () => {
    const boosts = boostsEnAttente
    boostsEnAttente = []
    return boosts.length > 0 ? boosts : undefined
  }

  /**
   * Empile la ligne, ou la FOND dans la précédente si c'est le même ennemi qui
   * frappe la même cible.
   *
   * Une attaque gonflée par deux boosts arrive en deux temps (2 dégâts puis 1),
   * et une manigance peut poser sa menace en plusieurs fois : ce sont des
   * étapes de calcul, pas des faits séparés. On additionne, et on garde l'état
   * final — « 3 dégâts → 8 PV » plutôt que deux lignes à lire l'une avec
   * l'autre.
   */
  const empiler = (ligne: Ligne) => {
    const precedente = lignes[lignes.length - 1]
    const fusionnable =
      precedente !== undefined &&
      precedente.genre === ligne.genre &&
      precedente.cibleId === ligne.cibleId &&
      precedente.acteur === ligne.acteur &&
      precedente.valeur !== undefined &&
      ligne.valeur !== undefined
    if (!fusionnable) {
      lignes.push(ligne)
      return ligne
    }
    precedente.valeur = (precedente.valeur ?? 0) + (ligne.valeur ?? 0)
    precedente.restant = ligne.restant ?? precedente.restant
    precedente.plafond = ligne.plafond ?? precedente.plafond
    if (ligne.boosts) precedente.boosts = [...(precedente.boosts ?? []), ...ligne.boosts]
    return precedente
  }

  for (const fait of faits) {
    if (fait.type === 'card') {
      if (fait.boost) {
        boostsEnAttente.push({
          cle: fait.cle,
          nom: fait.nomCarte ?? fait.titre,
          cibleId: fait.cibleId,
        })
        continue
      }
      derniereCarte = {
        cle: fait.cle,
        genre: 'carte',
        titre: fait.nomCarte ?? fait.titre,
        heros: noms.heros(fait.joueur),
        cibleId: fait.cibleId,
      }
      lignes.push(derniereCarte)
      continue
    }

    if (fait.type === 'damage' || fait.type === 'heal') {
      const cible = noms.carte(fait.cibleId)
      // Une carte révélée en cours d'étape s'attribue ses conséquences ; hors
      // de ce cas, les dégâts sont ceux d'une activation ennemie.
      if (derniereCarte) {
        derniereCarte.effets = [
          ...(derniereCarte.effets ?? []),
          `${cible ?? fait.titre} : ${chiffreDegats(fait.valeur ?? 0, fait.restant)}`,
        ]
        continue
      }
      empiler({
        cle: fait.cle,
        genre: 'attaque',
        // Sans auteur connu, on garde la phrase du moteur plutôt que d'inventer
        // un attaquant : « untel subit 3 dégâts » reste vrai.
        titre: fait.acteur && cible ? `${fait.acteur} ${t('attaque')} ${cible}` : fait.titre,
        boosts: verser(),
        cibleId: fait.cibleId,
        acteur: fait.acteur,
        valeur: fait.valeur,
        restant: fait.restant,
      })
      continue
    }

    if (fait.type === 'threat') {
      const cible = noms.carte(fait.cibleId)
      // Une menace posée PENDANT une activation est une manigance d'ennemi ;
      // la même à l'étape 1 est la menace de phase, qui n'a pas d'auteur.
      const manigance = fait.acteur !== undefined
      const ligne: Ligne = {
        cle: fait.cle,
        genre: manigance ? 'manigance' : 'menace',
        titre:
          manigance && cible
            ? `${fait.acteur} ${t('manigance sur')} ${cible}`
            : (cible ?? fait.titre),
        boosts: verser(),
        cibleId: fait.cibleId,
        acteur: fait.acteur,
        valeur: fait.valeur,
        restant: fait.restant,
        plafond: fait.plafond,
      }
      if (derniereCarte) {
        derniereCarte.effets = [
          ...(derniereCarte.effets ?? []),
          `${cible ?? fait.titre}${chiffreDe(ligne) ? ` : ${chiffreDe(ligne)}` : ''}`,
        ]
        continue
      }
      empiler(ligne)
    }
  }

  return lignes
}

/**
 * Les activations telles que le MOTEUR les a résolues.
 *
 * C'est la seule source qui connaisse la composition d'un coup : la comparaison
 * de photos voit « 5 dégâts » mais ne saura jamais que c'était 3 d'attaque et
 * 2 de boost, et elle recompte ce que le moteur rend plusieurs fois autour
 * d'une même résolution. Quand le journal est là, il remplace la déduction —
 * il ne la complète pas, sinon chaque activation paraîtrait deux fois.
 */
function lignesDuMoteur(faits: FaitMechant[], noms: Noms): Ligne[] {
  return faits.map((fait, index) => ({
    cle: `moteur:${index}:${fait.auteur_id}:${fait.cible_id}`,
    genre: fait.genre === 'attaque' ? 'attaque' : 'manigance',
    cause: fait.cause || undefined,
    titre: `${fait.auteur} ${fait.genre === 'attaque' ? t('attaque') : t('manigance sur')} ${fait.cible}`,
    cibleId: fait.cible_id,
    acteur: fait.auteur,
    // Les dégâts se comptent en négatif comme partout ailleurs ici : c'est la
    // variation du compteur de la cible (voir HistoriquePartie).
    valeur: fait.genre === 'attaque' ? -fait.subi : fait.subi,
    restant: fait.restant ?? undefined,
    plafond: noms.plafond(fait.cible_id),
    calcul: { base: fait.base, boost: fait.boost, defense: fait.defense },
    boosts: fait.boosts.map((boost, rang) => ({
      cle: `moteur:${index}:boost:${rang}:${boost.id}`,
      nom: boost.nom,
      cibleId: boost.id,
      apport: boost.apport,
    })),
  }))
}

function etapeDe(
  entrees: EntreeHistorique[],
  definition: (typeof ETAPES)[number],
  noms: Noms,
  faitsMoteur: FaitMechant[]
): Etape | undefined {
  const brut = entrees.filter((e) => e.phase === definition.phase && e.type !== 'phase')
  if (brut.length === 0) return undefined

  // Le déroulé BRUT garde tout, y compris les rendus répétés du moteur : c'est
  // la vérité de ce qui s'est passé, et on vient l'y chercher. Les faits, eux,
  // sont dédoublonnés — un bilan qui compte deux fois ment sur le danger.
  const faits = sansDoublons(brut.filter((e) => TYPES_FAITS.has(e.type)))

  let menace = 0
  let degats = 0
  let cartes = 0
  for (const e of faits) {
    // `valeur` est la variation signée du compteur (voir HistoriquePartie) :
    // une menace retirée se soustrait d'elle-même, sans test de sens ici.
    if (e.type === 'threat') menace += e.valeur ?? 0
    if (e.type === 'damage') degats += Math.abs(e.valeur ?? 0)
    // Une carte de boost n'est pas une carte de plus : elle appartient à
    // l'activation, et le total la compterait deux fois.
    if (e.type === 'card' && !e.boost) cartes += 1
  }

  // Partage du travail quand le moteur a parlé : les COUPS viennent de lui,
  // qui seul en connaît la composition et ne les compte qu'une fois ; les
  // CARTES restent déduites, le journal ne les couvrant pas.
  //
  // Sans ce partage, les dégâts d'une attaque déclenchée par une carte révélée
  // paraissaient deux fois — une fois dans le journal, une fois collés à la
  // carte révélée juste avant, qui n'y était souvent pour rien.
  const duMoteur = faitsDeLEtape(faitsMoteur, definition.phase)
  const deduites = lignesDeLEtape(faits, noms)
  const lignes =
    duMoteur.length === 0
      ? deduites
      : rattacherAuxCauses(
          deduites.filter((l) => l.genre === 'carte').map((l) => ({ ...l, effets: undefined })),
          lignesDuMoteur(duMoteur, noms)
        )

  // Les totaux suivent CE QUI EST AFFICHÉ : un total calculé sur les entrées
  // déduites pendant qu'on montre le journal du moteur annoncerait un autre
  // chiffre que la somme des lignes juste en dessous.
  if (lignes !== deduites) {
    menace = lignes.reduce((somme, l) => somme + (l.genre === 'attaque' ? 0 : (l.valeur ?? 0)), 0)
    degats = lignes.reduce((somme, l) => somme + (l.genre === 'attaque' ? Math.abs(l.valeur ?? 0) : 0), 0)
    cartes = lignes.filter((l) => l.genre === 'carte').length
  }

  // Une étape qui n'a produit QUE de la narration n'a rien à montrer, mais son
  // déroulé reste consultable : on la garde, repliée.
  return { numero: definition.numero, titre: definition.titre, lignes, brut, menace, degats, cartes }
}

export function bilanDeLaPhase(
  entrees: EntreeHistorique[],
  round: number,
  noms: Noms = { carte: () => undefined, heros: () => undefined, plafond: () => undefined },
  faitsMoteur: FaitMechant[] = []
): Bilan | undefined {
  const dedans = entrees.filter((e) => e.round === round && PHASES_MECHANT.has(e.phase))
  // Ordre du jeu : l'historique empile les plus récentes en tête.
  const ordonnees = [...dedans].reverse()
  const etapes = ETAPES.map((definition) =>
    etapeDe(ordonnees, definition, noms, faitsMoteur)
  ).filter((e): e is Etape => e !== undefined)
  if (etapes.length === 0) return undefined
  return { cle: `${round}`, round, etapes }
}

export function RecapPhaseMechant({
  entrees,
  monde,
  actif,
  suspendu = false,
  cartesMonde,
  catalogue,
  playerId,
}: {
  entrees: EntreeHistorique[]
  monde: World | undefined
  actif: boolean
  /**
   * Un autre panneau occupe l'ecran : le bilan est RETENU, pas perdu.
   *
   * Le recap se remplit a la SORTIE de la phase du mechant, un instant qui ne
   * repasse pas : le couper a ce moment-la reviendrait a ne jamais l'afficher.
   * On le garde donc en etat et on ne le dessine pas, jusqu'a ce que la place
   * se libere.
   *
   * En mode detaille, ce panneau est le cartouche du deroule (DeroulePhase),
   * qui raconte la phase pendant qu'elle se joue. Deux panneaux qui se
   * disputent l'ecran ont deja coute un tour de correction sur ce chantier.
   */
  suspendu?: boolean
  /** Les cartes du monde par object id, pour retrouver celle d'une ligne. */
  cartesMonde?: Map<number, WorldCard>
  catalogue?: Catalogue
  playerId?: number
}) {
  const [bilan, setBilan] = useState<Bilan | undefined>(undefined)
  const [depliees, setDepliees] = useState<Set<number>>(() => new Set())
  const phasePrecedente = useRef<string | undefined>(undefined)

  // Les noms sont lus au moment du bilan, sur le monde tel qu'il est alors. Une
  // carte partie (toute carte de boost l'est) n'y répond plus : les entrées
  // portent donc leur propre `nomCarte`, qui, lui, ne s'efface pas.
  const noms: Noms = useMemo(
    () => ({
      carte: (id) => (id === undefined ? undefined : cartesMonde?.get(id)?.name),
      heros: (joueur) => {
        if (joueur === undefined) return undefined
        const heros = monde?.players?.[joueur]?.area_hero?.[0]?.name
        return heros ? heros.replace(/^\W*/, '') : `P${joueur + 1}`
      },
      plafond: (id) => {
        if (id === undefined) return undefined
        const cible = cartesMonde?.get(id)?.info?.target_threat
        return typeof cible === 'number' && cible > 0 ? cible : undefined
      },
    }),
    [cartesMonde, monde]
  )
  const nomsRef = useRef(noms)
  nomsRef.current = noms

  useEffect(() => {
    const phase = monde?.phase
    const avant = phasePrecedente.current
    phasePrecedente.current = phase

    if (!actif || phase === undefined || avant === undefined) return
    // On ne déclenche qu'à la SORTIE de la phase du méchant.
    if (!PHASES_MECHANT.has(avant) || PHASES_MECHANT.has(phase)) return
    setDepliees(new Set())
    setBilan(
      bilanDeLaPhase(entrees, monde?.round_id ?? 0, nomsRef.current, monde?.faits_mechant ?? [])
    )
  }, [monde?.phase, monde?.round_id, monde?.faits_mechant, actif, entrees])

  // La carte survolée, montrée dans le MÊME agrandissement que sur la table.
  //
  // Délai identique à celui du plateau (200 ms) : sans lui, l'aperçu clignote
  // dès qu'on traverse la liste pour atteindre « Continuer ».
  const [survolId, setSurvolId] = useState<number | undefined>(undefined)
  const minuteur = useRef<number | undefined>(undefined)

  const pointer = useCallback((cibleId: number | undefined) => {
    window.clearTimeout(minuteur.current)
    if (cibleId === undefined) {
      setSurvolId(undefined)
      return
    }
    minuteur.current = window.setTimeout(() => setSurvolId(cibleId), 200)
  }, [])

  // Au doigt, il n'y a pas de survol : l'appui ouvre l'aperçu, un second appui
  // (ou un appui ailleurs) le referme. Le délai n'a plus lieu d'être.
  const appuyer = useCallback((cibleId: number | undefined) => {
    window.clearTimeout(minuteur.current)
    setSurvolId((actuel) => (actuel === cibleId ? undefined : cibleId))
  }, [])

  useEffect(() => () => window.clearTimeout(minuteur.current), [])

  const contexte: ContexteCarte | undefined = useMemo(
    () =>
      catalogue
        ? { playerId: playerId ?? 0, actives: new Set(monde?.active_card_ids ?? []), catalogue }
        : undefined,
    [catalogue, playerId, monde?.active_card_ids]
  )

  const carteSurvolee: ScanCardProps | undefined = useMemo(() => {
    if (survolId === undefined || !contexte) return undefined
    const carte = cartesMonde?.get(survolId)
    // Une carte qui a quitté la table (une carte de boost part à la défausse
    // aussitôt résolue) n'est plus dans le monde : pas d'aperçu pour elle
    // plutôt qu'un aperçu qui mentirait sur son état.
    if (!carte) return undefined
    return toScanCard(carte, contexte)
  }, [survolId, cartesMonde, contexte])

  // Retenu tant qu'un autre panneau occupe l'ecran : le bilan reste en etat et
  // paraitra des que la place se libere (voir `suspendu`).
  if (!bilan || suspendu) return null

  const totaux = (etape: Etape) => {
    const morceaux: string[] = []
    if (etape.menace !== 0)
      morceaux.push(`${etape.menace > 0 ? '+' : ''}${etape.menace} ${t('menace')}`)
    if (etape.degats > 0) morceaux.push(`${etape.degats} ${t('dégâts')}`)
    if (etape.cartes > 0) morceaux.push(`${etape.cartes} ${t('carte(s)')}`)
    return morceaux.join(' · ')
  }

  const survolProps = (cibleId: number | undefined) =>
    cibleId === undefined
      ? {}
      : {
          className: 'est-survolable',
          onMouseEnter: () => pointer(cibleId),
          onMouseLeave: () => pointer(undefined),
          onPointerUp: (evenement: React.PointerEvent) => {
            if (evenement.pointerType === 'mouse') return
            appuyer(cibleId)
          },
        }

  const ligne = (ligne: Ligne) => (
    <li
      key={ligne.cle}
      className={`recap-ligne est-${ligne.genre}${ligne.cause ? ' est-declenchee' : ''}`}
    >
      <span className="recap-mechant-fait" {...survolProps(ligne.cibleId)}>
        <b>{ligne.titre}</b>
        {ligne.heros ? <em className="recap-mechant-heros">{ligne.heros}</em> : null}
        {ligne.cause ? (
          <em className="recap-mechant-cause">
            {t('déclenché par')} {ligne.cause}
          </em>
        ) : null}
      </span>
      {chiffreDe(ligne) ? (
        <strong className="recap-mechant-chiffre">{chiffreDe(ligne)}</strong>
      ) : null}
      {ligne.calcul ? (
        <span className="recap-mechant-calcul">{detailDuCalcul(ligne.calcul)}</span>
      ) : null}
      {ligne.boosts && ligne.boosts.length > 0 ? (
        <span className="recap-mechant-boosts">
          {t('boost')} :{' '}
          {ligne.boosts.map((boost, index) => (
            <span key={boost.cle}>
              {index > 0 ? ', ' : ''}
              <span {...survolProps(boost.cibleId)}>{boost.nom}</span>
              {boost.apport !== undefined ? ` (+${boost.apport})` : null}
            </span>
          ))}
        </span>
      ) : null}
      {ligne.effets?.map((effet) => (
        <small key={effet}>{effet}</small>
      ))}
    </li>
  )

  return (
    <div
      className="recap-mechant"
      role="dialog"
      aria-label={t('Bilan de la phase du méchant')}
      onPointerUp={(evenement) => {
        // Un appui hors d'une ligne referme l'aperçu (tactile).
        if (evenement.pointerType === 'mouse') return
        if (!(evenement.target as HTMLElement).closest('.est-survolable')) setSurvolId(undefined)
      }}
    >
      <div className="recap-mechant-carte">
        <header>
          <span className="plateau-eyebrow">{t('Phase du méchant')}</span>
          <strong>
            {t('Round')} {bilan.round}
          </strong>
        </header>

        {bilan.etapes.map((etape) => {
          const depliee = depliees.has(etape.numero)
          return (
            <section className="recap-mechant-groupe" key={etape.numero}>
              <span className="plateau-eyebrow">
                <i>{etape.numero}</i>
                {t(etape.titre)}
                {totaux(etape) ? <b className="recap-mechant-total">{totaux(etape)}</b> : null}
                <button
                  type="button"
                  className="recap-mechant-repli"
                  aria-expanded={depliee}
                  title={t('Voir le déroulé complet du moteur')}
                  onClick={() =>
                    setDepliees((avant) => {
                      const apres = new Set(avant)
                      if (!apres.delete(etape.numero)) apres.add(etape.numero)
                      return apres
                    })
                  }
                >
                  {depliee ? '▾' : '▸'}
                </button>
              </span>

              {etape.lignes.length > 0 ? <ul>{etape.lignes.map(ligne)}</ul> : null}

              {depliee ? (
                <ul className="recap-mechant-deroule">
                  {etape.brut.map((entree) => (
                    <li key={entree.cle}>{entree.titre}</li>
                  ))}
                </ul>
              ) : null}
            </section>
          )
        })}

        <button
          type="button"
          className="recap-mechant-ok"
          onClick={() => {
            setSurvolId(undefined)
            setBilan(undefined)
          }}
          autoFocus
        >
          {t('Continuer')}
        </button>
      </div>

      {carteSurvolee ? <CarteApercu carte={carteSurvolee} classe="au-dessus-du-bilan" /> : null}
    </div>
  )
}
