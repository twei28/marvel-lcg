// Disposition de la table en ronds en « grilles par zone » (27/10/2026, maquette dispo-ronds.html). Fonction PURE :
// chaque zone range ses ronds en colonnes (remplies LIGNE par ligne dans la grille visible, puis en colonnes a droite
// pour le surplus) et expose l'etat des fleches de pagination. Remplace l'ancien modele « adaptatif » (diametre et
// nombre de colonnes calcules d'apres la largeur mesuree), abandonne au profit de ronds de taille fixe + grilles fixes.
import { describe, expect, it } from 'vitest'
import { COLONNES_PAR_DEFAUT, GRILLES, disposerZone, enColonnes } from './disposition-ronds'

/** Transforme les colonnes visibles en lignes lisibles (pour comparer au rendu attendu). */
const lignes = <T>(colonnes: T[][]): T[][] => {
  const h = Math.max(0, ...colonnes.map((c) => c.length))
  return Array.from({ length: h }, (_, r) => colonnes.map((c) => c[r]).filter((x) => x !== undefined))
}

describe('enColonnes : remplissage ligne par ligne, surplus en colonnes a droite', () => {
  it('grille 2x2 : 1 -> une colonne, 2 -> deux colonnes d\'un rond, 3 -> 2 + 1 dessous, 4 -> 2x2', () => {
    expect(enColonnes([1], 2, 2).filter((c) => c.length)).toEqual([[1]])
    expect(enColonnes([1, 2], 2, 2).filter((c) => c.length)).toEqual([[1], [2]])
    expect(enColonnes([1, 2, 3], 2, 2).filter((c) => c.length)).toEqual([[1, 3], [2]])
    expect(enColonnes([1, 2, 3, 4], 2, 2)).toEqual([[1, 3], [2, 4]])
  })

  it('grille 2x2 : le surplus (5e rond et plus) ajoute des colonnes a droite, remplies de haut en bas', () => {
    expect(enColonnes([1, 2, 3, 4, 5], 2, 2)).toEqual([[1, 3], [2, 4], [5]])
    expect(enColonnes([1, 2, 3, 4, 5, 6], 2, 2)).toEqual([[1, 3], [2, 4], [5, 6]])
    expect(enColonnes([1, 2, 3, 4, 5, 6, 7], 2, 2)).toEqual([[1, 3], [2, 4], [5, 6], [7]])
  })

  it('grille 3x2 (cartes en jeu) : premiere ligne de 3, deuxieme ligne de 3, puis colonnes a droite', () => {
    expect(lignes(enColonnes([1, 2, 3], 3, 2))).toEqual([[1, 2, 3]])
    expect(lignes(enColonnes([1, 2, 3, 4], 3, 2))).toEqual([[1, 2, 3], [4]])
    expect(enColonnes([1, 2, 3, 4, 5, 6], 3, 2)).toEqual([[1, 4], [2, 5], [3, 6]])
    expect(enColonnes([1, 2, 3, 4, 5, 6, 7], 3, 2)).toEqual([[1, 4], [2, 5], [3, 6], [7]])
  })
})

describe('GRILLES : les grilles approuvees', () => {
  it('2x2 pour le mechant, les manigances, les allies et les sbires ; 1x1 pour le heros ; 3x2 pour les cartes en jeu', () => {
    expect(GRILLES.vilain).toEqual({ cols: 2, rows: 2 })
    expect(GRILLES.manigances).toEqual({ cols: 2, rows: 2 })
    expect(GRILLES.allies).toEqual({ cols: 2, rows: 2 })
    expect(GRILLES.sbires).toEqual({ cols: 2, rows: 2 })
    expect(GRILLES.heros).toEqual({ cols: 1, rows: 1 })
    expect(GRILLES.enJeu).toEqual({ cols: 3, rows: 2 })
  })
})

describe('disposerZone : fenetre visible et fleches', () => {
  const items = (n: number) => Array.from({ length: n }, (_, i) => i)

  it('un seul rond : une colonne, pas de fleche', () => {
    const d = disposerZone('allies', items(1), 0)
    expect(d.colonnes).toEqual([[0]])
    expect(d.fleches).toBe(false)
    expect(d.total).toBe(1)
  })

  it('4 ronds en 2x2 : tout tient, pas de fleche', () => {
    const d = disposerZone('sbires', items(4), 0)
    expect(d.colonnes).toEqual([[0, 2], [1, 3]])
    expect(d.fleches).toBe(false)
  })

  it('5 ronds en 2x2 : 3 colonnes au total, la grille n\'en montre que 2 -> fleche', () => {
    const d = disposerZone('sbires', items(5), 0)
    expect(d.total).toBe(3)
    expect(d.fleches).toBe(true)
    expect(d.colonnes).toEqual([[0, 2], [1, 3]]) // les deux premieres colonnes
    expect(d.peutReculer).toBe(false)
    expect(d.peutAvancer).toBe(true)
  })

  it('surplus : la page defile d\'une colonne (chevauchement), bornee a droite', () => {
    const page1 = disposerZone('sbires', items(5), 1)
    expect(page1.colonnes).toEqual([[1, 3], [4]]) // on a avance d'une colonne : la 2e reste visible, la 3e apparait
    expect(page1.page).toBe(1)
    expect(page1.peutAvancer).toBe(false)
    expect(page1.peutReculer).toBe(true)
    // Une page hors bornes est ramenee au maximum (pas de colonne vide a droite).
    const trop = disposerZone('sbires', items(5), 9)
    expect(trop.page).toBe(1)
    expect(trop.colonnes).toEqual([[1, 3], [4]])
  })

  it('cartes en jeu (3x2) : 6 ronds tiennent, 7 font apparaitre la fleche', () => {
    expect(disposerZone('enJeu', items(6), 0).fleches).toBe(false)
    const sept = disposerZone('enJeu', items(7), 0)
    expect(sept.fleches).toBe(true)
    expect(sept.total).toBe(4)
    expect(sept.colonnes).toHaveLength(3) // la grille montre 3 colonnes
  })

  it('heros (1x1) : plusieurs faces ne se chevauchent pas — une colonne visible, fleche des le 2e', () => {
    expect(disposerZone('heros', items(1), 0).fleches).toBe(false)
    const deux = disposerZone('heros', items(2), 0)
    expect(deux.fleches).toBe(true)
    expect(deux.colonnes).toEqual([[0]])
  })

  it('zone vide : aucune colonne, aucune fleche', () => {
    const d = disposerZone('allies', items(0), 0)
    expect(d.colonnes).toEqual([])
    expect(d.total).toBe(0)
    expect(d.fleches).toBe(false)
  })
})

describe('compatibilite', () => {
  it('le defaut des colonnes (reglage de l\'appareil) reste expose', () => {
    expect(COLONNES_PAR_DEFAUT).toEqual({ manigances: 3, allies: 3, sbires: 3, enJeu: 4 })
  })
})
