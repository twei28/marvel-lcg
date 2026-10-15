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

// ⚠ ESPIONNER LE PROTOTYPE, PAS L'INSTANCE (15/10/2026). Avec le stockage de
// jsdom, `vi.spyOn(window.localStorage, 'setItem')` n'intercepte RIEN : une
// propriete posee sur l'instance devient une ENTREE stockee, la vraie methode
// reste appelee. Les deux cas ci-dessous ne simulaient donc jamais le stockage
// plein ou interdit, et echouaient (« tout » au lieu de « sans-capture » /
// « rien »). Mesure par une sonde : instance -> non intercepte, prototype
// `Storage` -> intercepte.

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
    const vrai = Storage.prototype.setItem
    const spy = vi.spyOn(Storage.prototype, 'setItem').mockImplementation(function (this: Storage, cle, valeur) {
      // Le premier essai porte la capture : on le refuse, comme le ferait un
      // stockage plein. Le second ne la porte plus et doit passer.
      if (valeur.includes('base64') && refus++ === 0) throw new Error('QuotaExceededError')
      vrai.call(this, cle, valeur)
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
    const ecrire = vi.spyOn(Storage.prototype, 'setItem').mockImplementation(() => {
      throw new Error('localStorage access denied')
    })
    const relire = vi.spyOn(Storage.prototype, 'getItem').mockImplementation(() => {
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
