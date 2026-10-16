// @vitest-environment node
// L'import d'un deck OCTGN (.o8d) : public/js/marvelcdb/octgn.js (16/10/2026).
import { describe, it, expect } from 'vitest'
import fs from 'node:fs'
import path from 'node:path'
import * as module_ from '../../Fusion/marvel-lcg-src/public/js/marvelcdb/octgn.js'

// Module JS servi tel quel : ses types inferes sont trop etroits pour les faux du test.
// eslint-disable-next-line @typescript-eslint/no-explicit-any
const { lireO8d, versSlots, indexParNom } = module_ as any

const RACINE = path.resolve(__dirname, '../..')
const FICHIER = fs.readFileSync(path.join(RACINE, 'ui-check/tests/fixtures/Beast_Brain_over_Brawl.o8d'), 'utf8')
const TABLE = JSON.parse(fs.readFileSync(path.join(RACINE, 'Fusion/marvel-lcg-src/data/octgn_guids.json'), 'utf8'))

describe('lireO8d', () => {
  it("lit les 31 lignes (47 cartes) d'un vrai deck, apostrophes comprises", () => {
    const d = lireO8d(FICHIER)
    expect(d.cartes).toHaveLength(31)
    expect(d.cartes.reduce((s: number, c: { qte: number }) => s + c.qte, 0)).toBe(47)
    expect(d.cartes.map((c: { nom: string }) => c.nom)).toContain("Beast's Lab")
  })
  it("refuse ce qui n'est pas un deck", () => {
    expect(lireO8d('{"json": true}')).toBeNull()
    expect(lireO8d('<deck></deck>')).toBeNull()
    expect(lireO8d('')).toBeNull()
  })
  it('decode les entites et ignore une quantite absurde', () => {
    const d = lireO8d('<deck><card qty="2" id="AB-1">Tom &amp; Jerry &#039;s</card><card qty="0" id="x">Rien</card></deck>')
    expect(d.cartes).toEqual([{ qte: 2, guid: 'ab-1', nom: "Tom & Jerry 's" }])
  })
})

describe('versSlots', () => {
  const catalogue = [
    { card_id: '01088', name: 'Energy' }, { card_id: '01089', name: 'Genius' }, { card_id: '16022', name: 'Genius' },
    { card_id: '01081', name: 'Armored Vest' }, { card_id: '35020', name: 'Aggressive Energy' }, { card_id: 'bt002', name: '* Wonder Man' },
  ]
  const sources = {
    parGuid: TABLE,
    existe: (c: string) => catalogue.some((x) => x.card_id === c),
    parNom: indexParNom(catalogue),
  }
  it('retrouve par GUID, retombe sur le nom, et rend ce qui reste', () => {
    const r = versSlots(lireO8d(FICHIER), sources)
    expect(r.total).toBe(47)
    expect(r.slots['01088']).toBe(1)                       // Energy, par GUID
    expect(r.slots['01081']).toBe(1)                       // Armored Vest, par GUID
    expect(r.slots['01089']).toBe(1)                       // Genius : GUID 32023 absent du jeu -> nom, la plus ancienne edition
    expect(r.slots['35020']).toBe(2)                       // Aggressive Energy : GUID vers 32047 absent -> nom
    const noms = r.inconnues.map((c: { nom: string }) => c.nom)
    expect(noms).toContain('Addition by Subtraction')      // carte propre a un autre Beast : rendue, pas tuee
    expect(r.inconnues.reduce((s: number, c: { qte: number }) => s + c.qte, 0) + Object.values(r.slots).reduce((s: number, n: unknown) => s + (n as number), 0)).toBe(47)
  })
  it("l'index par nom ne garde que les cartes officielles, la plus ancienne gagnant", () => {
    const idx = indexParNom(catalogue)
    expect(idx.get('genius')).toBe('01089')
    expect(idx.has('* wonder man')).toBe(false)
  })
})
