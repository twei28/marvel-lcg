import { beforeEach, describe, expect, it } from 'vitest'
import { CLE_FOND_IMAGE, appliquerFondImage, lireFondImage, retirerFondImage } from './fond-image'

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
})
