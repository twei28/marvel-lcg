// Où se posent les cartes qui SORTENT du deck rencontre.
//
// Deux gestes du mode « Sur la table », demandés par l'utilisateur le
// 14/09/2026 d'après la phase du méchant de play.marvelsimulator.com :
//
//   « les cartes boost sortent vraiment du paquet pour se mettre à côté, pour
//     ensuite voir à combien ; idem pour la carte d'activation, elle sort du
//     paquet et elle s'affiche, et ça j'aime vraiment bien »
//
// ⚠ AUCUN DOM ICI. Rien que de l'arithmétique sur des rectangles, pour que la
// règle se teste sans navigateur. `mesures-plateau.ts` mesure, ce fichier
// décide, le composant pose.

export type Boite = { x: number; y: number; w: number; h: number }

/** L'écart entre deux cartes posées à côté du paquet. */
export const ECART = 8

/**
 * De combien la carte rencontre grandit quand elle sort du paquet.
 *
 * ⚠ ELLE DOIT ÊTRE LUE, pas devinée : c'est tout l'intérêt du geste. À la
 * taille de la table (127 px) son texte est illisible ; à 1,7 fois elle
 * dépasse les 200 px, le seuil où le corps de texte redevient déchiffrable.
 */
export const AGRANDISSEMENT = 1.7

/**
 * Les places des cartes boost, à la suite, à DROITE du paquet.
 *
 * ⚠ ET À GAUCHE SI ELLES N'Y TIENNENT PAS. Le deck rencontre est en haut à
 * gauche de la table, donc la droite est presque toujours libre ; mais sur un
 * plateau étroit, une rangée de quatre boosts en sortirait. Mieux vaut les
 * poser du mauvais côté que hors de l'écran.
 */
export function placesDesBoosts(deck: Boite, cadre: Boite, nombre: number): Boite[] {
  if (nombre <= 0) return []
  const largeurTotale = nombre * deck.w + (nombre - 1) * ECART
  const aDroite = deck.x + deck.w + ECART
  const tientADroite = aDroite + largeurTotale <= cadre.x + cadre.w
  const depart = tientADroite ? aDroite : Math.max(cadre.x, deck.x - ECART - largeurTotale)
  return Array.from({ length: nombre }, (_, i) => ({
    x: depart + i * (deck.w + ECART),
    y: deck.y,
    w: deck.w,
    h: deck.h,
  }))
}

/**
 * La place de la carte rencontre agrandie, à côté du paquet.
 *
 * ⚠ ELLE GRANDIT VERS LE BAS ET VERS LA DROITE, jamais vers le haut : le deck
 * rencontre touche le bord supérieur de la table, et une carte centrée sur lui
 * en sortirait. Elle reste bornée au cadre dans les deux sens.
 */
export function placeDeLaRevelee(deck: Boite, cadre: Boite): Boite {
  const w = deck.w * AGRANDISSEMENT
  const h = deck.h * AGRANDISSEMENT
  const aDroite = deck.x + deck.w + ECART
  const x = aDroite + w + ECART <= cadre.x + cadre.w ? aDroite : Math.max(cadre.x + ECART, deck.x - ECART - w)
  // ⚠ LA BORNE HAUTE EN DERNIER, ET C'EST UN TEST QUI L'A DIT. Écrit dans
  // l'autre ordre, un cadre plus bas que la carte agrandie donnait un `y`
  // NÉGATIF : la carte sortait par le haut au lieu d'être simplement collée en
  // haut. Même piège que le bornage de `phase-sur-table.ts`.
  const y = Math.max(cadre.y + ECART, Math.min(deck.y, cadre.y + cadre.h - h - ECART))
  return { x, y, w, h }
}
