// L'inversion du deck et de la defausse (demande d'un joueur, 03/11/2026) : un seul reglage, garde dans le navigateur,
// qui ne passe que par `data-piles-inversees` sur <html> ; board.css echange alors la premiere pile de chaque groupe.
import { readFileSync } from 'node:fs'
import { dirname, join } from 'node:path'
import { fileURLToPath } from 'node:url'
import { act, renderHook } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it } from 'vitest'
import { appliquerInversionPiles, CLE_INVERSION_PILES, ecrireInversionPiles, lireInversionPiles, useInversionPiles } from './inversion-piles'

const ici = dirname(fileURLToPath(import.meta.url))

describe('reglage « Inverser le deck et la defausse »', () => {
  beforeEach(() => {
    window.localStorage.removeItem(CLE_INVERSION_PILES)
    delete document.documentElement.dataset.pilesInversees
  })
  afterEach(() => {
    window.localStorage.removeItem(CLE_INVERSION_PILES)
    delete document.documentElement.dataset.pilesInversees
  })

  it('est desactive par defaut', () => {
    expect(lireInversionPiles()).toBe(false)
  })

  it('se retient dans le navigateur', () => {
    ecrireInversionPiles(true)
    expect(window.localStorage.getItem(CLE_INVERSION_PILES)).toBe('oui')
    expect(lireInversionPiles()).toBe(true)
    ecrireInversionPiles(false)
    expect(lireInversionPiles()).toBe(false)
  })

  it('une valeur abimee vaut « desactive »', () => {
    window.localStorage.setItem(CLE_INVERSION_PILES, '??')
    expect(lireInversionPiles()).toBe(false)
  })

  it("pose et retire l'attribut de <html>", () => {
    appliquerInversionPiles(true)
    expect(document.documentElement.dataset.pilesInversees).toBe('oui')
    appliquerInversionPiles(false)
    expect(document.documentElement.dataset.pilesInversees).toBeUndefined()
  })

  it("le hook suit le reglage sans recharger, et rend <html> propre au demontage", () => {
    const { result, unmount } = renderHook(() => useInversionPiles())
    expect(result.current).toBe(false)
    expect(document.documentElement.dataset.pilesInversees).toBeUndefined()
    act(() => ecrireInversionPiles(true))
    expect(result.current).toBe(true)
    expect(document.documentElement.dataset.pilesInversees).toBe('oui')
    act(() => ecrireInversionPiles(false))
    expect(document.documentElement.dataset.pilesInversees).toBeUndefined()
    act(() => ecrireInversionPiles(true))
    unmount()
    expect(document.documentElement.dataset.pilesInversees).toBeUndefined()
  })

  it('le reglage etait deja actif a l\'ouverture : le plateau s\'ouvre inverse', () => {
    ecrireInversionPiles(true)
    renderHook(() => useInversionPiles())
    expect(document.documentElement.dataset.pilesInversees).toBe('oui')
  })
})

describe('board.css : la regle qui echange les piles', () => {
  const css = readFileSync(join(ici, 'board.css'), 'utf8').replace(/\/\*[\s\S]*?\*\//g, '')

  it('couvre le joueur, la rencontre et le deck special, et laisse la defausse en place', () => {
    const regle = css.match(/html\[data-piles-inversees='oui'\][^{]*\{[^}]*\}/)
    expect(regle, 'regle `data-piles-inversees` introuvable dans board.css').not.toBeNull()
    const [texte] = regle as RegExpMatchArray
    for (const zone of ['zone-piles-joueur', 'zone-piles-rencontre', 'zone-deck-special']) {
      expect(texte).toContain(`.${zone} .plateau-groupe > :first-child`)
    }
    expect(texte).toMatch(/order:\s*2/)
  })
})
