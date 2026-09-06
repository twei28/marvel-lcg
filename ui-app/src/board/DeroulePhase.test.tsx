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
    temps: 'mechant',
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

  it('ferme le cartouche quand la derniere etape est validee au CLAVIER', () => {
    // Depuis le correctif de fermeture, c'est avancer() qui fait disparaitre
    // le cartouche : ce chemin n'etait verifie qu'au clic, jamais au clavier,
    // alors que les deux passent par la meme fonction.
    render(<DeroulePhase etapes={etapes} onTerminer={() => {}} />)
    fireEvent.keyDown(document, { key: 'Enter' })
    fireEvent.keyDown(document, { key: 'Enter' })
    expect(document.querySelector('.deroule-phase')).toBeNull()
  })

  it('reapparait sur sa premiere etape a la phase suivante', () => {
    // Le piege symetrique et pire : si « termine » ne se reinitialise pas
    // quand la phase suivante arrive, le deroule ne reapparaitrait plus jamais
    // pour aucune phase du mechant suivante. C'est desormais l'identite de
    // phase (le round) qui dit « phase suivante », plus le contenu de la liste
    // d'etapes : celle-ci s'allonge aussi au sein d'une meme phase.
    const { container, rerender } = render(
      <DeroulePhase etapes={etapes} identitePhase={1} onTerminer={() => {}} />
    )
    fireEvent.click(suivant())
    fireEvent.click(suivant())
    expect(container).toBeEmptyDOMElement()

    const etapesSuivantes: EtapeDeroule[] = [
      { cle: 'x', temps: 'menace', titre: 'menace', regle: 'regle:menace', boosts: [], consequences: [] },
    ]
    rerender(<DeroulePhase etapes={etapesSuivantes} identitePhase={2} onTerminer={() => {}} />)
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

  it('montre les cinq temps, celui en cours mis en avant', () => {
    const { container } = render(<DeroulePhase etapes={etapes} onTerminer={() => {}} />)
    expect(container.querySelectorAll('.deroule-temps li')).toHaveLength(5)
    expect(container.querySelector('.deroule-temps li.est-courant')?.textContent).toMatch(/Menace/i)
  })

  it('marque comme passe un temps deja valide', () => {
    // `etapes` : menace puis mechant. Une fois la menace validee, elle doit
    // porter la marque de validation, pas rester « a venir ».
    render(<DeroulePhase etapes={etapes} onTerminer={() => {}} />)
    fireEvent.click(suivant())
    const menaceLi = [...document.querySelectorAll('.deroule-temps li')].find((li) =>
      li.textContent?.match(/Menace/i)
    )
    expect(menaceLi?.className).toContain('est-passe')
  })

  it('marque un temps sans aucune etape comme vide dans la chronologie', () => {
    // `etapes` ne porte que menace et mechant : sbires, distribution et
    // revelation n'ont produit aucune etape cette phase-ci.
    const { container } = render(<DeroulePhase etapes={etapes} onTerminer={() => {}} />)
    const sbiresLi = [...container.querySelectorAll('.deroule-temps li')].find((li) =>
      li.textContent?.match(/Sbires/i)
    )
    expect(sbiresLi?.className).toContain('est-vide')
    expect(sbiresLi?.textContent).toMatch(/Aucun/i)
  })

  it('ne coute aucun clic pour un temps vide : le compte de clics suit le nombre d etapes', () => {
    // La phase brute (voir brief) : menace, mechant, distribution ; ni
    // sbires, ni revelation ne produisent d'etape ici. Le joueur doit
    // traverser la phase en exactement 3 clics, pas 5 : un temps vide ne
    // consomme jamais de clic pour lui-meme.
    const onTerminer = vi.fn()
    const sansSbiresNiRevelation: EtapeDeroule[] = [
      { cle: 'a', temps: 'menace', titre: 'menace', regle: 'regle:menace', boosts: [], consequences: [] },
      { cle: 'b', temps: 'mechant', titre: 'attaque', regle: 'regle:activations', boosts: [], consequences: [] },
      { cle: 'c', temps: 'distribution', titre: 'distribution', regle: '', boosts: [], consequences: [] },
    ]
    render(<DeroulePhase etapes={sansSbiresNiRevelation} onTerminer={onTerminer} />)
    fireEvent.click(suivant())
    fireEvent.click(suivant())
    expect(onTerminer).not.toHaveBeenCalled()
    fireEvent.click(suivant())
    expect(onTerminer).toHaveBeenCalledTimes(1)
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

  it('enchaine quand meme une etape technique si l objet etape est RECREE avant l echeance', async () => {
    // board.tsx recalcule `etapes` (donc l'objet `etape`) a chaque trame du
    // moteur, meme quand rien n'a change. Mesure en partie reelle : la phase
    // du mechant peut emettre des trames plus vite que les 500ms du minuteur
    // (52 entrees de journal en 750ms). Si l'effet depend de l'IDENTITE de
    // `etape`, chaque trame annule le minuteur en cours et en repose un
    // nouveau : l'etape technique n'a alors plus jamais le temps de defiler
    // seule.
    const avecAuto: EtapeDeroule[] = [
      { cle: 'a', temps: 'revelation', titre: 'technique', regle: '', boosts: [], consequences: [], auto: true },
      { cle: 'b', temps: 'revelation', titre: 'Fin', regle: '', boosts: [], consequences: [] },
    ]
    vi.useFakeTimers()
    try {
      const { rerender } = render(<DeroulePhase etapes={avecAuto} onTerminer={() => {}} />)
      await act(async () => {
        await vi.advanceTimersByTimeAsync(300)
      })
      // Meme contenu, mais nouvelle identite de tableau ET de l'objet `etape`
      // en cours : exactement ce que produit board.tsx a chaque trame.
      const memeContenuIdentiteNeuve: EtapeDeroule[] = avecAuto.map((e) => ({ ...e }))
      rerender(<DeroulePhase etapes={memeContenuIdentiteNeuve} onTerminer={() => {}} />)
      await act(async () => {
        await vi.advanceTimersByTimeAsync(300)
      })
      // 600ms se sont ecoulees depuis le premier rendu, largement plus que
      // les 500ms du minuteur : l'etape technique doit avoir defile seule.
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

  it('ne laisse pas un Precedent de la phase precedente suspendre la phase suivante', async () => {
    // Le joueur clique « Precedent » (donc `suspendu` passe a vrai), puis ne
    // reclique plus « Suivant » : la phase se termine autrement (le moteur
    // avance de lui-meme). A la phase du mechant suivante, `suspendu` doit
    // etre remis a zero comme `index` et `termine`, sinon sa premiere etape
    // technique n'attend plus le clic qu'elle est censee eviter.
    const premierePhase: EtapeDeroule[] = [
      { cle: 'a1', temps: 'menace', titre: 'menace', regle: 'regle:menace', boosts: [], consequences: [] },
      { cle: 'a2', temps: 'mechant', titre: 'attaque', regle: 'regle:activations', boosts: [], consequences: [] },
    ]
    const deuxiemePhase: EtapeDeroule[] = [
      { cle: 'b1', temps: 'revelation', titre: 'technique', regle: '', boosts: [], consequences: [], auto: true },
      { cle: 'b2', temps: 'revelation', titre: 'Fin', regle: '', boosts: [], consequences: [] },
    ]
    vi.useFakeTimers()
    try {
      const { rerender } = render(
        <DeroulePhase etapes={premierePhase} identitePhase={1} onTerminer={() => {}} />
      )
      fireEvent.click(suivant())
      fireEvent.click(screen.getByRole('button', { name: /Précédent/i }))
      // La phase se termine ici sans reclic sur « Suivant » (le moteur passe
      // seul a la phase suivante) : c'est le round qui change, et lui seul.
      rerender(<DeroulePhase etapes={deuxiemePhase} identitePhase={2} onTerminer={() => {}} />)
      expect(screen.getByText('technique')).toBeInTheDocument()
      await act(async () => {
        await vi.advanceTimersByTimeAsync(600)
      })
      expect(screen.getByText('Fin')).toBeInTheDocument()
    } finally {
      vi.useRealTimers()
    }
  })

  it('retourne les boosts un par un', async () => {
    // Le moment de tension du jeu : chaque carte se lit avant la suivante.
    const avecBoosts: EtapeDeroule[] = [
      {
        cle: 'a',
        temps: 'mechant',
        titre: 'attaque',
        regle: 'regle:activations',
        carteId: 50,
        cibleId: 12,
        auteurNom: 'Ultron',
        cibleNom: 'Shuri',
        boosts: [
          { cle: 'b0', nom: 'Boost A', cibleId: 91, apport: 1 },
          { cle: 'b1', nom: 'Boost B', cibleId: 92, apport: 2 },
        ],
        consequences: [],
      },
    ]
    vi.useFakeTimers()
    try {
      render(<DeroulePhase etapes={avecBoosts} onTerminer={() => {}} />)
      expect(screen.getByText('Boost A')).toBeInTheDocument()
      expect(screen.queryByText('Boost B')).not.toBeInTheDocument()
      await act(async () => {
        await vi.advanceTimersByTimeAsync(1600)
      })
      expect(screen.getByText('Boost B')).toBeInTheDocument()
    } finally {
      vi.useRealTimers()
    }
  })

  it('n attend pas de clic pour les boosts : c est l etape qui attend', () => {
    const avecBoosts: EtapeDeroule[] = [
      {
        cle: 'a',
        temps: 'mechant',
        titre: 'attaque',
        regle: 'regle:activations',
        carteId: 50,
        boosts: [{ cle: 'b0', nom: 'Boost A', cibleId: 91, apport: 1 }],
        consequences: [],
      },
    ]
    render(<DeroulePhase etapes={avecBoosts} onTerminer={() => {}} />)
    expect(screen.getByRole('button', { name: /Suivant/i })).toBeInTheDocument()
  })

  it('n affiche aucun bloc de boost quand il n y en a pas', () => {
    const { container } = render(<DeroulePhase etapes={etapes} onTerminer={() => {}} />)
    expect(container.querySelector('.deroule-boosts')).toBeNull()
  })

  // Defaut 1 (voir brief) : rien ne reliait le bouton « Suivant » au moteur.
  // onSuivant est la porte que board.tsx doit brancher sur
  // moteur.avancerMaintenant() ; ces tests verifient le cote DeroulePhase de
  // ce branchement (qu'il est bien appele, au bon moment), pas ce que
  // board.tsx en fait reellement une fois cable (voir le rapport a ce sujet).
  it('appelle onSuivant une fois par clic sur Suivant, et avance', () => {
    const onSuivant = vi.fn()
    render(<DeroulePhase etapes={etapes} onSuivant={onSuivant} onTerminer={() => {}} />)
    fireEvent.click(suivant())
    expect(onSuivant).toHaveBeenCalledTimes(1)
    expect(screen.getByText('Ultron attaque Shuri')).toBeInTheDocument()
  })

  it('appelle onTerminer quand la derniere etape est validee', () => {
    const onSuivant = vi.fn()
    const onTerminer = vi.fn()
    render(<DeroulePhase etapes={etapes} onSuivant={onSuivant} onTerminer={onTerminer} />)
    fireEvent.click(suivant())
    fireEvent.click(suivant())
    expect(onTerminer).toHaveBeenCalledTimes(1)
    // onSuivant est appele a CHAQUE validation, la derniere y compris : c'est
    // ce qui permet a board.tsx de brancher onSuivant et onTerminer sur la
    // meme fonction (avancerMaintenant ne fait rien sans trame en attente,
    // l'appel surnumeraire de la derniere etape est donc sans effet).
    expect(onSuivant).toHaveBeenCalledTimes(2)
  })

  it('onSuivant absent ne casse rien : la prop est optionnelle', () => {
    render(<DeroulePhase etapes={etapes} onTerminer={() => {}} />)
    expect(() => fireEvent.click(suivant())).not.toThrow()
    expect(screen.getByText('Ultron attaque Shuri')).toBeInTheDocument()
  })
  // Defaut 2 (voir brief) : « arriver au bout des etapes CONNUES » n'est pas
  // « la phase est finie ». Depuis que chaque « Suivant » relache une trame du
  // moteur, la liste s'allonge PENDANT la phase : le cartouche doit attendre
  // la suite au lieu de se croire au bout, et la remise a zero doit suivre
  // l'identite de la phase (le round), jamais la longueur de la liste.
  const menaceSeule: EtapeDeroule[] = [
    { cle: 'a', temps: 'menace', titre: 'menace', regle: 'regle:menace', boosts: [], consequences: [] },
  ]

  it('attend la suite au lieu de se croire fini quand la liste s allonge', () => {
    // Le cas central. Une seule etape connue au depart (la menace), le joueur
    // valide, le moteur relache la premiere activation : le cartouche doit
    // afficher cette activation, sans jamais avoir dit que la phase etait
    // finie.
    const onTerminer = vi.fn()
    const { rerender } = render(
      <DeroulePhase
        etapes={menaceSeule}
        identitePhase={3}
        phaseMechantEnCours
        onTerminer={onTerminer}
      />
    )
    fireEvent.click(suivant())
    expect(onTerminer).not.toHaveBeenCalled()

    rerender(
      <DeroulePhase
        etapes={etapes}
        identitePhase={3}
        phaseMechantEnCours
        onTerminer={onTerminer}
      />
    )
    expect(screen.getByText('Ultron attaque Shuri')).toBeInTheDocument()
    expect(screen.queryByText('Menace sur la manigance principale')).not.toBeInTheDocument()
    expect(onTerminer).not.toHaveBeenCalled()
  })

  it('termine bien quand la phase du mechant est terminee', () => {
    // Meme situation, mais le moteur a quitte la phase du mechant : il n'y a
    // plus rien a attendre, la derniere etape connue est vraiment la derniere.
    const onTerminer = vi.fn()
    const { container } = render(
      <DeroulePhase
        etapes={menaceSeule}
        identitePhase={3}
        phaseMechantEnCours={false}
        onTerminer={onTerminer}
      />
    )
    fireEvent.click(suivant())
    expect(onTerminer).toHaveBeenCalledTimes(1)
    expect(container).toBeEmptyDOMElement()
  })

  it('se referme si la phase du mechant se termine pendant l attente', () => {
    // Le joueur valide la derniere etape alors que la phase court encore : le
    // cartouche attend. Si le moteur passe au tour du joueur sans rien
    // produire de plus, l'attente ne doit pas laisser le cartouche affiche
    // par-dessus le plateau pour le reste du tour.
    const onTerminer = vi.fn()
    const { container, rerender } = render(
      <DeroulePhase
        etapes={menaceSeule}
        identitePhase={3}
        phaseMechantEnCours
        onTerminer={onTerminer}
      />
    )
    fireEvent.click(suivant())
    expect(container).not.toBeEmptyDOMElement()

    rerender(
      <DeroulePhase
        etapes={menaceSeule}
        identitePhase={3}
        phaseMechantEnCours={false}
        onTerminer={onTerminer}
      />
    )
    expect(onTerminer).toHaveBeenCalledTimes(1)
    expect(container).toBeEmptyDOMElement()
  })

  it('repart de la premiere etape au round suivant', () => {
    // La remise a zero suit l'identite de la phase, et elle seule.
    const { rerender } = render(
      <DeroulePhase etapes={etapes} identitePhase={3} phaseMechantEnCours onTerminer={() => {}} />
    )
    fireEvent.click(suivant())
    expect(screen.getByText('Ultron attaque Shuri')).toBeInTheDocument()

    const roundSuivant: EtapeDeroule[] = [
      { cle: 'z1', temps: 'menace', titre: 'menace', regle: 'regle:menace', boosts: [], consequences: [] },
      { cle: 'z2', temps: 'mechant', titre: 'attaque', regle: 'regle:activations', boosts: [], consequences: [] },
    ]
    rerender(
      <DeroulePhase
        etapes={roundSuivant}
        identitePhase={4}
        phaseMechantEnCours
        onTerminer={() => {}}
      />
    )
    expect(screen.getByText('Menace sur la manigance principale')).toBeInTheDocument()
  })

  it('ne revient pas a la premiere etape quand la liste s allonge dans le meme round', () => {
    // Le defaut d'origine : la liste qui grossit pendant la phase faisait
    // repartir le cartouche au debut, et le joueur relisait en boucle des
    // etapes deja validees.
    const { rerender } = render(
      <DeroulePhase etapes={etapes} identitePhase={3} phaseMechantEnCours onTerminer={() => {}} />
    )
    fireEvent.click(suivant())
    expect(screen.getByText('Ultron attaque Shuri')).toBeInTheDocument()

    const plusLongue: EtapeDeroule[] = [
      ...etapes,
      { cle: 'c', temps: 'distribution', titre: 'distribution', regle: '', boosts: [], consequences: [] },
    ]
    rerender(
      <DeroulePhase
        etapes={plusLongue}
        identitePhase={3}
        phaseMechantEnCours
        onTerminer={() => {}}
      />
    )
    expect(screen.getByText('Ultron attaque Shuri')).toBeInTheDocument()
    expect(screen.queryByText('Menace sur la manigance principale')).not.toBeInTheDocument()
  })

  it('relache le moteur meme sur le clic qui met en attente', () => {
    // Sans cet appel, le clic qui met en attente ne relacherait aucune trame :
    // le moteur ne produirait jamais l'etape attendue, et l'attente serait
    // sans fin.
    const onSuivant = vi.fn()
    render(
      <DeroulePhase
        etapes={menaceSeule}
        identitePhase={3}
        phaseMechantEnCours
        onSuivant={onSuivant}
        onTerminer={() => {}}
      />
    )
    fireEvent.click(suivant())
    expect(onSuivant).toHaveBeenCalledTimes(1)
  })

  it('dit qu il attend la suite, sans bloquer le bouton', () => {
    render(
      <DeroulePhase
        etapes={menaceSeule}
        identitePhase={3}
        phaseMechantEnCours
        onTerminer={() => {}}
      />
    )
    expect(document.querySelector('.deroule-attente')).toBeNull()
    fireEvent.click(suivant())
    expect(document.querySelector('.deroule-attente')).not.toBeNull()
    expect(screen.getByRole('button', { name: /Suivant/i })).toBeInTheDocument()
  })
  it('laisse relire en arriere pendant l attente', () => {
    // « Precedent » RELIT : il doit rester utilisable meme quand le cartouche
    // attend la suite, sinon la sortie d'attente le repousserait aussitot en
    // avant et le bouton serait mort a l'ecran.
    render(
      <DeroulePhase etapes={etapes} identitePhase={3} phaseMechantEnCours onTerminer={() => {}} />
    )
    fireEvent.click(suivant())
    fireEvent.click(suivant())
    fireEvent.click(screen.getByRole('button', { name: /Précédent/i }))
    expect(screen.getByText('Menace sur la manigance principale')).toBeInTheDocument()
    expect(screen.queryByText('Ultron attaque Shuri')).not.toBeInTheDocument()
  })
})
