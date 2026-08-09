// triche.ts — le canal du mode Bac à sable.
//
// Toutes les interventions passent par `/sandbox_command`, qui n'accepte que
// des appels `Puzzle.<methode>` : le serveur rejette tout le reste à l'analyse
// syntaxique, donc aucun code arbitraire ne circule.
//
// LES CARTES SONT VISÉES PAR IDENTIFIANT D'OBJET, jamais par nom. Le moteur
// accepte les deux (`FindOrCreateFace`), mais viser par nom a deux défauts :
// deux cartes homonymes sont indiscernables, et un nom introuvable fait
// FABRIQUER une carte détachée au lieu d'échouer — ce qui produisait des
// doublons fantômes dans l'ancienne console. L'identifiant, lui, désigne
// exactement la carte qu'on a sous les yeux.

/** Une intervention envoyée, telle qu'on la raconte dans l'historique. */
export type Intervention = {
  /** Ce qu'on lit dans le journal : « Soigne 3 sur Rhino ». */
  libelle: string
  /** Vrai si le moteur a accepté. */
  reussi: boolean
}

async function envoyer(commandes: string[]): Promise<boolean> {
  try {
    const reponse = await fetch('/sandbox_command', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ commands: commandes }),
    })
    return reponse.ok
  } catch {
    return false
  }
}

/** Échappe une chaîne pour l'insérer dans une commande Python. */
function texte(valeur: string): string {
  return `'${valeur.replace(/\\/g, '\\\\').replace(/'/g, "\\'")}'`
}

// --- Interventions sur une carte -------------------------------------------

export const soigner = (id: number, valeur: number) =>
  envoyer([`Puzzle.Heal(${id}, ${valeur})`])

export const blesser = (id: number, valeur: number) =>
  envoyer([`Puzzle.Damage(${id}, ${valeur})`])

export const redresser = (id: number) => envoyer([`Puzzle.Ready(${id})`])
export const incliner = (id: number) => envoyer([`Puzzle.Exhaust(${id})`])
export const defausser = (id: number) => envoyer([`Puzzle.Discard(${id})`])
export const retirer = (id: number) => envoyer([`Puzzle.Remove(${id})`])
export const retourner = (id: number) => envoyer([`Puzzle.Flip(${id})`])

export const rendreConfus = (id: number) => envoyer([`Puzzle.Confuse(${id})`])
export const assommer = (id: number) => envoyer([`Puzzle.Stun(${id})`])
export const rendreCoriace = (id: number) => envoyer([`Puzzle.Tough(${id})`])

export const poserMenace = (id: number, valeur: number) =>
  envoyer([`Puzzle.PlaceThreat(${id}, ${valeur})`])

export const fixerMenace = (id: number, valeur: number) =>
  envoyer([`Puzzle.SetThreat(${id}, ${valeur})`])

export const poserCompteur = (id: number, nom: string, taille: number) =>
  envoyer([`Puzzle.Counter(${id}, ${texte(nom)}, ${taille})`])

// --- Depuis les piles ------------------------------------------------------

/** Deck ou défausse du joueur -> la main. */
export const envoyerEnMain = (id: number) => envoyer([`Puzzle.Gain(${id})`])

/**
 * Pile Rencontre -> le plateau.
 *
 * `PutIntoPlay` laisse le MOTEUR décider de la destination : un sbire s'engage
 * avec le joueur, une manigance annexe se pose, une amélioration s'attache.
 * C'est le comportement voulu par défaut ; « placer ailleurs » passe par
 * `Reveal`, qui suit le cheminement normal d'une carte Rencontre révélée.
 */
export const mettreEnJeu = (id: number) => envoyer([`Puzzle.PutIntoPlay(${id})`])
export const reveler = (id: number) => envoyer([`Puzzle.Reveal(${id})`])

/** Remet une carte sur le dessus du deck du joueur. */
export const remettreDansLeDeck = (id: number) => envoyer([`Puzzle.PutIntoDeck(${id})`])
