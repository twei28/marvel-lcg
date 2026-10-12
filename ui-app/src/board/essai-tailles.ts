// UNE SEULE TAILLE DE CARTE PAR ECRAN (refonte du 12/10/2026, lot 2,
// decisions 29, 48 et 54) : toutes les cartes de la boite de l'essai ont la
// meme hauteur (`--essai-carte-h`, cartouche-essai.css), 170 px au plus. Si
// l'ecran ne tient pas dans la boite, elles rapetissent TOUTES ensemble, jamais
// de barre de defilement ni de debordement. La boite et « Continuer » ne
// bougent pas : seul le contenu du corps s'adapte.

export const CARTE_MAX = 170
export const CARTE_MIN = 56
const PAS = 0.9

/**
 * De combien le contenu deborde du corps, en pixels (0 : tout tient). Le corps
 * est en `overflow: hidden` : on mesure aussi chaque element, rogne ou non.
 */
export function excedent(corps: HTMLElement): number {
  let pire = Math.max(0, corps.scrollHeight - corps.clientHeight, corps.scrollWidth - corps.clientWidth)
  const boite = corps.getBoundingClientRect()
  for (const el of Array.from(corps.querySelectorAll<HTMLElement>('*'))) {
    const r = el.getBoundingClientRect()
    if (r.width === 0 || r.height === 0) continue
    pire = Math.max(pire, r.bottom - boite.bottom, r.right - boite.right, boite.top - r.top, boite.left - r.left)
  }
  return Math.max(0, Math.round(pire))
}

/** Le contenu deborde-t-il du corps (au-dela de `marge` pixels) ? */
export function deborde(corps: HTMLElement, marge = 2): boolean {
  return excedent(corps) > marge
}

/** La hauteur posee aujourd'hui sur la boite, ou le maximum. */
export function hauteurPosee(section: HTMLElement): number {
  const brute = parseFloat(section.style.getPropertyValue('--essai-carte-h'))
  return Number.isFinite(brute) && brute > 0 ? brute : CARTE_MAX
}

/**
 * Pose la plus grande hauteur de carte qui tient, en partant de `depart` et en
 * descendant. Chaque mesure relit la mise en page (synchrone) : appele avant la
 * peinture, l'ecran ne montre jamais l'etat qui deborde. Rend la hauteur posee.
 */
export function ajusterLesCartes(section: HTMLElement, corps: HTMLElement, depart = CARTE_MAX, marge = 2): number {
  const poser = (h: number) => section.style.setProperty('--essai-carte-h', `${h}px`)
  let hauteur = Math.max(CARTE_MIN, Math.min(CARTE_MAX, depart))
  poser(hauteur)
  // La meilleure taille : le plus petit excedent, et a excedent egal la plus
  // grande. Un debordement que la taille des cartes ne change pas (un cadre
  // qui depasse de 3 px) ne doit pas les reduire au minimum pour rien.
  let meilleure = { hauteur, excedent: excedent(corps) }
  while (meilleure.excedent > marge && hauteur > CARTE_MIN) {
    hauteur = Math.max(CARTE_MIN, Math.floor(hauteur * PAS))
    poser(hauteur)
    const e = excedent(corps)
    if (e < meilleure.excedent) meilleure = { hauteur, excedent: e }
  }
  poser(meilleure.hauteur)
  return meilleure.hauteur
}
