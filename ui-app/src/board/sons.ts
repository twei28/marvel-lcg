// Sons du jeu.
//
// Deux sources, une seule table de mixage :
//  - le MOTEUR nomme un son par rendu (`world.sound_name` : "activate",
//    "token", "phase"...), joué par `useSons` ;
//  - le PLATEAU joue lui-même ce que le moteur ne connaît pas : le survol des
//    menus, la carte qui vole, les gestes du mode manuel.
// Les fichiers `<nom>.wav` sont servis à la racine (résolus dans
// assets/sounds/ par le serveur ; sources dans assets/sounds/SOURCES.md).
//
// Règles (refonte des sons, docs/superpowers/specs/2026-09-15-refonte-des-sons-design.md) :
//  - « Bruitages » coupé ou onglet caché : rien ne part ;
//  - volume des effets réglable (défaut 20 %, celui du client d'origine) ;
//  - au plus 2 sons à la fois : un 3e qui arrive pendant une rafale est sauté ;
//  - pas de son sous le voile d'ouverture, ni pendant une question du moteur
//    (le rendu se répète tant qu'elle est ouverte), sauf le gong de phase.
//
// L'autoplay navigateur peut refuser un son avant la première interaction :
// l'échec est silencieux, le son suivant passera.

import { useEffect } from 'react'
import type { World } from './world'

/** Le réglage « Bruitages », partagé avec le lanceur (prepare/sons.js). */
export const CLE_SONS = 'marvel-board-sons'
/** Le volume des effets, en %, partagé avec le lanceur. */
export const CLE_VOLUME_SONS = 'marvel-board-volume-sons'
export const VOLUME_PAR_DEFAUT = 20
export const MAX_SIMULTANES = 2

/** Le survol doit s'entendre à peine : une fraction du volume des effets. */
const FACTEUR_SURVOL = 0.35
const ECART_SURVOL_MS = 80
/** Un son du moteur de la même famille qu'un geste joué juste avant est un doublon. */
const FENETRE_DOUBLON_MS = 600

/** Les sept familles de la spec : plusieurs noms du moteur, un même son. */
const FAMILLE: Record<string, string> = {
  activate: 'capacite',
  damage: 'impact',
  target: 'impact',
  directattack: 'impact',
  draw: 'carte',
  carddrop: 'carte',
  set: 'carte',
  equip: 'carte',
  cardpick: 'carte',
  shuffle: 'carte',
  flip: 'retournement',
  reveal: 'retournement',
  token: 'jeton',
  addcounter: 'jeton',
  removecounter: 'jeton',
  gainlp: 'jeton',
  destroyed: 'disparition',
  banished: 'disparition',
  negate: 'disparition',
  phase: 'gong',
  nextturn: 'gong',
}

/** Le son d'un geste manuel, par méthode `Puzzle.*` (triche.ts). */
const SON_DU_GESTE: Record<string, string> = {
  Flip: 'flip',
  Reveal: 'reveal',
  Exhaust: 'draw',
  Ready: 'draw',
  MoveTo: 'draw',
  Gain: 'draw',
  Attach: 'equip',
  Engage: 'draw',
  PutIntoPlay: 'carddrop',
  PutIntoDeck: 'draw',
  Discard: 'draw',
  SwapWithDeckTop: 'draw',
  Mulligan: 'draw',
  DrawUpToHandSize: 'draw',
  Shuffle: 'shuffle',
  ShuffleDiscardIntoDeck: 'shuffle',
  Damage: 'damage',
  Heal: 'gainlp',
  PlaceThreat: 'token',
  SetThreat: 'token',
  Token: 'token',
  Counter: 'token',
  Stun: 'token',
  Confuse: 'token',
  Tough: 'token',
  Remove: 'banished',
  AdvanceVillain: 'destroyed',
  AdvanceMainScheme: 'destroyed',
  EndRound: 'nextturn',
}

type Lecteur = HTMLAudioElement

const enCours = new Set<Lecteur>()
const dernierGeste = new Map<string, number>()
let dernierSurvol = -Infinity
let dernierRenderJoue = -1
/** L'état de la table, posé par `useSons` à chaque rendu. */
let porte = { silence: false }

/** Remet la table de mixage à zéro (tests). */
export function reinitialiserSons(): void {
  enCours.clear()
  dernierGeste.clear()
  dernierSurvol = -Infinity
  dernierRenderJoue = -1
  porte = { silence: false }
}

export function lireVolumeSons(): number {
  try {
    const brut = window.localStorage.getItem(CLE_VOLUME_SONS)
    if (brut === null) return VOLUME_PAR_DEFAUT
    const valeur = Number(brut)
    return Number.isFinite(valeur) ? Math.min(100, Math.max(0, valeur)) : VOLUME_PAR_DEFAUT
  } catch {
    return VOLUME_PAR_DEFAUT
  }
}

export function ecrireVolumeSons(volume: number): void {
  try {
    window.localStorage.setItem(CLE_VOLUME_SONS, String(Math.round(Math.min(100, Math.max(0, volume)))))
  } catch {
    // Stockage refusé : le réglage vaut pour cette page seulement.
  }
}

function sonsCoupes(): boolean {
  try {
    return window.localStorage.getItem(CLE_SONS) === 'off'
  } catch {
    return false
  }
}

function maintenant(): number {
  return typeof performance !== 'undefined' ? performance.now() : Date.now()
}

/**
 * Joue `<nom>.wav` si la table le permet. Renvoie vrai si le son est parti.
 * `facteur` module le volume des effets (le survol est plus bas).
 */
