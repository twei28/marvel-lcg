// LE CLAVIER DU CARTOUCHE DU BAS (decision D37 du 04/10/2026) : Espace =
// Suivant ; chiffres 1 a 9 = le choix affiche « (n) » ; Echap = le refus.
// Module PUR cote DOM : il trouve la cible de la touche, le controleur clique.
import { afterEach, describe, expect, it } from 'vitest'
import { boutonPageSuivante, cibleDeLaTouche, clavierBloque } from './clavier-cartouche'

afterEach(() => {
  document.body.innerHTML = ''
})

/** Un cartouche avec trois choix numerotes et un refus. */
function cartouche(html = ''): Element | null {
  document.body.innerHTML = `
    <section class="deroule-phase est-scene">
      <button class="deroule-vignette" data-choix="1">Spider-Man</button>
      <button class="deroule-vignette" data-choix="2">Black Widow</button>
      <button class="deroule-vignette" data-choix="3">Hawkeye</button>
      <button class="bh-bouton" data-refus>Ne pas défendre</button>
      ${html}
    </section>`
  return document.querySelector('.deroule-phase')
}

describe('cibleDeLaTouche', () => {
  it('« 2 » vise le deuxieme choix visible', () => {
    const racine = cartouche()
    expect(cibleDeLaTouche('2', racine)?.textContent).toBe('Black Widow')
  })

  it('Echap vise le refus', () => {
    const racine = cartouche()
    expect(cibleDeLaTouche('Escape', racine)?.textContent).toBe('Ne pas défendre')
  })

  it('« 0 », « a », un chiffre sans choix : rien', () => {
    const racine = cartouche()
    expect(cibleDeLaTouche('0', racine)).toBeUndefined()
    expect(cibleDeLaTouche('a', racine)).toBeUndefined()
    expect(cibleDeLaTouche('7', racine)).toBeUndefined()
    expect(cibleDeLaTouche('Enter', racine)).toBeUndefined()
  })

  it('sans racine : rien', () => {
    expect(cibleDeLaTouche('1', null)).toBeUndefined()
    expect(cibleDeLaTouche('Escape', null)).toBeUndefined()
  })

  it('un choix sous une rangee masquee (aria-hidden) ne se vise pas : le sous-cadre passe devant', () => {
    document.body.innerHTML = `
      <section class="deroule-phase est-scene">
        <div class="deroule-rangee est-grisee" aria-hidden="true">
          <button class="deroule-vignette" data-choix="1">Spider-Man</button>
          <button class="bh-bouton" data-refus>Ne pas défendre</button>
        </div>
        <div class="deroule-sous-cadre est-reponses">
          <button class="deroule-vignette" data-choix="1">Sens d'Araignée</button>
          <button class="bh-bouton" data-refus>Aucune réponse</button>
        </div>
      </section>`
    const racine = document.querySelector('.deroule-phase')
    expect(cibleDeLaTouche('1', racine)?.textContent).toBe('Sens d\'Araignée')
    expect(cibleDeLaTouche('Escape', racine)?.textContent).toBe('Aucune réponse')
  })

  it('un choix cache (hidden) ne se vise pas', () => {
    const racine = cartouche('<button class="deroule-vignette" data-choix="4" hidden>Cache</button>')
    expect(cibleDeLaTouche('4', racine)).toBeUndefined()
  })
})

describe('clavierBloque', () => {
  it('libre quand rien n est ouvert', () => {
    cartouche()
    expect(clavierBloque(document)).toBe(false)
  })

  it('bloque quand le volet du journal est ouvert', () => {
    cartouche('<aside class="volet-journal"></aside>')
    expect(clavierBloque(document)).toBe(true)
  })

  it('bloque quand une confirmation est ouverte', () => {
    cartouche('<div class="confirm-voile"></div>')
    expect(clavierBloque(document)).toBe(true)
  })

  it('bloque quand les reglages ou le menu d une carte sont ouverts', () => {
    cartouche('<div class="reglages-fenetre"></div>')
    expect(clavierBloque(document)).toBe(true)
    cartouche('<div class="menu-actions-carte"></div>')
    expect(clavierBloque(document)).toBe(true)
  })
})

describe('boutonPageSuivante', () => {
  it('trouve le bouton qui tourne la page', () => {
    const racine = cartouche('<button class="bh-bouton deroule-suivant" data-page-suivante>Suivant (espace)</button>')
    expect(boutonPageSuivante(racine)?.textContent).toBe('Suivant (espace)')
  })

  it('rien sur la derniere page, ni sans racine', () => {
    expect(boutonPageSuivante(cartouche())).toBeUndefined()
    expect(boutonPageSuivante(null)).toBeUndefined()
  })
})
