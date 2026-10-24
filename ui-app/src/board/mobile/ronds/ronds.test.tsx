// Les RONDS (24/10/2026) : la repartition en trois rangees, ce que dit un rond, les etats en initiales, le choix de
// plateau a chaque debut de partie.
import { act, fireEvent, render, renderHook, screen } from '@testing-library/react'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import type { ScanCardProps } from '../../../components/ScanCard'
import type { UniteAffichee } from '../../zones'
import type { BandesPortrait } from '../bandes-portrait'
import { ChoixPlateau, CLE_CHOIX_PLATEAU, useChoixPlateau } from './ChoixPlateau'
import { Rond, apparenceDe, urlDuJeton, type DecorRonds } from './Rond'
import { TableRonds } from './TableRonds'
import { SEUIL_INITIALES, etatsDe, initialesDe } from './etats-ronds'
import { repartirEnRonds, type TitresRonds } from './repartir-ronds'

const carte = (id: string, kind: ScanCardProps['kind'], reste: Partial<ScanCardProps> = {}): ScanCardProps => ({
  id,
  name: `Carte ${id}`,
  kind,
  imageUrl: `/scan/${id}.jpg`,
  ...reste,
})
const unite = (id: string, kind: ScanCardProps['kind'], reste: Partial<ScanCardProps> = {}, attachees: ScanCardProps[] = []): UniteAffichee => ({
  cle: `u-${id}`,
  carte: carte(id, kind, reste),
  attachees,
})
const vide = { unites: [] }
const bandes = (reste: Partial<BandesPortrait> = {}): BandesPortrait => ({
  vilain: vide,
  manigances: vide,
  engages: vide,
  heros: vide,
  soutiens: vide,
  ameliorations: vide,
  main: [],
  piles: [],
  ...reste,
})
const titres: TitresRonds = { vilain: 'V', manigances: 'M', allies: 'A', sbires: 'S', heros: 'H', enJeu: 'J' }
const decor = (reste: Partial<DecorRonds> = {}): DecorRonds => ({
  interactifs: new Map(),
  effets: new Map(),
  ouvrirPile: vi.fn(),
  ouvrirCarte: vi.fn(),
  agir: vi.fn(),
  ...reste,
})

beforeEach(() => {
  window.sessionStorage.clear()
  window.localStorage.clear()
})

describe('la repartition en ronds', () => {
  it('range le mechant, les manigances, les allies, les sbires, le heros et les cartes en jeu en trois rangees', () => {
    const rangees = repartirEnRonds(
      bandes({
        vilain: { epinglee: unite('rhino', 'villain'), unites: [unite('usine', 'environment')] },
        manigances: { epinglee: unite('effraction', 'main-scheme'), unites: [unite('annexe', 'side-scheme')] },
        engages: { unites: [unite('shocker', 'minion')] },
        heros: { epinglee: unite('spidey', 'hero'), unites: [unite('daredevil', 'ally')] },
        soutiens: { unites: [unite('heli', 'support')] },
        ameliorations: { unites: [unite('toile', 'upgrade')] },
      }),
      titres
    )
    expect(rangees.map((r) => [r.gauche.cle, r.droite.cle])).toEqual([
      ['vilain', 'manigances'],
      ['allies', 'sbires'],
      ['heros', 'enJeu'],
    ])
    expect(rangees[0].gauche.unites.map((u) => u.carte.id)).toEqual(['rhino'])
    // L'environnement quitte la zone du mechant : il rejoint les manigances.
    expect(rangees[0].droite.unites.map((u) => u.carte.id)).toEqual(['effraction', 'annexe', 'usine'])
    expect(rangees[1].gauche.unites.map((u) => u.carte.id)).toEqual(['daredevil'])
    expect(rangees[1].droite.unites.map((u) => u.carte.id)).toEqual(['shocker'])
    expect(rangees[2].gauche.unites.map((u) => u.carte.id)).toEqual(['spidey'])
    expect(rangees[2].droite.unites.map((u) => u.carte.id)).toEqual(['heli', 'toile'])
  })

  it('une table vide donne trois rangees de zones vides, sans planter', () => {
    const rangees = repartirEnRonds(bandes(), titres)
    expect(rangees).toHaveLength(3)
    expect(rangees.flatMap((r) => [r.gauche, r.droite]).every((z) => z.unites.length === 0)).toBe(true)
  })
})

