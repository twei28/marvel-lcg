// L'annonce du site, telle que le plateau la recupere.
//
// Chaine complete : l'administrateur pose l'annonce dans /admin, le site la
// range en base, le moteur la relaie sur /get_annonce (il est le seul a
// pouvoir parler au site : le navigateur est sur p<N>.<domaine> et son cookie
// ne voyagerait pas jusqu'a <domaine>), et ce module l'interroge.
//
// DEUX HORLOGES, ET C'EST LE POINT. Le site envoie les SECONDES QUI RESTENT,
// jamais une heure de fin : le navigateur d'un joueur peut avoir plusieurs
// minutes d'ecart avec le serveur, et un instant absolu lui ferait afficher un
// decompte faux. On note donc l'instant LOCAL de la reponse et on decompte a
// partir de la.
//
// Rien ici ne doit pouvoir interrompre une partie : toute erreur reseau est
// avalee, le bandeau se tait, la partie continue.

import { useEffect, useState } from 'react'

/** Ce que le moteur renvoie : un objet vide quand il n'y a rien a dire. */
export type AnnonceServeur = { texte?: string; secondes?: number }

/** Ce que le bandeau affiche. */
export type Annonce = { texte: string; secondes: number }

/** Toutes les 30 s : un preavis de dix minutes doit etre vu, pas rate de peu. */
export const PERIODE_INTERROGATION_MS = 30_000
/** Le decompte descend a la seconde, pour qu'il ne paraisse jamais fige. */
export const PERIODE_DECOMPTE_MS = 1_000
/** Le bandeau PASSE toutes les 30 s. Voir `usePassage`. */
export const PERIODE_PASSAGE_MS = 30_000
/** ...et reste deux secondes. Le temps de lire une phrase, pas davantage. */
export const DUREE_PASSAGE_MS = 2_000

export async function lireAnnonce(): Promise<Annonce | null> {
  try {
    const reponse = await fetch('/get_annonce', { cache: 'no-store' })
    if (!reponse.ok) return null
    const brut: AnnonceServeur = await reponse.json()
    const texte = (brut?.texte ?? '').trim()
    const secondes = Number(brut?.secondes ?? 0)
    if (!texte || !Number.isFinite(secondes) || secondes <= 0) return null
    return { texte, secondes }
  } catch {
    return null
  }
}

/** L'annonce en cours, decomptee, ou null quand il n'y a rien a montrer. */
export function useAnnonce(): Annonce | null {
  const [recue, setRecue] = useState<{ annonce: Annonce; a: number } | null>(null)
  const [maintenant, setMaintenant] = useState(() => Date.now())

  useEffect(() => {
    let vivant = true
    const demander = async () => {
      const annonce = await lireAnnonce()
      if (!vivant) return
      setRecue(annonce ? { annonce, a: Date.now() } : null)
    }
    void demander()
    const battement = window.setInterval(() => void demander(), PERIODE_INTERROGATION_MS)
    return () => {
      vivant = false
      window.clearInterval(battement)
    }
  }, [])

  useEffect(() => {
    if (!recue) return
    const battement = window.setInterval(() => setMaintenant(Date.now()), PERIODE_DECOMPTE_MS)
    return () => window.clearInterval(battement)
  }, [recue])

  if (!recue) return null
  const restant = recue.annonce.secondes - Math.floor((maintenant - recue.a) / 1000)
  // Echeance passee : on se tait sans attendre la prochaine interrogation.
  if (restant <= 0) return null
  return { texte: recue.annonce.texte, secondes: restant }
}

/** Le bandeau est-il visible EN CE MOMENT ?
 *
 *  ⚠ IL PASSE, IL NE S'INSTALLE PAS (demande de l'utilisateur, 13/09/2026).
 *  Deux secondes toutes les trente, et entre deux passages l'ecran de jeu est
 *  entierement libre. Une bande posee a demeure se regarde une fois puis ne se
 *  voit plus ; celle-ci revient, et c'est ce qui la fait lire.
 *
 *  Le PREMIER passage est immediat : une annonce qui arrive alors qu'on joue
 *  ne doit pas attendre trente secondes pour se montrer.
 */
export function usePassage(actif: boolean): boolean {
  const [visible, setVisible] = useState(false)

  useEffect(() => {
    if (!actif) {
      setVisible(false)
      return
    }
    let fin = 0
    const passer = () => {
      setVisible(true)
      fin = window.setTimeout(() => setVisible(false), DUREE_PASSAGE_MS)
    }
    passer()
    const battement = window.setInterval(passer, PERIODE_PASSAGE_MS)
    return () => {
      window.clearInterval(battement)
      window.clearTimeout(fin)
    }
  }, [actif])

  return visible
}
