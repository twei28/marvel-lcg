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
 * Les places des cartes boost, à la suite de l'ATTAQUANT.
 *
 * ⚠ CONTRE LA CARTE QUI FRAPPE, PAS CONTRE LE PAQUET. Elles se posaient à côté
 * du deck rencontre, en haut à gauche, loin du méchant : « à côté du méchant
 * qui frappe » (choix de l'utilisateur parmi trois, 14/09/2026). On voit à qui
 * appartient ce boost, et ça vaut aussi pour un sbire. Le trajet depuis le
 * paquet reste visible, puisque c'est de là qu'elles partent.
 *
 * ⚠ ET À GAUCHE SI ELLES N'Y TIENNENT PAS. Mieux vaut les poser du mauvais
 * côté que hors de l'écran.
 *
 * `ancre` est la carte de l'attaquant ; à défaut (attaquant disparu de la
 * table) l'appelant passe le paquet, et on retrouve l'ancien comportement.
 */
export function placesDesBoosts(ancre: Boite, cadre: Boite, nombre: number): Boite[] {
  if (nombre <= 0) return []
  const w = Math.min(ancre.w, Math.max(1, (cadre.w - (nombre - 1) * ECART) / nombre))
  const h = ancre.h * w / Math.max(1, ancre.w)
  const largeurTotale = nombre * w + (nombre - 1) * ECART
  const aDroite = ancre.x + ancre.w + ECART
  const tientADroite = aDroite + largeurTotale <= cadre.x + cadre.w
  const depart = tientADroite ? aDroite : Math.max(cadre.x, ancre.x - ECART - largeurTotale)
  return Array.from({ length: nombre }, (_, i) => ({
    x: depart + i * (w + ECART),
    y: Math.max(cadre.y, Math.min(ancre.y, cadre.y + cadre.h - h)),
    w,
    h,
  }))
}

/** Les cartes lisibles au centre, avec leur orientation et sans déborder. */
export function placesDeLecture(cadre: Boite, ratios: number[]): Boite[] {
  if (!ratios.length) return []
  const marge = 24
  const ecart = 20
  const largeur = Math.max(1, cadre.w - marge * 2 - ecart * (ratios.length - 1))
  const hauteur = Math.max(1, Math.min(560, cadre.h * 0.68, cadre.h - 140))
  const h = Math.min(hauteur, largeur / ratios.reduce((s, r) => s + r, 0))
  const total = ratios.reduce((s, r) => s + r * h, 0) + ecart * (ratios.length - 1)
  let x = cadre.x + (cadre.w - total) / 2
  return ratios.map((ratio) => {
    const w = h * ratio
    const place = { x, y: cadre.y + (cadre.h - h) / 2, w, h }
    x += w + ecart
    return place
  })
}

/** Compatibilité des appelants : une carte rencontre se lit désormais au centre. */
export function placeDeLaRevelee(deck: Boite, cadre: Boite): Boite {
  return placesDeLecture(cadre, [deck.w / deck.h])[0]
}
