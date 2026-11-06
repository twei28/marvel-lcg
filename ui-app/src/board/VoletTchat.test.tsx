// @vitest-environment jsdom
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { act, cleanup, fireEvent, render, screen, waitFor, within } from '@testing-library/react'
import { VoletTchat } from './VoletTchat'
import type { TransportTchat, VueTchat } from './tchat'

afterEach(() => {
  cleanup()
  vi.useRealTimers()
})

beforeEach(() => {
  window.history.pushState({}, '', '/board.html')
})

const rien = () => {}

function transportSimule(partial: Partial<TransportTchat> = {}): TransportTchat {
  return {
    lire: vi.fn(async (): Promise<VueTchat> => ({ actif: false, messages: [], dernier: 0 })),
    dire: vi.fn(async () => true),
    ...partial,
  }
}

describe('VoletTchat — ouverture et fermeture', () => {
  it('ferme par defaut, aucun panneau dans le document', () => {
    render(<VoletTchat ouvert={false} ouvrir={rien} fermer={rien} transport={transportSimule()} />)
    expect(screen.queryByRole('dialog')).toBeNull()
  })

  it('un clic sur la languette fermee appelle ouvrir()', () => {
    const ouvrir = vi.fn()
    render(<VoletTchat ouvert={false} ouvrir={ouvrir} fermer={rien} transport={transportSimule()} />)
    fireEvent.click(screen.getByTitle('Ouvrir le tchat'))
    expect(ouvrir).toHaveBeenCalled()
  })

  it('Echap referme le volet ouvert', () => {
    const fermer = vi.fn()
    render(<VoletTchat ouvert fermer={fermer} ouvrir={rien} transport={transportSimule()} />)
    expect(screen.getByRole('dialog', { name: 'Tchat' })).toBeTruthy()
    fireEvent.keyDown(document, { key: 'Escape' })
    expect(fermer).toHaveBeenCalled()
  })
})

describe('VoletTchat — onglet Table', () => {
  it('absent sans tableId', () => {
    render(<VoletTchat ouvert ouvrir={rien} fermer={rien} transport={transportSimule()} />)
    expect(screen.queryByRole('button', { name: /^Table/ })).toBeNull()
  })

  it('absent en relecture meme avec tableId', () => {
    window.history.pushState({}, '', '/board.html?relecture')
    render(<VoletTchat ouvert ouvrir={rien} fermer={rien} tableId="t1" transport={transportSimule()} />)
    expect(screen.queryByRole('button', { name: /^Table/ })).toBeNull()
  })

  it('present pour un spectateur en direct avec tableId', () => {
    window.history.pushState({}, '', '/board.html?spectateur')
    render(<VoletTchat ouvert ouvrir={rien} fermer={rien} tableId="t1" spectateur transport={transportSimule()} />)
    expect(screen.getByRole('button', { name: /^Table/ })).toBeTruthy()
  })
})

describe('VoletTchat — messages et pastilles', () => {
  it('affiche les messages renvoyes par le transport, dedupliques par id', async () => {
    let appel = 0
    const transport = transportSimule({
      lire: vi.fn(async (): Promise<VueTchat> => {
        appel += 1
        return {
          actif: true,
          pseudo: 'moi',
          messages: [{ id: 1, pseudo: 'bob', texte: 'salut', quand: '21:30' }],
          dernier: appel === 1 ? 0 : 1,
        }
      }),
    })
    render(<VoletTchat ouvert ouvrir={rien} fermer={rien} transport={transport} />)
    await waitFor(() => expect(screen.getByText('salut')).toBeTruthy())
    // Le curseur ne bouge pas tant que `dernier` reste a 0 (meme message
    // represente) : un second rendu identique ne doit pas en ajouter un autre.
    await act(async () => {
      await Promise.resolve()
    })
    expect(screen.getAllByText('salut')).toHaveLength(1)
  })

  it('un message recu sur un autre onglet pose une pastille de non-lus', async () => {
    const transport = transportSimule({
      lire: vi.fn(async (fil): Promise<VueTchat> => {
        if (fil === 'table') {
          return { actif: true, messages: [{ id: 9, pseudo: 'bob', texte: 'coucou table', quand: '21:30' }], dernier: 9 }
        }
        return { actif: true, pseudo: 'moi', messages: [], dernier: 0 }
      }),
    })
    window.history.pushState({}, '', '/board.html')
    render(<VoletTchat ouvert ouvrir={rien} fermer={rien} tableId="t1" transport={transport} />)
    await waitFor(() => {
      const bouton = screen.getByRole('button', { name: /^Table/ })
      expect(bouton.textContent).toContain('1')
    })
  })
})

