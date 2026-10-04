// Le pas à pas : mettre en lumière ce que l'étape courante vient de faire.
//
// ⚠ DÉBRANCHÉ, à la demande de l'utilisateur : `usePasAPas` n'a plus aucun
// appelant. Le mode d'emploi du remontage est dans board.tsx, au commentaire
// qui explique pourquoi (double emploi avec le cartouche du déroulé).
//
// Le RYTHME ne vit pas ici — il est dans moteur.ts, qui retient l'accusé de
// réception (`/client_updated`) le temps qu'une étape se lise. Le moteur attend
// sans limite, c'est donc le client qui donne le tempo, et AUCUN monde n'est
// mis en tampon : ce module ne fait que décorer le rendu déjà affiché.
//
// Trois règles apprises en montant la chose :
//
// 1. ON NE RE-PARSE RIEN. `EntreeHistorique` porte déjà `cibleId`, `type` et
//    `valeur` — la variation signée du compteur, extraite une fois pour toutes
//    et dans les deux langues. Re-lire le texte du moteur à coups d'expression
//    régulière serait une deuxième vérité, vouée à diverger.
//
// 2. LE HALO SE POSE EN IMPÉRATIF, comme halo-statut.ts : classes CSS ajoutées
//    puis retirées sur l'élément réel. Passer par React ferait re-rendre le
//    plateau entier à chaque étape, pour une décoration transitoire.
//
// 3. ON NE RECENTRE QUE SI C'EST NÉCESSAIRE. Un `scrollIntoView` systématique
//    fait bouger le plateau à chaque étape même quand la carte était déjà sous
//    les yeux, ce qui donne le mal de mer et fait justement rater l'étape.

import { useEffect } from 'react'
import type { EntreeHistorique } from './HistoriquePartie'
import { mouvementReduit } from './affichage'

/** Durée du halo. Volontairement plus courte que le délai minimal d'une étape
 *  (300 ms) x 2 : le halo doit s'éteindre avant la fin de l'étape, sinon deux
 *  étapes rapides se chevauchent et on ne sait plus laquelle on regarde. */
const DUREE_HALO = 900

/** Teinte du halo par nature d'étape. Mêmes familles que le journal. */
const TEINTES: Partial<Record<EntreeHistorique['type'], string>> = {
  damage: 'degats',
  heal: 'soin',
  threat: 'menace',
  card: 'revelation',
}

function elementDeLaCarte(cibleId: number): HTMLElement | null {
  return document.querySelector<HTMLElement>(
    `.plateau-scene .scan-card[data-card-id="${cibleId}"]`
  )
}

/** Vrai quand la carte est déjà lisible à l'écran, marge comprise. */
export function estBienVisible(rect: DOMRect, hauteur: number, largeur: number): boolean {
  const margeH = hauteur * 0.1
  const margeL = largeur * 0.1
  return (
    rect.top >= margeH &&
    rect.bottom <= hauteur - margeH &&
    rect.left >= margeL &&
    rect.right <= largeur - margeL
  )
}

/** Le texte qui flotte au-dessus de la carte, ou undefined s'il n'y a rien à
 *  dire. `valeur` est signée : on garde son signe, il porte le sens. */
export function texteFlottant(entree: EntreeHistorique): string | undefined {
  if (entree.valeur === undefined || entree.valeur === 0) return undefined
  const signe = entree.valeur > 0 ? '+' : '−'
  const n = Math.abs(entree.valeur)
  if (entree.type === 'threat') return `${signe}${n} ⚠`
  if (entree.type === 'damage' || entree.type === 'heal') return `${signe}${n} ♥`
  return `${signe}${n}`
}

/**
 * Illumine la carte concernée par `entree`, et la ramène à l'écran si elle en
 * était sortie. Exporté pour le test : la logique de choix est ici, l'effet de
 * bord (classes, minuteur) reste au bout.
 */
export function montrerEtape(entree: EntreeHistorique): (() => void) | undefined {
  if (entree.cibleId === undefined) return undefined
  const teinte = TEINTES[entree.type]
  if (!teinte) return undefined

  const el = elementDeLaCarte(entree.cibleId)
  if (!el) return undefined

  const rect = el.getBoundingClientRect()
  if (!estBienVisible(rect, window.innerHeight, window.innerWidth)) {
    el.scrollIntoView({ behavior: 'smooth', block: 'center', inline: 'center' })
  }

  const classes = ['pas-a-pas-halo', `pas-a-pas-${teinte}`]
  el.classList.add(...classes)

  const texte = texteFlottant(entree)
  let bulle: HTMLElement | undefined
  if (texte) {
    bulle = document.createElement('span')
    bulle.className = `pas-a-pas-chiffre pas-a-pas-${teinte}`
    bulle.textContent = texte
    el.appendChild(bulle)
  }

  const minuteur = window.setTimeout(() => {
    el.classList.remove(...classes)
    bulle?.remove()
  }, DUREE_HALO)

  return () => {
    window.clearTimeout(minuteur)
    el.classList.remove(...classes)
    bulle?.remove()
  }
}

/**
 * Suit la dernière entrée d'historique et met en lumière sa carte.
 *
 * On s'accroche à `entrees[0]` — l'historique empile du plus récent au plus
 * ancien — et on ne réagit qu'au changement de clé : le même rendu peut être
 * republié plusieurs fois pendant qu'une question est ouverte.
 */
export function usePasAPas(entrees: EntreeHistorique[], actif: boolean): void {
  const derniere = entrees[0]
  const cle = derniere?.cle
  useEffect(() => {
    if (!actif || !derniere) return
    if (mouvementReduit()) return
    return montrerEtape(derniere)
    // `cle` suffit : une entrée est immuable, sa clé identifie le fait.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [cle, actif])
}
