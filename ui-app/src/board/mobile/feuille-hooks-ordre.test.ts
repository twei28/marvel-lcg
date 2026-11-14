// ⚠ Garde : le hook de la feuille de choix de cible doit etre declare AVANT le retour anticipe de board.tsx
// (`if (!etat.monde || !plateau || voile)`). Place apres, le nombre de hooks change quand la partie apparait : erreur React 310, ecran
// noir (vu au premier essai dans un vrai navigateur, 26/10/2026 ; les tests de composants ne le voient pas).
import { readFileSync } from 'node:fs'
import { dirname, join } from 'node:path'
import { fileURLToPath } from 'node:url'
import { describe, expect, it } from 'vitest'

describe('board.tsx : l ordre des hooks', () => {
  it('feuilleCibles est declare avant le retour anticipe de la partie', () => {
    const source = readFileSync(join(dirname(fileURLToPath(import.meta.url)), '../../board.tsx'), 'utf8')
    const hook = source.indexOf('const feuilleCibles = useMemo(')
    const retour = source.indexOf('if (!etat.monde || !plateau || voile) {')
    expect(hook).toBeGreaterThan(0)
    expect(retour).toBeGreaterThan(0)
    expect(hook).toBeLessThan(retour)
  })
})
