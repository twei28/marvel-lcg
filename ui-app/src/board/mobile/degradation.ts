// Le plancher du modele de condensation : que faire quand la fenetre n'a MEME
// PAS la place de dessiner une pastille « +N » par bande.
//
// condenser() sait replier des tuiles, mais il ne sait pas disparaitre : une
// bande non vide rend toujours au moins la pastille « +N » (64 px, le plancher
// de lisibilite), plus le cout fixe de sa boite. Six bandes exigent donc un
// minimum incompressible. En dessous, la grille CSS comprimait les rangees et
// l'overflow:hidden de .bande-tuiles coupait EN SILENCE : c'est le bug que ce
// module supprime.
//
// La regle, decidee avec l'utilisateur : degrader EXPLICITEMENT. Sous la
// hauteur requise, les bandes les moins urgentes tombent a une ligne de resume
// touchable (titre + chiffres cles, plus aucune tuile), pour que les bandes
// vitales gardent les leurs. Rien n'est jamais coupe en silence.
//
// Tout ce fichier est pur : il ne touche ni au DOM ni a React, et c'est
// exactement la partie testable de la promesse.

import type { CleBande } from './bandes'
import { TUILE_PLANCHER } from './condensation'
import type { UniteAffichee } from '../zones'

export type ModeBande = 'tuiles' | 'resume'

/**
 * Les hauteurs REELLES de la boite d'une bande, relevees sur le DOM (voir la
 * sonde de PlateauMobile). Aucune de ces valeurs n'est devinee : elles sortent
 * de getComputedStyle sur une vraie .bande et du rectangle d'un vrai
 * .bande-titre.
 */
export type MesuresBande = {
  /** Hauteur du bouton .bande-titre. */
  titre: number
  /** Padding vertical de .bande (haut + bas). */
  remplissage: number
  /** Bordures horizontales de .bande (haut + bas). */
  bordure: number
  /** row-gap de .bande : il separe le titre des tuiles. */
  ecart: number
}

/**
 * Valeurs de repli, utilisees UNIQUEMENT avant la premiere mesure (et sous
 * jsdom, qui ne fait aucune mise en page). Elles recopient mobile.css :
 * .bande-titre min-height 44, .bande padding 6px*2, border-bottom 1px,
 * gap 4px. Des que la sonde a mesure, ce sont ses valeurs qui servent.
 */
export const MESURES_PAR_DEFAUT: MesuresBande = {
  titre: 44,
  remplissage: 12,
  bordure: 1,
  ecart: 4,
}

/** Cout vertical d'une bande reduite a sa ligne de resume : le titre et la bordure. */
export function coutResume(mesures: MesuresBande): number {
  return mesures.titre + mesures.bordure
}

/**
 * Cout vertical d'une bande qui garde ses tuiles, HORS tuiles : le titre, le
 * padding, la bordure et l'ecart de grille qui separe le titre des tuiles.
 */
export function coutFixeTuiles(mesures: MesuresBande): number {
  return mesures.titre + mesures.remplissage + mesures.bordure + mesures.ecart
}

/**
 * Ordre dans lequel les bandes PERDENT leurs tuiles, la premiere d'abord.
 *
 * Le critere n'est pas « ce qui est joli », c'est ce qu'une ligne de resume
 * fait PERDRE. Une ligne de resume donne le titre, le nombre de cartes et
 * jusqu'a trois chiffres, et un appui ouvre la bande en focus : ce qui se
 * resume bien en chiffres se degrade bien.
 *
 *  1. rencontre : deck et defausse. Leur contenu EST un nombre, la ligne de
 *     resume le dit aussi bien que la tuile. Rien ne s'y joue directement.
 *  2. complots : la menace posee est toute l'information, et elle tient en
 *     « 7/12 ». On agit dessus rarement et jamais dans l'urgence d'un tour.
 *  3. vilain : une SEULE entite, deux chiffres (PV, menace). La ligne de
 *     resume les porte en entier ; il reste un appui pour l'attaquer.
 *  4. terrain : plusieurs sbires, chacun avec ses PV et son etat. La perte
 *     grandit avec leur nombre, un compte ne les remplace pas.
 *  5. main : les cartes que tu peux jouer CE tour. Elles sont heterogenes,
 *     aucun chiffre ne dit ce qu'elles font.
 *  6. heros : ton aire de jeu (identite, allies, ameliorations, soutiens).
 *     C'est de la que part chaque action, et son etat (epuise, blesse,
 *     resistant) n'est pas resumable. Elle n'est jamais degradee la premiere
 *     et, en pratique, jamais degradee tout court.
 */
