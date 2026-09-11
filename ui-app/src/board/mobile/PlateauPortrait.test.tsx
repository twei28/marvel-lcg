import { fireEvent, render, screen } from '@testing-library/react'
import { afterEach, describe, expect, it, vi } from 'vitest'
import { PlateauPortrait } from './PlateauPortrait'
import { APPUI_LONG_MS } from './useAppuiLong'
import type { BoardProps } from '../Board'
import type { EmplacementAffiche, Plateau, UniteAffichee } from '../zones'
import type { CleEmplacement } from '../zones'
import type { ScanCardProps } from '../../components/ScanCard'

const unite = (cle: string, carte: Partial<ScanCardProps>): UniteAffichee =>
  ({ cle, carte: { id: cle, name: cle, kind: 'unknown', imageUrl: '', ...carte }, attachees: [] }) as UniteAffichee

const emplacement = (cle: CleEmplacement, ...unites: UniteAffichee[]): EmplacementAffiche =>
  ({ cle, titre: cle, groupes: [unites], nombreSurLaLigne: unites.length }) as EmplacementAffiche

const plateau = (...emplacements: EmplacementAffiche[]): Plateau =>
  ({ emplacements, nombreDeCartes: 0, idsAffiches: new Set(), representantsDePile: new Map(), nombreIgnore: 0 }) as Plateau

const monde = { render_id: 1, round_id: 1, phase: 'Player 1 Turn', players: [] } as unknown as BoardProps['world']

describe('PlateauPortrait — bloc complot', () => {
  it('pose la manigance principale en petit, avec sa menace en cases a cote', () => {
    const { container } = render(
      <PlateauPortrait
        world={monde}
        playerId={0}
        plateau={plateau(
          emplacement(
            'complot-principal',
            unite('L’Effraction', { name: 'L’Effraction', kind: 'main-scheme', schemeThreat: '3/6' })
          )
        )}
      />
    )
    expect(container.querySelector('.portrait-nom')).toHaveTextContent('L’Effraction')
    expect(document.querySelectorAll('.barre-menace-case')).toHaveLength(6)
    expect(document.querySelectorAll('.barre-menace-case.est-pose')).toHaveLength(3)
  })

  it('ne pose jamais de chiffre sur l illustration de la manigance', () => {
    // Regle centrale du chantier (deja violee une fois a la tache 4) : un
    // chiffre ne va jamais sur le scan. Meme si `stats` trainait dessus.
    render(
      <PlateauPortrait
        world={monde}
        playerId={0}
        plateau={plateau(
          emplacement(
            'complot-principal',
            unite('Complot', {
              name: 'Complot',
              kind: 'main-scheme',
              schemeThreat: '2/5',
              stats: [{ label: 'ATQ', value: 2 }],
            })
          )
        )}
      />
    )
    expect(document.querySelector('.scan-card .scan-stats-calee')).toBeNull()
  })

  it('ne pose aucune pastille de menace sur l illustration : la BarreMenace suffit', () => {
    // Defaut corrige (post tache 6) : CarteAvecChiffres ne retirait pas
    // `schemeThreat`, donc ScanCard posait SA PROPRE pastille de menace sur
    // le scan en plus de la BarreMenace, doublon exactement inverse de celui
    // que la BarreMenace existe pour eviter.
    render(
      <PlateauPortrait
        world={monde}
        playerId={0}
        plateau={plateau(
          emplacement(
            'complot-principal',
            unite('Complot', { name: 'Complot', kind: 'main-scheme', schemeThreat: '3/6' })
          )
        )}
      />
    )
    expect(document.querySelector('.scan-card .scheme-threat-badge')).toBeNull()
  })

  it('sans manigance principale, ne dessine ni carte ni barre', () => {
    const { container } = render(<PlateauPortrait world={monde} playerId={0} plateau={plateau()} />)
    expect(container.querySelector('.barre-menace-bloc')).toBeNull()
  })
})