export function jouerSon(nom: string, facteur = 1): boolean {
  if (!nom || sonsCoupes()) return false
  if (typeof document !== 'undefined' && document.visibilityState === 'hidden') return false
  for (const lecteur of enCours) {
    if (lecteur.ended || lecteur.paused || lecteur.error) enCours.delete(lecteur)
  }
  if (enCours.size >= MAX_SIMULTANES) return false
  try {
    // Un élément par lecture : deux sons identiques peuvent se chevaucher, le
    // navigateur garde le fichier en cache.
    const lecteur = new Audio(`/${nom}.wav`)
    lecteur.volume = Math.min(1, Math.max(0, (lireVolumeSons() / 100) * facteur))
    lecteur.addEventListener('ended', () => enCours.delete(lecteur))
    enCours.add(lecteur)
    void lecteur.play().catch(() => enCours.delete(lecteur))
    return true
  } catch {
    return false
  }
}

/** Survol d'un bouton ou d'un héros dans un menu : très bas, jamais en rafale. */
export function jouerSurvol(): void {
  const t = maintenant()
  if (t - dernierSurvol < ECART_SURVOL_MS) return
  if (jouerSon('survol', FACTEUR_SURVOL)) dernierSurvol = t
}

/**
 * Une carte décolle pour voler d'une zone à l'autre (CoucheAnimations).
 *
 * ⚠ PAS DE PORTE « QUESTION » ICI. Cette règle vise le son du MOTEUR, que le
 * rendu répète tant que la question reste ouverte. Un vol est un mouvement
 * réel, joué une fois ; le couper pendant une question le rendait muet en
 * mode manuel (la question du moteur y reste garée) et pendant presque toutes
 * les pioches. Constaté au navigateur le 07/10/2026 : Ctrl+D sans vol.wav.
 */
export function jouerVol(): void {
  if (porte.silence) return
  jouerSon('vol')
}

/**
 * Un geste du mode manuel vient d'être accepté (triche.ts) : il sonne comme
 * en automatique, et la famille est notée pour ne pas la rejouer si le moteur
 * l'annonce aussi dans le rendu qui suit.
 */
export function jouerGeste(commandes: readonly string[]): void {
  if (porte.silence) return
  for (const commande of commandes) {
    const methode = /^Puzzle\.(\w+)\(/.exec(commande)?.[1]
    const nom = methode ? SON_DU_GESTE[methode] : undefined
    if (!nom) continue
    if (jouerSon(nom)) dernierGeste.set(FAMILLE[nom] ?? nom, maintenant())
    return
  }
}

/**
 * Le survol des boutons et des héros d'un MENU (pas de la table de jeu, où il
 * deviendrait un bruit de fond). Écoute déléguée sur `racine` : seul l'élément
 * qui répond à `selecteur` compte, et passer d'un de ses enfants à un autre ne
 * relance pas le son. Souris seulement : au doigt, il n'y a pas de survol.
 * Renvoie de quoi retirer l'écoute.
 */
/** Les menus du plateau : la fenêtre « ⌂ Menu » et les Réglages (même cadre). */
export const SELECTEUR_SURVOL_PLATEAU = '.reglages-fenetre button'

export function installerSurvol(racine: Document | HTMLElement, selecteur: string): () => void {
  let dernier: Element | null = null
  const surEntree = (evenement: Event) => {
    const type = (evenement as Event & { pointerType?: string }).pointerType
    if (type && type !== 'mouse') return
    const cible = evenement.target instanceof Element ? evenement.target.closest(selecteur) : null
    if (cible === dernier) return
    dernier = cible
    if (cible && !(cible instanceof HTMLButtonElement && cible.disabled)) jouerSurvol()
  }
  racine.addEventListener('pointerover', surEntree)
  return () => racine.removeEventListener('pointerover', surEntree)
}

/**
 * @param silence Le voile d'ouverture est EN PLACE : on ne joue rien.
 *
 * ⚠ LE SILENCE DE L'OUVERTURE VAUT AUSSI POUR LES SONS (spec du 15/09/2026,
 * « aucun son pendant la mise en place »). Le plateau appelle ce hook avant
 * son retour anticipe du voile — il le faut, les hooks ne se sautent pas — et
 * chaque trame de mise en place portant un `sound_name` etait donc jouee
 * derriere le voile. Parametre OPTIONNEL : les autres appelants ne changent
 * pas.
 *
 * ⚠ La porte est posee APRES `dernierRenderJoue`, comme celle d'`actif` : une
 * trame avalee sous le voile est avalee pour de bon, et ne repart pas en
 * rafale au moment ou la table apparait.
 */
export function useSons(
  monde: World | undefined,
  actif: boolean,
  joueurInterroge: boolean,
  silence = false
) {
  porte = { silence }
  useEffect(() => {
    if (!monde || monde.render_id === dernierRenderJoue) return
    dernierRenderJoue = monde.render_id

    if (!actif) return
    if (silence) return
    if (document.visibilityState !== 'visible') return

    const nom = monde.sound_name
    if (!nom) return
    // Comme l'original : pas de son pendant qu'on attend NOTRE decision (le
    // rendu se repete tant que la question est ouverte), sauf le gong de phase.
    if (joueurInterroge && nom !== 'phase') return
    const geste = dernierGeste.get(FAMILLE[nom] ?? nom)
    if (geste !== undefined && maintenant() - geste < FENETRE_DOUBLON_MS) return
    jouerSon(nom)
  }, [monde, monde?.render_id, actif, joueurInterroge, silence])
}
