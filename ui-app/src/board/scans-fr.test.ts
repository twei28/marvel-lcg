// La regle est minuscule mais elle porte trois pieges :
//  - le defaut est ACTIF, donc l'absence de cle ne doit pas etre lue comme un
//    refus ;
//  - une carte absente de la liste doit sortir INCHANGEE, sans quoi le plateau
//    demande une image qui n'existe pas ;
//  - les arts alternatifs (01088_dh_drax) n'existent pas en francais, et c'est
//    l'absence de la liste qui les protege, sans regle dediee.
import { beforeEach, describe, expect, it } from 'vitest'
import { CLE_SCANS_FR, picIdFr, scansFrActifs } from './scans-fr'
import { CODES_SCAN_FR } from './scans-fr-liste'

/** La liste reelle est generee ; les tests travaillent sur un echantillon. */
const AVEC_SCAN = '01001a'

beforeEach(() => {
  window.localStorage.clear()
  ;(CODES_SCAN_FR as Set<string>).clear()
  ;(CODES_SCAN_FR as Set<string>).add(AVEC_SCAN)
})

describe('scansFrActifs', () => {
  it('vaut vrai quand la preference n a jamais ete ecrite', () => {
    expect(scansFrActifs()).toBe(true)
  })

  it('vaut faux seulement sur la valeur off', () => {
    window.localStorage.setItem(CLE_SCANS_FR, 'off')
    expect(scansFrActifs()).toBe(false)
    window.localStorage.setItem(CLE_SCANS_FR, 'on')
    expect(scansFrActifs()).toBe(true)
  })
})

describe('picIdFr', () => {
  it('prefixe une carte couverte quand l option est active', () => {
    expect(picIdFr(AVEC_SCAN)).toBe('fr_01001a')
  })

  it('laisse une carte non couverte inchangee', () => {
    expect(picIdFr('75001a')).toBe('75001a')
  })

  it('ne touche a rien quand l option est coupee', () => {
    window.localStorage.setItem(CLE_SCANS_FR, 'off')
    expect(picIdFr(AVEC_SCAN)).toBe(AVEC_SCAN)
  })

  it('laisse passer les dos generiques', () => {
    for (const dos of ['player', 'encounter', 'villain', 'no_image']) {
      expect(picIdFr(dos)).toBe(dos)
    }
  })

  it('conserve un art alternatif choisi par le joueur', () => {
    expect(picIdFr('01088_dh_drax')).toBe('01088_dh_drax')
  })
})
