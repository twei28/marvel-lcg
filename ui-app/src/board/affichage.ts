// affichage.ts — le reglage « Affichage » du plateau : Normal, Colore, Sobre.
//
// ⚠ LES NOMS ONT CHANGE (18/10/2026, demande de l'utilisateur) SANS CHANGER LES VALEURS RANGEES :
//   valeur `epure`  -> se lit « Normal » (l'affichage de depart de tout le monde, ex-« Epure »)
//   valeur `normal` -> se lit « Colore » (couleurs du heros, halo vif, ex-« Normal »)
//   valeur `sobre`  -> se lit « Sobre » (inchange)
// Les navigateurs et les comptes qui avaient range `normal` ou `sobre` gardent donc leur choix.
//
// Meme cle que la preparation (Fusion/marvel-lcg-src/public/js/prepare/
// affichage-choix.js) : un choix fait avant la partie suit sur le plateau, et
// inversement. Il se traduit par `data-affichage` sur <html>, que lit
// `styles/affichage-sobre.css`.

import { enVueJoueur } from './essais'

export const CLE_AFFICHAGE = 'mc_affichage_v1'

export type Affichage = 'normal' | 'sobre' | 'epure'

/** L'affichage de depart : `epure`, qui se lit « Normal » (18/10/2026). */
export const AFFICHAGE_PAR_DEFAUT: Affichage = 'epure'

/** Toute valeur inconnue (absente, abimee, ancienne) vaut l'affichage de depart. */
export function normaliserAffichage(valeur: unknown): Affichage {
  return valeur === 'normal' || valeur === 'sobre' || valeur === 'epure' ? valeur : AFFICHAGE_PAR_DEFAUT
}

/**
 * PASSAGE UNIQUE AU NOUVEL AFFICHAGE (19/10/2026) : jumeau de `migrerAffichage` de la preparation
 * (public/js/prepare/affichage-choix.js), meme cle de passage, meme version. Rend vrai si le passage
 * vient d'avoir lieu dans ce navigateur : le compte porte alors encore l'ancien choix, a corriger.
 */
export const CLE_MIGRATION_AFFICHAGE = 'mc_affichage_migre'
export const VERSION_MIGRATION_AFFICHAGE = '2026-10-19'
export function migrerAffichage(stockage: Pick<Storage, 'getItem' | 'setItem'> | null | undefined): boolean {
  try {
    if (!stockage || stockage.getItem(CLE_MIGRATION_AFFICHAGE) === VERSION_MIGRATION_AFFICHAGE) return false
    stockage.setItem(CLE_AFFICHAGE, AFFICHAGE_PAR_DEFAUT)
    stockage.setItem(CLE_MIGRATION_AFFICHAGE, VERSION_MIGRATION_AFFICHAGE)
    return true
  } catch {
    return false
  }
}

// Fait AVANT toute lecture du choix range (la preparation l'a peut-etre deja fait : alors rien).
let migreAuChargement = false
try {
  migreAuChargement = migrerAffichage(globalThis.localStorage)
} catch {
  /* stockage indisponible */
}

/** Sobre ou epure : les deux coupent couleurs vives et mouvement. */
export function estSobreOuEpure(affichage: Affichage): boolean {
  return affichage !== 'normal'
}

/**
 * L'ÉPURÉ EST RÉSERVÉ AU COMPTE DE L'ADMINISTRATEUR (16/10/2026). Même mémo de
 * session que les pages (public/js/prepare/affichage-choix.js, `epurePermis`) :
 * la réponse de `/get_site_admin`, retenue dans l'onglet. Le plateau la pose lui
 * aussi, une fois `essaisOuverts` entendu (board.tsx). Un « épuré » rangé se
 * montre en sobre pour qui n'y a pas droit, sans être effacé.
 */
export const CLE_EPURE_PERMIS = 'mc_epure_permis'

/**
 * L'ÉPURÉ POUR TOUT LE MONDE (18/10/2026) : c'est l'affichage « Normal », celui de depart. Tant que ce reglage
 * est vrai, `epurePermis()` repond oui a tous ; faux, l'ancienne reserve a l'administrateur
 * (`epurePermisReserve`) reprend. Les trois affichages (Normal, Colore, Sobre) se CHOISISSENT : plus rien n'est
 * force ni cache (demande de l'utilisateur : « ils choisissent entre les trois »).
 */
let epurePourTous = true

export function reglerEpurePourTous(valeur: boolean): void {
  epurePourTous = valeur
}

export function epurePermis(): boolean {
  return epurePourTous || epurePermisReserve()
}

/** L'ancienne règle : réservé à l'administrateur (conservée, voir `epurePourTous`). */
export function epurePermisReserve(): boolean {
  try {
    if (enVueJoueur()) return false
    const hote = globalThis.location?.hostname ?? ''
    if (hote === 'localhost' || hote === '127.0.0.1' || hote === '[::1]') return true
    return globalThis.sessionStorage?.getItem(CLE_EPURE_PERMIS) === 'oui'
  } catch {
    return false
  }
}

export function retenirEpurePermis(ok: boolean): void {
  try {
    globalThis.sessionStorage?.setItem(CLE_EPURE_PERMIS, ok ? 'oui' : 'non')
  } catch {
    /* stockage indisponible : la question sera reposee */
  }
}

export function lireAffichage(): Affichage {
  try {
    const v = normaliserAffichage(window.localStorage.getItem(CLE_AFFICHAGE))
    return v === 'epure' && !epurePermis() ? 'sobre' : v
  } catch {
    return AFFICHAGE_PAR_DEFAUT
  }
}

/**
 * ⚠ L'EPURE EST UN SOBRE EN PLUS DEPOUILLE. `data-affichage` vaut `sobre` pour
 * les deux, donc toute la feuille sobre (gris, sans mouvement) et chaque test
 * `=== 'sobre'` jouent aussi en epure ; `data-epure` ajoute le reste
 * (`styles/affichage-epure.css`).
 */
export function appliquerAffichage(demande: Affichage): void {
  const affichage = demande === 'epure' && !epurePermis() ? 'sobre' : demande
  const racine = document.documentElement
  racine.dataset.affichage = affichage === 'normal' ? 'normal' : 'sobre'
  if (affichage === 'epure') racine.dataset.epure = 'oui'
  else delete racine.dataset.epure
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
  migreAuChargement = false // un choix fait par le joueur prime sur le passage unique
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
    const reponse = (await r.json()) as ReponsePreferences
    // Le passage vient d'avoir lieu ici : on corrige le compte et on garde le navigateur pour reference.
    if (migreAuChargement) {
      migreAuChargement = false
      if (reponse?.compte) envoyer({ affichage: AFFICHAGE_PAR_DEFAUT })
      return undefined
    }
    return affichageDuCompte(reponse)
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
  // L'épuré garde ses animations (16/10/2026) : seul le sobre les coupe.
  if (document.documentElement.dataset.affichage === 'sobre' && !document.documentElement.dataset.epure) return true
  return window.matchMedia('(prefers-reduced-motion: reduce)').matches
}
