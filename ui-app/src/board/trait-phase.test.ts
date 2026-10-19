// Ce que le trait dit, et par où il passe.
//
// ⚠ LE CAS QUI COMPTE LE PLUS est `chaque temps compte dans SON unité`. C'est
// la demande exacte de l'utilisateur (14/09/2026) : « si c'est les dégâts le
// nombre de dégâts, si c'est la manigance le nombre de manigances, si c'est le
// nombre de contre le nombre de contre ». Un trait qui dirait « 3 » sans unité
// laisserait croire à des dégâts sur une manigance.
import { describe, expect, it } from 'vitest'
import { alerteMenace, contenuDuTrait, deltaSurTable, deltasDesEffets, etiquetteDuTrait, traitEntre, type Boite } from './trait-phase'
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

  it('l’étiquette se pose au milieu de la COURBE (arc creusé de 20 % de la corde)', () => {
    const t = traitEntre(carte(0, 0), carte(400, 0))!
    // Corde de 300 : contrôle 60 plus haut, milieu de l'arc = moitié de ce décalage.
    expect(t.cy).toBe(10)
    expect(t.mx).toBe(250)
    expect(t.my).toBe(40)
  })

  it('l’arc se creuse toujours du même côté : en haut à l’horizontale, quel que soit le sens', () => {
    const droite = traitEntre(carte(0, 0), carte(400, 0))!
    const gauche = traitEntre(carte(400, 0), carte(0, 0))!
    expect(droite.cy).toBeLessThan(droite.y1)
    expect(gauche.cy).toBeLessThan(gauche.y1)
  })

  it('à la verticale, l’arc se creuse vers la droite, de haut en bas comme de bas en haut', () => {
    const bas = traitEntre(carte(0, 0), carte(0, 400))!
    const haut = traitEntre(carte(0, 400), carte(0, 0))!
    expect(bas.cx).toBeGreaterThan(bas.x1)
    expect(haut.cx).toBeGreaterThan(haut.x1)
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

describe('la carte touchee sur la table (v3, Q7)', () => {
  it('une attaque resolue : « −3 » et l ancien niveau des PV en fantome', () => {
    const d = deltaSurTable(etape({ titre: 'attaque', etat: 'resolu', montant: 3, restant: 5, cibleId: 1 }), 10)
    expect(d).toEqual({ texte: '−3 PV', ton: 'degats', avant: 0.8 })
  })

  it('une manigance qui atteint son seuil puis se vide : le depart vient de la menace d avant', () => {
    const d = deltaSurTable(
      etape({ titre: 'manigance', etat: 'resolu', montant: 3, restant: 0, plafond: 6, menaceAvant: 3, cibleId: 9 })
    )
    expect(d).toEqual({ texte: '+3', ton: 'menace', avant: 0.5 })
  })

  it('rien sur une annonce, sans cible, ou sans montant', () => {
    expect(deltaSurTable(etape({ titre: 'attaque', etat: 'annonce', valeurAnnoncee: 2, cibleId: 1 }))).toBeUndefined()
    expect(deltaSurTable(etape({ titre: 'attaque', etat: 'resolu', montant: 2 }))).toBeUndefined()
    expect(deltaSurTable(etape({ titre: 'manigance', etat: 'resolu', montant: 0, cibleId: 1 }))).toBeUndefined()
  })

  it('une attaque a 0 degat : « −0 PV » ; la riposte aussi', () => {
    expect(deltaSurTable(etape({ titre: 'attaque', etat: 'resolu', montant: 0, restant: 5, cibleId: 1 }))?.texte).toBe('−0 PV')
    expect(deltaSurTable(etape({ titre: 'riposte', etat: 'resolu', montant: 2, restant: 3, cibleId: 1 }))?.texte).toBe('−2 PV')
  })

  it('sans maximum de PV connu, pas de fantome invente', () => {
    expect(deltaSurTable(etape({ titre: 'attaque', etat: 'resolu', montant: 2, restant: 4, cibleId: 1 }))?.avant).toBeUndefined()
  })
})

describe('l alerte de menace (v3, Q16)', () => {
  it('a 80 % du seuil ou plus apres l etape', () => {
    expect(alerteMenace(etape({ titre: 'manigance', etat: 'resolu', restant: 8, plafond: 10 }))).toEqual({
      restant: 8,
      plafond: 10,
    })
  })

  it('pas en dessous de 80 %, ni sur une attaque, ni sans seuil', () => {
    expect(alerteMenace(etape({ titre: 'manigance', etat: 'resolu', restant: 7, plafond: 10 }))).toBeUndefined()
    expect(alerteMenace(etape({ titre: 'attaque', etat: 'resolu', restant: 9, plafond: 10 }))).toBeUndefined()
    expect(alerteMenace(etape({ titre: 'menace', restant: 9 }))).toBeUndefined()
  })
})

describe('l’étiquette posée sur le trait', () => {
  it('dit le nombre et son unité', () => {
    expect(etiquetteDuTrait({ montant: 3, unite: 'dégâts' })).toBe('3 dégâts')
  })

  it('un coup à 0 dégât ne pose AUCUNE étiquette (le bandeau et le « −0 PV » le disent)', () => {
    expect(etiquetteDuTrait({ montant: 0, unite: 'dégâts' })).toBe('')
  })

  it('rien quand le jeton ou le bandeau porte déjà le nombre', () => {
    expect(etiquetteDuTrait({ montant: 3, unite: 'dégâts' }, true)).toBe('')
  })
})

describe('« −X PV » des effets d’une carte révélée', () => {
  const effet = (cible_id: number, montant: number) => ({ genre: 'degats' as const, cible: 'C' + cible_id, cible_id, montant, restant: 3 })
  const revelation = (sur: Partial<EtapeDeroule>) => etape({ temps: 'revelation', titre: 'revelation', ...sur })

  it('une ligne par carte blessée (trois cibles à la fois)', () => {
    const d = deltasDesEffets(revelation({ effets: [effet(1, 1), effet(83, 1), effet(84, 1)] }))
    expect(d.map((x) => x.cibleId)).toEqual([1, 83, 84])
    expect(d.every((x) => x.texte === '−1 PV' && x.ton === 'degats')).toBe(true)
  })

  it('deux effets sur la même carte s’additionnent', () => {
    expect(deltasDesEffets(revelation({ effets: [effet(1, 1), effet(1, 2)] }))).toEqual([{ cibleId: 1, texte: '−3 PV', ton: 'degats' }])
  })

  it('ni menace, ni dégât à 0, ni annonce', () => {
    expect(deltasDesEffets(revelation({ effets: [{ genre: 'menace', cible: 'M', cible_id: 5, montant: 2 }, effet(1, 0)] }))).toEqual([])
    expect(deltasDesEffets(revelation({ etat: 'annonce', effets: [effet(1, 1)] }))).toEqual([])
  })

  it('pas de doublon avec l’attaque ou la riposte : leur « −X PV » est celui de deltaSurTable', () => {
    expect(deltasDesEffets(etape({ temps: 'mechant', titre: 'attaque', cibleId: 1, montant: 2, restant: 3, effets: [effet(1, 2)] }))).toEqual([])
    expect(deltasDesEffets(etape({ temps: 'revelation', titre: 'riposte', effets: [effet(1, 2)] }))).toEqual([])
  })

  it('pas hors de la révélation', () => {
    expect(deltasDesEffets(etape({ temps: 'mechant', titre: 'manigance', effets: [effet(1, 1)] }))).toEqual([])
  })
})
