// Le plein ecran et le verrouillage en paysage, au premier geste.
//
// Le plateau se joue en paysage (spec du 07/09/2026, §4.8). Un navigateur
// mobile ne donne le plein ecran et le verrouillage d'orientation qu'en
// reponse a un geste de l'utilisateur : on s'accroche donc au PREMIER
// pointerdown, une seule fois. Tout refus est avale : le filet, c'est
// EcranPortrait, qui couvre le plateau tant que l'appareil est en portrait.

import { useEffect } from 'react'

export function doitDemanderPleinEcran(dejaEnPleinEcran: boolean, supporte: boolean): boolean {
  return supporte && !dejaEnPleinEcran
}

export function doitMontrerEcranPortrait(orientation: 'portrait' | 'paysage'): boolean {
  return orientation === 'portrait'
}

type Verrou = { lock?: (orientation: 'landscape') => Promise<void> }

export async function demanderPleinEcranPaysage(doc: Document = document): Promise<void> {
  const racine = doc.documentElement as HTMLElement & { requestFullscreen?: () => Promise<void> }
  const supporte = typeof racine.requestFullscreen === 'function'
  if (!doitDemanderPleinEcran(Boolean(doc.fullscreenElement), supporte)) return
  try {
    await racine.requestFullscreen!()
    // Le verrouillage n'est accepte QU'EN plein ecran : d'ou l'ordre.
    const verrou = (doc.defaultView?.screen as { orientation?: Verrou } | undefined)?.orientation
    if (verrou && typeof verrou.lock === 'function') await verrou.lock('landscape')
  } catch {
    // Refus (iOS Safari, navigateur de bureau, permission) : l'ecran portrait
    // fait le travail. Rien a signaler au joueur.
  }
}

export function usePleinEcranAuPremierGeste(actif: boolean): void {
  useEffect(() => {
    if (!actif) return
    const surGeste = () => {
      void demanderPleinEcranPaysage()
    }
    document.addEventListener('pointerdown', surGeste, { once: true })
    return () => document.removeEventListener('pointerdown', surGeste)
  }, [actif])
}
