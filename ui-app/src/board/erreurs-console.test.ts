// Une erreur console est souvent la seule trace d'un bug de rendu, et elle
// disparait avec l'onglet. On les garde donc en memoire, plafonnees, pour que
// le rapport de bug puisse les recopier.
import { afterEach, beforeEach, describe, expect, it } from 'vitest'
import { erreursRecentes, installerCollecteErreurs, viderErreurs } from './erreurs-console'

let desinstaller: (() => void) | undefined

beforeEach(() => viderErreurs())
afterEach(() => {
  desinstaller?.()
  desinstaller = undefined
})

describe('collecte des erreurs console', () => {
  it('retient ce qui passe par console.error', () => {
    desinstaller = installerCollecteErreurs()
    console.error('boum', 42)
    expect(erreursRecentes()).toEqual(['boum 42'])
  })

  it('laisse console.error faire son travail', () => {
    const vus: unknown[][] = []
    const original = console.error
    console.error = (...args: unknown[]) => void vus.push(args)
    desinstaller = installerCollecteErreurs()
    console.error('toujours affiche')
    desinstaller()
    desinstaller = undefined
    console.error = original
    expect(vus).toEqual([['toujours affiche']])
  })

  it('plafonne a 20 et garde les plus RECENTES', () => {
    desinstaller = installerCollecteErreurs()
    for (let i = 0; i < 25; i += 1) console.error(`erreur ${i}`)
    const gardees = erreursRecentes()
    expect(gardees).toHaveLength(20)
    expect(gardees[0]).toBe('erreur 5')
    expect(gardees[19]).toBe('erreur 24')
  })

  it('rend la console intacte apres desinstallation', () => {
    const avant = console.error
    installerCollecteErreurs()()
    expect(console.error).toBe(avant)
  })

  it("n'empile pas deux relais quand on installe deux fois", () => {
    desinstaller = installerCollecteErreurs()
    const seconde = installerCollecteErreurs()
    console.error('une seule fois')
    seconde()
    expect(erreursRecentes()).toEqual(['une seule fois'])
  })

  it('nomme les Error par leur type et leur message', () => {
    desinstaller = installerCollecteErreurs()
    console.error(new TypeError('carte introuvable'))
    expect(erreursRecentes()).toEqual(['TypeError: carte introuvable'])
  })
})
