// Constat du 06/10/2026 (lot 7, navigateur) : dans « Déplacer vers », le
// bouton « Sous la pile » prenait toute la largeur et écrasait le nom de la
// pile sur trois lignes (« Deck / du / héros »). Cause : `.menu-triche-liste
// button { width: 100% }` est plus spécifique que `.menu-triche-sous { width:
// auto }`. jsdom ne calcule pas la cascade : on lit la feuille elle-même.
import { readFileSync } from 'node:fs'
import { describe, expect, it } from 'vitest'

const css = readFileSync('src/board/board.css', 'utf-8')

function regle(selecteur: string): string | undefined {
  const echappe = selecteur.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
  return new RegExp(`(?:^|[\\s}])${echappe}\\s*\\{([^}]*)\\}`).exec(css)?.[1]
}

describe('« Sous la pile » garde sa largeur naturelle', () => {
  it('une règle au moins aussi spécifique que `.menu-triche-liste button` lui rend width: auto', () => {
    const corps = regle('.menu-triche-liste button.menu-triche-sous')
    expect(corps, 'aucune règle `.menu-triche-liste button.menu-triche-sous`').toBeDefined()
    expect(corps).toMatch(/width:\s*auto/)
  })
})
