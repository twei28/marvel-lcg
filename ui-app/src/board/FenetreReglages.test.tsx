// La fenetre des reglages : ce qu'elle range, et ce qu'elle ne cache pas.
//
// ⚠ LE CAS QUI COMPTE LE PLUS est `un sous-reglage inutilisable reste VISIBLE`.
// C'est le defaut que l'utilisateur a decrit le 14/09/2026 : on ne peut pas
// savoir qu'un reglage existe s'il n'apparait qu'une fois son parent active.
// Les autres cas verifient surtout qu'aucun reglage n'a ete perdu en chemin :
// c'est un rangement, pas une refonte.
import { fireEvent, render, screen, within } from '@testing-library/react'
import { describe, expect, it, vi } from 'vitest'
import { ContenuOnglet, FenetreReglages, ONGLETS, type ProprietesReglages } from './FenetreReglages'

function proprietes(sur: Partial<ProprietesReglages> = {}): ProprietesReglages {
  return {
    animations: true,
    basculerAnimations: vi.fn(),
    sons: true,
    basculerSons: vi.fn(),
    musique: false,
    basculerMusique: vi.fn(),
    succes: true,
    basculerSucces: vi.fn(),
    scansFr: true,
    basculerScansFr: vi.fn(),
    textesCdb: false,
    basculerTextesCdb: vi.fn(),
    basculerLangue: vi.fn(),

    // Essais fermes par defaut, comme pour presque tout le monde : le mode
    // « Sur la table » ne doit alors pas etre propose.
    essais: false,
    modePhase: 'detaille',
    changerModePhase: vi.fn(),
    libelleModePhase: (m) =>
      m === 'detaille' ? 'Détaillé' : m === 'sur-table' ? 'Sur la table' : 'Instantané',
    tempsParDecision: 0,
    texteTempsParDecision: () => 'le moteur n’attend pas',
    avanceAuto: false,
    basculerAvanceAuto: vi.fn(),
    delaiPasAPas: 1200,
    reglerDelaiPasAPas: vi.fn(),
    validationCourte: false,
    basculerValidationCourte: vi.fn(),
    autoCible: true,
    basculerAutoCible: vi.fn(),
    revelation: 'court',
    cyclerRevelation: vi.fn(),

    meteo: true,
    basculerMeteo: vi.fn(),
    apercuMeteo: undefined,
    reglerApercuMeteo: vi.fn(),
    reponseAmbiance: 'demander',
    cyclerReponseAmbiance: vi.fn(),

    designEssai: true,
    basculerDesignEssai: vi.fn(),
    modeActions: 'simple',
    changerModeActions: vi.fn(),
    curseurs: false,
    basculerCurseurs: vi.fn(),
    montrerDisposition: false,
    reglageMode: 'auto',
    cyclerReglageMode: vi.fn(),
    ...sur,
  }
}

function ligne(libelle: string) {
  return screen.getByText(libelle).closest('.ligne-option') as HTMLElement
}

describe('un sous-reglage inutilisable reste VISIBLE', () => {
  // ⚠ Le coeur du changement. Avant, « Vitesse du deroule » n'existait dans le
  // DOM que si « Avance toute seule » etait active : impossible de savoir
  // qu'elle existait. Maintenant elle est la, grisee.
  it('« Vitesse du deroule » est affichee meme quand l’avance auto est coupee', () => {
    render(<ContenuOnglet onglet="deroule" p={proprietes({ avanceAuto: false })} />)
    const curseur = ligne('Vitesse du déroulé')
    expect(curseur).toBeTruthy()
    expect(curseur.className).toContain('est-desactive')
    expect(within(curseur).getByRole('slider')).toBeDisabled()
  })

  it('et elle devient utilisable des que l’avance auto est allumee', () => {
    render(<ContenuOnglet onglet="deroule" p={proprietes({ avanceAuto: true })} />)
    const curseur = ligne('Vitesse du déroulé')
    expect(curseur.className).not.toContain('est-desactive')
    expect(within(curseur).getByRole('slider')).not.toBeDisabled()
  })

  it('« Avance toute seule » est visible mais inerte en phase instantanee', () => {
    // Elle ne veut rien dire hors du mode detaille, mais la cacher reviendrait
    // a faire croire qu'elle n'existe pas.
    render(<ContenuOnglet onglet="deroule" p={proprietes({ modePhase: 'instantane' })} />)
    const bascule = ligne('Avance toute seule')
    expect(bascule).toBeTruthy()
    expect(bascule).toBeDisabled()
  })

  it('« Actions » est visible mais inerte sans le nouveau design', () => {
    render(<ContenuOnglet onglet="avance" p={proprietes({ designEssai: false })} />)
    const choix = ligne('Actions')
    expect(choix.className).toContain('est-desactive')
    for (const bouton of within(choix).getAllByRole('button')) expect(bouton).toBeDisabled()
  })

  it('un sous-reglage porte le retrait, son parent non', () => {
    render(<ContenuOnglet onglet="deroule" p={proprietes()} />)
    expect(ligne('Avance toute seule').className).toContain('est-enfant')
    expect(ligne('Validation courte').className).not.toContain('est-enfant')
  })
})

