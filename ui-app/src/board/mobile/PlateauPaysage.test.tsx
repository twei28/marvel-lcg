import { afterEach, describe, expect, it, vi } from 'vitest'
import { fireEvent, render, screen } from '@testing-library/react'
import { PlateauPaysage } from './PlateauPaysage'
import { REQUETE_PAYSAGE } from './useOrientation'
import type { EtatInteractif } from '../interaction'
import type { EmplacementAffiche, Plateau, UniteAffichee } from '../zones'
import type { World } from '../world'

const MONDE = { phase: 'Player 1 Turn', round_id: 3, prompt: '', players: [] } as unknown as World

const unite = (id: string, name: string, kind: UniteAffichee['carte']['kind'], extra: Partial<UniteAffichee['carte']> = {}): UniteAffichee => ({
  cle: `u${id}`,
  carte: { id, name, kind, imageUrl: '', ...extra },
  attachees: [],
})

function plateau(emplacements: EmplacementAffiche[]): Plateau {
  return {
    emplacements,
    nombreDeCartes: emplacements.length,
    idsAffiches: new Set<number>(),
    representantsDePile: new Map<number, number>(),
    nombreIgnore: 0,
  }
}

const PLATEAU = plateau([
  { cle: 'rencontre', titre: 'Méchant', nombreSurLaLigne: 1, groupes: [[unite('1', 'Rhino', 'villain', { allyHp: '12/22' })]] },
  { cle: 'piles-rencontre', titre: 'Piles', nombreSurLaLigne: 1, groupes: [[{ ...unite('20', 'Encounter deck', 'villain', { facedown: true, pileCount: 23 }), pileTitre: 'Deck de rencontre' }]] },
  {
    cle: 'terrain-soutien', titre: 'Héros', nombreSurLaLigne: 3,
    groupes: [[unite('2', 'Spider-Man', 'hero')], [unite('3', 'Black Cat', 'hero')], [unite('4', 'Aunt May', 'ally')]],
    proprietaires: [0, 1, 1],
  },
  { cle: 'main', titre: 'Main', nombreSurLaLigne: 2, groupes: [[unite('5', 'Backflip', 'event'), unite('6', 'Enhanced Spider-Sense', 'event')]] },
])

/** Orientation simulee : paysage par defaut. */
function orienter(paysage: boolean) {
  vi.stubGlobal('matchMedia', (requete: string) => ({
    media: requete,
    matches: requete === REQUETE_PAYSAGE ? paysage : false,
    onchange: null,
    addEventListener: () => {},
    removeEventListener: () => {},
    addListener: () => {},
    removeListener: () => {},
    dispatchEvent: () => false,
  }))
}

const cartePosee = (id: string) =>
  document.querySelector<HTMLElement>(`.carte-posee:has(.scan-card[data-card-id="${id}"])`)