describe('PlateauPortrait — bloc vilain', () => {
  it('montre les PV du vilain a cote, jamais sur l illustration', () => {
    // Defaut corrige (post tache 6) : chiffresDe ne lisait QUE `stats`, vide
    // tant qu'aucune stat n'est modifiee — le vilain n'affichait donc
    // quasiment jamais ses PV a cote, pendant que ScanCard les dessinait
    // LUI-MEME sur la carte (jauge-carte). Repere sur play.marvelsimulator.com :
    // le vilain montre son "10/10" a cote.
    const { container } = render(
      <PlateauPortrait
        world={monde}
        playerId={0}
        plateau={plateau(
          emplacement(
            'terrain-combat',
            unite('Rhino', {
              name: 'Rhino',
              kind: 'villain',
              jauge: { remplissage: 1, genre: 'pv', alarme: false, texte: '10 / 10' },
            })
          )
        )}
      />
    )
    expect(screen.getByText('10 / 10')).toBeInTheDocument()
    expect(container.querySelector('.scan-card .jauge-carte')).toBeNull()
  })
})

describe('PlateauPortrait — compteurs de rencontre', () => {
  it('compte le deck et la defausse de rencontre', () => {
    render(
      <PlateauPortrait
        world={monde}
        playerId={0}
        plateau={plateau(
          emplacement(
            'piles-rencontre',
            unite('rencontre-encounter-deck', { pileCount: 33 }),
            unite('rencontre-encounter-discard', { pileCount: 0 })
          )
        )}
      />
    )
    expect(screen.getByText('33')).toBeInTheDocument()
    expect(screen.getAllByText('0').length).toBeGreaterThan(0)
  })

  it('sans pile de rencontre, montre des compteurs a zero plutot que rien', () => {
    // Un bloc qui apparait/disparait ferait sauter la hauteur des autres
    // (spec du 11/09/2026) : la rencontre montre toujours ses compteurs.
    const { container } = render(<PlateauPortrait world={monde} playerId={0} plateau={plateau()} />)
    expect(container.querySelector('.portrait-compteurs')).not.toBeNull()
  })
})

describe('PlateauPortrait — ennemis engages, heros et allies', () => {
  it('dit qu aucun ennemi n est engage quand le bloc est vide', () => {
    render(<PlateauPortrait world={monde} playerId={0} plateau={plateau()} />)
    expect(screen.getByText('Aucun ennemi engagé')).toBeInTheDocument()
  })

  it('montre les ennemis engages quand il y en a', () => {
    // getByText('Baron Zemo') matcherait DEUX noeuds : le nom affiche
    // (.portrait-nom) et le texte de secours que ScanCard pose derriere
    // l'image (.scan-fallback, aria-hidden mais toujours dans le DOM). On
    // cible donc le nom affiche precisement, comme les autres tests de ce
    // fichier (bloc complot, ci-dessus).
    const { container } = render(
      <PlateauPortrait
        world={monde}
        playerId={0}
        plateau={plateau(emplacement('nemesis', unite('Baron Zemo', { name: 'Baron Zemo', kind: 'minion' })))}
      />
    )
    expect(container.querySelector('.portrait-engages .portrait-nom')).toHaveTextContent('Baron Zemo')
    expect(screen.queryByText('Aucun ennemi engagé')).toBeNull()
  })

  it('montre le heros et ses allies', () => {
    const { container } = render(
      <PlateauPortrait
        world={monde}
        playerId={0}
        plateau={plateau(
          emplacement(
            'terrain-soutien',
            unite('Steve Rogers', { name: 'Steve Rogers', kind: 'hero' }),
            unite('Hope Summers', { name: 'Hope Summers', kind: 'ally' })
          )
        )}
      />
    )
    const noms = Array.from(container.querySelectorAll('.portrait-heros .portrait-nom')).map((el) => el.textContent)
    expect(noms).toEqual(['Steve Rogers', 'Hope Summers'])
  })

  it('montre les PV d un ennemi engage a cote (jauge), rien sur l illustration', () => {
    const { container } = render(
      <PlateauPortrait
        world={monde}
        playerId={0}
        plateau={plateau(
          emplacement(
            'nemesis',
            unite('Baron Zemo', {
              name: 'Baron Zemo',
              kind: 'minion',
              jauge: { remplissage: 0.5, genre: 'pv', alarme: false, texte: '5 / 10' },
            })
          )
        )}
      />
    )
    expect(screen.getByText('5 / 10')).toBeInTheDocument()
    expect(container.querySelector('.scan-card .jauge-carte')).toBeNull()
  })

  it('montre les PV d un allie a cote (allyHp, sans jauge calculable), rien sur l illustration', () => {
    const { container } = render(
      <PlateauPortrait
        world={monde}
        playerId={0}
        plateau={plateau(
          emplacement('terrain-soutien', unite('Hope Summers', { name: 'Hope Summers', kind: 'ally', allyHp: '3/3' }))
        )}
      />
    )
    expect(screen.getByText('3/3')).toBeInTheDocument()
    expect(container.querySelector('.scan-card .ally-hp-badge')).toBeNull()
  })

  it('ne pose jamais de chiffre sur l illustration d un engage ou d un allie', () => {
    // Meme regle que pour le complot (tache 5) : `stats` ne doit jamais
    // atterrir sur ScanCard directement, meme via ces nouveaux blocs.
    render(
      <PlateauPortrait
        world={monde}
        playerId={0}
        plateau={plateau(
          emplacement(
            'nemesis',
            unite('Rhino', { name: 'Rhino', kind: 'minion', stats: [{ label: 'ATQ', value: 4 }] })
          )
        )}
      />
    )
    expect(document.querySelector('.scan-card .scan-stats-calee')).toBeNull()
  })
})