export const ORDRE_DEGRADATION: CleBande[] = [
  'rencontre',
  'complots',
  'vilain',
  'terrain',
  'main',
  'heros',
]

export type ExigenceBande = {
  cle: CleBande
  /**
   * Poids RELATIF pour le partage de la hauteur qui reste une fois tous les
   * planchers servis. Mettre 0 pour une bande sans aucune unite.
   */
  poids: number
  /**
   * Hauteur MINIMALE de tuiles sous laquelle la bande coupe. Vaut le plancher
   * de lisibilite (la pastille « +N » fait TUILE_PLANCHER.hauteur), augmente
   * de ce que la bande empile en plus des tuiles (les bandeaux joueurs replies
   * de la bande Heros). Vaut 0 pour une bande sans aucune unite.
   */
  plancher: number
}

export type PlanBandes = {
  modes: Map<CleBande, ModeBande>
  /** Hauteur accordee aux TUILES, pour les bandes restees en mode tuiles. */
  hauteurs: Map<CleBande, number>
  /**
   * 2 quand meme les lignes de resume ne tiennent pas les unes sous les
   * autres : elles passent alors sur deux colonnes. Cas extreme (paysage tres
   * bas) ; sinon toujours 1.
   */
  colonnes: 1 | 2
  /**
   * Vrai quand MEME les lignes de resume sur deux colonnes ne tiennent pas :
   * six bandes en deux colonnes demandent 3 * 45 = 135 px, et rien n'existait
   * en dessous. La rangee du bas etait alors rognee par l'overflow:hidden de
   * .pm-bandes, sans aucune route vers elle : le meme perte silencieuse que ce
   * module supprime partout ailleurs, un cran plus bas.
   *
   * Le comportement defini, a ce plancher-la : la vue d'etat DEFILE. C'est une
   * exception assumee au « le niveau 1 ne defile jamais », et elle ne
   * l'affaiblit pas : cette regle existe pour que la condensation soit le
   * mecanisme plutot qu'une barre de defilement, or ici il ne reste RIEN a
   * condenser (toutes les bandes sont deja reduites a une ligne, sur deux
   * colonnes). Le choix n'est plus « defiler ou condenser » mais « defiler ou
   * perdre des bandes ». Sous ~135 px de zone de bandes, aucune mise en page
   * ne rend six lignes de 44 px lisibles ; le defilement garde au moins toutes
   * les bandes ATTEIGNABLES, et un appui ouvre toujours la feuille de focus.
   */
  defilement: boolean
}

/** Le plancher de tuiles d'une bande non vide : la pastille « +N » et rien de moins. */
export function plancherTuiles(supplement = 0): number {
  return TUILE_PLANCHER.hauteur + supplement
}

/**
 * Decide, pour la hauteur reellement disponible, quelles bandes gardent leurs
 * tuiles et combien de hauteur chacune recoit.
 *
 * INVARIANT tenu par cette fonction : la somme de ce qui sera rendu
 * (coutFixeTuiles + hauteur pour une bande en tuiles, coutResume par rangee de
 * resumes) ne depasse jamais `disponible` — ou, quand aucune mise en page ne le
 * permet plus, le plan le DIT avec defilement === true et le rendu ouvre une
 * barre de defilement. Rien n'est jamais coupe en silence : comme
 * .bande-tuiles n'existe QUE en mode tuiles, il ne peut pas etre rogne.
 */
