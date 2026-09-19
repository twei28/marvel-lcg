// CoucheTriche.test.tsx — le bandeau, la pile et la résolution différée d'un
// geste, isolés du plateau entier.
//
// Le crochet `useTriche` a besoin d'un monde complet ; les tests du bandeau et
// de la pile visent directement le composant `<CoucheTriche>`, avec une
// `couche` construite à la main. C'est ce que `useTriche` lui donnerait de
// toute façon : `{ menu, pile, setMenu, setPile, emettreGeste, avisRefus }`.
// Les tests de résolution (plus bas) ont besoin du VRAI `useTriche`, sur le
// modèle de `board/manuel/clavier-wiring.test.tsx`.
import { act, fireEvent, render, screen } from '@testing-library/react'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { CoucheTriche, useTriche } from './CoucheTriche'
import { catalogueVide, type Catalogue } from './catalogue'
import { carteSurTable, siege, tableAvec } from './plateau-de-test'
import type { World, WorldCard } from './world'

function coucheVide() {
  return {
    menu: undefined,
    pile: undefined,
    setMenu: vi.fn(),
    setPile: vi.fn(),
    // Appelle vraiment le déposeur, comme le ferait le `emettreGeste` réel de
    // `useTriche` : sans ça, `triche.melanger` ne serait jamais invoqué dans
    // le test « la pile ouverte propose de la mélanger » plus bas, et `fetch`
    // ne verrait jamais passer la commande.
    emettreGeste: vi.fn(async (_libelle: string, deposer: () => Promise<boolean>) => {
      await deposer()
    }),
    avisRefus: undefined as string | undefined,
    annulationEnCours: false,
    menuTable: undefined as { x: number; y: number } | undefined,
    setMenuTable: vi.fn(),
  }
}

const CARTE: WorldCard = { id: 1, name: 'Carte test', card_type: 'Ally' } as WorldCard

beforeEach(() => {
  vi.stubGlobal('fetch', vi.fn(async () => ({ ok: true }) as Response))
})

describe('le bandeau ne dénonce que le bac à sable', () => {
  it('s’affiche en bac à sable', () => {
    const { container } = render(<CoucheTriche actif manuel={false} couche={coucheVide()} />)
    expect(container.querySelector('.bandeau-triche')).not.toBeNull()
  })

  it('ne s’affiche pas en mode manuel : il n’y a rien à dénoncer', () => {
    const { container } = render(<CoucheTriche actif manuel couche={coucheVide()} />)
    expect(container.querySelector('.bandeau-triche')).toBeNull()
  })
})

describe('la pile ouverte propose de la mélanger', () => {
  it('mélange la pile visée quand on clique dessus', async () => {
    const couche = {
      ...coucheVide(),
      pile: { titre: 'Deck Rencontre', cartes: [CARTE], duJoueur: false, zone: 'EncounterDeck' },
    }
    const { getByText } = render(<CoucheTriche actif manuel couche={couche} />)
    fireEvent.click(getByText('Mélanger'))
    await Promise.resolve()
    expect(fetch).toHaveBeenCalledWith('/sandbox_command', expect.objectContaining({
      body: JSON.stringify({ commands: ["Puzzle.Shuffle('EncounterDeck')"] }),
    }))
  })
})

describe('l’avis de refus ne se montre qu’en mode manuel', () => {
  it('reste invisible sans avis à montrer', () => {
    const { container } = render(<CoucheTriche actif manuel couche={coucheVide()} />)
    expect(container.querySelector('.avis-refus-manuel')).toBeNull()
  })

  it('s’affiche quand un avis est posé, en mode manuel', () => {
    const couche = { ...coucheVide(), avisRefus: 'Retourner — Rhino (refusé)' }
    const { container, getByText } = render(<CoucheTriche actif manuel couche={couche} />)
    expect(container.querySelector('.avis-refus-manuel')).not.toBeNull()
    expect(getByText('Retourner — Rhino (refusé)')).toBeTruthy()
  })

  it('reste masqué hors mode manuel, même avec un avis posé', () => {
    // Défensif : `useTriche` ne pose `avisRefus` qu'en mode manuel, mais le
    // composant ne doit pas dépendre de cette seule discipline de l'appelant.
    const couche = { ...coucheVide(), avisRefus: 'Retourner — Rhino (refusé)' }
    const { container } = render(<CoucheTriche actif manuel={false} couche={couche} />)
    expect(container.querySelector('.avis-refus-manuel')).toBeNull()
  })
})

