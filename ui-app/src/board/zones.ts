// Decoupage du descripteur en emplacements de table.
//
// La disposition reprend celle de l'ancien plateau, mesuree sur le jeu :
// une table de taille FIXE, mise a l'echelle de la fenetre, qui ne defile
// jamais. Trois colonnes : les piles a gauche, les personnages au centre, les
// complots a droite, la main en bas sur toute la largeur.
//
// Aucune zone du descripteur n'est jetee en silence : chaque tableau de cartes
// de /get_world atterrit dans un emplacement, sauf UNE exception documentee plus
// bas (area_insert). Les emplacements vides ne sont pas dessines.
//
// Les piles (decks, defausses) sont resumees a une carte porteuse de leur
// hauteur : 38 dos de deck de rencontre cote a cote n'apprennent rien.

import { kindLabel, type ScanCardProps } from '../components/ScanCard'
import type { Catalogue } from './catalogue'
import { representantNemesis, scanUrl, toPileCard, toScanCard, type ContexteCarte } from './card-model'
import { t } from './langue'
import { collectionPourJoueur, lireArtsRessources } from './variantes'
import { estUneCarte, isVisibleFor, type World, type WorldCard, type WorldPlayer } from './world'

/** Une carte posee, avec ce qui lui est attache (ameliorations, statuts). */
/** Réduit un libellé à sa substance : sans accents, sans ponctuation, sans
 *  casse. « Némésis » et « nemesis » doivent se rejoindre. */
function reduire(texte: string): string {
  return (
    texte
      .normalize('NFD')
      .replace(/[\u0300-\u036f]/g, '')
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, ' ')
      .trim()
      // Le pluriel ne compte pas : « Manigances annexes » nomme bien une
      // « Manigance annexe ».
      .replace(/(\w{3,})s\b/g, '$1')
  )
}

/**
 * La pastille de type de cette carte dit-elle déjà ce que dit le titre de sa
 * zone ? « Méchant » dans la zone Méchant, « Environnement » dans la zone
 * « Alliés, sbires et environnement ». Le dos d'une carte (« Carte ») n'apprend
 * rien non plus : une pile de deck se reconnaît à sa zone.
 */
export function pastilleRedondante(titreZone: string, carte: ScanCardProps): boolean {
  if (carte.facedown === true) return true
  const type = reduire(carte.labelType || (carte.estNemesis === true ? t('Némésis') : t(kindLabel[carte.kind])))
  if (!type) return false
  const zone = reduire(titreZone)
  return zone === type || zone.split(' ').includes(type) || zone.includes(' ' + type) || zone.startsWith(type + ' ')
}

/** Un groupe dans une pile ouverte : d'où viennent ces cartes. */
export type GroupeDePile = { cle: string; titre: string; cartes: ScanCardProps[] }

export type UniteAffichee = {
  cle: string
  carte: ScanCardProps
  attachees: ScanCardProps[]
  /**
   * Contenu complet d'une pile PUBLIQUE (defausse, victoire, retirees...) : on
   * peut cliquer la pile pour l'etaler et la regarder. Absent = pile non
   * regardable (deck secret) ou carte simple.
   */
  pileContenu?: ScanCardProps[]
  /** Titre de la pile regardable (« Discard pile »...). */
  pileTitre?: string
  /**
   * Une pile faite de PLUSIEURS piles (« autres piles ») : à l'ouverture, les
   * cartes se lisent groupées par origine, un titre par groupe.
   */
  pileGroupes?: GroupeDePile[]
  /**
   * Phases A VENIR (vilain ou complot) : posees en petit tas DERRIERE la carte
   * actuelle, pour dire qu'il en reste, sans les etaler sur la table.
   */
  stagesArriere?: ScanCardProps[]
  /** Toutes les phases (actuelle + a venir), pour la vue au clic du bouton. */
  stagesTout?: ScanCardProps[]
  /** Titre de la vue des phases (« Villain stages »...). */
  stagesTitre?: string
}

/**
 * Les emplacements de la table. Ce sont les noms des zones de la grille dans
 * board.css : ajouter une valeur ici demande d'ajouter la zone la-bas.
 */
export type CleEmplacement =
  | 'piles-rencontre'
  | 'rencontre'
  | 'complot-principal'
  | 'complots-secondaires'
  | 'terrain-combat'
  | 'terrain-soutien'
  | 'deck-special'
  | 'piles-joueur'
  | 'nemesis'
  | 'annexes'
  | 'reserve'
  | 'main'

