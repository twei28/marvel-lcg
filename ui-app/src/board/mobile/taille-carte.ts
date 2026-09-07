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
/**
 * Marge mesuree en reel (Playwright, 1050x480, tache 12, fix round 1) qui
 * couvre DEUX couts que le reste de la formule ne voit pas :
 *
 * 1. La bande de jauge PV/menace (ScanCard.css .jauge-carte) deborde SOUS le
 *    cadre via une marge basse negative (~18 px, `--jauge-epaisseur * 1.15`) :
 *    elle ne fait pas partie de la hauteur "utile" de la carte mais prend
 *    quand meme de la place reelle dans la rangee.
 * 2. HAUTEUR_BARRE (48) est la cible de conception de `.pm-barre`
 *    (medaillon.css, --pm-barre-h), mais `.pm-barre` n'a qu'un min-height :
 *    son contenu peut la pousser plus haut. Mesure sur les 34 etats de
 *    `?etat=` (aucune partie live derriere la vue) : le bandeau
 *    `.plateau-action-attente` (« Saved state. Aucune partie derriere cette
 *    vue... ») pousse la barre a 88 px, deux lignes de texte que le jeu reel
 *    n'affiche jamais (il montre une demande d'action courte). C'est un
 *    ecart de la page de fixtures elle-meme, hors perimetre de cette tache
 *    (medaillon.css et le composant qui rend ce bandeau n'y figurent pas) :
 *    cette marge absorbe le pire cas mesure plutot que de suivre un chiffre
 *    de conception que le rendu ne respecte pas toujours.
 *
 * Consequence acceptee : au plancher LARGEUR_MIN (84 px) sur les 34 etats
 * mesures, le bandeau de type deja retire (paysage.css) et le gap de
 * .scan-visuel neutralise pour les cartes posees (idem). Une fois le
 * bandeau `.plateau-action-attente` remplace par une vraie barre d'action
 * (partie live), la marge reelle necessaire sera plus proche de ~40 (jauge
 * seule + le vrai ecart HAUTEUR_BARRE) : a revisiter alors.
 */
export const MARGE_SCANCARD = 80
export const HAUTEUR_FIXE = HAUTEUR_BARRE + HAUTEUR_MAIN_VISIBLE + 2 * HAUTEUR_ETIQUETTE + MARGE_SCANCARD

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
