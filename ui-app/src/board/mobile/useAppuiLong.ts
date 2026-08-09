// L'appui long : « regarder » et « jouer » avec le meme doigt.
//
// Le geste a d'abord ete pose sur la petite carte de la main, et c'etait une
// erreur : on demandait de jouer une carte AVANT de pouvoir la lire, sur une
// vignette de 108 px ou le texte de regles est illisible. La sequence correcte
// est celle que decrit l'utilisateur :
//
//     appui court  -> la carte s'agrandit  (on LIT)
//     appui long   -> sur la carte agrandie, elle est jouee  (on DECIDE)
//
// Ce module ne connait donc qu'une chose : transformer un maintien du doigt en
// une action, et laisser le clic simple tranquille.

import { useEffect, useRef } from 'react'

/**
 * Duree d'un appui LONG, en millisecondes.
 *
 * 450 ms est le seuil habituel : assez long pour ne pas se declencher en
 * reposant le doigt, assez court pour ne pas donner l'impression que rien ne
 * repond.
 */
export const APPUI_LONG_MS = 450

export type AppuiLong = {
  /** A epandre sur l'element qui doit reagir au maintien. */
  gestes: {
    onPointerDown: () => void
    onPointerUp: () => void
    onPointerLeave: () => void
    onPointerCancel: () => void
    onContextMenu: (evenement: { preventDefault: () => void }) => void
  }
  /** Vrai si le maintien vient de declencher l'action : le clic qui suit est mort. */
  vientDeDeclencher: () => boolean
}

export function useAppuiLong(action: (() => void) | undefined): AppuiLong {
  const minuteur = useRef<number | undefined>(undefined)
  const declenche = useRef(false)
  // L'action change a chaque rendu (fermeture de couche, carte differente) :
  // la lire dans une ref evite de rearmer le minuteur pour rien.
  const derniere = useRef(action)
  derniere.current = action

  const arreter = () => {
    if (minuteur.current !== undefined) {
      window.clearTimeout(minuteur.current)
      minuteur.current = undefined
    }
  }

  // Un demontage pendant le maintien — la carte est jouee, la couche se ferme —
  // laisserait sinon un minuteur tirer dans le vide.
  useEffect(() => arreter, [])

  return {
    gestes: {
      onPointerDown: () => {
        if (!derniere.current) return
        declenche.current = false
        minuteur.current = window.setTimeout(() => {
          declenche.current = true
          derniere.current?.()
        }, APPUI_LONG_MS)
      },
      onPointerUp: arreter,
      onPointerLeave: arreter,
      onPointerCancel: arreter,
      // Le menu contextuel d'Android sur appui long volerait le geste.
      onContextMenu: (evenement) => evenement.preventDefault(),
    },
    vientDeDeclencher: () => {
      if (!declenche.current) return false
      declenche.current = false
      return true
    },
  }
}