describe('ce que dit un rond', () => {
  it('PV : anneau vert pour un allie, rouge pour un sbire de la rencontre, avec la part restante', () => {
    const allie = apparenceDe(carte('a', 'ally', { allyHp: '3/4', jauge: { remplissage: 0.75, genre: 'pv', alarme: false, texte: '3 / 4' } }))
    expect(allie).toMatchObject({ texte: '3 / 4', part: 0.75, couleur: '#3d9b57' })
    const sbire = apparenceDe(carte('s', 'minion', { camp: 'encounter', allyHp: '2/3', jauge: { remplissage: 0.66, genre: 'pv', alarme: false } }))
    expect(sbire.couleur).toBe('#c4453c')
    expect(sbire.texte).toBe('2/3')
  })

  it('le mechant a l\'anneau vert (ses PV), ses sbires l\'ont rouge', () => {
    const mechant = apparenceDe(carte('v', 'villain', { camp: 'encounter', jauge: { remplissage: 1, genre: 'pv', alarme: false, texte: '14 / 14' } }))
    expect(mechant.couleur).toBe('#3d9b57')
  })

  it('menace : anneau orange et pastille « 3/7 »', () => {
    const menace = apparenceDe(carte('m', 'main-scheme', { schemeThreat: '3/7', jauge: { remplissage: 0.43, genre: 'menace', alarme: false } }))
    expect(menace).toMatchObject({ texte: '3/7', couleur: '#d9822b' })
  })

  it('un environnement a l\'anneau violet', () => {
    expect(apparenceDe(carte('e', 'environment')).couleur).toBe('#8a6bd1')
  })

  it('un soutien sans PV a un anneau gris et pas de pastille', () => {
    expect(apparenceDe(carte('s', 'support'))).toMatchObject({ texte: undefined, couleur: '#6a7280' })
  })
})

describe('les jetons montrent l\'illustration anglaise (sans filigrane)', () => {
  it('retire le prefixe fr_ du scan, laisse le reste tel quel', () => {
    expect(urlDuJeton('/scan/fr_01095.jpg')).toBe('/vignette/01095.jpg')
    expect(urlDuJeton('/vignette/fr_01095')).toBe('/vignette/01095')
    expect(urlDuJeton('/scan/01095.jpg')).toBe('/vignette/01095.jpg')
    expect(urlDuJeton('data:image/png;base64,AAA')).toBe('data:image/png;base64,AAA')
  })

  it('le rond s\'habille de l\'anglais, ses ameliorations aussi', () => {
    const u = unite('x', 'ally', { imageUrl: '/scan/fr_01058.jpg' }, [carte('t', 'upgrade', { imageUrl: '/scan/fr_01008.jpg' })])
    const { container } = render(<Rond unite={u} zone="allies" decor={decor()} />)
    expect((container.querySelector('.rond-art') as HTMLElement).style.backgroundImage).toContain('/vignette/01058')
    expect((container.querySelector('.rond-mini') as HTMLElement).style.backgroundImage).toContain('/vignette/01008')
  })
})

describe('les etats', () => {
  it('prennent la couleur de leur carte de statut', () => {
    const etats = etatsDe([
      carte('1', 'status', { name: 'Sonné' }),
      carte('2', 'status', { name: 'Désorienté' }),
      carte('3', 'status', { name: 'Tenace' }),
      carte('4', 'status', { name: 'Hébété' }),
      carte('5', 'status', { name: 'Intensifié' }),
      carte('6', 'upgrade', { name: 'Lance-toile' }),
    ])
    expect(etats.map((e) => e.fond)).toEqual(['#8fcf3a', '#7a3a82', '#ef8b18', '#9a2624', '#f4a7c2'])
  })

  it('initiales : deux lettres, majuscule puis minuscule', () => {
    expect(initialesDe('Sonné')).toBe('So')
    expect(initialesDe('désorienté')).toBe('Dé')
    expect(initialesDe('')).toBe('?')
  })

  it('un rond montre les noms jusqu\'a deux etats, les initiales au-dela', () => {
    const deux = unite('x', 'ally', {}, [carte('1', 'status', { name: 'Sonné' }), carte('2', 'status', { name: 'Tenace' })])
    const { container, rerender } = render(<Rond unite={deux} zone="allies" decor={decor()} />)
    expect([...container.querySelectorAll('.rond-etats i')].map((e) => e.textContent)).toEqual(['Sonné', 'Tenace'])
    const trois = unite('x', 'ally', {}, [carte('1', 'status', { name: 'Sonné' }), carte('2', 'status', { name: 'Tenace' }), carte('3', 'status', { name: 'Hébété' })])
    expect(SEUIL_INITIALES).toBe(2)
    rerender(<Rond unite={trois} zone="allies" decor={decor()} />)
    expect([...container.querySelectorAll('.rond-etats i')].map((e) => e.textContent)).toEqual(['So', 'Te', 'Hé'])
  })
})

