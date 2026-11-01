// La FEUILLE de choix de cible au telephone (maquette approuvee par l'utilisateur, 26/10/2026) : une fenetre qui se glisse au doigt
// sur trois positions, avec, DEDANS, les ronds des cibles possibles (PV, statuts, ATQ / MNG) qu'on touche pour choisir.
import { act, fireEvent, render, screen } from '@testing-library/react'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import type { ScanCardProps } from '../../components/ScanCard'
import type { EtatInteractif } from '../interaction'
import type { UniteAffichee } from '../zones'
import type { DecorRonds } from './ronds/Rond'
import { FeuilleCibles, type FeuilleCiblesProps } from './FeuilleCibles'

const MESURES = () => ({ haute: 560, basse: 410, reduite: 120 })

const carte = (id: string, reste: Partial<ScanCardProps> = {}): ScanCardProps => ({
  id,
  name: `Sbire ${id}`,
  kind: 'minion',
  imageUrl: `/scan/${id}.jpg`,
  camp: 'encounter',
  jauge: { texte: '3/3', remplissage: 1, genre: 'pv', alarme: false },
  ...reste,
})
const statut = (id: string, name: string): ScanCardProps => ({ id, name, kind: 'status', imageUrl: `/scan/${id}.jpg` })
const unite = (id: string, reste: Partial<ScanCardProps> = {}, attachees: ScanCardProps[] = []): UniteAffichee => ({ cle: `u-${id}`, carte: carte(id, reste), attachees })
const etat = (reste: Partial<EtatInteractif> = {}): EtatInteractif => ({ role: 'cible', choisie: false, ...reste })

const decor = (interactifs: Map<number, EtatInteractif>, reste: Partial<DecorRonds> = {}): DecorRonds => ({
  interactifs,
  effets: new Map(),
  ouvrirPile: vi.fn(),
  ouvrirCarte: vi.fn(),
  agir: vi.fn(),
  ...reste,
})

function monter(reste: Partial<FeuilleCiblesProps> = {}) {
  const interactifs = new Map<number, EtatInteractif>([
    [1, etat()],
    [2, etat()],
  ])
  const props: FeuilleCiblesProps = {
    signature: 'q1',
    source: 'Marrow',
    consigne: 'Choisis la cible',
    compte: '0/1 requise(s) · 2 possible(s)',
    unites: [unite('1', {}, [statut('s1', 'Stunned')]), unite('2', { jauge: { texte: '1/3', remplissage: 0.33, genre: 'pv', alarme: false } })],
    decor: decor(interactifs),
    prete: false,
    libelleValider: 'Réponse Marrow',
    libelleAnnuler: 'Annuler',
    annuler: vi.fn(),
    valider: vi.fn(),
    mesures: MESURES,
    ...reste,
  }
  const rendu = render(<FeuilleCibles {...props} />)
  return { props, ...rendu }
}


// jsdom n'a pas de PointerEvent : `fireEvent.pointerMove` rend un Event nu, sans `clientY`. Un MouseEvent nomme `pointer*` porte les coordonnees.
const geste = (cible: EventTarget, type: string, y: number) =>
  act(() => {
    cible.dispatchEvent(new MouseEvent(type, { clientY: y, clientX: 0, button: 0, bubbles: true, cancelable: true }))
  })
const appuyer = (element: Element, y: number) => geste(element, 'pointerdown', y)
const bouger = (y: number) => geste(window, 'pointermove', y)
const relacher = (y: number) => geste(window, 'pointerup', y)

const feuille = () => document.querySelector('.est-feuille-cible') as HTMLElement
const poignee = () => document.querySelector('.feuille-poignee') as HTMLElement
const entete = () => document.querySelector('.feuille-entete') as HTMLElement

beforeEach(() => {
  window.sessionStorage.clear()
})