// --- La résolution différée d'un geste (correction du 19/09/2026) ---------
//
// ÉCART CORRIGÉ : la version d'origine de la tâche 4 ter écrivait la ligne du
// geste tout de suite (sur le succès du DÉPÔT HTTP), et une ligne GÉNÉRIQUE
// séparée quand le moteur refusait plus tard — deux lignes qui pouvaient se
// contredire, sans dire quel geste était visé. Ici, la ligne n'est écrite
// qu'une fois, au rendu qui connaît l'issue réelle.
//
// Harnais calqué sur board/manuel/clavier-wiring.test.tsx : `useTriche` a
// besoin d'un monde complet pour observer son effet sur `render_id` et
// `manuel_refus`, pas d'une `couche` construite à la main.
const VILAIN = carteSurTable(7, '01001a', 'EncounterVillain', 'Rhino')
const AUTRE = carteSurTable(8, '01002a', 'EncounterVillain', 'Klaw')

function mondeManuel(surcharge: Partial<World> = {}): World {
  return tableAvec(siege(), {
    mode_manuel: true,
    // La boucle manuelle a deja pris la main (tache 8 bis) : ces cas
    // observent les GESTES manuels eux-memes, qui ne s'ouvrent que sur
    // `manuel_actif`, jamais sur la seule regle `mode_manuel`.
    manuel_actif: true,
    render_id: 1,
    manuel_refus: '',
    villains: [VILAIN, AUTRE],
    ...surcharge,
  } as never)
}

function Harness({
  world,
  ajouterAuJournal,
  catalogue,
}: {
  world: World
  ajouterAuJournal?: (l: string) => void
  catalogue?: Catalogue
}) {
  const triche = useTriche(world, 0, ajouterAuJournal)
  return (
    <CoucheTriche
      actif={triche.actif}
      manuel={triche.manuel}
      couche={triche.couche}
      catalogue={catalogue}
    />
  )
}

function survoler(id: number): void {
  const noeud = document.createElement('div')
  noeud.setAttribute('data-card-id', String(id))
  document.body.appendChild(noeud)
  fireEvent.pointerMove(noeud)
}

/** Laisse toutes les promesses en chaîne (fetch, triche.ts, emettreGeste) se résoudre. */
const attendreLeReseau = () => act(() => new Promise((resolve) => setTimeout(resolve, 0)))

