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

describe('la main pendant une question du moteur', () => {
  // ⚠ LA REGLE ELLE-MEME EST PARTIE (lot 3 de la refonte du cartouche,
  // 05/10/2026). Elle sortait la main du voile tant que `body.deroule-question`
  // etait pose ; la scene PC cache desormais la main pendant la phase (D3) et
  // le composant ne pose plus cette classe. Une regle restee la viserait un
  // body qui ne la porte jamais.
  it('aucune regle ne vise plus le body pendant une question (body.deroule-question)', () => {
    expect(css).not.toMatch(/\.deroule-question\s+\.plateau-scene/)
  })

  it('aucune autre regle ne colore la boite de la main en rouge', () => {
    const regles = [...css.matchAll(/([^{}]*\.zone-main[^{}]*)\{([^}]*)\}/g)]
    expect(regles.length).toBeGreaterThan(0)
    for (const [, selecteur, corps] of regles) {
      expect(corps, selecteur.trim()).not.toContain('166, 0, 0')
    }
  })
})
