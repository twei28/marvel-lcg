// clavier-wiring.test.tsx — le branchement du clavier, dans `useTriche`.
//
// `interpreterTouche` (clavier.test.ts) est pure et ne prouve que
// l'interprétation. Ici on prouve le CÂBLAGE : une touche pressée alors qu'on
// survole une carte réelle du DOM part bien vers le moteur — et, point de
// vigilance du brief, qu'elle ne morde pas pendant une saisie de texte.
//
// Harnais calqué sur `CoucheTriche.test.tsx` : `useTriche` a besoin d'un
// monde complet, construit ici avec `plateau-de-test.ts` comme
// `fixture-monde.ts` le fait déjà pour ce dossier.
import { act, fireEvent, render } from '@testing-library/react'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { CoucheTriche, useTriche } from '../CoucheTriche'
import { carteSurTable, siege, tableAvec } from '../plateau-de-test'
import type { World } from '../world'

const VILAIN = carteSurTable(7, '01001a', 'EncounterVillain', 'Rhino')
const MANIGANCE = carteSurTable(9, '01002a', 'MainScheme', 'Crisis')
const SANS_JETON = carteSurTable(4, '01003a', 'Event', 'Coup de circonstance')
// Dessus des deux piles du cas « piocher » (voir plus bas) : une du joueur,
// une du monde. Chacune devient la REPRÉSENTANTE de sa pile (`pilesParDessus`).
const DESSUS_DECK_JOUEUR = carteSurTable(20, '01004a', 'PlayerSideScheme', 'Dessus du deck joueur')
const DESSUS_DECK_RENCONTRE = carteSurTable(21, '01005a', 'EncounterVillain', 'Dessus du deck Rencontre')

function mondeManuel(): World {
  // ⚠ `SANS_JETON` va dans `allies`, PAS dans une pile (deck/défausse) : le
  // dessus d'une pile en devient le REPRÉSENTANT (voir `pilesParDessus`), donc
  // y placer la seule carte de la pile en ferait aussi une cible de pile, ce
  // qui n'est pas ce que ce cas veut prouver.
  return tableAvec(
    siege({ allies: [SANS_JETON], player_deck: [DESSUS_DECK_JOUEUR] }),
    {
      mode_manuel: true,
      villains: [VILAIN],
      area_schemes_main: [MANIGANCE],
      encounter_deck: [DESSUS_DECK_RENCONTRE],
    } as never
  )
}

type Capture = { estToucheEnfoncee?: (cle: string) => boolean }

function Harness({ world, capture }: { world: World; capture: Capture }) {
  const triche = useTriche(world, 0)
  capture.estToucheEnfoncee = triche.estToucheEnfoncee
  return <CoucheTriche actif={triche.actif} manuel={triche.manuel} couche={triche.couche} />
}

/** Pose un noeud portant `data-card-id`, hors du plateau, et le survole. */
function survoler(id: number): HTMLElement {
  const noeud = document.createElement('div')
  noeud.setAttribute('data-card-id', String(id))
  document.body.appendChild(noeud)
  fireEvent.pointerMove(noeud)
  return noeud
}

beforeEach(() => {
  vi.stubGlobal('fetch', vi.fn(async () => ({ ok: true }) as Response))
})

