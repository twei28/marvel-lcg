// affichage.ts — le reglage « Affichage : Normal / Sobre » du plateau.
//
// Meme cle que la preparation (Fusion/marvel-lcg-src/public/js/prepare/
// affichage-choix.js) : un choix fait avant la partie suit sur le plateau, et
// inversement. Il se traduit par `data-affichage` sur <html>, que lit
// `styles/affichage-sobre.css`.

import { enVueJoueur } from './essais'

export const CLE_AFFICHAGE = 'mc_affichage_v1'

export type Affichage = 'normal' | 'sobre'

export function normaliserAffichage(valeur: unknown): Affichage {
  return valeur === 'sobre' ? 'sobre' : 'normal'
}

export function lireAffichage(): Affichage {
  try {
    return normaliserAffichage(window.localStorage.getItem(CLE_AFFICHAGE))
  } catch {
    return 'normal'
  }
}

export function appliquerAffichage(affichage: Affichage): void {
  document.documentElement.dataset.affichage = affichage
}

function envoyer(changements: Record<string, Affichage>): void {
  // Vue Player de l'administrateur : le compte n'est pas ecrit (essais.ts).
  if (enVueJoueur()) return
  try {
    void fetch('/save_preferences', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ changements }),
    }).catch(() => {})
  } catch {
    /* hors ligne : le navigateur garde le choix */
  }
}

/** Range le choix : toujours dans le navigateur, et sur le compte s'il y en a un
    (un invite recoit un refus du serveur, sans consequence). */
export function ecrireAffichage(affichage: Affichage): void {
  try {
    window.localStorage.setItem(CLE_AFFICHAGE, affichage)
  } catch {
    /* stockage indisponible : le choix ne survivra pas au rechargement */
  }
  appliquerAffichage(affichage)
  envoyer({ affichage })
}

type ReponsePreferences = {
  compte?: boolean
  existe?: boolean
  preferences?: { affichage?: unknown }
}

/**
 * Le choix du compte, s'il fait foi (meme contrat que `reconcilier` dans
 * affichage-choix.js). `undefined` : le navigateur reste la reference (invite,
 * moteur local, compte sans fichier).
 */
export function affichageDuCompte(reponse: ReponsePreferences | null | undefined): Affichage | undefined {
  if (!reponse || !reponse.compte || !reponse.existe) return undefined
  return normaliserAffichage(reponse.preferences?.affichage)
}

/** Interroge le compte au chargement du plateau. */
export async function chercherAffichageDuCompte(): Promise<Affichage | undefined> {
  if (enVueJoueur()) return undefined
  try {
    const r = await fetch('/get_preferences', { cache: 'no-store' })
    if (!r.ok) return undefined
    return affichageDuCompte((await r.json()) as ReponsePreferences)
  } catch {
    return undefined
  }
}

/**
 * Faut-il renoncer au mouvement ? Vrai sous « mouvement reduit » du systeme ET
 * en affichage sobre. Les composants qui sautent une attente quand rien ne bouge
 * (PanneauManigance, pas-a-pas...) passent par ici : l'animation coupee par la
 * feuille sobre ne doit pas laisser une attente derriere elle.
 */
export function mouvementReduit(): boolean {
  if (document.documentElement.dataset.affichage === 'sobre') return true
  return window.matchMedia('(prefers-reduced-motion: reduce)').matches
}
