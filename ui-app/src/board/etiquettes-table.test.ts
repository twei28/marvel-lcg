import { afterEach, describe, expect, it } from 'vitest'
import { CLASSE_ETIQUETTES_TABLE, ecrireEtiquettesTable, lireEtiquettesTable } from './etiquettes-table'

afterEach(() => {
  window.localStorage.clear()
  document.body.classList.remove(CLASSE_ETIQUETTES_TABLE)
})

describe('etiquettes de type sur la table', () => {
  it('absentes par defaut', () => {
    expect(lireEtiquettesTable()).toBe(false)
  })
  it('l interrupteur les remet, et le choix est garde', () => {
    ecrireEtiquettesTable(true)
    expect(document.body.classList.contains(CLASSE_ETIQUETTES_TABLE)).toBe(true)
    expect(lireEtiquettesTable()).toBe(true)
    ecrireEtiquettesTable(false)
    expect(document.body.classList.contains(CLASSE_ETIQUETTES_TABLE)).toBe(false)
  })
})