describe('un geste manuel refusé se voit, sans jamais dire l’inverse (correction du 19/09/2026)', () => {
  it('n’écrit rien tant que l’issue n’est pas connue', async () => {
    const ajouterAuJournal = vi.fn()
    render(<Harness world={mondeManuel()} ajouterAuJournal={ajouterAuJournal} />)
    survoler(7)
    fireEvent.keyDown(document, { key: 'f' })
    await attendreLeReseau()
    expect(fetch).toHaveBeenCalled()
    expect(ajouterAuJournal).not.toHaveBeenCalled()
  })

  it('écrit la ligne SANS marque quand le rendu suivant dit que le geste est passé', async () => {
    const ajouterAuJournal = vi.fn()
    const avant = mondeManuel()
    const { rerender } = render(<Harness world={avant} ajouterAuJournal={ajouterAuJournal} />)
    survoler(7)
    fireEvent.keyDown(document, { key: 'f' })
    await attendreLeReseau()
    expect(ajouterAuJournal).not.toHaveBeenCalled()

    const suivant = { ...avant, render_id: 2, manuel_refus: '' } as World
    await act(async () => {
      rerender(<Harness world={suivant} ajouterAuJournal={ajouterAuJournal} />)
    })
    expect(ajouterAuJournal).toHaveBeenCalledTimes(1)
    expect(ajouterAuJournal).toHaveBeenCalledWith('Retourner — Rhino')
  })

  it('écrit la ligne AVEC sa marque quand le moteur refuse — jamais l’inverse, jamais deux lignes', async () => {
    const ajouterAuJournal = vi.fn()
    const avant = mondeManuel()
    const { container, rerender } = render(<Harness world={avant} ajouterAuJournal={ajouterAuJournal} />)
    survoler(7)
    fireEvent.keyDown(document, { key: 'f' })
    await attendreLeReseau()

    const suivant = {
      ...avant,
      render_id: 2,
      manuel_refus: "KeyError: 'zone inconnue : ZoneInconnue'",
    } as World
    await act(async () => {
      rerender(<Harness world={suivant} ajouterAuJournal={ajouterAuJournal} />)
    })

    // UNE SEULE ligne — jamais la ligne « faite » d'abord, puis une ligne de
    // refus générique ensuite (c'est exactement le défaut corrigé).
    expect(ajouterAuJournal).toHaveBeenCalledTimes(1)
    expect(ajouterAuJournal).toHaveBeenCalledWith('Retourner — Rhino (refusé)')
    expect(container.textContent).toContain('Retourner — Rhino (refusé)')
    // Le motif technique ne s'affiche jamais tel quel.
    expect(container.textContent).not.toContain('KeyError')
    expect(container.textContent).not.toContain('ZoneInconnue')
  })

  it('un dépôt qui échoue (réseau) reste immédiat : aucun rendu futur ne le concernera jamais', async () => {
    vi.stubGlobal('fetch', vi.fn(async () => ({ ok: false }) as Response))
    const ajouterAuJournal = vi.fn()
    render(<Harness world={mondeManuel()} ajouterAuJournal={ajouterAuJournal} />)
    survoler(7)
    fireEvent.keyDown(document, { key: 'f' })
    await attendreLeReseau()
    expect(ajouterAuJournal).toHaveBeenCalledTimes(1)
    expect(ajouterAuJournal).toHaveBeenCalledWith('Retourner — Rhino (refusé)')
  })

  it('ne devine pas quand deux gestes sont en vol au même rendu : issue inconnue pour chacun', async () => {
    const ajouterAuJournal = vi.fn()
    const avant = mondeManuel()
    const { rerender } = render(<Harness world={avant} ajouterAuJournal={ajouterAuJournal} />)

    survoler(7)
    fireEvent.keyDown(document, { key: 'f' }) // Retourner — Rhino
    survoler(8)
    fireEvent.keyDown(document, { key: 'q' }) // Incliner — Klaw
    await attendreLeReseau()
    expect(ajouterAuJournal).not.toHaveBeenCalled()

    const suivant = { ...avant, render_id: 2, manuel_refus: '' } as World
    await act(async () => {
      rerender(<Harness world={suivant} ajouterAuJournal={ajouterAuJournal} />)
    })

    // Un seul drainage moteur peut regrouper les deux commandes : impossible
    // de savoir laquelle a réussi. Ni succès ni refus inventés.
    expect(ajouterAuJournal).toHaveBeenCalledTimes(2)
    expect(ajouterAuJournal).toHaveBeenCalledWith('Retourner — Rhino (issue inconnue)')
    expect(ajouterAuJournal).toHaveBeenCalledWith('Incliner — Klaw (issue inconnue)')
  })

  it('ignore un rendu qui ne concerne aucun geste en attente (par ex. un autre joueur)', async () => {
    const ajouterAuJournal = vi.fn()
    const avant = mondeManuel()
    const { rerender } = render(<Harness world={avant} ajouterAuJournal={ajouterAuJournal} />)

    const suivant = { ...avant, render_id: 2, manuel_refus: "KeyError: 'zone inconnue : X'" } as World
    await act(async () => {
      rerender(<Harness world={suivant} ajouterAuJournal={ajouterAuJournal} />)
    })
    expect(ajouterAuJournal).not.toHaveBeenCalled()
  })

  it('ne rejoue rien sur un rendu React qui ne change pas render_id', async () => {
    const ajouterAuJournal = vi.fn()
    const avant = mondeManuel()
    const { rerender } = render(<Harness world={avant} ajouterAuJournal={ajouterAuJournal} />)
    survoler(7)
    fireEvent.keyDown(document, { key: 'f' })
    await attendreLeReseau()

    const suivant = { ...avant, render_id: 2, manuel_refus: '' } as World
    await act(async () => {
      rerender(<Harness world={suivant} ajouterAuJournal={ajouterAuJournal} />)
    })
    expect(ajouterAuJournal).toHaveBeenCalledTimes(1)

    // Même `render_id` : un second rendu React (pas un nouveau rendu moteur)
    // ne doit rien rejouer.
    await act(async () => {
      rerender(<Harness world={{ ...suivant }} ajouterAuJournal={ajouterAuJournal} />)
    })
    expect(ajouterAuJournal).toHaveBeenCalledTimes(1)
  })
})

