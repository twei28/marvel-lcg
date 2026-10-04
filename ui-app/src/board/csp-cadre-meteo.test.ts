// Le voile blanc avec un visage triste au milieu (signalé le 30/09/2026).
//
// La couche météo (CoucheMeteo) charge `/effects/weather/<ambiance>.html` dans
// une iframe du MÊME site. L'en-tête `frame-ancestors` posé le 28/09 pour
// l'activité Discord n'autorisait que Discord : le navigateur refusait donc la
// page, affichait sa page d'erreur (visage triste) en plein écran, à 55 %
// d'opacité, soit un voile blanc sur tout le plateau dès qu'une ambiance
// s'allumait. `'self'` doit figurer dans chaque `frame-ancestors`.
import { describe, expect, it } from 'vitest'
import { readFileSync } from 'node:fs'
import { dirname, join } from 'node:path'
import { fileURLToPath } from 'node:url'

const ici = dirname(fileURLToPath(import.meta.url))

describe('en-tête frame-ancestors du Caddyfile', () => {
  it('autorise le site à s’encadrer lui-même, sinon la couche météo est bloquée', () => {
    const caddyfile = readFileSync(join(ici, '../../../deploiement/Caddyfile'), 'utf-8')
    const lignes = caddyfile.split('\n').filter((l) => /^\s*header Content-Security-Policy/.test(l))
    expect(lignes.length).toBeGreaterThan(0)
    for (const ligne of lignes) expect(ligne).toContain("frame-ancestors 'self'")
  })
})
