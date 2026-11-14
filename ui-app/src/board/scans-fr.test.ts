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

describe('traducteurDuScanFr', () => {
  it('crédite Nicodede62 sous le scan français de Blade, Dazzler et Moon Knight, et rien ailleurs', async () => {
    const { traducteurDuScanFr } = await import('./scans-fr')
    expect(traducteurDuScanFr('/scan/fr_bl005')).toBe('Nicodede62')
    expect(traducteurDuScanFr('/scan/fr_dz017a')).toBe('Nicodede62')
    expect(traducteurDuScanFr('/vignette/fr_mk001e')).toBe('Nicodede62')
    // En anglais (scan sans prefixe), carte bonus sans scan FR, autre pack fan-made, carte officielle : rien.
    expect(traducteurDuScanFr('/scan/bl005')).toBeUndefined()
    expect(traducteurDuScanFr('/scan/fr_dz018')).toBeUndefined()
    expect(traducteurDuScanFr('/scan/fr_dy001a')).toBeUndefined()
    expect(traducteurDuScanFr('/scan/fr_01001a')).toBeUndefined()
    expect(traducteurDuScanFr(undefined)).toBeUndefined()
  })
})

describe('SCANS_FR_FANMADE', () => {
  it('les 17 cartes de Destiny (275 avec les 18 de Beast, les 23 de Mystique, les 17 de Blade, les 24 de Dazzler les 20 de Moon Knight et les 155 de La ville ne dort jamais) ont un scan francais, donc pas de voile', async () => {
    const { aScanFr, picIdFr, SCANS_FR_FANMADE } = await import('./scans-fr')
    expect(SCANS_FR_FANMADE.size).toBe(275)
    expect(aScanFr('dy001a')).toBe(true)
    expect(aScanFr('dy016')).toBe(true)
    expect(aScanFr('dy017')).toBe(false)
    window.localStorage.setItem('marvel-board-scans-fr', 'on')
    expect(picIdFr('dy015')).toBe('fr_dy015')
  })
})

describe('SCANS_FR_FANMADE (Blade de Rainy)', () => {
  it('les 17 cartes Blade ont toutes un scan francais, donc pas de voile', async () => {
    const { aScanFr, picIdFr } = await import('./scans-fr')
    for (const id of [
      'bl001a', 'bl001b', 'bl002', 'bl003', 'bl004', 'bl005', 'bl006', 'bl007', 'bl008', 'bl009', 'bl010', 'bl011',
      'bl012', 'bl013', 'bl014', 'bl015', 'bl016', 'bl017',
    ])
      expect(aScanFr(id)).toBe(true)
    window.localStorage.setItem('marvel-board-scans-fr', 'on')
    expect(picIdFr('bl009')).toBe('fr_bl009')
  })
})

describe('SCANS_FR_FANMADE (Dazzler de Lord Havok)', () => {
  it('les 24 cartes couvertes par le depot de l\'auteur ont un scan francais ; les cartes bonus sans scan gardent le voile', async () => {
    const { aScanFr, picIdFr } = await import('./scans-fr')
    for (const id of [
      'dz001a', 'dz001b', 'dz002', 'dz003', 'dz004', 'dz005', 'dz006', 'dz007', 'dz008', 'dz009', 'dz010',
      'dz011', 'dz012', 'dz013', 'dz014', 'dz015', 'dz016', 'dz017a', 'dz017b', 'dz019', 'dz020', 'dz021',
      'dz022', 'dz023',
    ])
      expect(aScanFr(id)).toBe(true)
    // dz018 (Sound Absorption) et dz024-dz038 (cartes bonus) : aucun scan FR dans le depot, le voile reste.
    expect(aScanFr('dz018')).toBe(false)
    expect(aScanFr('dz024')).toBe(false)
    expect(aScanFr('dz038')).toBe(false)
    window.localStorage.setItem('marvel-board-scans-fr', 'on')
    expect(picIdFr('dz009')).toBe('fr_dz009')
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
    expect(SCANS_FR_SEULS.size).toBe(25)
    expect(CODES_SANS_TEXTE_EN).toEqual([])
    expect(TEXTES_EN_SCAN_FR['bs002']).toMatch(/tucked under this card/)
  })
  it("les traits du texte posé restent anglais quand on passe une table vide", async () => {
    const { texteEnParagraphes } = await import('./traduction-posee')
    expect(texteEnParagraphes('Search for a [[TECH]] upgrade, a [[ELITE]] one.', {})).toContain('>ELITE<')
    expect(texteEnParagraphes('un [[ELITE]]')).toContain('>ÉLITE<')
  })
})

