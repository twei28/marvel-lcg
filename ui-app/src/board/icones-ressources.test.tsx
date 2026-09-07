import { describe, expect, it } from 'vitest'
import { render } from '@testing-library/react'
import { avecIcones, coutEnIcones, marquerRessources } from './icones-ressources'

describe('les ressources en icones', () => {
  it('remplace les jetons du moteur par des marqueurs', () => {
    expect(marquerRessources('Génère [[physical]][[energy]]')).toBe('Génère ⟦P⟧⟦E⟧')
  })

  it('remplace le mot devant « resource(s) », et garde le mot resource', () => {
    expect(marquerRessources('Pay 1 mental resource(s)')).toBe('Pay 1 ⟦M⟧ resource(s)')
    expect(marquerRessources('a wild resource')).toBe('a ⟦W⟧ resource')
  })

  it('laisse les autres mots tranquilles', () => {
    expect(marquerRessources('Mental Gymnastics')).toBe('Mental Gymnastics')
  })

  it('traduit un cout type en marqueurs, pas un cout ordinaire', () => {
    expect(coutEnIcones('BY')).toBe('⟦M⟧⟦E⟧')
    expect(coutEnIcones('rrg')).toBe('⟦P⟧⟦P⟧⟦W⟧')
    expect(coutEnIcones('2')).toBe('2')
    expect(coutEnIcones('1/3')).toBe('1/3')
    expect(coutEnIcones('')).toBe('')
  })

  it('rend les marqueurs en icones de la police du jeu, le reste en texte', () => {
    const { container } = render(<span>{avecIcones('Paie 1 ⟦M⟧ puis ⟦E⟧')}</span>)
    const icones = container.querySelectorAll('i.icone-res')
    expect(icones).toHaveLength(2)
    expect(icones[0]?.textContent).toBe('M')
    expect(icones[0]?.className).toBe('icone-res res-mental')
    expect(icones[0]?.getAttribute('aria-label')).toBe('mentale')
    expect(container.textContent).toBe('Paie 1 M puis E')
  })

  it('rend une chaine sans marqueur telle quelle', () => {
    expect(avecIcones('Attaque')).toBe('Attaque')
  })
})
