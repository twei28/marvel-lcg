// LE SILENCE DE L'OUVERTURE VAUT AUSSI POUR LES SONS.
//
// La spec du 15/09/2026 : « aucun son pendant la mise en place ». Defaut
// trouve en relecture : `useSons` etait appele avant le retour anticipe du
// voile, et chaque trame de mise en place portant un `sound_name` etait donc
// jouee DERRIERE le voile. L'ouverture etait silencieuse a l'oeil, pas a
// l'oreille.
//
// ⚠ Les noms de sons different d'un cas a l'autre : `sons.ts` garde un cache
// module par nom de fichier, partage par tous les cas de ce fichier.
import { renderHook } from '@testing-library/react'
import { afterEach, describe, expect, it, vi } from 'vitest'
import { useSons } from './sons'
import type { World } from './world'

/** Ce que la trame du moteur porte de pertinent pour le son. */
function monde(renderId: number, son: string): World {
  return { render_id: renderId, sound_name: son } as unknown as World
}

/** Remplace l'element audio du navigateur, et note ce qui part. */
function ecouterLesSons(): string[] {
  const joues: string[] = []
  vi.stubGlobal(
    'Audio',
    class {
      volume = 0
      currentTime = 0
      constructor(public src: string) {}
      play() {
        joues.push(this.src)
        return Promise.resolve()
      }
    }
  )
  return joues
}

afterEach(() => {
  vi.unstubAllGlobals()
})

describe('useSons pendant le voile d’ouverture', () => {
  it('joue le son d’une trame ordinaire', () => {
    const joues = ecouterLesSons()
    renderHook(() => useSons(monde(9001, 'temoin-ordinaire'), true, false))
    expect(joues).toEqual(['/temoin-ordinaire.wav'])
  })

  it('⚠ NE JOUE AUCUN SON TANT QUE LE VOILE EST EN PLACE', () => {
    // LE CAS QUI COMPTE. La mise en place envoie ses trames une par une, et
    // chacune peut porter un `sound_name` : derriere le voile, on entendait
    // toute la table se monter.
    const joues = ecouterLesSons()
    renderHook(() => useSons(monde(9002, 'temoin-sous-le-voile'), true, false, true))
    expect(joues).toEqual([])
  })

  it('ne rattrape pas les sons avales quand le voile se leve', () => {
    // Une trame passee sous le voile est passee pour de bon : elle ne doit pas
    // repartir en rafale au moment ou la table apparait.
    const joues = ecouterLesSons()
    const { rerender } = renderHook(
      ({ voile }: { voile: boolean }) => useSons(monde(9003, 'temoin-rattrapage'), true, false, voile),
      { initialProps: { voile: true } }
    )
    rerender({ voile: false })
    expect(joues).toEqual([])
  })
})
