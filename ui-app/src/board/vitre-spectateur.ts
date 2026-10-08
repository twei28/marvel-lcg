// LA VITRE DU SPECTATEUR ET DE LA RELECTURE (08/10/2026).
//
// Pour voir « 100 % de ce que le joueur a vu », ses fenêtres (payer, cibler,
// choisir), son menu de carte et ses boutons s'affichent tels quels. Ils ne
// doivent rien faire sous la souris de celui qui regarde : la vitre arrête
// les clics, en phase de CAPTURE, avant que le plateau ne les voie. Seules
// passent les commandes de celui qui regarde (barre de lecture, journal,
// fiche, barre du spectateur).
//
// Le moteur refuse de toute façon toute réponse d'un spectateur (403), et la
// relecture ne répond à rien : la vitre n'est pas une sécurité, c'est ce qui
// empêche un clic de déranger l'écran rejoué (ouvrir un menu, cocher une carte).

export const ZONES_LIBRES =
  '.relecture-barre, .relecture-bascule-journal, .relecture-journal, .relecture-fiche, .relecture-page, .barre-spectateur, [data-libre-spectateur]'

const EVENEMENTS = ['click', 'dblclick', 'auxclick', 'mousedown', 'mouseup', 'pointerdown', 'pointerup', 'contextmenu', 'dragstart', 'touchstart', 'keydown'] as const

/** Vrai si l'événement vise une commande de celui qui regarde. */
export function estLibre(cible: EventTarget | null): boolean {
  return cible instanceof Element && cible.closest(ZONES_LIBRES) !== null
}

/** Pose la vitre. Rend la fonction qui la retire. */
export function poserVitre(): () => void {
  const arreter = (evenement: Event) => {
    if (evenement instanceof KeyboardEvent) {
      // Le clavier de celui qui regarde est lu plus haut (fenêtre, capture) ;
      // ici, on empêche seulement les raccourcis du plateau de jouer.
      if (estLibre(evenement.target) && !(evenement.key === ' ' || evenement.key.startsWith('Arrow'))) return
      evenement.stopPropagation()
      return
    }
    if (estLibre(evenement.target)) return
    evenement.stopPropagation()
    evenement.preventDefault()
  }
  for (const nom of EVENEMENTS) document.addEventListener(nom, arreter, { capture: true, passive: false })
  return () => {
    for (const nom of EVENEMENTS) document.removeEventListener(nom, arreter, true)
  }
}
