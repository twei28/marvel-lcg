// L'ENCOCHE : la languette collee au bord de l'ecran qui cache la main (a
// droite, avec le nombre de cartes) ou le tiroir des piles (a gauche).
// Spec du 12/09/2026 : un tap OU un swipe vers l'interieur de l'ecran ouvre.
//
// Le swipe est lu sur l'encoche elle-meme : `pointerdown` memorise le point,
// `pointermove` de SEUIL_SWIPE px vers l'interieur declenche une fois. Le
// clic qui suit un swipe est avale, sinon le geste ouvrirait deux fois.
import { useRef, type ReactElement } from 'react'

export const SEUIL_SWIPE = 24

export function Encoche({
  cote,
  libelle,
  nombre,
  onOuvrir,
}: {
  cote: 'droite' | 'gauche'
  libelle: string
  /** Le nombre affiche dans la languette (la main). */
  nombre?: number
  onOuvrir: () => void
}): ReactElement {
  const depart = useRef<number | undefined>(undefined)
  const vientDeSwiper = useRef(false)
  const sens = cote === 'droite' ? -1 : 1

  return (
    <button
      type="button"
      className={`encoche encoche-${cote === 'droite' ? 'main' : 'piles'}`}
      data-tactile={cote === 'droite' ? 'main' : 'tiroir'}
      aria-label={libelle}
      onPointerDown={(evenement) => {
        depart.current = evenement.clientX
        vientDeSwiper.current = false
      }}
      onPointerMove={(evenement) => {
        if (depart.current === undefined) return
        if ((evenement.clientX - depart.current) * sens >= SEUIL_SWIPE) {
          depart.current = undefined
          vientDeSwiper.current = true
          onOuvrir()
        }
      }}
      onPointerUp={() => {
        depart.current = undefined
      }}
      onPointerCancel={() => {
        depart.current = undefined
      }}
      onClick={() => {
        if (vientDeSwiper.current) {
          vientDeSwiper.current = false
          return
        }
        onOuvrir()
      }}
    >
      {nombre !== undefined ? <b className="encoche-nombre">{nombre}</b> : <span aria-hidden="true">≡</span>}
      <span className="encoche-libelle">{libelle}</span>
    </button>
  )
}
