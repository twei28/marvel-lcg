import { beforeEach, describe, expect, it } from 'vitest'
import {
  CLE_FOND_COULEURS,
  CLE_FOND_IMAGE,
  appliquerFondImage,
  baseDuFondImage,
  ecrireGarderCouleurs,
  lireFondImage,
  lireGarderCouleurs,
  retirerFondImage,
} from './fond-image'

beforeEach(() => {
  window.localStorage.clear()
  appliquerFondImage(undefined)
})

describe('image de fond de la table', () => {
  it('rien par défaut : pas d’image, pas de variable, pas d’attribut', () => {
    expect(lireFondImage()).toBeUndefined()
    expect(document.documentElement.dataset.fondImage).toBeUndefined()
  })

  it('appliquer pose la variable et l’attribut, retirer les enlève', () => {
    appliquerFondImage('data:image/jpeg;base64,AAAA')
    expect(document.documentElement.style.getPropertyValue('--fond-image')).toContain('data:image/jpeg;base64,AAAA')
    expect(document.documentElement.dataset.fondImage).toBe('oui')
    appliquerFondImage(undefined)
    expect(document.documentElement.style.getPropertyValue('--fond-image')).toBe('')
    expect(document.documentElement.dataset.fondImage).toBeUndefined()
  })

  it('retirer efface l’image gardée sur l’appareil', () => {
    window.localStorage.setItem(CLE_FOND_IMAGE, 'data:image/jpeg;base64,AAAA')
    expect(lireFondImage()).toBe('data:image/jpeg;base64,AAAA')
    retirerFondImage()
    expect(lireFondImage()).toBeUndefined()
  })

  it('garder les couleurs est désactivé par défaut, et ne vaut qu’avec une image', () => {
    expect(lireGarderCouleurs()).toBe(false)
    appliquerFondImage('data:image/jpeg;base64,AAAA')
    expect(document.documentElement.dataset.fondCouleurs).toBeUndefined()
    expect(baseDuFondImage()).toBeUndefined()
  })

  it('garder les couleurs : l’image devient la couche de base des halos', () => {
    window.localStorage.setItem(CLE_FOND_IMAGE, 'data:image/jpeg;base64,AAAA')
    ecrireGarderCouleurs(true)
    expect(window.localStorage.getItem(CLE_FOND_COULEURS)).toBe('1')
    expect(document.documentElement.dataset.fondCouleurs).toBe('oui')
    expect(baseDuFondImage()).toBe('var(--fond-image)')
    ecrireGarderCouleurs(false)
    expect(document.documentElement.dataset.fondCouleurs).toBeUndefined()
    expect(baseDuFondImage()).toBeUndefined()
  })
})
