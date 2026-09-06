// Le cartouche du deroule : une etape a la fois, validee avant la suivante.
//
// Il est FIXE en bas au centre et ne bouge jamais : l'oeil sait ou lire et la
// main ou cliquer des le deuxieme tour. On peut revenir en arriere pour relire,
// ce qui ne rejoue rien dans la partie : c'est une relecture, pas un undo.
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { act, fireEvent, render, screen } from '@testing-library/react'
import { DeroulePhase } from './DeroulePhase'
import type { EtapeDeroule } from './deroule-phase'
import { CLE_REGLE_DEPLIEE } from './moteur'

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
// Le bouton de la DERNIERE etape, celle du bilan : il ne dit plus « Suivant »
// et c'est lui qui rend la main au joueur.
const aToiDeJouer = () => screen.getByRole('button', { name: /À toi de jouer/i })

describe('cartouche du deroule', () => {
  // Le depliant de la regle lit et ecrit son reglage dans localStorage
  // (lireRegleDepliee/ecrireRegleDepliee, moteur.ts) : chaque test repart
  // d'un stockage vide, sinon un reglage ecrit par un test en polluerait un
  // autre.
  beforeEach(() => {
    window.localStorage.clear()
  })

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
    // La derniere etape est desormais le BILAN, ajoute parce que la phase du
    // mechant est terminee (phaseMechantEnCours par defaut a false) : c'est son
    // bouton qui previent.
    const onTerminer = vi.fn()
    render(<DeroulePhase etapes={etapes} onTerminer={onTerminer} />)
    fireEvent.click(suivant())
    fireEvent.click(suivant())
    expect(onTerminer).not.toHaveBeenCalled()
    fireEvent.click(aToiDeJouer())
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
    fireEvent.click(aToiDeJouer())
    expect(container).toBeEmptyDOMElement()
  })

  it('ferme le cartouche quand la derniere etape est validee au CLAVIER', () => {
    // Depuis le correctif de fermeture, c'est avancer() qui fait disparaitre
    // le cartouche : ce chemin n'etait verifie qu'au clic, jamais au clavier,
    // alors que les deux passent par la meme fonction.
    render(<DeroulePhase etapes={etapes} onTerminer={() => {}} />)
    fireEvent.keyDown(document, { key: 'Enter' })
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
    fireEvent.click(aToiDeJouer())
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
    fireEvent.click(aToiDeJouer())
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
    // consomme jamais de clic pour lui-meme. Le bilan de fin de phase en
    // ajoute un quatrieme, et un seul, quel que soit le nombre de temps vides.
    const onTerminer = vi.fn()
    const sansSbiresNiRevelation: EtapeDeroule[] = [
      { cle: 'a', temps: 'menace', titre: 'menace', regle: 'regle:menace', boosts: [], consequences: [] },
      { cle: 'b', temps: 'mechant', titre: 'attaque', regle: 'regle:activations', boosts: [], consequences: [] },
      { cle: 'c', temps: 'distribution', titre: 'distribution', regle: '', boosts: [], consequences: [] },
    ]
    render(<DeroulePhase etapes={sansSbiresNiRevelation} onTerminer={onTerminer} />)
    fireEvent.click(suivant())
    fireEvent.click(suivant())
    fireEvent.click(suivant())
    expect(onTerminer).not.toHaveBeenCalled()
    fireEvent.click(aToiDeJouer())
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
    // Thor ») mais le composant ne rendait que le titre et la regle : la
    // donnee etait calculee puis jetee.
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

  it('affiche le chiffre du coup et le compteur de la cible', () => {
    // Une seule phrase concrete, son chiffre en dessous et le compteur de la
    // cible a droite : le titre generique disait moins que la ligne qu'il
    // surplombait.
    const attaque: EtapeDeroule[] = [
      {
        cle: 'a',
        temps: 'mechant',
        titre: 'attaque',
        regle: 'regle:activations',
        auteurNom: 'Klaw',
        cibleNom: 'Colossus',
        montant: 4,
        restant: 5,
        boosts: [],
        consequences: [],
      },
    ]
    render(<DeroulePhase etapes={attaque} onTerminer={() => {}} />)
    expect(screen.getByText('Klaw attaque Colossus')).toBeInTheDocument()
    expect(screen.getByText('→ 4 dégâts')).toBeInTheDocument()
    expect(screen.getByText('5')).toBeInTheDocument()
  })

  it('n affiche aucun compteur quand le fait n en porte pas', () => {
    // Un compteur faux serait pire que pas de compteur.
    const sansRestant: EtapeDeroule[] = [
      {
        cle: 'a',
        temps: 'mechant',
        titre: 'attaque',
        regle: 'regle:activations',
        auteurNom: 'Klaw',
        cibleNom: 'Colossus',
        montant: 4,
        boosts: [],
        consequences: [],
      },
    ]
    render(<DeroulePhase etapes={sansRestant} onTerminer={() => {}} />)
    expect(document.querySelector('.deroule-compteur')).toBeNull()
    expect(document.body.textContent ?? '').not.toMatch(/undefined|NaN/)
  })

  it('dit combien d etapes compte le temps courant', () => {
    const deuxSbires: EtapeDeroule[] = [
      { cle: 'a', temps: 'sbires', titre: 'attaque', regle: 'regle:activations', auteurNom: 'Drone', cibleNom: 'Shuri', boosts: [], consequences: [] },
      { cle: 'b', temps: 'sbires', titre: 'attaque', regle: 'regle:activations', auteurNom: 'Drone', cibleNom: 'Thor', boosts: [], consequences: [] },
    ]
    render(<DeroulePhase etapes={deuxSbires} onTerminer={() => {}} />)
    expect(screen.getByText('1 sur 2')).toBeInTheDocument()
    fireEvent.click(suivant())
    expect(screen.getByText('2 sur 2')).toBeInTheDocument()
  })

  it('n encombre pas le cartouche quand le temps n a qu une etape', () => {
    render(<DeroulePhase etapes={etapes} onTerminer={() => {}} />)
    expect(document.querySelector('.deroule-rang')).toBeNull()
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
    fireEvent.click(aToiDeJouer())
    expect(onTerminer).toHaveBeenCalledTimes(1)
    // onSuivant est appele a CHAQUE validation, la derniere y compris : c'est
    // ce qui permet a board.tsx de brancher onSuivant et onTerminer sur la
    // meme fonction (avancerMaintenant ne fait rien sans trame en attente,
    // l'appel surnumeraire de la derniere etape est donc sans effet).
    expect(onSuivant).toHaveBeenCalledTimes(3)
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
    // plus rien a attendre, et le bilan de fin de phase clot le cartouche.
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
    expect(screen.getByText('Fin de la phase du méchant')).toBeInTheDocument()
    fireEvent.click(aToiDeJouer())
    expect(onTerminer).toHaveBeenCalledTimes(1)
    expect(container).toBeEmptyDOMElement()
  })

  it('sort de l attente sur le bilan quand la phase du mechant se termine', () => {
    // Le joueur valide la derniere etape alors que la phase court encore : le
    // cartouche attend. Quand le moteur passe au tour du joueur, l'attente ne
    // doit pas laisser le cartouche affiche indefiniment : la fin de phase fait
    // apparaitre le bilan, sur lequel le cartouche avance tout seul, et c'est
    // ce bilan qui le referme.
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
    expect(screen.getByText('Fin de la phase du méchant')).toBeInTheDocument()
    expect(document.querySelector('.deroule-attente')).toBeNull()
    expect(onTerminer).not.toHaveBeenCalled()

    fireEvent.click(aToiDeJouer())
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

  describe('depliant de la regle', () => {
    const regle = () => screen.getByRole('button', { name: /la règle/i })

    it('montre la regle par defaut, sans rien avoir stocke', () => {
      render(<DeroulePhase etapes={etapes} onTerminer={() => {}} />)
      expect(screen.getByText(/Point 1/)).toBeInTheDocument()
      expect(regle()).toHaveAttribute('aria-expanded', 'true')
    })

    it('un clic la replie et ecrit le reglage dans le stockage', () => {
      render(<DeroulePhase etapes={etapes} onTerminer={() => {}} />)
      fireEvent.click(regle())
      expect(screen.queryByText(/Point 1/)).not.toBeInTheDocument()
      expect(regle()).toHaveAttribute('aria-expanded', 'false')
      expect(window.localStorage.getItem(CLE_REGLE_DEPLIEE)).toBe('off')
    })

    it('reste repliee au premier rendu quand le reglage est deja stocke replie', () => {
      window.localStorage.setItem(CLE_REGLE_DEPLIEE, 'off')
      render(<DeroulePhase etapes={etapes} onTerminer={() => {}} />)
      expect(screen.queryByText(/Point 1/)).not.toBeInTheDocument()
      expect(regle()).toHaveAttribute('aria-expanded', 'false')
    })

    it('le repli survit au passage a l etape suivante', () => {
      // Le coeur de la decision : un seul rendu ne prouve rien, il faut voir
      // le reglage tenir quand le moteur produit l'etape suivante (meme
      // motif que les tests ci-dessus qui font grossir `etapes` via
      // `rerender`, a identite de phase inchangee).
      const menaceSeule: EtapeDeroule[] = [etapes[0]]
      const { rerender } = render(
        <DeroulePhase etapes={menaceSeule} identitePhase={7} phaseMechantEnCours onTerminer={() => {}} />
      )
      fireEvent.click(regle())
      expect(screen.queryByText(/Point 1/)).not.toBeInTheDocument()

      fireEvent.click(suivant())
      rerender(
        <DeroulePhase etapes={etapes} identitePhase={7} phaseMechantEnCours onTerminer={() => {}} />
      )
      expect(screen.getByText('Ultron attaque Shuri')).toBeInTheDocument()
      expect(screen.queryByText(/Point 2/)).not.toBeInTheDocument()
      expect(regle()).toHaveAttribute('aria-expanded', 'false')
    })

    it('un stockage qui leve ne fait pas tomber le composant', () => {
      const espionLecture = vi.spyOn(window.localStorage, 'getItem').mockImplementation(() => {
        throw new Error('localStorage access denied')
      })
      const espionEcriture = vi.spyOn(window.localStorage, 'setItem').mockImplementation(() => {
        throw new Error('localStorage access denied')
      })
      try {
        render(<DeroulePhase etapes={etapes} onTerminer={() => {}} />)
        // Lecture en echec : repli sur le defaut (depliee).
        expect(screen.getByText(/Point 1/)).toBeInTheDocument()
        expect(() => fireEvent.click(regle())).not.toThrow()
        // Ecriture en echec elle aussi : le clic replie quand meme l'affichage,
        // seul le stockage ne suit pas.
        expect(screen.queryByText(/Point 1/)).not.toBeInTheDocument()
      } finally {
        espionLecture.mockRestore()
        espionEcriture.mockRestore()
      }
    })
  })
})

// Le bilan de fin de phase : la derniere etape, celle ou le joueur lit en deux
// lignes ce qu'il vient d'encaisser avant de decider de son tour.
//
// Il n'existe QUE quand la phase est finie : `phaseMechantEnCours` est la seule
// chose qui distingue proprement une phase en cours d'une phase terminee (voir
// board.tsx, qui la calcule sur `monde.phase`). Un bilan affiche au milieu de la
// phase mentirait sur ce qu'elle a coute.
describe('le bilan de fin de phase', () => {
  beforeEach(() => {
    window.localStorage.clear()
  })

  const coup = (extra: Partial<EtapeDeroule>): EtapeDeroule => ({
    cle: 'k',
    temps: 'sbires',
    titre: 'attaque',
    regle: 'regle:activations',
    auteurNom: 'Drone',
    cibleNom: 'Colossus',
    montant: 3,
    boosts: [],
    consequences: [],
    ...extra,
  })

  const troisCoupsSurColossus: EtapeDeroule[] = [
    coup({ cle: 'v', temps: 'mechant', auteurNom: 'Ultron', montant: 3, restant: 11 }),
    coup({ cle: 's1', montant: 2, restant: 9 }),
    coup({ cle: 's2', montant: 1, restant: 8 }),
  ]

  it('groupe en UNE ligne les coups portes sur le meme heros', () => {
    // Le piege du comptage : trois attaquants, un seul heros touche, une seule
    // ligne avec le total.
    render(<DeroulePhase etapes={troisCoupsSurColossus} onTerminer={() => {}} />)
    fireEvent.click(suivant())
    fireEvent.click(suivant())
    fireEvent.click(suivant())
    expect(screen.getByText('Fin de la phase du méchant')).toBeInTheDocument()
    expect(document.querySelectorAll('.deroule-bilan li')).toHaveLength(1)
    expect(screen.getByText('Colossus a pris 6 dégâts')).toBeInTheDocument()
    // Le compteur de la cible apres le dernier coup, a droite de sa ligne.
    expect(document.querySelector('.deroule-bilan-compteur')?.textContent).toBe('8')
  })

  it('fait deux lignes d une attaque et d une menace', () => {
    const attaqueEtMenace: EtapeDeroule[] = [
      {
        cle: 'm',
        temps: 'menace',
        titre: 'menace',
        regle: 'regle:menace',
        cibleNom: 'L’Effraction !',
        montant: 3,
        restant: 6,
        plafond: 8,
        boosts: [],
        consequences: [],
      },
      coup({ cle: 'a', montant: 6, restant: 8 }),
    ]
    render(<DeroulePhase etapes={attaqueEtMenace} onTerminer={() => {}} />)
    fireEvent.click(suivant())
    fireEvent.click(suivant())
    expect(document.querySelectorAll('.deroule-bilan li')).toHaveLength(2)
    expect(screen.getByText('L’Effraction ! a gagné 3 menaces')).toBeInTheDocument()
    expect(screen.getByText('Colossus a pris 6 dégâts')).toBeInTheDocument()
    expect(screen.getByText('6/8')).toBeInTheDocument()
  })

  it('n annonce aucun bilan tant que la phase du mechant court', () => {
    // Le point le plus important : arriver au bout des etapes CONNUES n'est pas
    // la fin de la phase. Le cartouche attend, il ne fait pas les comptes.
    render(
      <DeroulePhase
        etapes={troisCoupsSurColossus}
        identitePhase={3}
        phaseMechantEnCours
        onTerminer={() => {}}
      />
    )
    fireEvent.click(suivant())
    fireEvent.click(suivant())
    fireEvent.click(suivant())
    expect(screen.queryByText('Fin de la phase du méchant')).not.toBeInTheDocument()
    expect(document.querySelector('.deroule-bilan')).toBeNull()
    expect(document.querySelector('.deroule-attente')).not.toBeNull()
  })

  it('rend la main au joueur, sans jamais dire « Suivant » sur le bilan', () => {
    const onTerminer = vi.fn()
    const { container } = render(
      <DeroulePhase etapes={[coup({ cle: 'a' })]} onTerminer={onTerminer} />
    )
    fireEvent.click(suivant())
    expect(screen.queryByRole('button', { name: /Suivant/i })).toBeNull()
    fireEvent.click(aToiDeJouer())
    expect(onTerminer).toHaveBeenCalledTimes(1)
    expect(container).toBeEmptyDOMElement()
  })

  it('dit qu il ne s est rien passe plutot que de rester vide', () => {
    // Une carte revelee sans effet chiffre : la phase a bien eu lieu, elle n'a
    // rien coute. Le bilan doit le dire.
    const rienDuTout: EtapeDeroule[] = [
      {
        cle: 'c',
        temps: 'revelation',
        titre: 'Icy Grip révélée',
        regle: 'regle:revelation',
        carteId: 77,
        boosts: [],
        consequences: [],
      },
    ]
    render(<DeroulePhase etapes={rienDuTout} onTerminer={() => {}} />)
    fireEvent.click(suivant())
    expect(screen.getByText('Aucun dégât, aucune menace.')).toBeInTheDocument()
  })

  it('montre les cinq temps tous valides sur le bilan', () => {
    // Le bilan n'est pas un des cinq temps de la carte de reference : il vient
    // apres, et la chronologie les montre alors tous passes ou vides.
    const { container } = render(
      <DeroulePhase etapes={troisCoupsSurColossus} onTerminer={() => {}} />
    )
    fireEvent.click(suivant())
    fireEvent.click(suivant())
    fireEvent.click(suivant())
    const items = [...container.querySelectorAll('.deroule-temps li')]
    expect(items).toHaveLength(5)
    for (const item of items) {
      expect(item.className).toMatch(/est-passe|est-vide/)
    }
    expect(container.querySelector('.deroule-temps li.est-courant')).toBeNull()
  })

  it('laisse relire l etape precedente depuis le bilan', () => {
    render(<DeroulePhase etapes={troisCoupsSurColossus} onTerminer={() => {}} />)
    fireEvent.click(suivant())
    fireEvent.click(suivant())
    fireEvent.click(suivant())
    fireEvent.click(screen.getByRole('button', { name: /Précédent/i }))
    expect(screen.queryByText('Fin de la phase du méchant')).not.toBeInTheDocument()
    expect(screen.getByText('Drone attaque Colossus')).toBeInTheDocument()
  })

  it('ne rend toujours rien hors phase du mechant, sans etape', () => {
    // Le composant est monte des que le mode « detaille » est actif : sans
    // etape, il n'y a aucune fin de phase a annoncer.
    const { container } = render(<DeroulePhase etapes={[]} onTerminer={() => {}} />)
    expect(container).toBeEmptyDOMElement()
  })
})
