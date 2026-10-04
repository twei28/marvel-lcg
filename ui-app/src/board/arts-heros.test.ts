// Arts alternatifs des cartes de héros (02/10/2026) : le choix fait dans le
// wizard est rangé sous la clé du héros (« 38001 » pour Rogue). Il doit
// s'appliquer à toutes les faces qui ont cet art, y compris les cartes qui
// ne portent pas le numéro du héros (Touched, SP//dr, Ironheart 2 et 3).
import { beforeEach, describe, expect, it, vi } from 'vitest'

async function charger(choix: Record<string, string>) {
  window.localStorage.setItem('mc_hero_art_v1', JSON.stringify(choix))
  vi.resetModules()
  return import('./variantes')
}

describe('arts alternatifs des héros', () => {
  beforeEach(() => window.localStorage.clear())

  it('applique le choix à la face héros et à l\'alter ego', async () => {
    const { picIdAffiche } = await charger({ '15001': 'rog2' })
    expect(picIdAffiche('15001a', undefined)).toBe('15001a_rog2')
    expect(picIdAffiche('15001b', undefined)).toBe('15001b_rog2')
  })

  it('suit le choix de Rogue jusqu\'à Touched, qui porte un autre numéro', async () => {
    const { picIdAffiche } = await charger({ '38001': 'rog' })
    expect(picIdAffiche('38002', undefined)).toBe('38002_rog')
  })

  it('suit le choix d\'Ironheart sur ses formes 2 et 3', async () => {
    const { picIdAffiche } = await charger({ '29001': 'cb' })
    expect(picIdAffiche('29003a', undefined)).toBe('29003a_cb')
  })

  it('garde le scan quand la face n\'a pas cet art', async () => {
    // War Machine alter ego « cb » est écarté (texte différent de notre carte).
    const { picIdAffiche } = await charger({ '23001': 'cb' })
    expect(picIdAffiche('23001a', undefined)).toBe('23001a_cb')
    expect(picIdAffiche('23001b', undefined)).toBe('23001b')
  })

  it('donne à l\'alter ego son propre choix, qui l\'emporte sur celui du héros', async () => {
    const { picIdAffiche } = await charger({ '15001': 'rog2', '15001b': 'cb' })
    expect(picIdAffiche('15001a', undefined)).toBe('15001a_rog2')
    expect(picIdAffiche('15001b', undefined)).toBe('15001b_cb')
  })

  it('laisse le scan à l\'alter ego choisi « standard » alors que le héros a un art', async () => {
    const { picIdAffiche } = await charger({ '15001': 'rog2', '15001b': 'standard' })
    expect(picIdAffiche('15001a', undefined)).toBe('15001a_rog2')
    expect(picIdAffiche('15001b', undefined)).toBe('15001b')
  })

  it('ne laisse pas le choix de l\'alter ego toucher la face héros', async () => {
    const { picIdAffiche } = await charger({ '15001b': 'cb' })
    expect(picIdAffiche('15001a', undefined)).toBe('15001a')
    expect(picIdAffiche('15001b', undefined)).toBe('15001b_cb')
  })

  it('garde le scan sans choix enregistré', async () => {
    const { picIdAffiche } = await charger({})
    expect(picIdAffiche('38002', undefined)).toBe('38002')
  })
})

describe("l'autre face dans l'aperçu agrandi", () => {
  beforeEach(() => window.localStorage.clear())

  it("porte l'art choisi, comme la face visible (Captain America « Comic »)", async () => {
    window.localStorage.setItem('mc_hero_art_v1', JSON.stringify({ '03001': 'cb' }))
    vi.resetModules()
    const { autresFacesDe } = await import('./card-model')
    const carte = { card_id: '03001a', is_face_up: true, down_card_ids: ['03001b'], info: {} }
    const catalogue = { type: () => 'AlterEgo' }
    const faces = autresFacesDe(carte as never, catalogue as never)
    expect(faces).toHaveLength(1)
    expect(faces[0].url).toContain('03001b_cb')
  })

  it("reste en scan standard sans choix d'art", async () => {
    vi.resetModules()
    const { autresFacesDe } = await import('./card-model')
    const carte = { card_id: '03001a', is_face_up: true, down_card_ids: ['03001b'], info: {} }
    const faces = autresFacesDe(carte as never, { type: () => 'AlterEgo' } as never)
    expect(faces[0].url).not.toContain('_cb')
  })
})
