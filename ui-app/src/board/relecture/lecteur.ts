// Le « moteur » de la relecture : il pousse au plateau les mondes enregistres,
// avec la meme interface que `Moteur` (usePartieEnCours n'y voit que du feu),
// et pilote la lecture (pause, pas a pas, vitesse, saut).
import type { EtatMoteur, ModePhaseMechant } from '../moteur'
import type { Reponse } from '../ask'
import type { Relecture } from './fichier'

export const PAUSE_MAX_DEFAUT_S = 5
export const VITESSES = [0.5, 1, 2, 4] as const

export type Repere = { index: number; genre: 'round' | 'phase-mechant' | 'vaincu'; libelle: string }

export type ControleLecture = {
  index: number
  total: number
  enLecture: boolean
  vitesse: number
  pauseMaxS: number
  muet: boolean
  pointDeVue: number
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
  private saut = false
  private minuteur: number | undefined
  private debutAttente = 0
  private delaiAttente = 0
  private ecouteursEtat = new Set<(etat: EtatMoteur) => void>()
  private ecouteursControle = new Set<() => void>()
  private controle: ControleLecture

  constructor(readonly relecture: Relecture, readonly identite: string) {
    this.reperes = reperesDe(relecture)
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
    this.publier()
    this.saut = false
    if (this.enLecture) this.planifier()
  }
  suivant() {
    this.pause()
    this.aller(this.index + 1)
  }
  precedent() {
    this.pause()
    this.aller(this.index - 1)
  }
  lecture() {
    if (this.index >= this.relecture.trames.length - 1) {
      this.index = 0
      this.saut = true
      this.publier()
      this.saut = false
    }
    this.enLecture = true
    this.planifier()
    this.publierControle()
  }
  pause() {
    this.enLecture = false
    window.clearTimeout(this.minuteur)
    this.publierControle()
  }
  basculerLecture() {
    if (this.enLecture) this.pause()
    else this.lecture()
  }
  reglerVitesse(vitesse: number) {
    this.vitesse = vitesse
    if (this.enLecture) this.planifier()
    this.publierControle()
  }
  reglerPauseMax(secondes: number) {
    this.pauseMaxS = Math.max(0.5, secondes)
    if (this.enLecture) this.planifier()
    this.publierControle()
  }
  basculerMuet() {
    this.muet = !this.muet
    this.publierControle()
  }
  reglerPointDeVue(siege: number) {
    this.pointDeVue = siege
    this.publier()
  }

  /** Le temps enregistre « en cours », entre deux trames pendant l'attente : curseurs et etapes s'y calent. */
  tempsCourant(): number {
    const trames = this.relecture.trames
    const ici = trames[this.index].t
    const suivante = trames[this.index + 1]
    if (!this.enLecture || !suivante || this.delaiAttente <= 0) return ici
    const part = Math.min(1, (performance.now() - this.debutAttente) / this.delaiAttente)
    return ici + part * (suivante.t - ici)
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

  /** L'etape du cartouche que le joueur lisait a cet instant. */
  etapeA(t: number): string | undefined {
    let cle: string | undefined
    for (const e of this.relecture.etapes) {
      if (e.t > t) break
      cle = e.cle || undefined
    }
    return cle
  }

  private planifier() {
    window.clearTimeout(this.minuteur)
    const trames = this.relecture.trames
    const suivante = trames[this.index + 1]
    if (!suivante) {
      this.enLecture = false
      this.delaiAttente = 0
      this.publierControle()
      return
    }
    const ecart = Math.max(0, suivante.t - trames[this.index].t)
    this.delaiAttente = Math.min(ecart, this.pauseMaxS * 1000) / this.vitesse
    this.debutAttente = performance.now()
    this.minuteur = window.setTimeout(() => {
      this.index += 1
      this.publier()
      this.planifier()
    }, this.delaiAttente)
  }

  private calculerControle(): ControleLecture {
    return {
      index: this.index,
      total: this.relecture.trames.length,
      enLecture: this.enLecture,
      vitesse: this.vitesse,
      pauseMaxS: this.pauseMaxS,
      muet: this.muet,
      pointDeVue: this.pointDeVue,
    }
  }

  private publierControle() {
    this.controle = this.calculerControle()
    for (const ecouteur of this.ecouteursControle) ecouteur()
  }

  private publier() {
    const trame = this.relecture.trames[this.index]
    const interroges = Object.keys(trame.demandes).map(Number)
    const joueurDemande = interroges.includes(this.pointDeVue) ? this.pointDeVue : interroges[0]
    const etat: EtatMoteur = {
      monde: trame.monde,
      demande: joueurDemande === undefined ? undefined : trame.demandes[joueurDemande],
      aNous: false,
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

export function lecteurActif(): Lecteur | undefined {
  return actif
}

export function activerLecteur(lecteur: Lecteur | undefined) {
  actif?.pause()
  actif = lecteur
}

export function estRelecture(): boolean {
  return new URLSearchParams(window.location.search).has('relecture')
}
