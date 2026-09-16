// Un faux moteur, pour monter l'ECRAN DE JEU dans un test.
//
// Pourquoi (16/09/2026). `board.tsx` fait plus de 3600 lignes et n'etait rendu
// par aucun cas : trois defauts y sont passes le 15/09, dont une barre « Vue »
// tombee dans un autre bouton sans qu'un seul cas rougisse. Le composant ouvre
// un socket des son montage — c'est ce qui le rendait intestable. Ce module
// remplace le transport, RIEN D'AUTRE : l'ecran voit exactement les memes
// trames (`EtatMoteur`) qu'en partie reelle, et ses reponses sont enregistrees
// au lieu de partir sur le reseau.
//
// ⚠ Un faux a moitie juste donnerait des cas verts qui ne prouvent rien. Donc :
// on ne simule ici AUCUNE regle de jeu. Le test pose l'etat complet qu'il veut
// voir dessine, et lit ce que l'ecran en a fait.
import type { EtatMoteur, ModePhaseMechant } from './moteur'
import type { Reponse } from './ask'

/** Une reponse partie de l'ecran : ce que le vrai moteur aurait envoye. */
export type ReponseEnvoyee = { reponse: Reponse | null; bindPlayerId: number }

/** L'etat d'ouverture : ce que l'ecran voit avant la premiere trame. */
export function etatInitial(): EtatMoteur {
  return {
    hautsFaits: [],
    siegesAbsents: [],
    maxTimeout: 0,
    aNous: false,
    connecte: false,
    validationRequise: false,
    tentatives: 0,
  }
}

export class MoteurFaux {
  /** La derniere instance construite : le test emet ses trames par elle. */
  static derniere: MoteurFaux | undefined

  readonly reponses: ReponseEnvoyee[] = []
  readonly modesPhase: ModePhaseMechant[] = []
  demarrages = 0
  arrets = 0
  continuations = 0
  reconnexions = 0
  pasAPas = 0
  activites = 0

  private ecouteur: ((etat: EtatMoteur) => void) | undefined

  constructor(readonly playerId: number) {
    MoteurFaux.derniere = this
  }

  ecouter(ecouteur: (etat: EtatMoteur) => void): () => void {
    this.ecouteur = ecouteur
    return () => {
      this.ecouteur = undefined
    }
  }

  demarrer() {
    this.demarrages += 1
  }

  arreter() {
    this.arrets += 1
  }

  async repondre(reponse: Reponse | null, bindPlayerId = this.playerId): Promise<boolean> {
    this.reponses.push({ reponse, bindPlayerId })
    return true
  }

  continuer() {
    this.continuations += 1
  }

  reconnecterMaintenant() {
    this.reconnexions += 1
  }

  setModePhaseMechant(mode: ModePhaseMechant) {
    this.modesPhase.push(mode)
  }

  avancerMaintenant() {
    this.pasAPas += 1
  }

  signalerActiviteDuJoueur() {
    this.activites += 1
  }

  /** Pousse une trame vers l'ecran, comme le vrai moteur le ferait. */
  emettre(etat: EtatMoteur) {
    this.ecouteur?.(etat)
  }
}
