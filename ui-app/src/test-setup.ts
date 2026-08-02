// Charge les matchers DOM (toBeInTheDocument, toHaveClass...) pour tous les tests.
import '@testing-library/jest-dom/vitest'
import { vi } from 'vitest'

// jsdom n'implemente pas window.matchMedia. useModeMobile s'en sert pour
// ecouter les changements de media query. On fournit un stub en tant que
// Map de queries => listeners, pour que les tests fonctionnent.
if (typeof window !== 'undefined' && !window.matchMedia) {
  const mediaQueryListeners = new Map<string, Set<(e: MediaQueryListEvent) => void>>()

  vi.stubGlobal('matchMedia', (query: string) => {
    if (!mediaQueryListeners.has(query)) {
      mediaQueryListeners.set(query, new Set())
    }

    return {
      media: query,
      matches: false,
      onchange: null,
      addEventListener: (event: string, listener: (e: MediaQueryListEvent) => void) => {
        if (event === 'change') {
          mediaQueryListeners.get(query)?.add(listener)
        }
      },
      removeEventListener: (event: string, listener: (e: MediaQueryListEvent) => void) => {
        if (event === 'change') {
          mediaQueryListeners.get(query)?.delete(listener)
        }
      },
      dispatchEvent: () => true,
      addListener: () => {},
      removeListener: () => {},
    } as MediaQueryList
  })
}

// Polyfill localStorage.clear si manquant (jsdom ne le fournit pas).
if (typeof window !== 'undefined' && window.localStorage && !window.localStorage.clear) {
  const originalStorage = window.localStorage
  const data = new Map<string, string>()

  for (let i = 0; i < originalStorage.length; i++) {
    const cle = originalStorage.key(i)
    if (cle) data.set(cle, originalStorage.getItem(cle)!)
  }

  const mockStorage: Storage = {
    getItem: (key: string) => data.get(key) ?? null,
    setItem: (key: string, value: string) => {
      data.set(key, value)
    },
    removeItem: (key: string) => data.delete(key),
    clear: () => data.clear(),
    length: 0,
    key: (index: number) => {
      const keys = Array.from(data.keys())
      return keys[index] ?? null
    },
  }

  Object.defineProperty(mockStorage, 'length', {
    get: () => data.size,
  })

  vi.stubGlobal('localStorage', mockStorage)
}
