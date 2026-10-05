// La TABLE PAR BRIQUES, etape 1 (decision du 05/10/2026) : le modele pur, sans
// rien changer a l'ecran.
import { describe, expect, it } from 'vitest'
import fs from 'node:fs'
import path from 'node:path'
import {
  BRIQUES,
  DISPOSITION_DE_DEPART,
  DISPOSITION_ORIGINE,
  EPINGLEES,
  aireDeGrille,
  ancre,
  changerTaille,
  chevauchements,
  cleTable,
  deplacer,
  deposerBrique,
  ecrireTable,
  estValide,
  fusionner,
  lireTable,
  minimumDeZone,
  redimensionner,
  separer,
  styleDeGrille,
  titreDeZone,
  zoneDe,
  type Disposition,
} from './table-briques'

const css = fs.readFileSync(path.join(__dirname, 'bande-manigances.css'), 'utf8')
const airesDuCss = (() => {
  const bloc = /\.plateau-scene\.avec-bande \{[\s\S]*?grid-template-areas:([\s\S]*?);/.exec(css)
  if (!bloc) throw new Error('grid-template-areas introuvable dans bande-manigances.css')
  return [...bloc[1].matchAll(/'([^']+)'/g)].map((m) => m[1].trim().split(/\s+/))
})()

const titreDe = (d: Disposition, brique: (typeof BRIQUES)[number]) => titreDeZone(zoneDe(d, brique)!.briques)

describe('les titres automatiques', () => {
  it('l origine garde les titres d aujourd hui', () => {
    expect(titreDe(DISPOSITION_ORIGINE, 'allies')).toBe('Alliés, sbires et environnement')
    expect(titreDe(DISPOSITION_ORIGINE, 'heros')).toBe('Héros et soutiens')
    expect(titreDe(DISPOSITION_ORIGINE, 'mechant')).toBe('Méchant')
    expect(titreDe(DISPOSITION_ORIGINE, 'manigance-principale')).toBe('Manigance principale')
    expect(titreDe(DISPOSITION_ORIGINE, 'manigances-annexes')).toBe('Manigances annexes')
  })

  it('se traduit par les noms et le mot de liaison qu on lui passe', () => {
    expect(titreDeZone(['heros', 'soutiens'], (b) => (b === 'heros' ? 'Hero' : 'Allies'), 'and')).toBe('Hero and allies')
  })
})

describe('l origine et le depart', () => {
  it('l origine decrit exactement la grille de bande-manigances.css (aucun changement visible)', () => {
    const genere = aireDeGrille(DISPOSITION_ORIGINE)
      .split('\n')
      .map((ligne) => ligne.replace(/'/g, '').trim().split(/\s+/))
    expect(genere).toEqual(airesDuCss)
  })

  it('rangent chaque brique dans une zone, sans chevauchement', () => {
    for (const d of [DISPOSITION_ORIGINE, DISPOSITION_DE_DEPART]) {
      expect(estValide(d)).toBe(true)
      expect(chevauchements(d)).toEqual([])
      expect(d.zones.flatMap((z) => z.briques).sort()).toEqual([...BRIQUES].sort())
      for (const z of d.zones) expect(z.taille).toBe(1)
    }
  })

  it('ont les neuf zones d aujourd hui : les nouvelles briques restent dans leur zone', () => {
    expect(DISPOSITION_ORIGINE.zones).toHaveLength(9)
    expect(DISPOSITION_DE_DEPART.zones).toHaveLength(9)
    expect(zoneDe(DISPOSITION_DE_DEPART, 'sbires')).toBe(zoneDe(DISPOSITION_DE_DEPART, 'allies'))
    expect(zoneDe(DISPOSITION_DE_DEPART, 'soutiens')).toBe(zoneDe(DISPOSITION_DE_DEPART, 'heros'))
  })

  it('la grille d origine garde les colonnes de board.css, la personnalisee a des cases egales', () => {
    expect(styleDeGrille(DISPOSITION_ORIGINE).gridTemplateColumns).toBeUndefined()
    expect(styleDeGrille(DISPOSITION_DE_DEPART).gridTemplateColumns).toBe('repeat(12, minmax(0, 1fr))')
  })
})

describe('separer : sortir une brique de sa zone', () => {
  it('cree une zone a elle, avec son titre, et la zone d origine perd le sien', () => {
    const d = separer(DISPOSITION_DE_DEPART, 'sbires', 1, 3)!
    expect(d).toBeDefined()
    expect(titreDe(d, 'sbires')).toBe('Sbires')
    expect(titreDe(d, 'allies')).toBe('Alliés et environnement')
    expect(zoneDe(d, 'sbires')).toMatchObject({ col: 1, ligne: 3, largeur: 2, hauteur: 2 })
    expect(estValide(d)).toBe(true)
  })

  it('la brique sortie reprend la taille de cartes de sa zone', () => {
    const grande = changerTaille(DISPOSITION_DE_DEPART, 'heros', 1.3)
    expect(zoneDe(separer(grande, 'soutiens', 1, 3)!, 'soutiens')?.taille).toBe(1.3)
  })

  it('refuse une brique seule, une epinglee, ou une place prise', () => {
    expect(separer(DISPOSITION_DE_DEPART, 'mechant', 1, 3)).toBeUndefined()
    expect(separer(DISPOSITION_DE_DEPART, 'main', 1, 3)).toBeUndefined()
    expect(separer(DISPOSITION_DE_DEPART, 'sbires', 3, 5)).toBeUndefined()
    expect(separer(DISPOSITION_DE_DEPART, 'sbires', 12, 3)).toBeUndefined()
  })
})

describe('fusionner : deposer une brique sur une zone', () => {
  it('la manigance principale et les annexes donnent une zone au titre combine', () => {
    const d = fusionner(DISPOSITION_DE_DEPART, 'manigances-annexes', 'manigance-principale')!
    expect(d.zones).toHaveLength(8)
    expect(titreDe(d, 'manigance-principale')).toBe('Manigance principale et manigances annexes')
    expect(zoneDe(d, 'manigances-annexes')).toBe(zoneDe(d, 'manigance-principale'))
    expect(estValide(d)).toBe(true)
  })

  it('l ordre est celui du jeu, quel que soit le sens du geste', () => {
    const a = fusionner(DISPOSITION_DE_DEPART, 'mechant', 'allies')!
    const b = fusionner(DISPOSITION_DE_DEPART, 'mechant', 'heros')!
    expect(titreDe(a, 'mechant')).toBe('Alliés, méchant, sbires et environnement')
    expect(zoneDe(b, 'heros')?.briques).toEqual(['heros', 'soutiens', 'mechant'])
    expect(titreDe(b, 'heros')).toBe('Héros, soutiens et méchant')
  })

  it('garde la taille de cartes de la zone d accueil', () => {
    const accueil = changerTaille(DISPOSITION_DE_DEPART, 'allies', 0.8)
    expect(zoneDe(fusionner(accueil, 'mechant', 'allies')!, 'mechant')?.taille).toBe(0.8)
  })

  it('l accueil grandit jusqu au minimum d une zone fusionnee, dans la place que la source libere', () => {
    const d = fusionner(DISPOSITION_DE_DEPART, 'manigance-principale', 'mechant')!
    expect(d).toBeDefined()
    expect(zoneDe(d, 'mechant')).toMatchObject({ col: 3, largeur: 3, hauteur: 2 })
    expect(titreDe(d, 'mechant')).toBe('Méchant et manigance principale')
  })

  it('refuse les epinglees, soi-meme, et un agrandissement qui chevauche', () => {
    expect(fusionner(DISPOSITION_DE_DEPART, 'main', 'heros')).toBeUndefined()
    expect(fusionner(DISPOSITION_DE_DEPART, 'heros', 'main')).toBeUndefined()
    expect(fusionner(DISPOSITION_DE_DEPART, 'sbires', 'allies')).toBeUndefined()
    // Le mechant (3,1,2x2) devrait passer a 3 de large : il toucherait la manigance principale (5,1).
    expect(fusionner(DISPOSITION_DE_DEPART, 'sbires', 'mechant')).toBeUndefined()
  })

  it('separer puis fusionner de nouveau revient au meme ensemble de briques par zone', () => {
    const eclate = separer(DISPOSITION_DE_DEPART, 'sbires', 1, 3)!
    const retour = fusionner(eclate, 'sbires', 'allies')!
    expect(zoneDe(retour, 'allies')?.briques).toEqual(['allies', 'sbires', 'environnements'])
    expect(retour.zones).toHaveLength(9)
  })
})

describe('deplacer, redimensionner, changerTaille (par identifiant de zone)', () => {
  it('deplace une zone sur une place libre, refuse un chevauchement ou une sortie', () => {
    expect(deplacer(DISPOSITION_DE_DEPART, 'piles-joueur', 1, 3)?.zones.find((z) => ancre(z) === 'piles-joueur')).toMatchObject({ col: 1, ligne: 3 })
    expect(deplacer(DISPOSITION_DE_DEPART, 'piles-joueur', 3, 3)).toBeUndefined()
    expect(deplacer(DISPOSITION_DE_DEPART, 'piles-joueur', 12, 3)).toBeUndefined()
  })

  it('redimensionne sans descendre sous le minimum de la zone', () => {
    const min = minimumDeZone(['main'])
    expect(redimensionner(DISPOSITION_DE_DEPART, 'main', min.largeur - 1, 2)).toBeUndefined()
    expect(zoneDe(redimensionner(DISPOSITION_DE_DEPART, 'main', 6, 2)!, 'main')?.largeur).toBe(6)
    expect(redimensionner(DISPOSITION_DE_DEPART, 'main', 10, 3)).toBeUndefined()
  })

  it('borne la taille des cartes', () => {
    expect(zoneDe(changerTaille(DISPOSITION_DE_DEPART, 'main', 9), 'main')?.taille).toBe(1.6)
    expect(zoneDe(changerTaille(DISPOSITION_DE_DEPART, 'main', 0.1), 'main')?.taille).toBe(0.6)
    expect(zoneDe(changerTaille(DISPOSITION_DE_DEPART, 'main', 1.234), 'main')?.taille).toBe(1.25)
  })
})

describe('les garde-fous', () => {
  const copie = (): Disposition => structuredClone(DISPOSITION_DE_DEPART)

  it('repere une brique en double, manquante, ou une epinglee mal accompagnee', () => {
    const double = copie()
    double.zones[0].briques.push('heros')
    expect(estValide(double)).toBe(false)
    const manquante = copie()
    manquante.zones = manquante.zones.filter((z) => ancre(z) !== 'annexes')
    expect(estValide(manquante)).toBe(false)
    const melee = copie()
    zoneDe(melee, 'main')!.briques.push('sbires')
    expect(estValide(melee)).toBe(false)
  })

  it('refuse une taille de cartes hors bornes et une zone hors grille', () => {
    const d = copie()
    zoneDe(d, 'main')!.taille = 3
    expect(estValide(d)).toBe(false)
    const e = copie()
    zoneDe(e, 'main')!.largeur = 0
    expect(estValide(e)).toBe(false)
  })

  it('les epinglees sont exactement piles, deck du heros, mises de cote et main', () => {
    expect([...EPINGLEES].sort()).toEqual(['annexes', 'main', 'piles-joueur', 'piles-rencontre'])
  })
})

// L'ANCIEN texte, celui d'avant les briques (tools/test_preferences_serveur.py).
const ANCIEN = '12x8|1,1,2,2,100;3,1,2,2,100;5,1,3,2,100;8,1,5,2,100;3,3,10,2,100;' +
  '3,5,10,2,100;1,5,2,2,100;1,7,2,2,100;3,7,10,2,130'

describe('le texte compact', () => {
  it('s ecrit et se relit a l identique, pour une table eclatee comme pour le depart', () => {
    const d = fusionner(separer(DISPOSITION_DE_DEPART, 'sbires', 1, 3)!, 'manigances-annexes', 'manigance-principale')!
    expect(lireTable(ecrireTable(d))).toEqual(d)
    expect(lireTable(ecrireTable(DISPOSITION_DE_DEPART))).toEqual(DISPOSITION_DE_DEPART)
    expect(ecrireTable(DISPOSITION_DE_DEPART)).toBe(
      '12x8|pr:1,1,2,2,100;he+so:3,5,10,2,100;al+sb+en:3,3,10,2,100;me:3,1,2,2,100;' +
        'mp:5,1,3,2,100;mx:8,1,5,2,100;pj:1,5,2,2,100;an:1,7,2,2,100;ma:3,7,10,2,100'
    )
  })

  it('convertit l ancien texte : memes places, memes tailles, briques nouvelles dans leur zone', () => {
    const d = lireTable(ANCIEN)!
    expect(d).toBeDefined()
    expect(zoneDe(d, 'main')?.taille).toBe(1.3)
    expect(zoneDe(d, 'sbires')).toBe(zoneDe(d, 'allies'))
    expect(zoneDe(d, 'soutiens')).toBe(zoneDe(d, 'heros'))
    expect(zoneDe(d, 'allies')).toMatchObject({ col: 3, ligne: 3, largeur: 10, hauteur: 2 })
    expect(d.zones).toHaveLength(9)
    expect(lireTable(ecrireTable(d))).toEqual(d)
  })

  it('remet en ordre ce qui ne tient pas : rien de lisible, donc l origine', () => {
    expect(lireTable(ANCIEN.replace('3,7,10,2,130', '3,6,10,2,130'))).toBeUndefined()
    expect(lireTable(ANCIEN.replace('3,7,10,2,130', '3,7,2,2,130'))).toBeUndefined()
    expect(lireTable('abime')).toBeUndefined()
    expect(lireTable(undefined)).toBeUndefined()
    const bon = ecrireTable(DISPOSITION_DE_DEPART)
    expect(lireTable(bon.replace('me:', 'zz:'))).toBeUndefined()
    expect(lireTable(bon.replace('ma:3,7,10,2,100', 'ma+sb:3,7,10,2,100'))).toBeUndefined()
    expect(lireTable(bon.replace('an:1,7,2,2,100;', ''))).toBeUndefined()
    expect(lireTable(bon + '|autre')).toBeUndefined()
    expect(lireTable(bon.replace('12x8', '4x4'))).toBeUndefined()
  })

  it('reste sous les 400 caracteres que le serveur accepte, meme eclate a fond', () => {
    const d: Disposition = {
      colonnes: 12,
      lignes: 8,
      zones: BRIQUES.map((b) => ({ briques: [b], col: 12, ligne: 8, largeur: 12, hauteur: 8, taille: 1.6 })),
    }
    expect(ecrireTable(d).length).toBeLessThan(400)
  })
})

describe('la cle de compte', () => {
  it('une cle par nombre de joueurs, bornee de 1 a 4', () => {
    expect([0, 1, 2, 3, 4, 7].map(cleTable)).toEqual(['table-1', 'table-1', 'table-2', 'table-3', 'table-4', 'table-4'])
  })
})

describe('deposerBrique : le geste de l editeur', () => {
  it('sur une autre zone : elles fusionnent', () => {
    // La case (5, 1) est dans la manigance principale.
    const d = deposerBrique(DISPOSITION_DE_DEPART, 'mechant', 5, 1)
    expect(d && zoneDe(d, 'mechant')).toBe(d && zoneDe(d, 'manigance-principale'))
  })

  it('sur sa propre zone : rien ne change', () => {
    expect(deposerBrique(DISPOSITION_DE_DEPART, 'sbires', 4, 3)).toBe(DISPOSITION_DE_DEPART)
  })

  it('sur une case libre : la brique sort de sa zone', () => {
    const d = deposerBrique(DISPOSITION_DE_DEPART, 'sbires', 1, 3)
    expect(d && zoneDe(d, 'sbires')).toMatchObject({ briques: ['sbires'], col: 1, ligne: 3 })
  })

  it('refuse une brique seule lachee dehors, une epinglee, ou une place qui ne tient pas', () => {
    expect(deposerBrique(DISPOSITION_DE_DEPART, 'mechant', 1, 3)).toBeUndefined()
    expect(deposerBrique(DISPOSITION_DE_DEPART, 'main', 5, 1)).toBeUndefined()
    expect(deposerBrique(DISPOSITION_DE_DEPART, 'sbires', 2, 4)).toBeUndefined()
  })
})
