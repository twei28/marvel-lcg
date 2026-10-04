// Plus de halo rouge autour de la main du joueur (demande de l'utilisateur,
// 04/10/2026). La lueur venait d'UNE regle : `.deroule-question .plateau-scene
// .zone-main` posait une ombre et un fond rgba(166, 0, 0, …) sur toute la
// boite de la main, quasi invisibles sur le fond noir d'origine, mais une
// nappe pourpre des que la table est teintee. Verrou sur la FEUILLE (jsdom ne
// calcule pas les ombres).
import { describe, expect, it } from 'vitest'
import fs from 'node:fs'
import path from 'node:path'

const css = fs.readFileSync(path.join(__dirname, 'board.css'), 'utf8').replace(/\/\*[\s\S]*?\*\//g, '')

function bloc(selecteur: string): string {
  const i = css.indexOf(selecteur)
  if (i < 0) return ''
  return css.slice(i, css.indexOf('}', i))
}

describe('la main pendant une question du moteur', () => {
  it('sort du voile (z-index) mais sans lueur rouge ni fond colore', () => {
    const regle = bloc('.deroule-question .plateau-scene .zone-main')
    expect(regle, 'la regle qui sort la main du voile doit rester').toContain('z-index: 120')
    expect(regle).not.toContain('166, 0, 0')
    expect(regle).not.toMatch(/box-shadow/)
    expect(regle).not.toMatch(/background/)
  })

  it('aucune autre regle ne colore la boite de la main en rouge', () => {
    const regles = [...css.matchAll(/([^{}]*\.zone-main[^{}]*)\{([^}]*)\}/g)]
    expect(regles.length).toBeGreaterThan(0)
    for (const [, selecteur, corps] of regles) {
      expect(corps, selecteur.trim()).not.toContain('166, 0, 0')
    }
  })
})