describe('aucun reglage n’a ete perdu au rangement', () => {
  // Les 18 reglages de l'ancien panneau, avec l'onglet ou chacun doit se
  // trouver. Un reglage qui disparaitrait d'un onglet sans reapparaitre
  // ailleurs ferait rougir ce test.
  const ATTENDUS: Record<string, string[]> = {
    image: [
      'Animations',
      'Sons',
      'Musique',
      'Succès',
      'Scans en français',
      'Textes marvelcdb (réseau)',
      'Langue',
    ],
    deroule: [
      'Phase du méchant',
      'Avance toute seule',
      'Vitesse du déroulé',
      'Validation courte',
      'Auto-ciblage',
      'Cartes révélées',
    ],
    ambiance: ['Ambiance', 'Aperçu d’ambiance'],
    avance: ['Nouveau design', 'Actions', 'Curseurs des autres joueurs'],
  }

  for (const [onglet, libelles] of Object.entries(ATTENDUS)) {
    it(`l’onglet ${onglet} porte ses ${libelles.length} reglages`, () => {
      render(<ContenuOnglet onglet={onglet as (typeof ONGLETS)[number]} p={proprietes()} />)
      for (const libelle of libelles) expect(screen.getByText(libelle)).toBeTruthy()
    })
  }

  it('« Disposition » n’apparait QUE sur un appareil mobile', () => {
    // Sur un PC le plateau est de toute facon rendu en mode PC : le reglage
    // n'aurait aucun effet, et c'est lui qui a un jour enferme l'utilisateur.
    const { unmount } = render(
      <ContenuOnglet onglet="avance" p={proprietes({ montrerDisposition: false })} />
    )
    expect(screen.queryByText('Disposition')).toBeNull()
    unmount()
    render(<ContenuOnglet onglet="avance" p={proprietes({ montrerDisposition: true })} />)
    expect(screen.getByText('Disposition')).toBeTruthy()
  })

  it('la note du « temps par decision » ne sort qu’en phase detaillee et si le moteur en a un', () => {
    const { unmount } = render(
      <ContenuOnglet onglet="deroule" p={proprietes({ modePhase: 'detaille', tempsParDecision: 0 })} />
    )
    expect(screen.queryByText(/n’attend pas/)).toBeNull()
    unmount()
    render(
      <ContenuOnglet onglet="deroule" p={proprietes({ modePhase: 'detaille', tempsParDecision: 30 })} />
    )
    expect(screen.getByText(/n’attend pas/)).toBeTruthy()
  })
})

describe('chaque interrupteur appelle bien sa fonction', () => {
  it('basculer les animations', () => {
    const basculerAnimations = vi.fn()
    render(<ContenuOnglet onglet="image" p={proprietes({ basculerAnimations })} />)
    fireEvent.click(screen.getByText('Animations'))
    expect(basculerAnimations).toHaveBeenCalledTimes(1)
  })

  it('choisir la phase instantanee', () => {
    const changerModePhase = vi.fn()
    render(<ContenuOnglet onglet="deroule" p={proprietes({ changerModePhase })} />)
    fireEvent.click(screen.getByText('Instantané'))
    expect(changerModePhase).toHaveBeenCalledWith('instantane')
  })

  it('rechoisir la valeur deja active ne declenche rien', () => {
    // Sans quoi cliquer « Détaillé » alors qu'on y est ferait un aller-retour
    // inutile, visible a l'ecran sur les reglages qui se cyclent.
    const cyclerReglageMode = vi.fn()
    render(
      <ContenuOnglet
        onglet="avance"
        p={proprietes({ montrerDisposition: true, reglageMode: 'auto', cyclerReglageMode })}
      />
    )
    fireEvent.click(screen.getByText('Automatique'))
    expect(cyclerReglageMode).not.toHaveBeenCalled()
    fireEvent.click(screen.getByText('Ordinateur'))
    expect(cyclerReglageMode).toHaveBeenCalledTimes(1)
  })

  it('« Cartes revelees » atteint la valeur demandee en cyclant', () => {
    // Le moteur ne sait que cycler : off -> court -> long -> off. La fenetre
    // offre pourtant trois pastilles, donc elle cycle autant de fois qu'il
    // faut. Depuis « court », atteindre « off » demande deux pas.
    const cyclerRevelation = vi.fn()
    render(<ContenuOnglet onglet="deroule" p={proprietes({ revelation: 'court', cyclerRevelation })} />)
    // ⚠ Chercher DANS la ligne : « Non » est aussi l'etat affiche par chaque
    // interrupteur coupe de l'onglet, un `getByText` global en trouve plusieurs.
    const cartes = within(ligne('Cartes révélées'))
    fireEvent.click(cartes.getByText('5 s'))
    expect(cyclerRevelation).toHaveBeenCalledTimes(1)
    cyclerRevelation.mockClear()
    fireEvent.click(cartes.getByText('Non'))
    expect(cyclerRevelation).toHaveBeenCalledTimes(2)
  })
})

