// LA REGLE DE L'AGRANDISSEMENT AU SURVOL, en un seul endroit.
//
// « Quand on ne survole pas une carte, rien n'apparaît » (utilisateur,
// 10 septembre 2026, capture a l'appui : un sbire d'une etape precedente
// restait affiche en grand par-dessus le bouton « Suivant », alors que le
// curseur etait dans la modale, loin de toute carte).
//
// LA CAUSE. Les panneaux qui montrent une liste de cartes posaient leur survol
// sur CHAQUE carte (`onMouseEnter` / `onMouseLeave`). Or `mouseleave` n'est
// jamais emis quand l'element DISPARAIT sous le curseur : l'etape avance, la
// scene se redessine, la carte survolee est demontee, et l'agrandissement reste
// ouvert pour toujours. Aucun evenement ne viendra plus le fermer.
//
// LA REGLE. Deux garanties, et c'est tout ce que fait ce fichier :
//
//  1. UN SEUL ECOUTEUR, sur le CONTENEUR (`onMouseOver`, qui remonte). A chaque
//     mouvement on relit ce qu'il y a sous le pointeur : une `.scan-card`, ou
//     rien. Pas de `.scan-card` sous le pointeur, pas d'agrandissement. C'est
//     deja ce que fait la table depuis toujours (`Board.tsx`, `survol`) ; ce
//     fichier l'etend aux panneaux.
//  2. L'AGRANDISSEMENT EST DERIVE DE LA LISTE, jamais recopie. On ne retient
//     qu'un identifiant ; la carte est retrouvee dans la liste courante a
//     chaque rendu. Une carte qui quitte la liste emporte donc son
//     agrandissement avec elle, sans qu'aucun evenement soit necessaire.
//
// La seconde garantie est celle qui manquait, et c'est elle qui compte : la
// premiere ne repare que les cas ou le pointeur bouge encore.

import { useCallback, useState, type MouseEvent as ReactMouseEvent } from 'react'

export type ApercuSurvol<T> = {
  /** La carte a montrer en grand, ou `undefined`. Derivee de la liste. */
  regardee: T | undefined
  /** A poser sur le CONTENEUR, pas sur les cartes. */
  survol: (evenement: ReactMouseEvent) => void
  /** A poser sur le CONTENEUR : le pointeur sort du panneau. */
  quitter: () => void
  /** Pour le clavier, ou aucun pointeur ne survole quoi que ce soit. */
  viser: (id: string | undefined) => void
}

/**
 * @param cartes la liste COURANTE des cartes du panneau, dans l'ordre du rendu.
 * @param idDe   comment lire l'identifiant d'une entree ; par defaut `.id`,
 *               qui est celui que `ScanCard` pose en `data-card-id`.
 */
export function useApercuSurvol<T>(
  cartes: readonly T[],
  idDe: (carte: T) => string | undefined = (carte) => (carte as { id?: string }).id
): ApercuSurvol<T> {
  const [id, setId] = useState<string | undefined>(undefined)

  const survol = useCallback((evenement: ReactMouseEvent) => {
    const carte = (evenement.target as HTMLElement).closest<HTMLElement>('.scan-card')
    setId(carte?.dataset.cardId ?? undefined)
  }, [])

  const quitter = useCallback(() => setId(undefined), [])
  const viser = useCallback((vise: string | undefined) => setId(vise), [])

  // ⚠ On RETROUVE la carte a chaque rendu au lieu de garder l'objet : c'est la
  // garantie 2. Garder l'objet, c'est garder une carte qui n'est plus la.
  const regardee = id === undefined ? undefined : cartes.find((carte) => idDe(carte) === id)

  return { regardee, survol, quitter, viser }
}
