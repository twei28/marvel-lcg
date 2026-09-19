// L'orientation des AUTRES faces d'une carte recto-verso.
//
// « Find the Senator » (32065a, SideScheme, paysage) a pour verso « Protect the
// Senator » (32065b, Environment, portrait). L'apercu recopiait l'orientation
// de la face visible sur le verso, qui se lisait couche. Signale en jeu le
// 09/09/2026.
import { describe, expect, it } from 'vitest'
import { autresFacesDe, paysageSelonTypePapier } from './card-model'
import { catalogueVide, type Catalogue } from './catalogue'
import type { WorldCard } from './world'

const carte = (card_id: string, dos: string[]): WorldCard =>
  ({ id: 1, card_type: 'EncounterSideScheme', card_id, pic_id: card_id, is_face_up: true, down_card_ids: dos, info: {} }) as unknown as WorldCard

const catalogue = (types: Record<string, string>): Catalogue => ({ ...catalogueVide, type: (id) => types[id] })

describe('paysage selon le type imprime', () => {
  it('complots et statuts en paysage, le reste en portrait, l inconnu indecis', () => {
    expect(paysageSelonTypePapier('SideScheme')).toBe(true)
    expect(paysageSelonTypePapier('MainScheme')).toBe(true)
    expect(paysageSelonTypePapier('Status')).toBe(true)
    expect(paysageSelonTypePapier('Environment')).toBe(false)
    expect(paysageSelonTypePapier('Ally')).toBe(false)
    expect(paysageSelonTypePapier(undefined)).toBeUndefined()
  })
})

describe('les autres faces', () => {
  it('le verso portrait d un complot paysage est marque portrait', () => {
    const faces = autresFacesDe(carte('32065a', ['32065b']), catalogue({ '32065b': 'Environment' }))
    expect(faces).toHaveLength(1)
    expect(faces[0]?.isLandscape).toBe(false)
    expect(faces[0]?.url).toContain('32065b')
  })

  it('le verso complot d une carte portrait est marque paysage', () => {
    const faces = autresFacesDe(carte('32065b', ['32065a']), catalogue({ '32065a': 'SideScheme' }))
    expect(faces[0]?.isLandscape).toBe(true)
  })

  it('un heros custom (identifiant lettre) a bien son alter ego en autre face', () => {
    // Blink bk001a / bk001b : le motif purement numerique les ignorait (18/09/2026).
    const faces = autresFacesDe(carte('bk001a', ['bk001b']), catalogue({ bk001b: 'AlterEgo' }))
    expect(faces).toHaveLength(1)
    expect(faces[0]?.url).toContain('bk001b')
    expect(faces[0]?.isLandscape).toBe(false)
  })

  it('un dos generique n est pas une autre face, meme pour un heros custom', () => {
    expect(autresFacesDe(carte('bk001a', ['player']), catalogueVide)).toHaveLength(0)
    expect(autresFacesDe(carte('12001a', ['encounter']), catalogueVide)).toHaveLength(0)
  })

  it('sans type connu, l orientation reste indecise : l apercu garde celle de la face visible', () => {
    const faces = autresFacesDe(carte('32065a', ['32065b']), catalogueVide)
    expect(faces[0]?.isLandscape).toBeUndefined()
  })

  it('un dos generique n est pas une autre face', () => {
    expect(autresFacesDe(carte('32065a', ['encounter']), catalogueVide)).toEqual([])
  })
})
