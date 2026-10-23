// Le cartouche du deroule : une etape a la fois, validee avant la suivante.
//
// Il est FIXE en bas au centre et ne bouge jamais d'une etape a l'autre :
// l'oeil sait ou lire et la main ou cliquer des le deuxieme tour. « En bas »
// s'entend au-dessus de la MAIN du joueur, jamais par-dessus elle. On peut revenir en arriere pour relire,
// ce qui ne rejoue rien dans la partie : c'est une relecture, pas un undo.
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { act, fireEvent, render } from '@testing-library/react'
import { DELAI_ALERTE_FILET_MS, DeroulePhase } from './DeroulePhase'
import { CartoucheHorsPhase } from './CartouchePhase'
import type { EtapeDeroule } from './deroule-phase'
import type { ScanCardProps } from '../components/ScanCard'
import { ecran as screen } from '../test-textes'
import { ecrireDelaiAutoPhase } from './moteur'
import type { Demande, Option } from './ask'
import type { Interaction } from './interaction'
import type { QuestionDuMoteur } from './sous-cadre'

// Les requetes de texte tolerantes a une phrase decoupee : voir
// `src/test-textes.ts`, qui dit pourquoi elles existent.

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
//
// ⚠ DEPUIS LE 04/10/2026, LES TEMPS VIDES ONT LEUR ETAPE (« Aucun sbire engagé »,
// frise-phase.ts) : le raccourci les traverse d'abord, d'un « Suivant » chacune.
// Seules les etapes VIDES sont traversees : une vraie etape restante fait
// echouer le test comme avant.
const ETAPE_VIDE = /^(Aucune menace posée|Le méchant ne s’active pas|Aucun sbire engagé|Aucune carte rencontre distribuée|Rien à révéler)$/
// LA PHRASE DE L'ETAPE LUE (refonte du cartouche, 05/10/2026). Le cartouche du
// bas (scene PC) ne l'ecrit plus en toutes lettres : il dessine la rangee, et
// la phrase devient le nom accessible de son corps. Le telephone et la table
// l'ecrivent toujours en titre.
const etapeLue = () =>
  document.querySelector('.deroule-corps')?.getAttribute('aria-label') ??
  document.querySelector('.deroule-titre')?.textContent ??
  ''
