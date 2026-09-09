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
import { estActivation, estResolue } from './deroule-phase'
import { libelleDeStatut } from './deroule-textes'
import type { EntreeHistorique } from './HistoriquePartie'
import { t } from './langue'
import type { ScanCardProps } from '../components/ScanCard'
import {
  PHASES_DU_MECHANT,
  PHASES_DU_MECHANT_ORDONNEES,
  type PhaseDuMechant,
} from './moteur'
import type { FaitMechant, World, WorldCard } from './world'

/**
 * Les étapes de la phase du méchant, dans l'ordre de la carte de référence.
 *
 * Les phases NE SONT PLUS RECOPIÉES ICI : elles viennent de
 * `PHASES_DU_MECHANT_ORDONNEES` (moteur.ts), l'unique définition côté plateau.
 * Ce fichier en avait sa propre copie, et l'audit F6 du 06/09/2026 comptait
 * trois listes concurrentes pour une seule notion. Ce tableau ne dit plus que
 * ce qui lui appartient : le NUMÉRO et le TITRE de chaque étape.
 *
 * Le point 5 de la carte (« passer le jeton de premier joueur ») ne produit
 * aucun fait à raconter : il n'a pas d'étape, d'où l'absence d'une cinquième
 * phase dans la liste unique.
 */
const TITRES_ETAPES: Record<PhaseDuMechant, string> = {
  'Main Scheme Place Threat': 'Menace sur la manigance',
  'Enemy Activation': 'Activations',
  'Deal Encounter Cards': 'Cartes distribuées',
  'Reveal Encounter Cards': 'Cartes révélées',
}

const ETAPES = PHASES_DU_MECHANT_ORDONNEES.map((phase, rang) => ({
  phase,
  numero: rang + 1,
  titre: TITRES_ETAPES[phase],
}))

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
  genre: 'menace' | 'attaque' | 'manigance' | 'carte' | 'statut'
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
const PHASE_PAR_GENRE: Record<FaitMechant['genre'], PhaseDuMechant> = {
  menace: 'Main Scheme Place Threat',
  attaque: 'Enemy Activation',
  manigance: 'Enemy Activation',
  distribution: 'Deal Encounter Cards',
  revelation: 'Reveal Encounter Cards',
  // Un statut se pose au milieu d'autre chose : le repli le range aux
  // activations, comme les attaques, et sa phase reelle (que le fait porte)
  // le remet a sa place des qu'elle est connue.
  statut: 'Enemy Activation',
}