export function planifier(
  bandes: ExigenceBande[],
  disponible: number,
  mesures: MesuresBande
): PlanBandes {
  const fixe = coutFixeTuiles(mesures)
  const resume = coutResume(mesures)

  const enTuiles = new Set<CleBande>(bandes.map((bande) => bande.cle))
  const cout = () =>
    bandes.reduce(
      (somme, bande) =>
        somme + (enTuiles.has(bande.cle) ? fixe + bande.plancher : resume),
      0
    )

  // On degrade une bande a la fois, la moins urgente d'abord, et on s'arrete
  // des que le total tient. Une bande absente de `bandes` n'est pas dans
  // enTuiles : la retirer ne fait rien, l'ordre reste valable.
  for (const cle of ORDRE_DEGRADATION) {
    if (cout() <= disponible) break
    enTuiles.delete(cle)
  }

  const restantes = bandes.filter((bande) => enTuiles.has(bande.cle))
  const nombreResumes = bandes.length - restantes.length

  // Deux colonnes en dernier recours : toutes les bandes sont deja en resume
  // et leurs lignes ne tiennent toujours pas empilees. Deux par rangee divise
  // le besoin par deux, et une ligne de resume reste une cible de 44 px.
  const colonnes: 1 | 2 =
    restantes.length === 0 && bandes.length * resume > disponible ? 2 : 1

  const sommePoids = restantes.reduce((somme, bande) => somme + bande.poids, 0)
  const sommePlanchers = restantes.reduce((somme, bande) => somme + bande.plancher, 0)
  // Chaque bande gardee recoit d'abord son plancher ; seul le SURPLUS se
  // partage au prorata des poids. Un partage au prorata pur pourrait donner a
  // une bande moins que son plancher, et la couper : c'est precisement ce qui
  // arrivait a la bande Heros a 4 joueurs.
  const surplus = Math.max(
    0,
    disponible - restantes.length * fixe - sommePlanchers - nombreResumes * resume
  )

  const modes = new Map<CleBande, ModeBande>()
  const hauteurs = new Map<CleBande, number>()
  for (const bande of bandes) {
    if (!enTuiles.has(bande.cle)) {
      modes.set(bande.cle, 'resume')
      continue
    }
    modes.set(bande.cle, 'tuiles')
    // Math.floor, jamais Math.round ni Math.ceil : arrondir vers le haut fait
    // depasser la somme des parts de la hauteur mesuree, et ce depassement
    // d'un pixel est exactement ce que ce calcul existe pour empecher.
    const part = sommePoids > 0 ? Math.floor((bande.poids / sommePoids) * surplus) : 0
    hauteurs.set(bande.cle, bande.plancher + part)
  }

  // Ce que le rendu prendra REELLEMENT avec ce plan. Tant qu'une bande garde
  // ses tuiles, la boucle de degradation garantit que ca tient ; le seul cas
  // qui deborde encore est celui ou tout est deja en resume, sur deux
  // colonnes, et ou la hauteur ne suffit meme plus a ca.
  let rendu = Math.ceil(nombreResumes / colonnes) * resume
  for (const bande of restantes) rendu += fixe + (hauteurs.get(bande.cle) ?? 0)

  return { modes, hauteurs, colonnes, defilement: rendu > disponible }
}

/**
 * Les chiffres qui comptent dans une bande repliee : PV, menace ou hauteur de
 * pile de ses premieres unites. Limite a trois pour que la ligne reste une
 * ligne. Une carte face cachee ne divulgue rien, ici comme sur une tuile.
 */
export function chiffresResume(unites: UniteAffichee[]): string[] {
  const chiffres: string[] = []
  for (const unite of unites) {
    if (chiffres.length >= 3) break
    const carte = unite.carte
    if (carte.facedown === true && carte.peeking !== true) continue
    if (carte.allyHp) chiffres.push(carte.allyHp)
    else if (carte.schemeThreat) chiffres.push(carte.schemeThreat)
    else if (carte.pileCount !== undefined) chiffres.push(String(carte.pileCount))
  }
  return chiffres
}
