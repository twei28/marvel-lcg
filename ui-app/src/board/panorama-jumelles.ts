// REGISTRE des cartes jumelles a illustration continue (decision du 16/10/2026).
//
// Deux cartes dont les scans se raccordent bord a bord (ex. `tl011` 14/15 et
// `tl012` 15/15, Katana de Leonardo) sont posees COTE A COTE, 14 a gauche et
// 15 a droite, a cote de la carte qui les porte (jamais glissees dessous),
// quel que soit l'ordre dans lequel le moteur les a mises en jeu. Elles restent
// deux cartes distinctes : etat, clic, cible et paiement propres a chacune.
//
// Ce sont des DONNEES, pas de la logique par carte : declarer une paire, c'est
// ajouter UNE ligne ci-dessous. Ne declarer que les paires dont l'image se
// raccorde reellement ET que l'utilisateur a confirmees une a une.
import type { WorldCard } from './world'

export type PaireJumelle = {
  /** Code de la carte dessinee a gauche (la 14). */
  gauche: string
  /** Code de la carte dessinee a droite (la 15). */
  droite: string
}

export const PAIRES_JUMELLES: readonly PaireJumelle[] = [
  { gauche: 'tl011', droite: 'tl012' }, // Katana de Leonardo (14/15 + 15/15)
  { gauche: 'tm011', droite: 'tm012' }, // Nunchuck de Michelangelo (14/15 + 15/15), confirmee le 16/10/2026
  { gauche: 'tr011', droite: 'tr012' }, // Sai de Raphael (14/15 + 15/15), confirmee le 16/10/2026
]

/** Cote ou se dessine cette carte dans son panneau, ou `undefined` si elle n'est dans aucune paire. */
export type CotePanorama = 'gauche' | 'droite'

/**
 * La premiere paire declaree dont les DEUX cartes sont dans la liste (ce que
 * porte une meme carte). Une seule des deux : `undefined`, rendu normal.
 */
export function trouverPaire(cartes: readonly WorldCard[]): { gauche: WorldCard; droite: WorldCard } | undefined {
  for (const paire of PAIRES_JUMELLES) {
    const gauche = cartes.find((c) => c.card_id === paire.gauche)
    const droite = cartes.find((c) => c.card_id === paire.droite)
    if (gauche && droite) return { gauche, droite }
  }
  return undefined
}
