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

  it('traduit les compteurs du pack Red Sonja (stealth, fetter)', () => {
    // rs011 Crimson Shadow et rs018 She-Devil Shackled! : sans entree dans
    // la table, le plateau ecrivait le mot anglais brut en pleine partie
    // francaise (etape 8 bis de PROCESSUS-CARTE, 23/09/2026).
    vi.spyOn(langue, 'langueActuelle').mockReturnValue('fr')
    expect(nomDeCompteur('stealth')).toBe('discrétion')
    expect(nomDeCompteur('fetter')).toBe('entrave')
  })

  it('traduit les compteurs du pack Conan (crom, serpent)', () => {
    vi.spyOn(langue, 'langueActuelle').mockReturnValue('fr')
    expect(nomDeCompteur('crom')).toBe('Crom')
    expect(nomDeCompteur('serpent')).toBe('serpent')
  })

  it('traduit les compteurs du scenario Paibok (mastery, absorption)', () => {
    // Jetons de maitrise sur Paibok (sk141) et d'absorption sur Asti (sk163) : sans entree,
    // le plateau ecrivait « mastery » en pleine partie francaise.
    vi.spyOn(langue, 'langueActuelle').mockReturnValue('fr')
    expect(nomDeCompteur('mastery')).toBe('maîtrise')
    expect(nomDeCompteur('absorption')).toBe('absorption')
  })

  it('traduit le compteur de soupcon de Secret Invasion (sk194)', () => {
    // Jetons de soupcon sur l'environnement « Who Do You Trust? » : sans entree, le plateau ecrivait « suspicion ».
    vi.spyOn(langue, 'langueActuelle').mockReturnValue('fr')
    expect(nomDeCompteur('suspicion')).toBe('soupçon')
  })

  it('traduit le compteur du scenario Skrull Pantheon (faith)', () => {
    // Jetons de foi sur Kly'bn / Sl'gur't (sk170) : sans entree, le plateau ecrivait « faith ».
    vi.spyOn(langue, 'langueActuelle').mockReturnValue('fr')
    expect(nomDeCompteur('faith')).toBe('foi')
  })

  it('traduit le compteur honte de Hunting Season (hs060)', () => {
    vi.spyOn(langue, 'langueActuelle').mockReturnValue('fr')
    expect(nomDeCompteur('shame')).toBe('honte')
  })

  it('traduit les compteurs des tortues TMNT (swarm de Donatello, timer de tr014)', () => {
    // td016/td017 (essaims) et tr014 Mutagen Bomb : sans entree, « 4 swarm » / « 2 timer ».
    vi.spyOn(langue, 'langueActuelle').mockReturnValue('fr')
    expect(nomDeCompteur('swarm')).toBe('essaim')
    expect(nomDeCompteur('timer')).toBe('minuteur')
  })
})
