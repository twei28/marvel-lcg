// « Un autre » ECHANGE la cible quand le moteur n'en veut qu'une (maquette approuvee, 26/10/2026) : toucher une autre cible legale
// retire d'abord celle qui est choisie. Pur : decide seulement QUI retirer.
import { describe, expect, it } from 'vitest'
import type { EtatInteractif } from '../interaction'
import { cibleAEchanger } from './echange-cible'

const etat = (role: EtatInteractif['role'], choisie = false): EtatInteractif => ({ role, choisie, agir: () => undefined })

describe('cibleAEchanger', () => {
  const interactifs = new Map<number, EtatInteractif>([
    [1, etat('cible', true)],
    [2, etat('indisponible')],
    [3, etat('indisponible')],
  ])

  it('une seule cible voulue, une autre deja choisie : on retire la choisie pour laisser la place', () => {
    expect(cibleAEchanger({ id: 2, maximum: 1, legales: [1, 2], interactifs })).toBe(1)
  })

  it('refuse d echanger contre une carte que le moteur n a pas proposee', () => {
    expect(cibleAEchanger({ id: 3, maximum: 1, legales: [1, 2], interactifs })).toBeUndefined()
  })

  it('plusieurs cibles voulues : pas d echange (on retire a la main la carte qu on veut changer)', () => {
    expect(cibleAEchanger({ id: 2, maximum: 2, legales: [1, 2], interactifs })).toBeUndefined()
  })

  it('rien a retirer quand aucune cible n est choisie', () => {
    const vides = new Map<number, EtatInteractif>([[2, etat('cible')]])
    expect(cibleAEchanger({ id: 2, maximum: 1, legales: [2], interactifs: vides })).toBeUndefined()
  })

  it('toucher la cible deja choisie ne l echange pas contre elle-meme', () => {
    expect(cibleAEchanger({ id: 1, maximum: 1, legales: [1, 2], interactifs })).toBeUndefined()
  })
})
