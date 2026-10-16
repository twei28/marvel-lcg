// La feuille de la « Phase dynamique » : ses garde-fous (16/10/2026).
import { readFileSync } from 'node:fs'
import { join } from 'node:path'
import { describe, expect, it } from 'vitest'

const feuille = readFileSync(join(__dirname, 'cartouche-dynamique.css'), 'utf8')
const sansCommentaires = feuille.replace(/\/\*[\s\S]*?\*\//g, '')

/** Les règles « normales » : on ignore les @keyframes et le contenu des @media (traités à part). */
function selecteurs(css: string): string[] {
  const sansBlocsAt = css.replace(/@keyframes[^{]*\{(?:[^{}]*\{[^{}]*\})*[^{}]*\}/g, '')
  return [...sansBlocsAt.matchAll(/([^{}@]+)\{[^{}]*\}/g)]
    .flatMap((m) => m[1].split(','))
    .map((s) => s.trim())
    .filter(Boolean)
}

describe('cartouche-dynamique.css', () => {
  it('chaque règle est sous .est-dynamique, ou propre aux pièces .dyn-*', () => {
    const hors = selecteurs(sansCommentaires).filter((s) => !s.includes('.est-dynamique') && !s.startsWith('.dyn-'))
    expect(hors).toEqual([])
  })

  it('les autres présentations n’héritent de rien : aucune règle sur le body ni sur la racine hors @media d’animation', () => {
    const racine = selecteurs(sansCommentaires).filter((s) => /^(html|body)\b/.test(s) && !s.includes('.est-dynamique'))
    expect(racine).toEqual([])
  })

  it('la section ne déclare jamais `transform` (le déplacement à la main pose un `translate` inline)', () => {
    const regle = /\.est-dynamique\s*\{[^}]*\}/.exec(sansCommentaires)?.[0] ?? ''
    expect(regle).not.toMatch(/(^|[;{\s])transform\s*:/)
  })

  it('le panneau reste dans l’écran : ancré en haut et en bas, plafonné en hauteur, jamais plus large que l’écran', () => {
    const regle = /\.deroule-phase\.est-scene\.est-bis\.est-dynamique\s*\{[^}]*\}/.exec(sansCommentaires)?.[0] ?? ''
    expect(regle).toMatch(/max-height:\s*calc\(100dvh/)
    expect(regle).toMatch(/inset:\s*\d+px \d+px \d+px auto/)
    expect(regle).toMatch(/width:\s*var\(--dyn-l\)/)
  })

  it('le corps défile en interne et le pied reste fixe', () => {
    expect(sansCommentaires).toMatch(/\.est-dynamique \.deroule-corps\s*\{[^}]*overflow-y:\s*auto/)
    expect(sansCommentaires).toMatch(/\.est-dynamique \.deroule-boutons\s*\{[^}]*flex:\s*none/)
  })

  it('aucune couche décorative ne capte les clics', () => {
    expect(sansCommentaires).not.toMatch(/position:\s*fixed;[^}]*inset:\s*0[^}]*\}/)
  })

  it('l’animation d’entrée se coupe en sobre, en mouvement réduit et sans animations', () => {
    expect(feuille).toMatch(/prefers-reduced-motion/)
    expect(feuille).toMatch(/plateau-sans-animations/)
    expect(feuille).toMatch(/data-affichage='sobre'/)
  })
})
