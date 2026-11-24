import { describe, expect, it } from 'vitest'
import { assembleeDuMonde, avancementLongueVie, groupesEnCours, nomDuGroupe, verdictDeLAssemblee } from './assemblee-etat'
import type { AssembleeExport, World } from './world'

const base = (): AssembleeExport => ({
  code: 'KING-7F3A', table: 'p1', organisateur: 'p1', total_jetons: 5, seuil: 12, retournee: false, degats: 0, menace: 0, joueurs: 4,
  groupes: [
    { tab: 'p1', joueurs: 2, noms: 'Spider-Man, Hawkeye', etat: 0, recus: 0 },
    { tab: 'p2', joueurs: 2, noms: '', etat: 0, recus: 1 },
  ],
  terminee: false, gagnee: false,
})

describe('assemblee de Kingsfall', () => {
  it('rend undefined hors assemblee (champ vide, absent, ou sans groupe)', () => {
    expect(assembleeDuMonde(undefined)).toBeUndefined()
    expect(assembleeDuMonde({ assemblee: {} } as unknown as World)).toBeUndefined()
    expect(assembleeDuMonde({ assemblee: { code: 'KING-1', groupes: [] } } as unknown as World)).toBeUndefined()
    expect(assembleeDuMonde({ assemblee: base() } as unknown as World)?.code).toBe('KING-7F3A')
  })
  it('mesure l avancement de Longue vie vers le seuil, plein une fois retournee', () => {
    expect(avancementLongueVie(base())).toBeCloseTo(5 / 12)
    expect(avancementLongueVie({ ...base(), total_jetons: 20 })).toBe(1)
    expect(avancementLongueVie({ ...base(), retournee: true, total_jetons: 3 })).toBe(1)
    expect(avancementLongueVie({ ...base(), seuil: 0 })).toBe(0)
  })
  it('pas de verdict tant qu une table joue ; ensuite degats >= menace gagne', () => {
    expect(verdictDeLAssemblee(base())).toBe('en_attente')
    expect(verdictDeLAssemblee({ ...base(), terminee: true, gagnee: true, degats: 2, menace: 2 })).toBe('gagnee')
    expect(verdictDeLAssemblee({ ...base(), terminee: true, gagnee: false, degats: 1, menace: 2 })).toBe('perdue')
  })
  it('compte les groupes encore en jeu et nomme un groupe par ses heros, sinon sa table', () => {
    const a = base()
    expect(groupesEnCours(a)).toBe(2)
    expect(groupesEnCours({ ...a, groupes: [{ ...a.groupes[0]!, etat: 1 }, a.groupes[1]!] })).toBe(1)
    expect(nomDuGroupe(a.groupes[0]!)).toBe('Spider-Man, Hawkeye')
    expect(nomDuGroupe(a.groupes[1]!)).toBe('p2')
  })
})
