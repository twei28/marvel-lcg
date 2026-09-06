// Le mode « Detaille » existe, et c'est celui qu'on a en arrivant.
//
// Il remplace « manuel » comme defaut : la phase du mechant se deroule
// desormais etape par etape a moins qu'on ne demande explicitement d'aller
// plus vite. Les trois anciens modes restent disponibles.
import { describe, expect, it } from 'vitest'
import { libelleModePhase, lireModePhaseMechant, modeSuivant, MODES } from './moteur'

describe('mode detaille', () => {
  it('figure dans la liste des modes', () => {
    expect(MODES).toContain('detaille')
  })

  it('est le mode par defaut, sans rien de memorise', () => {
    window.localStorage.clear()
    expect(lireModePhaseMechant()).toBe('detaille')
  })

  it('respecte encore l ancienne case a cocher de ceux qui l avaient reglee', () => {
    // Migration : son ABSENCE ne dit rien et ne doit pas priver un nouveau venu
    // du mode detaille ; sa presence, elle, est un choix a honorer.
    window.localStorage.clear()
    window.localStorage.setItem('marvel-board-phase-rapide', 'off')
    expect(lireModePhaseMechant()).toBe('manuel')
  })

  it('laisse les trois anciens modes disponibles', () => {
    expect(MODES).toEqual(expect.arrayContaining(['manuel', 'pas-a-pas', 'instantane']))
  })

  it('affiche son propre libelle, pas celui d un autre mode', () => {
    // Le panneau Options affichait « Instantane » pour le mode detaille,
    // pourtant le defaut : un ternaire a trois branches sans branche pour lui.
    expect(libelleModePhase('detaille')).toBe('Détaillé')
    expect(libelleModePhase('manuel')).toBe('Manuel')
    expect(libelleModePhase('pas-a-pas')).toBe('Pas à pas')
    expect(libelleModePhase('instantane')).toBe('Instantané')
  })

  it('repasse par detaille dans le cycle du bouton Options', () => {
    // Le cycle a trois positions ne repassait jamais par « detaille » : un
    // seul clic desactivait la fonctionnalite pour toute la session.
    expect(modeSuivant('detaille')).toBe('manuel')
    expect(modeSuivant('manuel')).toBe('pas-a-pas')
    expect(modeSuivant('pas-a-pas')).toBe('instantane')
    expect(modeSuivant('instantane')).toBe('detaille')
  })
})
