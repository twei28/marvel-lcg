// Le plateau en bandes (spec du 12/09/2026) : quatre bandes, la main derriere
// son encoche, les piles derriere la leur, le bandeau qui porte le menu et
// l'action principale.
import { act, fireEvent, render, screen } from '@testing-library/react'
import { afterEach, describe, expect, it, vi } from 'vitest'
import { PlateauPortrait, questionSurLaMain } from './PlateauPortrait'
import { APPUI_LONG_MS } from './useAppuiLong'
import type { BoardProps } from '../Board'
import type { EtatInteractif } from '../interaction'
import type { CleEmplacement, EmplacementAffiche, Plateau, UniteAffichee } from '../zones'
import type { ScanCardProps } from '../../components/ScanCard'

const unite = (cle: string, carte: Partial<ScanCardProps>, extra: Partial<UniteAffichee> = {}): UniteAffichee =>
  ({ cle, carte: { id: cle, name: cle, kind: 'unknown', imageUrl: '', ...carte }, attachees: [], ...extra }) as UniteAffichee

const emplacement = (cle: CleEmplacement, ...unites: UniteAffichee[]): EmplacementAffiche =>
  ({ cle, titre: cle, groupes: [unites], nombreSurLaLigne: unites.length }) as EmplacementAffiche

const plateau = (...emplacements: EmplacementAffiche[]): Plateau =>
  ({ emplacements, nombreDeCartes: 0, idsAffiches: new Set(), representantsDePile: new Map(), nombreIgnore: 0 }) as Plateau

const monde = { render_id: 1, round_id: 1, phase: 'Player 1 Turn', players: [] } as unknown as BoardProps['world']

const rendre = (props: Partial<BoardProps>) =>
  render(<PlateauPortrait world={monde} playerId={0} plateau={plateau()} {...props} />)

afterEach(() => {
  vi.useRealTimers()
})

describe('PlateauPortrait — les quatre bandes', () => {
  it('rend les quatre bandes dans l ordre, chacune avec son texte quand elle est vide', () => {
    const { container } = rendre({})
    const bandes = [...container.querySelectorAll('.bande')].map((b) => b.className)
    expect(bandes).toEqual(['bande bande-vilain est-vide', 'bande bande-manigances est-vide', 'bande bande-engages est-vide', 'bande bande-heros est-vide'])
    expect(screen.getByText('Aucun ennemi engagé')).toBeInTheDocument()
    expect(screen.getByText('Aucune manigance')).toBeInTheDocument()
  })

  it('epingle le mechant, la manigance principale et l identite au bord gauche de leur bande', () => {
    const { container } = rendre({
      plateau: plateau(
        emplacement('rencontre', unite('rhino', { kind: 'villain' })),
        emplacement('complot-principal', unite('effraction', { kind: 'main-scheme', schemeThreat: '3/7' })),
        emplacement('complots-secondaires', unite('annexe', { kind: 'side-scheme' })),
        emplacement('terrain-soutien', unite('peter', { kind: 'alter-ego' }), unite('soutien', { kind: 'support' }))
      ),
    })
    expect(container.querySelector('.bande-vilain .est-epinglee [data-card-id="rhino"]')).not.toBeNull()
    expect(container.querySelector('.bande-manigances .est-epinglee [data-card-id="effraction"]')).not.toBeNull()
    expect(container.querySelector('.bande-manigances .bande-carte:not(.est-epinglee)[data-card-id="annexe"]')).not.toBeNull()
    expect(container.querySelector('.bande-heros .est-epinglee[data-card-id="peter"]')).not.toBeNull()
    expect(container.querySelector('.bande-heros .bande-carte:not(.est-epinglee)[data-card-id="soutien"]')).not.toBeNull()
  })

  it('tait la pastille « Manigance principale / annexe », que la bande repete deja', () => {
    const { container } = rendre({
      plateau: plateau(
        emplacement('complot-principal', unite('effraction', { kind: 'main-scheme' })),
        emplacement('complots-secondaires', unite('annexe', { kind: 'side-scheme' })),
        emplacement('terrain-combat', unite('sbire', { kind: 'minion' }))
      ),
    })
    expect(container.querySelectorAll('.bande-manigances .kind-pill')).toHaveLength(0)
    expect(container.querySelector('.bande-engages .kind-pill')).toHaveTextContent(/sbire/i)
  })

  it('dessine les attachements sous leur porteuse, comme le plateau PC', () => {
    const { container } = rendre({
      plateau: plateau(
        emplacement('rencontre', unite('rhino', { kind: 'villain' }, { attachees: [{ id: 'armure', name: 'Armure', kind: 'attachment', imageUrl: '' } as ScanCardProps] }))
      ),
    })
    expect(container.querySelector('.bande-vilain .plateau-unite .est-attachee .scan-card')).not.toBeNull()
  })

  it('laisse ScanCard poser ses pastilles (PV, menace) sur la carte', () => {
    const { container } = rendre({
      plateau: plateau(emplacement('rencontre', unite('rhino', { kind: 'villain', allyHp: '12/14' }))),
    })
    expect(container.querySelector('.bande-vilain .scan-card')?.textContent).toContain('12/14')
  })

  it('les onglets du multijoueur vivent dans l en-tete de la bande du heros', () => {
    const choisir = vi.fn()
    const { container } = rendre({
      joueursAffichables: [
        { id: 0, nom: 'Spider-Man' },
        { id: 1, nom: 'Hulk' },
      ],
      joueurRegarde: 0,
      choisirJoueurRegarde: choisir,
    })
    expect(container.querySelector('.bande-heros .bande-entete .portrait-onglets')).not.toBeNull()
    fireEvent.click(screen.getByRole('tab', { name: 'Hulk' }))
    expect(choisir).toHaveBeenCalledWith(1)
  })
})

