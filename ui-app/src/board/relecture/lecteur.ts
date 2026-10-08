// Le « moteur » de la relecture : il pousse au plateau les mondes enregistres,
// avec la meme interface que `Moteur` (usePartieEnCours n'y voit que du feu),
// et pilote la lecture (pause, pas a pas, vitesse, saut).
import type { EtatMoteur, ModePhaseMechant } from '../moteur'
import type { Reponse } from '../ask'
import type { Relecture, VuEnregistre } from './fichier'

export const PAUSE_MAX_DEFAUT_S = 5
/** Un temps mort plus long que la pause max est ramene a ceci (decision du 08/10/2026 : 5 s -> 2 s). */
export const PAUSE_RACCOURCIE_MS = 2000
export const VITESSES = [0.5, 1, 2, 4] as const

/**
 * Le temps de lecture d'un intervalle enregistre [debut, fin], ses evenements
 * interieurs (clics, survols, selections) gardes : chaque temps mort ENTRE deux
 * evenements plus long que `pauseMaxMs` est ramene a PAUSE_RACCOURCIE_MS, le
 * reste joue en temps reel. Rend les bornes en temps reel et en temps de lecture.
 */
export function echelle(debut: number, fin: number, points: number[], pauseMaxMs: number): { reel: number[]; lu: number[] } {
  const reel = [debut, ...points.filter((t) => t > debut && t < fin).sort((a, b) => a - b), fin]
  const lu = [0]
  for (let i = 1; i < reel.length; i++) {
    const ecart = Math.max(0, reel[i] - reel[i - 1])
    lu.push(lu[i - 1] + (ecart > pauseMaxMs ? Math.min(ecart, PAUSE_RACCOURCIE_MS) : ecart))
  }
  return { reel, lu }
}

/** Le temps enregistre correspondant a `ecoule` ms de lecture dans l'echelle. */
export function tempsReel(e: { reel: number[]; lu: number[] }, ecoule: number): number {
  for (let i = 1; i < e.lu.length; i++) {
    if (ecoule <= e.lu[i]) {
      const part = e.lu[i] === e.lu[i - 1] ? 1 : (ecoule - e.lu[i - 1]) / (e.lu[i] - e.lu[i - 1])
      return e.reel[i - 1] + part * (e.reel[i] - e.reel[i - 1])
    }
  }
  return e.reel[e.reel.length - 1]
}

/** L'inverse de `tempsReel` : ou en est la lecture quand le temps enregistre vaut `reel`. */
export function tempsLu(e: { reel: number[]; lu: number[] }, reel: number): number {
  for (let i = 1; i < e.reel.length; i++) {
    if (reel <= e.reel[i]) {
      const etendue = e.reel[i] - e.reel[i - 1]
      const part = etendue <= 0 ? 1 : (reel - e.reel[i - 1]) / etendue
      return e.lu[i - 1] + Math.max(0, part) * (e.lu[i] - e.lu[i - 1])
    }
  }
  return e.lu[e.lu.length - 1]
}

/** Empreinte d'une question, pour reconnaitre une NOUVELLE decision d'une question repetee. */
function empreinteDemandes(demandes: Record<number, { event_name?: string; options?: { id: number }[] }>): string {
  return Object.entries(demandes)
    .map(([p, d]) => `${p}:${d.event_name ?? ''}:${(d.options ?? []).map((o) => o.id).join(',')}`)
    .join('|')
}

export type Repere = { index: number; genre: 'round' | 'phase-mechant' | 'vaincu'; libelle: string }

export type ControleLecture = {
  index: number
  total: number
  enLecture: boolean
  vitesse: number
  pauseMaxS: number
  muet: boolean
  /** Le siege affiche (celui que la vue automatique suit, ou celui choisi). */
  pointDeVue: number
  /** Vrai : la vue suit le joueur qui a la main (decision du 08/10/2026). */
  vueAuto: boolean
}

