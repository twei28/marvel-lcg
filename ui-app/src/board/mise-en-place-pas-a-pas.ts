// LA MISE EN PLACE, CARTE PAR CARTE (10/10/2026, décisions de l'utilisateur).
//
// Le moteur résout la mise en place d'un trait (Rules Reference v1.8,
// Appendix II « Setup ») et ne s'arrête qu'à ses questions. Le plateau, lui,
// montre chaque carte qui arrive en jeu, en grand, dans l'ordre, et attend
// « Continuer » avant la suivante : méchant, manigances, sbires, attachements,
// environnements, dégâts, menace de départ.
//
// Module PUR : on compare deux photos du monde, on en tire des étapes.

import type { World, WorldCard } from './world'
import { estUneCarte } from './world'
import { estFormeEnergieSpectrum } from './formes-energie-spectrum'
import type { Fige } from './coups-sur-table'
import { environnementVisible } from './ville-etat'
import { PAIRES_JUMELLES } from './panorama-jumelles'

export type GenreEtape = 'arrivee' | 'retournement' | 'degats' | 'menace'

export type EtapeMiseEnPlace = {
  cle: string
  carteId: number
  picId: string
  codeCarte: string
  type: string
  traits: string[]
  /** Clé de traduction de la légende (« Méchant », « Manigance annexe »...). */
  legende: string
  /** Nom du héros pour « Engagé avec », ou nombre pour un dégât / une menace. */
  detail?: { cle: string; valeur: string | number }
  paysage: boolean
  /** Ce que l'étape change sur la table (absent : une arrivée). */
  genre?: GenreEtape
  /** La carte AVANT l'étape : ce que la table montre tant qu'on n'a pas cliqué. */
  avant?: { pic?: string; code?: string; pv?: number; menace?: number }
}

type Vu = { pic: string; code?: string; pv?: number; menace?: number }

/** Ce que le plateau a déjà présenté, par identifiant de carte. */
export type MemoireMiseEnPlace = Map<number, Vu>

const TYPES_PAYSAGE = new Set(['MainScheme', 'EncounterSideScheme', 'PlayerSideScheme', 'SideScheme'])
const IDENTITES = new Set(['Hero', 'AlterEgo'])

type CarteEnJeu = { carte: WorldCard; engageAvec?: string }

function cartes(zone: unknown): WorldCard[] {
  return Array.isArray(zone) ? zone.filter(estUneCarte) : []
}

/** Toutes les cartes en jeu que la mise en place peut faire arriver. */
export function cartesEnJeu(monde: World): CarteEnJeu[] {
  const liste: CarteEnJeu[] = []
  for (const carte of cartes(monde.area_villain)) liste.push({ carte })
  for (const carte of cartes(monde.area_schemes_main)) liste.push({ carte })
  for (const carte of cartes(monde.area_schemes_side)) liste.push({ carte })
  // La ville : la mise en place ne presente que le lieu de DEPART (Midtown), pas les neuf lieux (23/10/2026). Tous les joueurs y partent.
  for (const carte of environnementVisible(monde, 0, cartes(monde.area_environment))) liste.push({ carte })
  for (const joueur of monde.players ?? []) {
    const heros = cartes(joueur.area_hero).find((c) => IDENTITES.has(c.card_type))
    for (const carte of cartes(joueur.engaged_enemies)) liste.push({ carte, engageAvec: heros?.name })
    for (const carte of cartes(joueur.area_hero)) liste.push({ carte })
    for (const carte of cartes(joueur.allies)) liste.push({ carte })
    for (const carte of cartes(joueur.supports)) liste.push({ carte })
    for (const carte of environnementVisible(monde, (monde.players ?? []).indexOf(joueur), cartes(joueur.environment_area))) liste.push({ carte })
  }
  return liste
}

export function legendeDe(carte: WorldCard): string {
  switch (carte.card_type) {
    case 'Villain':
    case 'EncounterVillain':
      return 'Méchant'
    case 'MainScheme':
      return 'Manigance principale'
    case 'EncounterSideScheme':
    case 'SideScheme':
      return 'Manigance annexe'
    case 'Minion':
      return 'Sbire'
    case 'Attachment':
      return 'Attachement'
    case 'Environment':
      return 'Environnement'
    default:
      return 'Carte de mise en place'
  }
}

