// Le style de la pastille « Errata » suit la charte du site (décision du 09/11/2026) : bleu #3f86e0, coins ~4 px,
// jamais de pilule (999px) ni le doré de l'ancienne version.
import { readFileSync } from 'node:fs'
import { describe, expect, it } from 'vitest'

const css = readFileSync('src/board/errata.css', 'utf8')

describe('errata.css', () => {
  it('pas de pilule, pas de doré', () => {
    expect(css).not.toMatch(/999px/)
    expect(css).not.toMatch(/f4c430/i)
    expect(css).not.toMatch(/244,\s*196,\s*48/)
  })

  it('la pastille et la note ont des coins de 4 px et le bleu du site', () => {
    const mot = /\.pastille-errata-mot\s*\{[^}]*\}/.exec(css)?.[0] ?? ''
    expect(mot).toMatch(/border-radius:\s*4px/)
    expect(mot).toMatch(/#3f86e0/i)
    const note = /\.note-errata\s*\{[^}]*\}/.exec(css)?.[0] ?? ''
    expect(note).toMatch(/border-radius:\s*4px/)
  })
})
