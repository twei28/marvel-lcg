import { describe, expect, it } from 'vitest'
import { appuiCompte, issueAppui } from './appui-tactile'
import { APPUI_LONG_MS } from '../mobile/useAppuiLong'
import { SEUIL_GLISSER } from '../glisser/useGlisser'

const appui = { x: 100, y: 200, debut: 1000 }

describe('appui long ou glisser, au doigt (lot 4, question 11)', () => {
  it('un doigt immobile assez longtemps ouvre le menu', () => {
    expect(issueAppui(appui, 1000 + APPUI_LONG_MS, 100, 200)).toBe('menu')
  })

  it('tant que la duree n est pas atteinte, on attend', () => {
    expect(issueAppui(appui, 1000 + APPUI_LONG_MS - 1, 100, 200)).toBe('attente')
  })

  it('un deplacement au-dela du seuil du glisser annule l appui, meme apres la duree', () => {
    expect(issueAppui(appui, 1000 + 10, 100 + SEUIL_GLISSER, 200)).toBe('glisser')
    expect(issueAppui(appui, 1000 + APPUI_LONG_MS + 50, 100, 200 + SEUIL_GLISSER)).toBe('glisser')
  })

  it('un tremblement sous le seuil ne compte pas', () => {
    expect(issueAppui(appui, 1000 + APPUI_LONG_MS, 103, 202)).toBe('menu')
  })

  it('seuls le doigt et le stylet comptent : la souris a deja son clic droit', () => {
    expect(appuiCompte('touch')).toBe(true)
    expect(appuiCompte('pen')).toBe(true)
    expect(appuiCompte('mouse')).toBe(false)
    expect(appuiCompte('')).toBe(false)
  })
})
