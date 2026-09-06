// Le cartouche du deroule : une etape a la fois, validee avant la suivante.
//
// Il est FIXE en bas au centre et ne bouge jamais : l'oeil sait ou lire et la
// main ou cliquer des le deuxieme tour. On peut revenir en arriere pour relire,
// ce qui ne rejoue rien dans la partie : c'est une relecture, pas un undo.
import { describe, expect, it, vi } from 'vitest'
import { act, fireEvent, render, screen } from '@testing-library/react'
import { DeroulePhase } from './DeroulePhase'
import type { EtapeDeroule } from './deroule-phase'

const etapes: EtapeDeroule[] = [
  { cle: 'a', temps: 'menace', titre: 'menace', regle: 'regle:menace', boosts: [], consequences: [] },
  {
    cle: 'b',
    temps: 'activations',
    titre: 'attaque',
    regle: 'regle:activations',
    carteId: 50,
    cibleId: 12,
    auteurNom: 'Ultron',
    cibleNom: 'Shuri',
    boosts: [],
    consequences: [],
  },
]

const suivant = () => screen.getByRole('button', { name: /Suivant/i })

describe('cartouche du deroule', () => {
  it('montre la premiere etape et rien d autre', () => {
    render(<DeroulePhase etapes={etapes} onTerminer={() => {}} />)
    expect(screen.getByText('Menace sur la manigance principale')).toBeInTheDocument()
    expect(screen.queryByText('Ultron attaque Shuri')).not.toBeInTheDocument()
  })

  it('avance d une etape au clic sur Suivant', () => {
    render(<DeroulePhase etapes={etapes} onTerminer={() => {}} />)
    fireEvent.click(suivant())
    expect(screen.getByText('Ultron attaque Shuri')).toBeInTheDocument()
  })

  it('rappelle la regle de l etape courante', () => {
    render(<DeroulePhase etapes={etapes} onTerminer={() => {}} />)
    expect(screen.getByText(/Point 1/)).toBeInTheDocument()
  })

  it('revient en arriere sans rien rejouer', () => {
    render(<DeroulePhase etapes={etapes} onTerminer={() => {}} />)
    fireEvent.click(suivant())
    fireEvent.click(screen.getByRole('button', { name: /Précédent/i }))
    expect(screen.getByText('Menace sur la manigance principale')).toBeInTheDocument()
  })

  it('n offre pas de Precedent sur la premiere etape', () => {
    render(<DeroulePhase etapes={etapes} onTerminer={() => {}} />)
    expect(screen.queryByRole('button', { name: /Précédent/i })).toBeNull()
  })

  it('previent quand la derniere etape est validee', () => {
    const onTerminer = vi.fn()
    render(<DeroulePhase etapes={etapes} onTerminer={onTerminer} />)
    fireEvent.click(suivant())
    fireEvent.click(suivant())
    expect(onTerminer).toHaveBeenCalledTimes(1)
  })

  it('ne rend rien sans etape', () => {
    const { container } = render(<DeroulePhase etapes={[]} onTerminer={() => {}} />)
    expect(container).toBeEmptyDOMElement()
  })

  it('disparait une fois la derniere etape validee', () => {
    // Defaut constate en partie reelle : onTerminer ne suffit pas a faire
    // disparaitre le cartouche si l'appelant n'en fait rien (board.tsx passe
    // un no-op). Le composant doit se masquer lui-meme.
    const { container } = render(<DeroulePhase etapes={etapes} onTerminer={() => {}} />)
    fireEvent.click(suivant())
    fireEvent.click(suivant())
    expect(container).toBeEmptyDOMElement()
  })

  it('reapparait sur sa premiere etape a la phase suivante', () => {
    // Le piege symetrique et pire : si « termine » ne se reinitialise pas
    // quand une nouvelle liste d'etapes arrive, le deroule ne reapparaitrait
    // plus jamais pour aucune phase du mechant suivante.
    const { container, rerender } = render(
      <DeroulePhase etapes={etapes} onTerminer={() => {}} />
    )
    fireEvent.click(suivant())
    fireEvent.click(suivant())
    expect(container).toBeEmptyDOMElement()

    const etapesSuivantes: EtapeDeroule[] = [
      { cle: 'x', temps: 'menace', titre: 'menace', regle: 'regle:menace', boosts: [], consequences: [] },
    ]
    rerender(<DeroulePhase etapes={etapesSuivantes} onTerminer={() => {}} />)
    expect(screen.getByText('Menace sur la manigance principale')).toBeInTheDocument()
  })

  it('ne revient pas a la premiere etape quand le tableau est juste RECREE', () => {
    // board.tsx recalcule `etapes` a chaque trame du moteur (useMemo dont une
    // dependance change d'identite en permanence). Un tableau de MEME CONTENU
    // mais de nouvelle identite ne doit ni faire reculer l'etape courante, ni
    // rouvrir un cartouche deja termine : sinon il se rouvre au round suivant,
    // pendant le tour du joueur, par-dessus le bouton de fin de tour.
    const { rerender } = render(<DeroulePhase etapes={etapes} onTerminer={() => {}} />)
    fireEvent.click(suivant())
    expect(screen.getByText('Ultron attaque Shuri')).toBeInTheDocument()

    // Meme contenu, nouvelle identite de tableau ET des objets qu'il contient.
    const memeContenuIdentiteNeuve: EtapeDeroule[] = etapes.map((e) => ({ ...e }))
    rerender(<DeroulePhase etapes={memeContenuIdentiteNeuve} onTerminer={() => {}} />)
    expect(screen.getByText('Ultron attaque Shuri')).toBeInTheDocument()
    expect(screen.queryByText('Menace sur la manigance principale')).not.toBeInTheDocument()
  })

  it('ne rouvre pas un cartouche deja termine quand le tableau est juste RECREE', () => {
    const { container, rerender } = render(
      <DeroulePhase etapes={etapes} onTerminer={() => {}} />
    )
    fireEvent.click(suivant())
    fireEvent.click(suivant())
    expect(container).toBeEmptyDOMElement()

    const memeContenuIdentiteNeuve: EtapeDeroule[] = etapes.map((e) => ({ ...e }))
    rerender(<DeroulePhase etapes={memeContenuIdentiteNeuve} onTerminer={() => {}} />)
    expect(container).toBeEmptyDOMElement()
  })

  it('montre les quatre temps, celui en cours mis en avant', () => {
    const { container } = render(<DeroulePhase etapes={etapes} onTerminer={() => {}} />)
    expect(container.querySelectorAll('.deroule-temps li')).toHaveLength(4)
    expect(container.querySelector('.deroule-temps li.est-courant')?.textContent).toMatch(/Menace/i)
  })

  it('avance a la touche Entree', () => {
    // fireEvent (et non document.dispatchEvent) : setIndex declenche un
    // rendu, et fireEvent l'enveloppe dans un act() pour eviter
    // l'avertissement React sur une mise a jour hors act().
    render(<DeroulePhase etapes={etapes} onTerminer={() => {}} />)
    fireEvent.keyDown(document, { key: 'Enter' })
    expect(screen.getByText('Ultron attaque Shuri')).toBeInTheDocument()
  })

  it('avance aussi a la barre d espace', () => {
    render(<DeroulePhase etapes={etapes} onTerminer={() => {}} />)
    fireEvent.keyDown(document, { key: ' ' })
    expect(screen.getByText('Ultron attaque Shuri')).toBeInTheDocument()
  })

  it('deroule tout a la touche Echap', () => {
    const onToutDerouler = vi.fn()
    render(
      <DeroulePhase etapes={etapes} onTerminer={() => {}} onToutDerouler={onToutDerouler} />
    )
    document.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape', bubbles: true }))
    expect(onToutDerouler).toHaveBeenCalledTimes(1)
  })

  it('supporte de passer de zero etape a plusieurs sans tomber', () => {
    // Le plateau monte ce composant des que le mode « detaille » est actif,
    // donc hors phase du mechant, avec une liste vide. Si le `return null`
    // court-circuite un hook, React compte un hook de plus au rendu suivant
    // et fait tomber tout le plateau.
    const { rerender } = render(<DeroulePhase etapes={[]} onTerminer={() => {}} />)
    rerender(<DeroulePhase etapes={etapes} onTerminer={() => {}} />)
    expect(screen.getByText('Menace sur la manigance principale')).toBeInTheDocument()
  })

  it('laisse le clavier tranquille quand on ecrit ailleurs', () => {
    // Le tchat est a portee de main pendant la phase : taper un espace dans son
    // champ ne doit pas faire avancer la phase du mechant.
    render(<DeroulePhase etapes={etapes} onTerminer={() => {}} />)
    const champ = document.createElement('input')
    document.body.append(champ)
    champ.focus()
    champ.dispatchEvent(new KeyboardEvent('keydown', { key: ' ', bubbles: true }))
    expect(screen.getByText('Menace sur la manigance principale')).toBeInTheDocument()
    champ.remove()
  })

  it('laisse un bouton du plateau reagir a Entree, sans avancer la phase', () => {
    // L'ecouteur excluait bien les champs de saisie, mais faisait
    // preventDefault() sur TOUTE autre cible : Entree ou Espace sur n'importe
    // quel bouton du plateau (hors cartouche) avancait la phase au lieu
    // d'activer ce bouton.
    render(<DeroulePhase etapes={etapes} onTerminer={() => {}} />)
    const autreBouton = document.createElement('button')
    document.body.append(autreBouton)
    // fireEvent (et non document.dispatchEvent) : voir la remarque plus haut
    // sur l'avance a la touche Entree, meme raison.
    fireEvent.keyDown(autreBouton, { key: 'Enter' })
    expect(screen.getByText('Menace sur la manigance principale')).toBeInTheDocument()
    expect(screen.queryByText('Ultron attaque Shuri')).not.toBeInTheDocument()
    autreBouton.remove()
  })

  it('avance quand meme au clavier depuis le bouton Suivant du cartouche', () => {
    // Le bouton Suivant est un bouton comme un autre, mais IL EST le
    // cartouche : la restriction ci-dessus ne doit pas le neutraliser.
    render(<DeroulePhase etapes={etapes} onTerminer={() => {}} />)
    fireEvent.keyDown(suivant(), { key: 'Enter' })
    expect(screen.getByText('Ultron attaque Shuri')).toBeInTheDocument()
  })

  it('affiche les consequences de l etape, pas seulement le titre et la regle', () => {
    // deroule-phase.ts construit bien `consequences` (« +1 pour Shuri, +1 pour
    // Thor ») mais le composant ne rendait que le titre, la regle et le brut :
    // la donnee etait calculee puis jetee.
    const avecConsequences: EtapeDeroule[] = [
      {
        cle: 'a',
        temps: 'menace',
        titre: 'menace',
        regle: 'regle:menace',
        boosts: [],
        consequences: [
          { cle: 'c1', texte: '+1 pour Shuri' },
          { cle: 'c2', texte: '+1 pour Thor' },
        ],
      },
    ]
    render(<DeroulePhase etapes={avecConsequences} onTerminer={() => {}} />)
    expect(screen.getByText('+1 pour Shuri')).toBeInTheDocument()
    expect(screen.getByText('+1 pour Thor')).toBeInTheDocument()
  })

  it('n affiche rien de plus quand l etape n a pas de consequence', () => {
    render(<DeroulePhase etapes={etapes} onTerminer={() => {}} />)
    expect(document.querySelector('.deroule-consequences')).toBeNull()
  })

  it('enchaine seule une etape technique', async () => {
    // Le charabia du moteur se voit passer, il ne se clique pas.
    const avecAuto: EtapeDeroule[] = [
      { cle: 'a', temps: 'revelation', titre: 'Rage of Ultron were discarded', regle: '', boosts: [], consequences: [], auto: true },
      { cle: 'b', temps: 'revelation', titre: 'Fin', regle: '', boosts: [], consequences: [] },
    ]
    vi.useFakeTimers()
    try {
      render(<DeroulePhase etapes={avecAuto} onTerminer={() => {}} />)
      expect(screen.getByText('Rage of Ultron were discarded')).toBeInTheDocument()
      // act() : le setState declenche par le minuteur (un setTimeout natif,
      // hors evenement React) n'est sinon pas garanti applique avant l'assertion.
      await act(async () => {
        await vi.advanceTimersByTimeAsync(600)
      })
      expect(screen.getByText('Fin')).toBeInTheDocument()
    } finally {
      vi.useRealTimers()
    }
  })

  it('n enchaine PAS une etape ordinaire', async () => {
    vi.useFakeTimers()
    try {
      render(<DeroulePhase etapes={etapes} onTerminer={() => {}} />)
      await act(async () => {
        await vi.advanceTimersByTimeAsync(3000)
      })
      expect(screen.getByText('Menace sur la manigance principale')).toBeInTheDocument()
    } finally {
      vi.useRealTimers()
    }
  })

  it('suspend l enchainement des qu on revient en arriere', async () => {
    // Sinon « Precedent » serait inutilisable sur une etape automatique : elle
    // repartirait en avant aussitot.
    const suite: EtapeDeroule[] = [
      { cle: 'a', temps: 'menace', titre: 'menace', regle: 'regle:menace', boosts: [], consequences: [] },
      { cle: 'b', temps: 'revelation', titre: 'technique', regle: '', boosts: [], consequences: [], auto: true },
      { cle: 'c', temps: 'revelation', titre: 'Fin', regle: '', boosts: [], consequences: [] },
    ]
    vi.useFakeTimers()
    try {
      render(<DeroulePhase etapes={suite} onTerminer={() => {}} />)
      fireEvent.click(screen.getByRole('button', { name: /Suivant/i }))
      await act(async () => {
        await vi.advanceTimersByTimeAsync(600)
      })
      expect(screen.getByText('Fin')).toBeInTheDocument()
      fireEvent.click(screen.getByRole('button', { name: /Précédent/i }))
      expect(screen.getByText('technique')).toBeInTheDocument()
      await act(async () => {
        await vi.advanceTimersByTimeAsync(3000)
      })
      expect(screen.getByText('technique')).toBeInTheDocument()
    } finally {
      vi.useRealTimers()
    }
  })
})
