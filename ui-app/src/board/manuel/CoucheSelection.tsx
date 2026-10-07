// Ce que montre et capte la multi-selection du mode manuel (selection.ts) :
// le cadre des cartes selectionnees, le rectangle trace sur une zone vide, et
// le clic simple qui vide la selection.
//
// ⚠ UN ATTRIBUT, PAS UNE CLASSE : React reecrit le `className` d'une carte des
// que son etat change (meme raison que CoucheMarques.tsx).
import { useEffect, useState } from 'react'
import { SEUIL_GLISSER } from '../glisser/useGlisser'
import { selection, useSelection } from './selection'
import './selection.css'

const ATTR = 'data-selectionnee'

/** Les cartes de la TABLE qu'on peut selectionner : ni la main, ni les piles. */
export function cartesSelectionnables(): HTMLElement[] {
  return [...document.querySelectorAll<HTMLElement>('.plateau-scene .scan-card[data-card-id]')].filter(
    (carte) => !carte.closest('.zone-main') && !carte.closest('.plateau-unite[data-pile]')
  )
}

type Boite = { gauche: number; haut: number; droite: number; bas: number }

const rectangle = (a: { x: number; y: number }, b: { x: number; y: number }): Boite => ({
  gauche: Math.min(a.x, b.x),
  haut: Math.min(a.y, b.y),
  droite: Math.max(a.x, b.x),
  bas: Math.max(a.y, b.y),
})

/** Les cartes que touche le rectangle. */
export function cartesDansLeRectangle(boite: Boite): number[] {
  const ids: number[] = []
  for (const carte of cartesSelectionnables()) {
    const r = carte.getBoundingClientRect()
    if (r.width === 0) continue
    if (r.right >= boite.gauche && r.left <= boite.droite && r.bottom >= boite.haut && r.top <= boite.bas) {
      ids.push(Number(carte.dataset.cardId))
    }
  }
  return [...new Set(ids)]
}

/** Un appui qui peut commencer un rectangle : sur la table, hors carte, hors bouton ou fenetre. */
function appuiSurLeVide(cible: EventTarget | null): boolean {
  if (!(cible instanceof Element)) return false
  if (!cible.closest('.plateau-cadre')) return false
  return !cible.closest('.scan-card, button, a, input, select, textarea, [role="menu"], [role="dialog"], .plateau-unite')
}

export function CoucheSelection() {
  const choisies = useSelection()
  const [trace, setTrace] = useState<Boite>()

  // Le cadre suit les cartes : repose a chaque image tant qu'il y a une selection.
  useEffect(() => {
    let image = 0
    const poser = () => {
      for (const carte of document.querySelectorAll<HTMLElement>(`[${ATTR}]`)) {
        if (!choisies.has(Number(carte.dataset.cardId))) carte.removeAttribute(ATTR)
      }
      for (const id of choisies) {
        for (const carte of document.querySelectorAll<HTMLElement>(`.plateau-scene .scan-card[data-card-id="${id}"]`)) {
          if (!carte.hasAttribute(ATTR)) carte.setAttribute(ATTR, '')
        }
      }
      if (choisies.size > 0) image = window.requestAnimationFrame(poser)
    }
    poser()
    return () => window.cancelAnimationFrame(image)
  }, [choisies])
  useEffect(
    () => () => {
      for (const carte of document.querySelectorAll(`[${ATTR}]`)) carte.removeAttribute(ATTR)
    },
    []
  )

  useEffect(() => {
    let depart: { x: number; y: number; ajouter: boolean } | undefined
    let trace = false
    const appui = (e: PointerEvent) => {
      depart = undefined
      trace = false
      if (e.pointerType !== 'mouse' || e.button !== 0 || e.shiftKey || e.altKey) return
      if (!appuiSurLeVide(e.target)) return
      depart = { x: e.clientX, y: e.clientY, ajouter: e.ctrlKey || e.metaKey }
    }
    const deplacement = (e: PointerEvent) => {
      if (!depart) return
      if (!trace && Math.hypot(e.clientX - depart.x, e.clientY - depart.y) < SEUIL_GLISSER) return
      trace = true
      window.getSelection()?.removeAllRanges()
      setTrace(rectangle(depart, { x: e.clientX, y: e.clientY }))
    }
    const lacher = (e: PointerEvent) => {
      const debut = depart
      depart = undefined
      if (!debut) return
      if (trace) {
        const ids = cartesDansLeRectangle(rectangle(debut, { x: e.clientX, y: e.clientY }))
        selection.remplacer(debut.ajouter ? [...selection.lire(), ...ids] : ids)
        setTrace(undefined)
        trace = false
        return
      }
      // Un clic simple sur la table vide : la selection se vide (OCTGN).
      if (!debut.ajouter) selection.vider()
    }
    // Un clic simple sur une carte NON selectionnee vide aussi la selection.
    const clicCarte = (e: PointerEvent) => {
      if (e.pointerType !== 'mouse' || e.button !== 0 || e.ctrlKey || e.metaKey || e.shiftKey || e.altKey) return
      const carte = e.target instanceof Element ? e.target.closest<HTMLElement>('.plateau-scene .scan-card[data-card-id]') : null
      if (carte && !selection.contient(Number(carte.dataset.cardId))) selection.vider()
    }
    const annuler = () => {
      depart = undefined
      trace = false
      setTrace(undefined)
    }
    document.addEventListener('pointerdown', appui)
    document.addEventListener('pointerdown', clicCarte)
    document.addEventListener('pointermove', deplacement)
    document.addEventListener('pointerup', lacher)
    document.addEventListener('pointercancel', annuler)
    return () => {
      document.removeEventListener('pointerdown', appui)
      document.removeEventListener('pointerdown', clicCarte)
      document.removeEventListener('pointermove', deplacement)
      document.removeEventListener('pointerup', lacher)
      document.removeEventListener('pointercancel', annuler)
      selection.vider()
    }
  }, [])

  return trace ? (
    <div
      className="selection-rectangle"
      aria-hidden="true"
      style={{ left: trace.gauche, top: trace.haut, width: trace.droite - trace.gauche, height: trace.bas - trace.haut }}
    />
  ) : null
}
