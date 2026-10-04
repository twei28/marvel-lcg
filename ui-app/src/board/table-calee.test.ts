// La table calee sur le recit : ce qui n'est pas raconte n'apparait pas.
import { describe, expect, it } from 'vitest'
import type { EtapeDeroule } from './deroule-phase'
import { majInstantanes, mondeDeLaTable, type Instantanes } from './table-calee'
import type { World } from './world'

const monde = (nom: string) => ({ phase: 'Villain Activation', nom }) as unknown as World
const etape = (cle: string, etat: string) => ({ cle, etat }) as unknown as EtapeDeroule
const vide: Instantanes = new Map()

describe('la table suit l etape affichee, pas le monde le plus recent', () => {
  it('le retournement du boost (trame sans changement d etape) ne bouge pas la table', () => {
    // Trame 1 : l'attaque est annoncee, le boost est face cachee.
    let inst = majInstantanes(vide, [etape('a1', 'intention')], monde('boost cache'), true)
    // Trame 2 : le boost est retourne, l'etape « attaque » n'a pas encore change.
    inst = majInstantanes(inst, [etape('a1', 'intention')], monde('boost retourne'), true)
    expect((mondeDeLaTable(inst, 'a1', false) as unknown as { nom: string }).nom).toBe('boost cache')
  })

  it('la resolution change l etape : la table montre alors son monde', () => {
    let inst = majInstantanes(vide, [etape('a1', 'intention')], monde('avant'), true)
    inst = majInstantanes(inst, [etape('a1', 'resolution')], monde('apres'), true)
    expect((mondeDeLaTable(inst, 'a1', false) as unknown as { nom: string }).nom).toBe('apres')
  })

  it('une etape deja vue garde son monde quand une suivante arrive', () => {
    let inst = majInstantanes(vide, [etape('m1', 'resolution')], monde('menace'), true)
    inst = majInstantanes(inst, [etape('m1', 'resolution'), etape('r1', 'resolution')], monde('revelation'), true)
    expect((mondeDeLaTable(inst, 'm1', false) as unknown as { nom: string }).nom).toBe('menace')
    expect((mondeDeLaTable(inst, 'r1', false) as unknown as { nom: string }).nom).toBe('revelation')
  })

  it('une question au joueur : monde reel, les clics doivent viser les vraies cartes', () => {
    const inst = majInstantanes(vide, [etape('a1', 'intention')], monde('x'), true)
    expect(mondeDeLaTable(inst, 'a1', true)).toBeUndefined()
  })

  it('etape sans instantane (le bilan) ou hors phase : monde reel', () => {
    const inst = majInstantanes(vide, [etape('a1', 'intention')], monde('x'), true)
    expect(mondeDeLaTable(inst, 'bilan', false)).toBeUndefined()
    expect(majInstantanes(inst, [], monde('y'), false).size).toBe(0)
  })
})
