// La marque du heros : ce que le fond du plateau devient, et ce qu'il ne
// devient jamais.
//
// ⚠ LE CAS QUI COMPTE LE PLUS est `un heros sans palette garde le fond
// commun`. La marque est un agrement : un heros que l'outil n'a pas mesure, un
// serveur sans le fichier, une reponse abimee, tout cela doit rendre un plateau
// NORMAL. Un fond casse serait pire que pas de couleur du tout.
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { bandeMechant, fondDe, identiteAffichee, identitesMechants, marqueDe, marqueMechantDe, oublierPalettes, palettes, type Couleur } from './halo-heros'

const ROUGE: Couleur = [140, 41, 31]
const BLEU: Couleur = [32, 43, 114]
const BLANC: Couleur = [219, 220, 222]
const SOMBRE = 'linear-gradient(180deg, rgba(14,18,24,0.96), rgba(6,6,8,0.98))'

describe('la bande diagonale que compose une palette', () => {
  it('sans couleur, le fond commun est rendu tel quel', () => {
    expect(fondDe(undefined, SOMBRE)).toBe(SOMBRE)
    expect(fondDe([], SOMBRE)).toBe(SOMBRE)
  })

  it('le fond sombre reste TOUJOURS en dessous', () => {
    // La bande est translucide : sans lui, le plateau serait transparent et
    // laisserait voir la page derriere.
    expect(fondDe([ROUGE], SOMBRE).endsWith(SOMBRE)).toBe(true)
  })

  it('c est UNE bande diagonale, pas une lueur d angle', () => {
    // ⚠ LE CAS QUI DIT LA FORME. Une premiere version posait trois
    // `radial-gradient` ancres dans le coin ; l'utilisateur l'a rejetee le
    // 14/09/2026 : « je voulais une marque diagonale avec un leger degrade ».
    const fond = fondDe([ROUGE, BLEU, BLANC], SOMBRE)
    expect(fond).not.toContain('radial-gradient')
    expect(fond.match(/linear-gradient/g)).toHaveLength(2) // la bande + le fond
    // 315deg progresse vers le HAUT GAUCHE : la position 0 % est le coin BAS
    // DROIT, celui que l'utilisateur a designe.
    expect(fond).toContain('linear-gradient(315deg,')
  })

  it('la premiere couleur est celle du coin, la plus dense', () => {
    const fond = fondDe([ROUGE, BLEU, BLANC], SOMBRE)
    expect(fond).toContain('rgba(140,41,31,1) 0%')
    // ⚠ ORDRE REVU (23/09/2026, demande de l'utilisateur) : primaire au
    // coin (0 %), TERTIAIRE ensuite (22 %), secondaire en dernier (38 %) --
    // pas l'ordre du fichier.
    expect(fond.indexOf('140,41,31')).toBeLessThan(fond.indexOf('219,220,222'))
    expect(fond.indexOf('219,220,222')).toBeLessThan(fond.indexOf('32,43,114'))
  })

  it('la bande s eteint avant le centre, pour ne pas teindre tout le plateau', () => {
    // Elle ne doit jamais atteindre la zone du mechant, en haut a gauche.
    expect(fondDe([ROUGE], SOMBRE)).toContain('rgba(140,41,31,0) 50%')
  })

  it('un heros a UNE seule couleur garde une bande complete', () => {
    // Onze cadres sont noirs ou gris, deux sets fan-made n'ont qu'un blanc :
    // la bande garde sa longueur et son degrade, elle porte juste une teinte.
    const fond = fondDe([BLANC], SOMBRE)
    expect(fond).toContain('rgba(219,220,222,1) 0%')
    expect(fond).toContain('rgba(219,220,222,0.75) 38%')
    expect(fond).toContain('rgba(219,220,222,0) 50%')
  })

  it('a DEUX couleurs, la seconde tient les deux derniers arrets', () => {
    const fond = fondDe([ROUGE, BLANC], SOMBRE)
    expect(fond).toContain('rgba(140,41,31,1) 0%')
    expect(fond).toContain('rgba(219,220,222,0.9) 22%')
    expect(fond).toContain('rgba(219,220,222,0.75) 38%')
  })

  it('au-dela de trois couleurs, les suivantes sont ignorees', () => {
    // ⚠ Trois arrets seulement : au-dela les teintes se melangent en boue.
    const fond = fondDe([ROUGE, BLEU, BLANC, [0, 255, 0]], SOMBRE)
    expect(fond).not.toContain('0,255,0')
  })
})

describe('le catalogue des palettes', () => {
  beforeEach(() => oublierPalettes())
  afterEach(() => {
    vi.unstubAllGlobals()
    oublierPalettes()
  })

  it('n est demande qu UNE FOIS, quel que soit le nombre d appels', () => {
    // ⚠ Le plateau se redessine plusieurs fois par seconde : une requete par
    // rendu noierait le serveur pour une reponse qui ne change jamais.
    const fetch = vi.fn().mockResolvedValue({ ok: true, json: async () => ({ palettes: {} }) })
    vi.stubGlobal('fetch', fetch)
    void palettes()
    void palettes()
    void palettes()
    expect(fetch).toHaveBeenCalledTimes(1)
  })

  it('rend les palettes servies par le moteur', async () => {
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue({
      ok: true,
      json: async () => ({ palettes: { '01001a': [ROUGE, BLEU, BLANC] } }),
    }))
    expect((await palettes())['01001a']).toEqual([ROUGE, BLEU, BLANC])
  })

  it('un serveur muet rend un catalogue vide, pas une erreur', async () => {
    vi.stubGlobal('fetch', vi.fn().mockRejectedValue(new Error('hors ligne')))
    expect(await palettes()).toEqual({})
  })

  it('une reponse qui n est pas du JSON rend un catalogue vide', async () => {
    // ⚠ Le moteur sert une IMAGE pour tout chemin inconnu : sur un serveur
    // d'avant cette route, la reponse est un JPEG en 200.
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue({
      ok: true,
      json: async () => {
        throw new SyntaxError('Unexpected token')
      },
    }))
    expect(await palettes()).toEqual({})
  })

  it('un JSON sans la cle attendue rend un catalogue vide', async () => {
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue({ ok: true, json: async () => ({}) }))
    expect(await palettes()).toEqual({})
  })
})