describe('VoletTchat — creer une table depuis le tchat', () => {
  function transportAvecMessageDeBob(): TransportTchat {
    return transportSimule({
      lire: vi.fn(async (): Promise<VueTchat> => ({
        actif: true,
        pseudo: 'moi',
        messages: [{ id: 1, pseudo: 'bob', texte: 'salut', quand: '21:30' }],
        dernier: 1,
      })),
    })
  }

  it('cliquer sur un pseudo (hors selection) ouvre un onglet MP avec cette personne', async () => {
    render(<VoletTchat ouvert ouvrir={rien} fermer={rien} transport={transportAvecMessageDeBob()} />)
    await waitFor(() => expect(screen.getByText('salut')).toBeTruthy())
    fireEvent.click(screen.getByRole('button', { name: 'bob' }))
    expect(screen.getByRole('button', { name: 'bob', hidden: false })).toHaveClass('est-actif')
  })

  it('le bouton Creer une table bascule en mode selection, ou cliquer un pseudo le choisit sans ouvrir de MP', async () => {
    render(<VoletTchat ouvert ouvrir={rien} fermer={rien} transport={transportAvecMessageDeBob()} />)
    await waitFor(() => expect(screen.getByText('salut')).toBeTruthy())
    fireEvent.click(screen.getByRole('button', { name: 'Créer une table' }))
    fireEvent.click(screen.getByRole('button', { name: 'bob' }))
    // Choisi pour l'invitation : pas d'onglet MP ouvert pour autant, mais compte dans Valider.
    expect(screen.queryByRole('button', { name: 'bob', hidden: false })).not.toHaveClass('est-actif')
    expect(screen.getByRole('button', { name: /^Valider/ }).textContent).toContain('(1)')
  })

  it('Valider redirige vers /prepare.html avec les pseudos choisis', async () => {
    render(<VoletTchat ouvert ouvrir={rien} fermer={rien} transport={transportAvecMessageDeBob()} />)
    await waitFor(() => expect(screen.getByText('salut')).toBeTruthy())
    fireEvent.click(screen.getByRole('button', { name: 'Créer une table' }))
    fireEvent.click(screen.getByRole('button', { name: 'bob' }))
    const original = window.location
    const remplacement = { ...original, href: '' }
    Object.defineProperty(window, 'location', { value: remplacement, writable: true })
    fireEvent.click(screen.getByRole('button', { name: /^Valider/ }))
    expect(window.location.href).toBe('/prepare.html?inviter=bob')
    Object.defineProperty(window, 'location', { value: original, writable: true })
  })
})

describe('VoletTchat — Général toujours en premier, jamais fermable', () => {
  beforeEach(() => {
    window.localStorage.clear()
  })

  it('reste le premier onglet et n\'a pas de croix, meme avec des conversations privees', async () => {
    window.history.pushState({}, '', '/board.html?spectateur')
    const transport = transportSimule({
      lire: vi.fn(async (): Promise<VueTchat> => ({
        actif: true,
        pseudo: 'moi',
        messages: [{ id: 1, pseudo: 'bob', texte: 'salut', quand: '21:30' }],
        dernier: 1,
        prives: { bob: 1, alice: 2 },
      })),
    })
    const { container } = render(<VoletTchat ouvert ouvrir={rien} fermer={rien} tableId="t1" spectateur transport={transport} />)
    const onglets = () => container.querySelector('.volet-tchat-onglets') as HTMLElement
    await waitFor(() => expect(within(onglets()).getByRole('button', { name: 'bob' })).toBeTruthy())
    const boutons = within(onglets()).getAllByRole('button')
    expect(boutons[0].textContent).toContain('Général')
    const boutonGeneral = within(onglets()).getByRole('button', { name: /^Général/ })
    // Général n'est jamais enveloppe dans `.volet-tchat-onglet-mp` (la paire
    // nom+croix des conversations privees) : pas de croix a cote de lui.
    expect(boutonGeneral.parentElement?.className).not.toContain('volet-tchat-onglet-mp')
    expect(within(onglets()).getAllByTitle('Fermer cette conversation')).toHaveLength(2)
  })
})