const PHASES_MECHANT = new Set(['Main Scheme Place Threat', 'Enemy Activation', 'Deal Encounter Cards', 'Reveal Encounter Cards'])

/** Les reperes de la barre : debut de chaque round, de chaque phase du mechant, et chaque defaite d'un heros ou d'un allie. */
export function reperesDe(relecture: Relecture): Repere[] {
  const reperes: Repere[] = []
  let roundVu: number | undefined
  let dansPhase = false
  let allies: Set<number>[] = []
  let elimines: boolean[] = []
  relecture.trames.forEach(({ monde }, index) => {
    if (monde.round_id !== roundVu) {
      if (roundVu !== undefined) reperes.push({ index, genre: 'round', libelle: `Round ${monde.round_id}` })
      roundVu = monde.round_id
    }
    const enPhase = PHASES_MECHANT.has(monde.phase)
    if (enPhase && !dansPhase) reperes.push({ index, genre: 'phase-mechant', libelle: `Phase du méchant, round ${monde.round_id}` })
    dansPhase = enPhase
    const joueurs = monde.players ?? []
    joueurs.forEach((joueur, p) => {
      const ici = new Set((joueur.allies ?? []).map((c) => c.id))
      const defausse = new Set((joueur.player_discard_pile ?? []).map((c) => c.id))
      for (const id of allies[p] ?? []) {
        if (!ici.has(id) && defausse.has(id)) {
          const nom = (joueur.player_discard_pile ?? []).find((c) => c.id === id)?.name ?? 'Allié'
          reperes.push({ index, genre: 'vaincu', libelle: `${nom.replace(/^\W*/, '')} vaincu` })
        }
      }
      const elimine = joueur.is_eliminated === true
      if (elimine && !elimines[p]) {
        const nom = joueur.area_hero?.[0]?.name?.replace(/^\W*/, '') ?? `Joueur ${p + 1}`
        reperes.push({ index, genre: 'vaincu', libelle: `${nom} vaincu` })
      }
      elimines[p] = elimine
    })
    allies = joueurs.map((j) => new Set((j.allies ?? []).map((c) => c.id)))
    elimines = elimines.slice(0, joueurs.length)
  })
  return reperes
}

export class Lecteur {
  readonly reperes: Repere[]
  private index = 0
  private enLecture = false
  private vitesse = 1
  private pauseMaxS = PAUSE_MAX_DEFAUT_S
  private muet = false
  private pointDeVue = 0
  private vueAuto = true
  private siegeSuivi = 0
  private saut = false
  private echelleCourante: { reel: number[]; lu: number[] } | undefined
  private readonly vusParCle = new Map<string, VuEnregistre[]>()
  private readonly instantsEvenements: number[]
  readonly decisions: number[]
  private minuteur: number | undefined
  private debutAttente = 0
  private delaiAttente = 0
  /**
   * Le temps enregistre ou la lecture s'est arretee ENTRE deux trames. En
   * pause, ce que le joueur faisait a cet instant (selection, loupe...) reste
   * a l'ecran, et la lecture repart de la.
   */
  private tempsArrete: number | undefined
  private ecouteursEtat = new Set<(etat: EtatMoteur) => void>()
  private ecouteursControle = new Set<() => void>()
  private controle: ControleLecture

  constructor(readonly relecture: Relecture, readonly identite: string) {
    this.reperes = reperesDe(relecture)
    for (const vu of relecture.vus ?? []) {
      const cle = `${vu.p}|${vu.g}`
      const liste = this.vusParCle.get(cle) ?? []
      liste.push(vu)
      this.vusParCle.set(cle, liste)
    }
    for (const liste of this.vusParCle.values()) liste.sort((a, b) => a.t - b.t)
    this.instantsEvenements = [...(relecture.vus ?? []).map((v) => v.t), ...relecture.curseurs.map((c) => c.t)].sort((a, b) => a - b)
    this.decisions = []
    let avant = ''
    relecture.trames.forEach((trame, i) => {
      const empreinte = empreinteDemandes(trame.demandes)
      if (empreinte !== '' && empreinte !== avant) this.decisions.push(i)
      avant = empreinte
    })
    this.controle = this.calculerControle()
  }

