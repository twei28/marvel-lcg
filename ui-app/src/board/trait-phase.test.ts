// Ce que le trait dit, et par où il passe.
//
// ⚠ LE CAS QUI COMPTE LE PLUS est `chaque temps compte dans SON unité`. C'est
// la demande exacte de l'utilisateur (14/09/2026) : « si c'est les dégâts le
// nombre de dégâts, si c'est la manigance le nombre de manigances, si c'est le
// nombre de contre le nombre de contre ». Un trait qui dirait « 3 » sans unité
// laisserait croire à des dégâts sur une manigance.
import { describe, expect, it } from 'vitest'
import { contenuDuTrait, traitEntre, type Boite } from './trait-phase'
import type { EtapeDeroule } from './deroule-phase'

const etape = (sur: Partial<EtapeDeroule>): EtapeDeroule =>
  ({ cle: 'x', temps: 'mechant', titre: '', regle: '', boosts: [], ...sur }) as EtapeDeroule

describe('ce que le trait dit', () => {
  it('une attaque compte en dégâts', () => {
    expect(contenuDuTrait(etape({ titre: 'attaque', montant: 3 }))).toEqual({
      montant: 3,
      unite: 'dégâts',
      ton: 'degats',
    })
  })

  it('une manigance compte en menaces', () => {
    const c = contenuDuTrait(etape({ titre: 'manigance', montant: 2 }))
    expect(c.unite).toBe('menaces')
    expect(c.ton).toBe('menaces')
  })

  it('la menace du point 1 compte en menaces aussi', () => {
    expect(contenuDuTrait(etape({ titre: 'menace', montant: 1 })).unite).toBe('menace')
  })

  it('une distribution compte en cartes, pas en dégâts', () => {
    // « Colossus reçoit 2 cartes rencontre » en Héroïque : des cartes reçues ne
    // sont pas des dégâts, et le bilan lui-même ne les compte pas comme tels.
    const c = contenuDuTrait(etape({ titre: 'distribution', montant: 2 }))
    expect(c.unite).toBe('cartes')
    expect(c.ton).toBe('neutre')
  })

  it('le singulier s’accorde : 1 dégât, 2 dégâts', () => {
    expect(contenuDuTrait(etape({ titre: 'attaque', montant: 1 })).unite).toBe('dégât')
    expect(contenuDuTrait(etape({ titre: 'attaque', montant: 2 })).unite).toBe('dégâts')
  })

  it('un retrait de menace s’accorde sur la QUANTITÉ, pas sur le signe', () => {
    // Un nombre négatif reste « 1 contre », jamais « -1 contres ».
    expect(contenuDuTrait(etape({ titre: 'contre', montant: -1 })).unite).toBe('contre')
    expect(contenuDuTrait(etape({ titre: 'contre', montant: -3 })).unite).toBe('contres')
  })

  it('un statut porte son NOM, pas un nombre', () => {
    // « Étourdi » dit tout ; « 1 » ne dirait rien.
    const c = contenuDuTrait(etape({ titre: 'statut', statut: 'Étourdi' }))
    expect(c.unite).toBe('Étourdi')
    expect(c.ton).toBe('statut')
    expect(c.montant).toBeUndefined()
  })

  it('un titre inconnu ne ment pas sur l’unité', () => {
    // Mieux vaut un trait qui montre seulement la direction qu'un trait qui
    // annonce des dégâts là où il n'y en a pas.
    const c = contenuDuTrait(etape({ titre: 'revelation', montant: 4 }))
    expect(c.unite).toBe('')
    expect(c.ton).toBe('neutre')
    expect(c.montant).toBe(4)
  })
})

const carte = (x: number, y: number): Boite => ({ x, y, w: 100, h: 140 })

describe('par où le trait passe', () => {
  it('il part du BORD de la carte, jamais de son centre', () => {
    // Un trait tiré de centre à centre passe sous les deux cartes : on n'en
    // voit que le milieu, et il a l'air de sortir de nulle part.
    const t = traitEntre(carte(0, 0), carte(400, 0))!
    expect(t.x1).toBe(100) // bord droit de la carte de départ
    expect(t.x2).toBe(400) // bord gauche de la carte d'arrivée
    expect(t.y1).toBe(70)
  })

  it('il marche dans l’autre sens', () => {
    const t = traitEntre(carte(400, 0), carte(0, 0))!
    expect(t.x1).toBe(400)
    expect(t.x2).toBe(100)
  })

  it('à la verticale, il sort par le haut et le bas', () => {
    const t = traitEntre(carte(0, 0), carte(0, 400))!
    expect(t.x1).toBe(50)
    expect(t.y1).toBe(140)
    expect(t.y2).toBe(400)
  })

  it('l’étiquette se pose au milieu du segment', () => {
    const t = traitEntre(carte(0, 0), carte(400, 0))!
    expect(t.mx).toBe(250)
    expect(t.my).toBe(70)
  })

  it('deux cartes confondues ne donnent AUCUN trait', () => {
    // Il n'y a alors pas de direction à montrer, et une étiquette se poserait
    // sur un segment de longueur nulle.
    expect(traitEntre(carte(10, 10), carte(10, 10))).toBeUndefined()
  })

  it('en diagonale, les deux extrémités restent sur les bords', () => {
    const a = carte(0, 0)
    const b = carte(300, 300)
    const t = traitEntre(a, b)!
    const dansLaBoite = (x: number, y: number, c: Boite) =>
      x > c.x && x < c.x + c.w && y > c.y && y < c.y + c.h
    expect(dansLaBoite(t.x1, t.y1, a)).toBe(false)
    expect(dansLaBoite(t.x2, t.y2, b)).toBe(false)
  })
})

describe('le trait sur une ANNONCE', () => {
  // ⚠ Le coup n'a pas eu lieu : l'étape ne porte aucun `montant`, seulement
  // `valeurAnnoncee`. Choix de l'utilisateur parmi trois (14/09/2026) : « dès
  // l'annonce, avec le montant prévu », en sachant que ce nombre changera après
  // les boosts et la défense. C'est le prix à payer pour décider si l'on défend.
  it('porte le montant PRÉVU tant que le coup n’a pas eu lieu', () => {
    const c = contenuDuTrait(
      etape({ titre: 'attaque', etat: 'annonce', valeurAnnoncee: 3 })
    )
    expect(c.montant).toBe(3)
    expect(c.unite).toBe('dégâts')
  })

  it('le montant RÉEL l’emporte dès que le coup est résolu', () => {
    // Sur le pas suivant, `montant` existe : c'est lui qui compte, et il peut
    // être bien plus petit (défense) ou plus grand (boosts).
    const c = contenuDuTrait(
      etape({ titre: 'attaque', etat: 'resolu', valeurAnnoncee: 3, montant: 1 })
    )
    expect(c.montant).toBe(1)
    expect(c.unite).toBe('dégât')
  })

  it('une annonce sans valeur connue ne montre aucun nombre', () => {
    const c = contenuDuTrait(etape({ titre: 'attaque', etat: 'annonce' }))
    expect(c.montant).toBeUndefined()
  })
})
