// Le mode « Detaille » existe, et c'est celui qu'on a en arrivant.
//
// Il remplace « manuel » comme defaut : la phase du mechant se deroule
// desormais etape par etape a moins qu'on ne demande explicitement d'aller
// plus vite. Les anciens modes « manuel » et « pas-a-pas » ont disparu : il ne
// reste que « detaille » (avec son reglage « avance auto ») et « instantane ».
import { describe, expect, it } from 'vitest'
import { lireAvanceAuto, libelleModePhase, lireModePhaseMechant, MODES } from './moteur'

describe('mode detaille', () => {
  it('figure dans la liste des modes', () => {
    expect(MODES).toContain('detaille')
  })

  it('est le mode par defaut, sans rien de memorise', () => {
    window.localStorage.clear()
    expect(lireModePhaseMechant()).toBe('detaille')
  })

  // Migration : « manuel » (case decochee) devient « detaille » SANS avance
  // auto - ce joueur cliquait pour avancer, il continue de cliquer.
  it('respecte encore l ancienne case a cocher decochee : detaille, sans avance auto', () => {
    window.localStorage.clear()
    window.localStorage.setItem('marvel-board-phase-rapide', 'off')
    expect(lireModePhaseMechant()).toBe('detaille')
    expect(lireAvanceAuto()).toBe(false)
  })

  // Ne garde plus que DEUX positions : « manuel » et « pas-a-pas » ont
  // disparu (le premier n'apportait rien que « detaille » ne fasse deja
  // mieux, le second est devenu le reglage « avance auto »).
  it('ne garde que deux positions', () => {
    expect(MODES).toEqual(['detaille', 'instantane'])
  })

  it('affiche son propre libelle, pas celui d un autre mode', () => {
    // Le panneau Options affichait « Instantane » pour le mode detaille,
    // pourtant le defaut : un ternaire a trois branches sans branche pour lui.
    expect(libelleModePhase('detaille')).toBe('Détaillé')
    expect(libelleModePhase('instantane')).toBe('Instantané')
  })
})
