// Retours de Raven (iPhone, Safari, 12/10/2026), fiche
// .planning/todos/2026-10-12-mode-tablette.md :
// 2. une carte de la main ouverte en grand se change d'un glisser du doigt ;
// 3. l'identite montre son autre face sans changer de forme ;
// 1. la carte ouverte passe au-dessus de la fenetre du mulligan ;
// 4-7. les regles de mise en page (jsdom ne mesure rien : la mesure est
//      faite dans WebKit et Chromium, captures du 13/10/2026).
import { readFileSync } from 'node:fs'
import { act, fireEvent, render } from '@testing-library/react'
import { afterAll, afterEach, beforeAll, describe, expect, it, vi } from 'vitest'
import { PlateauPortrait } from './PlateauPortrait'
import { CarteOuverte, SEUIL_GLISSER_CARTE } from './CarteOuverte'
import { APPUI_LONG_MS } from './useAppuiLong'
import type { BoardProps } from '../Board'
import type { CleEmplacement, EmplacementAffiche, Plateau, UniteAffichee } from '../zones'
import type { ScanCardProps } from '../../components/ScanCard'

const unite = (cle: string, carte: Partial<ScanCardProps> = {}): UniteAffichee =>
  ({ cle, carte: { id: cle, name: cle, kind: 'event', imageUrl: `/scan/${cle}`, ...carte }, attachees: [] }) as UniteAffichee

const emplacement = (cle: CleEmplacement, ...unites: UniteAffichee[]): EmplacementAffiche =>
  ({ cle, titre: cle, groupes: [unites], nombreSurLaLigne: unites.length }) as EmplacementAffiche

const plateau = (...emplacements: EmplacementAffiche[]): Plateau =>
  ({ emplacements, nombreDeCartes: 0, idsAffiches: new Set(), representantsDePile: new Map(), nombreIgnore: 0 }) as Plateau

const monde = { render_id: 1, round_id: 1, phase: 'Player 1 Turn', players: [] } as unknown as BoardProps['world']

const nomOuvert = () => document.querySelector('.carte-ouverte')?.getAttribute('aria-label')

const glisser = (dx: number, dy = 0) => {
  const section = document.querySelector('.carte-ouverte')!
  fireEvent.pointerDown(section, { clientX: 200, clientY: 300 })
  fireEvent.pointerMove(section, { clientX: 200 + dx / 2, clientY: 300 + dy / 2 })
  fireEvent.pointerUp(section, { clientX: 200 + dx, clientY: 300 + dy })
}

afterEach(() => {
  vi.useRealTimers()
})

// jsdom n'a pas de PointerEvent : sans lui, fireEvent.pointer* perd clientX.
const avaitPointerEvent = 'PointerEvent' in window
beforeAll(() => {
  if (!avaitPointerEvent) {
    Object.defineProperty(window, 'PointerEvent', { configurable: true, value: class extends MouseEvent {} })
  }
})
afterAll(() => {
  if (!avaitPointerEvent) Reflect.deleteProperty(window, 'PointerEvent')
})

describe('carte de la main en grand : glisser vers ses voisines (retour 2)', () => {
  const ouvrirLaMainSur = (cle: string) => {
    render(
      <PlateauPortrait
        world={monde}
        playerId={0}
        plateau={plateau(emplacement('main', unite('11'), unite('12'), unite('13')))}
      />
    )
    fireEvent.click(document.querySelector('.encoche-main')!)
    fireEvent.click([...document.querySelectorAll('.main-portrait .scan-card')][Number(cle) - 11])
  }

  it('glisser a gauche ouvre la suivante, a droite la precedente', () => {
    ouvrirLaMainSur('12')
    expect(nomOuvert()).toBe('12')
    expect(document.querySelector('.carte-ouverte-position')).toHaveTextContent('2 / 3')
    glisser(-(SEUIL_GLISSER_CARTE + 10))
    expect(nomOuvert()).toBe('13')
    glisser(SEUIL_GLISSER_CARTE + 10)
    glisser(SEUIL_GLISSER_CARTE + 10)
    expect(nomOuvert()).toBe('11')
  })

  it('aux bouts de la main, le glisser ne fait rien (pas de boucle)', () => {
    ouvrirLaMainSur('11')
    glisser(SEUIL_GLISSER_CARTE + 10)
    expect(nomOuvert()).toBe('11')
    expect(document.querySelector('.carte-ouverte-voisine')).toBeDisabled()
  })

  it('un glisser trop court ou surtout vertical ne change pas de carte', () => {
    ouvrirLaMainSur('12')
    glisser(-(SEUIL_GLISSER_CARTE - 10))
    expect(nomOuvert()).toBe('12')
    glisser(-(SEUIL_GLISSER_CARTE + 10), 200)
    expect(nomOuvert()).toBe('12')
  })

  it('une carte de la TABLE ouverte en grand n a pas de voisines', () => {
    render(
      <PlateauPortrait
        world={monde}
        playerId={0}
        plateau={plateau(emplacement('rencontre', unite('7', { kind: 'villain' })), emplacement('main', unite('11'), unite('12')))}
      />
    )
    fireEvent.click(document.querySelector('.bande-carte .scan-card')!)
    expect(document.querySelector('.carte-ouverte')).not.toBeNull()
    expect(document.querySelector('.carte-ouverte-voisines')).toBeNull()
  })

  it('un doigt qui glisse lentement ne joue pas la carte (le maintien est annule)', () => {
    vi.useFakeTimers()
    const agir = vi.fn()
    render(<CarteOuverte carte={{ id: '5', name: '5', kind: 'event', imageUrl: '', onSelect: agir }} onFermer={() => {}} />)
    const scan = document.querySelector('.carte-ouverte-scan')!
    const section = document.querySelector('.carte-ouverte')!
    fireEvent.pointerDown(scan, { clientX: 200, clientY: 300 })
    fireEvent.pointerMove(section, { clientX: 170, clientY: 300 })
    act(() => {
      vi.advanceTimersByTime(APPUI_LONG_MS + 50)
    })
    expect(agir).not.toHaveBeenCalled()
  })
})