// --- Faire apparaître une carte du catalogue (tâche 6) ---------------------
// « Faire apparaître une carte » est une action de TABLE (ronde de
// correction 1) : elle s'atteint par un clic droit HORS de toute carte, pas
// via le menu d'une carte précise — le jour où l'on cherche une carte, c'est
// justement parce qu'il en manque une.
describe('faire apparaître une carte, en mode manuel', () => {
  function ouvrirMenuSur(id: number): void {
    const noeud = document.createElement('div')
    noeud.setAttribute('data-card-id', String(id))
    document.body.appendChild(noeud)
    fireEvent.contextMenu(noeud)
  }

  /** Un clic droit dans le vide : aucun `data-card-id` sous le curseur. */
  function clicDroitSurTable(): void {
    const table = document.createElement('div')
    document.body.appendChild(table)
    fireEvent.contextMenu(table)
  }

  const catalogueDeTest: Catalogue = {
    ...catalogueVide,
    chercherParNom: (fragment) =>
      fragment.length < 2 ? [] : [{ card_id: '01094', name: 'Rhino' }],
  }

  it('le clic droit sur une carte n’offre plus « Faire apparaître » : ce n’est pas une action de carte', async () => {
    render(<Harness world={mondeManuel()} catalogue={catalogueDeTest} />)
    ouvrirMenuSur(VILAIN.id)
    expect(screen.getByText('Incliner')).toBeTruthy()
    expect(screen.queryByText('Faire apparaître une carte')).toBeNull()
  })

  it('le clic droit dans le vide ouvre le menu de la table, le clic ouvre le catalogue', async () => {
    render(<Harness world={mondeManuel()} catalogue={catalogueDeTest} />)
    clicDroitSurTable()
    fireEvent.click(screen.getByText('Faire apparaître une carte'))
    expect(screen.getByRole('searchbox')).toBeTruthy()
  })

  it('ne s’ouvre pas hors du mode manuel : le bac à sable garde son clic droit dans le vide inerte', async () => {
    const monde = { ...mondeManuel(), mode_manuel: false, manuel_actif: false, mode_sandbox: true } as World
    render(<Harness world={monde} catalogue={catalogueDeTest} />)
    clicDroitSurTable()
    expect(screen.queryByText('Faire apparaître une carte')).toBeNull()
  })

  // RONDE DE CORRECTION 1 (tache 8 bis). Lacune de filet signalee par la
  // revue : aucun cas ne couvrait « partie manuelle, mise en place en
  // cours » (mode_manuel VRAI, manuel_actif FAUX) - exactement l'etat dans
  // lequel le mode etait bloque avant le correctif. Temoin de REFUS : MEME
  // geste, MEME carte (VILAIN) que le premier cas de ce bloc (qui, lui,
  // ouvre bien le menu « Incliner » en manuel ACTIF) - seul `manuel_actif`
  // change, preuve que c'est cette variable, et pas `mode_manuel`, qui
  // arme le clic droit.
  it('pendant la mise en place (mode_manuel vrai, manuel_actif encore faux) : le clic droit n’ouvre aucun menu manuel', async () => {
    const monde = { ...mondeManuel(), manuel_actif: false } as World
    render(<Harness world={monde} catalogue={catalogueDeTest} />)
    ouvrirMenuSur(VILAIN.id)
    expect(screen.queryByText('Incliner')).toBeNull()
    expect(screen.queryByText('Faire apparaître une carte')).toBeNull()
    clicDroitSurTable()
    expect(screen.queryByText('Faire apparaître une carte')).toBeNull()
  })

  it('poser une carte du catalogue l’envoie en zone de résolution, et ferme le catalogue', async () => {
    const ajouterAuJournal = vi.fn()
    const avant = mondeManuel()
    const { rerender } = render(
      <Harness world={avant} ajouterAuJournal={ajouterAuJournal} catalogue={catalogueDeTest} />
    )
    clicDroitSurTable()
    fireEvent.click(screen.getByText('Faire apparaître une carte'))
    fireEvent.change(screen.getByRole('searchbox'), { target: { value: 'rhi' } })
    fireEvent.click(screen.getByText('Rhino'))
    await attendreLeReseau()

    expect(fetch).toHaveBeenCalledWith('/sandbox_command', expect.objectContaining({
      body: JSON.stringify({ commands: ["Puzzle.MoveTo('01094', 'ProcessingArea', 'Top')"] }),
    }))
    expect(screen.queryByRole('searchbox')).toBeNull()

    // Le nom, pas seulement l'identifiant : le journal doit rester lisible
    // pour qui relit la partie plus tard (ronde de correction 1). La ligne
    // n'est écrite qu'au rendu suivant (voir la résolution différée d'un
    // geste, plus haut).
    const suivant = { ...avant, render_id: 2, manuel_refus: '' } as World
    await act(async () => {
      rerender(
        <Harness world={suivant} ajouterAuJournal={ajouterAuJournal} catalogue={catalogueDeTest} />
      )
    })
    expect(ajouterAuJournal).toHaveBeenCalledWith('Faire apparaître — Rhino')
  })
})

