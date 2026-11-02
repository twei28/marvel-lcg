// La regle est minuscule mais elle porte trois pieges :
//  - le defaut est ACTIF, donc l'absence de cle ne doit pas etre lue comme un
//    refus ;
//  - une carte absente de la liste doit sortir INCHANGEE, sans quoi le plateau
//    demande une image qui n'existe pas ;
//  - les arts alternatifs (01088_dh_drax) n'existent pas en francais, et c'est
//    l'absence de la liste qui les protege, sans regle dediee.
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { CLE_SCANS_FR, picIdFr, scanDejaFrancais, scansFrActifs } from './scans-fr'
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

  it('vaut vrai quand localStorage leve une exception (mode prive, iframe sandbox)', () => {
    const spy = vi.spyOn(window.localStorage, 'getItem').mockImplementation(() => {
      throw new Error('localStorage access denied')
    })
    try {
      expect(scansFrActifs()).toBe(true)
    } finally {
      spy.mockRestore()
    }
  })
})

describe('picIdFr', () => {
  it('prefixe une carte couverte quand l option est active', () => {
    expect(picIdFr(AVEC_SCAN)).toBe('fr_01001a')
  })

  it('laisse une carte non couverte inchangee', () => {
    expect(picIdFr('sg001a')).toBe('sg001a')
  })

  it('ne touche a rien quand l option est coupee', () => {
    window.localStorage.setItem(CLE_SCANS_FR, 'off')
    expect(picIdFr(AVEC_SCAN)).toBe(AVEC_SCAN)
  })

  it('prefixe les trois cartes d etat, deposees a la main hors archive OCTGN', () => {
    window.localStorage.setItem(CLE_SCANS_FR, 'on')
    expect(picIdFr('tough')).toBe('fr_tough')
    expect(picIdFr('stunned')).toBe('fr_stunned')
    expect(picIdFr('confused')).toBe('fr_confused')
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

describe('scanUrl', () => {
  it('demande le fichier francais pour une carte couverte', async () => {
    const { scanUrl } = await import('./card-model')
    expect(scanUrl(AVEC_SCAN)).toBe('/scan/fr_01001a')
  })

  it('demande le fichier anglais pour une carte non couverte', async () => {
    const { scanUrl } = await import('./card-model')
    expect(scanUrl('sg001a')).toBe('/scan/sg001a')
  })
})

describe('alignerScansSurLangue', () => {
  it('coupe les scans francais quand l interface passe en anglais', async () => {
    const { alignerScansSurLangue } = await import('./scans-fr')
    alignerScansSurLangue('en')
    expect(window.localStorage.getItem(CLE_SCANS_FR)).toBe('off')
    expect(scansFrActifs()).toBe(false)
    expect(picIdFr(AVEC_SCAN)).toBe(AVEC_SCAN)
  })

  it('rallume les scans francais quand l interface repasse en francais', async () => {
    const { alignerScansSurLangue } = await import('./scans-fr')
    window.localStorage.setItem(CLE_SCANS_FR, 'off')
    alignerScansSurLangue('fr')
    expect(window.localStorage.getItem(CLE_SCANS_FR)).toBe('on')
    expect(picIdFr(AVEC_SCAN)).toBe('fr_01001a')
  })

  it('ne casse pas la bascule quand localStorage leve une exception', async () => {
    const { alignerScansSurLangue } = await import('./scans-fr')
    const spy = vi.spyOn(window.localStorage, 'setItem').mockImplementation(() => {
      throw new Error('localStorage access denied')
    })
    try {
      expect(() => alignerScansSurLangue('en')).not.toThrow()
    } finally {
      spy.mockRestore()
    }
  })
})

describe('scanDejaFrancais', () => {
  it('le pack Superior Iron Man (scans imprimés en francais) n\'a pas besoin de voile, les autres oui', () => {
    expect(scanDejaFrancais('si005')).toBe(true)
    expect(scanDejaFrancais('si001a')).toBe(true)
    expect(scanDejaFrancais('sk170b')).toBe(false)
    expect(scanDejaFrancais('si005_cb')).toBe(false)
  })
})

describe('SCANS_FR_FANMADE', () => {
  it('les 17 cartes de Destiny (35 avec les 18 de Beast) ont un scan francais, donc pas de voile', async () => {
    const { aScanFr, picIdFr, SCANS_FR_FANMADE } = await import('./scans-fr')
    expect(SCANS_FR_FANMADE.size).toBe(35)
    expect(aScanFr('dy001a')).toBe(true)
    expect(aScanFr('dy016')).toBe(true)
    expect(aScanFr('dy017')).toBe(false)
    window.localStorage.setItem('marvel-board-scans-fr', 'on')
    expect(picIdFr('dy015')).toBe('fr_dy015')
  })
})

describe('SCANS_FR_FANMADE (Beast de Proust)', () => {
  it('les 18 cartes de Beast (Proust) ont un scan francais, donc pas de voile', async () => {
    const { aScanFr, picIdFr } = await import('./scans-fr')
    for (const id of ['bs001a', 'bs001b', 'bs002', 'bs009', 'bs015', 'bs017']) expect(aScanFr(id)).toBe(true)
    expect(aScanFr('bs018')).toBe(false)
    window.localStorage.setItem('marvel-board-scans-fr', 'on')
    expect(picIdFr('bs013')).toBe('fr_bs013')
  })
})

describe('Beast (Proust) : scan français seul, texte anglais posé dessus', () => {
  it('chaque carte à scan français seul a son texte anglais', async () => {
    const { SCANS_FR_SEULS } = await import('./scans-fr')
    const { TEXTES_EN_SCAN_FR, CODES_SANS_TEXTE_EN } = await import('./textes-en-scan-fr')
    expect(SCANS_FR_SEULS.size).toBe(18)
    expect(CODES_SANS_TEXTE_EN).toEqual([])
    expect(TEXTES_EN_SCAN_FR['bs002']).toMatch(/tucked under this card/)
  })
  it("les traits du texte posé restent anglais quand on passe une table vide", async () => {
    const { texteEnParagraphes } = await import('./traduction-posee')
    expect(texteEnParagraphes('Search for a [[TECH]] upgrade, a [[ELITE]] one.', {})).toContain('>ELITE<')
    expect(texteEnParagraphes('un [[ELITE]]')).toContain('>ÉLITE<')
  })
})
