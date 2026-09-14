// Mesurer où est la carte qui agit, pour poser le cartouche à côté d'elle.
//
// Le pendant DOM de `phase-sur-table.ts`, qui lui ne fait que l'arithmétique.
// Ici on mesure, là-bas on décide, et c'est là-bas que les cas se testent.
//
// ⚠ ON REMESURE À CHAQUE ÉTAPE, ET AUSSI QUAND LA FENÊTRE CHANGE. La table est
// mise à l'échelle (`--echelle`) et recentrée en permanence : une position
// retenue d'une étape à l'autre serait fausse dès le premier redimensionnement.
import { useEffect, useLayoutEffect, useState } from 'react'
import { placeDuCartouche, type Boite, type Place } from './phase-sur-table'

/** La taille supposée du cartouche tant qu'il n'a pas été mesuré. */
const TAILLE_PAR_DEFAUT = { w: 280, h: 140 }

function boiteDe(el: Element, origine: DOMRect): Boite {
  const r = el.getBoundingClientRect()
  return { x: r.left - origine.left, y: r.top - origine.top, w: r.width, h: r.height }
}

/**
 * La place du cartouche pour l'étape en cours.
 *
 * `carteId` est l'identifiant MONDE de la carte qui agit ; il est absent sur
 * les étapes qui n'ont pas d'auteur (la menace posée par la règle du jeu).
 * Rend `undefined` tant que le plateau n'est pas mesurable : le composant
 * n'affiche alors rien plutôt qu'un cartouche au mauvais endroit.
 */
export function useAncrageSurTable(
  carteId: number | undefined,
  cle: string,
  actif: boolean,
  elementCartouche: HTMLElement | null
): Place | undefined {
  const [place, setPlace] = useState<Place | undefined>(undefined)
  // ⚠ UNE SECONDE MESURE, AU REPOS. Une carte qui vient d'arriver sur la table
  // n'a pas encore sa place finale au premier rendu : elle vole encore. Ce
  // compteur relance la mesure une fois le vol fini. Un `dispatchEvent('resize')`
  // aurait fait le même effet en réveillant tous les autres écouteurs de la
  // page, pour une mesure qui ne concerne que ce cartouche.
  const [seconde, setSeconde] = useState(0)

  useLayoutEffect(() => {
    if (!actif) {
      setPlace(undefined)
      return
    }
    const mesurer = () => {
      const cadreEl = document.querySelector<HTMLElement>('.plateau-cadre')
      if (!cadreEl) return
      const origine = cadreEl.getBoundingClientRect()
      // ⚠ jsdom ne calcule aucune géométrie : tous les rectangles y valent 0.
      // Un cadre de taille nulle ne peut rien ancrer, et le composant le sait.
      if (origine.width === 0 || origine.height === 0) return
      const cadre: Boite = { x: 0, y: 0, w: origine.width, h: origine.height }
      const carteEl =
        carteId === undefined
          ? null
          : cadreEl.querySelector<HTMLElement>(`.scan-card[data-card-id="${carteId}"]`)
      const taille = elementCartouche
        ? { w: elementCartouche.offsetWidth, h: elementCartouche.offsetHeight }
        : TAILLE_PAR_DEFAUT
      setPlace(placeDuCartouche(carteEl ? boiteDe(carteEl, origine) : undefined, cadre, taille))
    }
    mesurer()
    window.addEventListener('resize', mesurer)
    return () => window.removeEventListener('resize', mesurer)
    // `cle` change à chaque étape : c'est lui qui déclenche la remesure.
  }, [carteId, cle, actif, elementCartouche, seconde])

  useEffect(() => {
    if (!actif) return
    setSeconde(0)
    const minuteur = window.setTimeout(() => setSeconde(1), 260)
    return () => window.clearTimeout(minuteur)
  }, [carteId, cle, actif])

  return place
}