export type Reglages = {
  /** Le panneau de la manigance principale la présente déjà (confirm_main_scheme). */
  panneauPrincipale: boolean
  /** Le panneau des manigances annexes les présente déjà (confirm_side_scheme). */
  panneauAnnexe: boolean
}

function presenteeParUnPanneau(carte: WorldCard, reglages: Reglages): boolean {
  if (carte.card_type === 'MainScheme') return reglages.panneauPrincipale
  if (carte.card_type === 'EncounterSideScheme') return reglages.panneauAnnexe
  return false
}

function etape(
  carte: WorldCard,
  legende: string,
  cle: string,
  detail?: EtapeMiseEnPlace['detail'],
  genre: GenreEtape = 'arrivee',
  avant?: EtapeMiseEnPlace['avant']
): EtapeMiseEnPlace {
  return {
    genre,
    avant,
    cle,
    carteId: carte.id,
    picId: carte.pic_id,
    codeCarte: carte.card_id,
    type: carte.card_type,
    // Les clefs du moteur portent un prefixe « t_ » (`t_LOCATION`) : sans lui, la traduction du trait (LIEU) est retrouvee.
    traits: Object.keys(carte.traits ?? {}).map((cle) => (cle.startsWith('t_') ? cle.slice(2).replace(/_/g, ' ') : cle)),
    legende,
    detail,
    paysage: TYPES_PAYSAGE.has(carte.card_type),
  }
}

function pv(carte: WorldCard): number | undefined {
  const v = carte.info?.health
  return typeof v === 'number' ? v : undefined
}

function menace(carte: WorldCard): number | undefined {
  const v = carte.info?.k_threat
  return typeof v === 'number' ? v : undefined
}

/**
 * Les étapes nouvelles entre la mémoire et ce monde, et la mémoire mise à jour.
 *
 * Ordre : les cartes arrivées, dans l'ordre de leur création (identifiant
 * croissant, qui suit l'ordre où le moteur les a fait naître), puis les
 * retournements, puis les dégâts et la menace posée.
 */
export function etapesNouvelles(
  memoire: MemoireMiseEnPlace,
  monde: World,
  reglages: Reglages
): { etapes: EtapeMiseEnPlace[]; memoire: MemoireMiseEnPlace } {
  const suite = new Map(memoire)
  const arrivees: EtapeMiseEnPlace[] = []
  const changements: EtapeMiseEnPlace[] = []
  const enJeu = [...cartesEnJeu(monde)].sort((a, b) => a.carte.id - b.carte.id)
  for (const { carte, engageAvec } of enJeu) {
    const avant = memoire.get(carte.id)
    const maintenant: Vu = { pic: carte.pic_id, code: carte.card_id, pv: pv(carte), menace: menace(carte) }
    suite.set(carte.id, maintenant)
    const visible = carte.is_face_up && Boolean(carte.pic_id)
    if (!visible) continue
    const cle = `${monde.render_id}-${carte.id}`
    if (!avant) {
      if (IDENTITES.has(carte.card_type)) continue
      // Le setup moteur les pose puis les retourne : ne pas mémoriser leur image
      // transitoire face visible comme une arrivée à rejouer au joueur.
      if (estFormeEnergieSpectrum(carte)) continue
      if (presenteeParUnPanneau(carte, reglages)) continue
      arrivees.push(
        etape(carte, legendeDe(carte), `${cle}-e`, engageAvec ? { cle: 'héros', valeur: engageAvec } : undefined)
      )
      continue
    }
    if (avant.pic !== carte.pic_id && carte.card_type === 'MainScheme') {
      const m = maintenant.menace
      changements.push(
        etape(carte, 'Manigance principale retournée', `${cle}-r`, m ? { cle: 'menace de départ', valeur: m } : undefined, 'retournement', {
          pic: avant.pic,
          code: avant.code,
          menace: avant.menace,
        })
      )
      continue
    }
    if (avant.pv !== undefined && maintenant.pv !== undefined && maintenant.pv < avant.pv) {
      changements.push(etape(carte, 'Dégâts', `${cle}-d`, { cle: 'dégâts', valeur: avant.pv - maintenant.pv }, 'degats', { pv: avant.pv }))
    }
    if (
      carte.card_type !== 'MainScheme' &&
      avant.menace !== undefined &&
      maintenant.menace !== undefined &&
      maintenant.menace > avant.menace
    ) {
      changements.push(etape(carte, 'Menace', `${cle}-m`, { cle: 'menace', valeur: maintenant.menace - avant.menace }, 'menace', {
          menace: avant.menace,
        }))
    }
  }
  // Les retournements de manigances principales dans l'ORDRE DE LA TABLE
  // (1B avant 2B), pas des numeros de carte : sur Tower Defense, 2B portait le
  // plus petit numero et passait devant (10/10/2026). Tri stable : le reste ne
  // bouge pas.
  const rang = new Map(cartes(monde.area_schemes_main).map((c, i) => [c.id, i]))
  const rangDe = (e: EtapeMiseEnPlace) => (e.type === 'MainScheme' ? rang.get(e.carteId) ?? 0 : 0)
  changements.sort((a, b) => (a.type === 'MainScheme' && b.type === 'MainScheme' ? rangDe(a) - rangDe(b) : 0))
  return { etapes: [...arrivees, ...changements], memoire: suite }
}

