// Les traits d'un heros en ce moment (idee de Lilipulse, 28/10/2026) : imprimes, gagnes, perdus.
import { describe, expect, it } from 'vitest'
import { PAS_PAR_CHEVAUCHEMENT } from './reglages-affichage-cartes'
import { normaliserTrait, pastillesDeTraits, pastillesVisibles } from './traits-heros'

describe('normaliserTrait', () => {
  it('rend la meme cle pour la forme du moteur et celle du catalogue', () => {
    expect(normaliserTrait('t_WEB-WARRIOR')).toBe('WEB-WARRIOR')
    expect(normaliserTrait('t_DARK_ELF')).toBe(normaliserTrait('Dark Elf'))
    expect(normaliserTrait('t_AVATAR_OF_LOKI')).toBe('AVATAR OF LOKI')
  })
})

describe('pastillesDeTraits : Rocket gagne Aerien', () => {
  const imprimes = ['GUARDIAN']
  it('marque le trait gagne, garde l imprime', () => {
    const p = pastillesDeTraits(imprimes, ['t_GUARDIAN', 't_AERIAL'], 'en')
    expect(p.map((x) => [x.cle, x.etat])).toEqual([['GUARDIAN', 'imprime'], ['AERIAL', 'gagne']])
  })
  it('marque un trait imprime que le moteur ne donne plus comme perdu, apres les gagnes', () => {
    const p = pastillesDeTraits(['GUARDIAN', 'OUTLAW'], ['t_GUARDIAN', 't_AERIAL'], 'en')
    expect(p.map((x) => [x.cle, x.etat])).toEqual([['GUARDIAN', 'imprime'], ['AERIAL', 'gagne'], ['OUTLAW', 'perdu']])
  })
  it('ne dit rien quand le moteur ne donne pas les traits (pas « tout perdu »)', () => {
    expect(pastillesDeTraits(imprimes, undefined, 'en')).toEqual([])
  })
  it('traduit en francais', () => {
    expect(pastillesDeTraits(imprimes, ['t_GUARDIAN', 't_AERIAL'], 'fr').map((x) => x.texte)).toContain('AÉRIEN')
  })
})

describe('pastillesVisibles : les trois reglages', () => {
  const p = pastillesDeTraits(['GUARDIAN', 'OUTLAW'], ['t_GUARDIAN', 't_AERIAL'], 'en')
  it('« tous » montre tout', () => expect(pastillesVisibles(p, 'tous')).toHaveLength(3))
  it('« changements » ne montre que gagnes et perdus', () => {
    expect(pastillesVisibles(p, 'changements').map((x) => x.cle)).toEqual(['AERIAL', 'OUTLAW'])
  })
  it('« changements » ne montre rien tant que rien n a bouge', () => {
    expect(pastillesVisibles(pastillesDeTraits(['GUARDIAN'], ['t_GUARDIAN'], 'en'), 'changements')).toEqual([])
  })
  it('« aucun » ne montre rien', () => expect(pastillesVisibles(p, 'aucun')).toEqual([]))
})

describe('chevauchement des ameliorations', () => {
  it('garde la moitie existante et ordonne les quatre niveaux du plus cache au plus espace', () => {
    expect(PAS_PAR_CHEVAUCHEMENT.moitie).toBe(63)
    const pas = [PAS_PAR_CHEVAUCHEMENT.moitie, PAS_PAR_CHEVAUCHEMENT.quart, PAS_PAR_CHEVAUCHEMENT.collees, PAS_PAR_CHEVAUCHEMENT.espacees]
    expect([...pas].sort((a, b) => a - b)).toEqual(pas)
    expect(PAS_PAR_CHEVAUCHEMENT.collees).toBe(127)
  })
})