describe('déclarer la fin d’une partie manuelle (tâche 7)', () => {
  function ouvrirFinManuelle(): void {
    const table = document.createElement('div')
    document.body.appendChild(table)
    fireEvent.contextMenu(table)
    fireEvent.click(screen.getByText('Terminer la partie'))
  }

  it('envoie Puzzle.Win() après confirmation d’une victoire', async () => {
    render(<Harness world={mondeManuel()} />)
    ouvrirFinManuelle()
    fireEvent.click(screen.getByText('Victoire'))
    fireEvent.click(screen.getByText('Confirmer'))
    await attendreLeReseau()

    expect(fetch).toHaveBeenCalledWith('/sandbox_command', expect.objectContaining({
      body: JSON.stringify({ commands: ['Puzzle.Win()'] }),
    }))
  })

  it('envoie Puzzle.Lose() après confirmation d’une défaite, et ferme le panneau', async () => {
    render(<Harness world={mondeManuel()} />)
    ouvrirFinManuelle()
    fireEvent.click(screen.getByText('Défaite'))
    fireEvent.click(screen.getByText('Confirmer'))
    await attendreLeReseau()

    expect(fetch).toHaveBeenCalledWith('/sandbox_command', expect.objectContaining({
      body: JSON.stringify({ commands: ['Puzzle.Lose()'] }),
    }))
    expect(screen.queryByText('Confirmer')).toBeNull()
  })

  it('n’envoie rien tant que la confirmation n’a pas eu lieu', async () => {
    render(<Harness world={mondeManuel()} />)
    ouvrirFinManuelle()
    fireEvent.click(screen.getByText('Victoire'))
    await attendreLeReseau()
    expect(fetch).not.toHaveBeenCalledWith('/sandbox_command', expect.anything())
  })

  it('écrit la ligne du journal au rendu suivant, comme tout autre geste', async () => {
    const ajouterAuJournal = vi.fn()
    const avant = mondeManuel()
    const { rerender } = render(<Harness world={avant} ajouterAuJournal={ajouterAuJournal} />)
    ouvrirFinManuelle()
    fireEvent.click(screen.getByText('Victoire'))
    fireEvent.click(screen.getByText('Confirmer'))
    await attendreLeReseau()
    expect(ajouterAuJournal).not.toHaveBeenCalled()

    const suivant = { ...avant, render_id: 2, manuel_refus: '', game_over: true, players_won: true } as World
    await act(async () => {
      rerender(<Harness world={suivant} ajouterAuJournal={ajouterAuJournal} />)
    })
    expect(ajouterAuJournal).toHaveBeenCalledWith('Fin de partie — Victoire')
  })

  // ⚠ CORRECTION (ronde 1) : le texte de `FinManuelle` affirmait que cette
  // décision ne se rattrape pas. Le relecteur a tracé le chemin complet côté
  // moteur et a montré que c'était faux : le Ctrl+Z du mode rejoue la partie
  // moins son dernier geste, fin de partie déclarée comprise, et l'état
  // obtenu est sain. Le texte a été corrigé pour dire l'inverse (« tu
  // pourras revenir en arrière ») ; ce test verrouille la partie de cette
  // promesse qu'on PEUT tenir depuis le client : que déclarer la fin ne
  // désarme pas le Ctrl+Z d'aucune façon (pas de garde oubliée, pas de
  // couche démontée sous l'écran de fin) — sans ça, la prochaine
  // modification pourrait le casser en silence et rendre le texte faux à
  // nouveau.
  it('le Ctrl+Z défait aussi une fin de partie déclarée : ce n’est pas irréversible', async () => {
    const ajouterAuJournal = vi.fn()
    const avant = mondeManuel()
    const { rerender } = render(<Harness world={avant} ajouterAuJournal={ajouterAuJournal} />)
    ouvrirFinManuelle()
    fireEvent.click(screen.getByText('Victoire'))
    fireEvent.click(screen.getByText('Confirmer'))
    await attendreLeReseau()

    const finDeclaree = { ...avant, render_id: 2, manuel_refus: '', game_over: true, players_won: true } as World
    await act(async () => {
      rerender(<Harness world={finDeclaree} ajouterAuJournal={ajouterAuJournal} />)
    })
    expect(ajouterAuJournal).toHaveBeenCalledWith('Fin de partie — Victoire')

    // La fin déclarée n'a rien désarmé : le MÊME Ctrl+Z, sur la MÊME route
    // (`/manuel_undo`), fonctionne exactement comme pour n'importe quel
    // autre geste — voir `manuel/clavier-wiring.test.tsx`.
    fireEvent.keyDown(document, { key: 'z', ctrlKey: true })
    await attendreLeReseau()
    expect(fetch).toHaveBeenCalledWith('/manuel_undo', { method: 'POST' })
    expect(ajouterAuJournal).toHaveBeenCalledWith('Dernier geste annulé')
  })
})

