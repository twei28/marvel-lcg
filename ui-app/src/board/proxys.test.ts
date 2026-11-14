import { describe, expect, it } from 'vitest'
import { estUnProxy } from './proxys'

describe('proxys', () => {
  it('signale le proxy de 63028 sur le scan comme sur la vignette, et rien ailleurs', () => {
    expect(estUnProxy('/scan/63028')).toBe(true)
    expect(estUnProxy('/vignette/63028')).toBe(true)
    expect(estUnProxy('/scan/63028?v=3')).toBe(true)
    expect(estUnProxy('/scan/63029')).toBe(false)
    expect(estUnProxy('/scan/fr_bl005')).toBe(false)
    expect(estUnProxy(undefined)).toBe(false)
  })
})