describe('l autre face d une carte recto-verso (retour 3)', () => {
  const peter: ScanCardProps = {
    id: '1',
    name: 'Peter Parker',
    kind: 'alter-ego',
    imageUrl: '/scan/01001b',
    autresFaces: [{ url: '/scan/01001a', type: 'Hero' }],
  }
  const image = () => document.querySelector('.carte-ouverte-scan img')?.getAttribute('src') ?? ''

  it('le bouton montre l autre face, puis revient a la face en jeu', () => {
    const changer = vi.fn()
    render(<CarteOuverte carte={{ ...peter, onSelect: changer }} onFermer={() => {}} />)
    expect(image()).toContain('01001b')
    fireEvent.click(document.querySelector('.carte-ouverte-face')!)
    expect(image()).toContain('01001a')
    expect(document.querySelector('.carte-ouverte-face')).toHaveTextContent('Face en jeu')
    fireEvent.click(document.querySelector('.carte-ouverte-face')!)
    expect(image()).toContain('01001b')
    // Regarder n'est pas jouer : la forme ne change pas.
    expect(changer).not.toHaveBeenCalled()
  })

  it('pas de bouton pour une carte a une seule face', () => {
    render(<CarteOuverte carte={{ id: '2', name: 'Quinjet', kind: 'support', imageUrl: '/scan/x' }} onFermer={() => {}} />)
    expect(document.querySelector('.carte-ouverte-face')).toBeNull()
  })
})

describe('la carte ouverte passe devant la fenetre du mulligan (retour 1)', () => {
  it('elle est montee dans <body>, hors du contexte d empilement du plateau', () => {
    render(
      <PlateauPortrait world={monde} playerId={0} plateau={plateau(emplacement('rencontre', unite('7', { kind: 'villain' })))} />
    )
    fireEvent.click(document.querySelector('.bande-carte .scan-card')!)
    const voile = document.querySelector('.carte-ouverte-voile')!
    expect(voile.parentElement).toBe(document.body)
    expect(voile.closest('.plateau-portrait')).toBeNull()
  })
})

describe('les regles de mise en page (retours 4 a 7)', () => {
  const PORTRAIT = readFileSync('src/board/mobile/portrait.css', 'utf-8')
  const BOARD = readFileSync('src/board/board.css', 'utf-8')

  it('4-5 : au telephone, les ameliorations se posent a plat, a gauche si le reglage le demande', () => {
    const bloc = PORTRAIT.slice(PORTRAIT.indexOf('@layer utilitaires'))
    expect(bloc).toMatch(/\.bande-rail \.plateau-unite \{[^}]*padding-left: 0;[^}]*padding-right: 0;/)
    expect(bloc).toMatch(/\.bande-rail \.est-attachee\.est-a-gauche \{\s*order: -1;/)
  })

  it('6 : telephone couche, le Fin du tour flottant s efface (la barre a le sien)', () => {
    expect(BOARD).toMatch(
      /@media \(pointer: coarse\) and \(orientation: landscape\) and \(max-height: 560px\) \{\s*\.bouton-fin-tour \{\s*display: none;/
    )
  })

  it('7 : ecran bas, la carte agrandie suit la hauteur de l ecran', () => {
    expect(BOARD).toMatch(/@media \(max-height: 560px\) \{\s*\.carte-apercu \{\s*--largeur-face: min\(345px, calc\(\(100dvh - 52px\) \* 127 \/ 176\)\);/)
  })
})
