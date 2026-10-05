// LE CLAVIER DU CARTOUCHE DU BAS (decision D37 du 04/10/2026).
//
// Espace = Suivant (l'ecouteur de DeroulePhase le fait deja) ; chiffres 1 a 9
// = le choix qui porte ce numero, affiche « (n) » ; Echap = le refus (« Ne pas
// défendre », « Aucune réponse », « Continuer sans rien jouer »).
//
// Module PUR cote DOM : il TROUVE l'element que la touche vise, il ne clique
// pas et n'ecoute rien. C'est le controleur (DeroulePhase) qui clique, apres
// ses gardes (champ de saisie, bouton exterieur), ce qui garde un seul
// ecouteur clavier pour tout le cartouche.
//
// Convention DOM du cartouche : chaque choix cliquable porte `data-choix="n"`,
// le refus `data-refus`, le bouton qui tourne la page `data-page-suivante`.

/**
 * Un element que le joueur VOIT : ni `hidden`, ni sous un `aria-hidden`. La
 * rangee grisee sous un sous-cadre est `aria-hidden` : ses choix ne doivent pas
 * repondre a la place de ceux du sous-cadre, qui portent les memes numeros.
 */
function estVisible(element: Element): boolean {
  return element.closest('[hidden], [aria-hidden="true"]') === null
}

/**
 * L'element que la touche vise dans le cartouche, ou `undefined`.
 *
 * Un chiffre vise le choix qui porte CE numero (`data-choix`), pas le n-ieme
 * element du document : un choix indisponible garde son numero, et la touche
 * doit cliquer ce qui est ecrit a l'ecran. Les numeros vont de 1 a 9 : « 0 »
 * ne vise rien.
 */
export function cibleDeLaTouche(touche: string, racine: Element | null): HTMLElement | undefined {
  if (!racine) return undefined
  if (touche === 'Escape') {
    return [...racine.querySelectorAll<HTMLElement>('[data-refus]')].find(estVisible)
  }
  if (!/^[1-9]$/.test(touche)) return undefined
  return [...racine.querySelectorAll<HTMLElement>('[data-choix]')].find(
    (element) => element.dataset.choix === touche && estVisible(element)
  )
}

/**
 * Ce qui, ouvert par-dessus le cartouche, garde le clavier pour lui : le volet
 * du journal, les reglages, une confirmation (qui ecoute Echap en capture), le
 * menu d'une carte et son voile de cibles.
 */
export const SELECTEURS_BLOQUANTS =
  '.volet-journal, .reglages-fenetre, .confirm-voile, .menu-actions-carte, .plateau-cibles-menu-voile'

/** Vrai si une fenetre ouverte doit garder la touche : le cartouche la laisse. */
export function clavierBloque(doc: Document): boolean {
  return doc.querySelector(SELECTEURS_BLOQUANTS) !== null
}

/**
 * Le bouton qui tourne la page (decision D41 : un contenu trop long se coupe
 * en pages, « Suivant » tourne la page avant de passer a l'etape suivante),
 * s'il existe, sinon `undefined`.
 */
export function boutonPageSuivante(racine: Element | null): HTMLElement | undefined {
  return racine?.querySelector<HTMLElement>('[data-page-suivante]') ?? undefined
}