  // --- Interface de `Moteur` -------------------------------------------------
  ecouter(ecouteur: (etat: EtatMoteur) => void): () => void {
    this.ecouteursEtat.add(ecouteur)
    return () => this.ecouteursEtat.delete(ecouteur)
  }
  demarrer() {
    this.publier()
  }
  arreter() {}
  async repondre(_reponse: Reponse | null, _bindPlayerId?: number): Promise<boolean> {
    return false
  }
  continuer() {}
  reconnecterMaintenant() {}
  setModePhaseMechant(_mode: ModePhaseMechant) {}
  avancerMaintenant() {}
  signalerActiviteDuJoueur() {}

  // --- Pilotage ---------------------------------------------------------------
  ecouterControle(ecouteur: () => void): () => void {
    this.ecouteursControle.add(ecouteur)
    return () => this.ecouteursControle.delete(ecouteur)
  }
  lireControle(): ControleLecture {
    return this.controle
  }

  aller(index: number) {
    const borne = Math.max(0, Math.min(this.relecture.trames.length - 1, index))
    this.saut = Math.abs(borne - this.index) > 1
    this.index = borne
    this.tempsArrete = undefined
    this.publier()
    this.saut = false
    if (this.enLecture) this.planifier()
  }
  /** Jusqu'a la prochaine decision d'un joueur (decision du 08/10/2026). */
  suivant() {
    this.pause()
    const prochaine = this.decisions.find((i) => i > this.index)
    this.aller(prochaine ?? this.relecture.trames.length - 1)
  }
  precedent() {
    this.pause()
    const precedente = [...this.decisions].reverse().find((i) => i < this.index)
    this.aller(precedente ?? 0)
  }
  roundSuivant() {
    this.pause()
    const prochain = this.reperes.find((r) => r.genre === 'round' && r.index > this.index)
    this.aller(prochain?.index ?? this.relecture.trames.length - 1)
  }
  roundPrecedent() {
    this.pause()
    const debuts = [0, ...this.reperes.filter((r) => r.genre === 'round').map((r) => r.index)]
    const precedent = [...debuts].reverse().find((i) => i < this.index)
    this.aller(precedent ?? 0)
  }
  vitessePlus() {
    const i = VITESSES.indexOf(this.vitesse as (typeof VITESSES)[number])
    this.reglerVitesse(VITESSES[Math.min(VITESSES.length - 1, (i === -1 ? 1 : i) + 1)])
  }
  vitesseMoins() {
    const i = VITESSES.indexOf(this.vitesse as (typeof VITESSES)[number])
    this.reglerVitesse(VITESSES[Math.max(0, (i === -1 ? 1 : i) - 1)])
  }
  /** Se place a un instant enregistre (la trame qui le precede, et l'instant lui-meme). */
  allerAuTemps(t: number) {
    const trames = this.relecture.trames
    let index = 0
    while (index + 1 < trames.length && trames[index + 1].t <= t) index += 1
    this.aller(index)
    this.tempsArrete = Math.max(trames[index].t, t)
  }
  lecture() {
    if (this.index >= this.relecture.trames.length - 1) {
      this.index = 0
      this.tempsArrete = undefined
      this.saut = true
      this.publier()
      this.saut = false
    }
    this.enLecture = true
    this.planifier(this.tempsArrete)
    this.tempsArrete = undefined
    this.publierControle()
  }
  pause() {
    if (this.enLecture) this.tempsArrete = this.tempsCourant()
    this.enLecture = false
    window.clearTimeout(this.minuteur)
    this.publierControle()
  }
  basculerLecture() {
    if (this.enLecture) this.pause()
    else this.lecture()
  }
  reglerVitesse(vitesse: number) {
    const ici = this.enLecture ? this.tempsCourant() : undefined
    this.vitesse = vitesse
    if (this.enLecture) this.planifier(ici)
    this.publierControle()
  }
  reglerPauseMax(secondes: number) {
    const ici = this.enLecture ? this.tempsCourant() : undefined
    this.pauseMaxS = Math.max(0.5, secondes)
    if (this.enLecture) this.planifier(ici)
    this.publierControle()
  }
  basculerMuet() {
    this.muet = !this.muet
    this.publierControle()
  }
  /** Un siege choisi a la main tient jusqu'au retour a l'automatique. */
  reglerPointDeVue(siege: number | 'auto') {
    this.vueAuto = siege === 'auto'
    if (siege !== 'auto') this.pointDeVue = siege
    this.publier()
  }

