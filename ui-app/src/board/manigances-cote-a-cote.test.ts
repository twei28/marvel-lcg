// Plusieurs manigances principales cote a cote (10/10/2026, Tower Defense) :
// la zone principale d'une table personnalisee prend ses cases sur les annexes.
import { describe, expect, it } from 'vitest'
import fs from 'node:fs'
import path from 'node:path'
import {
  DISPOSITION_DE_DEPART,
  DISPOSITION_ORIGINE,
  elargirManigancePrincipale,
  zoneDe,
  type Disposition,
} from './table-briques'

const SCENE = 1920

const largeurs = (d: Disposition) => ({
  principale: zoneDe(d, 'manigance-principale')!,
  annexes: zoneDe(d, 'manigances-annexes')!,
})

describe('elargirManigancePrincipale', () => {
  it('ne touche ni la table d’origine ni une seule principale', () => {
    expect(elargirManigancePrincipale(DISPOSITION_ORIGINE, 3, SCENE)).toBe(DISPOSITION_ORIGINE)
    expect(elargirManigancePrincipale(DISPOSITION_DE_DEPART, 1, SCENE)).toBe(DISPOSITION_DE_DEPART)
  })

  it('élargit la principale à droite en prenant sur les annexes, les autres zones ne bougent pas', () => {
    const avant = largeurs(DISPOSITION_DE_DEPART)
    for (const nombre of [2, 3]) {
      const d = elargirManigancePrincipale(DISPOSITION_DE_DEPART, nombre, SCENE)
      const { principale, annexes } = largeurs(d)
      expect(principale.col).toBe(avant.principale.col)
      expect(principale.largeur * (SCENE / 12)).toBeGreaterThanOrEqual(nombre * 210)
      expect(annexes.col).toBe(principale.col + principale.largeur)
      expect(annexes.col + annexes.largeur).toBe(avant.annexes.col + avant.annexes.largeur)
      expect(annexes.largeur).toBeGreaterThanOrEqual(1)
      const autres = d.zones.filter((z) => z !== principale && z !== annexes)
      expect(autres).toEqual(DISPOSITION_DE_DEPART.zones.filter((z) => !z.briques.some((b) => b.startsWith('manigance'))))
    }
  })

  it('laisse toujours au moins une case aux annexes', () => {
    const d = elargirManigancePrincipale(DISPOSITION_DE_DEPART, 12, SCENE)
    expect(largeurs(d).annexes.largeur).toBe(1)
  })

  it('élargit vers la gauche quand les annexes sont à gauche', () => {
    const inverse: Disposition = {
      ...DISPOSITION_DE_DEPART,
      zones: DISPOSITION_DE_DEPART.zones.map((z) =>
        z.briques.includes('manigance-principale')
          ? { ...z, col: 10 }
          : z.briques.includes('manigances-annexes')
            ? { ...z, col: 5 }
            : z
      ),
    }
    const { principale, annexes } = largeurs(elargirManigancePrincipale(inverse, 2, SCENE))
    expect(principale.col + principale.largeur).toBe(13)
    expect(annexes.col).toBe(5)
    expect(annexes.col + annexes.largeur).toBe(principale.col)
  })

  it('ne fait rien quand les annexes ne la jouxtent pas sur les mêmes rangées', () => {
    const ailleurs: Disposition = {
      ...DISPOSITION_DE_DEPART,
      zones: DISPOSITION_DE_DEPART.zones.map((z) =>
        z.briques.includes('manigances-annexes') ? { ...z, ligne: 3 } : z
      ),
    }
    expect(elargirManigancePrincipale(ailleurs, 2, SCENE)).toBe(ailleurs)
  })
})

describe('bande des manigances (table d’origine)', () => {
  it('les principales restent sur une seule ligne', () => {
    const css = fs.readFileSync(path.join(__dirname, 'bande-manigances.css'), 'utf8')
    expect(css).toMatch(/\.zone-complot-principal \.plateau-cartes,[\s\S]*?flex-wrap: nowrap/)
  })
})