/**
 * LE PANNEAU DE LA MANIGANCE PRINCIPALE AVANT LE MECHANT (10/10/2026).
 *
 * Livret « Learn to Play », etape 10 : le paquet du mechant et celui des
 * manigances principales entrent en jeu ENSEMBLE ; la mise en place de la
 * manigance (etape 12) et son retournement viennent apres. L'utilisateur veut
 * voir 1A, 2A, PUIS les mechants. Au lever du voile, la file tient deja les
 * mechants, et le panneau attendait qu'elle soit vide : il passe devant, mais
 * seulement devant un mechant, et seulement pour une manigance PRINCIPALE (une
 * annexe de mise en place arrive a l'etape 12, apres le mechant).
 */
export function panneauAvantLaFile(tete: EtapeMiseEnPlace | undefined, carteDuPanneau: WorldCard | undefined): boolean {
  if (!tete || !carteDuPanneau || carteDuPanneau.card_type !== 'MainScheme') return false
  return tete.type === 'Villain' || tete.type === 'EncounterVillain'
}

const RETOURNEMENT = 'Manigance principale retournée'

/**
 * LES RETOURNEMENTS DANS L'ORDRE DE LA TABLE, MEME ARRIVES EN DEUX TRAMES.
 *
 * Tower Defense : la mise en place de 1A revele 2A, qui se retourne en 2B AVANT
 * que 1A ne se retourne (moteur, etape 12 imbriquee). Les deux retournements
 * arrivent dans deux trames, 2B d'abord. L'utilisateur veut 1B puis 2B : on
 * remet les retournements EN ATTENTE dans l'ordre de `area_schemes_main`, sans
 * deplacer le reste ni l'etape deja affichee (les `figees` premieres).
 */
export function ordonnerRetournements(file: EtapeMiseEnPlace[], monde: World, figees: number): EtapeMiseEnPlace[] {
  const rang = new Map(cartes(monde.area_schemes_main).map((c, i) => [c.id, i]))
  const places: number[] = []
  file.forEach((e, i) => {
    if (i >= figees && e.legende === RETOURNEMENT) places.push(i)
  })
  if (places.length < 2) return file
  const tries = places.map((i) => file[i]).sort((a, b) => (rang.get(a.carteId) ?? 0) - (rang.get(b.carteId) ?? 0))
  const resultat = [...file]
  places.forEach((i, k) => {
    resultat[i] = tries[k]
  })
  return resultat
}

/**
 * LE MECHANT ATTEND LA PREMIERE QUESTION (10/10/2026).
 *
 * Avec la confirmation des manigances principales, la premiere question du
 * moteur est TOUJOURS le panneau de 1A. Mais la trame du monde peut arriver
 * avant elle : le mechant, deja en file, passait alors devant (mesure sur Tower
 * Defense, une fois sur quatre). Tant que le moteur n'a rien demande pendant la
 * mise en place, un mechant en tete de file attend ; la question ne peut pas
 * manquer d'arriver (au pire, le mulligan).
 */
export function mechantAttendLaQuestion(
  tete: EtapeMiseEnPlace | undefined,
  etat: { enMiseEnPlace: boolean; confirmPrincipale: boolean; demandePresente: boolean }
): boolean {
  if (!tete || !etat.enMiseEnPlace || !etat.confirmPrincipale || etat.demandePresente) return false
  return tete.type === 'Villain' || tete.type === 'EncounterVillain'
}