function faitsDeLEtape(faits: FaitMechant[], phase: string): FaitMechant[] {
  return faits.filter((fait) => {
    // Les activations RÉSOLUES seulement. Depuis la tâche A3, une activation
    // s'annonce avant de se résoudre : ce récap est un bilan d'APRÈS-phase, il
    // ne raconte que ce qui a eu lieu. Une intention y aurait paru comme un
    // coup à zéro dégât, et une activation annulée aurait compté pour un coup
    // qui n'a jamais été porté. (Un fait sans `etat` est une résolution :
    // c'est tout ce que le moteur savait produire avant les deux temps.)
    if (estActivation(fait) && !estResolue(fait)) return false
    return (fait.phase ?? PHASE_PAR_GENRE[fait.genre]) === phase
  })
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
 * La phase telle que le MOTEUR l'a enregistrée, genre par genre.
 *
 * C'est la seule source qui connaisse la composition d'un coup : la comparaison
 * de photos voit « 5 dégâts » mais ne saura jamais que c'était 3 d'attaque et
 * 2 de boost, et elle recompte ce que le moteur rend plusieurs fois autour
 * d'une même résolution. Elle est aussi la seule à survivre à un rechargement
 * de page. Quand elle est là, elle remplace la déduction — elle ne la complète
 * pas, sinon chaque fait paraîtrait deux fois.
 *
 * Les quatre genres y sont, comme dans le cartouche du déroulé
 * (`etapesDeroule`, deroule-phase.ts) : la menace du point 1, les activations
 * du point 2, la distribution du point 3, les révélations du point 4. Le récap
 * n'en lisait que les activations et déduisait le reste du journal — deux
 * sources pour une seule phase, que l'audit F6 du 06/09/2026 reprochait.
 */
function lignesDuMoteur(faits: FaitMechant[], noms: Noms): Ligne[] {
  return faits.map((fait, index): Ligne => {
    if (fait.genre === 'menace') {
      return {
        cle: `moteur:${index}:menace:${fait.cible_id}`,
        genre: 'menace',
        // Le nom que porte la table AUJOURD'HUI quand elle le connaît encore :
        // une manigance qui a changé de stade a changé de nom, et le fait garde
        // celui qu'elle avait. Repli sur le nom du fait, qui ne s'efface pas.
        titre: noms.carte(fait.cible_id) ?? fait.cible,
        cibleId: fait.cible_id,
        valeur: fait.montant,
        restant: fait.restant ?? undefined,
        // Le seuil du fait d'abord : c'est celui du moment de la pose. La carte
        // ne sert que de repli, pour un moteur qui ne l'inscrivait pas encore.
        plafond: fait.plafond ?? noms.plafond(fait.cible_id),
      }
    }

    if (fait.genre === 'distribution') {
      return {
        cle: `moteur:${index}:distribution:${fait.joueur ?? 'x'}`,
        genre: 'carte',
        // La carte est FACE CACHÉE : on ne nomme que le héros qui la reçoit.
        // Même formule que le cartouche (deroule-textes.ts, `titreEtape`).
        titre: t('Carte rencontre distribuée'),
        heros: fait.joueur_nom ?? noms.heros(fait.joueur ?? undefined),
      }
    }

    if (fait.genre === 'revelation') {
      return {
        cle: `moteur:${index}:revelation:${fait.carte_id}`,
        genre: 'carte',
        titre: fait.carte,
        heros: fait.joueur_nom ?? noms.heros(fait.joueur ?? undefined),
        cibleId: fait.carte_id,
      }
    }

    // Reste les activations. Une intention n'arrive jamais jusqu'ici
    // (`faitsDeLEtape` ne garde que les résolutions), mais le type ne le sait
    // pas : le repli garde la forme d'une ligne juste plutôt que de mentir.
    // Une carte de STATUT posee pendant la phase. Sans `valeur`, elle ne
    // fusionne jamais avec une autre ligne (voir `empiler`) : sonne PUIS
    // robuste sur la meme cible font bien deux lignes.
    if (fait.genre === 'statut') {
      return {
        cle: `moteur:${index}:statut:${fait.cible_id}:${fait.statut}`,
        genre: 'statut',
        titre: `${noms.carte(fait.cible_id) ?? fait.cible} ${t('gagne')} ${libelleDeStatut(fait.statut)}`,
        cibleId: fait.cible_id,
        cause: fait.cause || undefined,
      }
    }

    if (!estResolue(fait)) {
      return {
        cle: `moteur:${index}:annonce:${fait.auteur_id}:${fait.cible_id}`,
        genre: fait.genre === 'attaque' ? 'attaque' : 'manigance',
        titre: `${fait.auteur} ${fait.genre === 'attaque' ? t('attaque') : t('manigance sur')} ${fait.cible}`,
        cibleId: fait.cible_id,
        acteur: fait.auteur,
      }
    }

    return {
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
    }
  })
}

function etapeDe(
  entrees: EntreeHistorique[],
  definition: (typeof ETAPES)[number],
  noms: Noms,
  faitsMoteur: FaitMechant[]
): Etape | undefined {
  const brut = entrees.filter((e) => e.phase === definition.phase && e.type !== 'phase')
  const duMoteur = faitsDeLEtape(faitsMoteur, definition.phase)
  // Une étape n'existe que si QUELQUE CHOSE s'y est passé. Les faits du moteur
  // suffisent : le journal local ne couvre pas la distribution (les cartes
  // partent face cachée, aucune photo ne change), et l'étape 3 restait donc
  // barrée en toutes circonstances (constat M3 de l'audit du 06/09/2026).
  if (brut.length === 0 && duMoteur.length === 0) return undefined

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

  // UNE SEULE SOURCE, LES FAITS DU MOTEUR, avec un REPLI PAR GENRE.
  //
  // Le moteur enregistre les quatre points de la carte de référence. Le récap
  // en lisait les activations et déduisait tout le reste du journal local :
  // deux sources pour une seule phase, avec deux durées de vie (le journal ne
  // survit pas à un rechargement). Il lit désormais comme le cartouche.
  //
  // Le repli est le même que celui d'`etapesDeroule` : un genre ABSENT des
  // faits de l'étape se relit dans le journal, pour ce genre-là seulement.
  // C'est ce qui garde un bilan lisible face à un moteur pas encore à jour ou
  // à une sauvegarde plus ancienne, sans jamais compter deux fois un fait que
  // les deux sources connaissent.
  const deduites = lignesDeLEtape(faits, noms)
  const lignesMoteur = lignesDuMoteur(duMoteur, noms)

  const aDuMoteur = (genre: Ligne['genre']) => lignesMoteur.some((l) => l.genre === genre)
  const activationsMoteur = duMoteur.some(estActivation)
  const cartesMoteur = duMoteur.some(
    (f) => f.genre === 'distribution' || f.genre === 'revelation'
  )
  const deduitesDeGenre = (garder: (genre: Ligne['genre']) => boolean) =>
    deduites.filter((l) => garder(l.genre))

  // Les CARTES d'abord, parce que les activations qu'elles déclenchent se
  // rangent dessous (`rattacherAuxCauses`). Une carte venue des faits ne porte
  // pas les `effets` que le journal collait sous elle : ils sont repris de la
  // ligne déduite de la même carte, la seule à les connaître. Ce n'est pas une
  // seconde source du FAIT, c'est le même détail que le déroulé brut déjà
  // consultable sous le repli.
  const effetsDeduits = new Map<number | undefined, string[] | undefined>(
    deduites.filter((l) => l.genre === 'carte').map((l) => [l.cibleId, l.effets])
  )
  const lignesCarte = cartesMoteur
    ? lignesMoteur
        .filter((l) => l.genre === 'carte')
        .map((l) => ({ ...l, effets: activationsMoteur ? undefined : effetsDeduits.get(l.cibleId) }))
    : deduitesDeGenre((genre) => genre === 'carte').map((l) =>
        activationsMoteur ? { ...l, effets: undefined } : l
      )
  const activations = activationsMoteur
    ? lignesMoteur.filter((l) => l.genre === 'attaque' || l.genre === 'manigance')
    : deduitesDeGenre((genre) => genre === 'attaque' || genre === 'manigance')
  const menaces = aDuMoteur('menace')
    ? lignesMoteur.filter((l) => l.genre === 'menace')
    : deduitesDeGenre((genre) => genre === 'menace')

  // Rien du moteur du tout : on garde la liste déduite TELLE QUELLE, ordre
  // compris. La recomposition par genre ci-dessous mélangerait sinon l'ordre du
  // journal, qui est celui du jeu.
  const rienDuMoteur = lignesMoteur.length === 0
  const lignes = rienDuMoteur
    ? deduites
    : [...menaces, ...rattacherAuxCauses(lignesCarte, activations)]

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
  const dedans = entrees.filter((e) => e.round === round && PHASES_DU_MECHANT.has(e.phase))
  // Ordre du jeu : l'historique empile les plus récentes en tête.
  const ordonnees = [...dedans].reverse()
  // Le MÊME filtre que sur les entrées, et le même que celui d'`etapesDeroule`
  // (deroule-phase.ts) : sans lui, un fait du round précédent reparaîtrait dans
  // le bilan du suivant. Un fait sans `round_id` (moteur ou sauvegarde
  // antérieurs à ce champ) est gardé quel que soit le round demandé.
  const faitsDuRound = faitsMoteur.filter(
    (f) => f.round_id === undefined || f.round_id === round
  )
  const etapes = ETAPES.map((definition) =>
    etapeDe(ordonnees, definition, noms, faitsDuRound)
  ).filter((e): e is Etape => e !== undefined)
  if (etapes.length === 0) return undefined
  return { cle: `${round}`, round, etapes }
}

export function RecapPhaseMechant({
  entrees,
  monde,
  actif,
  phaseMechantEnCours,
  cartesMonde,
  catalogue,
  playerId,
}: {
  entrees: EntreeHistorique[]
  monde: World | undefined
  actif: boolean
  /**
   * Le moteur est-il encore dans une des quatre phases du méchant ?
   *
   * C'est board.tsx qui la calcule, sur `PHASES_DU_MECHANT` (moteur.ts),
   * L'UNIQUE définition côté plateau, et le cartouche du déroulé la reçoit
   * déjà. Ce panneau la comparait de son côté, sur sa propre photo de
   * `monde.phase` : deux façons de savoir qu'une phase est finie, pour une
   * seule notion (constat F6 de l'audit du 06/09/2026).
   *
   * Absente (montage plus ancien, test) : on retombe sur `monde.phase`, lue
   * avec la même définition unique.
   */
  phaseMechantEnCours?: boolean
  /** Les cartes du monde par object id, pour retrouver celle d'une ligne. */
  cartesMonde?: Map<number, WorldCard>
  catalogue?: Catalogue
  playerId?: number
}) {
  const [bilan, setBilan] = useState<Bilan | undefined>(undefined)
  const [depliees, setDepliees] = useState<Set<number>>(() => new Set())
  // Le OUI/NON du rendu precedent, pour ne declencher qu'a la SORTIE de la
  // phase. Il ne compare plus deux photos du monde : il suit le meme booleen
  // que le cartouche.
  const dansLaPhaseAvant = useRef<boolean | undefined>(undefined)
  // Le round de la phase RACONTEE. Le moteur quitte la phase du mechant et
  // incremente le round dans la meme foulee : lire `monde.round_id` a la sortie
  // rend parfois le round SUIVANT, et le bilan ne trouve alors ni entree ni
  // fait (meme piege que dans DeroulePhase.tsx). On retient donc le round vu
  // PENDANT la phase.
  const roundDeLaPhase = useRef<number | undefined>(undefined)

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

  // Une seule definition de « la phase du mechant » : celle que board.tsx
  // calcule sur `PHASES_DU_MECHANT` et passe en prop. Le repli sur
  // `monde.phase` consomme la MEME liste, il n'en invente pas une seconde.
  const dedans =
    phaseMechantEnCours ?? (monde?.phase !== undefined && PHASES_DU_MECHANT.has(monde.phase))
  if (dedans && monde?.round_id !== undefined) roundDeLaPhase.current = monde.round_id

  useEffect(() => {
    const avant = dansLaPhaseAvant.current
    dansLaPhaseAvant.current = dedans

    if (!actif || monde?.phase === undefined || avant === undefined) return
    // On ne déclenche qu'à la SORTIE de la phase du méchant.
    if (!avant || dedans) return
    setDepliees(new Set())
    setBilan(
      bilanDeLaPhase(
        entrees,
        roundDeLaPhase.current ?? monde?.round_id ?? 0,
        nomsRef.current,
        monde?.faits_mechant ?? []
      )
    )
  }, [dedans, monde?.phase, monde?.round_id, monde?.faits_mechant, actif, entrees])

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

  // `actif` autant que le bilan : un recap CONSTITUE en Instantane survivait
  // au passage en Detaille (le bilan reste en etat, et `actif` n'etait lu que
  // par le detecteur de transition qui le fabrique). Le joueur voyait alors
  // les deux bilans, celui-la meme qu'A5 a supprime.
  if (!bilan || !actif) return null

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
