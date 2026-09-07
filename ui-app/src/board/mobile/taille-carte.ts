// La largeur d'une carte posee, deduite de la hauteur de l'ecran.
//
// En paysage, la hauteur est la ressource rare : deux rangees de cartes, la
// main en eventail et la barre du bas doivent tenir dans 480 px (430 avec la
// barre du navigateur). La largeur de carte est donc une consequence, jamais
// une constante : celle qui remplit une rangee, entre un plancher de
// lisibilite et le plafond du plateau PC.
//
// paysage.css reproduit EXACTEMENT cette formule avec 100dvh. Cette version
// existe pour etre testee, et pour que les deux ne divergent pas sans qu'un
// test le dise.

/** La barre du bas (outils, ou demande du moteur). */
export const HAUTEUR_BARRE = 48
/** Ce que la main en eventail laisse voir au repos. */
export const HAUTEUR_MAIN_VISIBLE = 90
/** L'etiquette d'une rangee (« MECHANT », « TON HEROS »). */
export const HAUTEUR_ETIQUETTE = 14
export const HAUTEUR_FIXE = HAUTEUR_BARRE + HAUTEUR_MAIN_VISIBLE + 2 * HAUTEUR_ETIQUETTE

/** En dessous, le nom et les bulles de stats ne se lisent plus. */
export const LARGEUR_MIN = 84
/** La largeur d'une carte du plateau PC (board.css:893) : inutile d'aller au-dela. */
export const LARGEUR_MAX = 150
/** Largeur sur hauteur d'une carte a jouer. */
export const RATIO_CARTE = 63 / 88

export function hauteurRangee(hauteurFenetre: number): number {
  return (hauteurFenetre - HAUTEUR_FIXE) / 2
}

export function largeurCarte(hauteurFenetre: number): number {
  const ideale = hauteurRangee(hauteurFenetre) * RATIO_CARTE
  return Math.min(LARGEUR_MAX, Math.max(LARGEUR_MIN, ideale))
}
