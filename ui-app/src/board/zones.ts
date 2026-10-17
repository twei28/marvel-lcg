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
import { trouverPaire, type CotePanorama } from './panorama-jumelles'
import type { CleBrique } from './table-briques'
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
export type GroupeDePile = {
  cle: string
  titre: string
  cartes: ScanCardProps[]
  /** Pile MASQUÉE : le groupe ne montre que son nombre de cartes, jamais les cartes. */
  masque?: { nombre: number }
}

/**
 * Le secteur « ennemis engagés » du joueur regardé, dans `terrain-combat`
 * (voir `EmplacementAffiche.groupesPiles`). Lâcher un sbire dessus, en mode
 * manuel, engage ce sbire (`Puzzle.Engage`) plutôt que de le déplacer vers une
 * pile ordinaire — voir `board/manuel/glisser-manuel.ts`.
 */
export const CLE_PILE_ENGAGES = 'terrain-combat-engages'

/** Trait des cartes du deck Weather de Storm (voir `meteoEnJeu`). */
const TRAIT_METEO = 't_WEATHER'

export type UniteAffichee = {
  cle: string
  carte: ScanCardProps
  attachees: ScanCardProps[]
  /**
   * Carte d'une paire jumelle a illustration continue (`panorama-jumelles.ts`) :
   * posee A COTE de son porteur, pas dessous. Le rendu colle la `gauche` (14) et
   * la `droite` (15) bord a bord.
   */
  panorama?: CotePanorama
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
  /**
   * Tâche 5 (glisser-déposer, mode manuel) : présent SEULEMENT quand cette
   * unité est une pile désignable sans ambiguïté (un deck, une défausse...),
   * jamais sur une carte posée (allié, héros, sbire...) ni sur une pile
   * FONDUE de plusieurs origines (« Cartes visibles », « Cartes cachées » :
   * voir `pileFondue`) — celles-là mélangent plusieurs piles moteur
   * derrière un seul dos de carte, et il n'y a pas de pile unique à nommer.
   * Vaut toujours `cle` : deux fonctions qui recalculeraient la même chaîne
   * finiraient par diverger.
   */
  pile?: string
  /** Emplacement matériel d'une pile actuellement vide. Il reste dessiné et
   *  ciblable en mode manuel afin d'y déposer sa première carte. */
  pileVide?: boolean
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
  | 'annexes'
  | 'reserve'
  // AJOUT (pack wave) : la Rising Tide area, meme case que 'deck-special' et
  // 'reserve' (voir Board.tsx et board.css, "colonne-terrain-soutien") --
  // aucun heros n'a deux de ces trois zones personnelles a la fois.
  | 'rising-tide'
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
   * `groupes`. Renseigne pour `terrain-soutien` et `terrain-combat`, ou les
   * aires de tous les joueurs sont aplaties ; `undefined` pour un groupe a
   * personne (l'environnement). Le mode mobile s'en sert pour ne deplier
   * qu'un joueur a la fois ; le mode manuel pour poser une carte chez le
   * joueur du groupe vise (lot 5 du 06/10/2026, `data-joueur`).
   */
  proprietaires?: (number | undefined)[]
  /**
   * Tâche 5 (glisser-déposer, mode manuel) : le SECTEUR de chaque groupe,
   * même longueur que `groupes`, pour les emplacements qui mélangent
   * plusieurs secteurs différents dans un même emplacement (`terrain-combat`
   * pose côte à côte alliés, ennemis engagés et environnement). `data-zone`
   * ne descend qu'au niveau de l'emplacement entier ; un secteur nommé ici
   * permet de viser LE BON groupe au lâcher, sans confondre par exemple un
   * allié et un ennemi engagé — voir `CLE_PILE_ENGAGES`. Absent = aucun
   * secteur de cet emplacement n'a besoin d'être distingué.
   */
  groupesPiles?: (string | undefined)[]
  /**
   * Table par briques (05/10/2026) : la BRIQUE de chaque groupe, meme longueur
   * que `groupes`, pour les deux emplacements qui en melangent plusieurs
   * (`terrain-combat` : allies, sbires, environnement ; `terrain-soutien` :
   * heros, soutiens). C'est ce qui permet a la table de les separer ou de les
   * regrouper autrement (table-rendu.ts). Absent = une seule brique.
   */
  groupesBriques?: (CleBrique | undefined)[]
  /**
   * Seulement sur une zone ASSEMBLEE par la table (table-rendu.ts) : les
   * emplacements d'origine dont elle reprend des groupes. Le premier est
   * `cle` ; tous donnent leur classe CSS `zone-<cle>` a la zone.
   */
  emplacementsDOrigine?: CleEmplacement[]
  /** Idem : l'emplacement d'origine de chaque groupe, cible de depot de la carte lachee dessus. */
  groupesDOrigine?: CleEmplacement[]
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
   * Le siege qui REGARDE l'ecran, s'il differe de `playerId`.
   *
   * ⚠ AJOUTE LE 25/09/2026, demande de l'utilisateur : « nous toujours a
   * gauche, et les autres a la suite ». `playerId` reste le point de vue du
   * RENDU (visibilite des cartes, badges « autres joueurs » du multijoueur) :
   * en vue Auto, il suit le joueur dont c'est le tour (`joueurActif` dans
   * board.tsx), pas forcement le viewer local. Sans ce champ separe, la zone
   * « Heros et soutiens » du viewer se decalait a droite des qu'on suivait
   * quelqu'un d'autre. Absent (replay, etat enregistre...), on retombe sur
   * `playerId` : comportement inchange.
   */
  viewerId?: number
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
 *
 * ⚠ L'attachement se lit EN CHAINE, pas sur un seul etage. `su001b` Master
 * Planner glisse une carte face cachee sous `su012` Contingency Plan, qui est
 * elle-meme une amelioration posee sur l'identite : la carte glissee pend donc
 * a deux etages de la racine. En ne lisant que les attachements DIRECTS des
 * racines, on la faisait disparaitre de la table alors que le moteur l'avait
 * bien posee (rapport de bug du 09/09/2026). Le sous-arbre est aplati derriere
 * sa racine, porteur avant porte, pour que le rendu garde une liste plate.
 */
function enUnites(
  liste: WorldCard[],
  rendu: Rendu,
  options: {
    dansLaMain?: boolean
    proprietaire?: string
    collectionRessources?: string
    herosArt?: string
  } = {}
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
    herosArt: options.herosArt,
  }

  // `vus` n'est pas de la prudence gratuite : un etat corrompu ou deux cartes
  // s'attachent l'une a l'autre boucherait la boucle a l'infini et figerait le
  // plateau. On coupe au lieu de tourner.
  const vus = new Set<number>()
  const sousArbre = (id: number): WorldCard[] => {
    if (vus.has(id)) return []
    vus.add(id)
    return (attacheesPar.get(id) ?? []).flatMap((attachee) => [
      attachee,
      ...sousArbre(attachee.id),
    ])
  }

  const descendants = (id: number, vu = new Set<number>()): WorldCard[] => {
    if (vu.has(id)) return []
    vu.add(id)
    return (attacheesPar.get(id) ?? []).flatMap((fille) => [fille, ...descendants(fille.id, vu)])
  }

  const racines = liste.filter((carte) => carte.bind_object_id === 0 || !ids.has(carte.bind_object_id))
  return racines.flatMap((carte): UniteAffichee[] => {
    const pendantes = sousArbre(carte.id)
    const paire = options.dansLaMain ? undefined : trouverPaire(pendantes)
    if (!paire) {
      return [
        {
          cle: `carte-${carte.id}`,
          carte: toScanCard(carte, ctxCarte),
          attachees: pendantes.map((attachee) => toScanCard(attachee, ctxCarte)),
        },
      ]
    }
    // Paire jumelle : les deux cartes sortent de la cascade et se posent A COTE
    // du porteur (14 puis 15, quel que soit l'ordre d'arrivee). Ce qui pendait
    // sous elles les suit.
    const sortantes = new Set<number>()
    const retient = (racine: WorldCard) => {
      sortantes.add(racine.id)
      for (const fille of descendants(racine.id)) sortantes.add(fille.id)
    }
    retient(paire.gauche)
    retient(paire.droite)
    const unite = (jumelle: WorldCard, panorama: CotePanorama): UniteAffichee => ({
      cle: `carte-${jumelle.id}`,
      carte: toScanCard(jumelle, ctxCarte),
      attachees: descendants(jumelle.id).map((fille) => toScanCard(fille, ctxCarte)),
      panorama,
    })
    return [
      {
        cle: `carte-${carte.id}`,
        carte: toScanCard(carte, ctxCarte),
        attachees: pendantes.filter((a) => !sortantes.has(a.id)).map((a) => toScanCard(a, ctxCarte)),
      },
      unite(paire.gauche, 'gauche'),
      unite(paire.droite, 'droite'),
    ]
  })
}