describe('ce que la feuille montre', () => {
  it('le titre de la source, la consigne et le compteur sont dans la fenetre', () => {
    monter()
    expect(screen.getByText('Marrow')).toBeTruthy()
    expect(screen.getByText('Choisis la cible')).toBeTruthy()
    expect(screen.getByText('0/1 requise(s) · 2 possible(s)')).toBeTruthy()
  })

  it('montre UN rond par cible possible, avec ses PV (pastille) et ses statuts', () => {
    monter()
    const ronds = document.querySelectorAll('.feuille-cibles .rond')
    expect(ronds).toHaveLength(2)
    expect(ronds[0]!.querySelector('.rond-pastille')!.textContent).toBe('3/3')
    expect(ronds[1]!.querySelector('.rond-pastille')!.textContent).toBe('1/3')
    expect(ronds[0]!.querySelector('.rond-etats')!.textContent).toContain('Stunned')
  })

  it('chaque rond se lit au lecteur d ecran : nom, PV, statuts', () => {
    monter()
    expect(screen.getByRole('button', { name: 'Sbire 1, 3/3, Stunned' })).toBeTruthy()
    expect(screen.getByRole('button', { name: 'Sbire 2, 1/3' })).toBeTruthy()
  })

  it('toucher un rond choisit la cible, comme sur la table', () => {
    const { props } = monter()
    fireEvent.click(screen.getByRole('button', { name: 'Sbire 2, 1/3' }))
    expect(props.decor.agir).toHaveBeenCalledTimes(1)
    expect((props.decor.agir as ReturnType<typeof vi.fn>).mock.calls[0]![0].id).toBe('2')
  })

  it('la cible choisie porte la marque de choix (anneau dore)', () => {
    const interactifs = new Map<number, EtatInteractif>([
      [1, etat({ choisie: true })],
      [2, etat()],
    ])
    monter({ decor: decor(interactifs) })
    expect(document.querySelectorAll('.feuille-cibles .rond.est-choisi')).toHaveLength(1)
    expect(document.querySelector('.feuille-cibles .rond.est-choisi')!.getAttribute('data-card-id')).toBe('1')
  })

  it('le bouton principal reste grise tant que le choix n est pas pret', () => {
    monter({ prete: false })
    expect((screen.getByRole('button', { name: 'Réponse Marrow' }) as HTMLButtonElement).disabled).toBe(true)
  })

  it('valider et annuler appellent leur action', () => {
    const { props } = monter({ prete: true })
    fireEvent.click(screen.getByRole('button', { name: 'Réponse Marrow' }))
    fireEvent.click(screen.getByRole('button', { name: 'Annuler' }))
    expect(props.valider).toHaveBeenCalledTimes(1)
    expect(props.annuler).toHaveBeenCalledTimes(1)
  })

  it('plus de cibles que la largeur n en tient : la rangee defile a l horizontale', () => {
    const unites = ['1', '2', '3', '4', '5'].map((id) => unite(id))
    monter({ unites, decor: decor(new Map(unites.map((u, i) => [i + 1, etat()]))) })
    expect(document.querySelectorAll('.feuille-cibles .rond')).toHaveLength(5)
    expect(document.querySelector('.feuille-cibles')!.getAttribute('data-defile')).toBe('horizontal')
  })
})

describe('la feuille se glisse au doigt', () => {
  it('commence en position basse', () => {
    monter()
    expect(feuille().getAttribute('data-position')).toBe('basse')
  })

  it('glisser la poignee vers le haut la fait monter en position haute', () => {
    monter()
    appuyer(poignee(), 600)
    bouger(500)
    bouger(300)
    relacher(300)
    expect(feuille().getAttribute('data-position')).toBe('haute')
  })

  it('glisser le TITRE marche aussi, vers le bas jusqu a la position reduite', () => {
    monter()
    appuyer(entete(), 300)
    bouger(450)
    bouger(700)
    relacher(700)
    expect(feuille().getAttribute('data-position')).toBe('reduite')
  })

  it('un toucher sans glisser ne bouge pas la feuille', () => {
    monter()
    appuyer(poignee(), 600)
    relacher(601)
    expect(feuille().getAttribute('data-position')).toBe('basse')
  })

  it('au clavier : fleche haut = haute, fleche bas = reduite', () => {
    monter()
    fireEvent.keyDown(poignee(), { key: 'ArrowUp' })
    expect(feuille().getAttribute('data-position')).toBe('haute')
    fireEvent.keyDown(poignee(), { key: 'ArrowDown' })
    fireEvent.keyDown(poignee(), { key: 'ArrowDown' })
    expect(feuille().getAttribute('data-position')).toBe('reduite')
  })

  it('la position choisie est gardee tant que la question dure, et oubliee a la question suivante', () => {
    const { props, rerender } = monter()
    fireEvent.keyDown(poignee(), { key: 'ArrowUp' })
    expect(feuille().getAttribute('data-position')).toBe('haute')
    // la meme question se redessine (un choix de plus) : la feuille reste ou le joueur l'a mise
    rerender(<FeuilleCibles {...props} compte="1/1 requise(s) · 2 possible(s)" />)
    expect(feuille().getAttribute('data-position')).toBe('haute')
    // une AUTRE question : retour a la position basse
    rerender(<FeuilleCibles {...props} signature="q2" />)
    expect(feuille().getAttribute('data-position')).toBe('basse')
  })

  it('la poignee et le titre ne laissent pas le geste filer vers la page (touch-action: none)', () => {
    monter()
    expect(poignee().getAttribute('data-geste')).toBe('feuille')
    expect(entete().getAttribute('data-geste')).toBe('feuille')
  })
})

describe('la feuille ne vole rien a la table', () => {
  it('annonce sa position au lecteur d ecran et se range comme une fenetre de decision', () => {
    monter()
    expect(feuille().getAttribute('role')).toBe('dialog')
    expect(feuille().getAttribute('aria-label')).toBe('Choisis la cible')
    expect(poignee().getAttribute('aria-label')).toBeTruthy()
  })

  it('le geste est suivi sur la FENETRE : un doigt qui quitte la poignee continue de la tirer', () => {
    monter()
    appuyer(poignee(), 600)
    bouger(350)
    expect(feuille().classList.contains('est-glissee')).toBe(true)
    relacher(250)
    expect(feuille().classList.contains('est-glissee')).toBe(false)
  })
})
