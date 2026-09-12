// Le plein ecran au telephone (spec du 07/09/2026, §3 et §6.3).
//
// Le premier tap sur le plateau le demande ; le retour au menu le quitte
// avant de naviguer, sinon la page suivante s'ouvre encore en plein ecran,
// sans barre d'adresse ni bouton Retour. Un refus (navigateur, geste non
// reconnu, iOS) n'est PAS une erreur : le jeu se joue aussi bien avec la barre
// du navigateur, un peu moins haut.

type DocumentPleinEcran = Document & {
  webkitFullscreenElement?: Element | null
  webkitExitFullscreen?: () => Promise<void> | void
}

export function enPleinEcran(): boolean {
  const d = document as DocumentPleinEcran
  return Boolean(d.fullscreenElement ?? d.webkitFullscreenElement)
}

/** Demande le plein ecran, sans jamais lever : la promesse est avalee. */
export function demanderPleinEcran(): void {
  if (enPleinEcran()) return
  const racine = document.documentElement as HTMLElement & { webkitRequestFullscreen?: () => Promise<void> | void }
  const demande = racine.requestFullscreen ?? racine.webkitRequestFullscreen
  if (!demande) return
  try {
    const resultat = demande.call(racine)
    if (resultat && typeof (resultat as Promise<void>).catch === 'function') {
      ;(resultat as Promise<void>).catch(() => undefined)
    }
  } catch {
    /* refuse : on joue avec la barre du navigateur */
  }
}

/** Quitte le plein ecran s'il est actif, sans jamais lever. */
export function quitterPleinEcran(): void {
  if (!enPleinEcran()) return
  const d = document as DocumentPleinEcran
  const sortie = d.exitFullscreen ?? d.webkitExitFullscreen
  if (!sortie) return
  try {
    const resultat = sortie.call(d)
    if (resultat && typeof (resultat as Promise<void>).catch === 'function') {
      ;(resultat as Promise<void>).catch(() => undefined)
    }
  } catch {
    /* deja sorti, ou refuse : rien a faire */
  }
}