describe('le clavier du mode manuel parle au moteur', () => {
  it('F retourne la carte survolee', async () => {
    render(<Harness world={mondeManuel()} capture={{}} />)
    survoler(7)
    fireEvent.keyDown(document, { key: 'f' })
    await act(async () => { await Promise.resolve() })
    expect(fetch).toHaveBeenCalledWith('/sandbox_command', expect.objectContaining({
      body: JSON.stringify({ commands: ['Puzzle.Flip(7)'] }),
    }))
  })

  it('un chiffre sur une manigance pose de la menace', async () => {
    render(<Harness world={mondeManuel()} capture={{}} />)
    survoler(9)
    fireEvent.keyDown(document, { key: '3' })
    await act(async () => { await Promise.resolve() })
    expect(fetch).toHaveBeenCalledWith('/sandbox_command', expect.objectContaining({
      body: JSON.stringify({ commands: ["Puzzle.PlaceThreat(9, 3)"] }),
    }))
  })

  it('Maj plus chiffre sur un personnage soigne au lieu de blesser', async () => {
    render(<Harness world={mondeManuel()} capture={{}} />)
    survoler(7)
    fireEvent.keyDown(document, { key: '3', shiftKey: true })
    await act(async () => { await Promise.resolve() })
    expect(fetch).toHaveBeenCalledWith('/sandbox_command', expect.objectContaining({
      body: JSON.stringify({ commands: ['Puzzle.Heal(7, 3)'] }),
    }))
  })

  it('sur une pile du JOUEUR, un chiffre pioche en main', async () => {
    render(<Harness world={mondeManuel()} capture={{}} />)
    survoler(20)
    fireEvent.keyDown(document, { key: '1' })
    await act(async () => { await Promise.resolve() })
    expect(fetch).toHaveBeenCalledWith('/sandbox_command', expect.objectContaining({
      body: JSON.stringify({ commands: ['Puzzle.Gain(20)'] }),
    }))
  })

  // LE CAS QUI COMPTE LE PLUS (retour de revue, 19/09/2026) : une carte
  // Rencontre ne va JAMAIS en main, elle se révèle et se résout. Sur une pile
  // du MONDE, le même chiffre doit sortir la carte vers la zone de
  // résolution — visible sur la table — et surtout PAS l'envoyer en main.
  it('sur une pile du MONDE (Rencontre), un chiffre sort en resolution — jamais en main', async () => {
    render(<Harness world={mondeManuel()} capture={{}} />)
    survoler(21)
    fireEvent.keyDown(document, { key: '1' })
    await act(async () => { await Promise.resolve() })
    expect(fetch).toHaveBeenCalledWith('/sandbox_command', expect.objectContaining({
      body: JSON.stringify({ commands: ["Puzzle.MoveTo(21, 'ProcessingArea', 'Top')"] }),
    }))
    expect(fetch).not.toHaveBeenCalledWith('/sandbox_command', expect.objectContaining({
      body: JSON.stringify({ commands: ['Puzzle.Gain(21)'] }),
    }))
    expect(fetch).not.toHaveBeenCalledWith('/sandbox_command', expect.objectContaining({
      body: JSON.stringify({ commands: ["Puzzle.MoveTo(21, 'HandsArea', 'Top')"] }),
    }))
  })

  it('un chiffre nu, sans modificateur, pose des degats (cas de base)', async () => {
    render(<Harness world={mondeManuel()} capture={{}} />)
    survoler(7)
    fireEvent.keyDown(document, { key: '3' })
    await act(async () => { await Promise.resolve() })
    expect(fetch).toHaveBeenCalledWith('/sandbox_command', expect.objectContaining({
      body: JSON.stringify({ commands: ['Puzzle.Damage(7, 3)'] }),
    }))
  })

  it('Q incline la carte survolee', async () => {
    render(<Harness world={mondeManuel()} capture={{}} />)
    survoler(7)
    fireEvent.keyDown(document, { key: 'q' })
    await act(async () => { await Promise.resolve() })
    expect(fetch).toHaveBeenCalledWith('/sandbox_command', expect.objectContaining({
      body: JSON.stringify({ commands: ['Puzzle.Exhaust(7)'] }),
    }))
  })

  it('R melange la pile survolee', async () => {
    render(<Harness world={mondeManuel()} capture={{}} />)
    survoler(20)
    fireEvent.keyDown(document, { key: 'r' })
    await act(async () => { await Promise.resolve() })
    expect(fetch).toHaveBeenCalledWith('/sandbox_command', expect.objectContaining({
      body: JSON.stringify({ commands: ["Puzzle.Shuffle('PlayerDeck')"] }),
    }))
  })

  // LE CRITIQUE (retour de revue, 19/09/2026) : Ctrl/Cmd/Alt sont les
  // raccourcis du NAVIGATEUR (Ctrl+F cherche, Ctrl+R recharge, Ctrl+1..9
  // change d'onglet). Sans garde, survoler une carte pendant Ctrl+F la
  // retournait — irreversible sur une carte face cachee. Le temoin qui
  // compte est le REFUS : ni geste, ni `preventDefault` (le retour de
  // `fireEvent.keyDown` est `true` quand l'evenement n'a PAS ete annule).
  it('Ctrl+chiffre ne pose rien, et laisse le raccourci du navigateur agir', async () => {
    render(<Harness world={mondeManuel()} capture={{}} />)
    survoler(7)
    const nonAnnule = fireEvent.keyDown(document, { key: '3', ctrlKey: true })
    await act(async () => { await Promise.resolve() })
    expect(fetch).not.toHaveBeenCalled()
    expect(nonAnnule).toBe(true)
  })

  it('Ctrl+F ne retourne rien, et laisse la recherche du navigateur s’ouvrir', async () => {
    render(<Harness world={mondeManuel()} capture={{}} />)
    survoler(7)
    const nonAnnule = fireEvent.keyDown(document, { key: 'f', ctrlKey: true })
    await act(async () => { await Promise.resolve() })
    expect(fetch).not.toHaveBeenCalled()
    expect(nonAnnule).toBe(true)
  })

  it('Cmd+F (Mac) ne retourne rien non plus', async () => {
    render(<Harness world={mondeManuel()} capture={{}} />)
    survoler(7)
    const nonAnnule = fireEvent.keyDown(document, { key: 'f', metaKey: true })
    await act(async () => { await Promise.resolve() })
    expect(fetch).not.toHaveBeenCalled()
    expect(nonAnnule).toBe(true)
  })

  // Alt sert DEJA a l'apercu immediat (Board.tsx) : une raison de plus pour
  // qu'il ne declenche aucun geste de jeu ici.
  it('Alt+chiffre ne pose rien : Alt sert deja a l’apercu immediat', async () => {
    render(<Harness world={mondeManuel()} capture={{}} />)
    survoler(7)
    const nonAnnule = fireEvent.keyDown(document, { key: '3', altKey: true })
    await act(async () => { await Promise.resolve() })
    expect(fetch).not.toHaveBeenCalled()
    expect(nonAnnule).toBe(true)
  })

  it('ne devine pas le jeton d’une carte qui n’en a pas', async () => {
    render(<Harness world={mondeManuel()} capture={{}} />)
    survoler(4)
    fireEvent.keyDown(document, { key: '3' })
    await act(async () => { await Promise.resolve() })
    expect(fetch).not.toHaveBeenCalled()
  })

  it('ne mord pas quand rien n’est survole', async () => {
    render(<Harness world={mondeManuel()} capture={{}} />)
    fireEvent.keyDown(document, { key: 'f' })
    await act(async () => { await Promise.resolve() })
    expect(fetch).not.toHaveBeenCalled()
  })

  it('ne mord pas hors du mode manuel', async () => {
    const monde = { ...mondeManuel(), mode_manuel: false, mode_sandbox: true } as World
    render(<Harness world={monde} capture={{}} />)
    survoler(7)
    fireEvent.keyDown(document, { key: 'f' })
    await act(async () => { await Promise.resolve() })
    expect(fetch).not.toHaveBeenCalled()
  })

  it('ne mord pas pendant une saisie de texte', async () => {
    const { container } = render(
      <>
        <Harness world={mondeManuel()} capture={{}} />
        <input aria-label="champ" />
      </>
    )
    survoler(7)
    const champ = container.querySelector('input') as HTMLInputElement
    champ.focus()
    fireEvent.keyDown(champ, { key: 'f' })
    await act(async () => { await Promise.resolve() })
    expect(fetch).not.toHaveBeenCalled()
  })
})