describe('PlateauPortrait — le geste sur une carte', () => {
  it('tap = ouvrir en grand, sans agir', () => {
    const agir = vi.fn()
    const { container } = rendre({
      plateau: plateau(emplacement('rencontre', unite('7', { name: 'Rhino', kind: 'villain' }))),
      interactifs: new Map([[7, { role: 'cible', choisie: false, agir } as EtatInteractif]]),
    })
    fireEvent.click(container.querySelector('.bande-carte .scan-card')!)
    expect(screen.getByRole('dialog', { name: 'Rhino' })).toBeInTheDocument()
    expect(agir).not.toHaveBeenCalled()
    // La carte ouverte est DECOREE : l'action du moteur y est proposee.
    fireEvent.click(screen.getByRole('button', { name: /Utiliser cette carte/ }))
    expect(agir).toHaveBeenCalledTimes(1)
  })

  it('appui long = agir avec l action du moteur', () => {
    vi.useFakeTimers()
    const agir = vi.fn()
    const { container } = rendre({
      plateau: plateau(emplacement('rencontre', unite('7', { name: 'Rhino', kind: 'villain' }))),
      interactifs: new Map([[7, { role: 'cible', choisie: false, agir } as EtatInteractif]]),
    })
    fireEvent.pointerDown(container.querySelector('.bande-carte')!)
    act(() => {
      vi.advanceTimersByTime(APPUI_LONG_MS)
    })
    expect(agir).toHaveBeenCalledTimes(1)
  })

  it('appui long sans action directe = le menu des actions de la carte (onCardClick)', () => {
    vi.useFakeTimers()
    const onCardClick = vi.fn()
    const { container } = rendre({
      plateau: plateau(emplacement('rencontre', unite('7', { name: 'Rhino', kind: 'villain' }))),
      onCardClick,
    })
    fireEvent.pointerDown(container.querySelector('.bande-carte')!)
    act(() => {
      vi.advanceTimersByTime(APPUI_LONG_MS)
    })
    expect(onCardClick).toHaveBeenCalledTimes(1)
    expect(onCardClick.mock.calls[0]?.[0]).toMatchObject({ id: '7' })
  })
})

