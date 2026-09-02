// Rendu du marqueur de MORSURE. L'illustration etant branchee (morsure.ts),
// la carte mordue porte l'alligator et PLUS la pastille texte : les deux
// ensemble feraient deux signaux pour une seule information.
import { describe, expect, it } from 'vitest'
import { render } from '@testing-library/react'
import { ScanCard } from './ScanCard'
import { IMAGE_MORSURE } from './morsure'

describe('marqueur de morsure sur la carte', () => {
  // Le libelle passe par `t()`, donc par la langue : on interroge les classes,
  // jamais le texte rendu.
  it('affiche l’alligator sur l’ennemi mordu, sans pastille texte', () => {
    const { container } = render(<ScanCard id="01094" name="Rhino" kind="villain" imageUrl="" mordu />)
    const marque = container.querySelector('img.marque-morsure')
    expect(marque).not.toBeNull()
    expect(marque?.getAttribute('src')).toBe(IMAGE_MORSURE)
    expect(container.querySelector('.pastille-morsure')).toBeNull()
  })

  it('pose l’alligator HORS du cadre, qui rogne son contenu', () => {
    const { container } = render(<ScanCard id="01094" name="Rhino" kind="villain" imageUrl="" mordu />)
    const marque = container.querySelector('.marque-morsure')
    expect(marque?.parentElement).toHaveClass('scan-visuel')
  })

  it('ne marque pas une carte face cachee', () => {
    const { container } = render(<ScanCard id="01094" name="Rhino" kind="villain" imageUrl="" mordu facedown />)
    expect(container.querySelector('.marque-morsure')).toBeNull()
    expect(container.querySelector('.pastille-morsure')).toBeNull()
  })

  it('donne au heros accroche sa pastille et sa classe, sans alligator', () => {
    const { container } = render(<ScanCard id="al001a" name="Alligator Loki" kind="hero" imageUrl="" accroche />)
    expect(container.querySelector('.pastille-accroche')).not.toBeNull()
    expect(container.querySelector('.scan-card')).toHaveClass('est-accroche')
    expect(container.querySelector('.marque-morsure')).toBeNull()
  })
})