describe('le rond', () => {
  it('montre le nom, la pastille de PV, les valeurs du moteur et grise une carte epuisee', () => {
    const u = unite('dd', 'ally', {
      name: 'Daredevil',
      allyHp: '3/4',
      jauge: { remplissage: 0.75, genre: 'pv', alarme: false, texte: '3 / 4' },
      exhausted: true,
      statsComplets: [
        { label: 'ATK', value: 3, base: 2 },
        { label: 'THW', value: 2, base: 2 },
        { label: 'DEF', value: 9, base: 9 },
      ],
    })
    const { container } = render(<Rond unite={u} zone="allies" decor={decor()} />)
    expect(screen.getByText('Daredevil')).toBeTruthy()
    expect(container.querySelector('.rond-pastille')?.textContent).toBe('3 / 4')
    expect(container.querySelector('.rond')?.classList.contains('est-epuise')).toBe(true)
    // Un allie ne montre que ATQ et CTR (la defense n'est pas la sienne a lire ici).
    expect(container.querySelector('.rond-stats')?.textContent).toBe('ATQ 3CTR 2')
    // Une valeur augmentee par une carte en jeu (3 au lieu de 2) est en vert.
    expect(container.querySelector('.stat-ATK')?.classList.contains('est-augmentee')).toBe(true)
    expect(container.querySelector('.stat-THW')?.classList.contains('est-augmentee')).toBe(false)
  })

  it('un toucher ouvre la feuille de la carte', () => {
    const d = decor()
    render(<Rond unite={unite('dd', 'ally', { name: 'Daredevil' })} zone="allies" decor={d} />)
    fireEvent.click(screen.getByRole('button', { name: /Daredevil/ }))
    expect(d.ouvrirCarte).toHaveBeenCalledTimes(1)
    expect(d.agir).not.toHaveBeenCalled()
  })

  it('un toucher CHOISIT la carte quand le moteur demande une cible', () => {
    const agir = vi.fn()
    const d = decor({ interactifs: new Map([[7, { role: 'cible', choisie: false, agir }]]) })
    render(<Rond unite={unite('7', 'minion', { name: 'Shocker' })} zone="sbires" decor={d} />)
    fireEvent.click(screen.getByRole('button', { name: /Shocker/ }))
    expect(d.agir).toHaveBeenCalledTimes(1)
    expect(d.ouvrirCarte).not.toHaveBeenCalled()
  })

  it('une manigance en paysage dont le scan est portrait est tournee d\'un quart de tour', () => {
    const u = unite('m', 'main-scheme', { isLandscape: true, scanIsPortrait: true })
    const { container } = render(<Rond unite={u} zone="manigances" decor={decor()} />)
    expect(container.querySelector('.rond-art-tourne img')).toBeTruthy()
  })

  it('une carte face cachee ne montre pas son illustration', () => {
    const { container } = render(<Rond unite={unite('f', 'minion', { facedown: true })} zone="sbires" decor={decor()} />)
    expect((container.querySelector('.rond-art') as HTMLElement).style.backgroundImage).toBe('')
  })

  it('les ameliorations attachees sont des ronds de la meme taille, decales sur le cote (le compte reserve la place)', () => {
    const u = unite('h', 'ally', {}, [carte('t', 'upgrade', { name: 'Lance-toile' }), carte('t2', 'upgrade', { name: 'Autre' })])
    const { container } = render(<Rond unite={u} zone="allies" decor={decor()} />)
    expect(container.querySelectorAll('.rond-mini')).toHaveLength(2)
    expect((container.querySelector('.rond') as HTMLElement).style.getPropertyValue('--nb-amelio')).toBe('2')
    expect((container.querySelectorAll('.rond-mini')[1] as HTMLElement).style.getPropertyValue('--rang')).toBe('1')
  })

  it('une carte prete (soutien, allie, amelioration, heros) a un anneau vert ; utilisee elle est grisee, sans anneau', () => {
    const { container, rerender } = render(<Rond unite={unite('s', 'support')} zone="enJeu" decor={decor()} />)
    expect(container.querySelector('.rond')?.classList.contains('est-prete')).toBe(true)
    rerender(<Rond unite={unite('s', 'support', { exhausted: true })} zone="enJeu" decor={decor()} />)
    expect(container.querySelector('.rond')?.classList.contains('est-prete')).toBe(false)
    expect(container.querySelector('.rond')?.classList.contains('est-epuise')).toBe(true)
    // Un sbire n'a pas d'anneau « pret » : il s'attaque, il ne s'utilise pas.
    rerender(<Rond unite={unite('m', 'minion')} zone="sbires" decor={decor()} />)
    expect(container.querySelector('.rond')?.classList.contains('est-prete')).toBe(false)
  })
})