// --- Ctrl+Z : annule le dernier geste (tache 6) ----------------------------
//
// Un cas particulier de la garde des modificateurs testee juste au-dessus :
// Ctrl+Z DOIT etre traite explicitement AVANT elle (sinon elle l'avale, comme
// tout Ctrl+lettre), mais la garde du FOCUS reste prioritaire sur Ctrl+Z
// (dans un champ de texte, c'est l'annulation de saisie du joueur, pas la
// notre).
describe('Ctrl+Z annule le dernier geste', () => {
  it('poste sur /manuel_undo et empeche le navigateur d’annuler', async () => {
    render(<Harness world={mondeManuel()} capture={{}} />)
    const nonAnnule = fireEvent.keyDown(document, { key: 'z', ctrlKey: true })
    await act(async () => { await Promise.resolve() })
    expect(fetch).toHaveBeenCalledWith('/manuel_undo', { method: 'POST' })
    // `preventDefault` a bien ete appele : on remplace VOLONTAIREMENT
    // l'annulation du navigateur, qui n'a aucun sens sur un plateau de jeu.
    expect(nonAnnule).toBe(false)
  })

  it('ne mord pas pendant une saisie de texte : c’est l’annulation du champ, pas la notre', async () => {
    const { container } = render(
      <>
        <Harness world={mondeManuel()} capture={{}} />
        <input aria-label="champ" />
      </>
    )
    const champ = container.querySelector('input') as HTMLInputElement
    champ.focus()
    const nonAnnule = fireEvent.keyDown(champ, { key: 'z', ctrlKey: true })
    await act(async () => { await Promise.resolve() })
    expect(fetch).not.toHaveBeenCalled()
    expect(nonAnnule).toBe(true)
  })

  it('ne mord pas hors du mode manuel', async () => {
    const monde = { ...mondeManuel(), mode_manuel: false, mode_sandbox: true } as World
    render(<Harness world={monde} capture={{}} />)
    fireEvent.keyDown(document, { key: 'z', ctrlKey: true })
    await act(async () => { await Promise.resolve() })
    expect(fetch).not.toHaveBeenCalled()
  })

  it('empeche deux annulations en vol en meme temps', async () => {
    let resoudre: (reponse: Response) => void = () => {}
    vi.stubGlobal(
      'fetch',
      vi.fn(() => new Promise<Response>((resolve) => { resoudre = resolve }))
    )
    render(<Harness world={mondeManuel()} capture={{}} />)

    fireEvent.keyDown(document, { key: 'z', ctrlKey: true })
    await act(async () => { await Promise.resolve() })
    expect(fetch).toHaveBeenCalledTimes(1)

    // La premiere annulation est encore en vol : une seconde pression ne doit
    // pas partir en meme temps qu'elle.
    fireEvent.keyDown(document, { key: 'z', ctrlKey: true })
    await act(async () => { await Promise.resolve() })
    expect(fetch).toHaveBeenCalledTimes(1)

    await act(async () => {
      resoudre({ ok: true } as Response)
      await Promise.resolve()
      await Promise.resolve()
    })

    // Une fois la premiere terminee, une nouvelle pression repart normalement.
    fireEvent.keyDown(document, { key: 'z', ctrlKey: true })
    await act(async () => { await Promise.resolve() })
    expect(fetch).toHaveBeenCalledTimes(2)
  })
})

describe("l'etat des touches est expose pour la tache 5", () => {
  it('sait que Maj est enfoncee pendant qu’elle l’est, et plus apres', () => {
    const capture: Capture = {}
    render(<Harness world={mondeManuel()} capture={capture} />)
    fireEvent.keyDown(document, { key: 'Shift', shiftKey: true })
    expect(capture.estToucheEnfoncee?.('Shift')).toBe(true)
    fireEvent.keyUp(document, { key: 'Shift', shiftKey: false })
    expect(capture.estToucheEnfoncee?.('Shift')).toBe(false)
  })
})
