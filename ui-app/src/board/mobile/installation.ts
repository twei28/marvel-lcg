// INSTALLER LE JEU COMME UNE APPLICATION (zone 3 de la refonte du 09/10/2026) :
// plein ecran, icone sur l'ecran d'accueil. Rien d'autre : pas de mode hors
// ligne, le service worker ne garde rien en cache.
//
// Le manifeste, les icones et le service worker sont servis par le moteur
// (`/pwa/...` et `/sw-plateau.js`, web_server.py) SANS controle de session ni
// de version : le navigateur les demande sans cookie quand il installe.
//
// Le telephone seulement : `preparerInstallation()` n'est appele que par le
// plateau en bandes. Sur PC, ni manifeste, ni service worker, ni bouton.
import { useEffect, useState } from 'react'

export const URL_MANIFESTE = '/pwa/plateau.webmanifest'
export const URL_SERVICE_WORKER = '/sw-plateau.js'

/** L'evenement que Chrome emet quand la page est installable. */
export type DemandeInstallation = Event & {
  prompt: () => Promise<void>
  userChoice: Promise<{ outcome: 'accepted' | 'dismissed' }>
}

let demandeRetenue: DemandeInstallation | undefined
const abonnes = new Set<() => void>()
let prepare = false

function prevenir(): void {
  for (const abonne of abonnes) abonne()
}

/** Deja installee et lancee depuis l'ecran d'accueil : rien a proposer. */
export function dejaInstallee(): boolean {
  try {
    return (
      window.matchMedia('(display-mode: standalone)').matches ||
      window.matchMedia('(display-mode: fullscreen)').matches
    )
  } catch {
    return false
  }
}

/**
 * Pose le lien du manifeste, enregistre le service worker et retient la
 * demande d'installation du navigateur. Une seule fois par page.
 */
export function preparerInstallation(): void {
  if (prepare || typeof document === 'undefined') return
  prepare = true
  if (!document.querySelector('link[rel="manifest"]')) {
    const lien = document.createElement('link')
    lien.rel = 'manifest'
    lien.href = URL_MANIFESTE
    document.head.append(lien)
  }
  window.addEventListener('beforeinstallprompt', (evenement) => {
    // Pas de bandeau du navigateur : le bouton discret du menu le remplace.
    evenement.preventDefault()
    demandeRetenue = evenement as DemandeInstallation
    prevenir()
  })
  window.addEventListener('appinstalled', () => {
    demandeRetenue = undefined
    prevenir()
  })
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register(URL_SERVICE_WORKER, { scope: '/' }).catch(() => undefined)
  }
}

/** Ouvre la fenetre d'installation du navigateur. Une demande ne sert qu'une fois. */
export async function installer(): Promise<boolean> {
  const demande = demandeRetenue
  if (!demande) return false
  demandeRetenue = undefined
  prevenir()
  try {
    await demande.prompt()
    const choix = await demande.userChoice
    return choix.outcome === 'accepted'
  } catch {
    return false
  }
}

/** Vrai quand le navigateur accepte d'installer le jeu maintenant. */
export function useInstallable(): boolean {
  const [oui, setOui] = useState(() => demandeRetenue !== undefined && !dejaInstallee())
  useEffect(() => {
    const suivre = () => setOui(demandeRetenue !== undefined && !dejaInstallee())
    abonnes.add(suivre)
    suivre()
    return () => {
      abonnes.delete(suivre)
    }
  }, [])
  return oui
}

/** Pour les tests : simule la demande du navigateur. */
export function retenirDemandePourTest(demande: DemandeInstallation | undefined): void {
  demandeRetenue = demande
  prevenir()
}
