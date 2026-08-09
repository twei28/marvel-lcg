// Le journal ne doit contenir QUE la partie en cours.
//
// Il survit volontairement aux rechargements de page (bascule de langue, F5,
// reconnexion) via sessionStorage. Mais au premier montage il adoptait la
// partie en cours SANS rien vérifier — exactement ce qui protège le F5 — et
// gardait donc le journal d'une partie déjà finie au-dessus de la suivante.
// Signalé en jeu : « l'historique garde tout l'historique ».
//
// Ces tests verrouillent les deux exigences À LA FOIS : garder sur F5, jeter
// sur nouvelle partie. Corriger l'une en cassant l'autre est le piège.
import { afterEach, describe, expect, it } from 'vitest'
import { renderHook } from '@testing-library/react'
import { useHistoriquePartie } from './HistoriquePartie'

const CLE = 'marvel-historique-partie'

const entree = (titre: string) => ({
  cle: `k:${titre}`,
  type: 'text' as const,
  renderId: 1,
  round: 1,
  phase: '',
  titre,
})

/** Ce que sessionStorage contient après une partie déjà jouée. */
function semer(partieId: number | undefined, titres: string[]): void {
  const entrees = titres.map(entree)
  window.sessionStorage.setItem(
    CLE,
    JSON.stringify(partieId === undefined ? entrees : { partieId, entrees })
  )
}

const monter = (partieId: number | undefined) =>
  renderHook(() => useHistoriquePartie(undefined, undefined, partieId))

const titres = (resultat: { current: { entrees: { titre: string }[] } }) =>
  resultat.current.entrees.map((e) => e.titre)

afterEach(() => window.sessionStorage.clear())

describe('portée du journal', () => {
  it('garde le journal quand on recharge LA MÊME partie (F5)', () => {
    semer(77, ['Round 1', 'Batroc attaque'])
    const { result } = monter(77)
    expect(titres(result)).toEqual(['Round 1', 'Batroc attaque'])
  })

  it("jette le journal d'une partie PRÉCÉDENTE", () => {
    semer(77, ['Round 1', 'Batroc attaque'])
    const { result } = monter(78)
    expect(titres(result)).toEqual([])
  })

  it('jette aussi un journal sans étiquette (ancien format)', () => {
    // On ne peut pas savoir à quelle partie il appartenait : le garder
    // risquerait de recoller le journal d'hier sur la partie d'aujourd'hui.
    semer(undefined, ['Round 1'])
    const { result } = monter(77)
    expect(titres(result)).toEqual([])
  })

  it('jette le journal quand une nouvelle partie démarre SANS rechargement', () => {
    semer(77, ['Round 1'])
    const { result, rerender } = renderHook(
      ({ partie }: { partie: number }) => useHistoriquePartie(undefined, undefined, partie),
      { initialProps: { partie: 77 } }
    )
    expect(titres(result)).toEqual(['Round 1'])
    rerender({ partie: 78 })
    expect(titres(result)).toEqual([])
  })

  it("réétiquette ce qu'il garde, pour que la partie SUIVANTE le jette", () => {
    // Sans réécriture, un journal d'ancien format survivrait au premier
    // rechargement puis resterait éternellement non étiqueté.
    semer(77, ['Round 1'])
    monter(77)
    const brut = JSON.parse(window.sessionStorage.getItem(CLE) ?? 'null')
    expect(brut.partieId).toBe(77)
  })
})