// --- Le bac à sable garde son journal (correction du 19/09/2026, ronde 2) --
//
// RÉGRESSION CORRIGÉE : l'effet de résolution ne tournait qu'en mode manuel
// (`if (!manuel ...)`), hérité de l'ancien effet qui n'avait de sens qu'à ce
// mode-là. Mais `emettreGeste` (correction ronde 1, ci-dessus) est devenu
// l'UNIQUE chemin d'écriture au journal pour LES DEUX modes — le bac à sable
// partage le même menu (`MenuTriche`) et les mêmes actions de pile. Chaque
// geste de bac à sable partait donc dans la file d'attente, et RIEN ne l'en
// sortait plus jamais : le journal restait muet pour tout ce mode. Un
// mensonge (le défaut d'origine) échangé contre un silence — pire, et le
// seul résultat que la revue ne voulait pas.
//
// ⚠ C'EST L'ABSENCE DE CE CAS QUI A LAISSÉ PASSER LA RÉGRESSION (constat de
// la revue) : tous les cas précédents qui utilisent le VRAI `useTriche` sont
// construits en mode manuel ; les cas « bac à sable » restants (plus haut,
// bandeau et pile) n'utilisent qu'une `couche` FACTICE dont `emettreGeste`
// appelle directement le déposeur — ils ne regardent jamais si un journal
// existe derrière. Celui-ci utilise le vrai `useTriche`, un vrai
// `ajouterAuJournal`, et déclenche le geste par le clic droit (`MenuTriche`),
// le seul chemin du bac à sable — la touche clavier, elle, reste réservée au
// mode manuel (`if (!manuel) return`, plus haut dans `useTriche`).
describe('le bac à sable garde son journal (correction du 19/09/2026, ronde 2)', () => {
  function mondeSandbox(surcharge: Partial<World> = {}): World {
    return tableAvec(siege(), {
      mode_manuel: false,
      mode_sandbox: true,
      render_id: 1,
      manuel_refus: '',
      villains: [VILAIN],
      ...surcharge,
    } as never)
  }

  function ouvrirMenuSur(id: number): void {
    const noeud = document.createElement('div')
    noeud.setAttribute('data-card-id', String(id))
    document.body.appendChild(noeud)
    fireEvent.contextMenu(noeud)
  }

  it('n’écrit rien tant que l’issue n’est pas connue, puis écrit la ligne au rendu suivant', async () => {
    const ajouterAuJournal = vi.fn()
    const avant = mondeSandbox()
    const { getByText, rerender } = render(<Harness world={avant} ajouterAuJournal={ajouterAuJournal} />)

    ouvrirMenuSur(VILAIN.id)
    fireEvent.click(getByText('Incliner'))
    await attendreLeReseau()
    // Le cœur de la régression : sans le correctif, cette assertion passe
    // aussi (rien n'est jamais écrit), mais celle du bloc suivant échoue —
    // c'est elle qui distingue « pas encore » de « jamais ».
    expect(ajouterAuJournal).not.toHaveBeenCalled()

    const suivant = { ...avant, render_id: 2, manuel_refus: '' } as World
    await act(async () => {
      rerender(<Harness world={suivant} ajouterAuJournal={ajouterAuJournal} />)
    })
    expect(ajouterAuJournal).toHaveBeenCalledTimes(1)
    expect(ajouterAuJournal).toHaveBeenCalledWith('Incliner — Rhino')
  })

  it('marque la ligne quand le moteur refuse, exactement comme en mode manuel', async () => {
    const ajouterAuJournal = vi.fn()
    const avant = mondeSandbox()
    const { getByText, rerender } = render(<Harness world={avant} ajouterAuJournal={ajouterAuJournal} />)

    ouvrirMenuSur(VILAIN.id)
    fireEvent.click(getByText('Incliner'))
    await attendreLeReseau()

    const suivant = {
      ...avant,
      render_id: 2,
      manuel_refus: "KeyError: 'zone inconnue : X'",
    } as World
    await act(async () => {
      rerender(<Harness world={suivant} ajouterAuJournal={ajouterAuJournal} />)
    })
    expect(ajouterAuJournal).toHaveBeenCalledTimes(1)
    expect(ajouterAuJournal).toHaveBeenCalledWith('Incliner — Rhino (refusé)')
  })
})
