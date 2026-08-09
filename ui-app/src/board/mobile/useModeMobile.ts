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

/**
 * Sur un ORDINATEUR, on rend toujours le plateau PC — un « mobile » memorise
 * est ignore.
 *
 * C'etait l'inverse, et ca enfermait : un clic de trop sur l'option posait
 * `mobile` en localStorage, le plateau passait en bandes, et le panneau qui
 * contenait l'option devenait inatteignable. Plus aucun moyen de revenir sans
 * ouvrir la console du navigateur.
 *
 * Le reglage garde donc du sens dans un seul sens : forcer le mode PC SUR un
 * telephone (ecran etroit mais on veut la table complete). Pour eprouver le
 * rendu mobile depuis un PC, `?mobile` dans l'adresse le force — un outil de
 * developpement n'a pas besoin d'un bouton permanent.
 */
export function modeEffectif(reglage: ReglageMode, correspond: boolean): ModeRendu {
  if (!correspond) return 'pc'
  return reglage === 'pc' ? 'pc' : 'mobile'
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
  /** Vrai sur un appareil reellement mobile : conditionne l'affichage du reglage. */
  surAppareilMobile: boolean
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

  // Echappatoire de developpement : `?mobile` force le rendu telephone depuis
  // un PC. Lue a chaque rendu, sans etat : on ne memorise rien qui puisse
  // reenfermer quelqu'un.
  const forceParAdresse =
    typeof window !== 'undefined' && new URLSearchParams(window.location.search).has('mobile')

  return {
    mode: forceParAdresse ? 'mobile' : modeEffectif(reglage, correspond),
    reglage,
    surAppareilMobile: correspond,
    changer,
  }
}