describe('la fenetre elle-meme', () => {
  it('ne rend rien tant qu’elle est fermee', () => {
    const { container } = render(
      <FenetreReglages ouvert={false} fermer={vi.fn()} {...proprietes()} />
    )
    expect(container.querySelector('.reglages-fenetre')).toBeNull()
  })

  it('ouvre sur l’onglet « Image et son », et on peut changer d’onglet', () => {
    render(<FenetreReglages ouvert fermer={vi.fn()} {...proprietes()} />)
    expect(screen.getByText('Animations')).toBeTruthy()
    fireEvent.click(screen.getByRole('tab', { name: 'Ambiance' }))
    expect(screen.getByText('Aperçu d’ambiance')).toBeTruthy()
    expect(screen.queryByText('Animations')).toBeNull()
  })

  it('affiche les quatre onglets, et un seul est selectionne', () => {
    render(<FenetreReglages ouvert fermer={vi.fn()} {...proprietes()} />)
    const onglets = screen.getAllByRole('tab')
    expect(onglets).toHaveLength(4)
    expect(onglets.filter((o) => o.getAttribute('aria-selected') === 'true')).toHaveLength(1)
  })

  it('se ferme par la croix, par Echap et par le fond', () => {
    // ⚠ Trois sorties, et c'est voulu : une fenetre qu'on ne ferme que par un
    // bouton precis est une fenetre dont on se sent prisonnier, exactement le
    // reproche fait a l'ancien empilement de menus.
    const fermer = vi.fn()
    const { container } = render(<FenetreReglages ouvert fermer={fermer} {...proprietes()} />)

    fireEvent.click(screen.getByTitle('Fermer'))
    expect(fermer).toHaveBeenCalledTimes(1)

    fireEvent.keyDown(document, { key: 'Escape' })
    expect(fermer).toHaveBeenCalledTimes(2)

    fireEvent.click(container.querySelector('.reglages-fond') as HTMLElement)
    expect(fermer).toHaveBeenCalledTimes(3)
  })

  it('un clic DANS la fenetre ne la ferme pas', () => {
    const fermer = vi.fn()
    const { container } = render(<FenetreReglages ouvert fermer={fermer} {...proprietes()} />)
    fireEvent.click(container.querySelector('.reglages-fenetre') as HTMLElement)
    expect(fermer).not.toHaveBeenCalled()
  })

  it('Echap ne ferme plus rien une fois la fenetre demontee', () => {
    // Un ecouteur clavier laisse en place capterait les raccourcis du plateau
    // (E = fin du tour, U = annuler) longtemps apres la fermeture.
    const fermer = vi.fn()
    const { unmount } = render(<FenetreReglages ouvert fermer={fermer} {...proprietes()} />)
    unmount()
    fireEvent.keyDown(document, { key: 'Escape' })
    expect(fermer).not.toHaveBeenCalled()
  })
})

describe('le mode « Sur la table » n’est proposé qu’aux essais', () => {
  const modes = () =>
    within(screen.getByText('Phase du méchant').closest('.ligne-option') as HTMLElement)
      .getAllByRole('button')
      .map((b) => b.textContent)

  it('sans les essais, deux modes seulement', () => {
    render(<ContenuOnglet onglet="deroule" p={proprietes({ essais: false })} />)
    expect(modes()).toEqual(['Détaillé', 'Instantané'])
  })

  it('avec les essais, le troisième apparaît entre les deux', () => {
    // Il raconte la même chose que « Détaillé », au même rythme : sa place est
    // à côté de lui, pas à la fin de la liste.
    render(<ContenuOnglet onglet="deroule" p={proprietes({ essais: true })} />)
    expect(modes()).toEqual(['Détaillé', 'Sur la table', 'Instantané'])
  })

  it('⚠ un mode DÉJÀ choisi reste dans la liste même sans les essais', () => {
    // Sinon l'écran des réglages montrerait trois... non, DEUX boutons dont
    // aucun n’est actif, et le joueur n’aurait aucun moyen d’en sortir : le
    // mode resterait actif sans être visible nulle part.
    render(<ContenuOnglet onglet="deroule" p={proprietes({ essais: false, modePhase: 'sur-table' })} />)
    expect(modes()).toEqual(['Détaillé', 'Sur la table', 'Instantané'])
  })
})
