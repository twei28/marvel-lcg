// Étape 8 bis de PROCESSUS-CARTE pour le pack Dazzler (backlog 12, 20/10/2026) :
// les cartes que deux cartes du pack posent SOUS elles doivent être dessinées.
//
// - Live Concert (`dz017a`, amélioration permanente posée par le Setup) range
//   chaque chanson jouée FACE VISIBLE sous elle : c'est la Setlist.
// - Lightbringr (`dz014`, soutien) glisse une chanson de la main FACE CACHÉE
//   sous lui ; son propriétaire peut la jouer « comme depuis la main ».
//
// L'état d'arrivée reprend ce que le moteur émet réellement, vérifié côté
// moteur par le cas `[dazzler] dz017a ... rendu` / `dz014 ... rendu` de
// `tools/cas/dazzler.py` (vérificateur `dz_rendu`, `ToDescriptor.Player`) :
// la carte posée suit son hôte dans la même zone, liée par `bind_object_id`.
import { describe, expect, it } from 'vitest'
import { carteSurTable, cartesDessinees, dessinee, siege, tableAvec } from './plateau-de-test'

const IDENTITE = 1
const CONCERT = 2
const CHANSON_1 = 11
const CHANSON_2 = 12
const LIGHTBRINGR = 20
const GLISSEE = 21

const monde = () =>
  tableAvec(
    siege({
      area_hero: [
        carteSurTable(IDENTITE, 'dz001a', 'Hero', 'Dazzler'),
        carteSurTable(CONCERT, 'dz017a', 'Upgrade', 'Live Concert'),
        carteSurTable(CHANSON_1, 'dz004', 'Event', '"Beautiful Dreamer"', { bind_object_id: CONCERT }),
        carteSurTable(CHANSON_2, 'dz011', 'Event', '"The Serpent is Coming"', { bind_object_id: CONCERT }),
      ],
      supports: [
        carteSurTable(LIGHTBRINGR, 'dz014', 'Support', 'Lightbringr'),
        carteSurTable(GLISSEE, 'dz007', 'Event', '"Hush Now Baby"', {
          bind_object_id: LIGHTBRINGR,
          is_face_up: false,
        }),
      ],
    })
  )

describe('Dazzler : la Setlist sous Live Concert', () => {
  it('dessine les deux chansons de la Setlist, portées par Live Concert', () => {
    expect(dessinee(monde(), CHANSON_1)).toBeDefined()
    expect(dessinee(monde(), CHANSON_2)).toBeDefined()
    expect(dessinee(monde(), CHANSON_1)?.portePar).toBe(CONCERT)
    expect(dessinee(monde(), CHANSON_2)?.portePar).toBe(CONCERT)
  })

  it('les montre face visible, juste derrière Live Concert', () => {
    const vues = cartesDessinees(monde())
    const rang = (id: number) => vues.findIndex((c) => c.id === id)
    expect(rang(CHANSON_1)).toBe(rang(CONCERT) + 1)
    expect(rang(CHANSON_2)).toBe(rang(CONCERT) + 2)
    expect(dessinee(monde(), CHANSON_1)?.facedown).toBe(false)
    expect(dessinee(monde(), CHANSON_1)?.peeking).toBe(false)
  })
})

describe('Dazzler : la chanson glissée sous Lightbringr', () => {
  it('dessine la carte glissée, portée par Lightbringr', () => {
    expect(dessinee(monde(), GLISSEE)).toBeDefined()
    expect(dessinee(monde(), GLISSEE)?.portePar).toBe(LIGHTBRINGR)
  })

  it('la marque posée face cachée, visible par son propriétaire', () => {
    const carte = dessinee(monde(), GLISSEE)
    expect(carte?.peeking).toBe(true)
    expect(carte?.facedown).toBe(false)
  })

  it('la dessine juste derrière Lightbringr', () => {
    const vues = cartesDessinees(monde())
    const rang = (id: number) => vues.findIndex((c) => c.id === id)
    expect(rang(GLISSEE)).toBe(rang(LIGHTBRINGR) + 1)
  })
})
