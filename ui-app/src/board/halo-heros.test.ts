// Le halo du heros : ce que le fond du plateau devient, et ce qu'il ne devient
// jamais.
//
// ⚠ LE CAS QUI COMPTE LE PLUS est `un heros sans palette garde le fond
// commun`. Le halo est un agrement : un heros que l'outil n'a pas mesure, un
// serveur sans le fichier, une reponse abimee, tout cela doit rendre un plateau
// NORMAL. Un fond casse serait pire que pas de couleur du tout.
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { fondDe, identiteAffichee, oublierPalettes, palettes, type Couleur } from './halo-heros'

const ROUGE: Couleur = [140, 41, 31]
const BLEU: Couleur = [32, 43, 114]
const BLANC: Couleur = [219, 220, 222]
const SOMBRE = 'linear-gradient(180deg, rgba(14,18,24,0.96), rgba(6,6,8,0.98))'

describe('le fond que compose une palette', () => {
  it('sans couleur, le fond commun est rendu tel quel', () => {
    expect(fondDe(undefined, SOMBRE)).toBe(SOMBRE)
    expect(fondDe([], SOMBRE)).toBe(SOMBRE)
  })

  it('le fond sombre reste TOUJOURS en dessous', () => {
    // Les halos sont translucides : sans lui, le plateau serait transparent et
    // laisserait voir la page derriere.
    expect(fondDe([ROUGE], SOMBRE).endsWith(SOMBRE)).toBe(true)
  })

  it('la premiere couleur est ancree au coin BAS DROIT', () => {
    // « En diagonale, la couleur en bas a droite » (utilisateur, 14/09/2026).
    const fond = fondDe([ROUGE, BLEU, BLANC], SOMBRE)
    // Et c'est bien la PREMIERE couche, donc celle de la couleur principale :
    // dans `radial-gradient(<forme> at <ancrage>, <couleur> ...)` la couleur
    // vient APRES l'ancrage, c'est donc la meme couche.
    const premiere = fond.slice(0, fond.indexOf('), '))
    expect(premiere).toContain('at 100% 100%')
    expect(premiere).toContain('140,41,31')
  })

  it('chaque couleur donne une couche, dans l ordre recu', () => {
    const fond = fondDe([ROUGE, BLEU, BLANC], SOMBRE)
    expect(fond.match(/radial-gradient/g)).toHaveLength(3)
    expect(fond.indexOf('140,41,31')).toBeLessThan(fond.indexOf('32,43,114'))
    expect(fond.indexOf('32,43,114')).toBeLessThan(fond.indexOf('219,220,222'))
  })

  it('une seule couleur ne fait qu une couche', () => {
    // Onze heros n'ont qu'un gris ou qu'un blanc sur leur cadre : le fond doit
    // rester correct, pas seulement « pas trop moche ».
    const fond = fondDe([BLANC], SOMBRE)
    expect(fond.match(/radial-gradient/g)).toHaveLength(1)
  })

  it('au-dela de trois couleurs, les suivantes sont ignorees', () => {
    // ⚠ Empiler plus de trois teintes translucides les melange en boue. Il n'y
    // a que trois ancrages definis : une quatrieme n'aurait nulle part ou aller.
    const fond = fondDe([ROUGE, BLEU, BLANC, [0, 255, 0]], SOMBRE)
    expect(fond.match(/radial-gradient/g)).toHaveLength(3)
    expect(fond).not.toContain('0,255,0')
  })

  it('chaque couche s eteint avant le bord, pour ne pas teindre tout le plateau', () => {
    // Le halo doit rester une POINTE de couleur dans un coin : il ne doit
    // jamais atteindre la zone du mechant, en haut a gauche.
    const fond = fondDe([ROUGE], SOMBRE)
    expect(fond).toContain('rgba(140,41,31,0) 66%')
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