describe('SCANS_FR_FANMADE (Mystique de Merlin)', () => {
  it('les 23 faces de Mystique ont un scan francais, donc pas de voile FR', async () => {
    const { aScanFr, picIdFr, SCANS_FR_FANMADE } = await import('./scans-fr')
    for (const id of ['my001a', 'my001b', 'my002', 'my003a', 'my003b', 'my005b', 'my007', 'my015', 'my018', 'my019']) expect(aScanFr(id)).toBe(true)
    expect([...SCANS_FR_FANMADE].filter((c) => c.startsWith('my'))).toHaveLength(23)
    expect(aScanFr('my020')).toBe(false)
    window.localStorage.setItem('marvel-board-scans-fr', 'on')
    expect(picIdFr('my003b')).toBe('fr_my003b')
  })
  it("sept cartes ont un scan FR seul (texte du scan EN périmé par la Release FR) avec leur texte anglais ; les autres gardent le scan EN", async () => {
    const { SCANS_FR_SEULS } = await import('./scans-fr')
    const { TEXTES_EN_SCAN_FR, CODES_SANS_TEXTE_EN } = await import('./textes-en-scan-fr')
    const mystique = [...SCANS_FR_SEULS].filter((c) => c.startsWith('my')).sort()
    expect(mystique).toEqual(['my005a', 'my005b', 'my007', 'my012', 'my013', 'my018', 'my019'])
    expect(CODES_SANS_TEXTE_EN).toEqual([])
    expect(TEXTES_EN_SCAN_FR['my012']).toMatch(/ready Mystique/)
    expect(SCANS_FR_SEULS.has('my010')).toBe(false)
  })
})

describe('SCANS_FR_FANMADE (Moon Knight de DesignHacker)', () => {
  it('les 20 cartes du depot de l\'auteur ont un scan francais ; les cartes bonus sans scan gardent le voile', async () => {
    const { aScanFr, picIdFr } = await import('./scans-fr')
    for (const id of [
      'mk001a', 'mk001b', 'mk001c', 'mk001d', 'mk001e', 'mk002', 'mk003', 'mk004', 'mk005', 'mk006', 'mk007', 'mk008',
      'mk009', 'mk010', 'mk011', 'mk012', 'mk013', 'mk014', 'mk015', 'mk016',
    ])
      expect(aScanFr(id)).toBe(true)
    expect(aScanFr('mk017')).toBe(false)
    expect(aScanFr('mk024')).toBe(false)
    window.localStorage.setItem('marvel-board-scans-fr', 'on')
    expect(picIdFr('mk005')).toBe('fr_mk005')
  })
})

describe('SCANS_FR_FANMADE (La ville ne dort jamais, MC×DC 2026)', () => {
  it('les 155 cartes du zip ont un scan francais ; les cartes d\'autres packs et l\'allie Punisher gardent le voile', async () => {
    const { aScanFr, picIdFr } = await import('./scans-fr')
    for (const id of [
      'pu001a', 'pu001b', 'pu002a', 'pu002b', 'pu003a', 'pu003b', 'pu004', 'pu005', 'pu006', 'pu007', 'pu008', 'pu009',
      'pu010', 'pu011', 'pu012', 'pu013', 'pu014', 'pu015', 'pu016', 'pu017', 'pu018', 'pu020', 'pu021', 'pu022',
      'pu023', 'pu024', 'pu025', 'pu026', 'pu027', 'pu028', 'pu030', 'pu031', 'pu032', 'pu033', 'pu034', 'pu035',
      'pu036', 'pu037', 'pu038', 'pu039', 'pu040', 'pu041', 'pu042', 'pu043', 'pu044', 'pu045', 'pu046', 'pu047',
      'pu048a', 'pu048b', 'pu049a', 'pu049b', 'pu050a', 'pu050b', 'pu051a', 'pu051b', 'pu052a', 'pu052b', 'pu053a', 'pu053b',
      'pu054a', 'pu054b', 'pu055a', 'pu055b', 'pu056a', 'pu056b', 'pu057a', 'pu057b', 'pu058', 'pu059', 'pu060', 'pu063',
      'pu064', 'pu065', 'pu066', 'pu068', 'pu070', 'pu071a', 'pu071b', 'pu072a', 'pu072b', 'pu073', 'pu074', 'pu075',
      'pu076', 'pu077', 'pu078', 'pu079', 'pu080', 'pu082', 'pu084', 'pu086a', 'pu086b', 'pu087a', 'pu087b', 'pu088a',
      'pu088b', 'pu089a', 'pu089b', 'pu090a', 'pu090b', 'pu091a', 'pu091b', 'pu092', 'pu093', 'pu094', 'pu095', 'pu096',
      'pu097', 'pu098', 'pu099', 'pu100', 'pu102', 'pu104', 'pu105', 'pu106a', 'pu106b', 'pu107', 'pu108', 'pu109',
      'pu110', 'pu111', 'pu113', 'pu114', 'pu115', 'pu116', 'pu117', 'pu118', 'pu119', 'pu120', 'pu121', 'pu123',
      'pu125', 'pu126', 'pu127', 'pu128', 'pu129', 'pu130', 'pu131', 'pu139', 'pu140', 'pu141', 'pu142', 'pu143',
      'pu144', 'pu145', 'pu147', 'pu148', 'pu149a', 'pu149b', 'pu151', 'pu279', 'pu280', 'pu281', 'pu282',
    ])
      expect(aScanFr(id)).toBe(true)
    // un second exemplaire (6019) n'a pas de fiche : il partage pu018 ; 6138 (pu146 ?) n'est pas associee ; Hawkeye et Resistance sont d'autres packs
    for (const id of ['pu019', 'pu146', 'pu283a', 'pu283b', 'pu284b', 'pu285b']) expect(aScanFr(id)).toBe(false)
    window.localStorage.setItem('marvel-board-scans-fr', 'on')
    expect(picIdFr('pu005')).toBe('fr_pu005')
    expect(picIdFr('pu006')).toBe('fr_pu006')
    expect(picIdFr('pu140')).toBe('fr_pu140')
    expect(picIdFr('pu146')).toBe('pu146')
  })
})
