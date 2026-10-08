// LES DÉFILEMENTS DU JOUEUR (08/10/2026) : sa main, le journal, une pile
// ouverte, une longue liste dans une fenêtre... Rejoués chez le spectateur et
// en relecture (genre « defil » de vu-partage.ts).
//
// Pas d'étiquette posée à la main sur chaque boîte qui défile (il y en a une
// vingtaine, et la prochaine serait oubliée) : une boîte se reconnaît à son
// CHEMIN de classes depuis le haut de la page. Dans le cadre du spectateur, le
// plateau a la même taille, les mêmes réglages et le même monde que chez le
// joueur : le même chemin désigne la même boîte.
import { useEffect } from 'react'
import { publierVuLimite, useVuDuJoueur } from './vu-partage'

export type Defilement = { k: string; i: number; x: number; y: number }

const PROFONDEUR = 6
const GARDES = 8

function maillon(element: Element): string {
  const classes = [...element.classList].filter((c) => !c.startsWith('est-') && !c.startsWith('a-')).sort()
  return element.tagName.toLowerCase() + classes.map((c) => `.${CSS.escape(c)}`).join('')
}

/** Le sélecteur qui désigne une boîte, et son rang parmi celles qui y répondent. */
export function cheminDe(element: Element, racine: ParentNode = document): { k: string; i: number } {
  const maillons: string[] = []
  let courant: Element | null = element
  while (courant && courant !== document.body && maillons.length < PROFONDEUR) {
    maillons.unshift(maillon(courant))
    courant = courant.parentElement
  }
  const k = maillons.join(' > ')
  const toutes = [...racine.querySelectorAll(k)]
  return { k, i: Math.max(0, toutes.indexOf(element)) }
}

function rapport(position: number, etendue: number): number {
  return etendue > 0 ? Math.round((position / etendue) * 1000) / 1000 : 0
}

/** Côté joueur : publie la position de chaque boîte qu'il fait défiler. */
export function suivreDefilements(siege: number): () => void {
  const connus = new Map<string, Defilement>()
  const surDefilement = (evenement: Event) => {
    const element = evenement.target
    if (!(element instanceof Element)) return
    const { k, i } = cheminDe(element)
    const cle = `${k}#${i}`
    connus.delete(cle)
    connus.set(cle, {
      k,
      i,
      x: rapport(element.scrollLeft, element.scrollWidth - element.clientWidth),
      y: rapport(element.scrollTop, element.scrollHeight - element.clientHeight),
    })
    while (connus.size > GARDES) connus.delete(connus.keys().next().value as string)
    publierVuLimite(siege, 'defil', [...connus.values()], 150)
  }
  document.addEventListener('scroll', surDefilement, true)
  return () => document.removeEventListener('scroll', surDefilement, true)
}

/** Remet chaque boîte à la position que le joueur lui avait donnée. */
export function appliquerDefilements(defilements: Defilement[], racine: ParentNode = document) {
  for (const d of defilements) {
    const element = racine.querySelectorAll(d.k)[d.i]
    if (!(element instanceof HTMLElement)) continue
    element.scrollLeft = d.x * (element.scrollWidth - element.clientWidth)
    element.scrollTop = d.y * (element.scrollHeight - element.clientHeight)
  }
}

/**
 * Côté spectateur : applique les défilements publiés par le siège regardé.
 * Une boîte qui s'ouvre après la valeur (une pile qu'on vient d'ouvrir) est
 * rattrapée au battement suivant.
 */
export function useDefilementsDuJoueur(siege: number | undefined) {
  const defilements = useVuDuJoueur<Defilement[]>('defil', siege)
  useEffect(() => {
    if (!defilements || defilements.length === 0) return
    appliquerDefilements(defilements)
    const rattrapage = window.setInterval(() => appliquerDefilements(defilements), 400)
    return () => window.clearInterval(rattrapage)
  }, [defilements])
}