describe('PlateauPaysage', () => {
  afterEach(() => {
    vi.unstubAllGlobals()
    document.body.className = ''
  })

  it('dessine les deux rangees, la main et la barre, sans ecran portrait en paysage', () => {
    orienter(true)
    // BarreBas ne rend rien de vide (aucune demande, aucun outil) : on lui
    // donne un contenu minimal pour verifier qu'elle est bien branchee.
    render(<PlateauPaysage world={MONDE} playerId={0} plateau={PLATEAU} actionsPartie={<span>Actions</span>} />)
    expect(screen.getByRole('region', { name: 'Méchant' })).toBeInTheDocument()
    expect(screen.getByRole('region', { name: /Ton héros/ })).toBeInTheDocument()
    expect(cartePosee('1')).not.toBeNull()
    expect(screen.getByText('12/22')).toBeInTheDocument()
    expect(screen.getByText('Deck de rencontre')).toBeInTheDocument()
    expect(document.querySelector('.main-eventail')).toBeInTheDocument()
    expect(document.querySelector('.pm-barre')).toBeInTheDocument()
    expect(screen.queryByRole('dialog', { name: 'Tourne ton téléphone' })).toBeNull()
    expect(document.body).toHaveClass('mode-plateau-paysage')
  })

  it('couvre le plateau de l\'ecran portrait sans le demonter', () => {
    orienter(false)
    render(<PlateauPaysage world={MONDE} playerId={0} plateau={PLATEAU} />)
    expect(screen.getByRole('dialog', { name: 'Tourne ton téléphone' })).toBeInTheDocument()
    expect(cartePosee('1')).not.toBeNull()
    expect(document.querySelector('.plateau-paysage')).toHaveClass('est-portrait')
  })

  it('separe deux heros en deux groupes, le heros actif en premier et marque', () => {
    orienter(true)
    render(<PlateauPaysage world={MONDE} playerId={0} plateau={PLATEAU} heroActifId={3} />)
    const groupes = [...document.querySelectorAll<HTMLElement>('.rangee-heros .rangee-cartes-groupe')]
    // Black Cat (joueur 1) est active : son groupe passe devant celui de Spider-Man.
    expect(groupes[0]).toHaveClass('est-actif')
    expect(groupes[0].querySelector('.scan-card')).toHaveAttribute('data-card-id', '3')
    expect(groupes[1].querySelector('.scan-card')).toHaveAttribute('data-card-id', '2')
    expect(screen.getAllByRole('separator')).toHaveLength(1)
    // Le badge « Active » de ScanCard suit heroActifId.
    expect(groupes[0].querySelector('.scan-card')?.textContent).toMatch(/Active|Actif/)
  })

  it('le tap sur une carte l\'ouvre en grand, et l\'action part de la carte ouverte', () => {
    orienter(true)
    const agir = vi.fn()
    const interactifs = new Map<number, EtatInteractif>([[1, { role: 'porteur', choisie: false, agir }]])
    render(<PlateauPaysage world={MONDE} playerId={0} plateau={PLATEAU} interactifs={interactifs} />)
    fireEvent.click(cartePosee('1')!)
    expect(agir).not.toHaveBeenCalled()
    expect(screen.getByRole('dialog', { name: 'Rhino' })).toBeInTheDocument()
    fireEvent.click(screen.getByRole('button', { name: /Utiliser cette carte/ }))
    expect(agir).toHaveBeenCalledOnce()
  })

  it('pendant un ciblage, la rangee compte ses cibles et le plateau s\'eteint', () => {
    orienter(true)
    const interactifs = new Map<number, EtatInteractif>([[1, { role: 'cible', choisie: false, agir: () => {} }]])
    render(<PlateauPaysage world={MONDE} playerId={0} plateau={PLATEAU} interactifs={interactifs} />)
    expect(document.querySelector('.rangee-ennemie .rangee-cartes-cibles')).toHaveTextContent('1')
    expect(document.querySelector('.plateau-paysage')).toHaveClass('est-en-ciblage')
  })

  it('un paiement demande montre « Payer » avant d\'eteindre le plateau', () => {
    orienter(true)
    const interactifs = new Map<number, EtatInteractif>([[5, { role: 'ressource', choisie: false, agir: () => {} }]])
    render(<PlateauPaysage world={MONDE} playerId={0} plateau={PLATEAU} interactifs={interactifs} />)
    expect(document.querySelector('.plateau-paysage')).not.toHaveClass('est-en-paiement')
    fireEvent.click(screen.getByRole('button', { name: 'Payer' }))
    expect(document.querySelector('.plateau-paysage')).toHaveClass('est-en-paiement')
  })

  it('etale une pile epinglee au tap', () => {
    orienter(true)
    const defausse: EmplacementAffiche = {
      cle: 'piles-joueur', titre: 'Piles', nombreSurLaLigne: 1,
      groupes: [[{ ...unite('30', 'Backflip', 'event', { discard: true }), pileTitre: 'Défausse', pileContenu: [unite('31', 'Backflip', 'event').carte] }]],
    }
    render(<PlateauPaysage world={MONDE} playerId={0} plateau={plateau([...PLATEAU.emplacements, defausse])} />)
    fireEvent.click(screen.getByRole('button', { name: /Défausse/ }))
    expect(screen.getByRole('dialog', { name: 'Défausse' })).toBeInTheDocument()
  })

  // `annexes` melange des piles fondues et des cartes posees isolees
  // (preuves, regle, ressources) : seules les piles restent epinglees, les
  // cartes posees rejoignent la rangee heros qui defile.
  it('separe piles et cartes posees d\'annexes : la pile s\'epingle, la carte rejoint la rangee', () => {
    orienter(true)
    const annexes: EmplacementAffiche = {
      cle: 'annexes', titre: 'Annexes', nombreSurLaLigne: 2,
      groupes: [[
        { ...unite('40', 'Mise de côté', 'villain', { pileCount: 3 }), pileTitre: 'Mise de côté' },
        unite('41', 'Règle permanente', 'environment'),
      ]],
    }
    render(<PlateauPaysage world={MONDE} playerId={0} plateau={plateau([...PLATEAU.emplacements, annexes])} />)
    expect(document.querySelector('.rangee-heros .pile-epinglee')).toHaveTextContent('Mise de côté')
    expect(cartePosee('41')).not.toBeNull()
  })

  it('ancre le cartouche du deroule sur la vraie hauteur mesuree de la barre', () => {
    orienter(true)
    let rappel: (() => void) | undefined
    let cibleObservee: Element | undefined
    class ResizeObserverBouchon {
      constructor(callback: () => void) {
        rappel = callback
      }
      observe(cible: Element) {
        cibleObservee = cible
      }
      disconnect() {}
    }
    vi.stubGlobal('ResizeObserver', ResizeObserverBouchon)
    const { unmount } = render(
      <PlateauPaysage world={MONDE} playerId={0} plateau={PLATEAU} actionsPartie={<span>Actions</span>} />
    )
    // L'element observe doit etre la piste des rangees (`.pp-rangees`), pas la
    // racine du plateau : elle seule bouge quand la barre du bas change de taille.
    expect(cibleObservee).toHaveClass('pp-rangees')
    const barre = document.querySelector<HTMLElement>('.pm-barre')!
    Object.defineProperty(barre, 'offsetHeight', { value: 88, configurable: true })
    rappel?.()
    expect(document.body.style.getPropertyValue('--pp-barre-h')).toBe('88px')
    unmount()
    expect(document.body.style.getPropertyValue('--pp-barre-h')).toBe('')
  })

  it('un paiement par une identite posee', () => {
    orienter(true)
    const agir = vi.fn()
    // La carte id 2 (Spider-Man, terrain-soutien) porte le role « ressource » :
    // c'est une identite posee, pas une carte de la main.
    const interactifs = new Map<number, EtatInteractif>([[2, { role: 'ressource', choisie: false, agir }]])
    render(<PlateauPaysage world={MONDE} playerId={0} plateau={PLATEAU} interactifs={interactifs} />)
    fireEvent.click(screen.getByRole('button', { name: 'Payer' }))
    fireEvent.click(cartePosee('2')!)
    fireEvent.click(screen.getByRole('button', { name: /Utiliser/ }))
    expect(agir).toHaveBeenCalledOnce()
  })
})
