// Le plateau sur un telephone : l'aiguillage entre les deux rendus.
//
// Par defaut, PlateauPortrait : le telephone joue DEBOUT (spec du
// 11/09/2026), c'est ainsi qu'on le tient et c'est ce qui laisse la hauteur
// necessaire au panneau de decision en bas. Couche, EcranPaysage le dit sans
// rien demonter. L'ancien modele a medaillons reste atteignable par
// `?medaillons` dans l'adresse, pour le comparer sur un vrai telephone
// jusqu'a sa suppression (sous-projet 3). Lu a chaque rendu, sans etat : on
// ne memorise rien qui puisse enfermer quelqu'un, meme regle que `?mobile`
// dans useModeMobile.ts.
//
// Il accepte exactement les BoardProps du plateau PC : c'est ce qui permet a
// board.tsx de choisir l'un ou l'autre sans rien adapter.

import type { BoardProps } from '../Board'
import { EcranPaysage } from './EcranPaysage'
import { PlateauMedaillons } from './PlateauMedaillons'
import { PlateauPortrait } from './PlateauPortrait'
import { useOrientation } from './useOrientation'

export function veutLesMedaillons(recherche: string): boolean {
  return new URLSearchParams(recherche).has('medaillons')
}

export function PlateauMobile(props: BoardProps) {
  // useOrientation() est un hook : il doit s'executer avant tout `return`
  // conditionnel, sous peine de violer les regles des hooks React.
  const orientation = useOrientation()
  if (veutLesMedaillons(window.location.search)) return <PlateauMedaillons {...props} />
  if (orientation === 'paysage') return <EcranPaysage />
  return <PlateauPortrait {...props} />
}
