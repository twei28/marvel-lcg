// Le liseré des cartes SHINOBI du pack TMNT quand la table est délavée (18/10/2026, réponses de l'utilisateur,
// questions une à une) : un liseré par classe, de la couleur de la barre du bas de ses cartes ; une carte Dual
// (deux classes) porte un DÉGRADÉ des deux couleurs, comme sa barre.
import { readFileSync } from 'node:fs'
import { dirname, join } from 'node:path'
import { fileURLToPath } from 'node:url'
import { describe, expect, it } from 'vitest'
import { aspectDeClasse } from './catalogue'

const ici = dirname(fileURLToPath(import.meta.url))
const css = readFileSync(join(ici, 'board.css'), 'utf8')

// Couleurs prélevées sur les scans (barre du bas) : sb001, sj001, sa001, sh001.
const COULEURS: Record<string, string> = {
  bushido: '#20f8d0',
  'kuji-kiri': '#f800a8',
  ninjutsu: '#9870e0',
  taijutsu: '#f87800',
}

describe('aspectDeClasse, classes Shinobi', () => {
  it('chaque classe est son propre aspect', () => {
    expect(aspectDeClasse('Bushido')).toBe('bushido')
    expect(aspectDeClasse('Kuji-Kiri')).toBe('kuji-kiri')
    expect(aspectDeClasse('Ninjutsu')).toBe('ninjutsu')
    expect(aspectDeClasse('Taijutsu')).toBe('taijutsu')
  })

  it('une Dual porte les deux classes, dans l ordre imprime', () => {
    expect(aspectDeClasse('Bushido;Ninjutsu')).toBe('bushido-ninjutsu')
    expect(aspectDeClasse('Kuji-Kiri;Taijutsu')).toBe('kuji-kiri-taijutsu')
    expect(aspectDeClasse('Ninjutsu;Taijutsu')).toBe('ninjutsu-taijutsu')
  })

  it('la carte des quatre classes est « shinobi »', () => {
    expect(aspectDeClasse('Bushido;Kuji-Kiri;Ninjutsu;Taijutsu')).toBe('shinobi')
  })

  it('une signature « Hero;Taijutsu » est Taijutsu : un aspect l emporte sur Hero, comme pour les autres', () => {
    expect(aspectDeClasse('Hero;Taijutsu')).toBe('taijutsu')
  })

  it('les aspects existants ne changent pas', () => {
    expect(aspectDeClasse('Aggression')).toBe('aggression')
    expect(aspectDeClasse('Hero')).toBe('hero')
    expect(aspectDeClasse('Campaign;Basic')).toBe('basic')
    expect(aspectDeClasse('Campaign')).toBeUndefined()
  })
})

describe('board.css, liseré Shinobi', () => {
  it('chaque classe a sa couleur, celle de la barre de ses cartes', () => {
    for (const [classe, couleur] of Object.entries(COULEURS)) {
      expect(css).toContain(`.plateau.est-delave .scan-card.aspect-${classe} { --lisere-aspect: ${couleur}; }`)
    }
  })

  it('chaque Dual et la carte des quatre classes ont un dégradé', () => {
    for (const dual of ['bushido-kuji-kiri', 'bushido-ninjutsu', 'bushido-taijutsu', 'kuji-kiri-ninjutsu', 'kuji-kiri-taijutsu', 'ninjutsu-taijutsu', 'shinobi']) {
      expect(css, dual).toContain(`.plateau.est-delave .scan-card.aspect-${dual} .scan-frame`)
    }
    expect(css).toContain('linear-gradient(90deg, var(--lisere-a), var(--lisere-b))')
  })
})

// L'EPURE (18/10/2026, « c'est parfait pour l'epure ») : le meme liseré, pour TOUS les aspects et les Shinobi,
// de 1,5 px (la moitie de la premiere simulation), sans qu'il faille l'effet delave.
describe('affichage-epure.css, liseré des cartes', () => {
  const epure = readFileSync(join(ici, '../../styles/affichage-epure.css'), 'utf8')

  it('chaque aspect et chaque classe Shinobi a sa couleur', () => {
    const attendues: Record<string, string> = {
      aggression: '#d1382c', justice: '#e6be3c', leadership: '#3f86e0', protection: '#34ae61', pool: '#ef67b0',
      determination: '#965cc4', venomized: '#6b6b7a', hero: '#a878e8', basic: '#aab3bd', ...COULEURS,
    }
    for (const [aspect, couleur] of Object.entries(attendues)) {
      expect(epure, aspect).toContain(`html[data-epure] .scan-card.aspect-${aspect} { --lisere-aspect: ${couleur}; }`)
    }
  })

  it('le trait fait 1,5 px et prend la couleur de l aspect', () => {
    expect(epure).toContain("html[data-epure] .scan-card[class*='aspect-'] .scan-frame")
    expect(epure).toContain('border: 1.5px solid var(--lisere-aspect, transparent)')
  })

  it('chaque Dual et la carte des quatre classes ont leur dégradé', () => {
    for (const dual of ['bushido-kuji-kiri', 'bushido-ninjutsu', 'bushido-taijutsu', 'kuji-kiri-ninjutsu', 'kuji-kiri-taijutsu', 'ninjutsu-taijutsu', 'shinobi']) {
      expect(epure, dual).toContain(`html[data-epure] .scan-card.aspect-${dual} .scan-frame`)
    }
    expect(epure).toContain('linear-gradient(90deg, var(--lisere-a), var(--lisere-b))')
  })
})
