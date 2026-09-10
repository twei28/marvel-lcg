import { afterEach, describe, expect, it, vi } from 'vitest'
import * as langue from './langue'
import { nomDeCompteur } from './compteurs-fr'

afterEach(() => vi.restoreAllMocks())

describe('nomDeCompteur', () => {
  it('traduit un compteur connu en français', () => {
    vi.spyOn(langue, 'langueActuelle').mockReturnValue('fr')
    expect(nomDeCompteur('steel')).toBe('acier')
    expect(nomDeCompteur('charge')).toBe('charge')
  })

  it('traduit le compteur a deux mots du pack Spider-Woman', () => {
    // La clef porte un ESPACE (« psionic web »), pas un souligne : la
    // recherche se fait sur la clef brute, et une table indexee autrement
    // laisserait « psionic web » a l'ecran en pleine partie francaise.
    vi.spyOn(langue, 'langueActuelle').mockReturnValue('fr')
    expect(nomDeCompteur('psionic web')).toBe('toile psionique')
  })

  it('laisse un compteur inconnu en anglais, mots séparés', () => {
    vi.spyOn(langue, 'langueActuelle').mockReturnValue('fr')
    expect(nomDeCompteur('tic_tac_toe_1_1')).toBe('tic tac toe 1 1')
  })

  it('ne traduit rien en anglais', () => {
    vi.spyOn(langue, 'langueActuelle').mockReturnValue('en')
    expect(nomDeCompteur('steel')).toBe('steel')
  })
})