describe('la table en ronds', () => {
  it('dessine un rond par carte, dans les six zones', () => {
    const { container } = render(
      <TableRonds
        decor={decor()}
        bandes={bandes({
          vilain: { epinglee: unite('rhino', 'villain'), unites: [] },
          manigances: { epinglee: unite('eff', 'main-scheme'), unites: [] },
          engages: { unites: [unite('shocker', 'minion'), unite('sable', 'minion')] },
          heros: { epinglee: unite('spidey', 'hero'), unites: [] },
        })}
      />
    )
    expect(container.querySelectorAll('.rond')).toHaveLength(5)
    expect(container.querySelectorAll('.ronds-zone')).toHaveLength(6)
    expect(container.querySelectorAll('.ronds-rangee')).toHaveLength(3)
  })
})

describe('le choix du plateau a chaque debut de partie', () => {
  it('on demande au round 1, tant qu\'on n\'a pas repondu', () => {
    const { result } = renderHook(() => useChoixPlateau(1, false))
    expect(result.current.demander).toBe(true)
    act(() => result.current.repondre('ronds'))
    expect(result.current.demander).toBe(false)
    expect(window.localStorage.getItem('marvel-tel-plateau')).toBe('ronds')
    expect(window.sessionStorage.getItem(CLE_CHOIX_PLATEAU)).toBe('1')
  })

  it('« garder ce choix » coche : la question ne revient plus, aux parties suivantes non plus', () => {
    const { result } = renderHook(() => useChoixPlateau(1, false))
    act(() => result.current.repondre('ronds', true))
    expect(window.localStorage.getItem('marvel-tel-plateau-memorise')).toBe('oui')
    window.sessionStorage.clear()
    expect(renderHook(() => useChoixPlateau(1, false)).result.current.demander).toBe(false)
  })

  it('sans « garder ce choix », la question se repose a chaque partie', () => {
    const { result } = renderHook(() => useChoixPlateau(1, false))
    act(() => result.current.repondre('cartes'))
    expect(window.localStorage.getItem('marvel-tel-plateau-memorise')).toBeNull()
    window.sessionStorage.clear()
    expect(renderHook(() => useChoixPlateau(1, false)).result.current.demander).toBe(true)
  })

  it('on ne redemande pas apres un rechargement en plein round 1', () => {
    window.sessionStorage.setItem(CLE_CHOIX_PLATEAU, '1')
    const { result } = renderHook(() => useChoixPlateau(1, false))
    expect(result.current.demander).toBe(false)
  })

  it('on redemande a la partie suivante : le marqueur tombe des le round 2', () => {
    window.sessionStorage.setItem(CLE_CHOIX_PLATEAU, '1')
    const { rerender } = renderHook(({ round }) => useChoixPlateau(round, false), { initialProps: { round: 1 } })
    rerender({ round: 2 })
    expect(window.sessionStorage.getItem(CLE_CHOIX_PLATEAU)).toBeNull()
    const suivante = renderHook(() => useChoixPlateau(1, false))
    expect(suivante.result.current.demander).toBe(true)
  })

  it('on ne demande jamais en vue d\'etat, ni sans partie, ni apres le round 1', () => {
    expect(renderHook(() => useChoixPlateau(1, true)).result.current.demander).toBe(false)
    expect(renderHook(() => useChoixPlateau(undefined, false)).result.current.demander).toBe(false)
    expect(renderHook(() => useChoixPlateau(3, false)).result.current.demander).toBe(false)
  })

  it('la fenetre propose les deux plateaux et pre-selectionne le dernier choix', () => {
    window.localStorage.setItem('marvel-tel-plateau', 'ronds')
    const repondre = vi.fn()
    render(<ChoixPlateau repondre={repondre} />)
    const boutons = screen.getAllByRole('button')
    expect(boutons).toHaveLength(2)
    expect(boutons[1].className).toContain('est-propose')
    fireEvent.click(boutons[0])
    expect(repondre).toHaveBeenCalledWith('cartes', false)
    fireEvent.click(screen.getByRole('checkbox'))
    fireEvent.click(boutons[1])
    expect(repondre).toHaveBeenLastCalledWith('ronds', true)
  })
})

