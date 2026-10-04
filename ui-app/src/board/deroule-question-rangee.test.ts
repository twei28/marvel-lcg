// Les choix de defense COTE A COTE (capture du 04/10/2026 : Hulk au-dessus,
// Black Widow et « Ne pas défendre » dessous). Verrous sur la FEUILLE : jsdom
// ne calcule pas la mise en page.
import { describe, expect, it } from 'vitest'
import fs from 'node:fs'
import path from 'node:path'

const css = fs.readFileSync(path.join(__dirname, 'deroule-onglets.css'), 'utf8').replace(/\/\*[\s\S]*?\*\//g, '')
const bloc = (selecteur: string) => {
  const i = css.lastIndexOf(selecteur + ' {')
  return i < 0 ? '' : css.slice(i, css.indexOf('}', i))
}

describe('la question de defense en scene', () => {
  it('ne replie jamais ses choix sur deux lignes', () => {
    const regle = bloc('.deroule-phase.est-question .dc-boutons')
    expect(regle).toContain('flex-wrap: nowrap')
    expect(regle).toContain('max-width: none')
  })

  it('partage la largeur entre les choix au lieu de deborder du cadre', () => {
    const regle = bloc('.deroule-phase.est-question .dc-boutons > .af-action-wrap')
    expect(regle).toContain('flex: 1 1 0')
    expect(regle).toContain('min-width: 0')
    expect(bloc('.deroule-phase.est-question .dc-boutons .af-action')).toContain('white-space: normal')
  })

  it('plusieurs defenseurs : le titre passe au-dessus, une seule colonne', () => {
    const regle = bloc('.deroule-phase.est-question:has(.af-action-wrap.a-vignette ~ .af-action-wrap.a-vignette)')
    expect(regle).toContain('grid-template-columns: minmax(0, auto)')
  })
})
