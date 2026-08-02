// Le plateau se dessine-t-il en mode mobile ou en mode PC ?
//
// La decision est prise en JavaScript, pas en CSS : ce n'est pas une question
// d'apparence mais de composant a monter. Le reglage a trois etats permet de
// tester le mode mobile depuis un PC, et de repasser en mode PC sur une tablette.
//
// La memorisation suit le modele de la bascule ?ui=old : localStorage, jamais
// l'adresse (le lancement d'une partie efface toute query string) et jamais un
// cookie (le serveur en pose deja deux).

import { useEffect, useState } from 'react'

export type ReglageMode = 'auto' | 'mobile' | 'pc'
export type ModeRendu = 'mobile' | 'pc'

export const CLE_MODE = 'mode-plateau'

/** Un ecran etroit OU un pointeur grossier suffit : la virgule est un OU en CSS. */
export const REQUETE_MOBILE = '(max-width: 900px), (pointer: coarse)'

export function modeEffectif(reglage: ReglageMode, correspond: boolean): ModeRendu {
  if (reglage === 'mobile') return 'mobile'
  if (reglage === 'pc') return 'pc'
  return correspond ? 'mobile' : 'pc'
}

export function lireReglage(): ReglageMode {
  try {
    const valeur = window.localStorage.getItem(CLE_MODE)
    return valeur === 'mobile' || valeur === 'pc' ? valeur : 'auto'
  } catch {
    return 'auto'
  }
}

export function ecrireReglage(reglage: ReglageMode): void {
  try {
    window.localStorage.setItem(CLE_MODE, reglage)
  } catch {
    // Navigation privee, quota plein : le reglage ne survit pas, le jeu si.
  }
}

export function useModeMobile(): {
  mode: ModeRendu
  reglage: ReglageMode
  changer: (reglage: ReglageMode) => void
} {
  const [reglage, setReglage] = useState<ReglageMode>(lireReglage)
  const [correspond, setCorrespond] = useState(
    () => window.matchMedia(REQUETE_MOBILE).matches
  )

  useEffect(() => {
    const liste = window.matchMedia(REQUETE_MOBILE)
    const surChangement = (evenement: MediaQueryListEvent) => setCorrespond(evenement.matches)
    liste.addEventListener('change', surChangement)
    return () => liste.removeEventListener('change', surChangement)
  }, [])

  const changer = (suivant: ReglageMode) => {
    ecrireReglage(suivant)
    setReglage(suivant)
  }

  return { mode: modeEffectif(reglage, correspond), reglage, changer }
}