export type EmplacementAffiche = {
  cle: CleEmplacement
  titre: string
  /** Groupes de cartes, separes visuellement, sans etiquette propre. */
  groupes: UniteAffichee[][]
  /** Nombre d'elements dessines sur la ligne : sert au chevauchement en CSS. */
  nombreSurLaLigne: number
  /**
   * Identifiant du joueur proprietaire de chaque groupe, meme longueur que
   * `groupes`. Renseigne pour `terrain-soutien` seulement, ou les aires de tous
   * les joueurs sont aplaties. Le rendu PC l'ignore : c'est le mode mobile qui
   * s'en sert pour ne deplier qu'un joueur a la fois.
   */
  proprietaires?: number[]
}

export type Plateau = {
  emplacements: EmplacementAffiche[]
  /** Nombre de cartes reellement dessinees, piles comprises (1 par pile). */
  nombreDeCartes: number
  /**
   * Identifiants des cartes REELLEMENT dessinees. Une pile n'en montre qu'une :
   * les 33 autres cartes d'un deck n'y sont pas. L'interaction s'en sert pour
   * savoir quelles cibles demandees par le moteur ne sont pas sur la table et
   * ont besoin d'un selecteur (une capacite de recherche cible le deck).
   */
  idsAffiches: Set<number>
  /**
   * Pour une carte compactee dans une pile, id de la carte qui represente cette
   * pile sur la table. Sert a mettre en avant la pile quand une action cible une
   * carte hors table.
   */
  representantsDePile: Map<number, number>
  /**
   * Entrees ecartees parce qu'elles n'avaient pas la forme d'une carte. Doit
   * rester a zero ; sinon le contrat du descripteur a bouge et l'interface le
   * dit au lieu de faire comme si de rien n'etait.
   */
  nombreIgnore: number
}

/**
 * Zones volontairement NON affichees comme telles :
 *
 * - area_insert : carte-repere de regles (pic_id « rule »), un aide-memoire du
 *   moteur, pas une carte posee sur la table.
 * - area_status_cards : liste globale des cartes de statut (Stunned/Confused/
 *   Tough). Le moteur les rend DEJA sur leur personnage (ToDescriptor.Card les
 *   attache a leur porteur), ou elles s'affichent en petits marqueurs. Les
 *   remontrer ici en pile ferait un doublon qui n'apprend rien et mange une case.
 */
const ZONES_IGNOREES = ['area_insert', 'area_status_cards']

type Options = {
  playerId: number
  catalogue: Catalogue
  /** Rafraichi quand le joueur change de collection d'arts (cosmetique). */
  artsVersion?: number
  /**
   * La vue est BRAQUEE sur `playerId` : on ne pose que SA table. Les aires des
   * autres joueurs (heros, allies, soutiens, ennemis engages, piles) sortent du
   * plateau ; la table commune — mechant, complots, environnement, deck
   * rencontre — reste, elle n'est a personne.
   *
   * Sert le mode « Vue : un joueur » de la barre du haut. En « Auto », la table
   * montre tout le monde, comme une vraie partie a plusieurs.
   */
  seulCeJoueur?: boolean
}

/** Contexte de rendu : la traduction des cartes, plus le compte des ecarts. */
type Rendu = {
  ctx: ContexteCarte
  ecartes: { total: number }
  representantsDePile: Map<number, number>
}

/**
 * Ne garde que ce qui a vraiment la forme d'une carte.
 *
 * Le descripteur n'est pas homogene : `additional_decks` contient des DECKS la
 * ou tout le reste contient des cartes. Une zone d'une forme imprevue doit
 * couter une zone, pas la table entiere.
 */
function cartes(liste: readonly unknown[] | undefined, rendu: Rendu): WorldCard[] {
  if (!Array.isArray(liste)) return []
  const gardees = liste.filter(estUneCarte)
  rendu.ecartes.total += liste.length - gardees.length
  return gardees
}

/**
 * Regroupe une liste de cartes en unites : les racines (bind_object_id === 0)
 * portent celles qui leur sont attachees.
 *
 * Verifie sur les 34 etats enregistres : une carte attachee est toujours dans
 * la meme zone que son porteur. Une carte dont le porteur est introuvable est
 * traitee comme une racine plutot que disparaitre.
 */
