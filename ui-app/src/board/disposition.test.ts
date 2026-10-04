// La TABLE PERSONNALISABLE, etape 1 (decision du 04/10/2026) : les zones du
// plateau PC decrites par des DONNEES, sans rien changer a l'ecran.
import { describe, expect, it } from 'vitest'
import fs from 'node:fs'
import path from 'node:path'
import {
  DISPOSITION_DE_DEPART,
  MINIMUMS,
  changerTaille,
  cleTable,
  deplacer,
  ecrireTable,
  lireTable,
  redimensionner,
  styleDeGrille,
  DISPOSITION_ORIGINE,
  ZONES,
  aireDeGrille,
  chevauchements,
  estValide,
  type Disposition,
} from './disposition'

const css = fs.readFileSync(path.join(__dirname, 'bande-manigances.css'), 'utf8')
const airesDuCss = (() => {
  const bloc = /\.plateau-scene\.avec-bande \{[\s\S]*?grid-template-areas:([\s\S]*?);/.exec(css)
  if (!bloc) throw new Error('grid-template-areas introuvable dans bande-manigances.css')
  return [...bloc[1].matchAll(/'([^']+)'/g)].map((m) => m[1].trim().split(/\s+/))
})()

describe('la disposition d origine', () => {
  it('decrit exactement la grille de bande-manigances.css (aucun changement visible)', () => {
    const genere = aireDeGrille(DISPOSITION_ORIGINE)
      .split('\n')
      .map((ligne) => ligne.replace(/'/g, '').trim().split(/\s+/))
    expect(genere).toEqual(airesDuCss)
  })

  it('place les neuf zones, main comprise, sans chevauchement', () => {
    expect(ZONES).toHaveLength(9)
    expect(ZONES).toContain('main')
    expect(Object.keys(DISPOSITION_ORIGINE.zones).sort()).toEqual([...ZONES].sort())
    expect(chevauchements(DISPOSITION_ORIGINE)).toEqual([])
    expect(estValide(DISPOSITION_ORIGINE)).toBe(true)
  })

  it('a une taille de cartes normale (1) partout', () => {
    for (const zone of ZONES) expect(DISPOSITION_ORIGINE.zones[zone].taille).toBe(1)
  })
})

describe('les garde-fous', () => {
  const copie = (): Disposition => structuredClone(DISPOSITION_ORIGINE)

  it('repere deux zones qui se chevauchent', () => {
    const d = copie()
    d.zones.main = { ...d.zones.main, ligne: 3 }
    expect(chevauchements(d)).toContainEqual(['terrain-soutien', 'main'])
    expect(estValide(d)).toBe(false)
  })

  it('refuse une zone qui sort de la grille, ou plus petite que le minimum', () => {
    const d = copie()
    d.zones.main = { ...d.zones.main, col: 3, largeur: 4 }
    expect(estValide(d)).toBe(false)
    const e = copie()
    e.zones.main = { ...e.zones.main, largeur: 0 }
    expect(estValide(e)).toBe(false)
  })

  it('refuse une taille de cartes hors bornes', () => {
    const d = copie()
    d.zones.main = { ...d.zones.main, taille: 3 }
    expect(estValide(d)).toBe(false)
  })
})

// Le texte qu'accepte le serveur (tools/test_preferences_serveur.py, meme valeur).
const TABLE = '12x8|1,1,2,2,100;3,1,2,2,100;5,1,3,2,100;8,1,5,2,100;3,3,10,2,100;' +
  '3,5,10,2,100;1,5,2,2,100;1,7,2,2,100;3,7,10,2,130'

describe('la grille aimantee de l editeur (12 x 8)', () => {
  it('part d une copie de l origine, valide et respectant les minimums', () => {
    expect(DISPOSITION_DE_DEPART.colonnes).toBe(12)
    expect(DISPOSITION_DE_DEPART.lignes).toBe(8)
    expect(estValide(DISPOSITION_DE_DEPART)).toBe(true)
  })

  it('deplace une zone sur une place libre, refuse un chevauchement ou une sortie', () => {
    const libre = deplacer(DISPOSITION_DE_DEPART, 'piles-joueur', 1, 3)
    expect(libre?.zones['piles-joueur']).toMatchObject({ col: 1, ligne: 3 })
    expect(deplacer(DISPOSITION_DE_DEPART, 'piles-joueur', 3, 3)).toBeUndefined()
    expect(deplacer(DISPOSITION_DE_DEPART, 'piles-joueur', 12, 3)).toBeUndefined()
  })

  it('redimensionne sans descendre sous le minimum de la zone', () => {
    expect(redimensionner(DISPOSITION_DE_DEPART, 'main', MINIMUMS.main.largeur - 1, 2)).toBeUndefined()
    expect(redimensionner(DISPOSITION_DE_DEPART, 'main', 6, 2)?.zones.main.largeur).toBe(6)
    // Plus grand que la place libre : chevauchement, refuse.
    expect(redimensionner(DISPOSITION_DE_DEPART, 'main', 10, 3)).toBeUndefined()
  })

  it('borne la taille des cartes', () => {
    expect(changerTaille(DISPOSITION_DE_DEPART, 'main', 9).zones.main.taille).toBe(1.6)
    expect(changerTaille(DISPOSITION_DE_DEPART, 'main', 0.1).zones.main.taille).toBe(0.6)
    expect(changerTaille(DISPOSITION_DE_DEPART, 'main', 1.234).zones.main.taille).toBe(1.25)
  })

  it('une grille 12 x 8 se dessine en colonnes egales', () => {
    expect(styleDeGrille(DISPOSITION_DE_DEPART)).toMatchObject({
      gridTemplateColumns: 'repeat(12, minmax(0, 1fr))',
      gridTemplateRows: 'repeat(8, minmax(0, 1fr))',
    })
    expect(styleDeGrille(DISPOSITION_ORIGINE).gridTemplateColumns).toBeUndefined()
  })
})

describe('le texte compact, partage avec le serveur', () => {
  it('s ecrit et se relit a l identique', () => {
    const d = lireTable(TABLE)
    expect(d?.zones.main.taille).toBe(1.3)
    expect(ecrireTable(d!)).toBe(TABLE)
  })

  it('remet en ordre ce qui ne tient pas : rien de lisible, donc l origine', () => {
    expect(lireTable(TABLE.replace('3,7,10,2,130', '3,6,10,2,130'))).toBeUndefined()
    expect(lireTable(TABLE.replace('3,7,10,2,130', '3,7,2,2,130'))).toBeUndefined()
    expect(lireTable('abime')).toBeUndefined()
    expect(lireTable(undefined)).toBeUndefined()
  })

  it('une cle par nombre de joueurs, bornee de 1 a 4', () => {
    expect([0, 1, 2, 3, 4, 7].map(cleTable)).toEqual(['table-1', 'table-1', 'table-2', 'table-3', 'table-4', 'table-4'])
  })
})
