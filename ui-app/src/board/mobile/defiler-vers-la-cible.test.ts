import { describe, expect, it } from 'vitest'
import { cleDesCibles } from './defiler-vers-la-cible'
import type { EtatInteractif } from '../interaction'

const etat = (role: EtatInteractif['role']): EtatInteractif => ({ role, choisie: false }) as EtatInteractif

describe('cleDesCibles', () => {
  it('ne retient que les cibles, triees : la meme question donne la meme cle', () => {
    expect(cleDesCibles(undefined)).toBe('')
    expect(cleDesCibles(new Map([[9, etat('cible')], [3, etat('cible')], [5, etat('porteur')]]))).toBe('3,9')
    expect(cleDesCibles(new Map([[3, etat('cible')], [9, etat('cible')]]))).toBe('3,9')
    expect(cleDesCibles(new Map([[5, etat('ressource')]]))).toBe('')
  })
})
