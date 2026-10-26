// Disposition ADAPTATIVE des zones de la table en ronds (26/10/2026) : combien de colonnes par zone, quelle taille de rond, quelle
// largeur pour chaque zone, d'apres la LARGEUR REELLE du conteneur et sa hauteur. Fonction pure.
//
// Geometrie du CSS (ronds.css) reprise par la fonction :
//   - une rangee a 10 px de marge de chaque cote ; entre ses deux zones : 6 + 1 + 6 px de gouttiere et de separateur (+ 2 × 2 de marge) = 17 px ;
//   - une colonne = la largeur d'un rond (`d + 6`, ou `1,22 × d + 6` pour le mechant et le heros) ; 6 px entre deux colonnes ;
//   - donc une zone de `c` colonnes de coefficient `k` occupe `c × (k × d + 6) + (c − 1) × 6 = c × k × d + 12 × c − 6`.
import { describe, expect, it } from 'vitest'
import {
  COLONNES_PAR_DEFAUT,
  D_MAX,
  D_MIN,
  calculerDisposition,
  type ColonnesZones,
  type Comptes,
} from './disposition-ronds'

const comptes = (c: Partial<Record<keyof Comptes, number>> = {}): Comptes => ({
  vilain: { n: c.vilain ?? 1, amelios: 0 },
  manigances: { n: c.manigances ?? 2, amelios: 0 },
  allies: { n: c.allies ?? 0, amelios: 0 },
  sbires: { n: c.sbires ?? 0, amelios: 0 },
  heros: { n: c.heros ?? 1, amelios: 0 },
  enJeu: { n: c.enJeu ?? 0, amelios: 0 },
})

const GRANDE = 900 // une hauteur qui ne contraint rien : seule la largeur decide

function aucunDebordement(largeur: number, d: ReturnType<typeof calculerDisposition>): void {
  for (const rangee of d.rangees) {
    expect(rangee.gauche.largeur + rangee.droite.largeur + 17).toBeLessThanOrEqual(largeur - 20 + 0.01)
  }
}

describe('colonnes effectives', () => {
  it('une colonne n\'est comptee que s\'il y a assez de ronds pour la remplir', () => {
    const d = calculerDisposition({ largeur: 412, hauteur: GRANDE, comptes: comptes({ allies: 1, sbires: 2, enJeu: 5 }), colonnes: COLONNES_PAR_DEFAUT })
    expect(d.rangees[1].gauche.colonnes).toBe(1) // 1 allie : une colonne, pas trois
    expect(d.rangees[1].droite.colonnes).toBe(2) // 2 sbires : deux colonnes
    expect(d.rangees[2].droite.colonnes).toBe(4) // 5 cartes en jeu : quatre colonnes (le choix par defaut)
    expect(d.rangees[0].droite.colonnes).toBe(2) // 2 manigances
    expect(d.rangees[0].gauche.colonnes).toBe(1) // le mechant : toujours une colonne
  })

  it('les valeurs par defaut sont Manigances 3, Allies 3, Sbires 3, Cartes en jeu 4', () => {
    expect(COLONNES_PAR_DEFAUT).toEqual({ manigances: 3, allies: 3, sbires: 3, enJeu: 4 })
  })

  it('une zone vide n\'a aucune colonne et se reduit a un bandeau', () => {
    const d = calculerDisposition({ largeur: 412, hauteur: GRANDE, comptes: comptes({ allies: 0, sbires: 3 }), colonnes: COLONNES_PAR_DEFAUT })
    expect(d.rangees[1].gauche.colonnes).toBe(0)
    expect(d.rangees[1].gauche.vide).toBe(true)
    expect(d.rangees[1].gauche.largeur).toBeLessThanOrEqual(80) // un bandeau (titre + « — »)
    expect(d.rangees[1].droite.largeur).toBeGreaterThan(d.rangees[1].gauche.largeur * 3) // la voisine prend sa place
    aucunDebordement(412, d)
  })

  it('deux zones vides se partagent la rangee', () => {
    const d = calculerDisposition({ largeur: 412, hauteur: GRANDE, comptes: comptes({ allies: 0, sbires: 0 }), colonnes: COLONNES_PAR_DEFAUT })
    expect(d.rangees[1].gauche.vide && d.rangees[1].droite.vide).toBe(true)
    aucunDebordement(412, d)
  })
})

