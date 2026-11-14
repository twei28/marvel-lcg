// La zone « Mises de côté / autres piles » défile quand ses piles passent sur deux rangées (scénario Mephisto à DEUX joueurs :
// pile de mises de côté + une Damnation par joueur = 3 piles). Sans l'alignement « safe », le haut des piles débordait vers le
// haut, hors de portée du défilement : on n'en voyait qu'un liseré (constaté dans Chromium le 09/11/2026).
import { readFileSync } from 'node:fs'
import { describe, expect, it } from 'vitest'

const css = readFileSync('src/board/board.css', 'utf8')

function regle(selecteur: string): string {
  const i = css.indexOf(`${selecteur} {`)
  expect(i, `règle « ${selecteur} » introuvable`).toBeGreaterThan(-1)
  return css.slice(i, css.indexOf('}', i))
}

describe('zone des annexes (piles de côté, Damnation)', () => {
  it('défile plutôt que de déborder vers le haut', () => {
    const r = regle('.zone-annexes')
    expect(r).toContain('overflow-y: auto')
    expect(r).toContain('align-items: safe flex-end')
  })
})
