// Lot 2 de la refonte (12/10/2026) : une seule taille de carte par ecran, qui
// rapetisse toute ensemble quand l'ecran ne tient pas dans la boite.
import { describe, expect, it } from 'vitest'
import { ajusterLesCartes, CARTE_MAX, CARTE_MIN, deborde, excedent, hauteurPosee, ZOOM_MIN } from './essai-tailles'

/** Un rectangle factice : jsdom ne met rien en page. */
function rect(haut: number, gauche: number, largeur: number, hauteur: number): DOMRect {
  return {
    top: haut, left: gauche, width: largeur, height: hauteur,
    bottom: haut + hauteur, right: gauche + largeur, x: gauche, y: haut, toJSON: () => ({}),
  } as DOMRect
}

/**
 * Une boite de 300 px de haut, et une rangee dont la hauteur suit la carte :
 * deux fois `--essai-carte-h` (la carte et ce qu'elle porte dessous).
 */
function monter() {
  const section = document.createElement('section')
  const corps = document.createElement('div')
  const rangee = document.createElement('div')
  corps.appendChild(rangee)
  section.appendChild(corps)
  corps.getBoundingClientRect = () => rect(0, 0, 600, 300)
  rangee.getBoundingClientRect = () => rect(0, 0, 500, 2 * hauteurPosee(section))
  return { section, corps }
}

describe('essai-tailles : les cartes tiennent dans la boite', () => {
  it('un debordement que la taille des cartes ne change pas ne les reduit pas : la plus grande taille reste', () => {
    const { section, corps } = monter()
    // Un cadre qui depasse de 3 px a gauche, quelle que soit la carte (k1366, 12/10/2026).
    corps.firstElementChild!.getBoundingClientRect = () => rect(0, -3, 500, 100)
    expect(ajusterLesCartes(section, corps)).toBe(CARTE_MAX)
    expect(section.style.getPropertyValue('--essai-carte-h')).toBe('170px')
  })

  it('un ecran qui tient garde la plus grande taille (170 px)', () => {
    const { section, corps } = monter()
    corps.firstElementChild!.getBoundingClientRect = () => rect(0, 0, 500, 200)
    expect(ajusterLesCartes(section, corps)).toBe(CARTE_MAX)
    expect(section.style.getPropertyValue('--essai-carte-h')).toBe('170px')
  })

  it('un ecran qui deborde : toutes les cartes rapetissent, jusqu a tenir', () => {
    const { section, corps } = monter()
    const h = ajusterLesCartes(section, corps)
    expect(h).toBeLessThanOrEqual(150)
    expect(h).toBeGreaterThan(120)
    expect(deborde(corps)).toBe(false)
  })

  it('jamais sous le minimum, meme si rien ne tient', () => {
    const { section, corps } = monter()
    corps.firstElementChild!.getBoundingClientRect = () => rect(0, 0, 500, 50 * hauteurPosee(section))
    expect(ajusterLesCartes(section, corps)).toBe(CARTE_MIN)
  })

  it('un element qui sort sur le cote compte aussi comme un debordement', () => {
    const { corps } = monter()
    corps.firstElementChild!.getBoundingClientRect = () => rect(0, 0, 640, 100)
    expect(deborde(corps)).toBe(true)
  })

  it('un element masque (0 x 0) ne compte pas', () => {
    const { corps } = monter()
    corps.firstElementChild!.getBoundingClientRect = () => rect(900, 900, 0, 0)
    expect(deborde(corps)).toBe(false)
  })
})

describe('lot 5c : le texte qui deborde encore, cartes au minimum', () => {
  const zoom = (section: HTMLElement) => parseFloat(section.style.getPropertyValue('--essai-zoom-corps') || '1')
  it('quand les cartes n y peuvent rien, le contenu du corps rapetisse d un cran jusqu a tenir', () => {
    const { section, corps } = monter()
    // 330 px de texte quelle que soit la carte : seul le zoom le fait tenir (300 px).
    corps.firstElementChild!.getBoundingClientRect = () => rect(0, 0, 500, 330 * zoom(section))
    expect(ajusterLesCartes(section, corps)).toBe(CARTE_MAX)
    expect(zoom(section)).toBe(0.9)
    expect(zoom(section)).toBeLessThan(1)
    expect(zoom(section)).toBeGreaterThanOrEqual(ZOOM_MIN)
    expect(deborde(corps)).toBe(false)
  })

  it('un ecran qui tient garde le zoom a 1, et un nouvel ajustement le remet a 1', () => {
    const { section, corps } = monter()
    section.style.setProperty('--essai-zoom-corps', '0.85')
    corps.firstElementChild!.getBoundingClientRect = () => rect(0, 0, 500, 200)
    ajusterLesCartes(section, corps)
    expect(zoom(section)).toBe(1)
  })

  it('un debordement que le zoom ne change pas laisse le zoom a 1', () => {
    const { section, corps } = monter()
    corps.firstElementChild!.getBoundingClientRect = () => rect(0, 0, 500, 50 * hauteurPosee(section))
    ajusterLesCartes(section, corps)
    expect(zoom(section)).toBe(1)
  })
})

describe('excedent', () => {
  it('mesure le pire depassement en pixels', () => {
    const { corps } = monter()
    corps.firstElementChild!.getBoundingClientRect = () => rect(0, 0, 612, 100)
    expect(excedent(corps)).toBe(12)
  })
})