describe('la couleur suit le heros AFFICHE', () => {
  // Deux sieges, deux heros : Captain America et Hulk.
  const table = {
    players: [
      { area_hero: [{ card_id: '03001a' }] },
      { area_hero: [{ card_id: '10001a' }] },
    ],
  }

  it('changer de heros affiche change la carte d identite lue', () => {
    // ⚠ LE CAS QUI COMPTE : « quand on change de heros, la couleur doit
    // changer » (utilisateur, 14/09/2026). Deux sieges, deux identites.
    expect(identiteAffichee(table, 0)).toBe('03001a')
    expect(identiteAffichee(table, 1)).toBe('10001a')
  })

  it('les deux fonds obtenus sont differents', () => {
    // La preuve que l'exigence tient jusqu'au bout : ce sont bien deux fonds,
    // pas deux fois le meme.
    const cap = fondDe([[43, 62, 108], [152, 55, 46]], SOMBRE)
    const hulk = fondDe([[47, 112, 63], [220, 226, 224]], SOMBRE)
    expect(cap).not.toBe(hulk)
  })

  it('un siege vide ne rend AUCUNE identite, jamais celle du voisin', () => {
    // Un joueur elimine perd sa table : mieux vaut le fond commun qu'une
    // couleur empruntee a quelqu'un d'autre.
    expect(identiteAffichee({ players: [{ area_hero: [] }] }, 0)).toBe('')
    expect(identiteAffichee(table, 7)).toBe('')
    expect(identiteAffichee(null, 0)).toBe('')
    expect(identiteAffichee({}, 0)).toBe('')
  })
})

// L'affichage EPURE remplace la bande floue par trois bandes plates (15/10/2026).
describe('la marque aplatie de l affichage epure', () => {
  it('sans palette, aucune marque', () => {
    expect(marqueDe(undefined)).toBeUndefined()
    expect(marqueDe([])).toBeUndefined()
  })

  it('trois bandes nettes, 70 / 5 / 25 : primaire au coin, tertiaire fine au milieu, secondaire au bord', () => {
    const marque = marqueDe([ROUGE, BLEU, BLANC], 60)!
    expect(marque).toContain('315deg')
    // Deux positions par couleur : un arret net, jamais un degrade. Total 140 px.
    expect(marque).toContain('rgb(140,41,31) 0px 98px')
    expect(marque).toContain('rgb(219,220,222) 98px 105px')
    expect(marque).toContain('rgb(32,43,114) 105px 140px')
    expect(marque).toContain('transparent 140px')
    expect(marque).not.toContain('rgba')
  })

  it('un heros a deux couleurs repete la derniere', () => {
    const marque = marqueDe([ROUGE, BLEU], 40)!
    expect(marque.match(/rgb\(32,43,114\)/g)).toHaveLength(2)
  })
})

describe('le méchant au coin haut gauche (17/10/2026)', () => {
  const noir: Couleur = [10, 10, 10]
  const rouge: Couleur = [200, 30, 30]

  it('bandeMechant : principale au coin, secondaire ensuite, éteinte avant le centre', () => {
    const b = bandeMechant([noir, rouge])
    expect(b).toContain('135deg')
    expect(b.indexOf('rgba(10,10,10,1) 0%')).toBeGreaterThan(-1)
    expect(b).toContain('rgba(200,30,30,0.9) 26%')
    expect(b).toContain('rgba(200,30,30,0) 50%')
  })

  it('un méchant à une seule couleur répète cette couleur', () => {
    expect(bandeMechant([noir])).toContain('rgba(10,10,10,0.9) 26%')
  })

  it('fondDe pose la bande du méchant AVANT celle du héros, sur le fond sombre', () => {
    const fond = fondDe([rouge], 'SOMBRE', [noir, rouge])
    expect(fond.startsWith('linear-gradient(135deg')).toBe(true)
    expect(fond.indexOf('315deg')).toBeGreaterThan(fond.indexOf('135deg'))
    expect(fond.endsWith('SOMBRE')).toBe(true)
  })

  it('fondDe sans méchant reste identique à avant', () => {
    expect(fondDe([rouge], 'SOMBRE')).toBe(fondDe([rouge], 'SOMBRE', undefined))
    expect(fondDe([rouge], 'SOMBRE').startsWith('linear-gradient(315deg')).toBe(true)
  })

  it('marqueMechantDe : deux bandes nettes, 50 puis 50 %, sans dégradé', () => {
    const m = marqueMechantDe([noir, rouge], 96) ?? ''
    expect(m).toContain('135deg')
    expect(m).toContain('rgb(10,10,10) 0px 112px')
    expect(m).toContain('rgb(200,30,30) 112px 224px')
    expect(marqueMechantDe(undefined)).toBeUndefined()
  })

  it('identitesMechants : les cartes de la zone du méchant', () => {
    expect(identitesMechants({ area_villain: [{ card_id: '01094' }, { card_id: '' }, {}] })).toEqual(['01094'])
    expect(identitesMechants(null)).toEqual([])
  })
})
