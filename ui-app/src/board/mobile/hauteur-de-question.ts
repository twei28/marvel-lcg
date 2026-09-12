// La hauteur de la feuille de QUESTION posee au bas de l'ecran par board.tsx
// (l'assistant d'action `.actions-flottantes`, la question du moteur
// `.demande-centrale`, l'evenement `.evenement-centrale`), pour que la main
// en feuille se pose AU-DESSUS d'elle et non dessous (mesure le 12/09/2026 :
// « x / Jouer » recouvrait la moitie des cartes a payer).
//
// Ces feuilles sont dessinees par la page, hors du plateau : on les observe
// dans le DOM (comme retour-android.ts) plutot que de cabler chaque panneau.
import { useEffect, useState } from 'react'

export const FEUILLES_DE_QUESTION = '.actions-flottantes, .demande-centrale:not(.est-en-scene), .evenement-centrale'

function mesurer(): number {
  let hauteur = 0
  for (const element of document.querySelectorAll<HTMLElement>(FEUILLES_DE_QUESTION)) {
    if (getComputedStyle(element).position !== 'fixed') continue
    const boite = element.getBoundingClientRect()
    if (boite.bottom < window.innerHeight - 4) continue
    hauteur = Math.max(hauteur, boite.height)
  }
  return Math.round(hauteur)
}

export function useHauteurDeQuestion(): number {
  const [hauteur, setHauteur] = useState(0)
  useEffect(() => {
    if (typeof MutationObserver === 'undefined') return
    let demande: number | undefined
    const rafraichir = () => {
      demande = undefined
      setHauteur(mesurer())
    }
    const planifier = () => {
      if (demande !== undefined) return
      demande = window.requestAnimationFrame(rafraichir)
    }
    const observateur = new MutationObserver(planifier)
    observateur.observe(document.body, { childList: true, subtree: true, attributes: true, attributeFilter: ['class', 'style'] })
    window.addEventListener('resize', planifier)
    planifier()
    return () => {
      observateur.disconnect()
      window.removeEventListener('resize', planifier)
      if (demande !== undefined) window.cancelAnimationFrame(demande)
    }
  }, [])
  return hauteur
}
