// La pose des classes sur les vraies cartes du plateau.
//
// Imperatif, comme halo-statut.ts et pas-a-pas.ts : on ajoute des classes sur
// l'element reel, on les retire ensuite. Passer par React ferait re-rendre le
// plateau entier a chaque etape, pour une decoration transitoire.
import { afterEach, describe, expect, it, vi } from 'vitest'
import { renderHook } from '@testing-library/react'
import { useDerouleScene } from './useDerouleScene'
import type { EtapeDeroule } from './deroule-phase'

const etape = (extra: Partial<EtapeDeroule> = {}): EtapeDeroule => ({
  cle: 'k',
  temps: 'activations',
  titre: 'attaque',
  regle: 'regle:activations',
  boosts: [],
  consequences: [],
  ...extra,
})

/** Une fausse carte sur un faux plateau, comme le DOM reel les porte. */
function poserCarte(id: number): HTMLElement {
  let scene = document.querySelector('.plateau-scene')
  if (!scene) {
    scene = document.createElement('div')
    scene.className = 'plateau-scene'
    document.body.append(scene)
  }
  const carte = document.createElement('article')
  carte.className = 'scan-card'
  carte.setAttribute('data-card-id', String(id))
  scene.append(carte)
  return carte
}

afterEach(() => {
  document.body.innerHTML = ''
})

describe('pose de la mise en scene', () => {
  it('marque la carte qui agit', () => {
    const carte = poserCarte(50)
    renderHook(() => useDerouleScene(etape({ carteId: 50 }), true))
    expect(carte.classList.contains('deroule-en-avant')).toBe(true)
  })

  it('marque la cible a part', () => {
    const auteur = poserCarte(50)
    const cible = poserCarte(12)
    renderHook(() => useDerouleScene(etape({ carteId: 50, cibleId: 12 }), true))
    expect(auteur.classList.contains('deroule-en-avant')).toBe(true)
    expect(cible.classList.contains('deroule-cible')).toBe(true)
  })

  it('assombrit le plateau', () => {
    poserCarte(50)
    renderHook(() => useDerouleScene(etape({ carteId: 50 }), true))
    expect(document.body.classList.contains('deroule-voile')).toBe(true)
  })

  it('nettoie tout quand l etape change', () => {
    const carte = poserCarte(50)
    const { rerender } = renderHook(
      ({ e }: { e: EtapeDeroule | undefined }) => useDerouleScene(e, true),
      { initialProps: { e: etape({ carteId: 50 }) as EtapeDeroule | undefined } }
    )
    rerender({ e: etape({ cle: 'k2', carteId: undefined }) })
    expect(carte.classList.contains('deroule-en-avant')).toBe(false)
    expect(document.body.classList.contains('deroule-voile')).toBe(false)
  })

  it('nettoie tout au demontage', () => {
    // Sans cela, quitter la phase laisserait une carte agrandie et un plateau
    // assombri pour le reste de la partie.
    const carte = poserCarte(50)
    const { unmount } = renderHook(() => useDerouleScene(etape({ carteId: 50 }), true))
    unmount()
    expect(carte.classList.contains('deroule-en-avant')).toBe(false)
    expect(document.body.classList.contains('deroule-voile')).toBe(false)
  })

  it('ne pose rien quand la mise en scene est coupee', () => {
    const carte = poserCarte(50)
    renderHook(() => useDerouleScene(etape({ carteId: 50 }), false))
    expect(carte.classList.contains('deroule-en-avant')).toBe(false)
  })

  it('ne retire et ne repose rien quand l etape garde sa cle mais change d identite', () => {
    // `etape` vient de `etapes[index]`, reconstruit a chaque re-parse du
    // monde meme quand rien n'a change : un objet NEUF mais equivalent (meme
    // cle) ne doit pas faire retirer puis reposer les classes, sinon l'effet
    // se demonte/remonte a chaque trame (piege deja corrige dans
    // pas-a-pas.ts). On verrouille via un espion sur classList : aucun appel
    // add/remove ne doit survenir au second rendu.
    const carte = poserCarte(50)
    const { rerender } = renderHook(
      ({ e }: { e: EtapeDeroule | undefined }) => useDerouleScene(e, true),
      { initialProps: { e: etape({ carteId: 50 }) as EtapeDeroule | undefined } }
    )
    expect(carte.classList.contains('deroule-en-avant')).toBe(true)

    const ajoute = vi.spyOn(carte.classList, 'add')
    const retire = vi.spyOn(carte.classList, 'remove')

    // Meme cle ('k' par defaut), meme carteId, mais objet neuf.
    rerender({ e: etape({ carteId: 50 }) })

    expect(retire).not.toHaveBeenCalled()
    expect(ajoute).not.toHaveBeenCalled()
    expect(carte.classList.contains('deroule-en-avant')).toBe(true)
  })

  it('ne tombe pas sur une carte absente du plateau', () => {
    // Une carte peut avoir quitte la table entre le fait et son affichage.
    expect(() =>
      renderHook(() => useDerouleScene(etape({ carteId: 999 }), true))
    ).not.toThrow()
  })
})