describe('la main sous les zones', () => {
  it('affiche les cartes en rangee, le compte, et se replie par la fleche', async () => {
    const { MainSousLaTable } = await import('./MainSousLaTable')
    const replier = vi.fn()
    const { container } = render(
      <MainSousLaTable
        unites={[unite('1', 'event', { name: 'Pour la Justice' }), unite('2', 'support', { name: 'Héliporteur' })]}
        onOuvrir={vi.fn()}
        onJouer={vi.fn()}
        jouable={() => false}
        onReplier={replier}
      />
    )
    expect(container.querySelector('.main-dock')).toBeTruthy()
    expect(container.querySelector('.ronds-titre')?.textContent).toContain('2')
    fireEvent.click(screen.getByRole('button', { name: /Replier la main/ }))
    expect(replier).toHaveBeenCalledTimes(1)
  })

  it('une carte jouable se choisit au toucher, puis « Jouer » la joue', async () => {
    const { MainSousLaTable } = await import('./MainSousLaTable')
    const jouer = vi.fn()
    const u = unite('1', 'event', { name: 'Pour la Justice' })
    const { container } = render(
      <MainSousLaTable unites={[u]} onOuvrir={vi.fn()} onJouer={jouer} jouable={() => true} onReplier={vi.fn()} />
    )
    expect(screen.queryByText('Jouer')).toBeNull()
    fireEvent.click(container.querySelector('.main-portrait-carte .scan-card') as HTMLElement)
    fireEvent.click(screen.getByText('Jouer'))
    expect(jouer).toHaveBeenCalledTimes(1)
  })
})

describe('ROUND en grand', () => {
  it('ne s\'allume qu\'au passage a un round 2 ou plus, jamais au chargement ni au round 1', async () => {
    const { RoundEnGrand } = await import('./RoundEnGrand')
    const { container, rerender } = render(<RoundEnGrand round={undefined} />)
    rerender(<RoundEnGrand round={1} />)
    expect(container.querySelector('.round-en-grand')).toBeNull()
    rerender(<RoundEnGrand round={2} />)
    expect(container.querySelector('.round-en-grand')?.textContent).toContain('2')
  })
})

describe('un rond vaincu', () => {
  it('est grise, ecrit « VAINCU » et ne se touche plus', () => {
    const { container } = render(<Rond unite={unite('s', 'minion', { name: 'Shocker' })} zone="sbires" decor={decor()} vaincu />)
    expect(container.querySelector('.rond')?.classList.contains('rond-vaincu')).toBe(true)
    expect(container.querySelector('.rond-vaincu-etiquette')?.textContent).toBe('VAINCU')
    expect((container.querySelector('.rond-bouton') as HTMLButtonElement).disabled).toBe(true)
  })
})

describe('les etiquettes d\'un rond', () => {
  it('Garde sur un sbire gardien, Crise sur une manigance bloquante, +1 sur une ressource a depenser', () => {
    const garde = unite('g', 'minion', { keywords: [{ nom: 'Guard', definition: '' }] })
    const { container, rerender } = render(<Rond unite={garde} zone="sbires" decor={decor()} />)
    expect(container.querySelector('.rond-etiquette-garde')).toBeTruthy()
    rerender(<Rond unite={unite('c', 'main-scheme', { crise: 'Annexe' })} zone="manigances" decor={decor()} />)
    expect(container.querySelector('.rond-etiquette')?.textContent).toContain('Crise')
    rerender(
      <Rond unite={unite('5', 'support')} zone="enJeu" decor={decor({ interactifs: new Map([[5, { role: 'ressource', choisie: false }]]) })} />
    )
    expect(container.querySelector('.rond-etiquette-ressource')?.textContent).toBe('+1')
  })

  it('un degat ou une menace en cours s\'ecrit au-dessus du rond', () => {
    const u = unite('d', 'ally', { effectDelta: { kind: 'damage', value: 3 } })
    const { container } = render(<Rond unite={u} zone="allies" decor={decor()} />)
    expect(container.querySelector('.rond-delta')?.textContent).toBe('-3')
  })
})
