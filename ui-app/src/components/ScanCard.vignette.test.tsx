// La carte de la table demande sa VIGNETTE, l'apercu agrandi le scan complet.
//
// ⚠ LE CAS QUI COMPTE, ET IL VIENT D'UN CONSTAT (08/09/2026) : « les cartes ne
// sont pas plus nettes ». Un scan de 615 px reduit a 123 par le navigateur
// perd son texte ; la vignette, reduite sur le serveur avec un vrai filtre,
// le garde. Si une carte de table redemandait /scan/, tout ce travail serait
// invisible.
import { render } from '@testing-library/react'
import { describe, expect, it } from 'vitest'
import { ScanCard, versVignette } from './ScanCard'

function src(container: HTMLElement): string | null {
  return container.querySelector('.scan-frame img')?.getAttribute('src') ?? null
}

describe('la vignette', () => {
  it('une carte de la table demande /vignette/', () => {
    const { container } = render(<ScanCard id="1" name="Rhino" kind="villain" imageUrl="/scan/fr_01095" />)
    expect(src(container)).toBe('/vignette/fr_01095')
  })

  it("l'apercu agrandi garde le scan complet", () => {
    const { container } = render(
      <ScanCard id="1" name="Rhino" kind="villain" imageUrl="/scan/fr_01095" taille="grande" />
    )
    expect(src(container)).toBe('/scan/fr_01095')
  })

  // Les images de la vitrine sont importees par Vite, pas servies par le
  // jeu : rien a reecrire, et surtout rien a casser.
  it('une adresse qui n est pas un scan est rendue telle quelle', () => {
    expect(versVignette('/assets/groot-abc123.jpg')).toBe('/assets/groot-abc123.jpg')
    expect(versVignette('')).toBe('')
    expect(versVignette('data:image/png;base64,AAAA')).toBe('data:image/png;base64,AAAA')
  })
})
