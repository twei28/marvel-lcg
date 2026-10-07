import { afterEach, describe, expect, it } from 'vitest'
import { poserLesMarques } from './CoucheMarques'

afterEach(() => {
  document.body.innerHTML = ''
})

function table() {
  document.body.innerHTML = `
    <div class="plateau-scene">
      <div class="scan-card" data-card-id="1"></div>
      <div class="scan-card" data-card-id="2"></div>
    </div>`
}

describe('les marques posees sur les cartes de la table', () => {
  it('cible et surlignage en attributs, retires quand la marque disparait', () => {
    table()
    poserLesMarques({ cibles: { 1: 2 }, fleches: [], surlignages: { 2: 'vert' } })
    const un = document.querySelector<HTMLElement>('[data-card-id="1"]')!
    const deux = document.querySelector<HTMLElement>('[data-card-id="2"]')!
    expect(un.getAttribute('data-ciblee')).toBe('2')
    expect(un.style.getPropertyValue('--couleur-cible')).not.toBe('')
    expect(deux.getAttribute('data-surlignage')).toBe('vert')
    poserLesMarques({ cibles: {}, fleches: [], surlignages: {} })
    expect(un.hasAttribute('data-ciblee')).toBe(false)
    expect(deux.hasAttribute('data-surlignage')).toBe(false)
  })
  it('l attribut survit a une reecriture du className par React', () => {
    table()
    poserLesMarques({ cibles: { 1: 0 }, fleches: [], surlignages: {} })
    const un = document.querySelector<HTMLElement>('[data-card-id="1"]')!
    un.className = 'scan-card is-exhausted'
    expect(un.getAttribute('data-ciblee')).toBe('0')
  })
})
