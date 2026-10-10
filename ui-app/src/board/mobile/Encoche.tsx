// L'ENCOCHE : la languette collee au bord de l'ecran qui cache la main (a
// droite, avec le nombre de cartes) ou le tiroir des piles (a gauche).
// Spec du 12/09/2026 : un tap OU un swipe vers l'interieur de l'ecran ouvre.
//
// Le swipe est lu sur l'encoche elle-meme : `pointerdown` memorise le point,
// `pointermove` de SEUIL_SWIPE px vers l'interieur declenche une fois. Le
// clic qui suit un swipe est avale, sinon le geste ouvrirait deux fois.
//
// DEPLACABLE EN HAUTEUR (02/10/2026, signalement Yarro #40 : « sur telephone le
// bouton Piles cache le REC du perso »). Un APPUI LONG saisit la languette, le
// doigt la monte ou la descend, et sa place est retenue par cote. Le tap et le
// swipe vers l'interieur restent ce qu'ils etaient.
import { useEffect, useRef, useState, type CSSProperties, type ReactElement } from 'react'

export const SEUIL_SWIPE = 24
export const APPUI_LONG_DEPLACER_MS = 450

/** Hauteur minimale de la languette (portrait.css : min-height 72 px). */
const DEMI_HAUTEUR = 36
/** Garde-fous : sous la barre du haut, au-dessus du bord bas (en part d'ecran). */
export const RATIO_MIN = 0.16
export const RATIO_MAX = 0.94

/** Part de la hauteur de l'ecran (centre de la languette), ramenee dans les bornes. */
export function bornerRatio(ratio: number): number {
  if (!Number.isFinite(ratio)) return RATIO_MAX - 0.1
  return Math.min(RATIO_MAX, Math.max(RATIO_MIN, ratio))
}

const cleStockage = (cote: 'droite' | 'gauche') => `marvel-encoche-${cote}`

function lireRatio(cote: 'droite' | 'gauche'): number | undefined {
  try {
    const brut = window.localStorage.getItem(cleStockage(cote))
    if (brut === null) return undefined
    const valeur = Number(brut)
    return Number.isFinite(valeur) ? bornerRatio(valeur) : undefined
  } catch {
    return undefined
  }
}

function ecrireRatio(cote: 'droite' | 'gauche', ratio: number): void {
  try {
    window.localStorage.setItem(cleStockage(cote), String(ratio))
  } catch {
    // Stockage indisponible : la languette reprend sa place d'origine au prochain chargement.
  }
}

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

  // Place choisie par le joueur (centre de la languette, part de la hauteur de
  // l'ecran). Absente : la place d'origine de la feuille de style.
  const [ratio, setRatio] = useState<number | undefined>(() => lireRatio(cote))
  const [enDeplacement, setEnDeplacement] = useState(false)
  // FINE ET SEMI-TRANSPARENTE AU REPOS (zone 3, 10/10/2026) : pleine opacite
  // tant que le doigt la tient. La zone tactile, elle, garde ses 44 px.
  const [touchee, setTouchee] = useState(false)
  const minuteur = useRef<number | undefined>(undefined)
  const deplace = useRef(false)
  const vientDeDeplacer = useRef(false)

  const armerFin = () => {
    if (minuteur.current !== undefined) {
      window.clearTimeout(minuteur.current)
      minuteur.current = undefined
    }
  }
  useEffect(() => armerFin, [])

  const style: CSSProperties | undefined =
    ratio === undefined
      ? undefined
      : { top: `calc(${ratio * 100}% - ${DEMI_HAUTEUR}px)`, bottom: 'auto' }

  return (
    <button
      type="button"
      className={`encoche encoche-${cote === 'droite' ? 'main' : 'piles'}${enDeplacement ? ' est-deplacee' : ''}${touchee ? ' est-touchee' : ''}`}
      data-tactile={cote === 'droite' ? 'main' : 'tiroir'}
      aria-label={libelle}
      style={style}
      onContextMenu={(evenement) => evenement.preventDefault()}
      onPointerDown={(evenement) => {
        depart.current = evenement.clientX
        setTouchee(true)
        vientDeSwiper.current = false
        deplace.current = false
        vientDeDeplacer.current = false
        const cible = evenement.currentTarget
        const identifiant = evenement.pointerId
        armerFin()
        minuteur.current = window.setTimeout(() => {
          minuteur.current = undefined
          deplace.current = true
          depart.current = undefined
          setEnDeplacement(true)
          try {
            cible.setPointerCapture(identifiant)
          } catch {
            // Capture refusee : le doigt tactile est deja capture par la languette.
          }
          if (typeof navigator.vibrate === 'function') navigator.vibrate(15)
        }, APPUI_LONG_DEPLACER_MS)
      }}
      onPointerMove={(evenement) => {
        if (deplace.current) {
          const hauteur = window.innerHeight
          if (hauteur > 0) setRatio(bornerRatio(evenement.clientY / hauteur))
          return
        }
        // Le doigt a bouge avant la fin de l'appui long : ce n'est pas un maintien.
        if (
          depart.current !== undefined &&
          Math.abs(evenement.clientX - depart.current) > 8
        ) {
          armerFin()
        }
        if (depart.current === undefined) return
        if ((evenement.clientX - depart.current) * sens >= SEUIL_SWIPE) {
          depart.current = undefined
          vientDeSwiper.current = true
          onOuvrir()
        }
      }}
      onPointerUp={() => {
        depart.current = undefined
        setTouchee(false)
        armerFin()
        if (deplace.current) {
          deplace.current = false
          vientDeDeplacer.current = true
          setEnDeplacement(false)
          if (ratio !== undefined) ecrireRatio(cote, ratio)
        }
      }}
      onPointerCancel={() => {
        depart.current = undefined
        setTouchee(false)
        armerFin()
        if (deplace.current) {
          deplace.current = false
          setEnDeplacement(false)
          if (ratio !== undefined) ecrireRatio(cote, ratio)
        }
      }}
      onClick={() => {
        if (vientDeDeplacer.current) {
          vientDeDeplacer.current = false
          return
        }
        if (vientDeSwiper.current) {
          vientDeSwiper.current = false
          return
        }
        onOuvrir()
      }}
    >
      <span className="encoche-corps">
        {nombre !== undefined ? <b className="encoche-nombre">{nombre}</b> : <span aria-hidden="true">≡</span>}
        <span className="encoche-libelle">{libelle}</span>
      </span>
    </button>
  )
}
