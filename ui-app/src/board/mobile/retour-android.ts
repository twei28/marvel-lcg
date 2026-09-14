// Le RETOUR (Android, ou le geste de bord) ferme la feuille du sommet au lieu
// de quitter la partie (spec du 07/09/2026, §5.1).
//
// Les panneaux du plateau (Options, Historique, « … », journal, carte
// ouverte, selecteur, modales de cartes) gardent chacun leur etat, dans leur
// composant : on ne les reecrit pas. Ce module les OBSERVE dans le DOM : une
// feuille qui apparait pousse une entree d'historique, le Retour la retire et
// referme la feuille par son propre bouton, une feuille refermee a la main
// retire son entree. Le plateau ne connait aucune feuille de plus que cette
// liste ; en ajouter une, c'est une ligne ici.
import { useEffect } from 'react'

type Fermable = {
  /** L'element qui prouve que la feuille est ouverte. */
  selecteur: string
  /** Le bouton qui la referme ; a defaut, un bouton « Fermer » ou « Annuler » dedans. */
  bouton?: string
}

export const FERMABLES: readonly Fermable[] = [
  // ⚠ 14/09/2026 : `.popover-options` a disparu, les reglages sont une FENETRE
  // (board/FenetreReglages.tsx). Sans cette ligne, le Retour la laissait
  // ouverte et QUITTAIT LA PARTIE, ce que ce module existe precisement pour
  // empecher. Defaut attrape par `menus-mobile.spec.ts`.
  { selecteur: '.reglages-fond', bouton: '.reglages-fermer' },
  // `.popover-reglages` est desormais le menu « Partie » (meme classe, meme
  // bouton : seul son contenu a change).
  { selecteur: '.popover-reglages', bouton: '.bh-reglages' },
  { selecteur: '.popover-sauvegardes:not(.popover-reglages)', bouton: '.bh-save' },
  { selecteur: '.historique-panneau', bouton: '.bh-history' },
  { selecteur: '.panneau-journal', bouton: '.panneau-journal-fermer' },
  { selecteur: '.carte-ouverte-voile', bouton: '.carte-ouverte-fermer' },
  { selecteur: '.plateau-regardees-voile' },
  { selecteur: '.plateau-selecteur' },
  // Le plateau en bandes (12/09/2026) : le menu du bandeau, la main en
  // feuille, le tiroir des piles, le menu des actions d'une carte.
  { selecteur: '.portrait-menu-voile', bouton: '.portrait-menu-bouton' },
  { selecteur: '.main-feuille-voile', bouton: '.main-feuille-fermer' },
  { selecteur: '.tiroir-voile', bouton: '.tiroir-fermer' },
  { selecteur: '.menu-actions-carte' },
]

const MARQUE = 'feuilleMobile'

function feuillesOuvertes(): string[] {
  return FERMABLES.filter((f) => document.querySelector(f.selecteur) !== null).map((f) => f.selecteur)
}

/** Referme la feuille : son bouton connu, sinon un « Fermer » / « Annuler » dedans. */
export function fermerLaFeuille(selecteur: string): boolean {
  const fermable = FERMABLES.find((f) => f.selecteur === selecteur)
  const feuille = document.querySelector<HTMLElement>(selecteur)
  if (!fermable || !feuille) return false
  const bouton = fermable.bouton ? document.querySelector<HTMLElement>(fermable.bouton) : undefined
  if (bouton) {
    bouton.click()
    return true
  }
  const dedans = [...feuille.querySelectorAll<HTMLButtonElement>('button')].find((b) =>
    /^(fermer|annuler|close|cancel|×|✕)$/i.test((b.textContent ?? '').trim())
  )
  if (dedans) {
    dedans.click()
    return true
  }
  // Un voile qui se referme au toucher (les cibles depuis le menu).
  feuille.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true }))
  return true
}

/**
 * A monter une fois, sur le rendu portrait. `actif` = false ne fait rien : un
 * etat enregistre (`?etat=`) ne se joue pas, on n'y touche pas a l'historique.
 */
export function useRetourAndroid(actif: boolean): void {
  useEffect(() => {
    if (!actif) return
    // La pile des feuilles ouvertes, dans l'ordre d'apparition. Chacune a
    // pousse UNE entree d'historique.
    const ouvertes: string[] = []
    // Les popstate que NOUS provoquons (history.back() apres une fermeture a
    // la main) ne doivent pas refermer une autre feuille.
    let retoursAttendus = 0

    // SYNCHRONE, dans le rappel de l'observateur : une entree d'historique
    // poussee un tour de rendu plus tard laissait un Retour tres rapide (le
    // filet Playwright, un pouce prompt) quitter la page avant qu'elle existe.
    const synchroniser = () => {
      const maintenant = feuillesOuvertes()
      for (const s of maintenant) {
        if (!ouvertes.includes(s)) {
          ouvertes.push(s)
          window.history.pushState({ [MARQUE]: s }, '')
        }
      }
      for (const s of [...ouvertes]) {
        if (!maintenant.includes(s)) {
          ouvertes.splice(ouvertes.indexOf(s), 1)
          retoursAttendus += 1
          window.history.back()
        }
      }
    }
    const observateur = new MutationObserver(synchroniser)
    observateur.observe(document.body, { childList: true, subtree: true })

    const surRetour = () => {
      if (retoursAttendus > 0) {
        retoursAttendus -= 1
        return
      }
      const sommet = ouvertes.pop()
      if (sommet === undefined) return
      fermerLaFeuille(sommet)
    }
    window.addEventListener('popstate', surRetour)
    return () => {
      observateur.disconnect()
      window.removeEventListener('popstate', surRetour)
    }
  }, [actif])
}
