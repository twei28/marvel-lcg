// LE CARTOUCHE SE MET A L'ECHELLE, IL NE DEFILE PLUS.
//
// ⚠ POURQUOI CE FICHIER EXISTE. Signalé en partie le 15/09/2026, capture à
// l'appui, dans une fenêtre de 1009×663 : « on doit scroll putain, je t'ai dit
// que je voulais jamais scroll ».
//
// Le cartouche du mode Détaillé portait un plafond de hauteur et
// `overflow-y: auto` : il tenait dans l'écran, mais son contenu défilait
// dedans. Mesuré sur ce cas exact, bloc par bloc : 809 px de contenu pour
// 416 px visibles.
//
// Rétrécir chaque bloc le faisait tenir à quelques pixels près, donc la
// première capacité au texte un peu long aurait redébordé. La table du plateau
// résout ce problème depuis toujours en SE METTANT A L'ECHELLE de la fenêtre
// (`--echelle`, Board.tsx). Le cartouche fait désormais pareil.
//
// Module PUR : de l'arithmétique sur des hauteurs, testable sans navigateur.

/** L'échelle minimale : en deçà, le texte n'est plus lisible et mieux vaut
 *  rogner sur la marge du bas que rendre le cartouche illisible. */
export const AJUSTEMENT_MINIMUM = 0.55

/**
 * De combien réduire le cartouche pour qu'il tienne, sans jamais l'agrandir.
 *
 * `1` quand tout tient déjà : c'est le cas de tous les grands écrans, et rien
 * n'y change.
 *
 * ⚠ ON NE DEPASSE JAMAIS 1. Agrandir un cartouche qui a de la place le ferait
 * gonfler sur les grands écrans, ce que personne n'a demandé.
 */
export function ajustementDuCartouche(naturel: number, disponible: number): number {
  if (!Number.isFinite(naturel) || naturel <= 0) return 1
  if (!Number.isFinite(disponible) || disponible <= 0) return 1
  if (naturel <= disponible) return 1
  return Math.max(AJUSTEMENT_MINIMUM, disponible / naturel)
}

/**
 * La place dont le cartouche dispose, du haut de l'écran à son bord bas.
 *
 * `bas` est la distance entre le bas de l'écran et le bas du cartouche
 * (`--bas` dans la CSS) ; `marge` est ce qu'on laisse en haut pour ne pas le
 * coller au bord.
 */
export function placeDisponible(hauteurEcran: number, bas: number, marge = 16): number {
  return Math.max(0, hauteurEcran - bas - marge)
}
