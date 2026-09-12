// L'aiguillage du rendu telephone : le plateau portrait en bandes, en
// portrait comme en paysage (spec du 12/09/2026 : meme design, bandes plus
// larges quand le telephone est couche — c'est portrait.css qui le sait).
//
// Trois effets vivent ici, une seule fois par partie :
// - `body.mode-plateau-portrait`, lue par menus-mobile.css (les panneaux en
//   feuille) et par usePlacement (qui cesse de mesurer) ;
// - le Retour d'Android, qui referme la feuille du sommet au lieu de quitter
//   la partie (retour-android.ts) ; pas en vue d'etat (`?etat=`) ;
// - le plein ecran au premier tap, pas en vue d'etat.
import type { BoardProps } from '../Board'
import { useEffect } from 'react'
import { PlateauPortrait } from './PlateauPortrait'
import { demanderPleinEcran } from './plein-ecran'
import { useRetourAndroid } from './retour-android'
import './menus-mobile.css'

export function PlateauMobile(props: BoardProps) {
  useEffect(() => {
    document.body.classList.add('mode-plateau-portrait')
    return () => document.body.classList.remove('mode-plateau-portrait')
  }, [])
  useRetourAndroid(!new URLSearchParams(window.location.search).has('etat'))
  useEffect(() => {
    if (new URLSearchParams(window.location.search).has('etat')) return
    const premierTap = () => demanderPleinEcran()
    document.addEventListener('pointerdown', premierTap, { once: true })
    return () => document.removeEventListener('pointerdown', premierTap)
  }, [])
  return <PlateauPortrait {...props} />
}
