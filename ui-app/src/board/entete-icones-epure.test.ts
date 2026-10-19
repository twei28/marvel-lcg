// La rangée d'icônes d'en-tête des pages (`.reprise-boutons`) a UN style, en Normal (épuré) (18/10/2026).
// Constat de l'utilisateur : « pourquoi il n'y a que les deux premiers icônes qui ont le nouveau style ? » : FR et
// l'affichage avaient une règle dédiée, les autres icônes ne portaient que le fond gris plat de `.btn-icone` dès qu'elles
// n'étaient pas dans un `header.progress` (barre flottante de la page de préparation).
import { readFileSync } from 'node:fs'
import { dirname, join } from 'node:path'
import { fileURLToPath } from 'node:url'
import { describe, expect, it } from 'vitest'

const css = readFileSync(
  join(dirname(fileURLToPath(import.meta.url)), '../../../Fusion/marvel-lcg-src/public/css/affichage-epure-pages.css'),
  'utf8'
)

/** Le corps de la première règle dont la liste de sélecteurs contient `selecteur`. */
function regle(selecteur: string): string {
  const i = css.indexOf(selecteur)
  expect(i, selecteur).toBeGreaterThan(-1)
  const debut = css.indexOf('{', i)
  return css.slice(debut + 1, css.indexOf('}', debut))
}

describe('la rangée d icônes d en-tête, en Normal (épuré)', () => {
  it('toute icône de la rangée (btn-icone, bouton, lien) a le même fond, la même bordure et les mêmes coins coupés que FR', () => {
    const icones = regle('html[data-epure] .reprise-boutons .btn-icone,\nhtml[data-epure] .reprise-boutons > button,\nhtml[data-epure] .reprise-boutons > a {')
    const langue = regle('html[data-epure] header #zone-langue button,\nhtml[data-epure] header .btn-affichage {')
    for (const propriete of ['background: linear-gradient(180deg, #34415c 0%, #232c3f 100%) !important', 'border: 1px solid #4a5a7c !important', 'color: #dbe3f3 !important', 'clip-path: polygon(0 0, calc(100% - 7px) 0']) {
      expect(icones, propriete).toContain(propriete)
      expect(langue, propriete).toContain(propriete)
    }
  })

  it('le survol éclaircit le dégradé', () => {
    expect(css).toContain('html[data-epure] .reprise-boutons .btn-icone:hover')
    expect(regle('html[data-epure] .reprise-boutons .btn-icone:hover')).toContain('#4a5d82')
  })
})