function enUnites(
  liste: WorldCard[],
  rendu: Rendu,
  options: { dansLaMain?: boolean; proprietaire?: string; collectionRessources?: string } = {}
): UniteAffichee[] {
  const ids = new Set(liste.map((carte) => carte.id))
  const attacheesPar = new Map<number, WorldCard[]>()

  for (const carte of liste) {
    if (carte.bind_object_id === 0 || !ids.has(carte.bind_object_id)) continue
    const groupe = attacheesPar.get(carte.bind_object_id) ?? []
    groupe.push(carte)
    attacheesPar.set(carte.bind_object_id, groupe)
  }

  const ctxCarte: ContexteCarte = {
    ...rendu.ctx,
    dansLaMain: options.dansLaMain,
    proprietaire: options.proprietaire,
    collectionRessources: options.collectionRessources,
  }

  return liste
    .filter((carte) => carte.bind_object_id === 0 || !ids.has(carte.bind_object_id))
    .map((carte) => ({
      cle: `carte-${carte.id}`,
      carte: toScanCard(carte, ctxCarte),
      attachees: (attacheesPar.get(carte.id) ?? []).map((attachee) =>
        toScanCard(attachee, ctxCarte)
      ),
    }))
}

/** Un groupe de cartes posees. Vide = pas de groupe. */
function posees(
  liste: readonly unknown[] | undefined,
  rendu: Rendu,
  options: { dansLaMain?: boolean; proprietaire?: string; collectionRessources?: string } = {}
): UniteAffichee[] {
  const valides = cartes(liste, rendu)
  return valides.length === 0 ? [] : enUnites(valides, rendu, options)
}

/** Un groupe de piles : chaque pile devient une carte porteuse de sa hauteur. */
function piles(
  cle: string,
  listes: Array<{
    cle: string
    cartes: readonly unknown[] | undefined
    /** Carte a montrer pour cette pile. Par defaut : le dessus. */
    representant?: (cartes: WorldCard[]) => WorldCard | undefined
    /** Etiqueter la carte « Nemesis » au lieu de son type. */
    nemesis?: boolean
    /** Pile PUBLIQUE : cliquable pour etaler et regarder son contenu. */
    regardable?: boolean
    /** Titre affiche quand on ouvre la pile regardable. */
    titre?: string
    /** Deck special du heros (Invocation...) : etiquette + halo violet. */
    deckSpecial?: boolean
    /** Cette pile est une defausse : badge « Discard » sur le cote. */
    discard?: boolean
    /** Remplace l'etiquette de type par ce texte (nom du deck special...). */
    labelType?: string
  }>,
  rendu: Rendu
): UniteAffichee[] {
  return listes.flatMap((pile) => {
    const contenu = cartes(pile.cartes, rendu)
    const carte = toPileCard(contenu, rendu.ctx, pile.representant)
    if (!carte) return []
    const representantId = Number(carte.id)
    for (const contenue of contenu) {
      rendu.representantsDePile.set(contenue.id, representantId)
    }
    // UNE PILE SE POSE EN PORTRAIT, toujours.
    //
    // Une manigance se pose en PAYSAGE sur la table, et une defausse montre sa
    // carte du dessus : quand une manigance y arrivait, la pile passait de 127 a
    // 176 px de large. Deck et defausse ne tenaient alors plus cote a cote dans
    // les 270 px de la colonne de gauche, se repliaient l'une sous l'autre, et
    // le groupe montait de 203 a 358 px — il debordait sur la rangee du dessous
    // et decalait la table entiere. Mesure du 8/8/2026, signale en jeu.
    //
    // Une pile n'est pas une carte posee, c'est un tas : elle a l'encombrement
    // d'une pile, pas celui de ce qui se trouve dessus. Et le redressement ne
    // coute RIEN a l'image — le jeu sert tous ses scans en portrait et c'est le
    // plateau qui les tourne pour les manigances (voir `scanIsPortrait`). En
    // retirant `isLandscape`, on ne fait donc que ne pas la tourner.
    carte.isLandscape = false

    if (pile.nemesis) carte.estNemesis = true
    if (pile.deckSpecial) carte.deckSpecial = true
    if (pile.discard) carte.discard = true
    if (pile.labelType) carte.labelType = pile.labelType
    const unite: UniteAffichee = { cle: `${cle}-${pile.cle}`, carte, attachees: [] }
    if (pile.regardable && contenu.length > 0) {
      // Du dessus vers le fond : la derniere posee (dessus) en premier.
      unite.pileContenu = [...contenu].reverse().map((c) => toScanCard(c, rendu.ctx))
      unite.pileTitre = pile.titre ?? carte.name
    }
    return [unite]
  })
}

/**
 * Plusieurs piles fondues en UNE, dessinee comme un dos de carte avec son
 * compteur (07/09/2026). La zone « Mises de côté / autres piles » dessinait
 * chaque pile a part, et la premiere visible posait sa pastille de type sur le
 * titre de la zone. Elle n'a plus que deux paquets : ce qu'on a le droit de
 * regarder, et ce qui reste cache.
 *
 * La pile VISIBLE s'ouvre sur ses cartes groupees par origine (« Pile de
 * victoire », « Retirées de la partie »...) : voir `pileGroupes`. La pile
 * CACHEE ne s'ouvre pas : on n'y voit que le nombre.
 *
 * Aucune perte pour le moteur : chaque carte contenue est rattachee au
 * representant (`representantsDePile`), donc ciblable par le selecteur hors
 * table comme avant.
 */
