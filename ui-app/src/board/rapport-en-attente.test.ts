// Un signalement qui n'est pas parti ne doit pas disparaitre avec l'onglet.
//
// ⚠ NE PAS PERDRE LA CAPTURE SANS LE DIRE. Une capture pese jusqu'a quatre
// mega-octets en base64, le stockage local en tient environ cinq : un rapport
// avec capture peut ne pas rentrer alors que le texte, lui, rentre toujours.
// On garde donc ce qu'on peut, et on dit ce qu'on a garde.
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { garder, lire, oublier } from './rapport-en-attente'

const RAPPORT = {
  nom: 'Yarro',
  description: 'la carte disparait quand je la joue',
  capture: 'data:image/png;base64,AAAA',
}

beforeEach(() => {
  window.localStorage.clear()
})

describe('un signalement mis de cote', () => {
  it('n existe pas tant que rien n a echoue', () => {
    expect(lire()).toBeUndefined()
  })

  it('se relit a l identique apres un echec', () => {
    expect(garder(RAPPORT)).toBe('tout')
    expect(lire()).toMatchObject(RAPPORT)
  })

  it('s oublie quand on l a renvoye', () => {
    garder(RAPPORT)
    oublier()
    expect(lire()).toBeUndefined()
  })

  it('garde le texte meme quand la capture ne rentre pas', () => {
    let refus = 0
    const vrai = window.localStorage.setItem.bind(window.localStorage)
    const spy = vi.spyOn(window.localStorage, 'setItem').mockImplementation((cle, valeur) => {
      // Le premier essai porte la capture : on le refuse, comme le ferait un
      // stockage plein. Le second ne la porte plus et doit passer.
      if (valeur.includes('base64') && refus++ === 0) throw new Error('QuotaExceededError')
      vrai(cle, valeur)
    })
    try {
      expect(garder(RAPPORT)).toBe('sans-capture')
      const garde = lire()
      expect(garde?.description).toBe(RAPPORT.description)
      expect(garde?.capture).toBe('')
    } finally {
      spy.mockRestore()
    }
  })

  it('ne casse rien quand le stockage est interdit', () => {
    const ecrire = vi.spyOn(window.localStorage, 'setItem').mockImplementation(() => {
      throw new Error('localStorage access denied')
    })
    const relire = vi.spyOn(window.localStorage, 'getItem').mockImplementation(() => {
      throw new Error('localStorage access denied')
    })
    try {
      expect(garder(RAPPORT)).toBe('rien')
      expect(lire()).toBeUndefined()
    } finally {
      ecrire.mockRestore()
      relire.mockRestore()
    }
  })
})