describe('VoletTchat — fermer une conversation privee', () => {
  beforeEach(() => {
    window.localStorage.clear()
  })

  function transportAvecPrive(): TransportTchat {
    return transportSimule({
      lire: vi.fn(async (): Promise<VueTchat> => ({
        actif: true,
        pseudo: 'moi',
        messages: [{ id: 1, pseudo: 'bob', texte: 'salut', quand: '21:30' }],
        dernier: 1,
        prives: { bob: 1 },
      })),
    })
  }

  it('la croix ferme l\'onglet MP et revient au fil Général', async () => {
    const { container } = render(<VoletTchat ouvert ouvrir={rien} fermer={rien} transport={transportAvecPrive()} />)
    const onglets = () => container.querySelector('.volet-tchat-onglets') as HTMLElement
    await waitFor(() => expect(within(onglets()).getByRole('button', { name: 'bob' })).toBeTruthy())
    fireEvent.click(within(onglets()).getByRole('button', { name: 'bob' }))
    expect(within(onglets()).getByRole('button', { name: 'bob', hidden: false })).toHaveClass('est-actif')
    fireEvent.click(screen.getByTitle('Fermer cette conversation'))
    expect(within(onglets()).queryByRole('button', { name: 'bob' })).toBeNull()
    expect(within(onglets()).getByRole('button', { name: 'Général' })).toHaveClass('est-actif')
  })

  it('reste fermee apres un remontage tant qu\'aucun nouveau message n\'arrive', async () => {
    const transport = transportAvecPrive()
    const { container, unmount } = render(<VoletTchat ouvert ouvrir={rien} fermer={rien} transport={transport} />)
    const onglets = () => container.querySelector('.volet-tchat-onglets') as HTMLElement
    await waitFor(() => expect(within(onglets()).getByRole('button', { name: 'bob' })).toBeTruthy())
    fireEvent.click(within(onglets()).getByRole('button', { name: 'bob' }))
    fireEvent.click(screen.getByTitle('Fermer cette conversation'))
    unmount()
    const { container: container2 } = render(<VoletTchat ouvert ouvrir={rien} fermer={rien} transport={transportAvecPrive()} />)
    await waitFor(() => expect(screen.getByText('salut')).toBeTruthy())
    expect(container2.querySelector('.volet-tchat-onglets')?.textContent).not.toContain('bob')
  })

  it('reapparait quand un message plus recent arrive', async () => {
    window.localStorage.setItem('marvel-tchat-fermees', JSON.stringify({ bob: 1 }))
    const transport = transportSimule({
      lire: vi.fn(async (): Promise<VueTchat> => ({
        actif: true,
        pseudo: 'moi',
        messages: [],
        dernier: 0,
        prives: { bob: 2 },
      })),
    })
    render(<VoletTchat ouvert ouvrir={rien} fermer={rien} transport={transport} />)
    await waitFor(() => expect(screen.getByRole('button', { name: 'bob' })).toBeTruthy())
  })
})

