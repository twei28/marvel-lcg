// Charge les matchers DOM (toBeInTheDocument, toHaveClass...) pour tous les tests.
import '@testing-library/jest-dom/vitest'
import { vi } from 'vitest'

// jsdom ne fournit pas localStorage.clear - on le fournit.
if (typeof window !== 'undefined' && !window.localStorage.clear) {
  const data = new Map<string, string>()
  const mockStorage: Storage = {
    getItem: (key: string) => data.get(key) ?? null,
    setItem: (key: string, value: string) => data.set(key, value),
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
