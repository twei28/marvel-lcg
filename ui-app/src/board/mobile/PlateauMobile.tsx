// L'aiguillage du rendu telephone : le plateau en bandes. Depuis la zone 3
// de la refonte (10/10/2026), il ne sert plus qu'aux ecrans de moins de
// 768 px de large : un telephone couche plus large prend le plateau PC reduit
// (useModeMobile.ts). portrait.css garde ses bandes plus larges pour un
// petit telephone couche (667 px).
//
// Les effets qui vivent ici, une seule fois par partie :
// - `body.mode-plateau-portrait`, lue par menus-mobile.css (les panneaux en
//   feuille) et par usePlacement (qui cesse de mesurer) ;
// - le Retour d'Android, qui referme la feuille du sommet au lieu de quitter
//   la partie (retour-android.ts) ; pas en vue d'etat (`?etat=`) ;
// - le plein ecran au premier tap, pas en vue d'etat ;
// - la taille du texte (reglage a trois niveaux, `html[data-taille-texte]`) ;
// - l'installation en application (manifeste, service worker), pas en vue d'etat.
import type { BoardProps } from '../Board'
import { useEffect } from 'react'
import { PlateauPortrait } from './PlateauPortrait'
import { preparerInstallation } from './installation'
import { demanderPleinEcran } from './plein-ecran'
import { useReglagesTelephone } from './reglages-telephone'
import { useRetourAndroid } from './retour-android'
import './menus-mobile.css'
import './v2-mobile.css'

export function PlateauMobile(props: BoardProps) {
  useEffect(() => {
    document.body.classList.add('mode-plateau-portrait')
    return () => document.body.classList.remove('mode-plateau-portrait')
  }, [])
  useRetourAndroid(!new URLSearchParams(window.location.search).has('etat'))
  useEffect(() => {
    if (new URLSearchParams(window.location.search).has('etat')) return
    preparerInstallation()
    const premierTap = () => demanderPleinEcran()
    document.addEventListener('pointerdown', premierTap, { once: true })
    return () => document.removeEventListener('pointerdown', premierTap)
  }, [])
  // La taille du texte se pose sur <html> : tout le plateau est ecrit en rem.
  const { tailleTexte } = useReglagesTelephone()
  useEffect(() => {
    const racine = document.documentElement
    if (tailleTexte === 'normal') racine.removeAttribute('data-taille-texte')
    else racine.setAttribute('data-taille-texte', tailleTexte)
    return () => racine.removeAttribute('data-taille-texte')
  }, [tailleTexte])
  return <PlateauPortrait {...props} />
}
