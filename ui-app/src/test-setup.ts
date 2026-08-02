// Charge les matchers DOM (toBeInTheDocument, toHaveClass...) pour tous les tests.
import '@testing-library/jest-dom/vitest'
import { afterEach, vi } from 'vitest'

// jsdom n'implemente pas window.matchMedia. useModeMobile s'en sert pour savoir
// si l'ecran est etroit ou le pointeur grossier : sans ce bouchon, tout rendu de
// composant appelant le hook leverait une TypeError. Un test qui a besoin de
// piloter la valeur pose son propre bouchon avec vi.stubGlobal.
if (typeof window !== 'undefined' && !window.matchMedia) {
  window.matchMedia = ((media: string) => ({
    media,
    matches: false,
    onchange: null,
    addEventListener: () => {},
    removeEventListener: () => {},
    addListener: () => {},
    removeListener: () => {},
    dispatchEvent: () => false,
  })) as typeof window.matchMedia
}

// localStorage.clear() manque dans jsdom 26.1.0 en mode test
const ensureLocalStorageHasClear = () => {
  if (typeof window !== 'undefined' && typeof window.localStorage.clear !== 'function') {
    const data = new Map<string, string>()
    const storage = window.localStorage
    for (let i = 0; i < storage.length; i++) {
      const cle = storage.key(i)
      if (cle) data.set(cle, storage.getItem(cle)!)
    }
    const mockStorage: Storage = {
      getItem: (key: string) => data.get(key) ?? null,
      setItem: (key: string, value: string) => data.set(key, value),
      removeItem: (key: string) => data.delete(key),
      clear: () => data.clear(),
      length: 0,
      key: (index: number) => Array.from(data.keys())[index] ?? null,
    }
    Object.defineProperty(mockStorage, 'length', {
      get: () => data.size,
    })
    vi.stubGlobal('localStorage', mockStorage)
  }
}

ensureLocalStorageHasClear()

afterEach(() => {
  ensureLocalStorageHasClear()
})