/** Un groupe de cartes posees. Vide = pas de groupe. */
function posees(
  liste: readonly unknown[] | undefined,
  rendu: Rendu,
  options: {
    dansLaMain?: boolean
    proprietaire?: string
    collectionRessources?: string
    herosArt?: string
  } = {}
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
    /** Cette pile reste un encadre CIBLABLE meme sans carte dedans (mode
     *  manuel, 21/09/2026 puis correctif du 22/09/2026).
     *
     *  ⚠ PAR DEFAUT `false`, ET C'EST VOULU. La toute premiere version
     *  affichait un encadre vide pour TOUTE pile a 0 carte, sans distinction.
     *  Signale en jeu : un heros SANS deck special (Angel) affichait un
     *  encadre « Special deck » fantome, parce que `notre.additional_deck`
     *  vaut `[]` aussi bien pour « ce heros n'a pas ce mecanisme » que pour
     *  « son deck special est temporairement epuise » — le moteur ne
     *  distingue PAS les deux (le deck special n'est cree que par le script
     *  du heros lui-meme, `AbilityFactory.BeginGameWithSetAside`, jamais par
     *  un champ fixe). Impossible de deviner juste depuis le nombre de
     *  cartes : seules les DEUX piles que CHAQUE heros possede vraiment
     *  (son deck et sa defausse personnels) sont marquees `videAffichable`. */
    videAffichable?: boolean
  }>,
  rendu: Rendu
): UniteAffichee[] {
  return listes.flatMap((pile) => {
    const contenu = cartes(pile.cartes, rendu)
    const carte = toPileCard(contenu, rendu.ctx, pile.representant)
    const cleUnite = `${cle}-${pile.cle}`
    if (!carte) {
      if (!pile.videAffichable) return []
      return [{
        cle: cleUnite,
        carte: {
          id: `pile-vide-${cleUnite}`,
          name: pile.titre ?? pile.labelType ?? pile.cle,
          kind: 'unknown',
          imageUrl: '',
        },
        attachees: [],
        pile: cleUnite,
        pileVide: true,
      }]
    }
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
    // `pile` = `cle`, TOUJOURS : c'est ce qui rend chaque pile de cette
    // fonction désignable sans ambiguïté pour le glisser du mode manuel
    // (`board/manuel/glisser-manuel.ts`, `PILE_PAR_ZONE`) — le deck du héros
    // (`joueur-deck`) et le deck spécial (`soutien-deck`) partagent le même
    // `pile.cle` (« deck ») mais pas le même GROUPE (`cle`), donc pas la même
    // pile moteur. Un attribut qui aurait pris `pile.cle` seul les aurait
    // confondus et déplacé une carte dans la mauvaise pile en silence.
    const unite: UniteAffichee = { cle: cleUnite, carte, attachees: [], pile: cleUnite }
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
  if (!visible) {
    // Masquee : le clic dit d'ou viennent les cartes et combien il y en a,
    // sans jamais les montrer.
    unite.pileTitre = titre
    unite.pileGroupes = groupes.map((pile) => ({
      cle: pile.cle,
      titre: pile.titre,
      cartes: [],
      masque: { nombre: pile.contenu.length },
    }))
    unite.pileContenu = []
  }
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
/**
 * Le complot principal porte le nom de la manigance annexe a CRISE qui le
 * verrouille, s'il y en a une.
 *
 * Le moteur expose `info.crisis` sur la manigance annexe (has_crisis.py :
 * tant qu'elle est en jeu, aucune menace ne peut etre retiree du complot
 * principal). Rapport joueur du 11/09/2026 : Pour la Justice visait le complot
 * principal pendant que Collapsing Bridge etait en jeu, la carte partait sans
 * effet, et rien sur la table ne le disait. Le joueur a rejoue le meme coup
 * trois fois.
 */
function avecCrise(unites: UniteAffichee[], world: World): UniteAffichee[] {
  const annexes = Array.isArray(world.area_schemes_side) ? world.area_schemes_side : []
  const crise = annexes.find((carte) => Number(carte?.info?.crisis ?? 0) > 0)
  if (!crise) return unites
  for (const unite of unites) {
    unite.carte = { ...unite.carte, crise: String(crise.name ?? '') }
  }
  return unites
}

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
  // Le tri par nom se fait sur le nom du MOTEUR, jamais sur celui qui est
  // dessine : `UniteAffichee.carte.name` est traduit depuis le 11/09/2026
  // (voir noms-cartes-fr.ts) alors que `WorldCard.name` reste anglais. Les
  // comparer revenait a chercher « Le Bouffon Vert » parmi des « Green
  // Goblin » : plus aucune phase rattachee, tous les vilains « en attente ».
  // On relit donc les WorldCard actives, et on retrouve l'unite par son id.
  const cartesActives = cartes(world.area_villain, rendu)
  const nomMoteurParId = new Map(cartesActives.map((carte) => [String(carte.id), carte.name]))
  const nomsActifs = new Set(cartesActives.map((carte) => carte.name))
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
      const cible = actifs.find((u) => nomMoteurParId.get(u.carte.id) === nom) ?? actifs[0]
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
  proprietaires?: (number | undefined)[],
  // Secteur de chaque groupe (tache 5, glisser-depose) : meme longueur et
  // meme ordre que `groupes`. Seul terrain-combat le fournit pour l'instant
  // (voir EmplacementAffiche.groupesPiles).
  groupesPiles?: (string | undefined)[],
  // Brique de chaque groupe (EmplacementAffiche.groupesBriques).
  groupesBriques?: (CleBrique | undefined)[]
): EmplacementAffiche | undefined {
  // Les groupes vides sont retires ; on filtre proprietaires et secteurs du
  // meme geste, pour que les trois tableaux restent alignes apres coup.
  const gardes = groupes
    .map((groupe, index) => ({
      groupe,
      proprietaire: proprietaires?.[index],
      pile: groupesPiles?.[index],
      brique: groupesBriques?.[index],
    }))
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
    ...(proprietaires ? { proprietaires: gardes.map((garde) => garde.proprietaire) } : {}),
    ...(groupesPiles ? { groupesPiles: gardes.map((garde) => garde.pile) } : {}),
    ...(groupesBriques ? { groupesBriques: gardes.map((garde) => garde.brique) } : {}),
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
  // Heros proprietaire d'une zone : art par defaut des cartes de deck (TMNT).
  const herosDe = (joueur: WorldPlayer | undefined): string | undefined =>
    joueur?.area_hero?.[0]?.card_id
  const notreHeros = herosDe(notre)
  const renduNotre: Rendu = { ...rendu, ctx: { ...rendu.ctx, herosArt: notreHeros } }

  /**
   * Ce que le SCENARIO resout, c'est-a-dire la liste du monde moins ce qui
   * appartient deja a un joueur.
   *
   * ⚠ Le moteur publie encore la liste fusionnee dans `world.area_processing`
   * (la sienne PLUS celle de chaque joueur) pour ne pas casser l'ancien
   * client. Un moteur anterieur au 15/09/2026 ne publie pas du tout
   * `player.area_processing` : l'ensemble est alors vide, rien n'est retire,
   * et le plateau se comporte comme avant.
   */
  const idsEnResolutionChezUnJoueur = new Set(
    joueurs.flatMap((joueur) => (joueur.area_processing ?? []).map((carte) => carte.id))
  )
  const resolutionDuScenario = (world.area_processing ?? []).filter(
    (carte) => !idsEnResolutionChezUnJoueur.has(carte.id)
  )

  // Deck special consultable SEULEMENT si la regle l'autorise, ce que le moteur
  // encode par la visibilite : on ne l'ouvre que si ses cartes nous sont visibles
  // (sinon on n'a pas le droit de regarder dedans, comme un deck ordinaire).
  const cartesDeckSpecial = (notre?.additional_deck ?? []).filter(estUneCarte)
  const deckSpecialConsultable =
    cartesDeckSpecial.length > 0 &&
    cartesDeckSpecial.every((carte) => isVisibleFor(carte, options.playerId))
  // METEO (Storm, 01/10/2026) : la carte Weather EN JEU appartient a la case
  // Weather, pas aux soutiens, et les cartes NON UTILISEES du deck se rangent
  // SOUS elle (« les cartes climat non utilisees doivent aller sous celle qui
  // est en cours d'utilisation »). Limite volontairement au trait Weather : les
  // autres decks speciaux gardent leur disposition.
  const estMeteo = (carte: unknown): boolean =>
    estUneCarte(carte) && Boolean((carte.traits ?? {})[TRAIT_METEO])
  const meteoEnJeu = (notre?.supports ?? []).filter(estMeteo)
  const soutiensHorsMeteo = (notre?.supports ?? []).filter((carte) => !estMeteo(carte))
  const deckEstMeteo = cartesDeckSpecial.some(estMeteo)

  // Nom du deck special (ex. « Invocation »), pour son etiquette et sa zone.
  const nomSpecial =
    nomDeckSpecial(notre?.additional_deck) ??
    nomDeckSpecial(notre?.additional_discard_pile) ??
    nomDeckSpecial(meteoEnJeu) ??
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
      // ⚠ SEULEMENT CE QUE LE SCENARIO RESOUT. Le moteur publie encore la
      // liste FUSIONNEE (la sienne plus celle de chaque joueur) dans
      // `world.area_processing`, pour ne pas casser l'ancien client qui la
      // lit. Sans ce retrait, une carte jouee par un heros serait dessinee
      // DEUX fois : aupres de lui, et ici. Defaut signale en jeu le
      // 15/09/2026 : « les cartes que je joue se placent derriere le
      // mechant ».
      posees(resolutionDuScenario, rendu),
      posees(world.area_boost, rendu),
      posees(notre?.dealt_encounter_cards, rendu),
    ]),

    // Le complot actif (area_schemes_main), avec ses etapes A VENIR
    // (main_schemes_deck) empilees derriere et consultables au bouton.
    emplacement('complot-principal', t('Manigance principale'), [
      avecCrise(
        avecStages(
          posees(world.area_schemes_main, rendu),
          world.main_schemes_deck,
          'Scheme stages',
          rendu
        ),
        world
      ),
    ]),

    emplacement('complots-secondaires', t('Manigances annexes'), [
      posees(world.area_schemes_side, rendu),
    ]),

    // Rangee HAUTE de l'aire joueur : la ligne de combat (adjacente a la menace).
    // Allies, sbires engages ET environnement : tout ce qui "vit" sur le terrain.
    emplacement(
      'terrain-combat',
      t('Alliés, sbires et environnement'),
      [
        posees(notre?.allies, rendu, { proprietaire: nomHero(notre), herosArt: notreHeros }),
        posees(notre?.engaged_enemies, rendu, { proprietaire: nomHero(notre) }),
        // En multijoueur, les autres joueurs partagent l'aire : leur ligne de combat.
        ...autres.flatMap((joueur) => [
          posees(joueur.allies, rendu, { proprietaire: nomHero(joueur), herosArt: herosDe(joueur) }),
          posees(joueur.engaged_enemies, rendu, { proprietaire: nomHero(joueur) }),
        ]),
        // ⚠ TOUJOURS EN DERNIER (25/09/2026, demande de l'utilisateur :
        // l'environnement, ni allie ni sbire, doit rester du cote DROIT de
        // la zone, apres tout le monde — pas seulement apres NOTRE ligne de
        // combat, sinon un autre joueur s'intercalerait entre les deux en
        // multijoueur.
        posees(world.area_environment, rendu),
        posees(notre?.environment_area, rendu),
      ],
      // Lot 5 du 06/10/2026 (question 6) : le siege de chaque groupe, pour
      // poser une carte chez le joueur du groupe vise. L'environnement n'est a
      // personne.
      [
        options.playerId,
        options.playerId,
        ...autres.flatMap((joueur) => [joueurs.indexOf(joueur), joueurs.indexOf(joueur)]),
        undefined,
        undefined,
      ],
      // Tache 5 (glisser-depose) : seuls LES ENNEMIS ENGAGES DE NOTRE joueur
      // portent un secteur (`CLE_PILE_ENGAGES`) : lacher un sbire dessus
      // l'engage. Depuis le lot 2 du 06/10/2026, par
      // `Puzzle.MoveTo(..., 'EngagedEnemiesArea', siege=<le heros affiche>)` :
      // sans siege, une pile de joueur visait le premier joueur DU MOMENT, un
      // ordre qui tourne a chaque round. Le groupe d'un AUTRE joueur reste
      // sans secteur jusqu'au lot 5 (chez qui va une carte posee).
      [undefined, CLE_PILE_ENGAGES, ...autres.flatMap(() => [undefined, undefined]), undefined, undefined],
      ['allies', 'sbires', ...autres.flatMap((): CleBrique[] => ['allies', 'sbires']), 'environnements', 'environnements']
    ),

    // Rangee CENTRALE de l'aire joueur : d'abord le DECK SPECIAL du heros s'il en
    // a un (Invocation de Strange, Daredevil...), pose a GAUCHE du heros ; puis le
    // HEROS, puis ce qui gravite autour (soutiens, permanents, obligations).
    // Le DECK SPECIAL du heros (Invocation...) a sa PROPRE zone, a gauche : deck +
    // sa defausse cote a cote. Le heros et ses soutiens sont decales a sa droite.
    emplacement('deck-special', nomSpecial, [
      // La meteo EN JEU, avec le reste de son deck glisse DERRIERE elle comme
      // une pile d'ameliorations (voir `meteoEnJeu`).
      posees(meteoEnJeu, rendu).map((unite, index) =>
        index === 0 && deckEstMeteo
          ? {
              ...unite,
              attachees: [
                ...unite.attachees,
                ...cartes(notre?.additional_deck, rendu).map((carte) => toScanCard(carte, rendu.ctx)),
              ],
            }
          : unite
      ),
      piles(
        'soutien',
        [
          {
            cle: 'deck',
            // Sous la meteo en jeu quand il y en a une : pas deux fois a l'ecran.
            cartes: deckEstMeteo && meteoEnJeu.length > 0 ? undefined : notre?.additional_deck,
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
        herosArt: notreHeros,
      }),
    ]),

    // AJOUT (pack wave) : la Rising Tide area, meme case que 'deck-special' /
    // 'reserve' juste au-dessus. MEME PRINCIPE (Board.tsx exclut ces trois
    // clés de la case commune) : aucun heros n'a deux de ces zones a la fois,
    // l'emplacement vide disparait tout seul.
    //
    // ⚠ PAS `dansLaMain: true`, a la difference de la Reserve : la Reserve
    // porte `is_like_in_hand` (ses cartes sont visibles au proprietaire comme
    // si elles etaient en main), la Rising Tide area NON -- l'insert du pack
    // est explicite (« an area, rather than a deck »). Une carte face cachee
    // que le moteur rendrait visible doit donc garder l'encadre en
    // pointilles (`peeking`, card-model.ts) au lieu d'etre traitee comme une
    // carte de main ordinaire.
    emplacement('rising-tide', t('Ta marée montante'), [
      posees(notre?.rising_tide, rendu, {
        collectionRessources: notreCollection,
        herosArt: notreHeros,
      }),
    ]),

    // Chaque groupe est appairee a son proprietaire au moment ou elle est
    // construite (pas dans un tableau separe recompte a la main) : si un jour
    // un joueur gagne ou perd un groupe ici, le proprietaire suit sans qu'on
    // ait besoin de resynchroniser deux listes.
    ((): EmplacementAffiche | undefined => {
      const groupesEtProprietaires: Array<[UniteAffichee[], number, CleBrique]> = [
        [posees(notre?.area_hero, rendu, { herosArt: notreHeros }), options.playerId, 'heros'],
        [posees(soutiensHorsMeteo, rendu, { herosArt: notreHeros }), options.playerId, 'soutiens'],
        [posees(notre?.obligations_area, rendu), options.playerId, 'soutiens'],
        // La carte en cours de resolution se pose aupres de SON heros, le
        // temps que son texte s'applique : c'est ce qu'on fait sur une vraie
        // table, et non chez le mechant.
        [posees(notre?.area_processing, rendu, { herosArt: notreHeros }), options.playerId, 'soutiens'],
        ...autres.flatMap((joueur, index): Array<[UniteAffichee[], number, CleBrique]> => {
          const idJoueur = joueurs.indexOf(joueur)
          return [
            [
              piles(`soutien-autre-${index}`, [
                { cle: 'deck-special', cartes: joueur.additional_deck },
              ], rendu),
              idJoueur,
              'heros',
            ],
            [posees(joueur.area_hero, rendu, { herosArt: herosDe(joueur) }), idJoueur, 'heros'],
            [posees(joueur.supports, rendu, { herosArt: herosDe(joueur) }), idJoueur, 'soutiens'],
            [posees(joueur.area_processing, rendu, { herosArt: herosDe(joueur) }), idJoueur, 'soutiens'],
          ]
        }),
      ]
      // Le viewer local TOUJOURS EN TETE (25/09/2026), meme quand la vue Auto
      // suit un autre joueur (`options.playerId` devient alors son siege, et
      // ses groupes passeraient sinon devant ceux du viewer). Simple
      // partition stable : ordre inchange dans chaque moitie, donc AUCUN
      // effet quand le viewer suit son propre tour (cas le plus courant).
      const idViewer = options.viewerId ?? options.playerId
      const ordonnes = [
        ...groupesEtProprietaires.filter(([, idJoueur]) => idJoueur === idViewer),
        ...groupesEtProprietaires.filter(([, idJoueur]) => idJoueur !== idViewer),
      ]
      return emplacement(
        'terrain-soutien',
        t('Héros et soutiens'),
        ordonnes.map(([groupe]) => groupe),
        ordonnes.map(([, idJoueur]) => idJoueur),
        undefined,
        ordonnes.map(([, , brique]) => brique)
      )
    })(),

    // « Your piles » : UNIQUEMENT le deck et la defausse du joueur, cote a cote.
    emplacement('piles-joueur', t('Deck du héros'), [
      piles(
        'joueur',
        [
          { cle: 'deck', cartes: notre?.player_deck, videAffichable: true },
          {
            cle: 'defausse',
            cartes: notre?.player_discard_pile,
            regardable: true,
            titre: t('Pile de défausse'),
            videAffichable: true,
          },
        ],
        renduNotre
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
      // LE SET NEMESIS EST DANS LA PILE « CARTES VISIBLES » (06/10/2026).
      //
      // Il a d'abord rejoint cette zone (14/09/2026) : cette zone ne montre
      // JAMAIS une carte en jeu (des qu'une carte nemesis entre en jeu, elle part
      // chez le mechant, les sbires ou les manigances annexes ; il ne reste ici
      // que `set_aside_nemesis_sets`). Il restait une pile a part ; l'utilisateur
      // veut DEUX piles seulement, ouverte et masquee. Il est CONNU du joueur
      // (imprime dans le pack du heros) : pile ouverte, groupe « Set némésis ».
      // ⚠ Il est PERSONNEL (`notre`), le reste de la pile est commun : en
      // multijoueur il suit le heros AFFICHE.
      // Consequence assumee : il n'est plus une cible de depot du mode manuel
      // (`annexes-nemesis` n'existe plus), comme les autres piles fondues.
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
          { cle: 'nemesis', cartes: notre?.set_aside_nemesis_sets, titre: t('Set némésis') },
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


    emplacement('main', t('Ta main'), [
      posees(notre?.hand_cards, rendu, {
        dansLaMain: true,
        collectionRessources: notreCollection,
        herosArt: notreHeros,
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
