// D'ou vient l'etat de partie affiche par le plateau.
//
// Deux sources, un seul type de resultat. Le plateau ne sait pas laquelle il
// regarde : il recoit un World et le dessine.
//
//   - un etat enregistre (« fixture ») : aucun serveur de jeu necessaire pour
//     travailler l'affichage, aucune partie a lancer ;
//   - la partie en cours : /get_world?p=<joueur>, en LECTURE SEULE.
//
// Les etats enregistres vivent dans le codebase du jeu, hors depot, et ne
// doivent jamais etre edites a la main. On les lit, c'est tout.

import { estMultijoueur } from './moteur'
import type { World, AssembleeExport } from './world'

const DOSSIER_ETATS = '/public/js/fixtures'

export type EntreeCatalogue = {
  fichier: string
  titre: string
  description: string
}

/**
 * Le serveur repond 200 avec une PAGE HTML a la place de la ressource demandee
 * dans deux cas : cookie de version absent (avertissement de cache) et mot de
 * passe non fourni (page d'authentification). Sans ce controle, l'erreur remonte
 * sous la forme illisible « Unexpected token < in JSON ».
 */
function pageAuLieuDeDonnees(texte: string): boolean {
  return texte.trimStart().toLowerCase().startsWith('<!doctype html')
}

async function importerModule(url: string): Promise<Record<string, unknown>> {
  const module: unknown = await import(/* @vite-ignore */ url)
  if (typeof module !== 'object' || module === null) {
    throw new Error(`${url} does not export anything usable.`)
  }
  return module as Record<string, unknown>
}

/** Liste des etats enregistres. Vide si le catalogue n'est pas joignable. */
export async function chargerCatalogueEtats(): Promise<EntreeCatalogue[]> {
  const module = await importerModule(`${DOSSIER_ETATS}/index.js`)
  const liste = module.FIXTURES ?? module.default
  if (!Array.isArray(liste)) return []
  return liste.filter(
    (entree): entree is EntreeCatalogue =>
      typeof entree === 'object' &&
      entree !== null &&
      typeof (entree as EntreeCatalogue).fichier === 'string'
  )
}

/** Un etat enregistre. C'est le contenu exact d'une reponse /get_world. */
export async function chargerEtat(fichier: string): Promise<World> {
  const module = await importerModule(`${DOSSIER_ETATS}/${fichier}`)
  const monde = module.default
  if (typeof monde !== 'object' || monde === null) {
    throw new Error(`${fichier} has no default export.`)
  }
  return monde as World
}

/** La partie en cours. Lecture seule : aucune action n'est envoyee au moteur. */
export async function chargerPartieEnCours(playerId: number): Promise<World> {
  // ⚠ LE HOT-SEAT S'ANNONCE ICI AUSSI (15/09/2026). Depuis que le moteur
  // masque les cartes qu'un client n'a pas le droit de voir, il doit savoir
  // qu'un seul ecran joue PLUSIEURS heros : sans ce drapeau, la main du second
  // heros revenait anonyme a son propre joueur. Le socket et l'accuse de
  // reception le portaient deja (`adresseSocket`, `accuserReception`) ; cette
  // route-ci, non, parce que rien n'en dependait avant.
  const siege = estMultijoueur() ? `p=${playerId}` : `hot_seat&p=${playerId}`
  const reponse = await fetch(`/get_world?${siege}`, { cache: 'no-store' })
  if (!reponse.ok) {
    throw new Error(`/get_world answered ${reponse.status}.`)
  }

  const texte = await reponse.text()
  if (pageAuLieuDeDonnees(texte)) {
    throw new Error(
      'The server returned an HTML page instead of the descriptor: missing version cookie, or password-protected server. Open the game once at its root on this same host, then reload.'
    )
  }

  const monde: unknown = JSON.parse(texte)
  if (typeof monde !== 'object' || monde === null || !Array.isArray((monde as World).players)) {
    throw new Error('/get_world did not return a game descriptor.')
  }
  return monde as World
}

/** L'etat COMMUN de l'assemblee (Kingsfall multi-tables), relu a la demande : `{}` hors assemblee. Voir `handle_get_assemblee` cote moteur. */
export async function chargerAssemblee(playerId: number): Promise<Partial<AssembleeExport>> {
  const siege = estMultijoueur() ? `p=${playerId}` : `hot_seat&p=${playerId}`
  const reponse = await fetch(`/get_assemblee?${siege}`, { cache: 'no-store' })
  if (!reponse.ok) throw new Error(`/get_assemblee answered ${reponse.status}.`)
  const texte = await reponse.text()
  if (pageAuLieuDeDonnees(texte)) throw new Error('/get_assemblee returned an HTML page.')
  return JSON.parse(texte) as Partial<AssembleeExport>
}