describe('PlateauPortrait — main et barre du bas', () => {
  it('affiche les cartes de la main : sixieme bloc de repartirEnBlocs, pas seulement teste en isolation', () => {
    const { container } = render(
      <PlateauPortrait
        world={monde}
        playerId={0}
        plateau={plateau(
          emplacement(
            'main',
            unite('Quinjet', { name: 'Quinjet', kind: 'event' }),
            unite('Backflip', { name: 'Backflip', kind: 'event' })
          )
        )}
      />
    )
    expect(container.querySelectorAll('.main-portrait .scan-card')).toHaveLength(2)
  })

  it('un tap sur une carte de la main remonte props.onCardClick, avec la bonne carte', () => {
    const onCardClick = vi.fn()
    const { container } = render(
      <PlateauPortrait
        world={monde}
        playerId={0}
        onCardClick={onCardClick}
        plateau={plateau(emplacement('main', unite('Quinjet', { name: 'Quinjet', kind: 'event' })))}
      />
    )
    fireEvent.click(container.querySelector('.main-portrait .scan-card') as Element)
    expect(onCardClick).toHaveBeenCalledTimes(1)
    expect(onCardClick.mock.calls[0]?.[0]).toMatchObject({ id: 'Quinjet', name: 'Quinjet' })
  })

  it('un re-tap sur la carte deja focalisee la ferme via onFermerCarte, sans repasser par onCardClick', () => {
    // `carteFocalisee` est deja pose par board.tsx apres un premier tap
    // (task 7) : geste-carte.ts s'y raccroche au lieu d'inventer un etat
    // d'ouverture parallele (decision du 11/09/2026).
    const onCardClick = vi.fn()
    const onFermerCarte = vi.fn()
    const { container } = render(
      <PlateauPortrait
        world={monde}
        playerId={0}
        onCardClick={onCardClick}
        carteFocalisee={42}
        onFermerCarte={onFermerCarte}
        plateau={plateau(emplacement('main', unite('42', { id: '42', name: 'Quinjet', kind: 'event' })))}
      />
    )
    fireEvent.click(container.querySelector('.main-portrait .scan-card') as Element)
    expect(onFermerCarte).toHaveBeenCalledTimes(1)
    expect(onCardClick).not.toHaveBeenCalled()
  })

  it('carteFocalisee sur une AUTRE carte : le tap ouvre quand meme la carte tapee', () => {
    const onCardClick = vi.fn()
    const onFermerCarte = vi.fn()
    const { container } = render(
      <PlateauPortrait
        world={monde}
        playerId={0}
        onCardClick={onCardClick}
        carteFocalisee={7}
        onFermerCarte={onFermerCarte}
        plateau={plateau(emplacement('main', unite('42', { id: '42', name: 'Quinjet', kind: 'event' })))}
      />
    )
    fireEvent.click(container.querySelector('.main-portrait .scan-card') as Element)
    expect(onCardClick).toHaveBeenCalledTimes(1)
    expect(onFermerCarte).not.toHaveBeenCalled()
  })

  describe('appui long sur une carte de la main : jouer directement', () => {
    afterEach(() => {
      vi.useRealTimers()
    })

    it('joue la carte via onSelect quand le moteur en pose un, sans passer par onCardClick', () => {
      vi.useFakeTimers()
      const onCardClick = vi.fn()
      const onSelect = vi.fn()
      const { container } = render(
        <PlateauPortrait
          world={monde}
          playerId={0}
          onCardClick={onCardClick}
          plateau={plateau(emplacement('main', unite('Quinjet', { name: 'Quinjet', kind: 'event', onSelect })))}
        />
      )
      const porteuse = container.querySelector('.main-portrait-carte') as Element
      fireEvent.pointerDown(porteuse)
      vi.advanceTimersByTime(APPUI_LONG_MS)
      expect(onSelect).toHaveBeenCalledTimes(1)
      expect(onCardClick).not.toHaveBeenCalled()
    })

    it('a defaut d onSelect, joue via onCardClick (meme repli que MainEventail/MainMedaillons)', () => {
      vi.useFakeTimers()
      const onCardClick = vi.fn()
      const { container } = render(
        <PlateauPortrait
          world={monde}
          playerId={0}
          onCardClick={onCardClick}
          plateau={plateau(emplacement('main', unite('Quinjet', { name: 'Quinjet', kind: 'event' })))}
        />
      )
      const porteuse = container.querySelector('.main-portrait-carte') as Element
      fireEvent.pointerDown(porteuse)
      vi.advanceTimersByTime(APPUI_LONG_MS)
      expect(onCardClick).toHaveBeenCalledTimes(1)
      expect(onCardClick.mock.calls[0]?.[0]).toMatchObject({ id: 'Quinjet' })
    })
  })

  it('une demande du moteur (props.bas) fait basculer la barre : elle seule s affiche, pas les outils', () => {
    // BarreBas.tsx:25 — quand `demande` est fourni, elle remplace tout le
    // reste plutot que de s'y ajouter. Un test qui verifierait juste que
    // `bas` apparait, sans verifier que les outils disparaissent, passerait
    // meme si `demande`/`outils`/`onglets` etaient intervertis.
    render(
      <PlateauPortrait
        world={monde}
        playerId={0}
        bas={<span>Choisis une cible</span>}
        actionsPartie={<button type="button">Annuler</button>}
        outils={<button type="button">Vue</button>}
        plateau={plateau()}
      />
    )
    expect(screen.getByText('Choisis une cible')).toBeInTheDocument()
    expect(screen.queryByText('Annuler')).toBeNull()
    expect(screen.queryByText('Vue')).toBeNull()
  })

  it('sans demande, chaque prop atteint la bonne case de BarreBas (pas juste presente n importe ou)', () => {
    // getByText('Annuler')/getByText('Vue') passerait meme si `actionsPartie`
    // et `outils` etaient permutes en entrant dans BarreBas (les deux se
    // rendent, juste dans le mauvais conteneur) : on verifie donc la case
    // precise (BarreBas.tsx : outils -> .pm-outils, onglets -> .pm-onglets).
    const { container } = render(
      <PlateauPortrait
        world={monde}
        playerId={0}
        actionsPartie={<button type="button">Annuler</button>}
        outils={<button type="button">Vue</button>}
        plateau={plateau()}
      />
    )
    expect(container.querySelector('.pm-outils')).toHaveTextContent('Annuler')
    expect(container.querySelector('.pm-onglets')).toHaveTextContent('Vue')
  })
})
