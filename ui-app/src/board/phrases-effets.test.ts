// T15 : le toast dit ce qui arrive VRAIMENT. « Klaw gagne 1 menace » pour un statut Sonné
// « ne veut rien dire » (l'utilisateur, 19/10/2026).
import { describe, expect, it } from 'vitest'
import { deltasStatuts } from './effets-statuts'
import { phraseDeLEffet, phraseJeton, phraseMenace } from './phrases-effets'
import { placerToast } from './ToastEffetCarte'
import type { WorldCard } from './world'

describe('phraseDeLEffet', () => {
  it('un statut se reçoit, il ne se gagne pas et ne fait pas de menace', () => {
    expect(phraseDeLEffet('Klaw', { kind: 'status', statut: 'stunned', value: 1 })).toBe('Klaw reçoit un statut Sonné')
    expect(phraseDeLEffet('Luke Cage', { kind: 'status', statut: 'tough', value: 1 })).toBe('Luke Cage reçoit un statut Tenace')
    expect(phraseDeLEffet('Klaw', { kind: 'status', statut: 'stunned', value: 1 })).not.toMatch(/menace|gagne/)
  })

  it('tous les statuts ont leur nom français', () => {
    const noms = { stunned: 'Sonné', confused: 'Désorienté', tough: 'Tenace', exposed: 'Exposé', cloaked: 'Camouflé', dazed: 'Hébété', intensified: 'Intensifié' } as const
    for (const [statut, nom] of Object.entries(noms)) {
      expect(phraseDeLEffet('X', { kind: 'status', statut: statut as keyof typeof noms, value: 1 })).toBe(`X reçoit un statut ${nom}`)
    }
  })

  it('deux statuts d’un coup se disent ensemble', () => {
    expect(
      phraseDeLEffet('Hulk', { kind: 'status', statut: 'stunned', value: 1, aussi: [{ statut: 'confused', value: 1 }] })
    ).toBe('Hulk reçoit les statuts Sonné et Désorienté')
  })

  it('un statut retiré se perd', () => {
    expect(phraseDeLEffet('Klaw', { kind: 'status', statut: 'stunned', value: -1 })).toBe('Klaw perd le statut Sonné')
  })

  it('un jeton nommé se gagne, avec son nom', () => {
    expect(phraseDeLEffet('Spider-Man', { kind: 'token', jeton: 'rage', value: 1 })).toBe('Spider-Man gagne 1 jeton Rage')
    expect(phraseJeton('Spider-Man', 'web', 2)).toBe('Spider-Man gagne 2 jetons Toile')
    expect(phraseJeton('Spider-Man', 'rage', -1)).toBe('Spider-Man perd 1 jeton Rage')
    expect(phraseJeton('Ivan Banionis', 'acceleration', 1)).toBe('Ivan Banionis gagne 1 jeton d’accélération')
  })

  it('la menace s’accorde et ne sert qu’à une vraie menace', () => {
    expect(phraseDeLEffet('Trafic Clandestin', { kind: 'threat', value: 1 })).toBe('Trafic Clandestin gagne 1 menace')
    expect(phraseMenace('Trafic Clandestin', 3)).toBe('Trafic Clandestin gagne 3 menaces')
    expect(phraseMenace('Trafic Clandestin', -2)).toBe('Trafic Clandestin perd 2 menaces')
  })

  it('dégâts et soins gardent leurs verbes', () => {
    expect(phraseDeLEffet('Hulk', { kind: 'damage', value: -1 })).toBe('Hulk subit 1 dégât')
    expect(phraseDeLEffet('Hulk', { kind: 'damage', value: -4 })).toBe('Hulk subit 4 dégâts')
    expect(phraseDeLEffet('Hulk', { kind: 'heal', value: 2 })).toBe('Hulk récupère 2 PV')
  })
})

describe('deltasStatuts : plusieurs statuts à la fois', () => {
  const carte = (id: number, card_type: string, card_id: string, bind = 0): WorldCard =>
    ({ id, card_type, card_id, bind_object_id: bind, name: card_id, info: {} }) as unknown as WorldCard
  const monde = (...cartes: WorldCard[]) => new Map(cartes.map((c) => [c.id, c]))

  it('le badge garde le premier, `aussi` porte les autres', () => {
    const hulk = carte(5, 'Ally', '01050')
    const avant = monde(hulk)
    const apres = monde(hulk, carte(200, 'StatusCard', 'stunned', 5), carte(201, 'StatusCard', 'confused', 5))
    expect(deltasStatuts(avant, apres)).toEqual([
      [5, { kind: 'status', statut: 'stunned', value: 1, aussi: [{ statut: 'confused', value: 1 }] }],
    ])
  })
})

describe('placerToast : au-dessus de la carte, à côté si elle est tout en haut', () => {
  const ecran = { width: 1280, height: 720 }
  const taille = { width: 200, height: 30 }

  it('se pose AU-DESSUS, sans toucher le bas de la carte', () => {
    const p = placerToast({ left: 600, top: 250, width: 80, height: 115 }, taille, ecran)
    expect(p.cote).toBe('dessus')
    expect(p.top + taille.height).toBeLessThanOrEqual(250)
    expect(p.left).toBe(600 + 40 - 100)
  })

  it('une carte tout en haut reçoit le toast à gauche, sous la barre du haut', () => {
    const p = placerToast({ left: 500, top: 20, width: 80, height: 115 }, taille, ecran)
    expect(p.cote).toBe('gauche')
    expect(p.left + taille.width).toBeLessThanOrEqual(500)
    expect(p.top).toBeGreaterThanOrEqual(46)
  })

  it('une carte tout en haut près du bord gauche le reçoit à droite', () => {
    const p = placerToast({ left: 100, top: 50, width: 80, height: 115 }, taille, ecran)
    expect(p.cote).toBe('droite')
    expect(p.left).toBeGreaterThanOrEqual(100 + 80)
  })

  it('une carte juste sous la barre du haut ne reçoit pas le toast sur la barre', () => {
    const p = placerToast({ left: 214, top: 57, width: 85, height: 137 }, taille, ecran)
    expect(p.cote).toBe('gauche')
  })

  it('reste dans l’écran', () => {
    const p = placerToast({ left: 0, top: 300, width: 80, height: 115 }, taille, ecran)
    expect(p.left).toBeGreaterThanOrEqual(0)
  })
})
