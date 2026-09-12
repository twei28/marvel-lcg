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
import { useEffect } from 'react'
import { EcranPaysage } from './EcranPaysage'
import { PlateauMedaillons } from './PlateauMedaillons'
import { PlateauPortrait } from './PlateauPortrait'
import { useOrientation } from './useOrientation'
import { demanderPleinEcran } from './plein-ecran'
import { useRetourAndroid } from './retour-android'
import './menus-mobile.css'

export function veutLesMedaillons(recherche: string): boolean {
  return new URLSearchParams(recherche).has('medaillons')
}

export function PlateauMobile(props: BoardProps) {
  // useOrientation() est un hook : il doit s'executer avant tout `return`
  // conditionnel, sous peine de violer les regles des hooks React.
  const orientation = useOrientation()
  // La classe qui fait basculer les PANNEAUX en feuilles (menus-mobile.css,
  // spec du 07/09 §5.3) : Options, Historique, question du moteur... Posee
  // ICI, par le rendu mobile lui-meme, pour valoir aussi bien en partie que
  // sur un etat enregistre (`?etat=`). Sans elle, les panneaux gardaient leur
  // position PC : popover hors ecran, panneau flottant tronque (12/09/2026).
  useEffect(() => {
    document.body.classList.add('mode-plateau-portrait')
    return () => document.body.classList.remove('mode-plateau-portrait')
  }, [])
  // Le PREMIER tap demande le plein ecran (spec §3) : c'est le geste qui
  // l'autorise, et un refus n'est pas une erreur. Jamais sur un etat
  // enregistre (`?etat=`), qui se regarde plus qu'il ne se joue.
  // Le Retour Android referme la feuille du sommet (retour-android.ts), pas
  // sur un etat enregistre.
  useRetourAndroid(!new URLSearchParams(window.location.search).has('etat'))
  useEffect(() => {
    if (new URLSearchParams(window.location.search).has('etat')) return
    const premierTap = () => demanderPleinEcran()
    document.addEventListener('pointerdown', premierTap, { once: true })
    return () => document.removeEventListener('pointerdown', premierTap)
  }, [])
  if (veutLesMedaillons(window.location.search)) return <PlateauMedaillons {...props} />
  if (orientation === 'paysage') return <EcranPaysage />
  return <PlateauPortrait {...props} />
}