describe('taille des ronds d\'apres la LARGEUR', () => {
  it('capture de l\'utilisateur (1 allie, 2 sbires, 5 cartes en jeu) a 412 px : la rangee heros / cartes en jeu fixe 62 px', () => {
    // Rangee heros (1 colonne, k = 1,22) + cartes en jeu (4 colonnes, k = 1) : d ≤ (412 − 20 − 17 − (6 + 42)) / (1,22 + 4) = 62,6
    const d = calculerDisposition({ largeur: 412, hauteur: GRANDE, comptes: comptes({ allies: 1, sbires: 2, enJeu: 5 }), colonnes: COLONNES_PAR_DEFAUT })
    expect(d.d).toBe(62)
    aucunDebordement(412, d)
  })

  it('le meme plateau a 360 px : 52 px, toujours aucun debordement', () => {
    const d = calculerDisposition({ largeur: 360, hauteur: GRANDE, comptes: comptes({ allies: 1, sbires: 2, enJeu: 5 }), colonnes: COLONNES_PAR_DEFAUT })
    expect(d.d).toBe(52)
    aucunDebordement(360, d)
  })

  it('3 allies, 5 sbires, 7 cartes en jeu a 412 px : les rangees a 3 + 3 colonnes fixent 52 px', () => {
    // d ≤ (412 − 20 − 17 − (2 × 30)) / 6 = 52,5
    const d = calculerDisposition({ largeur: 412, hauteur: GRANDE, comptes: comptes({ allies: 3, sbires: 5, enJeu: 7 }), colonnes: COLONNES_PAR_DEFAUT })
    expect(d.d).toBe(52)
    expect(d.rangees[1].gauche.colonnes).toBe(3)
    expect(d.rangees[1].droite.colonnes).toBe(3)
    aucunDebordement(412, d)
  })

  it('jamais plus de 76 px, meme quand il y a peu de ronds', () => {
    const d = calculerDisposition({ largeur: 412, hauteur: GRANDE, comptes: comptes({ manigances: 1 }), colonnes: COLONNES_PAR_DEFAUT })
    expect(d.d).toBe(D_MAX)
  })

  it('JAMAIS de debordement horizontal : a 320 px les colonnes sont reduites plutot que les ronds sous 44 px', () => {
    for (const largeur of [320, 340, 360, 390, 412, 430, 915]) {
      for (const nb of [
        { allies: 3, sbires: 5, enJeu: 7 },
        { allies: 8, sbires: 8, enJeu: 12 },
        { allies: 0, sbires: 1, enJeu: 2 },
        { allies: 4, sbires: 4, enJeu: 4, manigances: 6 },
      ]) {
        const d = calculerDisposition({ largeur, hauteur: GRANDE, comptes: comptes(nb), colonnes: { manigances: 4, allies: 4, sbires: 4, enJeu: 4 } })
        expect(d.d).toBeGreaterThanOrEqual(D_MIN)
        aucunDebordement(largeur, d)
      }
    }
  })
})

