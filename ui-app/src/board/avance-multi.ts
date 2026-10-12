// QUI FAIT AVANCER LA PHASE DU MECHANT EN MULTI (refonte, lot 6, 12/10/2026).
//
// Decisions 10, 32 et 33 : les autres joueurs voient le MEME ecran, au meme
// rythme, sans bouton ; a la premiere phase du mechant l'hote choisit qui fait
// avancer, pour toute la partie, et peut changer d'avis dans les reglages :
//  - « concerne »  : le joueur concerne par l'etape (celui que l'ennemi vise,
//                    celui qui revele), le premier joueur pour les moments communs ;
//  - « tous »      : chacun se dit pret, on avance quand tout le monde l'est ;
//  - « quiconque » : le premier qui clique fait avancer tout le monde.
// Le serveur garde le choix (/set_avance_phase, /get_avance_phase) et l'etape
// que chacun lit, ses boosts retournes et sa cle « pret » (/set_etape).
import { useEffect, useState } from 'react'
import type { EtapesLues } from './etape-partagee'

export type PolitiqueAvance = 'concerne' | 'tous' | 'quiconque'

export const POLITIQUES: readonly PolitiqueAvance[] = ['concerne', 'tous', 'quiconque']

export function lirePolitique(brut: unknown): PolitiqueAvance | undefined {
  return typeof brut === 'string' && (POLITIQUES as readonly string[]).includes(brut)
    ? (brut as PolitiqueAvance)
    : undefined
}

/** Le siege qui donne le rythme en « concerne » : le joueur concerne, sinon le premier joueur. */
export function siegeMeneur(siegeConcerne: number | undefined, premierJoueur: number | undefined): number | undefined {
  return siegeConcerne ?? premierJoueur
}

/** Ce joueur-ci peut-il faire avancer l'etape ? */
export function peutAvancer(
  politique: PolitiqueAvance | undefined,
  siegeLocal: number | undefined,
  siegeConcerne: number | undefined,
  premierJoueur: number | undefined
): boolean {
  if (politique === undefined) return false
  if (politique !== 'concerne') return true
  const meneur = siegeMeneur(siegeConcerne, premierJoueur)
  // Meneur inconnu (monde sans jeton) : personne n'est bloque, plutot qu'une phase figee.
  return meneur === undefined || meneur === siegeLocal
}

export type Lecture = { siege: number; cle: string; boosts: number; t: number; valide: string }

function lectureDe(etapes: EtapesLues, siege: string): Lecture | undefined {
  const brut = etapes[siege] as (EtapesLues[string] & { boosts?: number; valide?: string }) | undefined
  if (!brut) return undefined
  return {
    siege: Number(siege),
    cle: brut.cle ?? '',
    boosts: Number(brut.boosts ?? 0) || 0,
    t: Number(brut.t) || 0,
    valide: brut.valide ?? '',
  }
}

/**
 * L'etape que ce joueur doit suivre, ou rien s'il donne lui-meme le rythme :
 * en « concerne », celle du meneur ; en « quiconque », celle du dernier qui a
 * clique (si c'est un autre). En « tous », personne ne suit : on avance
 * ensemble quand tout le monde est pret (`tousPrets`).
 */
export function lectureASuivre(
  politique: PolitiqueAvance | undefined,
  etapes: EtapesLues,
  siegeLocal: number | undefined,
  meneur: number | undefined
): Lecture | undefined {
  if (politique === 'concerne') {
    if (meneur === undefined || meneur === siegeLocal) return undefined
    return lectureDe(etapes, String(meneur))
  }
  if (politique === 'quiconque') {
    // Le plus recent des AUTRES : si nous avons republie apres son clic (memes
    // cle, heure plus recente), il reste celui qu'on suit ; on ne suit de toute
    // facon que ce qui est en avance sur nous.
    let recente: Lecture | undefined
    for (const siege of Object.keys(etapes)) {
      const lecture = lectureDe(etapes, siege)
      if (lecture && lecture.siege !== siegeLocal && (!recente || lecture.t > recente.t)) recente = lecture
    }
    return recente
  }
  return undefined
}

/** Les sieges qui se sont dits prets pour CETTE etape. */
export function siegesPrets(etapes: EtapesLues, cle: string | undefined, sieges: readonly number[]): number[] {
  if (!cle) return []
  return sieges.filter((siege) => {
    const brut = etapes[String(siege)] as (EtapesLues[string] & { pret?: string }) | undefined
    return brut?.pret === cle
  })
}

/** Tout le monde est pret : on peut avancer (« tous »). */
export function tousPrets(etapes: EtapesLues, cle: string | undefined, sieges: readonly number[]): boolean {
  return sieges.length > 0 && siegesPrets(etapes, cle, sieges).length === sieges.length
}

export const DELAI_LECTURE_AVANCE_MS = 700

/** Le choix de l'hote et les etapes lues par chacun, relus toutes les 700 ms. */
export function useAvanceMulti(actif: boolean): { politique: PolitiqueAvance | undefined; etapes: EtapesLues; charge: boolean } {
  const [etat, setEtat] = useState<{ politique: PolitiqueAvance | undefined; etapes: EtapesLues; charge: boolean }>({
    politique: undefined,
    etapes: {},
    charge: false,
  })
  useEffect(() => {
    if (!actif) return
    let vivant = true
    const lire = () =>
      Promise.all([
        fetch('/get_avance_phase', { cache: 'no-store' }).then((r) => (r.ok ? r.json() : {})),
        fetch('/get_etapes', { cache: 'no-store' }).then((r) => (r.ok ? r.json() : {})),
      ])
        .then(([avance, etapes]: [{ politique?: string }, EtapesLues]) => {
          if (!vivant) return
          setEtat({ politique: lirePolitique(avance?.politique), etapes: etapes ?? {}, charge: true })
        })
        .catch(() => undefined)
    void lire()
    const minuteur = window.setInterval(() => void lire(), DELAI_LECTURE_AVANCE_MS)
    return () => {
      vivant = false
      window.clearInterval(minuteur)
    }
  }, [actif])
  return etat
}

/** L'hote pose (ou change) la regle pour toute la partie. */
export function choisirPolitique(siege: number, politique: PolitiqueAvance): Promise<boolean> {
  return fetch('/set_avance_phase', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ p: siege, politique }),
  })
    .then((r) => r.ok)
    .catch(() => false)
}