  /** Le temps enregistre « en cours », entre deux trames pendant l'attente : curseurs et etapes s'y calent. */
  tempsCourant(): number {
    const trames = this.relecture.trames
    const ici = trames[this.index].t
    const suivante = trames[this.index + 1]
    if (!this.enLecture) return this.tempsArrete ?? ici
    if (!suivante || this.delaiAttente <= 0 || !this.echelleCourante) return ici
    const ecoule = Math.min(this.delaiAttente, performance.now() - this.debutAttente) * this.vitesse
    return tempsReel(this.echelleCourante, ecoule)
  }

  /** La premiere valeur publiee d'un genre (reglages et ecran valent des le debut de la partie). */
  premierVu<T = unknown>(p: number, g: string): T | undefined {
    return this.vusParCle.get(`${p}|${g}`)?.[0]?.v as T | undefined
  }

  /** La valeur d'un genre « v » que le siege publiait a l'instant t (la derniere avant t). */
  vuA<T = unknown>(t: number, p: number, g: string): T | undefined {
    const liste = this.vusParCle.get(`${p}|${g}`)
    if (!liste || liste.length === 0 || liste[0].t > t) return undefined
    let bas = 0
    let haut = liste.length - 1
    while (bas < haut) {
      const milieu = (bas + haut + 1) >> 1
      if (liste[milieu].t <= t) bas = milieu
      else haut = milieu - 1
    }
    return liste[bas].v as T
  }

  /** La derniere position connue de chaque curseur, perimee apres 5 s comme en partie. */
  curseursA(t: number): Record<string, { x: number; y: number; clic: number }> {
    const vus: Record<string, { x: number; y: number; clic: number; t: number }> = {}
    for (const c of this.relecture.curseurs) {
      if (c.t > t) break
      vus[c.p] = { x: c.x, y: c.y, clic: c.clic, t: c.t }
    }
    const frais: Record<string, { x: number; y: number; clic: number }> = {}
    for (const [p, c] of Object.entries(vus)) if (t - c.t < 5000) frais[p] = { x: c.x, y: c.y, clic: c.clic }
    return frais
  }

  /** Le mode de phase du joueur a cet instant (publie avec ses etapes). */
  modeA(t: number): string | undefined {
    let mode: string | undefined
    for (const e of this.relecture.etapes) {
      if (e.t > t) break
      if (e.mode) mode = e.mode
    }
    return mode
  }

  /** L'etape du cartouche que le joueur lisait a cet instant. */
  etapeA(t: number): string | undefined {
    let cle: string | undefined
    for (const e of this.relecture.etapes) {
      if (e.t > t) break
      cle = e.cle || undefined
    }
    return cle
  }

