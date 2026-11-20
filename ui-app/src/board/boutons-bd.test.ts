// Boutons des questions en style BD (decision du 04/10/2026) : verrous sur la
// FEUILLE elle-meme (jsdom ne calcule ni clip-path ni polices).
import { describe, expect, it } from 'vitest'
import fs from 'node:fs'
import path from 'node:path'

const lire = (nom: string) => fs.readFileSync(path.join(__dirname, nom), 'utf8')

describe('les boutons des questions en style BD', () => {
  it('une capacite est ambre, comme « jouer une carte » (plus mauve)', () => {
    const bloc = /\.tonalite-ability \{([^}]*)\}/.exec(lire('board.css'))?.[1] ?? ''
    expect(bloc).toContain('var(--menace)')
    expect(bloc).not.toContain('--statut')
  })

  it('ne touche QUE les panneaux de question, jamais les menus de carte', () => {
    const css = lire('boutons-bd.css').replace(/\/\*[\s\S]*?\*\//g, '')
    // Un `@media` n'est pas un selecteur : seules les regles qu'il contient comptent.
    const selecteurs = [...css.matchAll(/([^{}]+)\{/g)]
      .filter((m) => !m[1].trim().startsWith('@'))
      .flatMap((m) => m[1].split(',').map((s) => s.trim()))
    expect(selecteurs.length).toBeGreaterThan(0)
    // `:not(...)` reste dans le panneau : il ne fait que l'affiner (la question du centre hors cartouche).
    // Sur téléphone (commit 8cf9c6fe, 25/10/2026), la règle des boutons de défense s'écrit `body.mode-plateau-portrait .demande-centrale ...` :
    // le préfixe de mode ne sort pas du panneau, il le restreint au plateau en portrait.
    for (const s of selecteurs) expect(s).toMatch(/^(body\.mode-plateau-portrait )?\.(demande-centrale|assistant-action|deroule-phase)(:not\([^)]*\))? /)
  })

  it('le choix unique (Fin de phase) prend le jaune de « Continuer », en plus grand', () => {
    const css = lire('boutons-bd.css')
    const continuer = /\.demande-centrale \.dc-continue,\s*\.assistant-action \.assistant-confirmer,[^{]*\{([^}]*)\}/.exec(css)?.[1] ?? ''
    const unique = /\.demande-centrale \.dc-boutons\.est-choix-unique \.af-action \{([^}]*)\}/.exec(css)?.[1] ?? ''
    expect(continuer).toContain('background: var(--menace)')
    expect(unique).toContain('background: var(--menace)')
    expect(unique).toContain('color: #14100a')
    expect(unique).toMatch(/min-height: (\d+)px/)
    expect(Number(/min-height: (\d+)px/.exec(unique)?.[1])).toBeGreaterThan(48)
  })

  it('coins coupes, police Bangers, plus d arrondi ; refus gris', () => {
    const css = lire('boutons-bd.css')
    expect(css).toContain('clip-path: polygon(')
    expect(css).toContain("font-family: 'Bangers'")
    expect(css).toContain('border-radius: 0')
    expect(css).toMatch(/\.demande-centrale \.dc-pass[\s\S]*?color: #cbd5e1/)
  })
})
