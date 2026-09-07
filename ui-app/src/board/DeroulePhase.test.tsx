// Le cartouche du deroule : une etape a la fois, validee avant la suivante.
//
// Il est FIXE en bas au centre et ne bouge jamais d'une etape a l'autre :
// l'oeil sait ou lire et la main ou cliquer des le deuxieme tour. « En bas »
// s'entend au-dessus de la MAIN du joueur, jamais par-dessus elle. On peut revenir en arriere pour relire,
// ce qui ne rejoue rien dans la partie : c'est une relecture, pas un undo.
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { act, fireEvent, render, screen } from '@testing-library/react'
import { DELAI_ALERTE_FILET_MS, DELAI_DEFILEMENT_MS, DeroulePhase } from './DeroulePhase'
import type { EtapeDeroule } from './deroule-phase'
import type { ScanCardProps } from '../components/ScanCard'
import { CLE_REGLE_DEPLIEE } from './moteur'

const etapes: EtapeDeroule[] = [
  { cle: 'a', temps: 'menace', titre: 'menace', regle: 'regle:menace', boosts: [] },
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
      { cle: 'x', temps: 'menace', titre: 'menace', regle: 'regle:menace', boosts: [] },
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

  // --- Un temps n'est « vide » que lorsqu'il est passe ----------------------
  // Constate en partie : la chronologie affichait « Sbires (aucun) » barre
  // pendant que le moteur demandait dans quel ordre activer DEUX sbires. Leurs
  // faits n'existaient pas encore, donc le temps etait marque vide : la marque
  // etait prematuree et disait le contraire de la verite. Un temps se juge par
  // rapport au temps COURANT, celui de l'etape affichee : avant lui et sans
  // etape, vide ; lui, courant ; apres lui, a venir, jamais vide.
  const temps = (container: HTMLElement, nom: RegExp) =>
    [...container.querySelectorAll('.deroule-temps li')].find((li) => li.textContent?.match(nom))

  it('marque un temps sans aucune etape comme vide, une fois la phase finie', () => {
    // `etapes` ne porte que menace et mechant, et la phase est finie
    // (phaseMechantEnCours a false) : sur le bilan, tous les temps sont
    // passes, et sbires n'a produit aucune etape.
    const { container } = render(<DeroulePhase etapes={etapes} onTerminer={() => {}} />)
    fireEvent.click(suivant())
    fireEvent.click(suivant())
    expect(screen.getByText('Fin de la phase du méchant')).toBeInTheDocument()
    const sbires = temps(container, /Sbires/i)
    expect(sbires?.className).toContain('est-vide')
    expect(sbires?.textContent).toMatch(/Aucun/i)
  })

  it('dit « a venir », pas « vide », d un temps qui n est pas encore passe', () => {
    // Deux sbires pas encore actives : le cartouche est sur l'activation du
    // mechant, la phase court, et aucune etape de sbire n'existe encore. Le
    // temps est A VENIR : ni barre, ni « aucun ».
    const { container } = render(
      <DeroulePhase etapes={etapes} phaseMechantEnCours onTerminer={() => {}} />
    )
    fireEvent.click(suivant())
    expect(temps(container, /Méchant/i)?.className).toContain('est-courant')
    const sbires = temps(container, /Sbires/i)
    expect(sbires?.className).not.toContain('est-vide')
    expect(sbires?.className).not.toContain('est-passe')
    expect(sbires?.textContent).not.toMatch(/Aucun/i)
  })

  it('marque vide un temps deja passe sans etape, meme si la phase court encore', () => {
    // La phase a saute la menace (aucune etape) et en est au mechant : la
    // menace est derriere nous, et elle etait vide.
    const sansMenace: EtapeDeroule[] = [
      { cle: 'b', temps: 'mechant', titre: 'attaque', regle: 'regle:activations', boosts: [] },
    ]
    const { container } = render(
      <DeroulePhase etapes={sansMenace} phaseMechantEnCours onTerminer={() => {}} />
    )
    const menace = temps(container, /Menace/i)
    expect(menace?.className).toContain('est-vide')
    expect(menace?.textContent).toMatch(/Aucun/i)
  })

  it('met en avant le temps de l etape affichee, et lui seul', () => {
    const { container } = render(
      <DeroulePhase etapes={etapes} phaseMechantEnCours onTerminer={() => {}} />
    )
    expect(container.querySelectorAll('.deroule-temps li.est-courant')).toHaveLength(1)
    expect(temps(container, /Menace/i)?.className).toContain('est-courant')
    fireEvent.click(suivant())
    expect(container.querySelectorAll('.deroule-temps li.est-courant')).toHaveLength(1)
    expect(temps(container, /Méchant/i)?.className).toContain('est-courant')
    expect(temps(container, /Menace/i)?.className).toContain('est-passe')
  })

  it('ne coute aucun clic pour un temps vide : le compte de clics suit le nombre d etapes', () => {
    // La phase brute (voir brief) : menace, mechant, distribution ; ni
    // sbires, ni revelation ne produisent d'etape ici. Le joueur doit
    // traverser la phase en exactement 3 clics, pas 5 : un temps vide ne
    // consomme jamais de clic pour lui-meme. Le bilan de fin de phase en
    // ajoute un quatrieme, et un seul, quel que soit le nombre de temps vides.
    const onTerminer = vi.fn()
    const sansSbiresNiRevelation: EtapeDeroule[] = [
      { cle: 'a', temps: 'menace', titre: 'menace', regle: 'regle:menace', boosts: [] },
      { cle: 'b', temps: 'mechant', titre: 'attaque', regle: 'regle:activations', boosts: [] },
      { cle: 'c', temps: 'distribution', titre: 'distribution', regle: '', boosts: [] },
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
      },
    ]
    render(
      <DeroulePhase
        etapes={attaque}
        pvMaxParNom={new Map([['Colossus', 14]])}
        onTerminer={() => {}}
      />
    )
    expect(screen.getByText('Klaw attaque Colossus')).toBeInTheDocument()
    expect(screen.getByText('→ 4 dégâts')).toBeInTheDocument()
    // Avant → apres, sur le maximum que le monde connait.
    expect(screen.getByText('Colossus 9 → 5 / 14 PV')).toBeInTheDocument()
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
      },
    ]
    render(<DeroulePhase etapes={sansRestant} onTerminer={() => {}} />)
    expect(document.querySelector('.deroule-compteur')).toBeNull()
    expect(document.body.textContent ?? '').not.toMatch(/undefined|NaN/)
  })

  it('dit combien d etapes compte le temps courant', () => {
    const deuxSbires: EtapeDeroule[] = [
      { cle: 'a', temps: 'sbires', titre: 'attaque', regle: 'regle:activations', auteurNom: 'Drone', cibleNom: 'Shuri', boosts: [] },
      { cle: 'b', temps: 'sbires', titre: 'attaque', regle: 'regle:activations', auteurNom: 'Drone', cibleNom: 'Thor', boosts: [] },
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
      },
    ]
    vi.useFakeTimers()
    try {
      render(<DeroulePhase etapes={avecBoosts} onTerminer={() => {}} />)
      // Le nom parait deux fois : sur la carte de la scene et sur sa ligne.
      // Les deux se retournent ensemble.
      expect(screen.getAllByText('Boost A').length).toBeGreaterThan(0)
      expect(screen.queryAllByText('Boost B')).toHaveLength(0)
      await act(async () => {
        await vi.advanceTimersByTimeAsync(1600)
      })
      expect(screen.getAllByText('Boost B').length).toBeGreaterThan(0)
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
      },
    ]
    render(<DeroulePhase etapes={avecBoosts} onTerminer={() => {}} />)
    expect(screen.getByRole('button', { name: /Suivant/i })).toBeInTheDocument()
  })

  it('n affiche aucun bloc de boost quand il n y en a pas', () => {
    const { container } = render(<DeroulePhase etapes={etapes} onTerminer={() => {}} />)
    expect(container.querySelector('.deroule-boosts')).toBeNull()
  })

  it('avance d une etape a l autre au clic, sans rien acquitter', () => {
    const onSuivant = vi.fn()
    render(<DeroulePhase etapes={etapes} onSuivant={onSuivant} onTerminer={() => {}} />)
    fireEvent.click(suivant())
    expect(screen.getByText('Ultron attaque Shuri')).toBeInTheDocument()
    // Aucune trame retenue : il n'y a rien a acquitter, donc rien ne part.
    expect(onSuivant).not.toHaveBeenCalled()
  })

  it('appelle onTerminer quand la derniere etape est validee', () => {
    const onSuivant = vi.fn()
    const onTerminer = vi.fn()
    render(<DeroulePhase etapes={etapes} onSuivant={onSuivant} onTerminer={onTerminer} />)
    fireEvent.click(suivant())
    fireEvent.click(suivant())
    fireEvent.click(aToiDeJouer())
    expect(onTerminer).toHaveBeenCalledTimes(1)
    // Sans trame retenue, aucun accuse de reception ne part : onTerminer et
    // onSuivant sont deux portes distinctes, board.tsx les branche seulement
    // sur la meme fonction.
    expect(onSuivant).not.toHaveBeenCalled()
  })

  it('onSuivant absent ne casse rien : la prop est optionnelle', () => {
    render(<DeroulePhase etapes={etapes} phaseMechantEnCours trameRetenue={11} onTerminer={() => {}} />)
    expect(() => fireEvent.click(suivant())).not.toThrow()
    expect(screen.getByText('Ultron attaque Shuri')).toBeInTheDocument()
  })

  // --- Le rythme de la phase : qui dit « reçu » au moteur, et quand --------
  //
  // Defaut mesure en partie reelle : le moteur avait execute la menace, une
  // activation, l'accomplissement de la manigance principale et la defaite
  // pendant que le cartouche en etait a sa DEUXIEME etape. Deux causes, toutes
  // les deux corrigees ici :
  //  - le moteur laissait filer les micro-evenements « pas interessants », qui
  //    fabriquaient pourtant des etapes (voir pas-a-pas.test.ts) ;
  //  - le cartouche acquittait a CHAQUE clic, donc des l'etape 1 sur 4.
  //
  // La regle qui remplace : le plateau ne dit « reçu » que lorsque le joueur a
  // valide tout ce que le cartouche sait deja.
  describe('le rythme de la phase', () => {
    const troisEtapes: EtapeDeroule[] = [
      { cle: 'a', temps: 'menace', titre: 'menace', regle: 'regle:menace', boosts: [] },
      {
        cle: 'b',
        temps: 'mechant',
        titre: 'attaque',
        regle: 'regle:activations',
        auteurNom: 'Ultron',
        cibleNom: 'Shuri',
        boosts: [],
      },
      {
        cle: 'c',
        temps: 'sbires',
        titre: 'attaque',
        regle: 'regle:activations',
        auteurNom: 'Drone',
        cibleNom: 'Shuri',
        boosts: [],
      },
    ]

    it('acquitte tout de suite une trame qui ne fabrique aucune etape', () => {
      // Le moteur redessine le plateau des dizaines de fois par phase, et la
      // plupart de ces trames ne racontent rien qui devienne une etape. Le
      // cartouche reste a jour : ça file, exactement comme avant la reprise.
      const onSuivant = vi.fn()
      render(
        <DeroulePhase
          etapes={[]}
          identitePhase={3}
          phaseMechantEnCours
          trameRetenue={11}
          onSuivant={onSuivant}
          onTerminer={() => {}}
        />
      )
      expect(onSuivant).toHaveBeenCalledTimes(1)
    })

    it('n acquitte pas une trame qui fabrique une etape non validee', () => {
      const onSuivant = vi.fn()
      render(
        <DeroulePhase
          etapes={troisEtapes}
          identitePhase={3}
          phaseMechantEnCours
          trameRetenue={11}
          onSuivant={onSuivant}
          onTerminer={() => {}}
        />
      )
      expect(onSuivant).not.toHaveBeenCalled()
    })

    // LE test central de la reprise : c'est le RETARD du cartouche qui decide
    // du rythme, pas la nature de l'evenement. Tant qu'il reste une etape que
    // le joueur n'a pas lue, le moteur attend.
    it('acquitte au clic qui epuise les etapes connues, jamais aux precedents', () => {
      const onSuivant = vi.fn()
      render(
        <DeroulePhase
          etapes={troisEtapes}
          identitePhase={3}
          phaseMechantEnCours
          trameRetenue={11}
          onSuivant={onSuivant}
          onTerminer={() => {}}
        />
      )
      expect(onSuivant).not.toHaveBeenCalled()
      fireEvent.click(suivant())
      expect(onSuivant).not.toHaveBeenCalled()
      fireEvent.click(suivant())
      expect(onSuivant).not.toHaveBeenCalled()
      // Le troisieme clic epuise les etapes connues : le cartouche entre en
      // attente, il est a jour, et c'est LA qu'il dit « reçu ».
      fireEvent.click(suivant())
      expect(onSuivant).toHaveBeenCalledTimes(1)
      expect(document.querySelector('.deroule-attente')).not.toBeNull()
    })

    // Second chemin, indispensable : sans lui la phase se figerait sur le
    // premier micro-evenement muet qui suit une attente.
    it('acquitte la trame muette qui arrive pendant l attente', () => {
      const onSuivant = vi.fn()
      const cartouche = (trameRetenue: number | undefined) => (
        <DeroulePhase
          etapes={troisEtapes}
          identitePhase={3}
          phaseMechantEnCours
          trameRetenue={trameRetenue}
          onSuivant={onSuivant}
          onTerminer={() => {}}
        />
      )
      const { rerender } = render(cartouche(11))
      fireEvent.click(suivant())
      fireEvent.click(suivant())
      fireEvent.click(suivant())
      expect(onSuivant).toHaveBeenCalledTimes(1)
      // Le moteur relache la trame 11, puis en retient une nouvelle qui ne
      // fabrique aucune etape de plus.
      rerender(cartouche(undefined))
      rerender(cartouche(12))
      expect(onSuivant).toHaveBeenCalledTimes(2)
    })

    // Le piege symetrique : une trame qui apporte une etape de PLUS ne doit
    // surtout pas etre acquittee, meme si le cartouche etait en attente juste
    // avant. Sinon le moteur repartirait pendant que le joueur lit.
    it('n acquitte pas la trame qui apporte une etape de plus', () => {
      const onSuivant = vi.fn()
      const deuxEtapes = troisEtapes.slice(0, 2)
      const cartouche = (liste: EtapeDeroule[], trameRetenue: number | undefined) => (
        <DeroulePhase
          etapes={liste}
          identitePhase={3}
          phaseMechantEnCours
          trameRetenue={trameRetenue}
          onSuivant={onSuivant}
          onTerminer={() => {}}
        />
      )
      const { rerender } = render(cartouche(deuxEtapes, 11))
      fireEvent.click(suivant())
      fireEvent.click(suivant())
      expect(onSuivant).toHaveBeenCalledTimes(1)
      rerender(cartouche(deuxEtapes, undefined))
      rerender(cartouche(troisEtapes, 12))
      expect(onSuivant).toHaveBeenCalledTimes(1)
      // Le joueur atterrit tout seul sur l'etape de plus : il a deja clique
      // pour l'obtenir, il ne doit pas avoir a recliquer.
      expect(screen.getByText('Drone attaque Shuri')).toBeInTheDocument()
    })

    // La garde contre la rafale d'accuses. Elle se lie a l'IDENTITE de la
    // trame et non a un booleen : l'etat du cartouche se recalcule a chaque
    // publication du moteur, et un booleen ferait repartir l'accuse a chaque
    // fois, donc en boucle.
    it('n envoie qu un seul accuse par trame, meme recalcule plusieurs fois', () => {
      const onSuivant = vi.fn()
      const cartouche = (trameRetenue: number | undefined, pv: number) => (
        <DeroulePhase
          etapes={[]}
          identitePhase={3}
          phaseMechantEnCours
          trameRetenue={trameRetenue}
          pvMaxParNom={new Map([['Shuri', pv]])}
          onSuivant={onSuivant}
          onTerminer={() => {}}
        />
      )
      const { rerender } = render(cartouche(11, 14))
      expect(onSuivant).toHaveBeenCalledTimes(1)
      // Le plateau se redessine, la trame retenue est toujours la meme.
      rerender(cartouche(11, 13))
      rerender(cartouche(11, 12))
      rerender(cartouche(11, 11))
      expect(onSuivant).toHaveBeenCalledTimes(1)
      // Une AUTRE trame, elle, obtient bien son propre accuse.
      rerender(cartouche(12, 11))
      expect(onSuivant).toHaveBeenCalledTimes(2)
    })

    // Anti-gel : le moteur attend l'accuse de CHAQUE client. Un cartouche qui
    // n'a plus rien a montrer ne doit retenir personne, sinon toute la table
    // patiente jusqu'au filet anti-blocage (90 s par trame).
    it('acquitte encore une fois la partie finie', () => {
      const onSuivant = vi.fn()
      render(
        <DeroulePhase
          etapes={troisEtapes}
          identitePhase={3}
          phaseMechantEnCours
          partieFinie
          trameRetenue={11}
          onSuivant={onSuivant}
          onTerminer={() => {}}
        />
      )
      expect(onSuivant).toHaveBeenCalledTimes(1)
    })

    // Une nouvelle phase remet le compteur de trames a zero : les `render_id`
    // du moteur repartent de zero avec une nouvelle partie, et un numero deja
    // vu ne doit pas faire sauter son accuse.
    it('oublie la derniere trame acquittee quand la phase change', () => {
      const onSuivant = vi.fn()
      const cartouche = (identitePhase: number, trameRetenue: number | undefined) => (
        <DeroulePhase
          etapes={[]}
          identitePhase={identitePhase}
          phaseMechantEnCours
          trameRetenue={trameRetenue}
          onSuivant={onSuivant}
          onTerminer={() => {}}
        />
      )
      const { rerender } = render(cartouche(3, 11))
      expect(onSuivant).toHaveBeenCalledTimes(1)
      // Le moteur relache la trame, puis une NOUVELLE partie recommence a
      // numeroter ses rendus : le numero 11 revient sur une autre phase.
      rerender(cartouche(3, undefined))
      rerender(cartouche(4, 11))
      expect(onSuivant).toHaveBeenCalledTimes(2)
    })

    // UNE PARTIE NEUVE SANS RECHARGEMENT DE PAGE (« Rejouer », ou retour au
    // menu puis autre partie). Le heros tombe au round 3, la partie finie
    // masque le cartouche, puis le monde revient au round 1 EN PLEIN TOUR DU
    // JOUEUR : ni `phaseMechantEnCours` ni `termine`, donc rien ne remettait le
    // cartouche a zero. Il reapparaissait avec le bilan de la partie morte.
    it('efface tout quand une nouvelle partie commence sans rechargement', () => {
      const chute: EtapeDeroule[] = [
        {
          cle: 'y',
          temps: 'mechant',
          titre: 'attaque',
          regle: 'regle:activations',
          carteId: 50,
          cibleId: 12,
          auteurNom: 'Klaw',
          cibleNom: 'Colossus',
          montant: 6,
          restant: 0,
          defaite: true,
          boosts: [],
        },
      ]
      const { container, rerender } = render(
        <DeroulePhase
          etapes={chute}
          identitePhase={3}
          identitePartie="partie-A"
          phaseMechantEnCours
          onTerminer={() => {}}
        />
      )
      expect(screen.getByText(/Colossus est vaincu/)).toBeInTheDocument()
      // La partie finie masque le cartouche sans qu'il se dise `termine`.
      rerender(
        <DeroulePhase
          etapes={chute}
          identitePhase={3}
          identitePartie="partie-A"
          phaseMechantEnCours
          partieFinie
          onTerminer={() => {}}
        />
      )
      expect(container).toBeEmptyDOMElement()
      // La partie neuve : round 1, tour du joueur, plus aucun fait.
      rerender(
        <DeroulePhase
          etapes={[]}
          identitePhase={1}
          identitePartie="partie-B"
          onTerminer={() => {}}
        />
      )
      expect(container).toBeEmptyDOMElement()
      // Et la memoire est vide : sans quoi le bilan de la partie morte
      // reparaitrait des que le cartouche se croirait hors phase du mechant.
      expect(screen.queryByText(/Colossus/)).not.toBeInTheDocument()
      expect(screen.queryByText('Fin de la phase du méchant')).not.toBeInTheDocument()
    })

    it('repart de zero meme quand la partie neuve rouvre au MEME round', () => {
      // Deux parties peuvent s'arreter et repartir au meme round : la remise a
      // zero par la seule identite de phase ne jouerait alors pas.
      const menace: EtapeDeroule[] = [
        {
          cle: 'a',
          temps: 'menace',
          titre: 'menace',
          regle: 'regle:menace',
          cibleNom: 'L’Effraction !',
          montant: 3,
          boosts: [],
        },
      ]
      const { container, rerender } = render(
        <DeroulePhase
          etapes={menace}
          identitePhase={1}
          identitePartie="partie-A"
          phaseMechantEnCours
          onTerminer={() => {}}
        />
      )
      expect(screen.getByText('L’Effraction ! gagne 3 menaces')).toBeInTheDocument()
      rerender(
        <DeroulePhase
          etapes={[]}
          identitePhase={1}
          identitePartie="partie-B"
          onTerminer={() => {}}
        />
      )
      expect(container).toBeEmptyDOMElement()
    })
  })
  // Defaut 2 (voir brief) : « arriver au bout des etapes CONNUES » n'est pas
  // « la phase est finie ». Depuis que chaque « Suivant » relache une trame du
  // moteur, la liste s'allonge PENDANT la phase : le cartouche doit attendre
  // la suite au lieu de se croire au bout, et la remise a zero doit suivre
  // l'identite de la phase (le round), jamais la longueur de la liste.
  const menaceSeule: EtapeDeroule[] = [
    { cle: 'a', temps: 'menace', titre: 'menace', regle: 'regle:menace', boosts: [] },
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
      { cle: 'z1', temps: 'menace', titre: 'menace', regle: 'regle:menace', boosts: [] },
      { cle: 'z2', temps: 'mechant', titre: 'attaque', regle: 'regle:activations', boosts: [] },
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
      { cle: 'c', temps: 'distribution', titre: 'distribution', regle: '', boosts: [] },
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

  it('relache le moteur sur le clic qui met en attente', () => {
    // Sans cet accuse, le clic qui met en attente ne relacherait aucune trame :
    // le moteur ne produirait jamais l'etape attendue, et l'attente serait
    // sans fin.
    const onSuivant = vi.fn()
    render(
      <DeroulePhase
        etapes={menaceSeule}
        identitePhase={3}
        phaseMechantEnCours
        trameRetenue={11}
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

  // --- L'avance auto : une seule horloge, et c'est le cartouche ----------
  //
  // Defaut constate en partie reelle (brief « une seule horloge ») : « avance
  // toute seule » faisait avancer le MOTEUR toutes les 1200 ms pendant que le
  // cartouche attendait des clics. Le joueur lisait la menace, le mechant et
  // ses sbires avaient deja frappe. Desormais c'est le cartouche qui s'avance
  // lui-meme, par la MEME fonction que « Suivant » : l'accuse de reception
  // part par le meme chemin, et le moteur ne peut plus partir devant.
  describe('avance auto du cartouche', () => {
    const DELAI = 1000
    const troisEtapes: EtapeDeroule[] = [
      { cle: 'a', temps: 'menace', titre: 'menace', regle: 'regle:menace', boosts: [] },
      {
        cle: 'b',
        temps: 'mechant',
        titre: 'attaque',
        regle: 'regle:activations',
        auteurNom: 'Ultron',
        cibleNom: 'Shuri',
        boosts: [],
      },
      {
        cle: 'c',
        temps: 'sbires',
        titre: 'attaque',
        regle: 'regle:activations',
        auteurNom: 'Drone',
        cibleNom: 'Shuri',
        boosts: [],
      },
    ]
    const attendre = async (ms: number) => {
      await act(async () => {
        await vi.advanceTimersByTimeAsync(ms)
      })
    }
    // Une echeance a la fois : le minuteur de l'etape suivante n'est arme
    // qu'au rendu qui suit l'echeance de la precedente, et un seul `act` qui
    // avancerait de deux delais d'un coup ne laisserait pas React faire ce
    // rendu entre les deux. C'est une limite du temps simule, pas du
    // cartouche.
    const attendreEtapes = async (n: number) => {
      for (let i = 0; i < n; i += 1) await attendre(DELAI)
    }

    beforeEach(() => {
      vi.useFakeTimers()
    })
    afterEach(() => {
      vi.useRealTimers()
    })

    it('passe une etape toute seule apres le delai, et acquitte par le meme chemin que Suivant', async () => {
      const onSuivant = vi.fn()
      render(
        <DeroulePhase
          etapes={etapes}
          identitePhase={3}
          phaseMechantEnCours
          trameRetenue={11}
          avanceAuto
          delaiAvanceMs={DELAI}
          onSuivant={onSuivant}
          onTerminer={() => {}}
        />
      )
      expect(screen.getByText('Menace sur la manigance principale')).toBeInTheDocument()
      // Pas avant le delai : c'est un temps de lecture.
      await attendre(DELAI - 1)
      expect(screen.getByText('Menace sur la manigance principale')).toBeInTheDocument()
      expect(onSuivant).not.toHaveBeenCalled()
      await attendre(1)
      expect(screen.getByText('Ultron attaque Shuri')).toBeInTheDocument()
      // Le cartouche n'est pas encore a jour (il lui reste l'etape b a faire
      // lire) : rien n'est parti au moteur.
      expect(onSuivant).not.toHaveBeenCalled()
      // Le bout des etapes connues, atteint tout seul : le cartouche entre en
      // attente et acquitte, exactement comme au clic.
      await attendre(DELAI)
      expect(onSuivant).toHaveBeenCalledTimes(1)
      expect(document.querySelector('.deroule-attente')).not.toBeNull()
    })

    it('ne bouge pas tout seul sans avance auto, meme apres plusieurs delais', async () => {
      const onSuivant = vi.fn()
      render(
        <DeroulePhase
          etapes={etapes}
          identitePhase={3}
          phaseMechantEnCours
          trameRetenue={11}
          delaiAvanceMs={DELAI}
          onSuivant={onSuivant}
          onTerminer={() => {}}
        />
      )
      await attendre(DELAI * 4)
      expect(screen.getByText('Menace sur la manigance principale')).toBeInTheDocument()
      expect(onSuivant).not.toHaveBeenCalled()
    })

    it('ne pose aucun minuteur pendant l attente de la suite', async () => {
      // Au bout des etapes connues, il n'y a rien a avancer : un minuteur qui
      // « validerait » l'attente ne ferait que rappeler avancer() dans le
      // vide. On le prouve par le moteur : une seule trame acquittee, quel que
      // soit le temps qui passe.
      const onSuivant = vi.fn()
      const onTerminer = vi.fn()
      render(
        <DeroulePhase
          etapes={etapes}
          identitePhase={3}
          phaseMechantEnCours
          trameRetenue={11}
          avanceAuto
          delaiAvanceMs={DELAI}
          onSuivant={onSuivant}
          onTerminer={onTerminer}
        />
      )
      await attendreEtapes(2)
      expect(onSuivant).toHaveBeenCalledTimes(1)
      expect(vi.getTimerCount()).toBe(0)
      await attendreEtapes(5)
      expect(onSuivant).toHaveBeenCalledTimes(1)
      expect(onTerminer).not.toHaveBeenCalled()
    })

    it('repart tout seul sur l etape que le moteur vient de produire', async () => {
      // Le cartouche s'est mis en attente, le moteur a produit la suite : la
      // sortie d'attente l'affiche, et le minuteur repart dessus.
      const onSuivant = vi.fn()
      const cartouche = (liste: EtapeDeroule[], trame: number) => (
        <DeroulePhase
          etapes={liste}
          identitePhase={3}
          phaseMechantEnCours
          trameRetenue={trame}
          avanceAuto
          delaiAvanceMs={DELAI}
          onSuivant={onSuivant}
          onTerminer={() => {}}
        />
      )
      const { rerender } = render(cartouche(etapes, 11))
      await attendreEtapes(2)
      expect(onSuivant).toHaveBeenCalledTimes(1)
      rerender(cartouche(troisEtapes, 12))
      expect(screen.getByText('Drone attaque Shuri')).toBeInTheDocument()
      expect(onSuivant).toHaveBeenCalledTimes(1)
      await attendre(DELAI)
      expect(onSuivant).toHaveBeenCalledTimes(2)
    })

    it('« Precedent » suspend l avance : l etape relue ne repart pas en avant', async () => {
      render(
        <DeroulePhase
          etapes={troisEtapes}
          identitePhase={3}
          phaseMechantEnCours
          avanceAuto
          delaiAvanceMs={DELAI}
          onTerminer={() => {}}
        />
      )
      await attendre(DELAI)
      expect(screen.getByText('Ultron attaque Shuri')).toBeInTheDocument()
      fireEvent.click(screen.getByRole('button', { name: /Précédent/i }))
      expect(screen.getByText('Menace sur la manigance principale')).toBeInTheDocument()
      await attendre(DELAI * 4)
      expect(screen.getByText('Menace sur la manigance principale')).toBeInTheDocument()
    })

    it('« Suivant » apres un « Precedent » relance l avance', async () => {
      render(
        <DeroulePhase
          etapes={troisEtapes}
          identitePhase={3}
          phaseMechantEnCours
          avanceAuto
          delaiAvanceMs={DELAI}
          onTerminer={() => {}}
        />
      )
      await attendre(DELAI)
      fireEvent.click(screen.getByRole('button', { name: /Précédent/i }))
      fireEvent.click(suivant())
      expect(screen.getByText('Ultron attaque Shuri')).toBeInTheDocument()
      await attendre(DELAI)
      expect(screen.getByText('Drone attaque Shuri')).toBeInTheDocument()
    })

    it('ne valide jamais le bilan de fin de phase tout seul', async () => {
      // C'est le moment ou le joueur reprend la main : il doit le voir.
      const onTerminer = vi.fn()
      render(
        <DeroulePhase
          etapes={etapes}
          identitePhase={3}
          avanceAuto
          delaiAvanceMs={DELAI}
          onTerminer={onTerminer}
        />
      )
      await attendreEtapes(2)
      expect(aToiDeJouer()).toBeInTheDocument()
      await attendreEtapes(5)
      expect(aToiDeJouer()).toBeInTheDocument()
      expect(onTerminer).not.toHaveBeenCalled()
      fireEvent.click(aToiDeJouer())
      expect(onTerminer).toHaveBeenCalledTimes(1)
    })

    it('ne valide jamais la chute d un heros tout seul', async () => {
      // Le moment le plus important d'une partie ne defile pas comme les
      // autres : « Continuer » attend un vrai clic.
      const onTerminer = vi.fn()
      const chute: EtapeDeroule[] = [
        troisEtapes[0],
        { ...troisEtapes[1], montant: 4, restant: 0, defaite: true },
      ]
      render(
        <DeroulePhase
          etapes={chute}
          identitePhase={3}
          phaseMechantEnCours
          avanceAuto
          delaiAvanceMs={DELAI}
          onTerminer={onTerminer}
        />
      )
      await attendre(DELAI)
      expect(screen.getByRole('button', { name: /Continuer/i })).toBeInTheDocument()
      await attendreEtapes(5)
      expect(screen.getByRole('button', { name: /Continuer/i })).toBeInTheDocument()
      expect(onTerminer).not.toHaveBeenCalled()
    })

    it('n avance pas pendant que le moteur pose une question au joueur', async () => {
      // Le cartouche est replie, sans bouton : il n'a pas de minuteur non
      // plus. Une fois la question resolue, il repart de la ou il en etait.
      const cartouche = (questionAuJoueur: boolean) => (
        <DeroulePhase
          etapes={troisEtapes}
          identitePhase={3}
          phaseMechantEnCours
          questionAuJoueur={questionAuJoueur}
          avanceAuto
          delaiAvanceMs={DELAI}
          onTerminer={() => {}}
        />
      )
      const { rerender } = render(cartouche(true))
      await attendre(DELAI * 4)
      rerender(cartouche(false))
      expect(screen.getByText('Menace sur la manigance principale')).toBeInTheDocument()
      await attendre(DELAI)
      expect(screen.getByText('Ultron attaque Shuri')).toBeInTheDocument()
    })

    it('nettoie son minuteur au demontage', async () => {
      const onSuivant = vi.fn()
      const { unmount } = render(
        <DeroulePhase
          etapes={etapes}
          identitePhase={3}
          phaseMechantEnCours
          trameRetenue={11}
          avanceAuto
          delaiAvanceMs={DELAI}
          onSuivant={onSuivant}
          onTerminer={() => {}}
        />
      )
      unmount()
      expect(vi.getTimerCount()).toBe(0)
      await attendre(DELAI * 3)
      expect(onSuivant).not.toHaveBeenCalled()
    })
  })

  // --- Echap : « Tout derouler » fait defiler le CARTOUCHE ------------------
  //
  // Avant, Echap relachait le moteur pour tout le reste de la phase
  // (`passerToutLaPhase`, `phaseSautee`) : le moteur filait, le cartouche
  // restait sur son etape, et le joueur n'avait plus aucune autorite sur le
  // rythme. Desormais Echap fait defiler les etapes du cartouche, vite et
  // sans delai de lecture, par la MEME fonction que « Suivant » : l'accuse
  // part par le chemin ordinaire, le moteur suit, il ne precede jamais. Le
  // bilan, lui, attend toujours un vrai clic.
  describe('Echap : tout derouler', () => {
    const troisEtapes: EtapeDeroule[] = [
      { cle: 'a', temps: 'menace', titre: 'menace', regle: 'regle:menace', boosts: [] },
      {
        cle: 'b',
        temps: 'mechant',
        titre: 'attaque',
        regle: 'regle:activations',
        auteurNom: 'Ultron',
        cibleNom: 'Shuri',
        boosts: [],
      },
      {
        cle: 'c',
        temps: 'sbires',
        titre: 'attaque',
        regle: 'regle:activations',
        auteurNom: 'Drone',
        cibleNom: 'Shuri',
        boosts: [],
      },
    ]
    const echap = () =>
      document.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape', bubbles: true }))
    // Une echeance par act, meme raison que pour l'avance auto ci-dessus.
    const defiler = async (etapes: number) => {
      for (let i = 0; i < etapes; i += 1) {
        await act(async () => {
          await vi.advanceTimersByTimeAsync(DELAI_DEFILEMENT_MS)
        })
      }
    }

    beforeEach(() => {
      vi.useFakeTimers()
    })
    afterEach(() => {
      vi.useRealTimers()
    })

    it('fait defiler les etapes jusqu au bilan, qui attend un vrai clic', async () => {
      const onTerminer = vi.fn()
      render(<DeroulePhase etapes={troisEtapes} identitePhase={3} onTerminer={onTerminer} />)
      echap()
      await defiler(3)
      expect(aToiDeJouer()).toBeInTheDocument()
      await defiler(5)
      expect(aToiDeJouer()).toBeInTheDocument()
      expect(onTerminer).not.toHaveBeenCalled()
      fireEvent.click(aToiDeJouer())
      expect(onTerminer).toHaveBeenCalledTimes(1)
    })

    it('ne relache le moteur que par le chemin ordinaire, une trame a la fois', async () => {
      // Le moteur SUIT le cartouche : une trame acquittee quand le cartouche
      // est a jour, jamais un « laissez passer » pour toute la phase. La
      // preuve : entre deux trames, le cartouche attend la suite comme
      // d'habitude, et repart de lui-meme sur l'etape qui arrive.
      const onSuivant = vi.fn()
      const onTerminer = vi.fn()
      const cartouche = (liste: EtapeDeroule[], trame: number, enCours: boolean) => (
        <DeroulePhase
          etapes={liste}
          identitePhase={3}
          phaseMechantEnCours={enCours}
          trameRetenue={trame}
          onSuivant={onSuivant}
          onTerminer={onTerminer}
        />
      )
      const { rerender } = render(cartouche(etapes, 11, true))
      echap()
      await defiler(2)
      expect(document.querySelector('.deroule-attente')).not.toBeNull()
      expect(onSuivant).toHaveBeenCalledTimes(1)
      await defiler(3)
      expect(onSuivant).toHaveBeenCalledTimes(1)
      rerender(cartouche(troisEtapes, 12, true))
      expect(screen.getByText('Drone attaque Shuri')).toBeInTheDocument()
      await defiler(1)
      expect(onSuivant).toHaveBeenCalledTimes(2)
      rerender(cartouche(troisEtapes, 13, false))
      await defiler(3)
      expect(aToiDeJouer()).toBeInTheDocument()
      expect(onTerminer).not.toHaveBeenCalled()
    })

    it('ignore le delai de lecture de l avance auto', async () => {
      render(
        <DeroulePhase
          etapes={troisEtapes}
          identitePhase={3}
          avanceAuto
          delaiAvanceMs={1000}
          onTerminer={() => {}}
        />
      )
      echap()
      await defiler(3)
      expect(aToiDeJouer()).toBeInTheDocument()
    })

    it('s arrete sur un « Precedent » : le joueur reprend la main', async () => {
      render(<DeroulePhase etapes={troisEtapes} identitePhase={3} onTerminer={() => {}} />)
      echap()
      await defiler(3)
      expect(aToiDeJouer()).toBeInTheDocument()
      fireEvent.click(screen.getByRole('button', { name: /Précédent/i }))
      expect(screen.getByText('Drone attaque Shuri')).toBeInTheDocument()
      await defiler(5)
      expect(screen.getByText('Drone attaque Shuri')).toBeInTheDocument()
    })

    it('ne fait rien quand le moteur pose une question au joueur', async () => {
      render(
        <DeroulePhase
          etapes={troisEtapes}
          identitePhase={3}
          phaseMechantEnCours
          questionAuJoueur
          onTerminer={() => {}}
        />
      )
      echap()
      await defiler(5)
      expect(vi.getTimerCount()).toBe(0)
    })
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

  // LE CAS REEL DE FIN DE PHASE, celui que la partie produit vraiment.
  //
  // Le moteur quitte la phase du mechant et incremente le round dans la meme
  // foulee, sans retenir aucune trame entre les deux : le plateau ne voit donc
  // jamais l'etat intermediaire « phase finie, round inchange ». Or
  // `etapesDeroule` (deroule-phase.ts) filtre les faits sur le round du monde,
  // et `identitePhase` vaut ce meme round : a la premiere trame d'apres,
  // `etapes` retombe a zero ET la remise a zero du cartouche se declenche.
  // Sans memoire de la phase racontee, le bilan n'a plus rien a compter et le
  // joueur ne le voit jamais (constat 5 du rapport A3-fix).
  it('montre son bilan alors que le round a deja tourne et que les faits ont disparu', () => {
    const onTerminer = vi.fn()
    const { rerender } = render(
      <DeroulePhase
        etapes={troisCoupsSurColossus}
        identitePhase={3}
        phaseMechantEnCours
        onTerminer={onTerminer}
      />
    )
    fireEvent.click(suivant())
    fireEvent.click(suivant())
    fireEvent.click(suivant())
    expect(document.querySelector('.deroule-attente')).not.toBeNull()

    // La trame suivante : plus de phase du mechant, plus de faits du round, et
    // un round de plus.
    rerender(
      <DeroulePhase
        etapes={[]}
        identitePhase={4}
        phaseMechantEnCours={false}
        onTerminer={onTerminer}
      />
    )
    expect(screen.getByText('Fin de la phase du méchant')).toBeInTheDocument()
    expect(document.querySelectorAll('.deroule-bilan li')).toHaveLength(1)
    expect(screen.getByText('Colossus a pris 6 dégâts')).toBeInTheDocument()
    expect(onTerminer).not.toHaveBeenCalled()
  })

  it('rend la main sur « À toi de jouer » une fois le round tourne', () => {
    const onTerminer = vi.fn()
    const { container, rerender } = render(
      <DeroulePhase
        etapes={troisCoupsSurColossus}
        identitePhase={3}
        phaseMechantEnCours
        onTerminer={onTerminer}
      />
    )
    fireEvent.click(suivant())
    fireEvent.click(suivant())
    fireEvent.click(suivant())
    rerender(
      <DeroulePhase
        etapes={[]}
        identitePhase={4}
        phaseMechantEnCours={false}
        onTerminer={onTerminer}
      />
    )
    fireEvent.click(aToiDeJouer())
    expect(onTerminer).toHaveBeenCalledTimes(1)
    expect(container).toBeEmptyDOMElement()
  })

  // Le filet de la memoire : elle ne doit pas faire revivre la phase
  // precedente. Quand la phase du mechant SUIVANTE s'ouvre, le cartouche
  // repart de sa premiere etape, sur les etapes du nouveau round.
  it('oublie la phase racontee des que la suivante s ouvre', () => {
    const onTerminer = vi.fn()
    const { rerender } = render(
      <DeroulePhase
        etapes={troisCoupsSurColossus}
        identitePhase={3}
        phaseMechantEnCours
        onTerminer={onTerminer}
      />
    )
    fireEvent.click(suivant())
    fireEvent.click(suivant())
    fireEvent.click(suivant())
    rerender(
      <DeroulePhase etapes={[]} identitePhase={4} phaseMechantEnCours={false} onTerminer={onTerminer} />
    )
    expect(screen.getByText('Fin de la phase du méchant')).toBeInTheDocument()

    // La phase du mechant du round 4 s'ouvre avec sa propre menace.
    rerender(
      <DeroulePhase
        etapes={[
          {
            cle: 'm4',
            temps: 'menace',
            titre: 'menace',
            regle: 'regle:menace',
            cibleNom: 'L’Effraction !',
            montant: 1,
            restant: 7,
            boosts: [],
          },
        ]}
        identitePhase={4}
        phaseMechantEnCours
        onTerminer={onTerminer}
      />
    )
    expect(screen.queryByText('Fin de la phase du méchant')).not.toBeInTheDocument()
    expect(screen.getByText('L’Effraction ! gagne 1 menace')).toBeInTheDocument()
    expect(screen.queryByText('Colossus a pris 6 dégâts')).not.toBeInTheDocument()
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

  // --- Un heros tombe -------------------------------------------------------
  // Le moment le plus important d'une partie : il ne doit pas defiler comme
  // les autres. L'etape qui a mis le heros a terre reste affichee, marquee, et
  // le deroule n'affiche RIEN au-dela.
  const chuteDeColossus: EtapeDeroule[] = [
    { cle: 'x', temps: 'menace', titre: 'menace', regle: 'regle:menace', boosts: [] },
    {
      cle: 'y',
      temps: 'mechant',
      titre: 'attaque',
      regle: 'regle:activations',
      carteId: 50,
      cibleId: 12,
      auteurNom: 'Klaw',
      cibleNom: 'Colossus',
      montant: 6,
      restant: 0,
      defaite: true,
      boosts: [],
    },
    {
      cle: 'z',
      temps: 'sbires',
      titre: 'attaque',
      regle: 'regle:activations',
      carteId: 60,
      cibleId: 13,
      auteurNom: 'Drone',
      cibleNom: 'Spider-Man',
      montant: 2,
      boosts: [],
    },
  ]

  it('annonce la chute du heros sur l etape qui l a mis a terre', () => {
    const { container } = render(
      <DeroulePhase etapes={chuteDeColossus} onTerminer={() => {}} />
    )
    fireEvent.click(suivant())
    expect(screen.getByText('Klaw attaque Colossus')).toBeInTheDocument()
    expect(screen.getByText(/Colossus est vaincu/)).toBeInTheDocument()
    expect(screen.getByText(/La phase s.arrête ici/)).toBeInTheDocument()
    expect(container.querySelector('.deroule-defaite')).not.toBeNull()
  })

  it('n affiche aucune etape au-dela de la defaite', () => {
    render(<DeroulePhase etapes={chuteDeColossus} onTerminer={() => {}} />)
    fireEvent.click(suivant())
    // L'etape suivante existe pourtant bien dans la liste recue : le cartouche
    // s'arrete quand meme.
    expect(screen.queryByText('Drone attaque Spider-Man')).not.toBeInTheDocument()
    expect(screen.queryByRole('button', { name: /Suivant/i })).toBeNull()
  })

  it('dit « Continuer », et non « Suivant », sur l etape de defaite', () => {
    render(<DeroulePhase etapes={chuteDeColossus} onTerminer={() => {}} />)
    fireEvent.click(suivant())
    expect(screen.getByRole('button', { name: /Continuer/i })).toBeInTheDocument()
  })

  it('la defaite l emporte sur le bilan de fin de phase', () => {
    // Le deroule s'arrete net a la chute : il n'y a plus de fin de phase a
    // raconter derriere elle.
    const onTerminer = vi.fn()
    const { container } = render(
      <DeroulePhase etapes={chuteDeColossus} onTerminer={onTerminer} />
    )
    fireEvent.click(suivant())
    expect(screen.queryByText('Fin de la phase du méchant')).not.toBeInTheDocument()
    fireEvent.click(screen.getByRole('button', { name: /Continuer/i }))
    expect(onTerminer).toHaveBeenCalledTimes(1)
    expect(container).toBeEmptyDOMElement()
  })

  it('rend la main tout de suite meme si la phase du mechant court encore', () => {
    // Sans cela, « Continuer » aurait bascule le cartouche en « La suite
    // arrive… » sur une suite qu'il ne montrera jamais.
    const onTerminer = vi.fn()
    const { container } = render(
      <DeroulePhase etapes={chuteDeColossus} phaseMechantEnCours onTerminer={onTerminer} />
    )
    fireEvent.click(suivant())
    fireEvent.click(screen.getByRole('button', { name: /Continuer/i }))
    expect(onTerminer).toHaveBeenCalledTimes(1)
    expect(container).toBeEmptyDOMElement()
  })

  // LE COUP FATAL SE VOIT AVANT L'ECRAN DE FIN. C'est ce signal-la qui
  // autorise board.tsx a le laisser paraitre (voir `afficherFinDePartie`) :
  // sans lui, le cartouche et l'ecran basculaient sur la meme trame et l'etape
  // qui avait tue n'etait jamais lue.
  it('previent que le coup fatal a ete vu, au clic sur Continuer', () => {
    const onDefaiteVue = vi.fn()
    render(
      <DeroulePhase
        etapes={chuteDeColossus}
        phaseMechantEnCours
        onTerminer={() => {}}
        onDefaiteVue={onDefaiteVue}
      />
    )
    fireEvent.click(suivant())
    // Pas avant : le joueur lit encore l'etape.
    expect(onDefaiteVue).not.toHaveBeenCalled()
    fireEvent.click(screen.getByRole('button', { name: /Continuer/i }))
    expect(onDefaiteVue).toHaveBeenCalledTimes(1)
  })

  it('ne previent d aucun coup fatal a la fin d une phase ordinaire', () => {
    // Le piege qu'evite une prop dediee : `onTerminer` part a la fin de CHAQUE
    // phase du mechant, et s'en servir aurait declare le coup fatal vu des la
    // premiere phase de la partie.
    const onDefaiteVue = vi.fn()
    render(<DeroulePhase etapes={etapes} onTerminer={() => {}} onDefaiteVue={onDefaiteVue} />)
    fireEvent.click(suivant())
    fireEvent.click(suivant())
    fireEvent.click(aToiDeJouer())
    expect(onDefaiteVue).not.toHaveBeenCalled()
  })

  // LE cas negatif, le plus important : une marque posee trop largement
  // s'afficherait a tort sans que rien ne le signale.
  it('ne pose AUCUNE marque de defaite sur une etape ordinaire', () => {
    const { container } = render(<DeroulePhase etapes={etapes} onTerminer={() => {}} />)
    expect(container.querySelector('.deroule-defaite')).toBeNull()
    expect(screen.queryByText(/vaincu/i)).not.toBeInTheDocument()
    expect(screen.queryByText(/La phase s.arrête ici/)).not.toBeInTheDocument()
    expect(screen.getByRole('button', { name: /Suivant/i })).toBeInTheDocument()
    fireEvent.click(suivant())
    expect(container.querySelector('.deroule-defaite')).toBeNull()
    expect(screen.queryByText(/vaincu/i)).not.toBeInTheDocument()
    expect(screen.queryByRole('button', { name: /Continuer/i })).toBeNull()
  })
  // --- La fin de la partie l'emporte sur tout -------------------------------
  // Constate en partie : la manigance principale etait allee au bout, l'ecran
  // de defaite etait affiche, et le cartouche restait par-dessus le plateau a
  // annoncer « La suite arrive… » indefiniment.
  describe('fin de partie', () => {
    it('efface le cartouche', () => {
      const { container } = render(
        <DeroulePhase etapes={etapes} partieFinie onTerminer={() => {}} />
      )
      expect(container).toBeEmptyDOMElement()
    })

    it('efface le cartouche meme au milieu de la phase du mechant', () => {
      // C'est le cas reel : la phase du mechant courait encore, le cartouche
      // attendait « La suite arrive… », et la partie etait finie.
      const { container } = render(
        <DeroulePhase etapes={etapes} phaseMechantEnCours partieFinie onTerminer={() => {}} />
      )
      expect(container).toBeEmptyDOMElement()
      expect(screen.queryByText('La suite arrive…')).not.toBeInTheDocument()
    })

    it('efface aussi la mise en scene laissee sur le plateau', () => {
      // Sans cela, le plateau resterait assombri sous l'ecran de fin.
      const scene = document.createElement('div')
      scene.className = 'plateau-scene'
      const carte = document.createElement('article')
      carte.className = 'scan-card'
      carte.setAttribute('data-card-id', '50')
      scene.append(carte)
      document.body.append(scene)

      const { rerender } = render(
        <DeroulePhase etapes={etapes} phaseMechantEnCours onTerminer={() => {}} />
      )
      fireEvent.click(suivant())
      // Plus aucune carte de la table n'est touchee : la scene porte les
      // siennes. Seul le voile reste, et il doit tomber avec l'ecran de fin.
      expect(carte.className).toBe('scan-card')
      expect(document.body.classList.contains('deroule-voile')).toBe(true)

      rerender(
        <DeroulePhase etapes={etapes} phaseMechantEnCours partieFinie onTerminer={() => {}} />
      )
      expect(document.body.classList.contains('deroule-voile')).toBe(false)
      scene.remove()
    })

    it('ne relache plus le moteur au clavier une fois la partie finie', () => {
      // Le cartouche n'est plus a l'ecran : sa touche Entree ne doit pas
      // continuer a faire avancer le moteur derriere l'ecran de fin.
      const onSuivant = vi.fn()
      render(
        <DeroulePhase
          etapes={etapes}
          phaseMechantEnCours
          partieFinie
          onSuivant={onSuivant}
          onTerminer={() => {}}
        />
      )
      fireEvent.keyDown(document, { key: 'Enter' })
      expect(onSuivant).not.toHaveBeenCalled()
    })
  })

  // --- Les cartes de la scene ------------------------------------------------
  // La scene montre les cartes de l'etape ELLE-MEME, lues dans l'index du
  // monde par `carteScene`, jamais sur la table : la table peut etre en
  // avance sur le recit, et la carte revelee y est encore face cachee.
  describe('les cartes de la scene', () => {
    const scan = (id: number, nom: string): ScanCardProps => ({
      id: String(id),
      name: nom,
      kind: 'minion',
      imageUrl: `/scan/${id}`,
    })

    it('montre l auteur, ses boosts et la cible, tous par leur scan', () => {
      const appels: [number, boolean][] = []
      const carteScene = (id: number, faceVisible: boolean) => {
        appels.push([id, faceVisible])
        return scan(id, id === 50 ? 'Klaw' : id === 12 ? 'Colossus' : 'Boost')
      }
      const resolue: EtapeDeroule[] = [
        {
          cle: 'a',
          temps: 'mechant',
          titre: 'attaque',
          regle: 'regle:activations',
          carteId: 50,
          cibleId: 12,
          auteurNom: 'Klaw',
          cibleNom: 'Colossus',
          montant: 4,
          boosts: [{ cle: 'b', nom: 'Whip', cibleId: 77, apport: 1 }],
        },
      ]
      const { container } = render(
        <DeroulePhase etapes={resolue} carteScene={carteScene} onTerminer={() => {}} />
      )
      expect(container.querySelectorAll('.deroule-carte .scan-card')).toHaveLength(3)
      // L'auteur et la cible tels qu'ils sont ; le boost face visible, il est
      // encore face cachee dans le monde de cette trame.
      expect(appels).toEqual(
        expect.arrayContaining([
          [50, false],
          [77, true],
          [12, false],
        ])
      )
      expect(container.querySelector('.deroule-fleche')).not.toBeNull()
      expect(screen.getByText('Boost +1')).toBeInTheDocument()
    })

    it('montre la carte revelee face visible', () => {
      const appels: [number, boolean][] = []
      const carteScene = (id: number, faceVisible: boolean) => {
        appels.push([id, faceVisible])
        return scan(id, 'Captured by Hydra')
      }
      const revelation: EtapeDeroule[] = [
        {
          cle: 'r',
          temps: 'revelation',
          titre: 'revelation',
          regle: 'regle:revelation',
          carteId: 40,
          auteurNom: 'Scott Lang',
          cibleNom: 'Captured by Hydra',
          boosts: [],
        },
      ]
      const { container } = render(
        <DeroulePhase etapes={revelation} carteScene={carteScene} onTerminer={() => {}} />
      )
      // Autant d'appels que de rendus, mais toujours la carte 40, face visible.
      expect(appels.length).toBeGreaterThan(0)
      expect(appels.every(([id, faceVisible]) => id === 40 && faceVisible)).toBe(true)
      expect(container.querySelector('.deroule-carte.est-revelee .scan-card')).not.toBeNull()
      expect(container.querySelector('.deroule-fleche')).toBeNull()
    })

    it('montre un dos de carte pour la distribution', () => {
      const dos: ScanCardProps = {
        id: 'dos',
        name: 'Carte rencontre',
        kind: 'unknown',
        imageUrl: '/scan/encounter',
        facedown: true,
      }
      const distribution: EtapeDeroule[] = [
        {
          cle: 'd',
          temps: 'distribution',
          titre: 'distribution',
          regle: 'regle:distribution',
          auteurNom: 'Scott Lang',
          boosts: [],
        },
      ]
      const { container } = render(
        <DeroulePhase etapes={distribution} dosRencontre={dos} onTerminer={() => {}} />
      )
      expect(container.querySelector('.deroule-carte.est-dos .scan-card')).not.toBeNull()
    })

    // --- Le geste physique --------------------------------------------------
    // Decide avec l'utilisateur le 7 septembre 2026 : un jeton qui tombe sur
    // la carte visee (menace, degats), un boost qui arrive dos visible et se
    // retourne, la carte rencontre qui se retourne sur place.
    it('pose un jeton de menace sur la manigance', () => {
      const menace: EtapeDeroule[] = [
        {
          cle: 'm',
          temps: 'menace',
          titre: 'menace',
          regle: 'regle:menace',
          cibleId: 12,
          cibleNom: 'Hunting Down Heroes',
          montant: 2,
          restant: 7,
          plafond: 12,
          boosts: [],
        },
      ]
      const { container } = render(
        <DeroulePhase etapes={menace} carteScene={(id) => scan(id, 'Hunting Down Heroes')} onTerminer={() => {}} />
      )
      const jeton = container.querySelector('.deroule-carte.est-cible .deroule-jeton.est-menace')
      expect(jeton).not.toBeNull()
      expect(jeton?.textContent).toBe('+2')
    })

    it('pose un jeton de degats sur le heros attaque', () => {
      const attaque: EtapeDeroule[] = [
        {
          cle: 'a',
          temps: 'mechant',
          titre: 'attaque',
          regle: 'regle:activations',
          carteId: 50,
          cibleId: 12,
          auteurNom: 'Klaw',
          cibleNom: 'Colossus',
          etat: 'resolu',
          montant: 3,
          restant: 9,
          boosts: [],
        },
      ]
      const { container } = render(
        <DeroulePhase etapes={attaque} carteScene={(id) => scan(id, String(id))} onTerminer={() => {}} />
      )
      const jeton = container.querySelector('.deroule-carte.est-cible .deroule-jeton.est-degats')
      expect(jeton?.textContent).toBe('3')
    })

    it('ne pose aucun jeton sur une annonce, ni sur un coup a zero', () => {
      const etapes2: EtapeDeroule[] = [
        {
          cle: 'a',
          temps: 'mechant',
          titre: 'attaque',
          regle: 'regle:activations',
          carteId: 50,
          cibleId: 12,
          etat: 'annonce',
          valeurAnnoncee: 2,
          boosts: [],
        },
        {
          cle: 'b',
          temps: 'mechant',
          titre: 'attaque',
          regle: 'regle:activations',
          carteId: 50,
          cibleId: 12,
          etat: 'resolu',
          montant: 0,
          restant: 9,
          boosts: [],
        },
      ]
      const { container } = render(
        <DeroulePhase etapes={etapes2} carteScene={(id) => scan(id, String(id))} onTerminer={() => {}} />
      )
      expect(container.querySelector('.deroule-jeton')).toBeNull()
      fireEvent.click(suivant())
      expect(container.querySelector('.deroule-jeton')).toBeNull()
    })

    it('retourne le boost et la carte revelee, jamais l auteur ni la cible', () => {
      const dos: ScanCardProps = {
        id: 'dos',
        name: 'Carte rencontre',
        kind: 'unknown',
        imageUrl: '/scan/encounter',
        facedown: true,
      }
      const etapes2: EtapeDeroule[] = [
        {
          cle: 'a',
          temps: 'mechant',
          titre: 'attaque',
          regle: 'regle:activations',
          carteId: 50,
          cibleId: 12,
          etat: 'resolu',
          montant: 3,
          boosts: [{ cle: 'b', nom: 'Whip', cibleId: 77, apport: 1 }],
        },
        {
          cle: 'r',
          temps: 'revelation',
          titre: 'revelation',
          regle: 'regle:revelation',
          carteId: 40,
          cibleNom: 'Captured by Hydra',
          boosts: [],
        },
      ]
      const { container } = render(
        <DeroulePhase
          etapes={etapes2}
          carteScene={(id) => scan(id, String(id))}
          dosRencontre={dos}
          onTerminer={() => {}}
        />
      )
      expect(container.querySelector('.deroule-carte.est-boost .deroule-retourne')).not.toBeNull()
      expect(container.querySelector('.deroule-carte.est-auteur .deroule-retourne')).toBeNull()
      expect(container.querySelector('.deroule-carte.est-cible .deroule-retourne')).toBeNull()
      // Le dos du retournement est le dos d'une carte rencontre.
      const dosBoost = container.querySelector('.deroule-carte.est-boost .deroule-retourne-dos img')
      expect(dosBoost?.getAttribute('src')).toBe('/scan/encounter')
      fireEvent.click(suivant())
      expect(container.querySelector('.deroule-carte.est-revelee .deroule-retourne')).not.toBeNull()
    })

    it('ouvre la loupe au survol d une carte de la scene, et la referme', () => {
      // Comme sur la table : pour lire vraiment une carte rencontre.
      // jsdom n'implemente pas ResizeObserver, que l'apercu observe pour se
      // placer : un bouchon inerte suffit ici.
      class ResizeObserverBouchon {
        observe() {}
        unobserve() {}
        disconnect() {}
      }
      vi.stubGlobal('ResizeObserver', ResizeObserverBouchon)
      const { container } = render(
        <DeroulePhase etapes={etapes} carteScene={(id) => scan(id, String(id))} onTerminer={() => {}} />
      )
      fireEvent.click(suivant())
      const figure = container.querySelector('.deroule-carte.est-auteur')
      expect(figure).not.toBeNull()
      expect(document.querySelector('.carte-apercu')).toBeNull()
      fireEvent.mouseEnter(figure as Element)
      expect(document.querySelector('.carte-apercu')).not.toBeNull()
      fireEvent.mouseLeave(figure as Element)
      expect(document.querySelector('.carte-apercu')).toBeNull()
      vi.unstubAllGlobals()
    })

    it('ecrit le nom a la place d une carte dont le scan manque', () => {
      const { container } = render(
        <DeroulePhase etapes={etapes} carteScene={() => undefined} onTerminer={() => {}} />
      )
      // L'etape de menace n'a pas de carte connue ; la suivante a un auteur.
      fireEvent.click(suivant())
      const absentes = container.querySelectorAll('.deroule-carte-absente')
      expect(absentes).toHaveLength(2)
      expect(absentes[0]?.textContent).toBe('Ultron')
      expect(absentes[1]?.textContent).toBe('Shuri')
    })

    it('ne montre aucune carte sur le bilan', () => {
      const { container } = render(
        <DeroulePhase etapes={etapes} phaseMechantEnCours={false} onTerminer={() => {}} />
      )
      // Jusqu'au bilan.
      while (screen.queryByText('À toi de jouer') === null) fireEvent.click(suivant())
      expect(container.querySelector('.deroule-cartes')).toBeNull()
    })
  })

  // --- Le cartouche s'efface devant la question du moteur -------------------
  // Constate en partie (Bruce Banner contre Ultron) : le moteur demandait dans
  // quel ordre activer deux sbires, et le cartouche disait « La suite
  // arrive… » par-dessus la question, bouton compris. Le joueur attendait le
  // moteur, qui l'attendait.
  //
  // Deux attentes, a ne jamais confondre : le moteur retient une trame (le
  // joueur attend le moteur, « La suite arrive… ») ; le moteur pose une
  // question (le moteur attend le joueur, « Le moteur attend ta réponse »).
  describe('question du moteur au joueur', () => {
    const menaceSeule: EtapeDeroule[] = [
      { cle: 'a', temps: 'menace', titre: 'menace', regle: 'regle:menace', boosts: [] },
    ]

    it('se replie sur sa chronologie et dit que le moteur attend le joueur', () => {
      const { container } = render(
        <DeroulePhase etapes={etapes} phaseMechantEnCours questionAuJoueur onTerminer={() => {}} />
      )
      expect(container.querySelectorAll('.deroule-temps li')).toHaveLength(5)
      expect(screen.getByText('Le moteur attend ta réponse')).toBeInTheDocument()
      // Ni titre, ni bouton : rien a lire ni a cliquer ici, c'est la question
      // du moteur qui a la main.
      expect(container.querySelector('.deroule-titre')).toBeNull()
      expect(screen.queryByText('Menace sur la manigance principale')).not.toBeInTheDocument()
      expect(screen.queryByRole('button')).toBeNull()
    })

    it('garde la scene et y loge la question quand on la lui donne', () => {
      // Livraison C de la spec du 7 septembre 2026 : « Defendre ? » se decide
      // en voyant l'attaque, dans la scene, a la place de Suivant.
      const annonce: EtapeDeroule[] = [
        {
          cle: 'activation:1',
          temps: 'mechant',
          titre: 'attaque',
          regle: 'regle:activations',
          carteId: 50,
          cibleId: 12,
          auteurNom: 'Ultron',
          cibleNom: 'Shuri',
          etat: 'annonce',
          valeurAnnoncee: 3,
          boosts: [],
        },
      ]
      const { container } = render(
        <DeroulePhase
          etapes={annonce}
          phaseMechantEnCours
          questionAuJoueur
          question={<button type="button">Défendre</button>}
          onTerminer={() => {}}
        />
      )
      // La scene entiere : chronologie, cartes de l'etape, titre de
      // l'intention, et la question a la place des boutons du cartouche.
      expect(container.querySelector('.deroule-phase.est-replie')).toBeNull()
      expect(container.querySelector('.deroule-cartes')).not.toBeNull()
      expect(screen.getByText('Ultron va attaquer Shuri')).toBeInTheDocument()
      expect(container.querySelector('.deroule-question-scene')).not.toBeNull()
      expect(screen.getByRole('button', { name: 'Défendre' })).toBeInTheDocument()
      expect(screen.queryByText('Suivant')).not.toBeInTheDocument()
      expect(screen.queryByText('Le moteur attend ta réponse')).not.toBeInTheDocument()
      // Le moment ou l'on peut agir change d'aspect : un bandeau « A toi »
      // dans la scene, et la main sort du voile (classe sur le body, lue par
      // board.css).
      expect(container.querySelector('.deroule-a-toi')).not.toBeNull()
      expect(screen.getByText('À toi de jouer')).toBeInTheDocument()
      expect(document.body.classList.contains('deroule-question')).toBe(true)
    })

    it('rend la main au voile une fois la question resolue', () => {
      const scene = (questionAuJoueur: boolean) => (
        <DeroulePhase
          etapes={etapes}
          phaseMechantEnCours
          questionAuJoueur={questionAuJoueur}
          question={questionAuJoueur ? <button type="button">Défendre</button> : undefined}
          onTerminer={() => {}}
        />
      )
      const { rerender, unmount } = render(scene(true))
      expect(document.body.classList.contains('deroule-question')).toBe(true)
      rerender(scene(false))
      expect(document.body.classList.contains('deroule-question')).toBe(false)
      rerender(scene(true))
      unmount()
      expect(document.body.classList.contains('deroule-question')).toBe(false)
    })

    it('se replie comme avant quand la question ne lui est pas donnee', () => {
      // Un ciblage sur la table : la scene laisse la place, la table doit
      // rester cliquable.
      const { container } = render(
        <DeroulePhase etapes={etapes} phaseMechantEnCours questionAuJoueur onTerminer={() => {}} />
      )
      expect(container.querySelector('.deroule-phase.est-replie')).not.toBeNull()
    })

    it('se redeploie sur la meme etape une fois la question resolue', () => {
      const cartouche = (questionAuJoueur: boolean) => (
        <DeroulePhase
          etapes={etapes}
          phaseMechantEnCours
          questionAuJoueur={questionAuJoueur}
          onTerminer={() => {}}
        />
      )
      const { rerender } = render(cartouche(false))
      fireEvent.click(suivant())
      expect(screen.getByText('Ultron attaque Shuri')).toBeInTheDocument()

      rerender(cartouche(true))
      expect(screen.queryByText('Ultron attaque Shuri')).not.toBeInTheDocument()

      // Pas de remise a zero : on revient sur la deuxieme etape, pas la
      // premiere.
      rerender(cartouche(false))
      expect(screen.getByText('Ultron attaque Shuri')).toBeInTheDocument()
      expect(screen.queryByText('Menace sur la manigance principale')).not.toBeInTheDocument()
      expect(screen.queryByText('Le moteur attend ta réponse')).not.toBeInTheDocument()
    })

    it('ne dit JAMAIS que le moteur attend le joueur quand c est le joueur qui attend le moteur', () => {
      // Le moteur retient une trame et calcule la suite : c'est « La suite
      // arrive… », et rien d'autre. Dire ici que le moteur attend une reponse
      // enverrait le joueur chercher une question qui n'existe pas.
      render(
        <DeroulePhase
          etapes={menaceSeule}
          identitePhase={3}
          phaseMechantEnCours
          trameRetenue={11}
          onTerminer={() => {}}
        />
      )
      fireEvent.click(suivant())
      expect(screen.getByText('La suite arrive…')).toBeInTheDocument()
      expect(screen.queryByText('Le moteur attend ta réponse')).not.toBeInTheDocument()
    })

    it('ne dit pas « La suite arrive… » quand c est au joueur d agir', () => {
      // Le cas de la partie reelle, dans l'ordre ou il s'est produit : le
      // joueur a valide tout ce que le cartouche savait (il attend la suite),
      // et la suite est... une question du moteur. « La suite arrive… »
      // mentirait : rien n'arrivera tant que le joueur n'a pas repondu. Le
      // texte d'attente ne s'affiche que lorsque c'est le MOTEUR qu'on attend.
      const cartouche = (questionAuJoueur: boolean) => (
        <DeroulePhase
          etapes={menaceSeule}
          identitePhase={3}
          phaseMechantEnCours
          trameRetenue={11}
          questionAuJoueur={questionAuJoueur}
          onTerminer={() => {}}
        />
      )
      const { rerender } = render(cartouche(false))
      fireEvent.click(suivant())
      expect(screen.getByText('La suite arrive…')).toBeInTheDocument()

      rerender(cartouche(true))
      expect(screen.queryByText('La suite arrive…')).not.toBeInTheDocument()
      expect(screen.getByText('Le moteur attend ta réponse')).toBeInTheDocument()
    })

    it('laisse le clavier a la question : Entree n avance pas un cartouche replie', () => {
      const cartouche = (questionAuJoueur: boolean) => (
        <DeroulePhase
          etapes={etapes}
          phaseMechantEnCours
          questionAuJoueur={questionAuJoueur}
          onTerminer={() => {}}
        />
      )
      const { rerender } = render(cartouche(true))
      fireEvent.keyDown(document, { key: 'Enter' })
      rerender(cartouche(false))
      expect(screen.getByText('Menace sur la manigance principale')).toBeInTheDocument()
    })

    it('ne deroule rien a Echap pendant une question, meme une fois celle-ci resolue', async () => {
      // Echap appartient a la question tant qu'elle est posee : le cartouche
      // n'en retient rien, et ne se met pas a defiler apres coup.
      vi.useFakeTimers()
      try {
        const cartouche = (questionAuJoueur: boolean) => (
          <DeroulePhase
            etapes={etapes}
            phaseMechantEnCours
            questionAuJoueur={questionAuJoueur}
            onTerminer={() => {}}
          />
        )
        const { rerender } = render(cartouche(true))
        document.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape', bubbles: true }))
        rerender(cartouche(false))
        await act(async () => {
          await vi.advanceTimersByTimeAsync(DELAI_DEFILEMENT_MS * 5)
        })
        expect(screen.getByText('Menace sur la manigance principale')).toBeInTheDocument()
        expect(screen.queryByText('Ultron attaque Shuri')).not.toBeInTheDocument()
      } finally {
        vi.useRealTimers()
      }
    })
  })
})

// ---------------------------------------------------------------------- A3 --
// L'ANNONCE avant la resolution, et le cout en clics qu'elle ne doit PAS
// ajouter.
//
// « Deux temps SEULEMENT quand on peut vraiment agir » (decision 7 de la
// spec) : sans question posee au joueur, l'etape ne doit etre vue qu'une fois,
// complete. C'est le mecanisme d'accuse qui en decide — s'il faisait attendre
// un clic sur l'intention, le joueur cliquerait deux fois par activation.
describe("l'annonce d'une activation", () => {
  const annonce: EtapeDeroule = {
    cle: 'activation:1',
    temps: 'mechant',
    titre: 'attaque',
    regle: 'regle:activations',
    etat: 'annonce',
    carteId: 50,
    cibleId: 12,
    auteurNom: 'Klaw',
    cibleNom: 'Colossus',
    valeurAnnoncee: 4,
    boosts: [],
  }
  // LA MEME etape, completee : meme cle, meme place dans la liste.
  const resolue: EtapeDeroule = {
    ...annonce,
    etat: 'resolu',
    valeurAnnoncee: undefined,
    montant: 4,
    restant: 8,
  }

  beforeEach(() => {
    window.localStorage.clear()
  })

  it("dit l'intention au futur proche, avec sa valeur imprimee", () => {
    render(<DeroulePhase etapes={[annonce]} onTerminer={() => {}} />)
    expect(screen.getByText('Klaw va attaquer Colossus')).toBeInTheDocument()
    expect(screen.getByText('→ 4 dégâts annoncés')).toBeInTheDocument()
  })

  // Le cas central : l'etape se COMPLETE sous les yeux du joueur. Il ne recule
  // pas d'une etape, il n'en valide pas une de plus.
  it("complete l'etape sur place, sans faire bouger le joueur", () => {
    const { rerender } = render(
      <DeroulePhase etapes={[annonce]} identitePhase={3} phaseMechantEnCours onTerminer={() => {}} />
    )
    expect(screen.getByText('Klaw va attaquer Colossus')).toBeInTheDocument()
    rerender(
      <DeroulePhase etapes={[resolue]} identitePhase={3} phaseMechantEnCours onTerminer={() => {}} />
    )
    expect(screen.getByText('Klaw attaque Colossus')).toBeInTheDocument()
    expect(screen.queryByText('Klaw va attaquer Colossus')).not.toBeInTheDocument()
    expect(screen.getByText('→ 4 dégâts')).toBeInTheDocument()
  })

  // Le test que la decision 7 reclame mot pour mot : UN accuse, pas deux.
  it("acquitte l'intention tout de suite quand aucune question n'est posee", () => {
    const onSuivant = vi.fn()
    const cartouche = (liste: EtapeDeroule[], trameRetenue: number | undefined) => (
      <DeroulePhase
        etapes={liste}
        identitePhase={3}
        phaseMechantEnCours
        trameRetenue={trameRetenue}
        onSuivant={onSuivant}
        onTerminer={() => {}}
      />
    )
    // Le moteur retient la trame ou il vient d'annoncer l'attaque. Le joueur
    // n'a rien a y faire : le cartouche dit « reçu » sans attendre un clic.
    const { rerender } = render(cartouche([annonce], 11))
    expect(onSuivant).toHaveBeenCalledTimes(1)
    // Le moteur resout et retient la trame suivante : LA, il attend le joueur.
    rerender(cartouche([annonce], undefined))
    rerender(cartouche([resolue], 12))
    expect(onSuivant).toHaveBeenCalledTimes(1)
    expect(screen.getByText('Klaw attaque Colossus')).toBeInTheDocument()
    // Un seul clic pour toute l'activation, comme avant les deux temps.
    fireEvent.click(suivant())
    expect(onSuivant).toHaveBeenCalledTimes(2)
  })

  it("ne dit pas « tu peux défendre » quand le moteur ne pose aucune question", () => {
    render(<DeroulePhase etapes={[annonce]} phaseMechantEnCours onTerminer={() => {}} />)
    expect(screen.queryByText(/tu peux défendre/i)).not.toBeInTheDocument()
  })

  // Le second temps, celui qui compte : le moteur attend une reponse, et le
  // cartouche dit ce qui va arriver pendant qu'on peut encore s'y opposer.
  it("dit la fenetre de reponse quand le moteur pose une question", () => {
    render(
      <DeroulePhase etapes={[annonce]} phaseMechantEnCours questionAuJoueur onTerminer={() => {}} />
    )
    expect(screen.getByText('Klaw va attaquer Colossus')).toBeInTheDocument()
    expect(screen.getByText('tu peux défendre ou répondre')).toBeInTheDocument()
    // Pas de bouton : c'est ailleurs qu'on repond, et « La suite arrive… »
    // serait un mensonge (c'est le moteur qui attend).
    expect(screen.queryByRole('button', { name: /Suivant/i })).not.toBeInTheDocument()
  })

  // Sur une etape ordinaire, le cartouche se replie comme avant : la fenetre
  // de reponse ne s'invite pas partout.
  it("garde le repli ordinaire devant une question sur une etape resolue", () => {
    render(
      <DeroulePhase etapes={[resolue]} phaseMechantEnCours questionAuJoueur onTerminer={() => {}} />
    )
    expect(screen.getByText('Le moteur attend ta réponse')).toBeInTheDocument()
    expect(screen.queryByText(/tu peux défendre/i)).not.toBeInTheDocument()
  })

  it("dit que l'attaque n'a pas lieu quand l'activation est annulee", () => {
    const annulee: EtapeDeroule = { ...annonce, etat: 'annule' }
    render(<DeroulePhase etapes={[annulee]} phaseMechantEnCours onTerminer={() => {}} />)
    expect(screen.getByText("L'attaque n'a pas lieu.")).toBeInTheDocument()
  })

  // L'avance automatique ne doit pas depasser une etape qui n'a pas fini de se
  // completer : le joueur manquerait le seul moment ou elle dit quelque chose.
  it("ne fait pas defiler une intention a l'avance auto", () => {
    vi.useFakeTimers()
    try {
      render(
        <DeroulePhase
          etapes={[annonce, { ...resolue, cle: 'activation:2', auteurNom: 'Drone' }]}
          phaseMechantEnCours
          avanceAuto
          delaiAvanceMs={50}
          onTerminer={() => {}}
        />
      )
      act(() => {
        vi.advanceTimersByTime(500)
      })
      expect(screen.getByText('Klaw va attaquer Colossus')).toBeInTheDocument()
    } finally {
      vi.useRealTimers()
    }
  })
})

// LE RYTHME, mesure en accuses de reception.
//
// Constate en partie reelle (Bishop contre Ultron, mode Detaille, avance auto
// sur Non) : le journal a saute de 192 a 262 en moins de deux secondes, deux
// activations de sbires, la distribution et la revelation resolues sur UN seul
// clic. Le cartouche se croyait a jour parce que le fait RESOLU remplace le
// fait d'intention sous la meme cle, sans allonger la liste : rien ne le
// remettait « en retard ».
//
// La regle que ces cas verrouillent : le cartouche n'est a jour que s'il est
// pose sur la DERNIERE etape connue, et que celle-ci est soit validee DANS SON
// ETAT COURANT, soit une intention sur laquelle le joueur ne peut rien.
describe('le rythme des accuses de reception', () => {
  const annonce: EtapeDeroule = {
    cle: 'activation:1',
    temps: 'sbires',
    titre: 'manigance',
    regle: 'regle:activations',
    etat: 'annonce',
    carteId: 50,
    cibleId: 12,
    auteurNom: 'Drone',
    cibleNom: 'Assault on NORAD',
    valeurAnnoncee: 1,
    boosts: [],
  }
  // LA MEME etape, completee : meme cle, meme place dans la liste.
  const resolue: EtapeDeroule = {
    ...annonce,
    etat: 'resolu',
    valeurAnnoncee: undefined,
    montant: 1,
    restant: 5,
  }
  const menace: EtapeDeroule = {
    cle: 'menace:0:9',
    temps: 'menace',
    titre: 'menace',
    regle: 'regle:menace',
    cibleNom: 'Assault on NORAD',
    montant: 1,
    boosts: [],
  }

  beforeEach(() => {
    window.localStorage.clear()
  })

  /** Le cartouche branche sur un moteur qui retient ses trames une par une. */
  const cartouche = (
    onSuivant: () => void,
    questionAuJoueur = false
  ) => (liste: EtapeDeroule[], trameRetenue: number | undefined) => (
    <DeroulePhase
      etapes={liste}
      identitePhase={3}
      phaseMechantEnCours
      questionAuJoueur={questionAuJoueur}
      trameRetenue={trameRetenue}
      onSuivant={onSuivant}
      onTerminer={() => {}}
    />
  )

  // LE CAS CENTRAL. L'intention est acquittee toute seule (decision 7) ; le
  // fait resolu qui prend sa place est une etape a valider, comme n'importe
  // quelle activation. Sans cela, un clic donne sur l'intention laissait le
  // cartouche « a jour » pour toutes les trames suivantes.
  it("redemande une validation quand le fait resolu remplace l'intention", () => {
    const accuses = vi.fn()
    const vue = cartouche(accuses)
    const { rerender } = render(vue([annonce], 11))
    // L'intention ne coute rien au joueur : elle part toute seule.
    expect(accuses).toHaveBeenCalledTimes(1)
    // Le joueur clique pendant la fenetre d'annonce. Cela ne doit pas valider
    // par avance la resolution, qui n'est pas encore arrivee.
    fireEvent.click(suivant())
    rerender(vue([annonce], undefined))
    rerender(vue([resolue], 12))
    expect(screen.getByText('Drone complote contre Assault on NORAD')).toBeInTheDocument()
    expect(accuses).toHaveBeenCalledTimes(1)
    // C'est LE clic de l'activation : le joueur a lu le resultat.
    fireEvent.click(suivant())
    expect(accuses).toHaveBeenCalledTimes(2)
  })

  // Le fait resolu n'est journalise qu'a la TOUTE FIN de l'activation (cote
  // moteur : apres les degats, les defaites, la riposte). Entre l'intention et
  // lui, le moteur rend plusieurs trames, dont certaines fabriquent des etapes
  // NEUVES (l'accomplissement de la manigance principale, par exemple). Le
  // cartouche doit redevenir en retard des la premiere.
  it("ne relache plus rien des qu'une etape neuve arrive pendant la fenetre d'annonce", () => {
    const accuses = vi.fn()
    const vue = cartouche(accuses)
    const { rerender } = render(vue([annonce], 11))
    expect(accuses).toHaveBeenCalledTimes(1)
    // Une etape de plus, alors que l'intention n'est toujours pas resolue.
    rerender(vue([annonce], undefined))
    rerender(vue([annonce, { ...menace, cle: 'menace:1:9' }], 12))
    expect(accuses).toHaveBeenCalledTimes(1)
    rerender(vue([annonce, { ...menace, cle: 'menace:1:9' }], undefined))
    rerender(vue([annonce, { ...menace, cle: 'menace:1:9' }], 13))
    expect(accuses).toHaveBeenCalledTimes(1)
  })

  // Trois activations d'affilee : trois clics, trois accuses « d'apres
  // resolution », jamais plus.
  it('demande exactement un clic par activation resolue', () => {
    const accuses = vi.fn()
    const vue = cartouche(accuses)
    const inten = (n: number): EtapeDeroule => ({ ...annonce, cle: `activation:${n}` })
    const finie = (n: number): EtapeDeroule => ({ ...resolue, cle: `activation:${n}` })
    let trame = 10
    let liste: EtapeDeroule[] = []
    const trameSuivante = (suite: EtapeDeroule[]) => {
      liste = suite
      rerender(vue(liste, undefined))
      rerender(vue(liste, ++trame))
    }
    const { rerender } = render(vue([inten(1)], trame))
    // Chaque intention part toute seule ; chaque resolution attend son clic.
    const accusesApresClic: number[] = []
    for (let n = 1; n <= 3; n += 1) {
      const debut = liste.slice(0, n - 1).map((_, rang) => finie(rang + 1))
      if (n > 1) trameSuivante([...debut, inten(n)])
      trameSuivante([...debut, finie(n)])
      fireEvent.click(suivant())
      accusesApresClic.push(accuses.mock.calls.length)
    }
    // 3 intentions acquittees toutes seules + 3 clics = 6 accuses, pas un de
    // plus : aucune trame n'est passee sans etre lue.
    expect(accusesApresClic).toEqual([2, 4, 6])
  })

  // Un clic donne sur l'intention ne doit pas FAIRE PERDRE la resolution : le
  // cartouche restait sinon sur « La suite arrive… » (la sortie d'attente ne
  // reagissait qu'a l'allongement de la liste, et la resolution n'allonge
  // rien) et le joueur ne reprenait pied qu'a l'etape suivante.
  it("montre la resolution meme quand le joueur a clique sur l'intention", () => {
    const accuses = vi.fn()
    const vue = cartouche(accuses)
    const { rerender } = render(vue([annonce], 11))
    fireEvent.click(suivant())
    expect(screen.getByText('La suite arrive…')).toBeInTheDocument()
    rerender(vue([annonce], undefined))
    rerender(vue([resolue], 12))
    expect(screen.getByText('Drone complote contre Assault on NORAD')).toBeInTheDocument()
    expect(screen.getByText('→ 1 menace')).toBeInTheDocument()
    expect(screen.queryByText('La suite arrive…')).not.toBeInTheDocument()
  })

  // LA SORTIE DU PIEGE NOMME PAR LA REVUE D'A3-FIX.
  //
  // Le cartouche se REPLIE devant une question du moteur : il n'a alors plus de
  // bouton, donc plus aucun moyen manuel de relacher la trame. Si la question
  // le rendait en meme temps « pas a jour », plus personne n'acquitterait et la
  // phase se figerait jusqu'au filet.
  //
  // Une question est donc une RAISON D'ACQUITTER. Cela ne coute aucun rythme :
  // le moteur ne produit rien de plus tant qu'on ne lui a pas repondu, et c'est
  // meme cet accuse-la qui lui permet d'ARRIVER a sa question (Python :
  // `Render` puis `WaitSync` puis `GetInput`).
  it("acquitte, sans bouton, quand le moteur attend une reponse", () => {
    const accuses = vi.fn()
    const { rerender } = render(cartouche(accuses, true)([annonce], 11))
    expect(accuses).toHaveBeenCalledTimes(1)
    // Replie : la fenetre de reponse est dite, et il n'y a plus de bouton.
    expect(screen.getByText('tu peux défendre ou répondre')).toBeInTheDocument()
    expect(screen.queryByRole('button', { name: /Suivant/i })).toBeNull()
    // Une trame de plus pendant la meme question : elle part aussi, sinon le
    // blocage revient par la porte de derriere.
    rerender(cartouche(accuses, true)([annonce], 12))
    expect(accuses).toHaveBeenCalledTimes(2)
    // La reponse donnee, le moteur resout : le cartouche se redeploie et
    // redemande un clic. Le rythme n'a rien perdu.
    rerender(cartouche(accuses, false)([resolue], 13))
    expect(screen.getByText('Drone complote contre Assault on NORAD')).toBeInTheDocument()
    expect(accuses).toHaveBeenCalledTimes(2)
    fireEvent.click(suivant())
    expect(accuses).toHaveBeenCalledTimes(3)
  })
})

// L'IDENTITE DE L'ETAPE COURANTE. Le cartouche retenait un NUMERO d'etape :
// une revelation qui s'inserait en amont (un Deferlement, par exemple) le
// faisait silencieusement reculer d'un cran, sur une etape deja validee
// (constat F3 de l'audit du 06/09/2026). Il retient desormais la CLE et
// retrouve son index a chaque rendu.
describe('l identite de l etape courante', () => {
  const menace: EtapeDeroule = {
    cle: 'menace:1:0:20',
    temps: 'menace',
    titre: 'menace',
    regle: 'regle:menace',
    cibleNom: 'L’Effraction !',
    montant: 1,
    boosts: [],
  }
  const revelation = (cle: string, heros: string, carte: string): EtapeDeroule => ({
    cle,
    temps: 'revelation',
    titre: 'revelation',
    regle: 'regle:revelation',
    auteurNom: heros,
    cibleNom: carte,
    boosts: [],
  })
  const carteB = revelation('revelation:1:0:2', 'Heros1', 'Carte B')
  const carteA = revelation('revelation:1:1:1', 'Heros0', 'Carte A')

  it('reste sur son etape quand une autre s insere en amont', () => {
    const { rerender } = render(
      <DeroulePhase etapes={[menace, carteB]} phaseMechantEnCours onTerminer={() => {}} />
    )
    fireEvent.click(suivant())
    expect(screen.getByText('Heros1 révèle Carte B')).toBeInTheDocument()
    // Le Deferlement : une revelation de plus, qui passe DEVANT celle qu'on
    // lit parce qu'elle appartient a un joueur plus avance dans l'ordre du
    // tour. Le joueur ne doit pas reculer d'un cran pour autant.
    rerender(
      <DeroulePhase etapes={[menace, carteA, carteB]} phaseMechantEnCours onTerminer={() => {}} />
    )
    expect(screen.getByText('Heros1 révèle Carte B')).toBeInTheDocument()
    expect(screen.queryByText('Heros0 révèle Carte A')).not.toBeInTheDocument()
  })

  it('garde son etape quand la liste est reordonnee sans rien gagner', () => {
    const { rerender } = render(
      <DeroulePhase etapes={[menace, carteA, carteB]} phaseMechantEnCours onTerminer={() => {}} />
    )
    fireEvent.click(suivant())
    fireEvent.click(suivant())
    expect(screen.getByText('Heros1 révèle Carte B')).toBeInTheDocument()
    // Meme liste, autre ordre : rien n'a ete produit, rien ne doit bouger.
    rerender(
      <DeroulePhase etapes={[menace, carteB, carteA]} phaseMechantEnCours onTerminer={() => {}} />
    )
    expect(screen.getByText('Heros1 révèle Carte B')).toBeInTheDocument()
  })

  // LE REPLI QUAND LA COUPE DE DEFAITE EMPORTE TOUT CE QU'ON LISAIT.
  //
  // `arreterSurDefaite` coupe sur l'ORDRE DES TEMPS, pas sur l'ordre d'arrivee
  // des faits : une activation journalisee sous « Reveal Encounter Cards »
  // (une attaque declenchee par une carte revelee, vu en partie reelle) garde
  // le temps `revelation` et reste DEVANT les etapes de revelation apres le
  // tri stable. La coupe emporte donc les deux revelations, dont celle que le
  // joueur lisait ET celle qu'il avait validee. Le repli « premiere etape non
  // validee » renvoyait alors a l'etape 0 : le joueur revenait a la MENACE et
  // ne voyait jamais le coup qui l'a tue (relecture A4).
  it('montre le coup fatal quand la coupe emporte l etape qu on lisait', () => {
    const mortelle: EtapeDeroule = {
      cle: 'fait:9:50',
      temps: 'revelation',
      titre: 'attaque',
      regle: 'regle:activations',
      carteId: 50,
      cibleId: 12,
      auteurNom: 'Ultron',
      cibleNom: 'Shuri',
      etat: 'resolu',
      montant: 6,
      restant: -4,
      defaite: true,
      boosts: [],
    }
    const { rerender } = render(
      <DeroulePhase etapes={[menace, carteA, carteB]} phaseMechantEnCours onTerminer={() => {}} />
    )
    fireEvent.click(suivant())
    fireEvent.click(suivant())
    expect(screen.getByText('Heros1 révèle Carte B')).toBeInTheDocument()
    // La carte revelee frappe, et le heros tombe.
    rerender(
      <DeroulePhase
        etapes={[menace, mortelle, carteA, carteB]}
        phaseMechantEnCours
        onTerminer={() => {}}
      />
    )
    expect(screen.getByText('Shuri est vaincu')).toBeInTheDocument()
    expect(screen.queryByText('Menace sur la manigance principale')).not.toBeInTheDocument()
  })

  // Le repli ORDINAIRE, quand la cle retenue disparait sans coupe de defaite :
  // la premiere etape NON VALIDEE.
  it('se replie sur la premiere etape non validee quand sa cle disparait', () => {
    const { rerender } = render(
      <DeroulePhase etapes={[menace, carteA, carteB]} phaseMechantEnCours onTerminer={() => {}} />
    )
    fireEvent.click(suivant())
    expect(screen.getByText('Heros0 révèle Carte A')).toBeInTheDocument()
    // Carte A s'en va (une defaite survenue plus tot coupe le deroule derriere
    // elle) : la menace reste la seule etape validee, donc on repart de celle
    // qui la suit.
    rerender(<DeroulePhase etapes={[menace, carteB]} phaseMechantEnCours onTerminer={() => {}} />)
    expect(screen.getByText('Heros1 révèle Carte B')).toBeInTheDocument()
  })
})

// LE MULTIJOUEUR DIT CE QU'IL ATTEND (constat F5 de l'audit du 06/09/2026).
//
// Le moteur n'avance qu'une fois TOUS les clients a jour, et il n'interroge
// qu'un joueur a la fois. « La suite arrive… » disait la meme chose dans les
// deux cas, et dans un troisieme : le moteur qui calcule.
describe("l'attente d'un autre joueur", () => {
  const deux: EtapeDeroule[] = [
    { cle: 'a', temps: 'menace', titre: 'menace', regle: 'regle:menace', boosts: [] },
  ]

  /** Valide la derniere etape connue : le cartouche entre alors en attente. */
  const epuiser = () => fireEvent.click(suivant())

  it('nomme le joueur que la table attend, au lieu de parler du moteur', () => {
    render(
      <DeroulePhase
        etapes={deux}
        phaseMechantEnCours
        attendUnAutreJoueur
        nomJoueurAttendu="Spider-Man"
        onTerminer={() => {}}
      />
    )
    epuiser()
    expect(screen.getByText('En attente de Spider-Man')).toBeInTheDocument()
    expect(screen.queryByText('La suite arrive…')).not.toBeInTheDocument()
  })

  it('dit au moins qu on attend quelqu un quand le moteur ne dit pas qui', () => {
    render(
      <DeroulePhase etapes={deux} phaseMechantEnCours attendUnAutreJoueur onTerminer={() => {}} />
    )
    epuiser()
    expect(screen.getByText("En attente d'un autre joueur")).toBeInTheDocument()
  })

  it('parle du moteur quand on n attend personne d autre', () => {
    render(<DeroulePhase etapes={deux} phaseMechantEnCours onTerminer={() => {}} />)
    epuiser()
    expect(screen.getByText('La suite arrive…')).toBeInTheDocument()
  })
})

// LA DEFAITE D'UN AUTRE JOUEUR (constat F5 de l'audit du 06/09/2026).
//
// `arreterSurDefaite` coupait le deroule chez TOUS les clients. Si le heros du
// joueur A tombait a la deuxieme activation, le cartouche de B ne montrait
// jamais l'attaque que B a subie ensuite : la decision 13 (« la phase s'arrete
// ici ») avait ete ecrite en pensant au solo.
describe('la chute du heros d un autre joueur', () => {
  const NOTRE_HEROS = 12
  const SON_HEROS = 77

  const attaque = (cle: string, cibleId: number, nom: string, defaite?: true): EtapeDeroule => ({
    cle,
    temps: 'sbires',
    titre: 'attaque',
    regle: 'regle:activations',
    carteId: 50,
    cibleId,
    auteurNom: 'Drone',
    cibleNom: nom,
    etat: 'resolu',
    montant: 4,
    restant: defaite ? -1 : 5,
    boosts: [],
    ...(defaite ? { defaite } : {}),
  })

  const liste = [
    attaque('a', SON_HEROS, 'Colossus', true),
    attaque('b', NOTRE_HEROS, 'Shuri'),
  ]

  it('marque l etape mais laisse la phase continuer', () => {
    const onDefaiteVue = vi.fn()
    render(
      <DeroulePhase
        etapes={liste}
        phaseMechantEnCours
        herosLocauxIds={new Set([NOTRE_HEROS])}
        onDefaiteVue={onDefaiteVue}
        onTerminer={() => {}}
      />
    )
    // La chute est DITE : elle reste le moment le plus important de la partie,
    // meme quand elle n'est pas la notre.
    expect(screen.getByText('Colossus est vaincu')).toBeInTheDocument()
    // Mais rien ne s'arrete : ni la mention d'arret, ni le bouton « Continuer ».
    expect(screen.queryByText("La phase s'arrête ici.")).not.toBeInTheDocument()
    expect(screen.queryByRole('button', { name: /Continuer/i })).toBeNull()
    fireEvent.click(suivant())
    expect(screen.getByText('Drone attaque Shuri')).toBeInTheDocument()
    expect(onDefaiteVue).not.toHaveBeenCalled()
  })

  it('arrete tout chez le joueur dont le heros est tombe', () => {
    const onDefaiteVue = vi.fn()
    render(
      <DeroulePhase
        etapes={liste}
        phaseMechantEnCours
        herosLocauxIds={new Set([SON_HEROS])}
        onDefaiteVue={onDefaiteVue}
        onTerminer={() => {}}
      />
    )
    expect(screen.getByText('Colossus est vaincu')).toBeInTheDocument()
    expect(screen.getByText("La phase s'arrête ici.")).toBeInTheDocument()
    fireEvent.click(screen.getByRole('button', { name: /Continuer/i }))
    expect(onDefaiteVue).toHaveBeenCalledTimes(1)
  })
})

// LE COMPTE A REBOURS DU FILET ANTI-BLOCAGE.
//
// Le filet relache la phase au bout de 90 s pour qu'un onglet fantome ne gele
// pas la table entiere. Sans un mot, le joueur voit la phase repartir seule et
// ne comprend pas pourquoi : le cartouche annonce donc les quinze dernieres
// secondes, discretement.
describe('le compte a rebours du filet', () => {
  const etape: EtapeDeroule = {
    cle: 'a',
    temps: 'menace',
    titre: 'menace',
    regle: 'regle:menace',
    boosts: [],
  }

  beforeEach(() => {
    vi.useFakeTimers()
    window.localStorage.clear()
  })
  afterEach(() => {
    vi.useRealTimers()
  })

  const vue = (echeanceFilet?: number) => (
    <DeroulePhase
      etapes={[etape]}
      phaseMechantEnCours
      echeanceFilet={echeanceFilet}
      onTerminer={() => {}}
    />
  )

  it('ne dit rien tant que l echeance est loin', () => {
    render(vue(Date.now() + DELAI_ALERTE_FILET_MS + 5_000))
    expect(screen.queryByText(/La phase reprend dans/)).not.toBeInTheDocument()
  })

  it('annonce les dernieres secondes', () => {
    render(vue(Date.now() + 12_000))
    expect(screen.getByText('La phase reprend dans 12 s')).toBeInTheDocument()
  })

  it('descend de seconde en seconde', () => {
    render(vue(Date.now() + 12_000))
    act(() => {
      vi.advanceTimersByTime(3_000)
    })
    expect(screen.getByText('La phase reprend dans 9 s')).toBeInTheDocument()
  })

  it('ne dit rien quand aucun filet n est arme', () => {
    render(vue(undefined))
    expect(screen.queryByText(/La phase reprend dans/)).not.toBeInTheDocument()
  })
})

// « TEMPS PAR DECISION » NON NUL : l'hypothese du mode Detaille tombe.
//
// Le mode suppose que le moteur ne produit rien tant qu'on ne lui a pas
// repondu. Un `max_timeout` regle a la preparation fait expirer `DoWaitSync` et
// `DoGetInput`, et le moteur poursuit sans notre accuse ni notre reponse. Le
// cartouche ne change RIEN a son rythme : il le dit, et c'est tout.
describe('la mention du temps par decision', () => {
  const etape: EtapeDeroule = {
    cle: 'a',
    temps: 'menace',
    titre: 'menace',
    regle: 'regle:menace',
    boosts: [],
  }

  const MENTION = /Temps par décision réglé/

  const vue = (tempsParDecision?: number, questionAuJoueur = false) => (
    <DeroulePhase
      etapes={[etape]}
      phaseMechantEnCours
      questionAuJoueur={questionAuJoueur}
      tempsParDecision={tempsParDecision}
      onTerminer={() => {}}
    />
  )

  it('ne dit rien quand le champ est nul, ni quand il est absent', () => {
    const { unmount } = render(vue(0))
    expect(screen.queryByText(MENTION)).not.toBeInTheDocument()
    unmount()
    render(vue(undefined))
    expect(screen.queryByText(MENTION)).not.toBeInTheDocument()
  })

  it('le dit quand le champ est non nul', () => {
    render(vue(30))
    expect(screen.getByText(MENTION)).toBeInTheDocument()
  })

  // Le cartouche replie devant une question du moteur est justement le moment
  // ou `DoGetInput` expire : la mention y a le plus de sens.
  it('le dit aussi quand le cartouche est replie devant une question', () => {
    render(vue(30, true))
    expect(screen.getByText(MENTION)).toBeInTheDocument()
  })
})

// LE CARTOUCHE FANTOME DE LA PARTIE MORTE, mesure en jeu le 07/09/2026.
//
// Le moteur publie l'etiquette de partie (`partieId`) des la reception de la
// trame, et le monde a la fin de la lecture qui suit : il y a donc au moins un
// rendu ou la partie est NEUVE et le monde encore celui d'avant. La memoire des
// etapes, videe par le changement de partie, se remplissait a nouveau dans ce
// rendu-la, et le cartouche affichait « The Break-In! gagne 1 menace 3/7 » avec
// son bouton « Suivant » en plein tour du joueur d'une AUTRE partie.
describe('une partie neuve n herite pas des etapes de la precedente', () => {
  const menace: EtapeDeroule = {
    cle: 'menace:3:0:20',
    temps: 'menace',
    titre: 'menace',
    regle: 'regle:menace',
    cibleNom: 'The Break-In!',
    montant: 1,
    boosts: [],
  }

  beforeEach(() => {
    window.localStorage.clear()
  })

  it('ignore les etapes du monde perime arrive apres la nouvelle etiquette', () => {
    const { container, rerender } = render(
      <DeroulePhase
        etapes={[menace]}
        identitePhase={3}
        identitePartie="partie-A"
        phaseMechantEnCours
        onTerminer={() => {}}
      />
    )
    expect(screen.getByText('The Break-In! gagne 1 menace')).toBeInTheDocument()

    // LE RENDU INTERMEDIAIRE : etiquette neuve, monde encore celui d'avant.
    rerender(
      <DeroulePhase
        etapes={[menace]}
        identitePhase={3}
        identitePartie="partie-B"
        phaseMechantEnCours
        onTerminer={() => {}}
      />
    )
    // Puis le monde de la partie neuve : round 1, tour du joueur, aucune etape.
    rerender(
      <DeroulePhase etapes={[]} identitePhase={1} identitePartie="partie-B" onTerminer={() => {}} />
    )
    expect(container).toBeEmptyDOMElement()
  })

  it('raconte normalement la premiere phase de la partie neuve', () => {
    const neuve: EtapeDeroule = { ...menace, cle: 'menace:1:0:20', cibleNom: 'Assault on NORAD' }
    const { rerender } = render(
      <DeroulePhase
        etapes={[menace]}
        identitePhase={3}
        identitePartie="partie-A"
        phaseMechantEnCours
        onTerminer={() => {}}
      />
    )
    rerender(
      <DeroulePhase
        etapes={[menace]}
        identitePhase={3}
        identitePartie="partie-B"
        phaseMechantEnCours
        onTerminer={() => {}}
      />
    )
    rerender(
      <DeroulePhase etapes={[]} identitePhase={1} identitePartie="partie-B" onTerminer={() => {}} />
    )
    // La phase du mechant de la partie neuve : le cartouche revient, sur SES
    // etapes. La garde ne doit pas l'avoir eteint pour de bon.
    rerender(
      <DeroulePhase
        etapes={[neuve]}
        identitePhase={1}
        identitePartie="partie-B"
        phaseMechantEnCours
        onTerminer={() => {}}
      />
    )
    expect(screen.getByText('Assault on NORAD gagne 1 menace')).toBeInTheDocument()
  })

  // LE GARDE-FOU. Tant que la garde court, le cartouche est MUET, et rien ne la
  // releve qu'une liste d'etapes vide. Si cette liste ne venait jamais (le monde
  // perime porte des etapes, et la partie neuve enchaine), la reposer a chaque
  // bascule la rendrait definitive : cartouche eteint pour le reste de la
  // session. Elle tombe donc a la deuxieme bascule.
  it('ne reste pas armee quand deux parties s enchainent sans liste vide', () => {
    const vue = (partie: string) => (
      <DeroulePhase
        etapes={[menace]}
        identitePhase={3}
        identitePartie={partie}
        phaseMechantEnCours
        onTerminer={() => {}}
      />
    )
    const { container, rerender } = render(vue('partie-A'))
    expect(screen.getByText('The Break-In! gagne 1 menace')).toBeInTheDocument()

    // Premiere bascule : la garde s'arme, le cartouche se tait.
    rerender(vue('partie-B'))
    expect(container).toBeEmptyDOMElement()

    // Deuxieme bascule sans que la liste vide attendue ne soit jamais venue :
    // la garde tombe plutot que de se reposer.
    rerender(vue('partie-C'))
    expect(screen.getByText('The Break-In! gagne 1 menace')).toBeInTheDocument()
  })
})
