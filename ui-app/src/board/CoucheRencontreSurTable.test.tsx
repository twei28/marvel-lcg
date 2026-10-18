import { act, cleanup, render } from '@testing-library/react'
import { createRef } from 'react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { CoucheRencontreSurTable, type ControleRencontre } from './CoucheRencontreSurTable'
import type { EtapeDeroule } from './deroule-phase'
import { boiteDeCarte } from './mesures-plateau'
import type { ScanCardProps } from '../components/ScanCard'

vi.mock('./traduction-carte', () => ({
  ScanCardTraduite: ({ id }: { id: number }) => <div className="scan-card" data-card-id={id}><div className="scan-frame" /></div>,
}))

const revelation: EtapeDeroule = { cle: 'entree:1', temps: 'revelation', titre: 'revelation', regle: '', carteId: 66, boosts: [] }
const scans = (id: number): ScanCardProps => ({ id: String(id), name: `Carte ${id}`, kind: 'side-scheme', imageUrl: '/scan.png', isLandscape: true })
type Vol = { finir: () => void; cancel: ReturnType<typeof vi.fn>; setKeyframes: ReturnType<typeof vi.fn>; frames: Keyframe[]; options: KeyframeAnimationOptions }
let vols: Vol[]

beforeEach(() => {
  vols = []
  document.body.innerHTML = '<div class="plateau-cadre"><div class="zone-piles-rencontre"><div class="scan-card"></div></div><div class="scan-card" data-card-id="66"><div class="scan-frame"></div></div></div>'
  vi.spyOn(HTMLElement.prototype, 'getBoundingClientRect').mockImplementation(function (this: HTMLElement) {
    const largeur = this.classList.contains('plateau-cadre') ? 1280 : this.classList.contains('rencontre-sortie') ? 500 : 100
    return { x: 10, y: 50, left: 10, top: 50, width: largeur, height: 200, right: 10 + largeur, bottom: 250, toJSON: () => ({}) }
  })
  vi.stubGlobal('matchMedia', () => ({ matches: false }))
  Object.defineProperty(HTMLElement.prototype, 'animate', { configurable: true, writable: true, value: vi.fn((frames, options) => {
    let finir!: () => void
    const finished = new Promise<Animation>((resolve) => { finir = () => resolve({} as Animation) })
    const cancel = vi.fn()
    const setKeyframes = vi.fn()
    vols.push({ finir, cancel, setKeyframes, frames: frames as Keyframe[], options: options as KeyframeAnimationOptions })
    return { finished, cancel, effect: { setKeyframes } } as unknown as Animation
  }) })
})

afterEach(() => { cleanup(); Reflect.deleteProperty(HTMLElement.prototype, 'animate'); vi.restoreAllMocks(); vi.unstubAllGlobals(); document.body.innerHTML = '' })
const finir = async (...indices: number[]) => act(async () => { for (const i of indices) vols[i].finir(); await Promise.resolve() })