describe('taille des ronds d\'apres la HAUTEUR', () => {
  it('quand la hauteur manque, les ronds rapetissent jusqu\'a 44 px puis l\'ecran defile (tient = false)', () => {
    const large = calculerDisposition({ largeur: 412, hauteur: GRANDE, comptes: comptes({ allies: 3, sbires: 5, enJeu: 7 }), colonnes: COLONNES_PAR_DEFAUT })
    const serre = calculerDisposition({ largeur: 412, hauteur: 300, comptes: comptes({ allies: 3, sbires: 5, enJeu: 7 }), colonnes: COLONNES_PAR_DEFAUT })
    expect(serre.d).toBe(D_MIN)
    expect(serre.tient).toBe(false)
    expect(serre.d).toBeLessThan(large.d)
    expect(large.tient).toBe(true)
  })

  it('plus il y a de hauteur, plus les ronds sont grands (monotone), sans jamais depasser ce que la largeur permet', () => {
    let precedent = 0
    for (const hauteur of [300, 400, 500, 600, 700, 900]) {
      const d = calculerDisposition({ largeur: 412, hauteur, comptes: comptes({ allies: 1, sbires: 2, enJeu: 5 }), colonnes: COLONNES_PAR_DEFAUT })
      expect(d.d).toBeGreaterThanOrEqual(precedent)
      expect(d.d).toBeLessThanOrEqual(62)
      precedent = d.d
    }
  })

  it('8 sbires et 9 cartes en jeu : tout tient, ou bien l\'ecran defile, mais jamais sous 44 px ni hors largeur', () => {
    const d = calculerDisposition({ largeur: 412, hauteur: 560, comptes: comptes({ allies: 2, sbires: 8, enJeu: 9 }), colonnes: COLONNES_PAR_DEFAUT })
    expect(d.d).toBeGreaterThanOrEqual(D_MIN)
    aucunDebordement(412, d)
  })
})

describe('colonnes en Auto', () => {
  const auto: ColonnesZones = { manigances: 0, allies: 0, sbires: 0, enJeu: 0 }

  it('Auto : jusqu\'a 3 colonnes tant que les ronds restent a 54 px ou plus', () => {
    // 2 allies + 2 sbires : 2 + 2 colonnes => d ≤ (375 − 36) / 4 = 84 → 76 ≥ 54 : on peut meme aller a 3 colonnes si les ronds suffisent
    const peu = calculerDisposition({ largeur: 412, hauteur: GRANDE, comptes: comptes({ allies: 2, sbires: 2, enJeu: 3 }), colonnes: auto })
    expect(peu.rangees[1].gauche.colonnes).toBe(2)
    expect(peu.rangees[1].droite.colonnes).toBe(2)
    expect(peu.d).toBeGreaterThanOrEqual(54)
  })

  it('Auto : 3 allies + 5 sbires a 412 px ne tiennent a 3 + 3 colonnes qu\'a 52 px (< 54) : on retombe a 2 colonnes pour garder des ronds lisibles', () => {
    const d = calculerDisposition({ largeur: 412, hauteur: GRANDE, comptes: comptes({ allies: 3, sbires: 5, enJeu: 3 }), colonnes: auto })
    const colonnesBande = d.rangees[1].gauche.colonnes + d.rangees[1].droite.colonnes
    expect(colonnesBande).toBeLessThan(6)
    expect(d.d).toBeGreaterThanOrEqual(54)
    aucunDebordement(412, d)
  })
})

describe('largeurs des zones', () => {
  it('les deux zones d\'une rangee occupent toute la largeur : le reste est partage, rien ne depasse', () => {
    const d = calculerDisposition({ largeur: 412, hauteur: GRANDE, comptes: comptes({ allies: 1, sbires: 2, enJeu: 5 }), colonnes: COLONNES_PAR_DEFAUT })
    for (const rangee of d.rangees) {
      expect(rangee.gauche.largeur + rangee.droite.largeur + 17).toBeCloseTo(412 - 20, 0)
    }
  })

  it('les ameliorations decalees sur le cote elargissent la colonne du rond qui les porte', () => {
    const sans = calculerDisposition({ largeur: 412, hauteur: GRANDE, comptes: comptes({ allies: 2, sbires: 2 }), colonnes: COLONNES_PAR_DEFAUT })
    const c = comptes({ allies: 2, sbires: 2 })
    c.allies.amelios = 2
    const avec = calculerDisposition({ largeur: 412, hauteur: GRANDE, comptes: c, colonnes: COLONNES_PAR_DEFAUT })
    expect(avec.rangees[1].gauche.largeurColonne).toBeGreaterThan(sans.rangees[1].gauche.largeurColonne)
    expect(avec.d).toBeLessThanOrEqual(sans.d)
    aucunDebordement(412, avec)
  })
})
