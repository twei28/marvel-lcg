// Le jeton de premier joueur, dit dans l'étiquette de type de l'identité (demande du 19/10/2026) :
// seulement à plusieurs héros, et même quand la table cache les étiquettes.
import { describe, expect, it } from 'vitest'
import { render } from '@testing-library/react'
import { PlusieursJoueurs, ScanCard } from './ScanCard'

const base = { id: '1', name: 'Spider-Man', imageUrl: '', kind: 'hero' } as const

function pastille(solo: boolean, props: Record<string, unknown>) {
  const { container } = render(
    <PlusieursJoueurs.Provider value={!solo}>
      <ScanCard {...base} {...props} />
    </PlusieursJoueurs.Provider>
  )
  return container.querySelector('.kind-pill')
}

describe('étiquette du premier joueur', () => {
  it('remplace le type par « Premier joueur », à plusieurs héros', () => {
    const p = pastille(false, { premierJoueur: true })
    expect(p?.textContent).toBe('Premier joueur')
    expect(p?.classList.contains('est-premier-joueur')).toBe(true)
  })

  it('reste muette en solo et sur un héros sans jeton', () => {
    expect(pastille(true, { premierJoueur: true })?.textContent).not.toBe('Premier joueur')
    expect(pastille(false, {})?.textContent).not.toBe('Premier joueur')
  })

  it('se montre même quand le type est masqué : seule la mention reste', () => {
    const p = pastille(false, { premierJoueur: true, masquerType: true })
    expect(p?.textContent).toBe('Premier joueur')
  })
})
