import { act, render } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { CoucheCurseurs } from './CoucheCurseurs'

let reponse: Record<string, unknown> = {}

beforeEach(() => {
  vi.useFakeTimers()
  const scene = document.createElement('div')
  scene.className = 'plateau-scene'
  scene.getBoundingClientRect = () => ({ left: 0, top: 0, width: 1000, height: 500 }) as DOMRect
  document.body.appendChild(scene)
  vi.stubGlobal(
    'fetch',
    vi.fn(async () => ({ ok: true, json: async () => reponse }))
  )
})

afterEach(() => {
  window.history.replaceState(null, '', '/')
  vi.useRealTimers()
  vi.unstubAllGlobals()
  document.body.innerHTML = ''
})

async function lecture() {
  await act(async () => {
    await vi.advanceTimersByTimeAsync(700)
  })
}

describe('onde au clic d un autre joueur', () => {
  it('rien a la premiere lecture, une onde par clic nouveau, retiree ensuite', async () => {
    reponse = { 1: { x: 0.5, y: 0.5, clic: 111 } }
    const { container } = render(<CoucheCurseurs actif monJoueur={0} nomsJoueurs={['A', 'B']} />)
    await lecture()
    expect(container.querySelectorAll('.curseur-onde')).toHaveLength(0)

    reponse = { 1: { x: 0.5, y: 0.5, clic: 222 } }
    await lecture()
    expect(container.querySelectorAll('.curseur-onde')).toHaveLength(1)

    await lecture()
    expect(container.querySelectorAll('.curseur-onde')).toHaveLength(0)
  })

  it('pas de nouvelle onde tant que le clic ne change pas, ni pour mon propre clic', async () => {
    reponse = { 1: { x: 0.2, y: 0.2, clic: 5 }, 0: { x: 0.1, y: 0.1, clic: 7 } }
    const { container } = render(<CoucheCurseurs actif monJoueur={0} nomsJoueurs={['A', 'B']} />)
    await lecture()
    reponse = { 1: { x: 0.9, y: 0.9, clic: 5 }, 0: { x: 0.1, y: 0.1, clic: 8 } }
    await lecture()
    expect(container.querySelectorAll('.curseur-onde')).toHaveLength(0)
  })
})

describe('joueur vu pour la premiere fois', () => {
  it('son dernier clic d avant n est pas rejoue', async () => {
    reponse = {}
    const { container } = render(<CoucheCurseurs actif monJoueur={0} nomsJoueurs={['A', 'B']} />)
    await lecture()
    reponse = { 1: { x: 0.5, y: 0.5, clic: 99 } }
    await lecture()
    expect(container.querySelectorAll('.curseur-onde')).toHaveLength(0)
    reponse = { 1: { x: 0.5, y: 0.5, clic: 100 } }
    await lecture()
    expect(container.querySelectorAll('.curseur-onde')).toHaveLength(1)
  })
})

describe('spectateur', () => {
  it('voit le curseur et l onde du joueur 0, meme si son propre siege vaut 0', async () => {
    window.history.replaceState(null, '', '/?spectateur')
    reponse = { 0: { x: 0.5, y: 0.5, clic: 1 } }
    const { container } = render(<CoucheCurseurs actif monJoueur={0} nomsJoueurs={['A']} />)
    await lecture()
    expect(container.querySelectorAll('.curseur-joueur')).toHaveLength(1)
    reponse = { 0: { x: 0.5, y: 0.5, clic: 2 } }
    await lecture()
    expect(container.querySelectorAll('.curseur-onde')).toHaveLength(1)
  })
})
