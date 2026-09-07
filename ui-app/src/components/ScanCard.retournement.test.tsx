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

  it('ne pivote pas une carte qui arrive déjà face visible', () => {
    const { container } = render(<ScanCard {...props} imageUrl="/face.jpg" />)
    expect(container.querySelector('.scan-frame')?.className).toBe('scan-frame')
  })
})