const traverserLesVides = () => {
  for (let garde = 0; garde < 6 && ETAPE_VIDE.test(etapeLue()); garde++) {
    fireEvent.click(screen.getByRole('button', { name: /Suivant/i }))
  }
}
// Le bouton du BILAN : « Terminer » dans le cartouche du bas, « À toi de
// jouer » sur le telephone et la table.
const terminer = () => {
  traverserLesVides()
  return screen.getByRole('button', { name: /^(Terminer|À toi de jouer)$/i })
}

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
    expect(etapeLue()).toBe('Menace sur la manigance principale')
    expect(etapeLue()).not.toBe('Ultron attaque Shuri')
  })

  it('une attaque rangee sous Revelation garde le nom de sa CIBLE', () => {
    // Le vilain qu'une carte revelee fait frapper une seconde fois est range
    // sous « Revelation » (le fait porte sa phase). La traduction des noms ne
    // doit pas prendre l'auteur pour la cible : « Klaw attaque Klaw ».
    const seconde: EtapeDeroule[] = [
      {
        cle: 'r',
        temps: 'revelation',
        titre: 'attaque',
        regle: 'regle:revelation',
        carteId: 50,
        cibleId: 12,
        auteurNom: 'Klaw',
        cibleNom: 'Colossus',
        boosts: [],
      },
    ]
    const nomFr = (id: number) => ({ 50: 'Klaw', 12: 'Colossus' })[id]
    render(<DeroulePhase etapes={seconde} onTerminer={() => {}} nomFr={nomFr} />)
    expect(etapeLue()).toBe('Klaw attaque Colossus')
    expect(etapeLue()).not.toBe('Klaw attaque Klaw')
  })

  it('⚠ une REVELATION garde le nom du HEROS qui revele, pas celui de la carte', () => {
    // LE DEFAUT SIGNALE DEUX FOIS le 14/09/2026 : « Maîtres du Chaos révèle
    // Maîtres du Chaos », puis « L'Homme-Radioactif révèle L'Homme-Radioactif ».
    //
    // Sur une revelation, `carteId` designe la carte REVELEE ; l'auteur, lui,
    // est le HEROS, et il n'a pas d'identifiant dans l'etape. Traduire l'auteur
    // par `carteId` remplacait donc le nom du heros par celui de la carte, des
    // DEUX cotes de la phrase.
    //
    // ⚠ CLASSE « NON REPRODUIT » A TORT une premiere fois : une capture
    // d'autoplay montrait `joueur_nom` correct, et j'en avais conclu qu'il n'y
    // avait rien. Le defaut n'etait pas dans la DONNEE, il etait dans
    // l'AFFICHAGE. Une donnee juste ne prouve pas un affichage juste.
    //
    // Le cas jumeau, juste au-dessus, garde la CIBLE depuis le 09/09/2026 :
    // le meme piege, a une ligne d'ecart.
    const revelation: EtapeDeroule[] = [
      {
        cle: 'rev',
        temps: 'revelation',
        titre: 'revelation',
        regle: 'regle:revelation',
        // La carte revelee, et elle seule, porte un identifiant.
        carteId: 77,
        auteurNom: 'Jessica Jones',
        cibleNom: 'Masters of Evil',
        boosts: [],
      },
    ]
    const nomFr = (id: number) => ({ 77: 'Maîtres du Chaos' })[id]
    render(<DeroulePhase etapes={revelation} onTerminer={() => {}} nomFr={nomFr} />)
    expect(etapeLue()).toBe('Jessica Jones révèle Maîtres du Chaos')
    expect(etapeLue()).not.toBe('Maîtres du Chaos révèle Maîtres du Chaos')
  })

  it('avance d une etape au clic sur Suivant', () => {
    render(<DeroulePhase etapes={etapes} onTerminer={() => {}} />)
    fireEvent.click(suivant())
    expect(etapeLue()).toBe('Ultron attaque Shuri')
  })

  it('ne rappelle plus la regle de l etape (retiree le 03/10/2026)', () => {
    render(<DeroulePhase etapes={etapes} onTerminer={() => {}} />)
    expect(screen.queryByText(/Point 1/)).toBeNull()
  })

  it('revient en arriere sans rien rejouer', () => {
    render(<DeroulePhase telephone etapes={etapes} onTerminer={() => {}} />)
    fireEvent.click(suivant())
    fireEvent.click(screen.getByRole('button', { name: /Précédent/i }))
    expect(etapeLue()).toBe('Menace sur la manigance principale')
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
    fireEvent.click(terminer())
    expect(onTerminer).toHaveBeenCalledTimes(1)
  })

  it('ne rend rien sans etape', () => {
    const { container } = render(<DeroulePhase etapes={[]} onTerminer={() => {}} />)
    expect(container).toBeEmptyDOMElement()
  })

  // Multi, 11/10/2026 : au debut de la phase, l'hote est interroge avant la
  // premiere etape ; sur telephone (rendu d'avant) et sur la table, les autres
  // joueurs ne voyaient rien. Ils voient maintenant qui on attend.
  it.each([
    ['telephone', { telephone: true }],
    ['sur la table', { presentation: 'table' as const }],
  ])('sans etape, un autre joueur interroge (%s) : « En attente de Black Panther »', (_nom, mode) => {
    render(
      <DeroulePhase
        etapes={[]}
        phaseMechantEnCours
        attendUnAutreJoueur
        nomJoueurAttendu="Black Panther"
        onTerminer={() => {}}
        {...mode}
      />
    )
    expect(screen.getByText('En attente de Black Panther')).toBeInTheDocument()
    expect(screen.queryAllByRole('button')).toHaveLength(0)
  })

  it('sans etape, personne d autre attendu : toujours rien (solo)', () => {
    const { container } = render(<DeroulePhase etapes={[]} phaseMechantEnCours telephone onTerminer={() => {}} />)
    expect(container).toBeEmptyDOMElement()
  })

  it('disparait une fois la derniere etape validee', () => {
    // Defaut constate en partie reelle : onTerminer ne suffit pas a faire
    // disparaitre le cartouche si l'appelant n'en fait rien (board.tsx passe
    // un no-op). Le composant doit se masquer lui-meme.
    const { container } = render(<DeroulePhase etapes={etapes} onTerminer={() => {}} />)
    fireEvent.click(suivant())
    fireEvent.click(suivant())
    fireEvent.click(terminer())
    expect(container).toBeEmptyDOMElement()
  })

  it('ferme le cartouche quand la derniere etape est validee au CLAVIER', () => {
    // Depuis le correctif de fermeture, c'est avancer() qui fait disparaitre
    // le cartouche : ce chemin n'etait verifie qu'au clic, jamais au clavier,
    // alors que les deux passent par la meme fonction.
    render(<DeroulePhase etapes={etapes} onTerminer={() => {}} />)
    // Menace, mechant, puis les trois temps vides (sbires, distribution,
    // revelation), puis le bilan : six Entree.
    for (let i = 0; i < 6; i++) fireEvent.keyDown(document, { key: 'Enter' })
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
    fireEvent.click(terminer())
    expect(container).toBeEmptyDOMElement()

    const etapesSuivantes: EtapeDeroule[] = [
      { cle: 'x', temps: 'menace', titre: 'menace', regle: 'regle:menace', boosts: [] },
    ]
    rerender(<DeroulePhase etapes={etapesSuivantes} identitePhase={2} onTerminer={() => {}} />)
    expect(etapeLue()).toBe('Menace sur la manigance principale')
  })

  it('ne revient pas a la premiere etape quand le tableau est juste RECREE', () => {
    // board.tsx recalcule `etapes` a chaque trame du moteur (useMemo dont une
    // dependance change d'identite en permanence). Un tableau de MEME CONTENU
    // mais de nouvelle identite ne doit ni faire reculer l'etape courante, ni
    // rouvrir un cartouche deja termine : sinon il se rouvre au round suivant,
    // pendant le tour du joueur, par-dessus le bouton de fin de tour.
    const { rerender } = render(<DeroulePhase etapes={etapes} onTerminer={() => {}} />)
    fireEvent.click(suivant())
    expect(etapeLue()).toBe('Ultron attaque Shuri')

    // Meme contenu, nouvelle identite de tableau ET des objets qu'il contient.
    const memeContenuIdentiteNeuve: EtapeDeroule[] = etapes.map((e) => ({ ...e }))
    rerender(<DeroulePhase etapes={memeContenuIdentiteNeuve} onTerminer={() => {}} />)
    expect(etapeLue()).toBe('Ultron attaque Shuri')
    expect(etapeLue()).not.toBe('Menace sur la manigance principale')
  })

  it('ne rouvre pas un cartouche deja termine quand le tableau est juste RECREE', () => {
    const { container, rerender } = render(
      <DeroulePhase etapes={etapes} onTerminer={() => {}} />
    )
    fireEvent.click(suivant())
    fireEvent.click(suivant())
    fireEvent.click(terminer())
    expect(container).toBeEmptyDOMElement()

    const memeContenuIdentiteNeuve: EtapeDeroule[] = etapes.map((e) => ({ ...e }))
    rerender(<DeroulePhase etapes={memeContenuIdentiteNeuve} onTerminer={() => {}} />)
    expect(container).toBeEmptyDOMElement()
  })

  it('montre les cinq pastilles (le Bilan compris), celle en cours mise en avant', () => {
    // D15, D34 : la distribution et la revelation n'en font qu'une, « 3. Cartes
    // rencontre ». Le telephone garde ses six onglets (plus bas).
    const { container } = render(<DeroulePhase etapes={etapes} onTerminer={() => {}} />)
    const pastilles = container.querySelectorAll('.deroule-pastille')
    expect(pastilles).toHaveLength(5)
    expect(pastilles[4].getAttribute('title')).toBe('Bilan')
    expect(container.querySelector('.deroule-pastille.est-courant')?.getAttribute('title')).toMatch(/menaces/i)
  })

  it('marque comme passe un temps deja valide', () => {
    // `etapes` : menace puis mechant. Une fois la menace validee, elle doit
    // porter la marque de validation, pas rester « a venir ».
    render(<DeroulePhase telephone etapes={etapes} onTerminer={() => {}} />)
    fireEvent.click(suivant())
    const menaceLi = [...document.querySelectorAll('.deroule-temps li')].find((li) =>
      li.textContent?.match(/Menace/i)
    )
    expect(menaceLi?.className).toContain('est-passe')
  })

  // ⚠ RENDU DU TELEPHONE (et de la table) : la frise des six onglets y reste.
  // Les cinq pastilles du cartouche du bas ont leurs cas dans
  // vue-cartouche.test.ts et CartouchePhase.test.tsx.
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
    const { container } = render(<DeroulePhase telephone etapes={etapes} onTerminer={() => {}} />)
    fireEvent.click(suivant())
    fireEvent.click(suivant())
    traverserLesVides()
    expect(etapeLue()).toBe('Fin de la phase du méchant')
    const sbires = temps(container, /Sbires/i)
    expect(sbires?.className).toContain('est-vide')
    expect(sbires?.textContent).toMatch(/Aucun/i)
  })

  it('dit « a venir », pas « vide », d un temps qui n est pas encore passe', () => {
    // Deux sbires pas encore actives : le cartouche est sur l'activation du
    // mechant, la phase court, et aucune etape de sbire n'existe encore. Le
    // temps est A VENIR : ni barre, ni « aucun ».
    const { container } = render(
      <DeroulePhase telephone etapes={etapes} phaseMechantEnCours onTerminer={() => {}} />
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
      <DeroulePhase telephone etapes={sansMenace} phaseMechantEnCours onTerminer={() => {}} />
    )
    const menace = temps(container, /Menace/i)
    expect(menace?.className).toContain('est-vide')
    expect(menace?.textContent).toMatch(/Aucun/i)
  })

  it('met en avant le temps de l etape affichee, et lui seul', () => {
    const { container } = render(
      <DeroulePhase telephone etapes={etapes} phaseMechantEnCours onTerminer={() => {}} />
    )
    expect(container.querySelectorAll('.deroule-temps li.est-courant')).toHaveLength(1)
    expect(temps(container, /Menace/i)?.className).toContain('est-courant')
    fireEvent.click(suivant())
    expect(container.querySelectorAll('.deroule-temps li.est-courant')).toHaveLength(1)
    expect(temps(container, /Méchant/i)?.className).toContain('est-courant')
    expect(temps(container, /Menace/i)?.className).toContain('est-passe')
  })

  it('un temps vide a son etape courte, avec Suivant (decision du 03/10/2026)', () => {
    // Menace, mechant, distribution : les sbires et la revelation n'ont rien
    // produit. Chacun est DIT par une etape courte qui coute un clic, au lieu
    // d'etre saute en silence.
    const onTerminer = vi.fn()
    const sansSbiresNiRevelation: EtapeDeroule[] = [
      { cle: 'a', temps: 'menace', titre: 'menace', regle: 'regle:menace', boosts: [] },
      { cle: 'b', temps: 'mechant', titre: 'attaque', regle: 'regle:activations', boosts: [] },
      { cle: 'c', temps: 'distribution', titre: 'distribution', regle: '', boosts: [] },
    ]
    render(<DeroulePhase etapes={sansSbiresNiRevelation} onTerminer={onTerminer} />)
    fireEvent.click(suivant())
    fireEvent.click(suivant())
    expect(etapeLue()).toBe('Aucun sbire engagé')
    fireEvent.click(suivant())
    fireEvent.click(suivant())
    expect(etapeLue()).toBe('Rien à révéler')
    fireEvent.click(suivant())
    expect(onTerminer).not.toHaveBeenCalled()
    fireEvent.click(terminer())
    expect(onTerminer).toHaveBeenCalledTimes(1)
  })

  it('les onglets passes portent leur resultat court', () => {
    const coups: EtapeDeroule[] = [
      { cle: 'a', temps: 'menace', titre: 'menace', regle: '', cibleNom: 'Effraction', montant: 1, boosts: [] },
      { cle: 'b', temps: 'mechant', titre: 'attaque', etat: 'resolu', regle: '', auteurNom: 'Rhino', cibleNom: 'Shuri', montant: 3, boosts: [] },
    ]
    const { container } = render(<DeroulePhase telephone etapes={coups} phaseMechantEnCours onTerminer={() => {}} />)
    expect(container.querySelector('.deroule-onglet-resume')).toBeNull()
    fireEvent.click(suivant())
    expect(temps(container, /Menace/i)?.querySelector('.deroule-onglet-resume')?.textContent).toBe('+1 menace')
    expect(temps(container, /Méchant/i)?.querySelector('.deroule-onglet-resume')).toBeNull()
  })

  it('avance a la touche Entree', () => {
    // fireEvent (et non document.dispatchEvent) : setIndex declenche un
    // rendu, et fireEvent l'enveloppe dans un act() pour eviter
    // l'avertissement React sur une mise a jour hors act().
    render(<DeroulePhase etapes={etapes} onTerminer={() => {}} />)
    fireEvent.keyDown(document, { key: 'Enter' })
    expect(etapeLue()).toBe('Ultron attaque Shuri')
  })

  it('avance aussi a la barre d espace', () => {
    render(<DeroulePhase etapes={etapes} onTerminer={() => {}} />)
    fireEvent.keyDown(document, { key: ' ' })
    expect(etapeLue()).toBe('Ultron attaque Shuri')
  })

  it('supporte de passer de zero etape a plusieurs sans tomber', () => {
    // Le plateau monte ce composant des que le mode « detaille » est actif,
    // donc hors phase du mechant, avec une liste vide. Si le `return null`
    // court-circuite un hook, React compte un hook de plus au rendu suivant
    // et fait tomber tout le plateau.
    const { rerender } = render(<DeroulePhase etapes={[]} onTerminer={() => {}} />)
    rerender(<DeroulePhase etapes={etapes} onTerminer={() => {}} />)
    expect(etapeLue()).toBe('Menace sur la manigance principale')
  })

  it('laisse le clavier tranquille quand on ecrit ailleurs', () => {
    // Le tchat est a portee de main pendant la phase : taper un espace dans son
    // champ ne doit pas faire avancer la phase du mechant.
    render(<DeroulePhase etapes={etapes} onTerminer={() => {}} />)
    const champ = document.createElement('input')
    document.body.append(champ)
    champ.focus()
    champ.dispatchEvent(new KeyboardEvent('keydown', { key: ' ', bubbles: true }))
    expect(etapeLue()).toBe('Menace sur la manigance principale')
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
    expect(etapeLue()).toBe('Menace sur la manigance principale')
    expect(etapeLue()).not.toBe('Ultron attaque Shuri')
    autreBouton.remove()
  })

  it('avance quand meme au clavier depuis le bouton Suivant du cartouche', () => {
    // Le bouton Suivant est un bouton comme un autre, mais IL EST le
    // cartouche : la restriction ci-dessus ne doit pas le neutraliser.
    render(<DeroulePhase etapes={etapes} onTerminer={() => {}} />)
    fireEvent.keyDown(suivant(), { key: 'Enter' })
    expect(etapeLue()).toBe('Ultron attaque Shuri')
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
        telephone
        etapes={attaque}
        pvMaxParNom={new Map([['Colossus', 14]])}
        onTerminer={() => {}}
      />
    )
    expect(etapeLue()).toBe('Klaw attaque Colossus')
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
    render(<DeroulePhase telephone etapes={deuxSbires} onTerminer={() => {}} />)
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
    expect(etapeLue()).toBe('Ultron attaque Shuri')
    // Aucune trame retenue : il n'y a rien a acquitter, donc rien ne part.
    expect(onSuivant).not.toHaveBeenCalled()
  })

  it('appelle onTerminer quand la derniere etape est validee', () => {
    const onSuivant = vi.fn()
    const onTerminer = vi.fn()
    render(<DeroulePhase etapes={etapes} onSuivant={onSuivant} onTerminer={onTerminer} />)
    fireEvent.click(suivant())
    fireEvent.click(suivant())
    fireEvent.click(terminer())
    expect(onTerminer).toHaveBeenCalledTimes(1)
    // Sans trame retenue, aucun accuse de reception ne part : onTerminer et
    // onSuivant sont deux portes distinctes, board.tsx les branche seulement
    // sur la meme fonction.
    expect(onSuivant).not.toHaveBeenCalled()
  })

  it('onSuivant absent ne casse rien : la prop est optionnelle', () => {
    render(<DeroulePhase etapes={etapes} phaseMechantEnCours trameRetenue={11} onTerminer={() => {}} />)
    expect(() => fireEvent.click(suivant())).not.toThrow()
    expect(etapeLue()).toBe('Ultron attaque Shuri')
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
      expect(etapeLue()).toBe('Drone attaque Shuri')
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
      expect(etapeLue()).not.toBe('Fin de la phase du méchant')
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
      expect(etapeLue()).toBe('L’Effraction ! gagne 3 menaces')
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
    expect(etapeLue()).toBe('Ultron attaque Shuri')
    expect(etapeLue()).not.toBe('Menace sur la manigance principale')
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
    traverserLesVides()
    expect(etapeLue()).toBe('Fin de la phase du méchant')
    fireEvent.click(terminer())
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
    traverserLesVides()
    expect(etapeLue()).toBe('Fin de la phase du méchant')
    expect(document.querySelector('.deroule-attente')).toBeNull()
    expect(onTerminer).not.toHaveBeenCalled()

    fireEvent.click(terminer())
    expect(onTerminer).toHaveBeenCalledTimes(1)
    expect(container).toBeEmptyDOMElement()
  })

  it('repart de la premiere etape au round suivant', () => {
    // La remise a zero suit l'identite de la phase, et elle seule.
    const { rerender } = render(
      <DeroulePhase etapes={etapes} identitePhase={3} phaseMechantEnCours onTerminer={() => {}} />
    )
    fireEvent.click(suivant())
    expect(etapeLue()).toBe('Ultron attaque Shuri')

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
    expect(etapeLue()).toBe('Menace sur la manigance principale')
  })

  it('ne revient pas a la premiere etape quand la liste s allonge dans le meme round', () => {
    // Le defaut d'origine : la liste qui grossit pendant la phase faisait
    // repartir le cartouche au debut, et le joueur relisait en boucle des
    // etapes deja validees.
    const { rerender } = render(
      <DeroulePhase etapes={etapes} identitePhase={3} phaseMechantEnCours onTerminer={() => {}} />
    )
    fireEvent.click(suivant())
    expect(etapeLue()).toBe('Ultron attaque Shuri')

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
    expect(etapeLue()).toBe('Ultron attaque Shuri')
    expect(etapeLue()).not.toBe('Menace sur la manigance principale')
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
      <DeroulePhase telephone etapes={etapes} identitePhase={3} phaseMechantEnCours onTerminer={() => {}} />
    )
    fireEvent.click(suivant())
    fireEvent.click(suivant())
    fireEvent.click(screen.getByRole('button', { name: /Précédent/i }))
    expect(etapeLue()).toBe('Menace sur la manigance principale')
    expect(etapeLue()).not.toBe('Ultron attaque Shuri')
  })

  // --- Echap ne deroule plus rien : pas a pas strict (decision du 03/10/2026)
  it('Echap ne fait rien : aucun « tout derouler », chaque etape attend son clic', () => {
    const onSuivant = vi.fn()
    render(<DeroulePhase etapes={etapes} trameRetenue={1} onSuivant={onSuivant} onTerminer={() => {}} />)
    fireEvent.keyDown(document, { key: 'Escape' })
    expect(etapeLue()).toBe('Menace sur la manigance principale')
    expect(onSuivant).not.toHaveBeenCalled()
  })

  describe('plus de rappel de regle (demande de l utilisateur, 03/10/2026)', () => {
    it('le cartouche n affiche plus « la règle » ni son texte', () => {
      render(<DeroulePhase etapes={etapes} identitePhase={1} phaseMechantEnCours onTerminer={() => {}} />)
      expect(screen.queryByRole('button', { name: /la règle/i })).toBeNull()
      expect(document.querySelector('.deroule-regle')).toBeNull()
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

  // Les lignes du bilan en trois colonnes (D19) : menace, heros et allies.
  const lignesDe = (rang: number) => [
    ...(document.querySelectorAll('.deroule-bilan .deroule-colonne')[rang]?.querySelectorAll('li:not(.deroule-rien)') ?? []),
  ]
  const lignesMenace = () => lignesDe(0)
  const lignesHeros = () => lignesDe(1)

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
    traverserLesVides()
    expect(etapeLue()).toBe('Fin de la phase du méchant')
    // Trois colonnes (D19) : une seule ligne chez les heros, avant -> apres
    // sur la phase entiere (6 degats, 8 restants).
    expect(lignesHeros()).toHaveLength(1)
    expect(lignesHeros()[0]?.textContent).toBe('Colossus 14 → 8')
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
    traverserLesVides()
    fireEvent.click(suivant())
    traverserLesVides()
    expect(lignesMenace().map((li) => li.textContent)).toEqual(['L’Effraction ! 3 → 6 / 8'])
    expect(lignesHeros().map((li) => li.textContent)).toEqual(['Colossus 14 → 8'])
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
    traverserLesVides()
    expect(etapeLue()).toBe('Fin de la phase du méchant')
    expect(lignesHeros().map((li) => li.textContent)).toEqual(['Colossus 14 → 8'])
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
    fireEvent.click(terminer())
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
    traverserLesVides()
    expect(etapeLue()).toBe('Fin de la phase du méchant')

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
    expect(etapeLue()).not.toBe('Fin de la phase du méchant')
    expect(etapeLue()).toBe('L’Effraction ! gagne 1 menace')
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
    expect(etapeLue()).not.toBe('Fin de la phase du méchant')
    expect(document.querySelector('.deroule-bilan')).toBeNull()
    expect(document.querySelector('.deroule-attente')).not.toBeNull()
  })

  it('rend la main au joueur, sans jamais dire « Suivant » sur le bilan', () => {
    const onTerminer = vi.fn()
    const { container } = render(
      <DeroulePhase etapes={[coup({ cle: 'a' })]} onTerminer={onTerminer} />
    )
    fireEvent.click(suivant())
    traverserLesVides()
    expect(screen.queryByRole('button', { name: /Suivant/i })).toBeNull()
    fireEvent.click(terminer())
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
    traverserLesVides()
    fireEvent.click(suivant())
    traverserLesVides()
    expect(etapeLue()).toBe('Fin de la phase du méchant')
    expect(screen.getByText('Aucun dégât, aucune menace.')).toBeInTheDocument()
  })

  it('sur le bilan, les quatre pastilles sont passees et celle du Bilan est en cours', () => {
    // Le Bilan est la cinquieme pastille (D34) : sur lui, les quatre temps de
    // la carte de reference sont passes, et lui seul est en cours.
    const { container } = render(
      <DeroulePhase etapes={troisCoupsSurColossus} onTerminer={() => {}} />
    )
    fireEvent.click(suivant())
    fireEvent.click(suivant())
    fireEvent.click(suivant())
    traverserLesVides()
    const items = [...container.querySelectorAll('.deroule-pastille')]
    expect(items).toHaveLength(5)
    for (const item of items.slice(0, 4)) {
      expect(item.className).toContain('est-passe')
    }
    expect(items[4].className).toContain('est-courant')
    // Chaque pastille passee porte son resultat court.
    expect(items[1].querySelector('.deroule-pastille-resume')?.textContent).toBe('3 dégâts')
  })

  it('laisse relire l etape precedente depuis le bilan', () => {
    render(<DeroulePhase telephone etapes={troisCoupsSurColossus} onTerminer={() => {}} />)
    fireEvent.click(suivant())
    fireEvent.click(suivant())
    fireEvent.click(suivant())
    fireEvent.click(screen.getByRole('button', { name: /Précédent/i }))
    expect(etapeLue()).not.toBe('Fin de la phase du méchant')
    expect(etapeLue()).toBe('Drone attaque Colossus')
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
    expect(etapeLue()).toBe('Klaw attaque Colossus')
    expect(screen.getByText(/Colossus est vaincu/)).toBeInTheDocument()
    expect(screen.getByText(/La phase s.arrête ici/)).toBeInTheDocument()
    expect(container.querySelector('.deroule-defaite')).not.toBeNull()
  })

  it('n affiche aucune etape au-dela de la defaite', () => {
    render(<DeroulePhase etapes={chuteDeColossus} onTerminer={() => {}} />)
    fireEvent.click(suivant())
    // L'etape suivante existe pourtant bien dans la liste recue : le cartouche
    // s'arrete quand meme.
    expect(etapeLue()).not.toBe('Drone attaque Spider-Man')
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
    expect(etapeLue()).not.toBe('Fin de la phase du méchant')
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
    fireEvent.click(terminer())
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
        <DeroulePhase telephone etapes={etapes} phaseMechantEnCours onTerminer={() => {}} />
      )
      fireEvent.click(suivant())
      // Plus aucune carte de la table n'est touchee : la scene porte les
      // siennes. Seul le voile reste, et il doit tomber avec l'ecran de fin.
      expect(carte.className).toBe('scan-card')
      expect(document.body.classList.contains('deroule-voile')).toBe(true)

      rerender(
        <DeroulePhase telephone etapes={etapes} phaseMechantEnCours partieFinie onTerminer={() => {}} />
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
  //
  // ⚠ ET DEPUIS LE 15/09/2026, ELLE N'EN MONTRE PLUS QUE DEUX SORTES.
  // L'utilisateur : « il n'y a pas besoin de montrer les cartes ; par contre,
  // tu peux mettre le nom, et quand on hover sur le nom, on voit la carte en
  // question. [...] Pour gagner de la place, arrete de montrer les cartes. »
  // Parmi trois portees possibles, il a choisi « seulement celles de l'etape » :
  // l'auteur et sa cible partent, remplaces par leurs noms dans la phrase ;
  // le BOOST reste (« elles restent montrees » : il est retourne sous les yeux
  // du joueur et change le resultat), la carte REVELEE et le DOS de la
  // distribution aussi (une carte jamais vue, « un nom seul ne dirait rien »).
  // ⚠ RENDU DU TELEPHONE (et d'avant) : la scene PC dessine ses cartes dans le
  // cartouche du bas (CartouchePhase.test.tsx). La loupe y arrive au lot 4.
  describe('les cartes de la scene', () => {
    const scan = (id: number, nom: string): ScanCardProps => ({
      id: String(id),
      name: nom,
      kind: 'minion',
      imageUrl: `/scan/${id}`,
    })

    it('ne dessine que le boost : l auteur et la cible sont des noms survolables', () => {
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
        <DeroulePhase telephone etapes={resolue} carteScene={carteScene} onTerminer={() => {}} />
      )
      // UNE SEULE CARTE DESSINEE : le boost. L'auteur et la cible sont des
      // noms, et c'est tout le sujet de la refonte.
      expect(container.querySelectorAll('.deroule-carte .scan-card')).toHaveLength(1)
      expect(container.querySelector('.deroule-carte.est-boost')).not.toBeNull()
      expect(container.querySelector('.deroule-carte.est-auteur')).toBeNull()
      expect(container.querySelector('.deroule-carte.est-cible')).toBeNull()
      // Le boost est force face visible : il est encore face cachee dans le
      // monde de cette trame.
      expect(appels).toEqual(expect.arrayContaining([[77, true]]))
      // Les deux noms portent l'identifiant moteur de leur carte, celui-la
      // meme que `apercu-survol` lit sous le pointeur.
      const noms = [...container.querySelectorAll('.deroule-nom')]
      expect(noms.map((n) => n.textContent)).toEqual(['Klaw', 'Colossus'])
      expect(noms.map((n) => n.getAttribute('data-card-id'))).toEqual(['50', '12'])
      // « Non, la phrase suffit » (15/09/2026) : elle dit deja qui frappe qui,
      // dans l'ordre.
      expect(container.querySelector('.deroule-fleche')).toBeNull()
      expect(screen.getByText('Boost +1')).toBeInTheDocument()
    })

    it('laisse le nom en texte ordinaire quand le plateau ne sait pas montrer la carte', () => {
      // « Il reste du texte ordinaire » (15/09/2026) : on ne promet que ce
      // qu'on peut tenir. Un nom souligne qui n'ouvre rien au survol est pire
      // que pas de souligne du tout. L'etape porte pourtant bien les deux
      // identifiants : c'est l'INDEX DES SCANS qui ne les connait pas.
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
          boosts: [],
        },
      ]
      const { container } = render(
        <DeroulePhase telephone etapes={resolue} carteScene={() => undefined} onTerminer={() => {}} />
      )
      expect(container.querySelector('.deroule-nom')).toBeNull()
      // Le nom reste ecrit, et toujours en gras : seul le souligne part.
      expect(screen.getByText('Klaw')).toBeInTheDocument()
      expect(screen.getByText('Colossus')).toBeInTheDocument()
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
        <DeroulePhase telephone etapes={revelation} carteScene={carteScene} onTerminer={() => {}} />
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
        <DeroulePhase telephone etapes={distribution} dosRencontre={dos} onTerminer={() => {}} />
      )
      expect(container.querySelector('.deroule-carte.est-dos .scan-card')).not.toBeNull()
    })

    // --- Le geste physique --------------------------------------------------
    // Decide avec l'utilisateur le 7 septembre 2026 : un boost qui arrive dos
    // visible et se retourne, la carte rencontre qui se retourne sur place.
    //
    // ⚠ LE JETON QUI TOMBAIT SUR LA CIBLE EST PARTI AVEC ELLE (15/09/2026). Il
    // se posait sur la carte visee, qui n'est plus dessinee : un jeton n'a pas
    // de sens pose sur rien. Ce qu'il disait n'est pas perdu, et les deux cas
    // qui suivent le verrouillent — la phrase porte le nombre, le compteur
    // porte l'avant et l'apres.
    it('ne pose plus de jeton sur la manigance : la phrase et le compteur le disent', () => {
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
        <DeroulePhase telephone etapes={menace} carteScene={(id) => scan(id, 'Hunting Down Heroes')} onTerminer={() => {}} />
      )
      expect(container.querySelector('.deroule-jeton')).toBeNull()
      expect(container.querySelector('.deroule-titre')).toHaveTextContent(
        'Hunting Down Heroes gagne 2 menaces'
      )
      // « 5 → 7 / 12 » : l'avant, l'apres et le seuil, a droite de la phrase.
      expect(container.querySelector('.deroule-compteur')?.textContent).toBe('5 → 7 / 12')
    })

    it('ne pose plus de jeton de degats non plus : le compteur porte les PV', () => {
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
        <DeroulePhase telephone etapes={attaque} carteScene={(id) => scan(id, String(id))} onTerminer={() => {}} />
      )
      expect(container.querySelector('.deroule-jeton')).toBeNull()
      expect(container.querySelector('.deroule-compteur')?.textContent).toContain('9')
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
        <DeroulePhase telephone etapes={etapes2} carteScene={(id) => scan(id, String(id))} onTerminer={() => {}} />
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
        <DeroulePhase telephone
          etapes={etapes2}
          carteScene={(id) => scan(id, String(id))}
          dosRencontre={dos}
          onTerminer={() => {}}
        />
      )
      expect(container.querySelector('.deroule-carte.est-boost .deroule-retourne')).not.toBeNull()
      // L'auteur et la cible ne sont plus dessines du tout : il n'y a donc
      // meme plus de figure a retourner.
      expect(container.querySelector('.deroule-carte.est-auteur')).toBeNull()
      expect(container.querySelector('.deroule-carte.est-cible')).toBeNull()
      // Le dos du retournement est le dos d'une carte rencontre.
      const dosBoost = container.querySelector('.deroule-carte.est-boost .deroule-retourne-dos img')
      expect(dosBoost?.getAttribute('src')).toBe('/scan/encounter')
      fireEvent.click(suivant())
      // Entre les deux : les sbires et la distribution, vides, ont leur etape.
      traverserLesVides()
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
        <DeroulePhase telephone etapes={etapes} carteScene={(id) => scan(id, String(id))} onTerminer={() => {}} />
      )
      fireEvent.click(suivant())
      // ⚠ C'EST LE NOM QU'ON SURVOLE, DESORMAIS. « Quand on hover sur le nom,
      // on voit la carte en question » (15/09/2026). Le nom porte le meme
      // `data-card-id` qu'une carte : `apercu-survol` ne fait pas la
      // difference, et c'est tout ce qu'il a fallu.
      const nom = container.querySelector('.deroule-nom')
      expect(nom?.textContent).toBe('Ultron')
      expect(document.querySelector('.carte-apercu')).toBeNull()
      // Le survol est ecoute sur le TITRE (`mouseOver`, qui remonte), pas sur
      // chaque nom : regle commune d'`apercu-survol.ts`.
      fireEvent.mouseOver(nom as Element)
      expect(document.querySelector('.carte-apercu')).not.toBeNull()
      // « Des que le curseur quitte le nom » (15/09/2026) : le pointeur revient
      // sur le titre, hors de tout nom, et rien ne reste ouvert.
      fireEvent.mouseOver(container.querySelector('.deroule-titre') as Element)
      expect(document.querySelector('.carte-apercu')).toBeNull()
      vi.unstubAllGlobals()
    })

    it('la loupe se ferme quand la carte survolee quitte la scene', () => {
      // LE DEFAUT DU 10 SEPTEMBRE 2026 (capture de l'utilisateur) : un sbire
      // d'une etape precedente restait montre en grand par-dessus le bouton
      // « Suivant », curseur loin de toute carte. Une carte demontee sous le
      // pointeur n'emet jamais `mouseleave` ; seule la derivation depuis la
      // liste courante ferme la loupe. On passe donc a l'etape suivante SANS
      // aucun evenement de souris.
      class ResizeObserverBouchon {
        observe() {}
        unobserve() {}
        disconnect() {}
      }
      vi.stubGlobal('ResizeObserver', ResizeObserverBouchon)
      const { container } = render(
        <DeroulePhase telephone etapes={etapes} carteScene={(id) => scan(id, String(id))} onTerminer={() => {}} />
      )
      fireEvent.click(suivant())
      const nom = container.querySelector('.deroule-nom')
      expect(nom).not.toBeNull()
      fireEvent.mouseOver(nom as Element)
      expect(document.querySelector('.carte-apercu')).not.toBeNull()
      fireEvent.click(suivant())
      expect(document.querySelector('.carte-apercu')).toBeNull()
      vi.unstubAllGlobals()
    })

    it('dit ce que la carte revelee a fait, quand le moteur le sait', () => {
      const revelation: EtapeDeroule[] = [
        {
          cle: 'r',
          temps: 'revelation',
          titre: 'revelation',
          regle: 'regle:revelation',
          carteId: 40,
          auteurNom: 'Scott Lang',
          cibleNom: 'Explosion',
          boosts: [],
          effets: [
            { genre: 'degats', cible: 'Scott Lang', cible_id: 9, montant: 1, restant: 10 },
            { genre: 'entree', carte: 'Hydra Mercenary', carte_id: 4, type: 'sbire' },
          ],
        },
      ]
      const { container } = render(<DeroulePhase telephone etapes={revelation} onTerminer={() => {}} />)
      const lignes = [...container.querySelectorAll('.deroule-effets li')].map((li) => li.textContent)
      expect(lignes).toEqual([
        '→ Scott Lang subit 1 dégât (10 PV)',
        '→ Hydra Mercenary entre en jeu (sbire)',
      ])
    })

    it('nomme les cartes en francais quand le plateau connait leur nom', () => {
      // Les faits du moteur portent les noms anglais ; sous des scans
      // francais, la scene disait « Thunderball manigance sur Thunderstruck ».
      const nomFr = (id: number) => ({ 50: 'Le Boulet', 12: 'Envoyer Bouler', 77: 'Chaos dans la Prison' })[id]
      const resolue: EtapeDeroule[] = [
        {
          cle: 'a',
          temps: 'mechant',
          titre: 'manigance',
          regle: 'regle:activations',
          carteId: 50,
          cibleId: 12,
          auteurNom: 'Thunderball',
          cibleNom: 'Thunderstruck',
          etat: 'resolu',
          base: 3,
          montant: 4,
          boosts: [{ cle: 'b', nom: 'Chaos In the Prison', cibleId: 77, apport: 1 }],
        },
      ]
      render(<DeroulePhase telephone etapes={resolue} nomFr={nomFr} onTerminer={() => {}} />)
      expect(etapeLue()).toBe('Le Boulet manigance sur Envoyer Bouler')
      expect(screen.getByText('3 imprimé + 1 (Chaos dans la Prison) = 4 menaces')).toBeInTheDocument()
    })

    it('ecrit le nom a la place d une carte DESSINEE dont le scan manque', () => {
      // La regle ne vaut plus que pour les cartes qui se dessinent encore : un
      // boost, une carte revelee, un dos. Pour l'auteur et la cible, le « nom a
      // la place de la carte » est devenu la regle generale, pas un repli.
      const avecBoost: EtapeDeroule[] = [
        {
          cle: 'a',
          temps: 'mechant',
          titre: 'attaque',
          regle: 'regle:activations',
          carteId: 50,
          cibleId: 12,
          auteurNom: 'Ultron',
          cibleNom: 'Shuri',
          montant: 4,
          boosts: [{ cle: 'b', nom: 'Whip', cibleId: 77, apport: 1 }],
        },
      ]
      const { container } = render(
        <DeroulePhase telephone etapes={avecBoost} carteScene={() => undefined} onTerminer={() => {}} />
      )
      const absentes = container.querySelectorAll('.deroule-carte-absente')
      expect(absentes).toHaveLength(1)
      expect(absentes[0]?.textContent).toBe('Whip')
    })

    it('ne montre aucune carte sur le bilan', () => {
      const { container } = render(
        <DeroulePhase telephone etapes={etapes} phaseMechantEnCours={false} onTerminer={() => {}} />
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

    it('grise son etape et dit que le moteur attend le joueur', () => {
      // Cartouche du bas (refonte du 04/10/2026) : l'etape reste sous les
      // yeux, GRISEE (D4), au lieu de se replier sur la chronologie.
      const { container } = render(
        <DeroulePhase etapes={etapes} phaseMechantEnCours questionAuJoueur onTerminer={() => {}} />
      )
      expect(container.querySelectorAll('.deroule-pastille')).toHaveLength(5)
      expect(screen.getByText('Le moteur attend ta réponse')).toBeInTheDocument()
      expect(container.querySelector('.deroule-rangee.est-grisee')).not.toBeNull()
      // Aucun bouton : rien a cliquer ici, c'est la question du moteur qui a
      // la main.
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
      // Le cartouche du bas : l'intention en rangee grisee, la question par-
      // dessus dans un sous-cadre (provisoire jusqu'au lot 4), a la place de
      // « Suivant ».
      expect(etapeLue()).toBe('Ultron va attaquer Shuri')
      expect(container.querySelector('.deroule-rangee.est-grisee')).not.toBeNull()
      const sousCadre = container.querySelector('.deroule-sous-cadre.est-provisoire')
      expect(sousCadre?.querySelector('button')?.textContent).toBe('Défendre')
      expect(screen.queryByRole('button', { name: /Suivant/ })).toBeNull()
      expect(screen.queryByText('Le moteur attend ta réponse')).not.toBeInTheDocument()
      // Plus de bandeau « À toi de jouer » (retire le 03/10/2026, demande de
      // l'utilisateur) ; la main reste visible (revirement du 05/10/2026).
      expect(container.querySelector('.deroule-a-toi')).toBeNull()
      expect(screen.queryByText('À toi de jouer')).toBeNull()
      expect(document.body.classList.contains('cartouche-scene')).toBe(false)
    })

    // ⚠ RENDU DU TELEPHONE jusqu'au lot 4 (loupe du cartouche du bas, D29).
    it('ouvre la loupe au survol d un nom PENDANT une question', () => {
      // Capture de l'utilisateur, 11/09/2026 : « Defendre ? » dans la scene,
      // la carte revelee au milieu, et rien en grand au survol.
      //
      // ⚠ LA MEME GARANTIE, SUR LE NOM (15/09/2026). C'est la branche la plus
      // exposee : c'est en decidant de defendre qu'on a le plus besoin de
      // relire la carte qui frappe, et le cartouche n'y dessine plus qu'une
      // question. Sans loupe rendue dans CETTE branche, survoler le nom
      // n'ouvrait rien du tout.
      class ResizeObserverBouchon {
        observe() {}
        unobserve() {}
        disconnect() {}
      }
      vi.stubGlobal('ResizeObserver', ResizeObserverBouchon)
      const scanLocal = (id: number): ScanCardProps => ({ id: String(id), name: `c${id}`, kind: 'minion', imageUrl: `/scan/${id}` })
      const annonce: EtapeDeroule[] = [
        {
          cle: 'activation:1',
          temps: 'mechant',
          titre: 'attaque',
          regle: 'regle:activations',
          carteId: 50,
          cibleId: 12,
          auteurNom: 'Klaw',
          cibleNom: 'Spider-Man',
          etat: 'annonce',
          valeurAnnoncee: 2,
          boosts: [],
        },
      ]
      const { container } = render(
        <DeroulePhase
          telephone
          etapes={annonce}
          phaseMechantEnCours
          questionAuJoueur
          question={<button type="button">Défendre</button>}
          carteScene={(id) => scanLocal(id)}
          onTerminer={() => {}}
        />
      )
      const nom = container.querySelector('.deroule-nom')
      expect(nom?.textContent).toBe('Klaw')
      fireEvent.mouseOver(nom as Element)
      expect(document.querySelector('.carte-apercu')).not.toBeNull()
      vi.unstubAllGlobals()
    })

    it('ne cache jamais la main : aucune classe sur le body, question ou pas', () => {
      // Revirement du 05/10/2026 : le carre laisse la table, la main et la
      // barre visibles et jouables (`main-visible.ts` la montre pendant une
      // question). Plus de `body.cartouche-scene`, plus de `body.deroule-question`.
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
      expect(document.body.classList.contains('cartouche-scene')).toBe(false)
      rerender(scene(false))
      expect(document.body.classList.contains('cartouche-scene')).toBe(false)
      rerender(scene(true))
      unmount()
      expect(document.body.classList.contains('cartouche-scene')).toBe(false)
      expect(document.body.classList.contains('deroule-question')).toBe(false)
    })

    it('sans question rendue, ne loge rien et ne montre aucun bouton', () => {
      // Un ciblage sur la table : le cartouche reste en bas, grise, et la
      // table au-dessus reste cliquable.
      const { container } = render(
        <DeroulePhase etapes={etapes} phaseMechantEnCours questionAuJoueur onTerminer={() => {}} />
      )
      expect(container.querySelector('.deroule-sous-cadre')).toBeNull()
      expect(container.querySelector('.deroule-rangee.est-grisee')).not.toBeNull()
      expect(screen.queryByRole('button')).toBeNull()
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
      expect(etapeLue()).toBe('Ultron attaque Shuri')

      // Pendant la question, l'etape reste la, grisee (D4).
      rerender(cartouche(true))
      expect(etapeLue()).toBe('Ultron attaque Shuri')
      expect(document.querySelector('.deroule-rangee.est-grisee')).not.toBeNull()

      // Pas de remise a zero : on revient sur la deuxieme etape, pas la
      // premiere.
      rerender(cartouche(false))
      expect(etapeLue()).toBe('Ultron attaque Shuri')
      expect(document.querySelector('.deroule-rangee.est-grisee')).toBeNull()
      expect(etapeLue()).not.toBe('Menace sur la manigance principale')
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
      expect(etapeLue()).toBe('Menace sur la manigance principale')
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
          await vi.advanceTimersByTimeAsync(5000)
        })
        expect(etapeLue()).toBe('Menace sur la manigance principale')
        expect(etapeLue()).not.toBe('Ultron attaque Shuri')
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

  it("dit l'intention au futur proche : l'ATQ annoncee, pas de degats", () => {
    render(<DeroulePhase etapes={[annonce]} onTerminer={() => {}} />)
    expect(screen.getByText('ATQ 4')).toBeInTheDocument()
    expect(etapeLue()).toBe('Klaw va attaquer Colossus')
    expect(screen.queryByText(/dégâts? annoncés?/)).toBeNull()
  })

  // Le cas central : l'etape se COMPLETE sous les yeux du joueur. Il ne recule
  // pas d'une etape, il n'en valide pas une de plus.
  it("complete l'etape sur place, sans faire bouger le joueur", () => {
    const { rerender } = render(
      <DeroulePhase etapes={[annonce]} identitePhase={3} phaseMechantEnCours onTerminer={() => {}} />
    )
    expect(etapeLue()).toBe('Klaw va attaquer Colossus')
    rerender(
      <DeroulePhase etapes={[resolue]} identitePhase={3} phaseMechantEnCours onTerminer={() => {}} />
    )
    expect(etapeLue()).toBe('Klaw attaque Colossus')
    expect(etapeLue()).not.toBe('Klaw va attaquer Colossus')
    // La MEME rangee, completee : le resultat s'y ajoute en gros (D11).
    expect(screen.getByText('4 dégâts subis')).toBeInTheDocument()
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
    expect(etapeLue()).toBe('Klaw attaque Colossus')
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
    expect(etapeLue()).toBe('Klaw va attaquer Colossus')
    expect(screen.getByText('tu peux défendre ou répondre')).toBeInTheDocument()
    // Pas de bouton : c'est ailleurs qu'on repond, et « La suite arrive… »
    // serait un mensonge (c'est le moteur qui attend).
    expect(screen.queryByRole('button', { name: /Suivant/i })).not.toBeInTheDocument()
  })

  // Signalement Yarro (30/09/2026) : « je peux bouger la fenetre dans le fond
  // mais pas la fenetre principale ». Le carre se deplace en l'attrapant sur
  // tout fond libre (revirement du 05/10/2026), question posee ou non (D2).
  it("se deplace en l attrapant sur son fond pendant une question", () => {
    const { container } = render(
      <DeroulePhase
        etapes={[annonce]}
        phaseMechantEnCours
        questionAuJoueur
        question={<button type="button">Défendre</button>}
        onTerminer={() => {}}
      />
    )
    const cartouche = container.querySelector<HTMLElement>('.deroule-phase.est-scene')
    const ligne = container.querySelector<HTMLElement>('.deroule-titre-court')
    expect(cartouche).not.toBeNull()
    expect(cartouche?.classList.contains('poignee-glisser')).toBe(true)
    expect(cartouche?.style.translate).toBe('')

    const pointeur = (type: string, x: number, y: number) =>
      new MouseEvent(type, { bubbles: true, clientX: x, clientY: y, button: 0 })
    act(() => {
      ligne?.dispatchEvent(pointeur('pointerdown', 100, 100))
    })
    act(() => {
      ligne?.dispatchEvent(pointeur('pointermove', 160, 60))
    })
    expect(cartouche?.style.translate).toBe('60px -40px')
  })

  // Seconde partie du meme signalement (01/10/2026, capture a l'appui) : le
  // cartouche des ETAPES du mechant (« Gagne 1 menace », bouton Suivant) ne
  // bougeait pas non plus.
  it("deplace aussi le carre des etapes, par son fond", () => {
    const { container } = render(
      <DeroulePhase etapes={[annonce]} phaseMechantEnCours onTerminer={() => {}} />
    )
    const cartouche = container.querySelector<HTMLElement>('.deroule-phase')
    const ligne = container.querySelector<HTMLElement>('.deroule-titre-court')
    expect(cartouche).not.toBeNull()
    expect(cartouche?.classList.contains('poignee-glisser')).toBe(true)

    const pointeur = (type: string, x: number, y: number) =>
      new MouseEvent(type, { bubbles: true, clientX: x, clientY: y, button: 0 })
    act(() => {
      ligne?.dispatchEvent(pointeur('pointerdown', 100, 100))
    })
    act(() => {
      ligne?.dispatchEvent(pointeur('pointermove', 30, 140))
    })
    expect(cartouche?.style.translate).toBe('-70px 40px')
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
    // D24 : la rangee barree et « Annulée » en gros (la cause s'y ajoute
    // quand le fait la porte).
    const annulee: EtapeDeroule = { ...annonce, etat: 'annule' }
    render(<DeroulePhase etapes={[annulee]} phaseMechantEnCours onTerminer={() => {}} />)
    expect(document.querySelector('.deroule-rangee.est-annulee')).not.toBeNull()
    expect(screen.getByText('Annulée')).toBeInTheDocument()
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
    // Le joueur valide pendant la fenetre d'annonce (Espace : le cartouche du
    // bas ne porte pas de « Suivant » sur une intention). Cela ne doit pas
    // valider par avance la resolution, qui n'est pas encore arrivee.
    fireEvent.keyDown(document, { key: ' ' })
    rerender(vue([annonce], undefined))
    rerender(vue([resolue], 12))
    expect(etapeLue()).toBe('Drone manigance sur Assault on NORAD')
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
    // Espace : le cartouche du bas ne porte pas de « Suivant » sur une intention.
    fireEvent.keyDown(document, { key: ' ' })
    expect(screen.getByText('La suite arrive…')).toBeInTheDocument()
    rerender(vue([annonce], undefined))
    rerender(vue([resolue], 12))
    expect(etapeLue()).toBe('Drone manigance sur Assault on NORAD')
    expect(document.querySelector('.deroule-resultat-texte')?.textContent).toBe('+1 menace')
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
    expect(etapeLue()).toBe('Drone manigance sur Assault on NORAD')
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
    traverserLesVides()
    expect(etapeLue()).toBe('Heros1 révèle Carte B')
    // Le Deferlement : une revelation de plus, qui passe DEVANT celle qu'on
    // lit parce qu'elle appartient a un joueur plus avance dans l'ordre du
    // tour. Le joueur ne doit pas reculer d'un cran pour autant.
    rerender(
      <DeroulePhase etapes={[menace, carteA, carteB]} phaseMechantEnCours onTerminer={() => {}} />
    )
    expect(etapeLue()).toBe('Heros1 révèle Carte B')
    expect(etapeLue()).not.toBe('Heros0 révèle Carte A')
  })

  it('garde son etape quand la liste est reordonnee sans rien gagner', () => {
    const { rerender } = render(
      <DeroulePhase etapes={[menace, carteA, carteB]} phaseMechantEnCours onTerminer={() => {}} />
    )
    fireEvent.click(suivant())
    traverserLesVides()
    fireEvent.click(suivant())
    expect(etapeLue()).toBe('Heros1 révèle Carte B')
    // Meme liste, autre ordre : rien n'a ete produit, rien ne doit bouger.
    rerender(
      <DeroulePhase etapes={[menace, carteB, carteA]} phaseMechantEnCours onTerminer={() => {}} />
    )
    expect(etapeLue()).toBe('Heros1 révèle Carte B')
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
    traverserLesVides()
    fireEvent.click(suivant())
    expect(etapeLue()).toBe('Heros1 révèle Carte B')
    // La carte revelee frappe, et le heros tombe.
    rerender(
      <DeroulePhase
        etapes={[menace, mortelle, carteA, carteB]}
        phaseMechantEnCours
        onTerminer={() => {}}
      />
    )
    expect(screen.getByText('Shuri est vaincu')).toBeInTheDocument()
    expect(etapeLue()).not.toBe('Menace sur la manigance principale')
  })

  // Le repli ORDINAIRE, quand la cle retenue disparait sans coupe de defaite :
  // la premiere etape NON VALIDEE.
  it('se replie sur la premiere etape non validee quand sa cle disparait', () => {
    const { rerender } = render(
      <DeroulePhase etapes={[menace, carteA, carteB]} phaseMechantEnCours onTerminer={() => {}} />
    )
    fireEvent.click(suivant())
    traverserLesVides()
    expect(etapeLue()).toBe('Heros0 révèle Carte A')
    // Carte A s'en va (une defaite survenue plus tot coupe le deroule derriere
    // elle) : la menace reste la seule etape validee, donc on repart de celle
    // qui la suit.
    rerender(<DeroulePhase etapes={[menace, carteB]} phaseMechantEnCours onTerminer={() => {}} />)
    expect(etapeLue()).toBe('Heros1 révèle Carte B')
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
    expect(etapeLue()).toBe('Drone attaque Shuri')
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
    expect(etapeLue()).toBe('The Break-In! gagne 1 menace')

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
    expect(etapeLue()).toBe('Assault on NORAD gagne 1 menace')
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
    expect(etapeLue()).toBe('The Break-In! gagne 1 menace')

    // Premiere bascule : la garde s'arme, le cartouche se tait.
    rerender(vue('partie-B'))
    expect(container).toBeEmptyDOMElement()

    // Deuxieme bascule sans que la liste vide attendue ne soit jamais venue :
    // la garde tombe plutot que de se reposer.
    rerender(vue('partie-C'))
    expect(etapeLue()).toBe('The Break-In! gagne 1 menace')
  })

  // Signalement Yarro n42 (02/10/2026) : apres un Undo, le monde revient en
  // arriere et n'a plus rien a raconter, mais la memoire du cartouche garde
  // la phase d'avant et la remontre en plein tour du joueur.
  describe('apres un Undo', () => {
    const cartouche = (liste: EtapeDeroule[], round: number, enPhase: boolean) => (
      <DeroulePhase
        etapes={liste}
        identitePhase={round}
        phaseMechantEnCours={enPhase}
        onTerminer={() => {}}
      />
    )
    const cartoucheAffiche = () => document.querySelector('.deroule-phase') !== null

    it('le cartouche est bien visible pendant la phase', () => {
      render(cartouche(etapes, 1, true))
      expect(cartoucheAffiche()).toBe(true)
    })

    it('un monde revenu au meme round, sans plus rien a raconter, efface le cartouche', () => {
      const { rerender } = render(cartouche(etapes, 1, true))
      rerender(cartouche([], 1, false))
      expect(cartoucheAffiche()).toBe(false)
    })

    it('un round qui recule efface le cartouche', () => {
      const { rerender } = render(cartouche(etapes, 2, true))
      rerender(cartouche([], 1, false))
      expect(cartoucheAffiche()).toBe(false)
    })

    it('la phase rejouee apres l Undo se raconte de nouveau', () => {
      const { rerender } = render(cartouche(etapes, 1, true))
      rerender(cartouche([], 1, false))
      rerender(cartouche(etapes, 1, true))
      expect(cartoucheAffiche()).toBe(true)
    })

    it('la fin ORDINAIRE d une phase (round suivant) garde son bilan', () => {
      const { rerender } = render(cartouche(etapes, 1, true))
      rerender(cartouche([], 2, false))
      expect(cartoucheAffiche()).toBe(true)
    })
  })
})

describe('les consequences d une carte revelee (rapport Yarro n46)', () => {
  it('s affichent a droite de la carte, une par ligne, dans son resume', () => {
    const revelation: EtapeDeroule = {
      cle: 'revelation:4:9:54',
      temps: 'revelation',
      titre: 'revelation',
      regle: 'regle:revelation',
      carteId: 54,
      auteurNom: 'Echo',
      cibleNom: 'Psionic Slash',
      boosts: [],
      consequences: [
        {
          cle: 'activation:7',
          temps: 'revelation',
          titre: 'manigance',
          regle: 'regle:activations',
          auteurNom: 'Bloody Mary',
          cibleNom: 'Stop the Presses!',
          etat: 'resolu',
          montant: 4,
          boosts: [],
        },
      ],
    }
    render(<DeroulePhase etapes={[revelation]} identitePhase={4} phaseMechantEnCours onTerminer={() => {}} />)
    expect(etapeLue()).toBe('Echo révèle Psionic Slash')
    // Le resume de la carte revelee (D16), pagine au besoin (D41).
    expect(document.querySelector('.deroule-revelee .deroule-lignes li')?.textContent).toContain(
      'Bloody Mary manigance sur Stop the Presses!'
    )
  })
})

// ------------------------------------------------- relecture d'un onglet passe
// Decision du 03/10/2026 : un clic sur un onglet PASSE le relit en lecture
// seule, avec « Revenir à l'étape en cours » ; plusieurs coups sont listes, un
// clic sur une ligne en donne le detail. Rien ne part au moteur pendant ce temps.
// ⚠ RENDU DU TELEPHONE, qui garde sa relecture (D36) : celle du cartouche du
// bas passe par ses pastilles (D22, D23), cas plus bas.
describe('la relecture d un onglet passe', () => {
  const coup = (cle: string, auteur: string, montant: number): EtapeDeroule => ({
    cle, temps: 'sbires', titre: 'attaque', etat: 'resolu', regle: '', auteurNom: auteur, cibleNom: 'Shuri',
    montant, base: montant, defense: 0, boosts: [],
  })
  const phase: EtapeDeroule[] = [
    { cle: 'm', temps: 'menace', titre: 'menace', regle: '', cibleNom: 'Effraction', montant: 1, boosts: [] },
    { cle: 'v', temps: 'mechant', titre: 'attaque', etat: 'resolu', regle: '', auteurNom: 'Rhino', cibleNom: 'Shuri', montant: 3, boosts: [] },
    coup('s1', 'Drone', 1),
    coup('s2', 'Hydra', 2),
    { cle: 'd', temps: 'distribution', titre: 'distribution', regle: '', auteurNom: 'Shuri', montant: 1, boosts: [] },
  ]
  const onglet = (nom: RegExp) =>
    [...document.querySelectorAll('.deroule-temps li')].find((li) => li.textContent?.match(nom))
  const aLaDistribution = (onSuivant = vi.fn()) => {
    render(<DeroulePhase telephone etapes={phase} phaseMechantEnCours trameRetenue={7} onSuivant={onSuivant} onTerminer={() => {}} />)
    for (let i = 0; i < 4; i++) fireEvent.click(suivant())
    expect(etapeLue()).toBe('Shuri reçoit sa carte rencontre')
    return onSuivant
  }

  it('un onglet passe se relit, en lecture seule, puis on revient', () => {
    const onSuivant = aLaDistribution()
    const avant = onSuivant.mock.calls.length
    fireEvent.click(onglet(/Méchant/i)!.querySelector('button')!)
    expect(etapeLue()).toBe('Rhino attaque Shuri')
    expect(screen.queryByRole('button', { name: /Suivant/i })).toBeNull()
    expect(onglet(/Méchant/i)?.className).toContain('est-relu')
    fireEvent.keyDown(document, { key: 'Enter' })
    expect(onSuivant.mock.calls.length).toBe(avant)
    // Entree ramene a l'etape en cours, sans rien valider.
    expect(etapeLue()).toBe('Shuri reçoit sa carte rencontre')
    fireEvent.click(onglet(/Menace/i)!.querySelector('button')!)
    fireEvent.click(screen.getByRole('button', { name: /Revenir à l’étape en cours/ }))
    expect(etapeLue()).toBe('Shuri reçoit sa carte rencontre')
    expect(onSuivant.mock.calls.length).toBe(avant)
  })

  it('plusieurs coups sont listes ; un clic sur une ligne en donne le detail', () => {
    aLaDistribution()
    fireEvent.click(onglet(/Sbires/i)!.querySelector('button')!)
    const lignes = document.querySelectorAll('.deroule-relecture-liste button')
    expect(lignes).toHaveLength(2)
    expect(lignes[0].textContent).toContain('Drone attaque Shuri')
    fireEvent.click(lignes[1])
    expect(document.querySelector('.deroule-relecture-liste')).toBeNull()
    expect(etapeLue()).toBe('Hydra attaque Shuri')
    expect(screen.getByText('→ 2 dégâts')).toBeInTheDocument()
  })

  it('un onglet a venir ne se relit pas', () => {
    aLaDistribution()
    expect(onglet(/Révéler/i)?.querySelector('button')).toBeNull()
    expect(onglet(/Bilan/i)?.querySelector('button')).toBeNull()
  })
})

// ⚠ RENDU DU TELEPHONE : la fleche « → Renfort » du cartouche du bas est plus
// bas (D17) et dans CartouchePhase.test.tsx (etat 9).
describe('le Renfort dans le cartouche (03/10/2026)', () => {
  it('la carte precedente annonce le Renfort, la suivante porte « Renfort de X » en surtitre', () => {
    const chaine: EtapeDeroule[] = [
      { cle: 'r1', temps: 'revelation', titre: 'revelation', regle: '', auteurNom: 'Shuri', cibleNom: 'Mines', suivieDUnRenfort: true, boosts: [] },
      { cle: 'r2', temps: 'revelation', titre: 'revelation', regle: '', auteurNom: 'Shuri', cibleNom: 'Bombe', parSurge: true, renfortDe: 'Mines', boosts: [] },
    ]
    render(<DeroulePhase telephone etapes={chaine} phaseMechantEnCours onTerminer={() => {}} />)
    expect(screen.getByText('→ Renfort : une autre carte est révélée')).toBeInTheDocument()
    expect(document.querySelector('.deroule-surtitre')).toBeNull()
    fireEvent.click(suivant())
    expect(document.querySelector('.deroule-surtitre')?.textContent).toBe('Renfort de Mines')
    expect(etapeLue()).toBe('Shuri révèle Bombe')
  })
})

// LOT 5 : LA RELECTURE DU CARTOUCHE DU BAS passe par ses pastilles (D22,
// D23). Meme mecanique que le telephone (l'etat `relecture` du controleur),
// autre dessin : la rangee de l'etape relue, sous un bandeau « Relecture »,
// et « Revenir à 2B ». Rien ne part au moteur pendant ce temps.
describe('la relecture par les pastilles du cartouche du bas (D22, D23)', () => {
  afterEach(() => {
    document.body.className = ''
  })
  const coup = (cle: string, auteur: string, montant: number): EtapeDeroule => ({
    cle, temps: 'sbires', titre: 'attaque', etat: 'resolu', regle: '', auteurNom: auteur, cibleNom: 'Shuri',
    montant, base: montant, defense: 0, boosts: [],
  })
  const phase: EtapeDeroule[] = [
    { cle: 'm', temps: 'menace', titre: 'menace', regle: '', cibleNom: 'Effraction', montant: 1, boosts: [] },
    { cle: 'v', temps: 'mechant', titre: 'attaque', etat: 'resolu', regle: '', auteurNom: 'Rhino', cibleNom: 'Shuri', montant: 3, boosts: [] },
    coup('s1', 'Drone', 1),
    coup('s2', 'Hydra', 2),
  ]
  const pastille = (rang: number) => document.querySelectorAll('li.deroule-pastille')[rang]
  const auDeuxiemeSbire = (onSuivant = vi.fn()) => {
    render(<DeroulePhase etapes={phase} phaseMechantEnCours trameRetenue={7} onSuivant={onSuivant} onTerminer={() => {}} />)
    for (let i = 0; i < 3; i++) fireEvent.click(suivant())
    expect(etapeLue()).toBe('Hydra attaque Shuri')
    return onSuivant
  }

  it('une pastille passee se relit, en lecture seule ; Entree ramene a l etape en cours sans rien valider', () => {
    const onSuivant = auDeuxiemeSbire()
    const avant = onSuivant.mock.calls.length
    fireEvent.click(pastille(1).querySelector('button')!)
    expect(document.querySelector('.deroule-phase.est-scene.est-relecture')).not.toBeNull()
    expect(document.querySelector('.deroule-bandeau')?.textContent).toBe('Relecture')
    expect(etapeLue()).toBe('Rhino attaque Shuri')
    expect(pastille(1).className).toContain('est-relu')
    expect(pastille(2).className).toContain('est-courant')
    expect(screen.queryByRole('button', { name: /Suivant \(espace\)/ })).toBeNull()
    fireEvent.keyDown(document, { key: 'Enter' })
    expect(onSuivant.mock.calls.length).toBe(avant)
    expect(etapeLue()).toBe('Hydra attaque Shuri')
    expect(document.querySelector('.est-relecture')).toBeNull()
  })

  it('« Revenir à 2B » ramene a l etape en cours, sans rien valider', () => {
    const onSuivant = auDeuxiemeSbire()
    const avant = onSuivant.mock.calls.length
    fireEvent.click(pastille(0).querySelector('button')!)
    fireEvent.click(screen.getByRole('button', { name: 'Revenir à 2B' }))
    expect(etapeLue()).toBe('Hydra attaque Shuri')
    expect(onSuivant.mock.calls.length).toBe(avant)
  })

  it('une pastille a venir, ou la courante, ne se relit pas', () => {
    auDeuxiemeSbire()
    expect(pastille(2).querySelector('button')).toBeNull()
    expect(pastille(3).querySelector('button')).toBeNull()
    expect(pastille(4).querySelector('button')).toBeNull()
  })

  it('plusieurs coups dans la pastille relue : « 1 / 2 », et « Suivant » montre le second', () => {
    render(
      <DeroulePhase
        etapes={[...phase, { cle: 'r', temps: 'revelation', titre: 'revelation', regle: '', auteurNom: 'Shuri', cibleNom: 'Bombe', boosts: [] }]}
        phaseMechantEnCours
        onTerminer={() => {}}
      />
    )
    for (let i = 0; i < 4; i++) fireEvent.click(suivant())
    fireEvent.click(pastille(2).querySelector('button')!)
    expect(document.querySelector('.deroule-page')?.textContent).toBe('1 / 2')
    expect(etapeLue()).toBe('Drone attaque Shuri')
    fireEvent.click(screen.getByRole('button', { name: 'Suivant' }))
    expect(etapeLue()).toBe('Hydra attaque Shuri')
    expect(screen.getByRole('button', { name: 'Revenir à 3' })).toBeInTheDocument()
  })

  // Verification du lot 5 : le controleur retient la relecture en onglets ;
  // ④ « Cartes rencontre » doit s'y relire par sa carte revelee, pas par un
  // autre temps (aucun cas ne relisait ④ a travers le controleur).
  it('la pastille ④ se relit par sa carte revelee', () => {
    render(
      <DeroulePhase
        etapes={[...phase, { cle: 'r', temps: 'revelation', titre: 'revelation', regle: '', auteurNom: 'Shuri', carteId: 88, cibleNom: 'Bombe', boosts: [] }]}
        onTerminer={() => {}}
      />
    )
    for (let i = 0; i < 5; i++) fireEvent.click(suivant())
    expect(document.querySelector('.deroule-bilan')).not.toBeNull()
    fireEvent.click(pastille(3).querySelector('button')!)
    expect(document.querySelector('.deroule-phase.est-scene.est-relecture .deroule-revelee')).not.toBeNull()
    expect(etapeLue()).toMatch(/Bombe/)
  })
})

// LOT 5 : LE RENFORT DANS LE CARTOUCHE DU BAS (D17) : la fleche et la carte
// suivante a cote, dans la meme rangee.
describe('le Renfort dans le cartouche du bas (D17)', () => {
  afterEach(() => {
    document.body.className = ''
  })
  it('la carte precedente porte « → Renfort » et la carte suivante a cote', () => {
    const chaine: EtapeDeroule[] = [
      { cle: 'r1', temps: 'revelation', titre: 'revelation', regle: '', auteurNom: 'Shuri', carteId: 88, cibleNom: 'Mines', suivieDUnRenfort: true, boosts: [] },
      { cle: 'r2', temps: 'revelation', titre: 'revelation', regle: '', auteurNom: 'Shuri', carteId: 89, cibleNom: 'Bombe', parSurge: true, renfortDe: 'Mines', boosts: [] },
    ]
    render(<DeroulePhase etapes={chaine} phaseMechantEnCours onTerminer={() => {}} />)
    traverserLesVides()
    const revelee = document.querySelector('.deroule-revelee.a-renfort')
    expect(revelee?.querySelector('.deroule-renfort-fleche')?.textContent).toBe('→ Renfort')
    expect(revelee?.querySelectorAll('.deroule-carte-grande')).toHaveLength(2)
  })
})

// LOT 5 : L'ATTENTE NOMMEE (D28) au pied du cartouche du bas, une fois les
// etapes connues epuisees : le moteur interroge un autre siege, on dit QUI
// choisit. Le retard d'un autre siege sur ses etapes (sans question) garde
// « En attente de X » (cas plus haut) : il lit, il ne choisit rien.
describe('l attente nommee du cartouche du bas (D28)', () => {
  afterEach(() => {
    document.body.className = ''
  })
  it('un autre siege interroge : « Spider-Man choisit… », jamais « En attente de » ni « La suite arrive… »', () => {
    render(
      <DeroulePhase
        etapes={[{ cle: 'a', temps: 'menace', titre: 'menace', regle: 'regle:menace', boosts: [] }, etapes[1]]}
        phaseMechantEnCours
        attendUnAutreJoueur
        nomJoueurAttendu="Spider-Man"
        questionDUnAutre={{ options: [] }}
        onTerminer={() => {}}
      />
    )
    fireEvent.click(suivant())
    expect(screen.getByText('Spider-Man choisit…')).toBeInTheDocument()
    expect(screen.queryByText('En attente de Spider-Man')).toBeNull()
    expect(screen.queryByText('La suite arrive…')).toBeNull()
  })

  it('sans etape, sans question : la scene PC ne rend rien (jamais deux cartouches fixes)', () => {
    const { container } = render(<DeroulePhase etapes={[]} onTerminer={() => {}} />)
    expect(container.querySelector('.deroule-phase')).toBeNull()
  })
})

describe('les pastilles du telephone (03/10/2026)', () => {
  it('chaque onglet separe son numero de son nom (le telephone ne garde que le numero)', () => {
    render(<DeroulePhase telephone etapes={etapes} onTerminer={() => {}} />)
    const premier = document.querySelector('.deroule-temps li')!
    expect(premier.querySelector('.deroule-onglet-numero')?.textContent).toBe('1.')
    expect(premier.querySelector('.deroule-onglet-libelle')?.textContent).toBe(' Placer les menaces')
    const bilan = document.querySelectorAll('.deroule-temps li')[5]
    expect(bilan.querySelector('.deroule-onglet-numero')).toBeNull()
    expect(bilan.querySelector('.deroule-onglet-libelle')?.textContent).toBe('Bilan')
  })
})

// LA SCENE PC DELEGUE SON RENDU AU CARTOUCHE DU BAS (lot 3 de la refonte,
// 05/10/2026). La mecanique (index, validation, accuse) ne bouge pas : seul le
// rendu change, et seulement en scene sur PC. La table et le telephone gardent
// le rendu d'avant (D21, D36).
describe('la scène PC délègue au cartouche', () => {
  afterEach(() => {
    document.body.className = ''
  })

  it('rend le cartouche du bas par defaut, sans la frise d avant', () => {
    const { container } = render(<DeroulePhase etapes={etapes} onTerminer={() => {}} />)
    expect(container.querySelector('.deroule-phase.est-scene')).not.toBeNull()
    expect(container.querySelector('.deroule-temps')).toBeNull()
    expect(container.querySelectorAll('.deroule-pastille')).toHaveLength(5)
  })

  it('le telephone garde le rendu d avant (six onglets)', () => {
    const { container } = render(<DeroulePhase etapes={etapes} telephone onTerminer={() => {}} />)
    expect(container.querySelector('.est-scene')).toBeNull()
    expect(container.querySelectorAll('.deroule-temps li')).toHaveLength(6)
  })

  it('la table n a plus de fenêtre : une ligne fine, et la carte qui agit se clique (16/10/2026)', () => {
    const { container } = render(
      <DeroulePhase etapes={etapes} presentation="table" onTerminer={() => {}} />
    )
    expect(container.querySelector('.est-scene')).toBeNull()
    expect(container.querySelector('.deroule-bulle-table')).toBeNull()
    expect(container.querySelector('.deroule-rond')).toBeNull()
    expect(container.querySelector('.tsm-bandeau')).not.toBeNull()
  })

  it('la bulle de la table porte la frise en onglets, plus la barre du haut (v3)', () => {
    const { container } = render(
      <DeroulePhase etapes={etapes} presentation="table" onTerminer={() => {}} />
    )
    const bulle = container.querySelector('.deroule-bulle-table')
    expect(bulle?.querySelector('.deroule-bulle-onglets.poignee-glisser .deroule-temps')).not.toBeNull()
    expect(document.querySelector('.deroule-temps-barre')).toBeNull()
  })

  it('sur la table, tous les boosts sortent ENSEMBLE : un seul geste les valide (16/10/2026)', () => {
    const avecBoosts: EtapeDeroule[] = [
      {
        cle: 'atk',
        temps: 'mechant',
        titre: 'attaque',
        regle: 'regle:activations',
        etat: 'resolu',
        carteId: 50,
        cibleId: 12,
        auteurNom: 'Ultron',
        cibleNom: 'Shuri',
        base: 2,
        montant: 4,
        restant: 6,
        boosts: [
          { cle: 'b1', nom: 'Assaut', cibleId: 70, apport: 1 },
          { cle: 'b2', nom: 'Avancée', cibleId: 71, apport: 1 },
        ],
      },
      { cle: 'apres', temps: 'sbires', titre: 'vide', regle: 'regle:activations', boosts: [] },
    ]
    const { container } = render(
      <DeroulePhase etapes={avecBoosts} presentation="table" onTerminer={() => {}} />
    )
    const phrase = () => container.querySelector('.tsm-phrase')?.textContent ?? ''
    const espace = () =>
      act(() => {
        document.dispatchEvent(new KeyboardEvent('keydown', { key: ' ', bubbles: true }))
      })
    // Les deux boosts sont déjà sortis : un seul geste valide l'étape.
    expect(phrase()).toContain('Ultron')
    espace()
    expect(phrase()).not.toContain('Ultron')
  })

  it('sur la table, Espace avance aussi quand le bouton de la carte a gardé le focus', () => {
    const { container } = render(<DeroulePhase etapes={etapes} presentation="table" onTerminer={() => {}} />)
    const avant = container.querySelector('.tsm-phrase')?.textContent
    const bouton = document.createElement('button')
    bouton.className = 'tsm-acteur'
    container.append(bouton)
    bouton.focus()
    fireEvent.keyDown(bouton, { key: ' ' })
    expect(container.querySelector('.tsm-phrase')?.textContent).not.toBe(avant)
  })

  it('la défense suivante attend la lecture du résultat et des boosts de l’attaque précédente', () => {
    const attaque: EtapeDeroule = {
      cle: 'klaw-resolu', temps: 'mechant', titre: 'attaque', regle: '', etat: 'resolu',
      carteId: 50, cibleId: 1, auteurNom: 'Klaw', cibleNom: 'Spider-Man', montant: 1,
      boosts: [{ cle: 'b1', cibleId: 66, nom: 'A', apport: 0 }, { cle: 'b2', cibleId: 72, nom: 'B', apport: 1 }],
    }
    render(<DeroulePhase etapes={[attaque]} presentation="table" questionAuJoueur phaseMechantEnCours
      question={<button>Défense du sbire suivant</button>} onTerminer={() => {}} />)
    expect(screen.queryByRole('button', { name: 'Défense du sbire suivant' })).toBeNull()
    expect(document.querySelector('.tsm-phrase')?.textContent).toContain('Klaw')
    fireEvent.keyDown(document, { key: ' ' })
    expect(screen.getByRole('button', { name: 'Défense du sbire suivant' })).toBeInTheDocument()
  })

  // Rapport de l'utilisateur, 18/10/2026 : « il fait les degats avant qu'il y ait les cartes boost ». Le
  // bandeau disait « 1 degat » des l'entree des boosts. Les degats se calculent boosts a l'ecran, puis partent.
  describe('les degats ne s’annoncent qu’une fois les boosts lisibles', () => {
    const attaque: EtapeDeroule = {
      cle: 'klaw-resultat', temps: 'mechant', titre: 'attaque', regle: '', etat: 'resolu',
      carteId: 50, cibleId: 1, auteurNom: 'Klaw', cibleNom: 'Spider-Man', montant: 1,
      boosts: [{ cle: 'b1', cibleId: 66, nom: 'A', apport: 0 }, { cle: 'b2', cibleId: 72, nom: 'B', apport: 1 }],
    }
    const scan = (id: number) => ({ id: String(id), name: `Carte ${id}`, kind: 'treachery' as const, imageUrl: '/scan.png' })
    // La couche des cartes (et donc la lecture des boosts) ne vit que dans le cadre du plateau.
    beforeEach(() => { document.body.insertAdjacentHTML('beforeend', '<div class="plateau-cadre"></div>') })
    afterEach(() => { document.querySelector('.plateau-cadre')?.remove() })
    const nombre = () => document.querySelector('.tsm-nombre')

    it('pendant l’entree des boosts : pas de « 1 degat » dans le bandeau', () => {
      render(
        <DeroulePhase etapes={[attaque]} presentation="table" carteScene={scan} onTerminer={() => {}} />
      )
      expect(document.querySelector('.tsm-phrase')?.textContent).toContain('Klaw')
      expect(nombre()).toBeNull()
    })

    it('lecture puis résultat : les dégâts exigent un nouveau clic après le départ des boosts', async () => {
      const cadre = document.querySelector('.plateau-cadre')!
      cadre.innerHTML = '<div class="zone-piles-rencontre"><div class="scan-card"><div class="scan-frame"></div></div></div>'
      const mesure = vi.spyOn(HTMLElement.prototype, 'getBoundingClientRect').mockReturnValue({ x: 0, y: 0, left: 0, top: 0, width: 500, height: 400, right: 500, bottom: 400, toJSON: () => ({}) })
      const valider = vi.fn()
      render(<DeroulePhase etapes={[attaque]} presentation="table" carteScene={scan} onEtapeValidee={valider} onTerminer={() => {}} />)
      await act(async () => { await Promise.resolve() })
      expect(document.querySelector('[data-lecture="lecture"]')).not.toBeNull()
      expect(nombre()).toBeNull()
      expect(document.querySelector('.delta-sur-table')).toBeNull()
      await act(async () => { fireEvent.keyDown(document, { key: ' ' }); await Promise.resolve() })
      expect(document.querySelector('.rencontre-sur-table')).toBeNull()
      expect(nombre()?.textContent).toMatch(/^1/)
      expect(valider).not.toHaveBeenCalled()
      fireEvent.keyDown(document, { key: ' ' })
      expect(valider).toHaveBeenCalledWith('klaw-resultat', 'resolu')
      mesure.mockRestore()
    })

    it('lit les boosts avant une interruption de dégâts et ne les rejoue pas à la résolution', async () => {
      document.querySelector('.plateau-cadre')!.innerHTML = '<div class="zone-piles-rencontre"><div class="scan-card"></div></div>'
      const mesure = vi.spyOn(HTMLElement.prototype, 'getBoundingClientRect').mockReturnValue({ x: 0, y: 0, left: 0, top: 0, width: 500, height: 400, right: 500, bottom: 400, toJSON: () => ({}) })
      const valider = vi.fn()
      const vue = (e: EtapeDeroule, question = false) => <DeroulePhase etapes={[e]} phaseMechantEnCours presentation="table" carteScene={scan} questionAuJoueur={question} question={<button>Utiliser Barrière énergétique</button>} onEtapeValidee={valider} onTerminer={() => {}} />
      const { rerender } = render(vue({ ...attaque, etat: 'annonce', boosts: [] }))
      fireEvent.keyDown(document, { key: ' ' })
      expect(valider).toHaveBeenCalledTimes(1)
      rerender(vue({ ...attaque, etat: 'annonce' }, true))
      await act(async () => { await Promise.resolve() })
      expect(document.querySelector('[data-lecture="lecture"]')).not.toBeNull()
      expect(screen.queryByRole('button', { name: 'Utiliser Barrière énergétique' })).toBeNull()
      await act(async () => { fireEvent.keyDown(document, { key: ' ' }); await Promise.resolve() })
      expect(screen.getByRole('button', { name: 'Utiliser Barrière énergétique' })).toBeInTheDocument()
      rerender(vue(attaque))
      await act(async () => { await Promise.resolve() })
      expect(document.querySelector('.rencontre-sur-table')).toBeNull()
      expect(nombre()?.textContent).toMatch(/^1/)
      mesure.mockRestore()
    })

    it('sans carte de boost a lire (scan introuvable) : le nombre se montre, rien n’attend une lecture qui n’aura pas lieu', () => {
      render(
        <DeroulePhase etapes={[attaque]} presentation="table" carteScene={() => undefined} onTerminer={() => {}} />
      )
      expect(nombre()?.textContent).toMatch(/^1/)
    })

    it('une attaque sans boost montre son nombre tout de suite', () => {
      render(
        <DeroulePhase etapes={[{ ...attaque, boosts: [] }]} presentation="table" carteScene={scan} onTerminer={() => {}} />
      )
      expect(nombre()?.textContent).toMatch(/^1/)
    })
  })

  it('sur la table, Echap demande confirmation avant de tout passer (Q32)', () => {
    const { container } = render(
      <DeroulePhase etapes={etapes} presentation="table" onTerminer={() => {}} />
    )
    act(() => {
      document.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape', bubbles: true }))
    })
    expect(container.querySelector('.tsm-confirmer')).not.toBeNull()
    act(() => {
      document.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape', bubbles: true }))
    })
    expect(container.querySelector('.tsm-confirmer')).toBeNull()
  })

  it('« Suivant (espace) » valide l etape, comme l ancien « Suivant »', () => {
    render(<DeroulePhase etapes={etapes} onTerminer={() => {}} />)
    fireEvent.click(screen.getByRole('button', { name: 'Suivant (espace)' }))
    expect(document.querySelector('.deroule-corps')?.getAttribute('aria-label')).toBe('Ultron attaque Shuri')
  })

  it('se deplace par son fond, et revient au milieu a la phase suivante (D2)', () => {
    const cartouche = (identitePhase: number) => (
      <DeroulePhase etapes={etapes} identitePhase={identitePhase} phaseMechantEnCours onTerminer={() => {}} />
    )
    const { container, rerender } = render(cartouche(1))
    const section = () => container.querySelector<HTMLElement>('.deroule-phase.est-scene')
    const poignee = container.querySelector<HTMLElement>('.deroule-phase.est-scene.poignee-glisser')
    expect(poignee).not.toBeNull()
    const pointeur = (type: string, x: number, y: number) =>
      new MouseEvent(type, { bubbles: true, clientX: x, clientY: y, button: 0 })
    act(() => {
      poignee?.dispatchEvent(pointeur('pointerdown', 100, 100))
    })
    act(() => {
      poignee?.dispatchEvent(pointeur('pointermove', 160, 60))
    })
    act(() => {
      window.dispatchEvent(pointeur('pointerup', 160, 60))
    })
    expect(section()?.style.translate).toBe('60px -40px')
    // La position tient d'une etape a l'autre de la MEME phase.
    fireEvent.click(screen.getByRole('button', { name: 'Suivant (espace)' }))
    expect(section()?.style.translate).toBe('60px -40px')
    rerender(cartouche(2))
    expect(section()?.style.translate).toBe('')
  })

  it('Espace valide l etape tout de suite : plus de page imposee (revirement du 05/10/2026)', () => {
    const longue: EtapeDeroule = {
      cle: 'rev',
      temps: 'revelation',
      titre: 'revelation',
      regle: '',
      carteId: 88,
      cibleNom: 'Explosion',
      effets: [1, 2, 3, 4, 5].map((n) => ({ genre: 'degats' as const, cible: `Cible ${n}`, cible_id: 100 + n, montant: 1 })),
      boosts: [],
    }
    const suivante: EtapeDeroule = { ...longue, cle: 'rev2', cibleNom: 'Charge', effets: [] }
    const onEtapeAffichee = vi.fn()
    render(
      <DeroulePhase
        etapes={[longue, suivante]}
        phaseMechantEnCours
        onEtapeAffichee={onEtapeAffichee}
        onTerminer={() => {}}
      />
    )
    traverserLesVides()
    expect(onEtapeAffichee).toHaveBeenLastCalledWith('rev')
    expect(document.querySelector('.deroule-page')).toBeNull()
    fireEvent.keyDown(document, { key: ' ' })
    expect(onEtapeAffichee).toHaveBeenLastCalledWith('rev2')
  })

  it('ne pose plus body.deroule-question, et ne cache plus la main (revirement du 05/10/2026)', () => {
    render(
      <DeroulePhase
        etapes={etapes}
        phaseMechantEnCours
        questionAuJoueur
        question={<button type="button">Défendre</button>}
        onTerminer={() => {}}
      />
    )
    expect(document.body.classList.contains('deroule-question')).toBe(false)
    expect(document.body.classList.contains('cartouche-scene')).toBe(false)
  })
})

// ------------------------------------------------------------------ LOT 4 --
// LE CLAVIER DES QUESTIONS (D37) : 1 a 9 cliquent le choix qui porte ce
// numero, Echap le refus. Les gardes d'avant passent D'ABORD : un champ de
// saisie, un bouton exterieur au cartouche, une fenetre ouverte par-dessus
// (volet du journal, confirmation) gardent la touche. Entree et Espace restent
// inertes pendant une question : ils ne valident rien a sa place.
describe('le clavier des questions du cartouche du bas (D37)', () => {
  const option = (id: number, name: string, bind_id: number, extra: Partial<Option> = {}): Option => ({
    id,
    name,
    bind_id,
    bind_player_id: 0,
    all_legal_targets: [50],
    target_num_range: [1, 1],
    target_payment: {},
    select_rule: '',
    target_must_include_traits: [],
    failure_reason: '',
    is_search: false,
    ...extra,
  })
  const defenseShuri = option(1, 'Defense', 12)
  const defenseAllie = option(2, 'Defense', 13)
  const demande: Demande = {
    options: [defenseShuri, defenseAllie],
    refus: [],
    prompt_text: '',
    event_name: 'WhenUnitBeingAttack',
    show_cancel: true,
    ability_type: 'Interrupt',
  }
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
  function question(): QuestionDuMoteur {
    const interaction = {
      cibles: [],
      ressources: [],
      options: demande.options,
      cartes: new Map(),
      ciblesHorsTable: [],
      raison: '',
      prete: false,
      coutAffiche: '',
      surpaiementRecompense: false,
      ciblesRestantes: 0,
      assistant: {
        etape: 'action',
        titre: '',
        cibleMinimum: 0,
        cibleMaximum: 0,
        cibleNombre: 0,
        ciblePossibles: 0,
        cibleRepetable: false,
        coutPaye: 0,
        coutSlots: [],
        coutRegles: [],
      },
      defocaliser: vi.fn(),
      focaliserCarte: vi.fn(),
      focaliserCible: vi.fn(),
      choisirOption: vi.fn(),
      abandonnerOption: vi.fn(),
      valider: vi.fn(),
      annuler: vi.fn(),
      paiementAutoChoix: 'pas-demande',
      basculerPaiementAuto: vi.fn(),
    } satisfies Interaction
    return {
      demande,
      interaction,
      cartesParId: new Map(),
      choisirOption: vi.fn(),
      survolerOption: vi.fn(),
      nomPorteur: (id) => (id === 12 ? 'Shuri' : id === 13 ? 'Okoye' : undefined),
      texteCapacite: () => undefined,
      estEnMain: () => false,
      carteScene: (id) => ({ id: String(id), name: `c${id}`, kind: 'minion', imageUrl: `/scan/${id}` }),
    }
  }
  function monter(q: QuestionDuMoteur) {
    return render(
      <DeroulePhase etapes={annonce} phaseMechantEnCours questionAuJoueur questionDuMoteur={q} onTerminer={() => {}} />
    )
  }

  afterEach(() => {
    document.querySelectorAll('.volet-journal, .bouton-exterieur').forEach((el) => el.remove())
  })

  it('« 2 » clique le deuxieme choix, « 1 » le premier', () => {
    const q = question()
    monter(q)
    fireEvent.keyDown(document, { key: '2' })
    expect(q.choisirOption).toHaveBeenLastCalledWith(defenseAllie)
    fireEvent.keyDown(document, { key: '1' })
    expect(q.choisirOption).toHaveBeenLastCalledWith(defenseShuri)
  })

  it('un chiffre sans choix ne fait rien', () => {
    const q = question()
    monter(q)
    fireEvent.keyDown(document, { key: '7' })
    fireEvent.keyDown(document, { key: '0' })
    expect(q.choisirOption).not.toHaveBeenCalled()
    expect(q.interaction.annuler).not.toHaveBeenCalled()
  })

  it('Echap clique le refus (« Ne pas défendre »)', () => {
    const q = question()
    monter(q)
    fireEvent.keyDown(document, { key: 'Escape' })
    expect(q.interaction.annuler).toHaveBeenCalledTimes(1)
    expect(q.choisirOption).not.toHaveBeenCalled()
  })

  it('Entree et Espace restent inertes pendant la question', () => {
    const q = question()
    monter(q)
    fireEvent.keyDown(document, { key: 'Enter' })
    fireEvent.keyDown(document, { key: ' ' })
    expect(q.choisirOption).not.toHaveBeenCalled()
    expect(q.interaction.annuler).not.toHaveBeenCalled()
    expect(q.interaction.valider).not.toHaveBeenCalled()
  })

  it('un champ de saisie garde toutes ses touches', () => {
    const q = question()
    monter(q)
    const champ = document.createElement('input')
    champ.className = 'bouton-exterieur'
    document.body.appendChild(champ)
    fireEvent.keyDown(champ, { key: '1' })
    fireEvent.keyDown(champ, { key: 'Escape' })
    expect(q.choisirOption).not.toHaveBeenCalled()
    expect(q.interaction.annuler).not.toHaveBeenCalled()
  })

  it('un bouton du plateau, hors du cartouche, garde ses touches', () => {
    const q = question()
    monter(q)
    const bouton = document.createElement('button')
    bouton.className = 'bouton-exterieur'
    document.body.appendChild(bouton)
    fireEvent.keyDown(bouton, { key: '1' })
    expect(q.choisirOption).not.toHaveBeenCalled()
  })

  it('Echap et les chiffres laissent la main au volet du journal ouvert par-dessus', () => {
    const q = question()
    monter(q)
    const volet = document.createElement('aside')
    volet.className = 'volet-journal'
    document.body.appendChild(volet)
    fireEvent.keyDown(document, { key: 'Escape' })
    fireEvent.keyDown(document, { key: '1' })
    expect(q.interaction.annuler).not.toHaveBeenCalled()
    expect(q.choisirOption).not.toHaveBeenCalled()
  })

  it('la table et le telephone ne gagnent aucune touche', () => {
    const q = question()
    render(
      <DeroulePhase telephone etapes={annonce} phaseMechantEnCours questionAuJoueur questionDuMoteur={q} onTerminer={() => {}} />
    )
    fireEvent.keyDown(document, { key: '1' })
    fireEvent.keyDown(document, { key: 'Escape' })
    expect(q.choisirOption).not.toHaveBeenCalled()
    expect(q.interaction.annuler).not.toHaveBeenCalled()
  })

  it('la loupe s ouvre pendant la question, au survol d une vignette, devant le carre', () => {
    // jsdom n'a pas ResizeObserver : la loupe (usePlacement) observe son panneau.
    vi.stubGlobal('ResizeObserver', class { observe() {} unobserve() {} disconnect() {} })
    monter(question())
    const vignette = document.querySelector('.deroule-vignette [data-card-id="50"]')
    expect(vignette).not.toBeNull()
    fireEvent.mouseOver(vignette as Element)
    expect(document.querySelector('.carte-apercu.au-dessus-du-deroule')).not.toBeNull()
    vi.unstubAllGlobals()
  })

  // LOT 5 (D26, D37) : hors phase, la defense se joue dans « Pendant ton
  // tour ». Le controleur, monte lui aussi (sans etape), lui prete son clavier :
  // les memes chiffres et la meme Echap.
  it('hors phase, les chiffres et Echap jouent la defense de « Pendant ton tour »', () => {
    const q = question()
    render(
      <>
        <DeroulePhase etapes={[]} questionAuJoueur onTerminer={() => {}} />
        <CartoucheHorsPhase coups={[{ ...annonce[0], horsPhase: true }]} questionAuJoueur questionDuMoteur={q} />
      </>
    )
    fireEvent.keyDown(document, { key: '2' })
    expect(q.choisirOption).toHaveBeenLastCalledWith(defenseAllie)
    fireEvent.keyDown(document, { key: 'Escape' })
    expect(q.interaction.annuler).toHaveBeenCalledTimes(1)
  })
})

describe('cle de l etape lue qui disparait (capture du 07/10/2026, Rhino / Assaut)', () => {
  // L'etape du journal (« carte:76 ») arrive avant le fait du moteur, puis le
  // fait la remplace sous une autre cle. Le cartouche lisait par repli sans
  // reprendre la cle, et sa sortie d'attente avancait une fois de trop :
  // « Aucun sbire » -> « Assaut » 25 ms -> « Aucun sbire ».
  const menaceJournal: EtapeDeroule = { cle: 'menace:57', temps: 'menace', titre: 'menace', regle: '', boosts: [] }
  const menace: EtapeDeroule = { cle: 'menace:1', temps: 'menace', titre: 'menace', regle: '', boosts: [] }
  const attaque: EtapeDeroule = { ...etapes[1], cle: 'activation:1' }
  const vide: EtapeDeroule = { cle: 'vide:sbires', temps: 'sbires', titre: 'vide', regle: '', boosts: [] }
  const revelee: EtapeDeroule = { cle: 'carte:76', temps: 'revelation', titre: 'revelation', regle: '', carteId: 70, boosts: [] }

  it('ne saute jamais l etape vide ni ne revient en arriere', () => {
    const vues: (string | undefined)[] = []
    const rendu = (liste: EtapeDeroule[]) => (
      <DeroulePhase etapes={liste} phaseMechantEnCours onTerminer={() => {}} onEtapeAffichee={(c) => vues.push(c)} />
    )
    const { rerender } = render(rendu([menaceJournal]))
    fireEvent.click(suivant())
    // La menace du journal est remplacee par le fait du moteur, sous une autre cle.
    rerender(rendu([menace]))
    fireEvent.click(suivant())
    rerender(rendu([menace, attaque]))
    fireEvent.click(suivant())
    rerender(rendu([menace, attaque, vide, revelee]))
    rerender(rendu([menace, attaque, vide, { ...revelee, cle: 'revelation:1:3:70' }]))
    const apresAttaque = vues.slice(vues.lastIndexOf('activation:1') + 1)
    expect(apresAttaque).toEqual(['vide:sbires'])
  })

  it('la menace validee puis recle par le moteur ne demande pas un second clic', () => {
    const vues: (string | undefined)[] = []
    const rendu = (liste: EtapeDeroule[]) => (
      <DeroulePhase etapes={liste} phaseMechantEnCours onTerminer={() => {}} onEtapeAffichee={(c) => vues.push(c)} />
    )
    const { rerender } = render(rendu([menaceJournal]))
    fireEvent.click(suivant())
    rerender(rendu([menace]))
    rerender(rendu([menace, attaque]))
    expect(vues.at(-1)).toBe('activation:1')
  })

  it('une autre etape a la meme place n est pas prise pour la validee', () => {
    const vues: (string | undefined)[] = []
    const rendu = (liste: EtapeDeroule[]) => (
      <DeroulePhase etapes={liste} phaseMechantEnCours onTerminer={() => {}} onEtapeAffichee={(c) => vues.push(c)} />
    )
    const { rerender } = render(rendu([menaceJournal]))
    fireEvent.click(suivant())
    rerender(rendu([{ ...menace, cibleId: 99 }]))
    rerender(rendu([{ ...menace, cibleId: 99 }, attaque]))
    expect(vues.at(-1)).toBe('menace:1')
  })
})

describe('bilan referme : publie au spectateur et a la relecture', () => {
  afterEach(() => {
    window.history.replaceState(null, '', '/')
    vi.unstubAllGlobals()
  })

  it('le joueur qui valide le bilan publie une etape vide', () => {
    const vues: (string | undefined)[] = []
    render(
      <DeroulePhase
        etapes={etapes}
        identitePhase={4}
        phaseMechantEnCours={false}
        onTerminer={() => {}}
        onEtapeAffichee={(c) => vues.push(c)}
      />
    )
    const bilan = /^(Terminer|À toi de jouer)$/i
    for (let garde = 0; garde < 12 && !screen.queryByRole('button', { name: bilan }); garde++) {
      fireEvent.click(screen.getByRole('button', { name: /Suivant/i }))
    }
    expect(vues.at(-1)).toBeDefined()
    fireEvent.click(screen.getByRole('button', { name: bilan }))
    expect(vues.at(-1)).toBeUndefined()
  })

  it('le spectateur cache le bilan quand le joueur l a referme, pas avant', async () => {
    window.history.replaceState(null, '', '/?spectateur=1')
    let publie: Record<string, { cle: string; t: number; mode: string }> = { 0: { cle: 'bilan', t: 1, mode: '' } }
    vi.stubGlobal('fetch', vi.fn(async () => ({ ok: true, json: async () => publie })))
    vi.useFakeTimers()
    try {
      const { container } = render(
        <DeroulePhase etapes={etapes} identitePhase={4} phaseMechantEnCours={false} onTerminer={() => {}} />
      )
      await act(async () => {
        await vi.advanceTimersByTimeAsync(50)
      })
      expect(container).not.toBeEmptyDOMElement()
      publie = { 0: { cle: '', t: 2, mode: '' } }
      await act(async () => {
        await vi.advanceTimersByTimeAsync(800)
      })
      expect(container).toBeEmptyDOMElement()
    } finally {
      vi.useRealTimers()
    }
  })
})

// REFONTE, LOT 4 (essai, 12/10/2026, decision 51) : tant que l'attaque retourne
// ses boosts, la table doit garder le monde d'avant l'etape.
describe('lot 4 : l ecran du resultat se signale a la table', () => {
  const avecBoosts: EtapeDeroule[] = [
    {
      cle: 'atk',
      temps: 'mechant',
      titre: 'attaque',
      regle: 'regle:activations',
      etat: 'resolu',
      carteId: 50,
      cibleId: 12,
      auteurNom: 'Ultron',
      cibleNom: 'Shuri',
      base: 2,
      montant: 4,
      restant: 6,
      boosts: [
        { cle: 'b1', nom: 'Assaut', cibleId: 70, apport: 1 },
        { cle: 'b2', nom: 'Avancée', cibleId: 71, apport: 1 },
      ],
    },
  ]

  it('dans l essai : vrai pendant les boosts, faux a l ecran du resultat', () => {
    const vus: boolean[] = []
    render(<DeroulePhase etapes={avecBoosts} essai onTerminer={() => {}} onAvantResultat={(v) => vus.push(v)} />)
    expect(vus.at(-1)).toBe(true)
    act(() => document.querySelector<HTMLButtonElement>('.deroule-suivant')?.click())
    expect(vus.at(-1)).toBe(false)
  })

  // Demande de l'utilisateur (13/10/2026) : « quand il y a plusieurs cartes boost,
  // comme pour Klaw, j'aimerais bien que les deux s'affichent en même temps ».
  it('dans l essai : les deux boosts arrivent caches, UN clic les retourne ensemble', () => {
    render(<DeroulePhase etapes={avecBoosts} essai onTerminer={() => {}} />)
    expect(document.querySelector('button[data-boost-suivant]')).not.toBeNull()
    act(() => document.querySelector<HTMLButtonElement>('button[data-boost-suivant]')?.click())
    expect(document.querySelector('button[data-boost-suivant]')).toBeNull()
  })

  it('sans l interrupteur : toujours faux, la table calee reste celle d avant le lot 4', () => {
    const vus: boolean[] = []
    render(<DeroulePhase etapes={avecBoosts} onTerminer={() => {}} onAvantResultat={(v) => vus.push(v)} />)
    expect(vus.every((v) => v === false)).toBe(true)
  })
})

// « Phase du méchant automatique » : Non / 2 s / 5 s (réglage personnel, demande du 23/10/2026).
describe('cartouche du deroule : phase du mechant automatique', () => {
  beforeEach(() => {
    window.localStorage.clear()
    vi.useFakeTimers()
  })
  afterEach(() => {
    vi.useRealTimers()
    window.localStorage.clear()
  })

  it('par defaut (Non) : l etape attend le clic, meme apres 10 s', () => {
    render(<DeroulePhase etapes={etapes} onTerminer={() => {}} />)
    act(() => {
      vi.advanceTimersByTime(10000)
    })
    expect(etapeLue()).toBe('Menace sur la manigance principale')
  })

  it('2 s : l etape suivante s affiche toute seule apres 2 s, pas avant', () => {
    window.localStorage.setItem('marvel-board-phase-auto', '2000')
    render(<DeroulePhase etapes={etapes} onTerminer={() => {}} />)
    act(() => {
      vi.advanceTimersByTime(1900)
    })
    expect(etapeLue()).toBe('Menace sur la manigance principale')
    act(() => {
      vi.advanceTimersByTime(200)
    })
    expect(etapeLue()).toBe('Ultron attaque Shuri')
  })

  it('5 s : rien a 4 s, l etape suivante a 5 s', () => {
    window.localStorage.setItem('marvel-board-phase-auto', '5000')
    render(<DeroulePhase etapes={etapes} onTerminer={() => {}} />)
    act(() => {
      vi.advanceTimersByTime(4000)
    })
    expect(etapeLue()).toBe('Menace sur la manigance principale')
    act(() => {
      vi.advanceTimersByTime(1100)
    })
    expect(etapeLue()).toBe('Ultron attaque Shuri')
  })

  it('le reglage change en cours de phase : pris en compte tout de suite', () => {
    render(<DeroulePhase etapes={etapes} onTerminer={() => {}} />)
    act(() => {
      ecrireDelaiAutoPhase(2000)
    })
    act(() => {
      vi.advanceTimersByTime(2100)
    })
    expect(etapeLue()).toBe('Ultron attaque Shuri')
  })
})