function pileFondue(
  cle: string,
  titre: string,
  listes: Array<{ cle: string; cartes: readonly unknown[] | undefined; titre: string }>,
  rendu: Rendu,
  visible: boolean
): UniteAffichee[] {
  const groupes = listes
    .map((pile) => ({ cle: pile.cle, titre: pile.titre, contenu: cartes(pile.cartes, rendu) }))
    .filter((pile) => pile.contenu.length > 0)
  if (groupes.length === 0) return []
  const tout = groupes.flatMap((pile) => pile.contenu)
  const carte = toPileCard(tout, rendu.ctx)
  if (!carte) return []
  const representant = tout.at(-1)
  const representantId = Number(carte.id)
  for (const contenue of tout) rendu.representantsDePile.set(contenue.id, representantId)
  // Un dos de carte, toujours : le contenu se lit en ouvrant la pile, pas sur
  // la table. Le dos est celui de la derniere carte arrivee.
  carte.isLandscape = false
  carte.facedown = true
  carte.kind = 'unknown'
  carte.name = titre
  carte.imageUrl = scanUrl(representant?.down_card_ids[0] ?? 'no_image')
  const unite: UniteAffichee = { cle: `${cle}-${visible ? 'visibles' : 'cachees'}`, carte, attachees: [] }
  if (visible) {
    unite.pileTitre = titre
    unite.pileGroupes = groupes.map((pile) => ({
      cle: pile.cle,
      titre: pile.titre,
      // Du dessus vers le fond, comme une pile qu'on etale.
      cartes: [...pile.contenu].reverse().map((c) => toScanCard(c, rendu.ctx)),
    }))
    unite.pileContenu = unite.pileGroupes.flatMap((groupe) => groupe.cartes)
  }
  return [unite]
}

/**
 * Attache a la 1ere unite (le vilain, ou le complot principal actuel) ses phases
 * A VENIR : un petit tas derriere la carte + une vue de TOUTES les phases au clic
 * du bouton. Evite d'etaler sur la table des cartes qui n'ont pas encore d'effet.
 */
function avecStages(
  unites: UniteAffichee[],
  aVenir: readonly unknown[] | undefined,
  titre: string,
  rendu: Rendu
): UniteAffichee[] {
  const stages = cartes(aVenir, rendu)
  if (unites.length === 0 || stages.length === 0) return unites
  const unite = unites[0]
  const representantId = Number(unite.carte.id)
  for (const stage of stages) {
    rendu.representantsDePile.set(stage.id, representantId)
  }
  unite.stagesArriere = stages.map((carte) => toScanCard(carte, rendu.ctx))
  unite.stagesTout = [unite.carte, ...unite.stagesArriere]
  unite.stagesTitre = titre
  return unites
}

/**
 * L'aire des vilains, qui gere aussi le MULTI-VILAINS.
 *
 * - Les vilains ACTIFS (area_villain) sont poses cote a cote : on ne cache
 *   jamais une menace qui agit.
 * - Le deck vilain est reparti par HEURISTIQUE DE NOM :
 *     * meme nom qu'un vilain actif  -> ses PHASES a venir, empilees derriere lui ;
 *     * nom different                -> un autre vilain EN ATTENTE.
 * - Les vilains en attente forment UNE pile grisee « Waiting » a cote, dont le
 *   clic n'ouvre QUE ce qui est cache (les vilains a venir).
 *
 * HEURISTIQUE VALIDEE le 2/8/2026 sur deux parties reelles enregistrees :
 *   - Sinister Six : 2 a 4 EncounterVillain simultanes dans area_villain,
 *     entremeles avec leurs attachements (bind_object_id porte le lien) ;
 *     les vilains pas encore en jeu attendent dans area_set_aside (face
 *     visible, card_type EncounterVillain) et en sortent quand ils entrent ;
 *     villain_deck reste vide toute la partie.
 *   - Wrecking Crew : 4 EncounterVillain simultanes, villain_deck vide.
 * Le deck vilain ne sert donc les phases que dans les scenarios classiques a
 * vilain unique (Rhino I/II/III...), ou la comparaison de noms est exacte.
 */
