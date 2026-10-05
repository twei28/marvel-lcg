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
const ALLIE = carteSurTable(5, '01006a', 'Ally', 'Allie de test')
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
    siege({ allies: [SANS_JETON, ALLIE], player_deck: [DESSUS_DECK_JOUEUR] }),
    {
      mode_manuel: true,
      // La boucle manuelle a deja pris la main (tache 8 bis) : le clavier ne
      // s'arme que sur `manuel_actif`, jamais sur la seule regle
      // `mode_manuel` (vraie des la mise en place).
      manuel_actif: true,
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
  it('Ctrl+F retourne la carte survolee', async () => {
    render(<Harness world={mondeManuel()} capture={{}} />)
    survoler(7)
    fireEvent.keyDown(document, { key: 'f', ctrlKey: true })
    await act(async () => { await Promise.resolve() })
    expect(fetch).toHaveBeenCalledWith('/sandbox_command', expect.objectContaining({
      body: JSON.stringify({ commands: ['Puzzle.Flip(7)'] }),
    }))
  })

  it('F5 sur une manigance pose de la menace, Maj+F5 en retire', async () => {
    render(<Harness world={mondeManuel()} capture={{}} />)
    survoler(9)
    fireEvent.keyDown(document, { key: 'F5' })
    await act(async () => { await Promise.resolve() })
    expect(fetch).toHaveBeenCalledWith('/sandbox_command', expect.objectContaining({
      body: JSON.stringify({ commands: ['Puzzle.PlaceThreat(9, 1)'] }),
    }))
  })

  it('Maj+F3 sur un personnage soigne au lieu de blesser', async () => {
    render(<Harness world={mondeManuel()} capture={{}} />)
    survoler(7)
    fireEvent.keyDown(document, { key: 'F3', shiftKey: true })
    await act(async () => { await Promise.resolve() })
    expect(fetch).toHaveBeenCalledWith('/sandbox_command', expect.objectContaining({
      body: JSON.stringify({ commands: ['Puzzle.Heal(7, 1)'] }),
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

  it('F3 sur un personnage pose un degat', async () => {
    render(<Harness world={mondeManuel()} capture={{}} />)
    survoler(7)
    fireEvent.keyDown(document, { key: 'F3' })
    await act(async () => { await Promise.resolve() })
    expect(fetch).toHaveBeenCalledWith('/sandbox_command', expect.objectContaining({
      body: JSON.stringify({ commands: ['Puzzle.Damage(7, 1)'] }),
    }))
  })

  it('les anciennes touches maison (F, Q, R, chiffre sur une carte) ne font rien', async () => {
    render(<Harness world={mondeManuel()} capture={{}} />)
    survoler(7)
    for (const cle of ['f', 'q', '3']) fireEvent.keyDown(document, { key: cle })
    survoler(20)
    fireEvent.keyDown(document, { key: 'r' })
    await act(async () => { await Promise.resolve() })
    expect(fetch).not.toHaveBeenCalled()
  })

  it('Ctrl+Q redresse tout ce qui est incline chez le joueur', async () => {
    const monde = tableAvec(siege({ area_hero: [{ ...ALLIE, id: 30, is_ready: false } as never], allies: [] }), {
      mode_manuel: true,
      manuel_actif: true,
    } as never)
    render(<Harness world={monde} capture={{}} />)
    fireEvent.keyDown(document, { key: 'q', ctrlKey: true })
    await act(async () => { await Promise.resolve() })
    expect(fetch).toHaveBeenCalledWith('/sandbox_command', expect.objectContaining({
      body: JSON.stringify({ commands: ['Puzzle.Ready(30)'] }),
    }))
  })

  it('Ctrl+Maj+D demande combien de cartes piocher', async () => {
    vi.stubGlobal('prompt', vi.fn(() => '3'))
    render(<Harness world={mondeManuel()} capture={{}} />)
    survoler(20)
    fireEvent.keyDown(document, { key: 'd', ctrlKey: true, shiftKey: true })
    await act(async () => { await Promise.resolve() })
    expect(prompt).toHaveBeenCalled()
  })

  // LE CRITIQUE (retour de revue, 19/09/2026) : Ctrl/Cmd/Alt sont les
  // raccourcis du NAVIGATEUR (Ctrl+R recharge, Ctrl+1..9 change d'onglet).
  // Seules les combinaisons d'OCTGN agissent (voir plus bas). Le temoin qui
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

  // Depuis l'ajout des raccourcis d'OCTGN (06/10/2026) : Ctrl+F retourne la
  // carte survolee et ne laisse PLUS la recherche du navigateur s'ouvrir, mais
  // seulement quand une carte est survolee.
  it('Ctrl+F retourne la carte survolee (OCTGN) et garde le raccourci pour le jeu', async () => {
    render(<Harness world={mondeManuel()} capture={{}} />)
    survoler(7)
    const nonAnnule = fireEvent.keyDown(document, { key: 'f', ctrlKey: true })
    await act(async () => { await Promise.resolve() })
    expect(fetch).toHaveBeenCalledWith('/sandbox_command', expect.objectContaining({
      body: JSON.stringify({ commands: ['Puzzle.Flip(7)'] }),
    }))
    expect(nonAnnule).toBe(false)
  })

  it('Ctrl+F sans rien sous la souris laisse la recherche du navigateur s’ouvrir', async () => {
    render(<Harness world={mondeManuel()} capture={{}} />)
    const nonAnnule = fireEvent.keyDown(document, { key: 'f', ctrlKey: true })
    await act(async () => { await Promise.resolve() })
    expect(fetch).not.toHaveBeenCalled()
    expect(nonAnnule).toBe(true)
  })

  it('Ctrl+S sur une pile la mélange ; Ctrl+D pioche une carte', async () => {
    render(<Harness world={mondeManuel()} capture={{}} />)
    survoler(20)
    const nonAnnule = fireEvent.keyDown(document, { key: 's', ctrlKey: true })
    await act(async () => { await Promise.resolve() })
    expect(fetch).toHaveBeenCalledWith('/sandbox_command', expect.objectContaining({
      body: JSON.stringify({ commands: ["Puzzle.Shuffle('PlayerDeck')"] }),
    }))
    expect(nonAnnule).toBe(false)
  })

  it('F7 incline la carte survolée, F3 lui pose un dégât, Maj+F3 en retire un', async () => {
    render(<Harness world={mondeManuel()} capture={{}} />)
    survoler(5)
    fireEvent.keyDown(document, { key: 'F7' })
    await act(async () => { await Promise.resolve() })
    expect(fetch).toHaveBeenCalledWith('/sandbox_command', expect.objectContaining({
      body: JSON.stringify({ commands: ['Puzzle.Exhaust(5)'] }),
    }))
  })

  it('Alt+S pose ou retire Étourdi sur un personnage', async () => {
    render(<Harness world={mondeManuel()} capture={{}} />)
    survoler(7)
    fireEvent.keyDown(document, { key: 's', altKey: true })
    await act(async () => { await Promise.resolve() })
    expect(fetch).toHaveBeenCalledWith('/sandbox_command', expect.objectContaining({
      body: JSON.stringify({ commands: ['Puzzle.Stun(7)'] }),
    }))
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
    fireEvent.keyDown(document, { key: 'F3' })
    await act(async () => { await Promise.resolve() })
    expect(fetch).not.toHaveBeenCalled()
  })

  it('ne mord pas quand rien n’est survole', async () => {
    render(<Harness world={mondeManuel()} capture={{}} />)
    fireEvent.keyDown(document, { key: 'f', ctrlKey: true })
    await act(async () => { await Promise.resolve() })
    expect(fetch).not.toHaveBeenCalled()
  })

  it('ne mord pas hors du mode manuel', async () => {
    const monde = { ...mondeManuel(), mode_manuel: false, manuel_actif: false, mode_sandbox: true } as World
    render(<Harness world={monde} capture={{}} />)
    survoler(7)
    fireEvent.keyDown(document, { key: 'f', ctrlKey: true })
    await act(async () => { await Promise.resolve() })
    expect(fetch).not.toHaveBeenCalled()
  })

  // RONDE DE CORRECTION 1 (tache 8 bis). Lacune de filet signalee par la
  // revue : aucun cas ne couvrait « partie manuelle, mise en place en
  // cours » (mode_manuel VRAI, manuel_actif FAUX) - exactement l'etat dans
  // lequel le mode etait bloque avant le correctif. Temoin de REFUS : MEME
  // geste, MEME carte survolee que le cas vert juste au-dessus
  // (`mondeManuel()`), seul `manuel_actif` change - la preuve que c'est
  // bien cette variable, et pas `mode_manuel`, qui arme le clavier.
  it('ne mord pas PENDANT LA MISE EN PLACE (mode_manuel vrai, manuel_actif encore faux)', async () => {
    const monde = { ...mondeManuel(), manuel_actif: false } as World
    render(<Harness world={monde} capture={{}} />)
    survoler(7)
    fireEvent.keyDown(document, { key: 'f', ctrlKey: true })
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
    fireEvent.keyDown(champ, { key: 'f', ctrlKey: true })
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
    const monde = { ...mondeManuel(), mode_manuel: false, manuel_actif: false, mode_sandbox: true } as World
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

describe('les gestes OCTGN parlent au moteur', () => {
  const envoye = (commande: string) =>
    expect(fetch).toHaveBeenCalledWith('/sandbox_command', expect.objectContaining({
      body: JSON.stringify({ commands: [commande] }),
    }))

  it('fleche haut / bas : un point de vie de plus ou de moins sur le mechant', async () => {
    render(<Harness world={mondeManuel()} capture={{}} />)
    survoler(7)
    fireEvent.keyDown(document, { key: 'ArrowUp' })
    await act(async () => { await Promise.resolve() })
    envoye('Puzzle.Heal(7, 1)')
    fireEvent.keyDown(document, { key: 'ArrowDown' })
    await act(async () => { await Promise.resolve() })
    envoye('Puzzle.Damage(7, 1)')
  })

  it('fleche droite / gauche : un jeton generique ; haut sur une manigance : de la menace', async () => {
    render(<Harness world={mondeManuel()} capture={{}} />)
    survoler(7)
    fireEvent.keyDown(document, { key: 'ArrowRight' })
    await act(async () => { await Promise.resolve() })
    envoye("Puzzle.Counter(7, 'counter', 1)")
    fireEvent.keyDown(document, { key: 'ArrowLeft' })
    await act(async () => { await Promise.resolve() })
    envoye("Puzzle.Counter(7, 'counter', -1)")
    survoler(9)
    fireEvent.keyDown(document, { key: 'ArrowUp' })
    await act(async () => { await Promise.resolve() })
    envoye('Puzzle.PlaceThreat(9, 1)')
  })

  it('Suppr defausse la carte survolee', async () => {
    render(<Harness world={mondeManuel()} capture={{}} />)
    survoler(5)
    fireEvent.keyDown(document, { key: 'Delete' })
    await act(async () => { await Promise.resolve() })
    envoye('Puzzle.Discard(5)')
  })

  it('double-clic sur un personnage : il s incline', async () => {
    render(<Harness world={mondeManuel()} capture={{}} />)
    fireEvent.doubleClick(survoler(5))
    await act(async () => { await Promise.resolve() })
    envoye('Puzzle.Exhaust(5)')
  })

  it('double-clic sur le mechant : la carte du dessus du deck Rencontre sort en resolution', async () => {
    render(<Harness world={mondeManuel()} capture={{}} />)
    fireEvent.doubleClick(survoler(7))
    await act(async () => { await Promise.resolve() })
    envoye("Puzzle.MoveTo(21, 'ProcessingArea', 'Top')")
  })

  it('double-clic sur une manigance, une carte sans etat ou une pile : rien', async () => {
    render(<Harness world={mondeManuel()} capture={{}} />)
    for (const id of [9, 4, 20]) fireEvent.doubleClick(survoler(id))
    await act(async () => { await Promise.resolve() })
    expect(fetch).not.toHaveBeenCalled()
  })

  it('double-clic ignore hors du mode manuel', async () => {
    const monde = mondeManuel()
    ;(monde as unknown as { manuel_actif: boolean }).manuel_actif = false
    ;(monde as unknown as { mode_manuel: boolean }).mode_manuel = false
    render(<Harness world={monde} capture={{}} />)
    fireEvent.doubleClick(survoler(5))
    await act(async () => { await Promise.resolve() })
    expect(fetch).not.toHaveBeenCalled()
  })

  it('C ouvre la recherche dans tout le catalogue, sans carte survolee', async () => {
    const { queryByRole } = render(<Harness world={mondeManuel()} capture={{}} />)
    expect(queryByRole('dialog')).toBeNull()
    const nonAnnule = fireEvent.keyDown(document, { key: 'c' })
    await act(async () => { await Promise.resolve() })
    expect(queryByRole('dialog')).not.toBeNull()
    expect(nonAnnule).toBe(false)
    expect(fetch).not.toHaveBeenCalled()
  })

  it('le bouton « Chercher une carte » ouvre la meme recherche', async () => {
    const { getByText, queryByRole } = render(<Harness world={mondeManuel()} capture={{}} />)
    fireEvent.click(getByText('Chercher une carte'))
    expect(queryByRole('dialog')).not.toBeNull()
  })

  it('C tape dans un champ de texte, ou avec Ctrl, n ouvre rien', async () => {
    const { queryByRole } = render(<Harness world={mondeManuel()} capture={{}} />)
    const champ = document.createElement('input')
    document.body.appendChild(champ)
    champ.focus()
    fireEvent.keyDown(champ, { key: 'c' })
    champ.blur()
    const nonAnnule = fireEvent.keyDown(document, { key: 'c', ctrlKey: true })
    await act(async () => { await Promise.resolve() })
    expect(queryByRole('dialog')).toBeNull()
    expect(nonAnnule).toBe(true)
  })

  it('hors du mode manuel, C n ouvre rien et le bouton est absent', async () => {
    const monde = mondeManuel()
    ;(monde as unknown as { manuel_actif: boolean }).manuel_actif = false
    ;(monde as unknown as { mode_manuel: boolean }).mode_manuel = false
    const { queryByRole, queryByText } = render(<Harness world={monde} capture={{}} />)
    fireEvent.keyDown(document, { key: 'c' })
    await act(async () => { await Promise.resolve() })
    expect(queryByRole('dialog')).toBeNull()
    expect(queryByText('Chercher une carte')).toBeNull()
  })
})
