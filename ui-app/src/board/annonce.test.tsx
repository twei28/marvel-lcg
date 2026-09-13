// Le preavis du site, et son decompte.
//
// Ce que ces cas protegent : un deploiement fait `systemctl restart narwhal`,
// l'orchestrateur emporte ses moteurs, et toute partie en cours est perdue. Le
// bandeau est le seul avertissement que recoit un joueur. S'il se tait a tort,
// ou s'il ment sur le temps restant, il ne sert a rien.
//
// ⚠ LE DECOMPTE EST LOCAL, ET C'EST LE POINT DU FICHIER. Le serveur envoie les
// SECONDES QUI RESTENT, jamais une heure de fin : le navigateur d'un joueur
// peut avoir plusieurs minutes d'ecart avec celle du serveur. Les cas verifient
// donc que le temps descend tout seul entre deux interrogations.
import { describe, expect, it, vi, afterEach, beforeEach } from 'vitest'
import { render, act, renderHook } from '@testing-library/react'
import { BandeauAnnonce, delaiLisible } from './BandeauAnnonce'
import { useAnnonce, lireAnnonce, PERIODE_INTERROGATION_MS } from './annonce'

function repondre(corps: unknown, ok = true) {
  return vi.fn().mockResolvedValue({
    ok,
    json: async () => corps,
  } as unknown as Response)
}

afterEach(() => {
  vi.useRealTimers()
  vi.unstubAllGlobals()
})

describe('lecture de l annonce', () => {
  it('rend le texte et les secondes du serveur', async () => {
    vi.stubGlobal('fetch', repondre({ texte: 'Mise a jour', secondes: 420 }))
    expect(await lireAnnonce()).toEqual({ texte: 'Mise a jour', secondes: 420 })
  })

  it('se tait quand il n y a rien a dire', async () => {
    vi.stubGlobal('fetch', repondre({}))
    expect(await lireAnnonce()).toBeNull()
  })

  // Partie locale : aucun site derriere le moteur, qui repond un objet vide.
  // Le bandeau ne doit pas apparaitre avec un texte vide et un decompte a zero.
  it('se tait sur une annonce deja perimee', async () => {
    vi.stubGlobal('fetch', repondre({ texte: 'Mise a jour', secondes: 0 }))
    expect(await lireAnnonce()).toBeNull()
  })

  it('se tait sur un texte vide, meme avec du temps restant', async () => {
    vi.stubGlobal('fetch', repondre({ texte: '   ', secondes: 300 }))
    expect(await lireAnnonce()).toBeNull()
  })

  // Rien ici ne doit pouvoir interrompre une partie.
  it('avale une panne reseau', async () => {
    vi.stubGlobal('fetch', vi.fn().mockRejectedValue(new Error('hors ligne')))
    expect(await lireAnnonce()).toBeNull()
  })

  it('avale un refus du moteur', async () => {
    vi.stubGlobal('fetch', repondre({}, false))
    expect(await lireAnnonce()).toBeNull()
  })
})

describe('decompte', () => {
  beforeEach(() => {
    vi.useFakeTimers()
  })

  it('descend tout seul entre deux interrogations', async () => {
    vi.stubGlobal('fetch', repondre({ texte: 'Mise a jour', secondes: 120 }))
    const { result } = renderHook(() => useAnnonce())
    await act(async () => { await vi.advanceTimersByTimeAsync(0) })
    expect(result.current?.secondes).toBe(120)
    await act(async () => { await vi.advanceTimersByTimeAsync(10_000) })
    expect(result.current?.secondes).toBe(110)
  })

  it('se tait des que l echeance est passee, sans attendre la reponse suivante', async () => {
    vi.stubGlobal('fetch', repondre({ texte: 'Mise a jour', secondes: 5 }))
    const { result } = renderHook(() => useAnnonce())
    await act(async () => { await vi.advanceTimersByTimeAsync(0) })
    expect(result.current).not.toBeNull()
    await act(async () => { await vi.advanceTimersByTimeAsync(6_000) })
    expect(result.current).toBeNull()
  })

  it('reinterroge le moteur, pour voir une annonce posee en cours de partie', async () => {
    const appel = repondre({})
    vi.stubGlobal('fetch', appel)
    renderHook(() => useAnnonce())
    await act(async () => { await vi.advanceTimersByTimeAsync(0) })
    expect(appel).toHaveBeenCalledTimes(1)
    await act(async () => { await vi.advanceTimersByTimeAsync(PERIODE_INTERROGATION_MS) })
    expect(appel).toHaveBeenCalledTimes(2)
  })
})

describe('le bandeau', () => {
  it('montre le message du site et le delai', () => {
    const { container } = render(<BandeauAnnonce texte="Mise a jour du jeu" secondes={420} />)
    expect(container.querySelector('.bandeau-annonce')).not.toBeNull()
    expect(container.textContent).toContain('Mise a jour du jeu')
    expect(container.textContent).toContain('7 minutes')
  })

  // « 0 minute » se lirait comme « c'est deja fini » alors qu'il reste le
  // temps d'appuyer sur Save.
  it('ne dit jamais zero minute', () => {
    expect(delaiLisible(30)).not.toContain('0')
    expect(delaiLisible(30)).toContain('moins')
  })

  it('accorde le singulier', () => {
    expect(delaiLisible(90)).toBe('1 minute')
  })

  // Le bandeau s'adresse a quelqu'un qui regarde ailleurs : il doit etre
  // annonce aux lecteurs d'ecran sans qu'on aille le chercher.
  it('se signale comme une alerte', () => {
    const { container } = render(<BandeauAnnonce texte="Mise a jour" secondes={60} />)
    expect(container.querySelector('.bandeau-annonce')?.getAttribute('role')).toBe('alert')
  })
})
