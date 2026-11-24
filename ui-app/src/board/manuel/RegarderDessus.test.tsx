// @vitest-environment jsdom
// « Regarder les X cartes du dessus d'un deck » (mode manuel, demande du testeur du 09/11/2026) :
// un REGARD, jamais un geste. Ni commande moteur, ni carte déplacée, ni état partagé.
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { fireEvent, render, screen } from '@testing-library/react'
import { CoucheTriche } from '../CoucheTriche'
import type { WorldCard } from '../world'
import { cartesDuDessus, nombreARegarder, REGARD_PAR_DEFAUT, RegarderDessus } from './RegarderDessus'

const carte = (id: number): WorldCard =>
  ({ id, name: `Carte ${id}`, card_type: 'Event', pic_id: `9900${id}`, card_id: `9900${id}` }) as WorldCard

// Du FOND (id 1) vers le DESSUS (id 8), comme `pilesParDessus`.
const DECK = [1, 2, 3, 4, 5, 6, 7, 8].map(carte)

describe('nombreARegarder / cartesDuDessus', () => {
  it('5 par défaut, borné par la taille du deck, jamais moins de 1', () => {
    expect(REGARD_PAR_DEFAUT).toBe(5)
    expect(nombreARegarder(Number.NaN, 8)).toBe(5)
    expect(nombreARegarder(0, 8)).toBe(5)
    expect(nombreARegarder(3, 8)).toBe(3)
    expect(nombreARegarder(50, 8)).toBe(8)
    expect(nombreARegarder(5, 2)).toBe(2)
    expect(nombreARegarder(5, 0)).toBe(1)
  })

  it('montre la carte du DESSUS d’abord et ne modifie pas la pile', () => {
    const copie = [...DECK]
    expect(cartesDuDessus(DECK, 3).map((c) => c.id)).toEqual([8, 7, 6])
    expect(DECK).toEqual(copie)
  })
})

describe('<RegarderDessus>', () => {
  it('affiche les X cartes du dessus, numérotées, sans bouton d’action sur les cartes', () => {
    const { container } = render(<RegarderDessus cartes={DECK} x={3} onChangerX={() => {}} onToutVoir={() => {}} />)
    expect(container.querySelectorAll('.regarder-dessus-carte')).toHaveLength(3)
    expect(Array.from(container.querySelectorAll('img')).map((i) => i.getAttribute('alt'))).toEqual(['Carte 8', 'Carte 7', 'Carte 6'])
    expect(Array.from(container.querySelectorAll('.regarder-dessus-rang')).map((n) => n.textContent)).toEqual(['1', '2', '3'])
    expect(container.querySelectorAll('.pile-triche-carte button')).toHaveLength(0)
    expect(container.textContent).toContain('rien n’est déplacé')
  })

  it('le champ demande X, et « Voir toute la pile » revient en arrière', () => {
    const onChangerX = vi.fn()
    const onToutVoir = vi.fn()
    render(<RegarderDessus cartes={DECK} x={5} onChangerX={onChangerX} onToutVoir={onToutVoir} />)
    fireEvent.change(screen.getByLabelText('Nombre de cartes à regarder'), { target: { value: '2' } })
    expect(onChangerX).toHaveBeenCalledWith(2)
    fireEvent.click(screen.getByText('Voir toute la pile'))
    expect(onToutVoir).toHaveBeenCalled()
  })
})

describe('dans la pile ouverte du mode manuel', () => {
  beforeEach(() => {
    vi.stubGlobal('fetch', vi.fn(async () => ({ ok: true }) as Response))
  })

  const couche = (zone: string) => ({
    menu: undefined, pile: { titre: 'Deck du héros', cartes: DECK, duJoueur: true, zone, siege: 0 },
    setMenu: vi.fn(), setPile: vi.fn(),
    emettreGeste: vi.fn(async () => {}), executerGeste: vi.fn(async () => {}),
    capturerEnLot: vi.fn(async (agir: () => Promise<void> | void) => { await agir() }),
    misDeCote: [] as number[], envoyerMisDeCote: vi.fn(), envoyerSetVersRencontre: vi.fn(),
    cardIdDe: () => undefined, tirerAuHasard: vi.fn(), avisRefus: undefined, annulationEnCours: false,
    menuTable: undefined, setMenuTable: vi.fn(), choixCible: undefined, choisirCible: vi.fn(),
    attacherChoisie: vi.fn(), fermerChoixCible: vi.fn(), estEnMain: () => false, poserDepuisLaMain: vi.fn(),
    versLaMain: vi.fn(async () => true), mainAffichee: [], mulliganOuvert: false, setMulliganOuvert: vi.fn(),
    excedent: undefined, setExcedent: vi.fn(), defausserExcedent: vi.fn(), defausserAuHasard: vi.fn(),
    confirmerMulligan: vi.fn(), echangerAvecLeDessus: vi.fn(),
  })

  it('propose « Regarder le dessus » sur un deck, montre 5 cartes et ne déplace RIEN', () => {
    const c = couche('PlayerDeck')
    const { container } = render(<CoucheTriche actif manuel couche={c as never} />)
    expect(container.querySelectorAll('.pile-triche-carte')).toHaveLength(8)
    fireEvent.click(screen.getByText('Regarder le dessus'))
    expect(container.querySelectorAll('.regarder-dessus-carte')).toHaveLength(5)
    // La pile entière (et ses boutons « En main ») n'est plus affichée : aucune carte ne peut partir en main.
    expect(container.querySelectorAll('.pile-triche-carte button')).toHaveLength(0)
    expect(c.versLaMain).not.toHaveBeenCalled()
    expect(c.emettreGeste).not.toHaveBeenCalled()
    expect(c.executerGeste).not.toHaveBeenCalled()
    expect(fetch).not.toHaveBeenCalled()
    fireEvent.click(screen.getByText('Voir toute la pile'))
    expect(container.querySelectorAll('.pile-triche-carte')).toHaveLength(8)
  })

  it('aussi sur le deck Rencontre', () => {
    render(<CoucheTriche actif manuel couche={couche('EncounterDeck') as never} />)
    expect(screen.getByText('Regarder le dessus')).toBeTruthy()
  })

  it('pas sur une défausse (le dessus n’y a pas la même portée), ni hors mode manuel', () => {
    const { rerender } = render(<CoucheTriche actif manuel couche={couche('DiscardPile') as never} />)
    expect(screen.queryByText('Regarder le dessus')).toBeNull()
    rerender(<CoucheTriche actif manuel={false} couche={couche('PlayerDeck') as never} />)
    expect(screen.queryByText('Regarder le dessus')).toBeNull()
  })
})
