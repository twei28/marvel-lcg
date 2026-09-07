// Le plateau sur un telephone : l'aiguillage entre les deux rendus.
//
// Par defaut, PlateauPaysage : deux rangees de vraies cartes, paysage
// obligatoire (spec du 07/09/2026). L'ancien modele a medaillons reste
// atteignable par `?medaillons` dans l'adresse, pour le comparer sur un vrai
// telephone jusqu'a sa suppression (sous-projet 3). Lu a chaque rendu, sans
// etat : on ne memorise rien qui puisse enfermer quelqu'un, meme regle que
// `?mobile` dans useModeMobile.ts.
//
// Il accepte exactement les BoardProps du plateau PC : c'est ce qui permet a
// board.tsx de choisir l'un ou l'autre sans rien adapter.

import type { BoardProps } from '../Board'
import { PlateauMedaillons } from './PlateauMedaillons'

export function veutLesMedaillons(recherche: string): boolean {
  return new URLSearchParams(recherche).has('medaillons')
}

export function PlateauMobile(props: BoardProps) {
  if (veutLesMedaillons(window.location.search)) return <PlateauMedaillons {...props} />
  // PlateauPaysage arrive a la tache 11 ; d'ici la, l'ancien rendu reste le seul.
  return <PlateauMedaillons {...props} />
}
