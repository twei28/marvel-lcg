// @vitest-environment jsdom
import { describe, it, expect, beforeEach } from 'vitest'
import { sonderPilesDuJoueur } from './sonde-affichage'

/** Pose une pile dans le DOM, avec une boîte de la taille voulue (jsdom ne mesure rien). */
function poser(pile: string, taille: { w: number; h: number }, style = '', avecCadre = true): HTMLElement {
  const unite = document.createElement('div')
  unite.className = 'plateau-unite'
  unite.dataset.pile = pile
  if (style) unite.setAttribute('style', style)
  if (avecCadre) {
    const cadre = document.createElement('div')
    cadre.className = 'scan-frame'
    unite.appendChild(cadre)
  }
  unite.getBoundingClientRect = () => ({ width: taille.w, height: taille.h } as DOMRect)
  document.body.appendChild(unite)
  return unite
}

describe('sonderPilesDuJoueur', () => {
  beforeEach(() => {
    document.body.innerHTML = ''
  })

  it('une pile dessinée normalement ne lève pas d’anomalie', () => {
    poser('joueur-deck', { w: 127, h: 178 })
    poser('joueur-defausse', { w: 127, h: 178 })
    const lignes = sonderPilesDuJoueur({ deck: 10, defausse: 17 })
    expect(lignes).toHaveLength(2)
    expect(lignes.some((l) => l.startsWith('ANOMALIE'))).toBe(false)
  })

  it('un deck non vide masqué par visibility est signalé avec son responsable', () => {
    poser('joueur-deck', { w: 127, h: 178 }, 'visibility: hidden')
    poser('joueur-defausse', { w: 127, h: 178 })
    const [deck] = sonderPilesDuJoueur({ deck: 10, defausse: 17 })
    expect(deck).toMatch(/^ANOMALIE joueur-deck/)
    expect(deck).toContain('visibility:hidden')
  })

  it('un deck non vide absent du DOM est signalé', () => {
    poser('joueur-defausse', { w: 127, h: 178 })
    const [deck] = sonderPilesDuJoueur({ deck: 10, defausse: 17 })
    expect(deck).toMatch(/^ANOMALIE joueur-deck.*absente du DOM/)
  })

  it('un deck non vide sans cadre de carte est signalé', () => {
    poser('joueur-deck', { w: 127, h: 178 }, '', false)
    const [deck] = sonderPilesDuJoueur({ deck: 10, defausse: 0 })
    expect(deck).toMatch(/^ANOMALIE/)
  })

  it('un cadre resté en retournement (n°48) est signalé : de chant, il est invisible', () => {
    const unite = poser('joueur-deck', { w: 127, h: 178 })
    unite.querySelector('.scan-frame')!.classList.add('retourne-dos')
    const [deck] = sonderPilesDuJoueur({ deck: 10, defausse: 0 })
    expect(deck).toMatch(/^ANOMALIE joueur-deck/)
    expect(deck).toContain('retourne-dos')
  })

  it('un deck vraiment vide et absent n’est pas une anomalie', () => {
    const [deck] = sonderPilesDuJoueur({ deck: 0, defausse: 0 })
    expect(deck).not.toMatch(/^ANOMALIE/)
  })
})
