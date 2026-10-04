import { describe, expect, it } from 'vitest'
import { render } from '@testing-library/react'
import { avecIcones, coutEnIcones, marquerRessources, ressourcesEnMots } from './icones-ressources'

describe('les ressources en icones', () => {
  it('remplace les jetons du moteur par des marqueurs', () => {
    expect(marquerRessources('Génère [[physical]][[energy]]')).toBe('Génère ⟦P⟧⟦E⟧')
  })

  it('remplace aussi le jeton a UN crochet des textes francais officiels (Boom Sonique)', () => {
    expect(marquerRessources('les ressources suivantes : [energy] [mental] [physical]')).toBe(
      'les ressources suivantes : ⟦E⟧ ⟦M⟧ ⟦P⟧'
    )
  })

  it('rend les icones en mots pour une infobulle native', () => {
    expect(ressourcesEnMots('Spend [[energy]][[mental]] puis [physical]')).toBe(
      'Spend énergiementale puis physique'
    )
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

  it("connait l'eclair, la ressource maison du pack Zeus (11/09/2026)", () => {
    expect(marquerRessources('Génère [[lightning]]')).toBe('Génère ⟦L⟧')
    expect(marquerRessources('a lightning resource')).toBe('a ⟦L⟧ resource')
    expect(coutEnIcones('YL')).toBe('⟦E⟧⟦L⟧')
    const { container } = render(<span>{avecIcones('Paie ⟦L⟧')}</span>)
    const icone = container.querySelector('i.icone-res.res-lightning')
    expect(icone).not.toBeNull()
    // Pas de glyphe d'eclair droit dans ChampionsIcons : c'est un SVG.
    expect(icone?.querySelector('svg')).not.toBeNull()
    expect(icone?.getAttribute('aria-label')).toBe('éclair')
    expect(container.textContent).toBe('Paie ')
  })
})
