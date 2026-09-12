// Les panneaux du plateau portrait sont des FEUILLES (spec du 07/09/2026, §5).
//
// jsdom ne fait pas de mise en page : on verrouille la REGLE dans la feuille,
// comme deroule-survol.test.ts, et la classe que board.tsx pose sur body.
import { readFileSync } from 'node:fs'
import { describe, expect, it } from 'vitest'
import { enModeFeuille } from '../placement/usePlacement'

const CSS = readFileSync('src/board/mobile/menus-mobile.css', 'utf-8')

/** Le bloc de declarations qui suit un selecteur, sans les regles voisines. */
function blocContenant(selecteur: string): string {
  const debut = CSS.indexOf(selecteur)
  expect(debut, `selecteur absent de menus-mobile.css : ${selecteur}`).toBeGreaterThan(-1)
  const ouvre = CSS.indexOf('{', debut)
  return CSS.slice(ouvre, CSS.indexOf('}', ouvre))
}

describe('menus-mobile.css : les panneaux deviennent des feuilles', () => {
  it.each([
    '.popover-sauvegardes',
    '.historique-panneau',
    '.demande-centrale:not(.est-en-scene)',
    '.plateau-selecteur',
    '.plateau-regardees',
    '.panneau-journal',
    '.salon-panneau',
    '.menu-actions-carte',
  ])('%s est colle en bas de l’ecran, sous la classe du plateau portrait', (selecteur) => {
    expect(CSS).toContain(`body.mode-plateau-portrait ${selecteur}`)
    const bloc = blocContenant(`body.mode-plateau-portrait ${selecteur}`)
    expect(bloc).toContain('position: fixed')
    expect(bloc).toContain('bottom: var(--feuille-bas, 96px)')
    expect(bloc).toContain('max-height: calc(100dvh - var(--feuille-bas, 96px) - 44px)')
  })

  it('l’apercu au survol est masque au doigt', () => {
    expect(blocContenant('body.mode-plateau-portrait .carte-apercu')).toContain('display: none')
  })

  it('rien ne s’applique sans la classe : chaque regle commence par body.mode-plateau-portrait', () => {
    const selecteurs = CSS.split('\n').filter((l) => /^  [.a-z]/.test(l))
    for (const l of selecteurs) expect(l.trim().startsWith('body.mode-plateau-portrait')).toBe(true)
  })
})

describe('enModeFeuille', () => {
  it('suit la classe posee sur body', () => {
    document.body.classList.remove('mode-plateau-portrait')
    expect(enModeFeuille()).toBe(false)
    document.body.classList.add('mode-plateau-portrait')
    expect(enModeFeuille()).toBe(true)
    document.body.classList.remove('mode-plateau-portrait')
  })
})