describe('PlateauPortrait — la main derriere son encoche', () => {
  const avecMain = plateau(emplacement('main', unite('quinjet', { kind: 'support' }), unite('backflip', { kind: 'event' })))

  it('est fermee au depart, l encoche dit combien de cartes, un tap l ouvre, le voile la ferme', () => {
    rendre({ plateau: avecMain })
    expect(document.querySelector('.main-feuille')).toBeNull()
    const encoche = document.querySelector('.encoche-main')!
    expect(encoche).toHaveAttribute('data-tactile', 'main')
    expect(encoche.querySelector('.encoche-nombre')).toHaveTextContent('2')
    fireEvent.click(encoche)
    expect(document.querySelectorAll('.main-feuille .main-portrait-carte')).toHaveLength(2)
    fireEvent.pointerDown(document.querySelector('.main-feuille-voile')!)
    expect(document.querySelector('.main-feuille')).toBeNull()
  })

  it('un swipe vers la gauche sur l encoche l ouvre aussi', () => {
    rendre({ plateau: avecMain })
    const encoche = document.querySelector('.encoche-main')!
    // jsdom n'a pas de PointerEvent : un MouseEvent au meme nom porte clientX.
    fireEvent(encoche, new MouseEvent('pointerdown', { bubbles: true, clientX: 470 }))
    fireEvent(encoche, new MouseEvent('pointermove', { bubbles: true, clientX: 430 }))
    expect(document.querySelector('.main-feuille')).not.toBeNull()
  })

  it('s ouvre toute seule quand une question porte sur une carte en main, et se range apres', () => {
    const { rerender } = render(
      <PlateauPortrait world={monde} playerId={0} plateau={avecMain} interactifs={new Map()} />
    )
    expect(document.querySelector('.main-feuille')).toBeNull()
    rerender(
      <PlateauPortrait
        world={monde}
        playerId={0}
        plateau={avecMain}
        interactifs={new Map([[Number('quinjet') || 0, { role: 'ressource', choisie: false, agir: () => {} } as EtatInteractif]])}
      />
    )
    // `quinjet` n'est pas un id numerique : on passe par un id qui l'est.
    expect(questionSurLaMain([unite('12', { kind: 'event' })], new Map([[12, { role: 'cible', choisie: false } as EtatInteractif]]))).toBe(true)
    expect(questionSurLaMain([unite('12', { kind: 'event' })], new Map([[12, { role: 'indisponible', choisie: false } as EtatInteractif]]))).toBe(false)
    // Une carte simplement JOUABLE (porteur) n'est pas une question : sinon
    // la main serait ouverte pendant tout le tour.
    expect(questionSurLaMain([unite('12', { kind: 'event' })], new Map([[12, { role: 'porteur', choisie: false } as EtatInteractif]]))).toBe(false)
    expect(questionSurLaMain([unite('12', { kind: 'event' })], new Map([[99, { role: 'cible', choisie: false } as EtatInteractif]]))).toBe(false)
  })

  it('en vrai : la question ouvre la main, sa fin la referme, mais pas si le joueur l avait ouverte lui-meme', () => {
    const main = plateau(emplacement('main', unite('12', { kind: 'event' })))
    const question = new Map([[12, { role: 'cible', choisie: false, agir: () => {} } as EtatInteractif]])
    const { rerender } = render(<PlateauPortrait world={monde} playerId={0} plateau={main} interactifs={new Map()} />)
    rerender(<PlateauPortrait world={monde} playerId={0} plateau={main} interactifs={question} />)
    expect(document.querySelector('.main-feuille')).not.toBeNull()
    rerender(<PlateauPortrait world={monde} playerId={0} plateau={main} interactifs={new Map()} />)
    expect(document.querySelector('.main-feuille')).toBeNull()
    // Ouverte a la main, elle survit a la question.
    fireEvent.click(document.querySelector('.encoche-main')!)
    rerender(<PlateauPortrait world={monde} playerId={0} plateau={main} interactifs={question} />)
    rerender(<PlateauPortrait world={monde} playerId={0} plateau={main} interactifs={new Map()} />)
    expect(document.querySelector('.main-feuille')).not.toBeNull()
  })
})

describe('PlateauPortrait — le tiroir des piles', () => {
  it('l encoche de gauche ouvre le tiroir, une pile par ligne, la consultable s etale', () => {
    rendre({
      plateau: plateau(
        emplacement(
          'piles-joueur',
          unite('joueur-deck', { name: 'Deck', pileCount: 30 }),
          unite('joueur-defausse', { name: 'Haymaker' }, { pileContenu: [{ id: 'h', name: 'Haymaker', kind: 'event', imageUrl: '' } as ScanCardProps], pileTitre: 'Défausse' })
        )
      ),
    })
    expect(document.querySelector('.tiroir')).toBeNull()
    fireEvent.click(document.querySelector('.encoche-piles')!)
    const piles = document.querySelectorAll('.tiroir-pile')
    expect(piles).toHaveLength(2)
    expect(piles[0]).toBeDisabled()
    expect(piles[0].textContent).toContain('Ton deck')
    expect(piles[0].textContent).toContain('30')
    fireEvent.click(piles[1])
    expect(document.querySelector('.plateau-regardees')).not.toBeNull()
    expect(document.querySelector('.tiroir')).toBeNull()
  })
})

describe('PlateauPortrait — le bandeau', () => {
  it('porte le menu « … » (les actions de partie) et l action principale', () => {
    const agir = vi.fn()
    rendre({
      actionsPartie: <div className="board-actions"><button type="button" className="bh-bouton bh-options">Options</button></div>,
      actionPrincipale: { libelle: 'Fin du tour', agir },
    })
    expect(document.querySelector('.pm-barre')).toBeNull()
    fireEvent.click(document.querySelector('.portrait-menu-bouton')!)
    expect(document.querySelector('.portrait-menu .bh-options')).not.toBeNull()
    fireEvent.click(document.querySelector('.portrait-action')!)
    expect(agir).toHaveBeenCalledTimes(1)
  })
})
