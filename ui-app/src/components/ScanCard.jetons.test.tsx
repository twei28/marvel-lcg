// Les jetons poses sur la carte, avec leur chiffre : menace sur une
// manigance, degats subis sur un personnage, compteurs (ressources,
// acceleration). Images fournies par l'utilisateur le 7 septembre 2026.
import { describe, expect, it } from 'vitest'
import { render } from '@testing-library/react'
import { ScanCard } from './ScanCard'

const base = { id: '1', name: 'Carte', imageUrl: '' } as const

describe('jetons sur la carte', () => {
  it('pose le jeton de menace avec son chiffre sur une manigance', () => {
    const { container } = render(<ScanCard {...base} kind="main-scheme" jetonMenace={9} />)
    const jeton = container.querySelector('.jeton-carte.jeton-menace')
    expect(jeton?.textContent).toBe('9')
  })

  it('ne pose aucun jeton de menace a zero', () => {
    const { container } = render(<ScanCard {...base} kind="side-scheme" jetonMenace={0} />)
    expect(container.querySelector('.jeton-menace')).toBeNull()
  })

  it('pose le jeton de degats subis, et rien sur un personnage intact', () => {
    const blesse = render(<ScanCard {...base} kind="hero" jetonDegats={4} />)
    expect(blesse.container.querySelector('.jeton-carte.jeton-degats')?.textContent).toBe('4')
    const intact = render(<ScanCard {...base} id="2" kind="hero" jetonDegats={0} />)
    expect(intact.container.querySelector('.jeton-degats')).toBeNull()
  })

  it('pose un jeton de compteur avec le chiffre et le nom', () => {
    const { container } = render(
      <ScanCard {...base} kind="upgrade" counters={[{ label: 'acier', value: 2, cle: 'steel' }]} />
    )
    const jeton = container.querySelector('.jeton-carte.jeton-compteur')
    expect(jeton?.querySelector('b')?.textContent).toBe('2')
    expect(jeton?.querySelector('.jeton-nom')?.textContent).toBe('acier')
    expect(container.querySelector('.counter-badge')).toBeNull()
  })

  it('reconnait le jeton d acceleration, sans chiffre quand il n y en a qu un', () => {
    const { container } = render(
      <ScanCard {...base} kind="main-scheme" counters={[{ label: 'accélération', value: 1, cle: 'acceleration' }]} />
    )
    const jeton = container.querySelector('.jeton-carte.jeton-acceleration')
    expect(jeton).not.toBeNull()
    expect(jeton?.querySelector('b')).toBeNull()
  })

  it('cache les jetons d une carte face cachee', () => {
    const { container } = render(<ScanCard {...base} kind="main-scheme" facedown jetonMenace={3} />)
    expect(container.querySelector('.jeton-carte')).toBeNull()
  })
})