/**
 * CE QUE LA TABLE NE MONTRE PAS ENCORE (13/10/2026, décisions de l'utilisateur).
 *
 * « Elles sont déjà présentes sur le plateau, donc c'est un petit peu bête » :
 * tant qu'une carte n'a pas eu son « Continuer », sa place reste un contour en
 * pointillés ; un jeton (dégâts, menace) garde sa valeur d'avant ; une
 * manigance principale garde sa face d'avant. La manigance que le panneau
 * présente (`panneauId`) attend elle aussi en pointillés.
 *
 * Plusieurs étapes sur la même carte : la valeur d'avant est celle de la
 * PREMIÈRE en attente.
 */
export type AttenteSurTable = {
  cachees: Set<number>
  figes: Fige[]
  faces: Map<number, { pic: string; code?: string; menace?: number }>
}

export function attenteSurTable(file: readonly EtapeMiseEnPlace[], panneauId?: number): AttenteSurTable {
  const cachees = new Set<number>()
  const figes: Fige[] = []
  const faces = new Map<number, { pic: string; code?: string; menace?: number }>()
  if (panneauId !== undefined) cachees.add(panneauId)
  const fige = (genre: Fige['genre'], cibleId: number, valeur: number | undefined) => {
    if (valeur === undefined || figes.some((f) => f.genre === genre && f.cibleId === cibleId)) return
    figes.push({ genre, cibleId, valeur })
  }
  for (const e of file) {
    const genre = e.genre ?? 'arrivee'
    if (genre === 'arrivee') cachees.add(e.carteId)
    else if (genre === 'degats') fige('degats', e.carteId, e.avant?.pv)
    else if (genre === 'menace') fige('menace', e.carteId, e.avant?.menace)
    else if (e.avant?.pic && !faces.has(e.carteId)) faces.set(e.carteId, { pic: e.avant.pic, code: e.avant.code, menace: e.avant.menace })
  }
  return { cachees, figes, faces }
}

/** Le monde où chaque manigance de `faces` montre encore sa face d'avant. */
export function avecFacesDAvant(monde: World, faces: AttenteSurTable['faces']): World {
  if (faces.size === 0) return monde
  const principales = cartes(monde.area_schemes_main)
  if (!principales.some((c) => faces.has(c.id))) return monde
  return {
    ...monde,
    area_schemes_main: principales.map((c) => {
      const f = faces.get(c.id)
      if (!f) return c
      const info = f.menace === undefined ? c.info : { ...c.info, k_threat: f.menace }
      return { ...c, pic_id: f.pic, card_id: f.code ?? c.card_id, info }
    }),
  }
}

/**
 * Paire jumelle EN TETE de file (The City + Never Sleeps, 23/10/2026) : les deux cartes se montrent ENSEMBLE, collées bord à bord, la 1re à
 * gauche, et un seul « Continuer » les pose toutes les deux. Le moteur les fait arriver dans deux trames différentes : la moitié pas encore
 * arrivée est montrée d'après son code (son étape, quand elle arrive, est écartée par `sansMoitiesDejaMontrees`). `undefined` : la tête se
 * montre seule.
 */
const estUneArrivee = (e: EtapeMiseEnPlace): boolean => e.genre === undefined || e.genre === 'arrivee'

export function paireEnTete(file: readonly EtapeMiseEnPlace[]): { gauche: EtapeMiseEnPlace; droite: EtapeMiseEnPlace } | undefined {
  const tete = file[0]
  if (!tete || !estUneArrivee(tete)) return undefined
  for (const paire of PAIRES_JUMELLES) {
    if (tete.codeCarte !== paire.gauche && tete.codeCarte !== paire.droite) continue
    const autreCode = tete.codeCarte === paire.gauche ? paire.droite : paire.gauche
    const autre: EtapeMiseEnPlace = file.find((e) => estUneArrivee(e) && e.codeCarte === autreCode) ?? {
      ...tete,
      cle: `${tete.cle}-jumelle`,
      carteId: -1,
      picId: autreCode,
      codeCarte: autreCode,
    }
    return tete.codeCarte === paire.gauche ? { gauche: tete, droite: autre } : { gauche: autre, droite: tete }
  }
  return undefined
}

/** Les arrivées d'une moitié de paire DÉJÀ montrée avec sa sœur ne se montrent pas une seconde fois. */
export function sansMoitiesDejaMontrees(etapes: readonly EtapeMiseEnPlace[], montrees: ReadonlySet<string>): EtapeMiseEnPlace[] {
  return etapes.filter((e) => !estUneArrivee(e) || !montrees.has(e.codeCarte))
}
