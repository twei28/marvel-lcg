// annulation.ts — le plateau sait qu'une ANNULATION vient d'avoir lieu (16/11/2026, demande de l'utilisateur : « il faut que le undo, enfin
// l'animation, soit hyper propre, là c'est pas du tout qualitatif »).
//
// Avant : l'annulation par instantané remet le monde comme avant l'action, mais le `render_id` ne recule pas. Le plateau voyait donc des
// changements ordinaires et les rejouait comme des événements : toast « Lance-toile perd 3 jetons Toile », badge « −3 », cartes qui revolent,
// lignes de journal « subit 2 dégâts » alors que rien ne s'est passé. Maintenant le moteur publie `restaurations` (un compteur qui ne fait
// qu'avancer) : un rendu qui le fait monter est une annulation, et chaque couche qui rejoue des changements s'abstient.
import { useEffect, useRef, useState } from 'react'
import type { World } from './world'
import { estResynchronisation } from './animations-en-scene'

export type Restauration = {
  /** Vrai pendant CE rendu (et, par le rejeu, les rendus qui le suivent de pres) : le monde reçu est un retour en arrière, pas un coup. */
  restauree: boolean
  /** Le `render_id` de la question retrouvée, quand `restauree`. */
  depuisRenderId?: number
  /** Le compteur du moteur (0 si absent). */
  n: number
  /** Numéro de l'ÉPISODE d'annulation (un par annulation, pas par rendu) : sert de clé à la ligne « Action annulée » du journal. */
  episode?: number
}

/**
 * Ce rendu est-il une annulation ? Pur : compare le compteur du rendu au précédent.
 * `precedent` absent = premier rendu (chargement de page, reconnexion) : jamais une annulation, même si le compteur n'est pas nul.
 */
export function estRestauration(actuel: number | undefined, precedent: number | undefined): boolean {
  if (actuel === undefined || precedent === undefined) return false
  return actuel > precedent
}

/** Après une annulation par REJEU, le moteur relance la partie : le plateau reçoit plusieurs rendus qui montent à toute allure. */
export const FENETRE_REJEU_MS = 1500
/** Après une annulation par INSTANTANÉ : la question re-posée suit de près. */
export const FENETRE_INSTANTANE_MS = 500

/**
 * Le même test, dans un composant. `restauree` est calculé PENDANT le rendu (et non dans un effet) pour que les couches du même rendu — vols
 * de cartes, toasts — le lisent tout de suite ; il reste vrai pendant une courte FENÊTRE après la détection, parce qu'un rejeu envoie plusieurs
 * rendus d'affilée et que seul le premier recule.
 */
export function useRestauration(monde: World | undefined, ignorer = false): Restauration {
  const vu = useRef<number | undefined>(undefined)
  const vuRender = useRef<number | undefined>(undefined)
  const fenetreJusqua = useRef(0)
  const episode = useRef(0)
  const depuis = useRef<number | undefined>(undefined)
  const n = monde?.restaurations ?? 0
  const renderId = monde?.render_id
  const maintenant = Date.now()
  // Deux chemins : l'INSTANTANE (le compteur du moteur monte, le render_id continue) et le REJEU (hors du tour du joueur : toute la partie est
  // relancee, le compteur repart de zero mais le render_id RECULE : voir `estResynchronisation`).
  const parInstantane = monde !== undefined && !ignorer && estRestauration(n, vu.current)
  const parRejeu = monde !== undefined && !ignorer && !parInstantane && estResynchronisation(renderId, vuRender.current)
  const detecte = parInstantane || parRejeu
  const dansLaFenetre = !ignorer && monde !== undefined && maintenant < fenetreJusqua.current
  const nouvelEpisode = detecte && !dansLaFenetre
  const numero = nouvelEpisode ? episode.current + 1 : episode.current
  const depuisCourant = nouvelEpisode ? (parInstantane ? monde?.restaure_depuis_render_id : renderId) : depuis.current
  useEffect(() => {
    if (monde) {
      vu.current = n
      vuRender.current = renderId
    }
    if (detecte) {
      fenetreJusqua.current = Date.now() + (parRejeu ? FENETRE_REJEU_MS : FENETRE_INSTANTANE_MS)
      episode.current = numero
      depuis.current = depuisCourant
    }
  }, [monde, n, renderId, detecte, parRejeu, numero, depuisCourant])
  const restauree = detecte || dansLaFenetre
  return { restauree, depuisRenderId: restauree ? depuisCourant : undefined, n, episode: restauree ? numero : undefined }
}

/** Combien de temps le bandeau « Coup annulé » reste affiché. */
export const DUREE_BANDEAU_ANNULE_MS = 1600
/** Au-delà, une demande d'annulation sans réponse du moteur est oubliée (le bandeau « Annulation… » ne reste jamais collé). */
export const DELAI_MAX_ATTENTE_MS = 8000

export type EtatBandeau = 'aucun' | 'attente' | 'annule'

/**
 * Le bandeau de retour d'annulation : « Annulation… » dès le clic (le moteur met une seconde à répondre, l'écran ne doit pas sembler figé),
 * puis « Coup annulé » quand le moteur confirme, puis plus rien.
 */
export function useBandeauAnnulation(restauree: boolean): { etat: EtatBandeau; demander: () => void } {
  const [etat, setEtat] = useState<EtatBandeau>('aucun')
  const minuteur = useRef<number | undefined>(undefined)
  const effacer = () => {
    if (minuteur.current !== undefined) window.clearTimeout(minuteur.current)
    minuteur.current = undefined
  }
  useEffect(() => effacer, [])
  useEffect(() => {
    if (!restauree) return
    effacer()
    setEtat('annule')
    minuteur.current = window.setTimeout(() => setEtat('aucun'), DUREE_BANDEAU_ANNULE_MS)
  }, [restauree])
  const demander = () => {
    effacer()
    setEtat('attente')
    minuteur.current = window.setTimeout(() => setEtat('aucun'), DELAI_MAX_ATTENTE_MS)
  }
  return { etat, demander }
}
