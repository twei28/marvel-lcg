// Où poser le cartouche quand la phase du méchant se joue SUR LA TABLE.
//
// Choix de l'utilisateur, 14/09/2026, parmi trois emplacements montrés : « à
// côté de l'action », près de la carte qui vient d'agir, avec le résumé de ce
// qui s'est passé. Son argument : l'œil est déjà là, il n'a pas à aller
// chercher le bouton ailleurs. Coût accepté en connaissance de cause : le
// bouton se déplace à chaque étape, donc la souris aussi.
//
// ⚠ CE FICHIER NE TOUCHE PAS AU DOM. Il ne fait que de l'arithmétique sur des
// rectangles, pour que la règle de placement se teste sans navigateur. Le
// composant mesure, appelle, et pose le résultat.

/** Un rectangle à l'écran, dans le repère du cadre du plateau. */
export type Boite = { x: number; y: number; w: number; h: number }

/** De combien le cartouche se décolle de la carte, et des bords du plateau. */
export const MARGE = 12

export type Place = {
  x: number
  y: number
  /** De quel côté de la carte il s'est posé, pour que la flèche pointe bien. */
  cote: 'droite' | 'gauche' | 'centre'
}

/**
 * La place du cartouche à côté de la carte qui agit.
 *
 * ⚠ IL NE SORT JAMAIS DU PLATEAU. Un cartouche à moitié dehors est un bouton
 * à moitié cliquable ; on préfère un cartouche collé au bord, quitte à
 * recouvrir un voisin, à un OK qu'on ne peut pas atteindre.
 *
 * ⚠ ET IL NE RECOUVRE JAMAIS LA CARTE QUI AGIT. C'est elle qu'on regarde :
 * la cacher pour annoncer ce qu'elle vient de faire n'aurait aucun sens. D'où
 * le passage à gauche quand la droite déborde, et le repli en bas seulement
 * quand aucun des deux côtés ne tient.
 */
export function placeDuCartouche(
  carte: Boite | undefined,
  cadre: Boite,
  taille: { w: number; h: number }
): Place {
  // Sans carte (l'étape de menace n'a pas d'auteur : c'est une règle du jeu
  // qui pose la menace), le cartouche se met en bas au centre, là où il ne
  // masque ni le méchant ni la main.
  if (!carte) {
    return {
      x: cadre.x + (cadre.w - taille.w) / 2,
      y: cadre.y + cadre.h - taille.h - MARGE,
      cote: 'centre',
    }
  }

  const aDroite = carte.x + carte.w + MARGE
  const aGauche = carte.x - taille.w - MARGE
  const tientADroite = aDroite + taille.w + MARGE <= cadre.x + cadre.w
  const tientAGauche = aGauche - MARGE >= cadre.x

  const y = borner(
    carte.y + carte.h / 2 - taille.h / 2,
    cadre.y + MARGE,
    cadre.y + cadre.h - taille.h - MARGE
  )

  if (tientADroite) return { x: aDroite, y, cote: 'droite' }
  if (tientAGauche) return { x: aGauche, y, cote: 'gauche' }

  // Ni à droite ni à gauche : sous la carte, recalé dans le plateau. Le cas
  // existe sur un petit écran, où une carte large ne laisse de place nulle part.
  return {
    x: borner(
      carte.x + carte.w / 2 - taille.w / 2,
      cadre.x + MARGE,
      cadre.x + cadre.w - taille.w - MARGE
    ),
    y: borner(
      carte.y + carte.h + MARGE,
      cadre.y + MARGE,
      cadre.y + cadre.h - taille.h - MARGE
    ),
    cote: 'centre',
  }
}

/**
 * ⚠ LA BORNE BASSE GAGNE quand le plateau est plus petit que le cartouche.
 * `Math.min(max, ...)` en premier donnerait une position négative, donc un
 * cartouche sorti par le haut, exactement le défaut qu'on veut éviter.
 */
function borner(valeur: number, min: number, max: number): number {
  return Math.max(min, Math.min(max, valeur))
}