describe('lecture et trajet des cartes rencontre', () => {
  it('attend le clic après l’entrée, puis la fin du départ avant de continuer', async () => {
    const controle = createRef<ControleRencontre>()
    const suite = vi.fn()
    const r = render(<CoucheRencontreSurTable etape={revelation} boostsMontres={0} carteScene={scans} actif controle={controle} />)
    expect(vols).toHaveLength(1)
    await finir(0)
    expect(r.container.querySelector('[data-lecture="lecture"]')).not.toBeNull()
    expect(suite).not.toHaveBeenCalled()
    act(() => { expect(controle.current?.valider(suite)).toBe(true) })
    expect(vols).toHaveLength(2)
    expect(suite).not.toHaveBeenCalled()
    act(() => { controle.current?.valider(suite) })
    await finir(1)
    expect(suite).toHaveBeenCalledTimes(1)
    expect(r.container.querySelector('style')?.textContent).toBe('')
  })

  it('une nouvelle clé pour la même carte ne crée ni départ ni deuxième entrée', async () => {
    const controle = createRef<ControleRencontre>()
    const r = render(<CoucheRencontreSurTable etape={revelation} boostsMontres={0} carteScene={scans} actif controle={controle} />)
    await finir(0)
    r.rerender(<CoucheRencontreSurTable etape={{ ...revelation, cle: 'revelation:1' }} boostsMontres={0} carteScene={scans} actif controle={controle} />)
    expect(vols).toHaveLength(1)
    expect(r.container.querySelectorAll('.rencontre-sortie')).toHaveLength(1)
    expect(r.container.querySelector('style')?.textContent).toContain('visibility: hidden')
  })

  it('garde les deux boosts lisibles jusqu’à validation, après leurs entrées successives', async () => {
    const controle = createRef<ControleRencontre>()
    const suite = vi.fn()
    const etape: EtapeDeroule = { ...revelation, titre: 'attaque', temps: 'mechant', etat: 'resolu', boosts: [
      { cle: 'b1', cibleId: 70, nom: 'A', apport: 1 }, { cle: 'b2', cibleId: 71, nom: 'B', apport: 2 },
    ] }
    const r = render(<CoucheRencontreSurTable etape={etape} boostsMontres={2} carteScene={scans} actif controle={controle} />)
    expect(vols.map((v) => v.options.delay)).toEqual([0, 900])
    await finir(0)
    expect(r.container.querySelector('[data-lecture="entree"]')).not.toBeNull()
    await finir(1)
    expect(r.container.querySelector('.rencontre-total')?.textContent).toBe('Boost +3')
    expect(suite).not.toHaveBeenCalled()
    act(() => { controle.current?.valider(suite) })
    await finir(2)
    expect(suite).not.toHaveBeenCalled()
    await finir(3)
    expect(suite).toHaveBeenCalledOnce()
  })

  it('annule le départ et sa continuation si une autre étape prend la main', async () => {
    const controle = createRef<ControleRencontre>()
    const suite = vi.fn()
    const r = render(<CoucheRencontreSurTable etape={revelation} boostsMontres={0} carteScene={scans} actif controle={controle} />)
    await finir(0)
    act(() => { controle.current?.valider(suite) })
    r.unmount()
    await finir(1)
    expect(suite).not.toHaveBeenCalled()
    expect(vols[1].cancel).toHaveBeenCalled()
  })

  it('un clic pendant l’entrée est retenu sans couper le trajet ni doubler la validation', async () => {
    const controle = createRef<ControleRencontre>()
    const suite = vi.fn()
    render(<CoucheRencontreSurTable etape={revelation} boostsMontres={0} carteScene={scans} actif controle={controle} />)
    act(() => { controle.current?.valider(suite); controle.current?.valider(suite) })
    expect(vols).toHaveLength(1)
    expect(suite).not.toHaveBeenCalled()
    await finir(0)
    expect(vols).toHaveLength(2)
    expect(suite).not.toHaveBeenCalled()
    await finir(1)
    expect(suite).toHaveBeenCalledOnce()
  })

  it('sans animations, conserve la lecture au centre et ne bloque pas la validation', async () => {
    vi.stubGlobal('matchMedia', () => ({ matches: true }))
    const controle = createRef<ControleRencontre>()
    const suite = vi.fn()
    const r = render(<CoucheRencontreSurTable etape={revelation} boostsMontres={0} carteScene={scans} actif controle={controle} />)
    await act(async () => { await Promise.resolve() })
    expect(r.container.querySelector('[data-lecture="lecture"]')).not.toBeNull()
    await act(async () => { controle.current?.valider(suite); await Promise.resolve() })
    expect(suite).toHaveBeenCalledOnce()
    expect(vols).toHaveLength(0)
  })

  it('suit la destination si la table se réorganise pendant le départ', async () => {
    const images: FrameRequestCallback[] = []
    vi.spyOn(window, 'requestAnimationFrame').mockImplementation((cb) => { images.push(cb); return images.length })
    const controle = createRef<ControleRencontre>()
    render(<CoucheRencontreSurTable etape={revelation} boostsMontres={0} carteScene={scans} actif controle={controle} />)
    await finir(0)
    act(() => { controle.current?.valider(vi.fn()) })
    const mesurer = vi.mocked(HTMLElement.prototype.getBoundingClientRect).getMockImplementation()!
    vi.mocked(HTMLElement.prototype.getBoundingClientRect).mockImplementation(function (this: HTMLElement) {
      const r = mesurer.call(this)
      return this.classList.contains('scan-frame') && !this.closest('.rencontre-sur-table') ? { ...r, left: r.left + 100, x: r.x + 100 } : r
    })
    act(() => { images.shift()!(0) })
    expect(vols[1].setKeyframes).toHaveBeenCalledOnce()
    expect(vols[1].setKeyframes.mock.calls[0][0][1].transform).not.toBe(vols[1].frames[1].transform)
    await finir(1)
  })

  it('ignore les copies de lecture dans les mesures de destination', () => {
    const cadre = document.querySelector<HTMLElement>('.plateau-cadre')!
    cadre.querySelector('[data-card-id="66"]')!.remove()
    cadre.insertAdjacentHTML('beforeend', '<div class="rencontre-sur-table"><div class="scan-card" data-card-id="66"></div></div>')
    expect(boiteDeCarte(66, { element: cadre, origine: cadre.getBoundingClientRect() })).toBeUndefined()
  })
})
