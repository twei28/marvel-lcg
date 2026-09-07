// La largeur d'une carte, deduite de la hauteur disponible.
//
// En paysage, la hauteur est la ressource rare : deux rangees de cartes, la
// main en eventail et la barre du bas doivent tenir dans 480 px (430 avec la
// barre du navigateur). La largeur de carte est donc une consequence, jamais
// une constante : celle qui remplit une rangee, entre un plancher de
// lisibilite et le plafond du plateau PC.
//
// Cette formule est une ESTIMATION en hauteur d'ecran (dvh), barre du bas
// supposee a sa hauteur NOMINALE (HAUTEUR_BARRE). paysage.css la reproduit
// EXACTEMENT pour --pp-card-w, qui ne sert plus qu'a la main (elle flotte
// hors des rangees, sans boite a mesurer). Les cartes POSEES, elles, ne
// devinent rien : en CSS, elles mesurent la vraie hauteur de leur rangee via
// une unite de conteneur (100cqh sur .rangee-cartes-fenetre), quelle que
// soit la hauteur reelle que la barre prend. Cette version JS/TS existe pour
// etre testee, et pour que la main et l'estimation ne divergent pas sans
// qu'un test le dise ; elle ne peut pas, en revanche, rejouer la mesure
// reelle des cartes posees (qui n'existe qu'au rendu, dans le navigateur).

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
/** La bande de jauge PV/menace (ScanCard.css .jauge-carte) deborde SOUS le
 * cadre via une marge basse negative : mesuree dans le navigateur, elle ne
 * fait pas partie de la hauteur "utile" de la carte mais prend quand meme de
 * la place reelle dans la rangee. */
export const HAUTEUR_JAUGE = 18

export function hauteurRangee(hauteurFenetre: number): number {
  return (hauteurFenetre - HAUTEUR_FIXE) / 2
}

export function largeurCarte(hauteurFenetre: number): number {
  const ideale = (hauteurRangee(hauteurFenetre) - HAUTEUR_JAUGE) * RATIO_CARTE
  return Math.min(LARGEUR_MAX, Math.max(LARGEUR_MIN, ideale))
}