  private planifier(depuis?: number) {
    window.clearTimeout(this.minuteur)
    const trames = this.relecture.trames
    const suivante = trames[this.index + 1]
    if (!suivante) {
      this.enLecture = false
      this.delaiAttente = 0
      this.publierControle()
      return
    }
    this.echelleCourante = echelle(trames[this.index].t, suivante.t, this.instantsDans(trames[this.index].t, suivante.t), this.pauseMaxS * 1000)
    this.delaiAttente = this.echelleCourante.lu[this.echelleCourante.lu.length - 1] / this.vitesse
    // Reprise d'une pause entre deux trames : on repart d'ou l'on s'etait arrete.
    const dejaLu = depuis === undefined ? 0 : tempsLu(this.echelleCourante, depuis) / this.vitesse
    this.debutAttente = performance.now() - dejaLu
    this.minuteur = window.setTimeout(() => {
      this.index += 1
      this.publier()
      this.planifier()
    }, Math.max(0, this.delaiAttente - dejaLu))
  }

  private instantsDans(debut: number, fin: number): number[] {
    const tous = this.instantsEvenements
    let bas = 0
    let haut = tous.length
    while (bas < haut) {
      const milieu = (bas + haut) >> 1
      if (tous[milieu] <= debut) bas = milieu + 1
      else haut = milieu
    }
    const dedans: number[] = []
    for (let i = bas; i < tous.length && tous[i] < fin; i++) dedans.push(tous[i])
    return dedans
  }

  private calculerControle(): ControleLecture {
    return {
      index: this.index,
      total: this.relecture.trames.length,
      enLecture: this.enLecture,
      vitesse: this.vitesse,
      pauseMaxS: this.pauseMaxS,
      muet: this.muet,
      pointDeVue: this.vueAuto ? this.siegeSuivi : this.pointDeVue,
      vueAuto: this.vueAuto,
    }
  }

  private publierControle() {
    this.controle = this.calculerControle()
    for (const ecouteur of this.ecouteursControle) ecouteur()
  }

  private publier() {
    const trame = this.relecture.trames[this.index]
    const interroges = Object.keys(trame.demandes).map(Number)
    if (interroges.length > 0 && !interroges.includes(this.siegeSuivi)) this.siegeSuivi = interroges[0]
    const vue = this.vueAuto ? this.siegeSuivi : this.pointDeVue
    const joueurDemande = interroges.includes(vue) ? vue : interroges[0]
    // ⚠ `aNous` VRAI QUAND LE SIEGE AFFICHE EST INTERROGE : c'est ce qui ouvre
    // les fenetres (payer, cibler, choisir) comme le joueur les a vues. Rien
    // n'en part : `repondre` ne fait rien ici, et la vitre de la relecture
    // (vitre-spectateur.ts) arrete les clics.
    const etat: EtatMoteur = {
      monde: trame.monde,
      demande: joueurDemande === undefined ? undefined : trame.demandes[joueurDemande],
      aNous: joueurDemande !== undefined && joueurDemande === vue,
      joueurDemande,
      connecte: true,
      validationRequise: false,
      tentatives: 0,
      hautsFaits: [],
      siegesAbsents: [],
      maxTimeout: 0,
      partieId: `relecture-${this.identite}`,
      saut: this.saut,
    }
    for (const ecouteur of this.ecouteursEtat) ecouteur(etat)
    this.publierControle()
  }
}

let actif: Lecteur | undefined

declare global {
  interface Window {
    /** Le lecteur de la page de relecture, lu aussi par son cadre (cadre-joueur.ts). */
    lecteurRelecture?: Lecteur
  }
}

/** Le lecteur de la relecture : celui de cette page, ou celui de la page qui contient ce cadre. */
export function lecteurActif(): Lecteur | undefined {
  if (actif) return actif
  try {
    if (window.parent !== window) return window.parent.lecteurRelecture
  } catch {
    // Parent d'une autre origine.
  }
  return undefined
}

export function activerLecteur(lecteur: Lecteur | undefined) {
  actif?.pause()
  actif = lecteur
  window.lecteurRelecture = lecteur
}

export function estRelecture(): boolean {
  return new URLSearchParams(window.location.search).has('relecture')
}