/**
 * Nom d'un deck special, deduit du TRAIT commun a toutes ses cartes : le deck
 * d'Invocation de Strange a des cartes toutes marquees « t_INVOCATION » ->
 * « Invocation ». A defaut de trait commun, on retombe sur « Special deck ».
 */
function nomDeckSpecial(liste: readonly unknown[] | undefined): string | undefined {
  const cartesDeck = (Array.isArray(liste) ? liste : []).filter(estUneCarte)
  if (cartesDeck.length === 0) return undefined
  const communs = Object.keys(cartesDeck[0].traits ?? {}).filter(
    (trait) => trait.startsWith('t_') && cartesDeck.every((c) => (c.traits ?? {})[trait])
  )
  const trait = communs[0]
  if (!trait) return undefined
  const mot = trait.slice(2)
  return mot.charAt(0) + mot.slice(1).toLowerCase()
}

/** Une carte de type vilain (utilise sur le brut du descripteur ou une WorldCard). */
function estVilain(carte: unknown): boolean {
  return (
    typeof carte === 'object' &&
    carte !== null &&
    (carte as { card_type?: unknown }).card_type === 'EncounterVillain'
  )
}

function airesVilains(world: World, rendu: Rendu): UniteAffichee[] {
  const actifs = posees(world.area_villain, rendu)
  const nomsActifs = new Set(actifs.map((unite) => unite.carte.name))
  const deck = cartes(world.villain_deck, rendu)
  const phases = deck.filter((carte) => nomsActifs.has(carte.name))
  // Vilains EN ATTENTE : ceux du deck vilain (autre nom) ET les vilains mis de
  // cote (Sinister Six range ses 6 vilains dans area_set_aside). On confirme sur
  // le vrai descripteur : Electro/Vulture actifs, les 4 autres en area_set_aside.
  const misDeCote = cartes(world.area_set_aside, rendu).filter(estVilain)
  const attente = [...deck.filter((carte) => !nomsActifs.has(carte.name)), ...misDeCote]

  // Phases a venir : derriere le vilain actif de MEME NOM, groupees par nom.
  // Jamais observe avec plusieurs noms a la fois (cf. commentaire ci-dessus),
  // mais si un scenario le fait un jour, chaque vilain garde ses phases.
  if (phases.length > 0 && actifs.length > 0) {
    const parNom = new Map<string, typeof phases>()
    for (const carte of phases) {
      const liste = parNom.get(carte.name) ?? []
      liste.push(carte)
      parNom.set(carte.name, liste)
    }
    for (const [nom, liste] of parNom) {
      const cible = actifs.find((u) => u.carte.name === nom) ?? actifs[0]
      cible.stagesArriere = liste.map((carte) => toScanCard(carte, rendu.ctx))
      cible.stagesTout = [cible.carte, ...cible.stagesArriere]
      cible.stagesTitre = t('Stades du Méchant')
    }
  }

  const unites = [...actifs]

  // Autres vilains EN ATTENTE : une pile grisee « Waiting », consultable.
  if (attente.length > 0) {
    const carte = toPileCard(attente, rendu.ctx)
    if (carte) {
      const representantId = Number(carte.id)
      for (const attendue of attente) {
        rendu.representantsDePile.set(attendue.id, representantId)
      }
      carte.inactif = true
      unites.push({
        cle: 'villains-attente',
        carte,
        attachees: [],
        pileContenu: attente.map((c) => toScanCard(c, rendu.ctx)),
        pileTitre: t('Méchants à venir'),
      })
    }
  }
  return unites
}

function emplacement(
  cle: CleEmplacement,
  titre: string,
  groupes: UniteAffichee[][],
  // Proprietaire de chaque groupe, meme longueur et meme ordre que `groupes`.
  // Seul terrain-soutien le fournit (voir plus bas) : c'est ce que lit le mode
  // mobile pour recoudre les groupes par joueur (mobile/joueurs.ts).
  proprietaires?: number[]
): EmplacementAffiche | undefined {
  // Les groupes vides sont retires ; on filtre les proprietaires du meme geste,
  // pour que les deux tableaux restent alignes apres coup.
  const gardes = groupes
    .map((groupe, index) => ({ groupe, proprietaire: proprietaires?.[index] }))
    .filter((garde) => garde.groupe.length > 0)
  if (gardes.length === 0) return undefined
  // On ne compte que les UNITES posees sur la rangee. Les upgrades ne prennent
  // plus de place en largeur : elles sont glissees derriere leur porteur (voir
  // .plateau-unite dans board.css), donc les inclure ici surcomprimerait la ligne.
  const nombreSurLaLigne = gardes.reduce((total, garde) => total + garde.groupe.length, 0)
  return {
    cle,
    titre,
    groupes: gardes.map((garde) => garde.groupe),
    nombreSurLaLigne,
    ...(proprietaires ? { proprietaires: gardes.map((garde) => garde.proprietaire as number) } : {}),
  }
}

