// La recherche dans les reglages (23/10/2026) : le filtre pur, puis la fenetre complete.
import { fireEvent, render, screen, within } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { correspond, filtrerReglages, normaliser } from './recherche-reglages'
import { FenetreReglages, ONGLETS, type ProprietesReglages } from './FenetreReglages'
import { reglerEpurePourTous } from './affichage'

describe('normaliser et correspond', () => {
  it('ignore la casse, les accents et les apostrophes', () => {
    expect(normaliser('  Météo  ET Décor ')).toBe('meteo et decor')
    expect(normaliser('Style d’affichage')).toBe('style d affichage')
  })
  it('tous les mots doivent se trouver, dans n’importe quel ordre', () => {
    expect(correspond('Barre d’avantage (estimation)', 'avantage barre')).toBe(true)
    expect(correspond('Barre d’avantage (estimation)', 'avantage son')).toBe(false)
  })
  it('requete vide : tout correspond', () => {
    expect(correspond('n’importe quoi', '   ')).toBe(true)
  })
})

function racine(): HTMLElement {
  const div = document.createElement('div')
  div.innerHTML = `
    <div data-onglet="jeu">
      <p class="reglages-groupe">Phase</p>
      <div class="ligne-option"><span class="ligne-option-libelle">Présentation<small>Étape par étape</small></span><span>Non 2 s 5 s</span></div>
      <div class="ligne-option"><span class="ligne-option-libelle">Carte révélée en grand</span></div>
      <p class="ligne-option-note">une note</p>
      <p class="reglages-groupe">Partie</p>
      <div class="ligne-option"><span class="ligne-option-libelle">Sauvegarde à chaque phase</span></div>
    </div>`
  return div
}
const visible = (el: Element | null) => !!el && !(el as HTMLElement).hidden

describe('filtrerReglages', () => {
  it('garde la ligne qui correspond, son titre, et cache le reste (notes comprises)', () => {
    const r = racine()
    expect(filtrerReglages(r, 'sauvegarde')).toBe(1)
    const [phase, partie] = Array.from(r.querySelectorAll('.reglages-groupe'))
    expect(visible(phase!)).toBe(false)
    expect(visible(partie!)).toBe(true)
    expect(visible(r.querySelector('.ligne-option-note'))).toBe(false)
  })
  it('les pastilles de choix ne comptent pas : « non » ne garde pas tout', () => {
    expect(filtrerReglages(racine(), 'non')).toBe(0)
  })
  it('l’aide d’une ligne se cherche aussi', () => {
    expect(filtrerReglages(racine(), 'etape par etape')).toBe(1)
  })
  it('les pastilles de l’aperçu d’ambiance suivent la ligne qui les précède', () => {
    const r = document.createElement('div')
    r.innerHTML = `<div data-onglet="apparence">
      <div class="ligne-option"><span class="ligne-option-libelle">Aperçu d’ambiance</span></div>
      <div class="apercu-pastilles">Auto Aucun Pluie</div>
      <div class="ligne-option"><span class="ligne-option-libelle">Animations</span></div></div>`
    filtrerReglages(r, 'apercu')
    expect(visible(r.querySelector('.apercu-pastilles'))).toBe(true)
    filtrerReglages(r, 'animations')
    expect(visible(r.querySelector('.apercu-pastilles'))).toBe(false)
  })

  it('requete vide : tout est remontre', () => {
    const r = racine()
    filtrerReglages(r, 'sauvegarde')
    expect(filtrerReglages(r, '')).toBe(3)
    expect(Array.from(r.querySelectorAll('[hidden]')).length).toBe(0)
  })
})

// --- La fenetre complete ---
function proprietes(sur: Partial<ProprietesReglages> = {}): ProprietesReglages {
  const f = vi.fn()
  return {
    affichage: 'epure', changerAffichage: f, animations: true, basculerAnimations: f, sons: true, basculerSons: f, musique: false,
    basculerMusique: f, scansFr: true, basculerScansFr: f, textesCdb: false, basculerTextesCdb: f, basculerLangue: f,
    modePhase: 'sur-table', changerModePhase: f, libelleModePhase: () => 'Plateau animé', tempsParDecision: 0, texteTempsParDecision: () => '',
    validationCourte: false, basculerValidationCourte: f, autoCible: true, basculerAutoCible: f, finTourAuto: false, basculerFinTourAuto: f,
    paiementAuto: false, basculerPaiementAuto: f, sauvegardeAuto: true, basculerSauvegardeAuto: f, revelation: 'court', cyclerRevelation: f,
    meteo: true, basculerMeteo: f, apercuMeteo: undefined, reglerApercuMeteo: f, reponseAmbiance: 'demander', cyclerReponseAmbiance: f,
    designEssai: true, basculerDesignEssai: f, modeActions: 'simple', changerModeActions: f, curseurs: true, basculerCurseurs: f,
    reglageMode: 'auto', cyclerReglageMode: f, montrerDisposition: false, telephone: false,
    ...sur,
  } as unknown as ProprietesReglages
}

describe('la recherche dans la fenetre des reglages', () => {
  beforeEach(() => window.localStorage.clear())
  afterEach(() => reglerEpurePourTous(true))

  const ouvrir = () => render(<FenetreReglages ouvert fermer={() => {}} {...proprietes()} />)
  const champ = () => screen.getByLabelText('Chercher un réglage') as HTMLInputElement

  it('retrouve un reglage d’un AUTRE onglet, avec son titre de section', () => {
    ouvrir()
    fireEvent.change(champ(), { target: { value: 'bruitages' } })
    const panneau = screen.getByRole('tabpanel')
    const visibles = Array.from(panneau.querySelectorAll<HTMLElement>('.ligne-option')).filter((e) => !e.hidden)
    // « Bruitages » et « Volume des bruitages » : les deux lignes qui portent le mot, rien d'autre.
    expect(visibles).toHaveLength(2)
    expect(within(visibles[0]!).getByText('Bruitages')).toBeTruthy()
    const titres = Array.from(panneau.querySelectorAll<HTMLElement>('.reglages-groupe')).filter((e) => !e.hidden)
    expect(titres.map((e) => e.textContent)).toEqual(['Sons'])
  })

  it('une recherche sans resultat le dit', () => {
    ouvrir()
    fireEvent.change(champ(), { target: { value: 'zzzzzz' } })
    expect(screen.getByText('Aucun réglage ne correspond à cette recherche.')).toBeTruthy()
  })

  it('Échap efface la recherche avant de fermer ; un clic sur un onglet la vide aussi', () => {
    ouvrir()
    fireEvent.change(champ(), { target: { value: 'meteo' } })
    fireEvent.keyDown(champ(), { key: 'Escape' })
    expect(champ().value).toBe('')
    fireEvent.change(champ(), { target: { value: 'meteo' } })
    fireEvent.click(screen.getByRole('tab', { name: 'Son' }))
    expect(champ().value).toBe('')
  })

  it('les quatre onglets restent proposes', () => {
    ouvrir()
    for (const o of ONGLETS) expect(screen.getAllByRole('tab').length).toBe(ONGLETS.length)
  })
})
