// SUR TÉLÉPHONE, LA PHASE DU MÉCHANT EST D'OFFICE « GUIDÉE » (demande du 26/10/2026) : « pas d'autres choix ».
//
//  - le mode lu (`lireModePhaseMechant`) et la présentation lue (`lirePresentationPhase`) sont forcés à la LECTURE sur
//    téléphone : `detaille` + `tris` (Guidée), quoi que le joueur ait rangé (Accéléré, Plateau animé…) ;
//  - la préférence rangée n'est JAMAIS écrasée : un PC ou une tablette du même joueur la garde ;
//  - la ligne « Présentation » des réglages n'est pas affichée sur téléphone, et l'est toujours sur PC.
import { render, screen } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { CLE_MODE_PHASE, lireModePhaseMechant, modePhaseEffectif } from './moteur'
import { CLE_PRESENTATION_PHASE, lirePresentationPhase, presentationEffective } from './phase-presentation'
import { estTelephoneMaintenant } from './mobile/useModeMobile'
import { ContenuOnglet, type ProprietesReglages } from './FenetreReglages'

function simulerEcran(telephone: boolean): void {
  vi.stubGlobal(
    'matchMedia',
    (requete: string) =>
      ({
        matches: telephone && requete.includes('max-width: 767px'),
        media: requete,
        addEventListener: () => {},
        removeEventListener: () => {},
        addListener: () => {},
        removeListener: () => {},
        dispatchEvent: () => false,
        onchange: null,
      }) as unknown as MediaQueryList
  )
  window.matchMedia = globalThis.matchMedia
}

beforeEach(() => {
  window.localStorage.clear()
})
afterEach(() => {
  vi.unstubAllGlobals()
})

describe('les fonctions pures', () => {
  it('modePhaseEffectif : sur téléphone toujours detaille, ailleurs le mode rangé', () => {
    for (const mode of ['detaille', 'sur-table', 'instantane'] as const) {
      expect(modePhaseEffectif(mode, true)).toBe('detaille')
      expect(modePhaseEffectif(mode, false)).toBe(mode)
    }
  })

  it('presentationEffective : sur téléphone toujours « tris » (Guidée), ailleurs la présentation rangée', () => {
    for (const presentation of ['etape', 'bis', 'tris', 'dynamique'] as const) {
      expect(presentationEffective(presentation, true)).toBe('tris')
      expect(presentationEffective(presentation, false)).toBe(presentation)
    }
  })
})

describe('la lecture sur un vrai écran', () => {
  it('téléphone : un joueur qui avait choisi Accéléré joue en Guidée, sans que sa préférence soit écrasée', () => {
    simulerEcran(true)
    expect(estTelephoneMaintenant()).toBe(true)
    window.localStorage.setItem(CLE_MODE_PHASE, 'instantane')
    window.localStorage.setItem(CLE_PRESENTATION_PHASE, 'tris')
    expect(lireModePhaseMechant()).toBe('detaille')
    expect(lirePresentationPhase()).toBe('tris')
    expect(window.localStorage.getItem(CLE_MODE_PHASE)).toBe('instantane')
  })

  it('téléphone : Plateau animé rangé est lu en Guidée aussi', () => {
    simulerEcran(true)
    window.localStorage.setItem(CLE_MODE_PHASE, 'sur-table')
    expect(lireModePhaseMechant()).toBe('detaille')
    expect(window.localStorage.getItem(CLE_MODE_PHASE)).toBe('sur-table')
  })

  it('PC : rien ne change, Accéléré reste Accéléré', () => {
    simulerEcran(false)
    expect(estTelephoneMaintenant()).toBe(false)
    window.localStorage.setItem(CLE_MODE_PHASE, 'instantane')
    expect(lireModePhaseMechant()).toBe('instantane')
  })

  it('le réglage « Plateau PC » forcé sur un téléphone rend la main : le mode rangé est lu', () => {
    simulerEcran(true)
    window.localStorage.setItem('mode-plateau', 'pc')
    window.localStorage.setItem(CLE_MODE_PHASE, 'instantane')
    expect(estTelephoneMaintenant()).toBe(false)
    expect(lireModePhaseMechant()).toBe('instantane')
  })
})

function proprietes(telephone: boolean): ProprietesReglages {
  const base: Record<string, unknown> = {
    affichage: 'normal',
    modePhase: 'detaille',
    libelleModePhase: (mode: string) => mode,
    texteTempsParDecision: () => '',
    tempsParDecision: 0,
    revelation: 'court',
    telephone,
  }
  return new Proxy(base, { get: (objet, cle: string) => (cle in objet ? objet[cle] : vi.fn()) }) as unknown as ProprietesReglages
}

describe('les réglages', () => {
  it('PC : la ligne « Présentation » de la phase du méchant est là', () => {
    simulerEcran(false)
    render(<ContenuOnglet onglet="jeu" p={proprietes(false)} />)
    expect(screen.getByText('Présentation')).toBeTruthy()
    expect(screen.getByText('Accéléré')).toBeTruthy()
  })

  it('téléphone : pas de ligne « Présentation », pas de choix Accéléré / Plateau animé, une note dit que c’est la Guidée', () => {
    simulerEcran(true)
    render(<ContenuOnglet onglet="jeu" p={proprietes(true)} />)
    expect(screen.queryByText('Présentation')).toBeNull()
    expect(screen.queryByText('Accéléré')).toBeNull()
    expect(screen.getByText(/Guidée sur téléphone/)).toBeTruthy()
    // le délai automatique des étapes reste proposé : il vaut pour la Guidée
    expect(screen.getByText('Phase du méchant automatique')).toBeTruthy()
  })
})
