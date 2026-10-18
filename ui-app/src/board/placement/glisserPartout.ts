/**
 * Glisser une fenetre de PARTOUT, pas seulement par sa poignee (demande de l'utilisateur, 18/10/2026 :
 * « qu'on puisse bouger les fenetres de partout, sauf depuis les boutons »).
 *
 * Sans toucher aux ~25 fenetres : un seul ecouteur sur le document. Quand on appuie dans une fenetre, hors d'un
 * element qui a son propre role (bouton, carte, champ, zone qui defile), on rejoue l'appui sur la poignee de
 * cette fenetre : c'est elle, via `useGlisserPanneau`, qui suit ensuite le pointeur. Un simple clic ne deplace
 * rien (seuil de 6 px dans le hook).
 *
 * La poignee est retrouvee par la marque que `useGlisserPanneau` pose sur son `onPointerDown`, lue dans les
 * proprietes React de l'element (`__reactProps$...`).
 */
import { MARQUE_GESTE } from './useGlisserPanneau'

/** Ce qui garde son role au clic : on ne glisse jamais depuis ces elements. */
export const INTERACTIFS =
  'button, a, input, select, textarea, label, summary, [role="button"], [role="slider"], [role="checkbox"], ' +
  '[role="switch"], [role="tab"], [contenteditable="true"], .scan-card, [data-choix], [data-refus], .af-action'

function proprietesReact(element: Element): Record<string, unknown> | undefined {
  const cle = Object.keys(element).find((k) => k.startsWith('__reactProps$'))
  return cle ? ((element as unknown as Record<string, Record<string, unknown>>)[cle] ?? undefined) : undefined
}

/** L'element de `racine` (ou elle-meme) dont l'`onPointerDown` vient de `useGlisserPanneau`. */
export function trouverPoignee(racine: Element): HTMLElement | undefined {
  const candidats = [racine, ...Array.from(racine.querySelectorAll('*'))]
  for (const element of candidats) {
    const gestionnaire = proprietesReact(element)?.onPointerDown as Record<string, unknown> | undefined
    if (typeof gestionnaire === 'function' && gestionnaire[MARQUE_GESTE]) return element as HTMLElement
  }
  return undefined
}

function defile(element: HTMLElement): boolean {
  const style = getComputedStyle(element)
  const defilable = (v: string) => v === 'auto' || v === 'scroll'
  return (
    (defilable(style.overflowY) && element.scrollHeight > element.clientHeight + 1) ||
    (defilable(style.overflowX) && element.scrollWidth > element.clientWidth + 1)
  )
}

/** La fenetre sous le pointeur : le plus petit ancetre flottant qui contient une poignee. */
function fenetreDe(cible: HTMLElement): { fenetre: HTMLElement; poignee: HTMLElement } | undefined {
  for (let a: HTMLElement | null = cible; a && a !== document.body; a = a.parentElement) {
    if (defile(a) && a !== cible) return undefined // le pointeur est dans une zone qui defile : elle garde son role
    const position = getComputedStyle(a).position
    if (position !== 'fixed' && position !== 'absolute') continue
    const r = a.getBoundingClientRect()
    // Un voile plein ecran n'est pas une fenetre : cliquer a cote d'elle ne la deplace pas.
    if (r.width >= window.innerWidth * 0.95 && r.height >= window.innerHeight * 0.95) return undefined
    const poignee = trouverPoignee(a)
    if (poignee) return { fenetre: a, poignee }
  }
  return undefined
}

function appui(evenement: PointerEvent) {
  if (evenement.defaultPrevented || !evenement.isTrusted) return
  if (evenement.pointerType === 'mouse' && evenement.button !== 0) return
  const cible = evenement.target
  if (!(cible instanceof HTMLElement)) return
  if (cible.closest(INTERACTIFS)) return
  const trouve = fenetreDe(cible)
  if (!trouve) return
  const { poignee } = trouve
  if (poignee.contains(cible)) return // la poignee gere deja son propre geste
  poignee.dispatchEvent(
    new PointerEvent('pointerdown', {
      bubbles: true,
      cancelable: true,
      clientX: evenement.clientX,
      clientY: evenement.clientY,
      pointerId: evenement.pointerId,
      pointerType: evenement.pointerType,
      button: evenement.button,
      isPrimary: evenement.isPrimary,
    })
  )
}

/** A appeler une fois ; rend la fonction qui retire l'ecouteur. */
export function installerGlisserPartout(): () => void {
  document.addEventListener('pointerdown', appui, true)
  return () => document.removeEventListener('pointerdown', appui, true)
}
