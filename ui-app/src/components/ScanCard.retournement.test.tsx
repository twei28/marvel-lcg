// Une carte cachée qui se révèle pivote sur place : le dos jusqu'à la tranche,
// puis la face depuis la tranche. Avant, l'image changeait d'un coup.
import { describe, expect, it } from 'vitest'
import { render, waitFor } from '@testing-library/react'
import { ScanCard } from './ScanCard'

const props = { id: '7', name: 'Traîtrise', kind: 'treachery' as const }

describe('ScanCard : le retournement', () => {
  it('garde le dos pendant la première moitié, puis montre la face', async () => {
    const { container, rerender } = render(<ScanCard {...props} imageUrl="/dos.jpg" facedown />)
    rerender(<ScanCard {...props} imageUrl="/face.jpg" facedown={false} />)
    const cadre = container.querySelector('.scan-frame')!
    expect(cadre.classList.contains('retourne-dos')).toBe(true)
    expect(container.querySelector('img')?.getAttribute('src')).toBe('/dos.jpg')
    await waitFor(() => expect(cadre.classList.contains('retourne-face')).toBe(true), { timeout: 1500 })
    expect(container.querySelector('img')?.getAttribute('src')).toBe('/face.jpg')
    await waitFor(() => expect(cadre.className).toBe('scan-frame'), { timeout: 1500 })
  })

  // Rapport de bug n°48 (04/10/2026) : le deck du héros disparaissait. Le
  // dessus du deck redevient face cachée EN PLEIN retournement (une recherche de
  // deck le montre un instant au joueur) : le nettoyage de l'effet coupe les
  // minuteries, et plus rien ne remet l'état à zéro. Le cadre garde `retourne-dos`,
  // dont l'animation finit à 90° : la pile est de chant, donc invisible.
  it('ne reste pas coincé de chant quand la carte se recache en plein retournement', async () => {
    const { container, rerender } = render(<ScanCard {...props} imageUrl="/dos.jpg" facedown />)
    rerender(<ScanCard {...props} imageUrl="/face.jpg" facedown={false} />)
    expect(container.querySelector('.scan-frame')!.classList.contains('retourne-dos')).toBe(true)
    rerender(<ScanCard {...props} imageUrl="/dos.jpg" facedown />)
    await new Promise((fin) => setTimeout(fin, 800))
    expect(container.querySelector('.scan-frame')?.className).toBe('scan-frame')
  })

  it('ne pivote pas une carte qui arrive déjà face visible', () => {
    const { container } = render(<ScanCard {...props} imageUrl="/face.jpg" />)
    expect(container.querySelector('.scan-frame')?.className).toBe('scan-frame')
  })
})
