// LE TOAST D'EFFET : une phrase courte POSÉE SUR LA CARTE QUI LA SUBIT (T15, 19/10/2026).
//
// Avant : un panneau au centre de la table, sous l'intitulé « Événement de jeu »,
// qui restait 2,4 s et recouvrait la table. Constat de l'utilisateur : la phrase
// ne disait pas ce qui arrivait (voir `phrases-effets.ts`), et le panneau
// n'était pas à côté de ce dont il parlait.
//
// Position : AU-DESSUS de la carte, jamais sur son bas (les cartes de statut y
// sont posées, et le toast les cachait). Si la carte est tout en haut de
// l'écran, il se pose À CÔTÉ (à gauche, sinon à droite). Il disparaît vite.
import { useLayoutEffect, useRef, useState } from 'react'
import { createPortal } from 'react-dom'
import './ToastEffetCarte.css'

export type ToastEffet = { id: number; texte: string }

/** Le temps pendant lequel le toast reste lisible, avant de s'effacer. */
export const DUREE_TOAST_EFFET = 1250

const ECART = 8
const MARGE = 6
/** Sous la barre du haut (42 px) : le toast ne la recouvre pas. */
const MARGE_HAUT = 46

export type PositionToast = { left: number; top: number; cote: 'dessus' | 'droite' | 'gauche' }

/**
 * Où poser un toast de taille `taille` pour une carte de boîte `carte`, dans un
 * écran de `ecran`. Pure : testée sans navigateur (ToastEffetCarte.test.ts).
 */
export function placerToast(
  carte: { left: number; top: number; width: number; height: number },
  taille: { width: number; height: number },
  ecran: { width: number; height: number }
): PositionToast {
  const borner = (x: number, min: number, max: number) => Math.max(min, Math.min(x, max))
  const milieuX = carte.left + carte.width / 2
  // Au-dessus : le bas du toast touche le haut de la carte, il ne la recouvre pas.
  const topDessus = carte.top - taille.height - ECART
  if (topDessus >= MARGE_HAUT) {
    return {
      left: borner(milieuX - taille.width / 2, MARGE, ecran.width - taille.width - MARGE),
      top: topDessus,
      cote: 'dessus',
    }
  }
  // Carte tout en haut : à côté, centré sur sa hauteur. À GAUCHE d'abord (c'est
  // la marge vide de la table, la droite est celle de ses voisines), sinon à droite.
  const top = borner(carte.top + carte.height / 2 - taille.height / 2, MARGE_HAUT, ecran.height - taille.height - MARGE)
  const aGauche = carte.left - taille.width - ECART
  if (aGauche >= MARGE) return { left: aGauche, top, cote: 'gauche' }
  return { left: Math.min(carte.left + carte.width + ECART, ecran.width - taille.width - MARGE), top, cote: 'droite' }
}

/** La carte visée, telle qu'on la voit : la première copie à l'écran portant ce numéro. */
function boiteDeLaCarte(id: number): { left: number; top: number; width: number; height: number } | undefined {
  for (const element of document.querySelectorAll(`[data-card-id="${id}"]`)) {
    const r = element.getBoundingClientRect()
    if (r.width > 0 && r.height > 0) return { left: r.left, top: r.top, width: r.width, height: r.height }
  }
  return undefined
}

function UnToast({ id, texte }: ToastEffet) {
  const noeud = useRef<HTMLDivElement | null>(null)
  const [position, setPosition] = useState<PositionToast | undefined>()
  const [visible, setVisible] = useState(true)

  useLayoutEffect(() => {
    const element = noeud.current
    if (!element) return
    const boite = boiteDeLaCarte(id)
    const ecran = { width: window.innerWidth, height: window.innerHeight }
    const taille = { width: element.offsetWidth, height: element.offsetHeight }
    // Carte introuvable (hors de l'écran, dans une pile) : en haut et au milieu, discret.
    setPosition(
      boite
        ? placerToast(boite, taille, ecran)
        : { left: (ecran.width - taille.width) / 2, top: 56, cote: 'dessus' }
    )
  }, [id, texte])

  useLayoutEffect(() => {
    setVisible(true)
    const minuterie = window.setTimeout(() => setVisible(false), DUREE_TOAST_EFFET)
    return () => window.clearTimeout(minuterie)
  }, [id, texte])

  if (!visible) return null
  return (
    <div
      ref={noeud}
      className={`toast-effet-carte${position ? ` est-${position.cote}` : ''}`}
      style={position ? { left: `${position.left}px`, top: `${position.top}px` } : { visibility: 'hidden' }}
      role="status"
      data-toast-carte={id}
    >
      {texte}
    </div>
  )
}

export function ToastsEffetsCartes({ toasts }: { toasts: ToastEffet[] }) {
  if (toasts.length === 0) return null
  return createPortal(
    <div className="couche-toasts-effets" aria-live="polite">
      {toasts.map((toast) => (
        <UnToast key={`${toast.id}|${toast.texte}`} {...toast} />
      ))}
    </div>,
    document.body
  )
}
