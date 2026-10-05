// La table personnalisable, etape 3 : l'ENREGISTREMENT. Une disposition par
// nombre de joueurs, dans le navigateur et sur le compte (decision du 04/10/2026).
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { DISPOSITION_DE_DEPART, DISPOSITION_ORIGINE, changerTaille, ecrireTable, zoneDe } from './table-briques'
import { CLE_TABLE, dispositionPour, enregistrerDisposition, tablesDuCompte, synchroniserTables } from './table-perso'

const envois: unknown[] = []
beforeEach(() => {
  envois.length = 0
  vi.stubGlobal('fetch', vi.fn(async (_url: string, init?: RequestInit) => {
    if (init?.body) envois.push(JSON.parse(String(init.body)))
    return new Response('{}')
  }))
})
afterEach(() => {
  window.localStorage.clear()
  vi.unstubAllGlobals()
})

const grande = changerTaille(DISPOSITION_DE_DEPART, 'main', 1.3)

describe('une disposition par nombre de joueurs', () => {
  it('sans choix : la disposition d origine', () => {
    expect(dispositionPour(1)).toBe(DISPOSITION_ORIGINE)
  })

  it('enregistre pour un nombre de joueurs, sans toucher aux autres, et previent le compte', () => {
    enregistrerDisposition(2, grande)
    expect(zoneDe(dispositionPour(2), 'main')?.taille).toBe(1.3)
    expect(dispositionPour(1)).toBe(DISPOSITION_ORIGINE)
    expect(envois).toEqual([{ changements: { 'table-2': ecrireTable(grande) } }])
  })

  it('« Disposition d origine » efface le choix, ici et sur le compte', () => {
    enregistrerDisposition(3, grande)
    enregistrerDisposition(3, undefined)
    expect(dispositionPour(3)).toBe(DISPOSITION_ORIGINE)
    expect(envois.at(-1)).toEqual({ changements: { 'table-3': null } })
  })

  it('un stockage abime revient a l origine (remise en ordre)', () => {
    window.localStorage.setItem(CLE_TABLE, JSON.stringify({ 'table-1': '12x8|abime' }))
    expect(dispositionPour(1)).toBe(DISPOSITION_ORIGINE)
    window.localStorage.setItem(CLE_TABLE, '{pas du json')
    expect(dispositionPour(1)).toBe(DISPOSITION_ORIGINE)
  })
})

describe('le compte fait foi quand il existe (meme contrat que la teinte)', () => {
  it('ne lit que les tables valides du compte', () => {
    const texte = ecrireTable(grande)
    expect(tablesDuCompte({ compte: true, existe: true, preferences: { 'table-4': texte, 'table-2': 'x', teinte: '1,1,10' } }))
      .toEqual({ 'table-4': texte })
    expect(tablesDuCompte({ compte: false, existe: false, preferences: {} })).toBeUndefined()
  })

  it('aligne le navigateur sur le compte', () => {
    enregistrerDisposition(1, grande, false)
    synchroniserTables({ 'table-4': ecrireTable(grande) })
    expect(dispositionPour(1)).toBe(DISPOSITION_ORIGINE)
    expect(zoneDe(dispositionPour(4), 'main')?.taille).toBe(1.3)
  })
})