describe('VoletTchat — pseudo Play (formulaire, pas window.prompt)', () => {
  it('affiche le formulaire tant que pseudoPlay.valeur est vide, rien d’autre', () => {
    render(
      <VoletTchat ouvert ouvrir={rien} fermer={rien} transport={transportSimule()} pseudoPlay={{ valeur: '', definir: vi.fn() }} />
    )
    expect(screen.getByText('Choisis un pseudo pour le tchat (visible des autres joueurs) :')).toBeTruthy()
    expect(screen.queryByPlaceholderText('Écrire un message…')).toBeNull()
    expect(screen.queryByRole('button', { name: 'Créer une table' })).toBeNull()
  })

  it('le bouton Rejoindre est desactive tant que le champ est vide', () => {
    render(
      <VoletTchat ouvert ouvrir={rien} fermer={rien} transport={transportSimule()} pseudoPlay={{ valeur: '', definir: vi.fn() }} />
    )
    expect(screen.getByRole('button', { name: 'Rejoindre' })).toBeDisabled()
  })

  it('valider le formulaire appelle definir() avec le pseudo nettoye', () => {
    const definir = vi.fn()
    render(
      <VoletTchat ouvert ouvrir={rien} fermer={rien} transport={transportSimule()} pseudoPlay={{ valeur: '', definir }} />
    )
    fireEvent.change(screen.getByPlaceholderText('Pseudo…'), { target: { value: '  zellichon  ' } })
    fireEvent.click(screen.getByRole('button', { name: 'Rejoindre' }))
    expect(definir).toHaveBeenCalledWith('zellichon')
  })

  it('une fois pseudoPlay.valeur rempli, le formulaire disparait et le fil normal s’affiche', () => {
    render(
      <VoletTchat ouvert ouvrir={rien} fermer={rien} transport={transportSimule()} pseudoPlay={{ valeur: 'zellichon', definir: vi.fn() }} />
    )
    expect(screen.queryByText('Choisis un pseudo pour le tchat (visible des autres joueurs) :')).toBeNull()
    expect(screen.getByPlaceholderText('Écrire un message…')).toBeTruthy()
  })

  it('sans pseudoPlay (plateau normal), le formulaire n’apparait jamais', () => {
    render(<VoletTchat ouvert ouvrir={rien} fermer={rien} transport={transportSimule()} />)
    expect(screen.queryByText('Choisis un pseudo pour le tchat (visible des autres joueurs) :')).toBeNull()
  })
})

describe('VoletTchat — envoi', () => {
  it('envoie le brouillon via le transport et vide le champ', async () => {
    const dire = vi.fn(async () => true)
    const transport = transportSimule({ dire })
    render(<VoletTchat ouvert ouvrir={rien} fermer={rien} transport={transport} />)
    const champ = screen.getByPlaceholderText('Écrire un message…') as HTMLInputElement
    fireEvent.change(champ, { target: { value: 'bonjour' } })
    fireEvent.click(screen.getByText('Envoyer'))
    await waitFor(() => expect(dire).toHaveBeenCalledWith('general', 'bonjour', '', ''))
    expect(champ.value).toBe('')
  })
})

describe('VoletTchat — drapeaux de langues', () => {
  beforeEach(() => {
    window.localStorage.clear()
  })

  it('cocher une langue l\'envoie avec le message suivant', async () => {
    const dire = vi.fn(async () => true)
    const transport = transportSimule({ dire })
    render(<VoletTchat ouvert ouvrir={rien} fermer={rien} transport={transport} />)
    fireEvent.click(screen.getByTitle('Langues parlées'))
    fireEvent.click(screen.getByText('🇫🇷 fr'))
    const champ = screen.getByPlaceholderText('Écrire un message…') as HTMLInputElement
    fireEvent.change(champ, { target: { value: 'bonjour' } })
    fireEvent.click(screen.getByText('Envoyer'))
    await waitFor(() => expect(dire).toHaveBeenCalledWith('general', 'bonjour', '', 'fr'))
  })

  it('le choix survit a un remontage (localStorage)', () => {
    const transport = transportSimule()
    const { unmount } = render(<VoletTchat ouvert ouvrir={rien} fermer={rien} transport={transport} />)
    fireEvent.click(screen.getByTitle('Langues parlées'))
    fireEvent.click(screen.getByText('🇬🇧 en'))
    unmount()
    render(<VoletTchat ouvert ouvrir={rien} fermer={rien} transport={transportSimule()} />)
    expect(screen.getByTitle('Langues parlées').textContent).toBe('🇬🇧')
  })

  it('affiche les drapeaux d\'un message a cote du pseudo', async () => {
    const lire = vi.fn(async (): Promise<VueTchat> => ({
      actif: true,
      pseudo: 'moi',
      messages: [{ id: 1, pseudo: 'bob', texte: 'salut', quand: '10:00', langues: 'fr,en' }],
      dernier: 1,
    }))
    render(<VoletTchat ouvert ouvrir={rien} fermer={rien} transport={transportSimule({ lire })} />)
    await waitFor(() => expect(screen.getByText('🇫🇷🇬🇧')).toBeTruthy())
  })
})