export function construirePlateau(world: World, options: Options): Plateau {
  const rendu: Rendu = {
    ctx: {
      playerId: options.playerId,
      actives: new Set(world.active_card_ids ?? []),
      catalogue: options.catalogue,
    },
    ecartes: { total: 0 },
    representantsDePile: new Map(),
  }

  const joueurs = Array.isArray(world.players) ? world.players : []

  // Un joueur ELIMINE quitte la table, carte de heros comprise.
  //
  // Le moteur defausse tout ce qu'il controlait (allies, soutiens, main, deck,
  // obligations) mais PAS sa carte d'identite : `Player.Eliminate` exclut
  // explicitement le type Identity de la defausse. Un heros mort restait donc
  // pose au milieu du terrain, seul rescape de son aire.
  //
  // Et il reste dans `world.players` VOLONTAIREMENT — le descripteur est
  // construit sur `const_seat_order_players`, ce qui garde les numeros de siege
  // stables et donc le sens de `playerId`. C'est donc a l'affichage de l'ecarter,
  // pas au moteur.
  const surLaTable = (joueur: WorldPlayer | undefined): boolean =>
    joueur !== undefined && !joueur.is_eliminated
  const notre: WorldPlayer | undefined = surLaTable(joueurs[options.playerId])
    ? joueurs[options.playerId]
    : undefined
  const autres = options.seulCeJoueur
    ? []
    : joueurs.filter((joueur, index) => index !== options.playerId && surLaTable(joueur))
  // En multi, les allies/sbires des deux camps cohabitent dans la meme zone :
  // chaque carte porte alors le NOM de son heros proprietaire en badge.
  const multi = joueurs.length > 1
  const nomHero = (joueur: WorldPlayer | undefined): string | undefined =>
    multi ? joueur?.area_hero?.[0]?.name : undefined

  // Collection d'arts des ressources doubles, choisie a la preparation. Elle
  // s'applique aux cartes DU joueur concerne (main, deck, defausse) : chacun
  // garde donc ses propres visuels en partie a plusieurs.
  const arts = lireArtsRessources()
  const collectionDe = (joueur: WorldPlayer | undefined): string => {
    const heros = joueur?.area_hero?.[0]
    return collectionPourJoueur(heros?.card_id, heros?.id, arts)
  }
  const notreCollection = collectionDe(notre)

  // Deck special consultable SEULEMENT si la regle l'autorise, ce que le moteur
  // encode par la visibilite : on ne l'ouvre que si ses cartes nous sont visibles
  // (sinon on n'a pas le droit de regarder dedans, comme un deck ordinaire).
  const cartesDeckSpecial = (notre?.additional_deck ?? []).filter(estUneCarte)
  const deckSpecialConsultable =
    cartesDeckSpecial.length > 0 &&
    cartesDeckSpecial.every((carte) => isVisibleFor(carte, options.playerId))
  // Nom du deck special (ex. « Invocation »), pour son etiquette et sa zone.
  const nomSpecial =
    nomDeckSpecial(notre?.additional_deck) ??
    nomDeckSpecial(notre?.additional_discard_pile) ??
    t('Deck spécial')

  // Au PLURIEL, une entree de ces deux zones est un deck entier, pas une carte.
  const decksSupplementaires = (world.additional_decks ?? []).map((deck, index) => ({
    cle: `deck-${index}`,
    cartes: deck,
  }))
  const defaussesSupplementaires = (world.additional_discard_piles ?? []).map((pile, index) => ({
    cle: `defausse-${index}`,
    cartes: pile,
  }))

  const emplacements = [
    emplacement('piles-rencontre', t('Deck Rencontre'), [
      piles(
        'rencontre',
        [
          // Le deck vilain (ses phases a venir) n'est plus une pile a part : il
          // est empile derriere le vilain actuel (voir avecStages plus bas).
          { cle: 'encounter-deck', cartes: world.encounter_deck },
          {
            cle: 'encounter-discard',
            cartes: world.encounter_discard_pile,
            regardable: true,
            titre: t('Défausse Rencontre'),
          },
        ],
        rendu
      ),
    ]),

    emplacement('rencontre', t('Méchant'), [
      airesVilains(world, rendu),
      posees(world.area_revealing, rendu),
      posees(world.area_processing, rendu),
      posees(world.area_boost, rendu),
      posees(notre?.dealt_encounter_cards, rendu),
    ]),

    // Le complot actif (area_schemes_main), avec ses etapes A VENIR
    // (main_schemes_deck) empilees derriere et consultables au bouton.
    emplacement('complot-principal', t('Manigance principale'), [
      avecStages(
        posees(world.area_schemes_main, rendu),
        world.main_schemes_deck,
        'Scheme stages',
        rendu
      ),
    ]),

    emplacement('complots-secondaires', t('Manigances annexes'), [
      posees(world.area_schemes_side, rendu),
    ]),

    // Rangee HAUTE de l'aire joueur : la ligne de combat (adjacente a la menace).
    // Allies, sbires engages ET environnement : tout ce qui "vit" sur le terrain.
    emplacement('terrain-combat', t('Alliés, sbires et environnement'), [
      posees(notre?.allies, rendu, { proprietaire: nomHero(notre) }),
      posees(notre?.engaged_enemies, rendu, { proprietaire: nomHero(notre) }),
      posees(world.area_environment, rendu),
      posees(notre?.environment_area, rendu),
      // En multijoueur, les autres joueurs partagent l'aire : leur ligne de combat.
      ...autres.flatMap((joueur) => [
        posees(joueur.allies, rendu, { proprietaire: nomHero(joueur) }),
        posees(joueur.engaged_enemies, rendu, { proprietaire: nomHero(joueur) }),
      ]),
    ]),

    // Rangee CENTRALE de l'aire joueur : d'abord le DECK SPECIAL du heros s'il en
    // a un (Invocation de Strange, Daredevil...), pose a GAUCHE du heros ; puis le
    // HEROS, puis ce qui gravite autour (soutiens, permanents, obligations).
    // Le DECK SPECIAL du heros (Invocation...) a sa PROPRE zone, a gauche : deck +
    // sa defausse cote a cote. Le heros et ses soutiens sont decales a sa droite.
    emplacement('deck-special', nomSpecial, [
      piles(
        'soutien',
        [
          {
            cle: 'deck',
            cartes: notre?.additional_deck,
            deckSpecial: true,
            titre: nomSpecial,
            regardable: deckSpecialConsultable,
          },
          // Sa defausse, JUSTE a cote (le cycle deck -> defausse -> remelange).
          // Une defausse est publique : toujours consultable. Le ruban « Discard »
          // ne sert qu'a la distinguer du deck : s'il n'y a QU'UNE pile affichee
          // (deck vide), il n'apporte rien et on ne le montre pas.
          {
            cle: 'defausse',
            cartes: notre?.additional_discard_pile,
            deckSpecial: true,
            discard: (notre?.additional_deck?.length ?? 0) > 0,
            titre: `${nomSpecial} discard`,
            regardable: true,
          },
        ],
        rendu
      ),
    ]),

    // La RESERVE (pack Brawn) prend la meme place que le deck special : a
    // GAUCHE du heros. C'est la zone personnelle du personnage, au meme titre
    // que l'Invocation de Strange — et aucun heros n'a les deux, l'emplacement
    // vide disparaissant tout seul (`emplacement()` retire les groupes vides).
    //
    // ⚠ En cartes POSEES et non en pile : contrairement a un deck special, on
    // joue et on depense les cartes de la reserve une par une, il faut donc
    // pouvoir les voir et les cliquer individuellement.
    emplacement('reserve', t('Ta réserve'), [
      posees(notre?.reserve, rendu, {
        dansLaMain: true,
        collectionRessources: notreCollection,
      }),
    ]),

    // Chaque groupe est appairee a son proprietaire au moment ou elle est
    // construite (pas dans un tableau separe recompte a la main) : si un jour
    // un joueur gagne ou perd un groupe ici, le proprietaire suit sans qu'on
    // ait besoin de resynchroniser deux listes.
    ((): EmplacementAffiche | undefined => {
      const groupesEtProprietaires: Array<[UniteAffichee[], number]> = [
        [posees(notre?.area_hero, rendu), options.playerId],
        [posees(notre?.supports, rendu), options.playerId],
        [posees(notre?.obligations_area, rendu), options.playerId],
        ...autres.flatMap((joueur, index): Array<[UniteAffichee[], number]> => {
          const idJoueur = joueurs.indexOf(joueur)
          return [
            [
              piles(`soutien-autre-${index}`, [
                { cle: 'deck-special', cartes: joueur.additional_deck },
              ], rendu),
              idJoueur,
            ],
            [posees(joueur.area_hero, rendu), idJoueur],
            [posees(joueur.supports, rendu), idJoueur],
          ]
        }),
      ]
      return emplacement(
        'terrain-soutien',
        t('Héros et soutiens'),
        groupesEtProprietaires.map(([groupe]) => groupe),
        groupesEtProprietaires.map(([, idJoueur]) => idJoueur)
      )
    })(),

    // « Your piles » : UNIQUEMENT le deck et la defausse du joueur, cote a cote.
    emplacement('piles-joueur', t('Deck du héros'), [
      piles(
        'joueur',
        [
          { cle: 'deck', cartes: notre?.player_deck },
          {
            cle: 'defausse',
            cartes: notre?.player_discard_pile,
            regardable: true,
            titre: t('Pile de défausse'),
          },
        ],
        rendu
      ),
    ]),

    // « Other zones » : tout le reste, rare et divers (decks/defausses
    // supplementaires, mise de cote, victoire, cartes retirees, preuves...).
    // Sa PROPRE rangee, SOUS « Your piles ». Ne se dessine que si non vide.
    // Etiquette : surtout PAS « cartes défaussées ». Cette zone montre les
    // cartes MISES DE CÔTÉ (cartes liées en attente, comme les Specialist de
    // Specialized Training), la pile de victoire et les cartes retirées — la
    // défausse, elle, est à côté du deck. L'ancien libellé laissait croire que
    // ces cartes étaient défaussées.
    emplacement('annexes', t('Mises de côté / autres piles'), [
      posees(world.area_evidence, rendu),
      posees(world.area_rule, rendu),
      posees(world.area_resources, rendu),
      // DEUX paquets, pas une pile par origine (07/09/2026) : chaque pile
      // dessinee a part posait sa pastille sur le titre de la zone, et la
      // colonne de 253 px n'en tient que deux par ligne. Le paquet VISIBLE
      // s'ouvre, groupe par origine ; le paquet CACHE ne montre que son nombre.
      //
      // Les vilains mis de cote (Sinister Six) sont montres a cote du vilain
      // actif (pile « Waiting »), pas ici : on les retire des mises de cote.
      // Le deck special (Invocation...) et sa defausse sont a gauche du heros.
      pileFondue(
        'annexes',
        t('Cartes visibles'),
        [
          {
            cle: 'set-aside-scenario',
            cartes: (world.area_set_aside ?? []).filter((carte) => !estVilain(carte)),
            titre: t('Mises de côté du scénario'),
          },
          { cle: 'victoire', cartes: world.victory_display, titre: t('Pile de victoire') },
          { cle: 'retirees', cartes: world.area_removed, titre: t('Retirées de la partie') },
          ...defaussesSupplementaires.map((pile, index) => ({
            ...pile,
            titre: `${t('Défausse supplémentaire')} ${index + 1}`,
          })),
        ],
        rendu,
        true
      ),
      pileFondue(
        'annexes',
        t('Cartes cachées'),
        [
          { cle: 'mise-de-cote', cartes: notre?.set_aside_deck, titre: t('Deck mis de côté') },
          ...decksSupplementaires.map((pile, index) => ({
            ...pile,
            titre: `${t('Deck supplémentaire')} ${index + 1}`,
          })),
        ],
        rendu,
        false
      ),
    ]),

    // Le set NEMESIS a sa propre zone (l'ancienne case « Other zones », a gauche) :
    // c'est une menace personnelle en attente, pas une pile de jeu. On y montre le
    // nemesis lui-meme (pas une treachery du set), etiquete « Nemesis ».
    emplacement('nemesis', t('Némésis'), [
      piles(
        'nemesis',
        [
          {
            cle: 'set',
            cartes: notre?.set_aside_nemesis_sets,
            representant: representantNemesis,
            nemesis: true,
          },
        ],
        rendu
      ),
    ]),

    emplacement('main', t('Ta main'), [
      posees(notre?.hand_cards, rendu, {
        dansLaMain: true,
        collectionRessources: notreCollection,
      }),
    ]),
  ].filter((e): e is EmplacementAffiche => e !== undefined)

  const nombreDeCartes = emplacements.reduce((total, e) => total + e.nombreSurLaLigne, 0)

  const idsAffiches = new Set<number>()
  for (const emplacement of emplacements) {
    for (const groupe of emplacement.groupes) {
      for (const unite of groupe) {
        idsAffiches.add(Number(unite.carte.id))
        for (const attachee of unite.attachees) idsAffiches.add(Number(attachee.id))
      }
    }
  }

  return {
    emplacements,
    nombreDeCartes,
    idsAffiches,
    representantsDePile: rendu.representantsDePile,
    nombreIgnore: rendu.ecartes.total,
  }
}

/** Expose la liste des zones volontairement non affichees, pour l'interface. */
export const zonesNonAffichees = ZONES_IGNOREES
